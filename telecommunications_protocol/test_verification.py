"""Regression tests for evidence integrity; these do not rerun the SAT solver."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock
import xml.etree.ElementTree as ET

import export_instances
import verify


LEGACY = Path(__file__).resolve().parent / "results" / "run-20261103-152340-96e1de"


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.results = self.root / "results"
        self.results.mkdir()
        self.run = self.results / "run-fixture"
        shutil.copytree(LEGACY, self.run)
        self.live = self.root / "telecommunications.als"
        shutil.copy2(self.run / "telecommunications.als", self.live)
        self.patches = [mock.patch.object(verify, "RESULTS", self.results),
                        mock.patch.object(verify, "MODEL", self.live)]
        for patch in self.patches:
            patch.start()

    def tearDown(self):
        for patch in reversed(self.patches):
            patch.stop()
        self.temp.cleanup()

    def summary(self):
        return (self.results / "verification_summary.md").read_text(encoding="utf-8")

    def edit_json(self, name, edit):
        path = self.run / name
        data = json.loads(path.read_text(encoding="utf-8"))
        edit(data)
        path.write_text(json.dumps(data), encoding="utf-8")

    def test_real_saved_evidence_passes_with_terminal_backspaces(self):
        log = (self.run / "analyzer.log").read_text(encoding="utf-8")
        self.assertIn("\b", log)
        self.assertEqual(len(verify.OUTCOME.findall(log)), 18)
        self.assertTrue(verify.summarize(self.run))
        self.assertIn("| 6 |", (self.results / "example_instances.md").read_text(encoding="utf-8"))

    def test_live_edit_cannot_relabel_old_evidence(self):
        old_hash = verify.sha256(self.live)
        self.live.write_text(self.live.read_text(encoding="utf-8") + "\n// changed live model\n", encoding="utf-8")
        self.assertTrue(verify.summarize(self.run))
        self.assertIn(old_hash, self.summary())
        self.assertIn("no; results apply only to the saved source", self.summary())
        self.assertNotIn(verify.sha256(self.live), self.summary())

    def test_modified_saved_source_fails_hash_validation(self):
        source = self.run / "telecommunications.als"
        source.write_text(source.read_text(encoding="utf-8") + "\n// altered snapshot\n", encoding="utf-8")
        self.assertFalse(verify.summarize(self.run))
        self.assertIn("source hash does not match", self.summary())

    def test_interrupted_execution_replaces_previous_example_claim(self):
        self.assertTrue(verify.summarize(self.run))
        self.edit_json("execution.json", lambda data: data.update(status="interrupted", process_exit_code=-15))
        self.assertFalse(verify.summarize(self.run))
        self.assertIn("unavailable", (self.results / "example_instances.md").read_text(encoding="utf-8"))

    def test_duplicate_log_outcome_fails(self):
        path = self.run / "analyzer.log"
        path.write_text(path.read_text(encoding="utf-8") + "\n00. check InitialIsValid 0 UNSAT\n", encoding="utf-8")
        self.assertFalse(verify.summarize(self.run))
        self.assertIn("Duplicate outcome", self.summary())

    def test_missing_log_outcome_fails(self):
        path = self.run / "analyzer.log"
        lines = path.read_text(encoding="utf-8").splitlines()
        path.write_text("\n".join(line for line in lines if "check InitialIsValid" not in line), encoding="utf-8")
        self.assertFalse(verify.summarize(self.run))
        self.assertIn("NOT COMPLETED", self.summary())

    def test_receipt_scope_mismatch_fails(self):
        self.edit_json("receipt.json", lambda data: data["commands"]["InitialIsValid"].update(
            source="check InitialIsValid for 1 but exactly 1 State, 5 Int, 4 seq"))
        self.assertFalse(verify.summarize(self.run))
        self.assertIn("receipt command or scope differs", self.summary())

    def test_sat_requires_saved_witness(self):
        (self.run / "ShowTransmit-solution-0.xml").unlink()
        self.assertFalse(verify.summarize(self.run))
        self.assertIn("SAT result has no saved XML witness", self.summary())

    def xml_path(self):
        return self.run / "ShowTwoMessageDelivery-solution-0.xml"

    def test_gapped_sequence_is_rejected_instead_of_compressed(self):
        path = self.xml_path()
        tree = ET.parse(path)
        row = tree.find(".//field[@label='route']/tuple")
        state = row.findall("atom")[0].get("label")
        row.findall("atom")[1].set("label", "3")
        tree.write(path, encoding="utf-8")
        instance = export_instances.Instance(path)
        with self.assertRaisesRegex(ValueError, "sequence index"):
            instance.sequence("route", state)

    def test_nonfunctional_sequence_is_rejected(self):
        path = self.xml_path()
        tree = ET.parse(path)
        field = tree.find(".//field[@label='route']")
        row = field.find("tuple")
        state = row.findall("atom")[0].get("label")
        field.append(ET.fromstring(ET.tostring(row)))
        tree.write(path, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "sequence index"):
            export_instances.Instance(path).sequence("route", state)

    def test_missing_xml_field_is_rejected(self):
        path = self.xml_path()
        tree = ET.parse(path)
        instance = tree.find("instance")
        instance.remove(instance.find("field[@label='ins']"))
        tree.write(path, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "missing"):
            export_instances.Instance(path)

    def test_missing_demonstration_does_not_silently_reuse_old_report(self):
        (self.run / "ShowTwoMessageDelivery-solution-0.xml").unlink()
        with self.assertRaisesRegex(ValueError, "required"):
            export_instances.export(self.run)

    def main_fixture(self, popen):
        jar = self.root / "alloy.jar"
        jar.write_bytes(b"test fixture, never executed")
        with mock.patch.object(verify, "JAR", jar), mock.patch.object(verify, "ROOT", self.root), \
             mock.patch.object(verify.shutil, "which", return_value="java"), \
             mock.patch.object(verify.subprocess, "run", return_value=SimpleNamespace(stdout="6.2.0\n", stderr="java fixture")), \
             mock.patch.object(verify.subprocess, "Popen", side_effect=popen), \
             mock.patch.object(verify.sys, "argv", ["verify.py"]), contextlib.redirect_stdout(io.StringIO()):
            result = verify.main()
        created = [path for path in self.results.glob("run-*") if path != self.run]
        self.assertEqual(len(created), 1)
        return result, created[0]

    def test_startup_failure_records_snapshot_and_failed_status(self):
        def fail(*args, **kwargs):
            raise OSError("simulated launch failure")
        result, run = self.main_fixture(fail)
        metadata = json.loads((run / "execution.json").read_text(encoding="utf-8"))
        self.assertEqual(result, 1)
        self.assertEqual(metadata["status"], "failed")
        self.assertEqual(metadata["model_sha256"], verify.sha256(run / "telecommunications.als"))
        self.assertIn("INCOMPLETE OR FAILED", self.summary())
        self.assertTrue((run / "analyzer.log").is_file())

    def test_interrupt_saves_log_and_stops_child(self):
        class Process:
            returncode = None
            terminated = False
            @property
            def stdout(self):
                def stream():
                    yield "00. check InitialIsValid 0 UNSAT\n"
                    raise KeyboardInterrupt
                return stream()
            def poll(self):
                return self.returncode
            def terminate(self):
                self.terminated = True
                self.returncode = -15
            def wait(self, timeout=None):
                return self.returncode
        process = Process()
        result, run = self.main_fixture(lambda *args, **kwargs: process)
        metadata = json.loads((run / "execution.json").read_text(encoding="utf-8"))
        self.assertEqual(result, 1)
        self.assertTrue(process.terminated)
        self.assertEqual(metadata["status"], "interrupted")
        self.assertIn("InitialIsValid", (run / "analyzer.log").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
