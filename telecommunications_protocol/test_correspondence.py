"""Evidence-integrity regressions for the correspondence runner; no SAT reruns."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest

import check_correspondence as runner

FIXTURE = Path(__file__).resolve().parent / "scale-results" / "correspondence-20261107-234959-f1e1a2"


class CorrespondenceEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.suite = Path(self.temp.name)
        shutil.copytree(FIXTURE / "sources", self.suite / "sources")
        for name in ("InitialStatesCorrespond", "ShowCorrespondingTransmit"):
            shutil.copytree(FIXTURE / name, self.suite / name)
        self.run = self.suite / "InitialStatesCorrespond"
        self.metadata = json.loads((self.run / "execution.json").read_text(encoding="utf-8"))

    def tearDown(self):
        self.temp.cleanup()

    def edit_receipt(self, edit):
        path = self.run / "alloy" / "receipt.json"
        receipt = json.loads(path.read_text(encoding="utf-8"))
        edit(receipt)
        path.write_text(json.dumps(receipt), encoding="utf-8")

    def test_real_frozen_evidence_passes(self):
        self.assertTrue(runner.validate(self.run, self.metadata)["validated"])

    def test_timeout_cannot_reuse_a_previous_unsat_receipt(self):
        self.metadata.update(status="timed_out", process_exit_code=-1)
        result = runner.validate(self.run, self.metadata)
        self.assertFalse(result["validated"])
        self.assertIsNone(result["observed"])

    def test_changed_imported_model_invalidates_evidence(self):
        dependency = self.suite / "sources" / "telecommunications_scalable.als"
        dependency.write_bytes(dependency.read_bytes() + b"\n// edited after execution\n")
        result = runner.validate(self.run, self.metadata)
        self.assertFalse(result["validated"])
        self.assertTrue(any("Frozen source hash differs" in error for error in result["errors"]))

    def test_receipt_command_scope_must_match_frozen_source(self):
        self.edit_receipt(lambda receipt: receipt["commands"][self.metadata["command"]].update(
            source=self.metadata["declaration"]["source"].replace("6 Int", "5 Int")))
        self.assertFalse(runner.validate(self.run, self.metadata)["validated"])

    def test_numeric_receipt_scope_must_match_command_text(self):
        self.edit_receipt(lambda receipt: receipt["commands"][self.metadata["command"]].update(bitwidth=5))
        self.assertFalse(runner.validate(self.run, self.metadata)["validated"])

    def test_missing_log_outcome_cannot_be_inferred_from_receipt(self):
        (self.run / "analyzer.log").write_text("incomplete output\n", encoding="utf-8")
        self.assertFalse(runner.validate(self.run, self.metadata)["validated"])

    def test_sat_requires_saved_xml(self):
        run = self.suite / "ShowCorrespondingTransmit"
        metadata = json.loads((run / "execution.json").read_text(encoding="utf-8"))
        self.assertTrue(runner.validate(run, metadata)["validated"])
        (run / "alloy" / "ShowCorrespondingTransmit-solution-0.xml").unlink()
        self.assertFalse(runner.validate(run, metadata)["validated"])

    def test_duplicate_results_do_not_satisfy_full_suite(self):
        metadata = json.loads((FIXTURE / "suite.json").read_text(encoding="utf-8"))
        metadata["results"][1] = metadata["results"][0]
        runner.summarize(self.suite, metadata)
        self.assertFalse(metadata["all_expectations_validated"])


if __name__ == "__main__":
    unittest.main()
