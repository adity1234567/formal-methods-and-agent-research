"""Evidence and resource-limit regressions; no SAT solver is launched."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock
import xml.etree.ElementTree as ET

import scale_verify as scale


class ScalingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = scale.MODEL.read_text(encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def fixture(self):
        generated, details = scale.generate(self.source, "RetrieveIsValid", 6, 4)
        original = self.root / "original-model.als"
        original.write_bytes(scale.MODEL.read_bytes())
        run = self.root / "run"
        run.mkdir()
        model = run / "telecommunications.als"
        model.write_text(generated, encoding="utf-8", newline="\n")
        alloy = run / "alloy"
        alloy.mkdir()
        metadata = {**details, "status": "completed", "process_exit_code": 0, "solver": "sat4j",
                    "no_overflow": True, "original_source_file": "../original-model.als",
                    "original_sha256": scale.digest(original), "model_sha256": scale.digest(model)}
        receipt = {"solver": "sat4j", "noOverflow": True, "commands": {"RetrieveIsValid": {
            "name": "RetrieveIsValid", "type": "check", "source": details["command_source"],
            "bitwidth": details["integer_bitwidth"], "maxseq": details["sequence_bound"]}}}
        (alloy / "receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
        (run / "analyzer.log").write_text("00. check RetrieveIsValid 0 UNSAT\n", encoding="utf-8")
        return run, metadata, receipt

    def test_generated_scope_keeps_message_bound_and_has_one_command(self):
        generated, details = scale.generate(self.source, "RetrieveIsValid", 8, 4)
        commands = scale.verify.declarations(generated)
        self.assertEqual(len(commands), 1)
        self.assertIn("8 SPC, 4 Message", commands[0]["source"])
        self.assertEqual(details["sequence_bound"], 8)
        self.assertGreaterEqual(2 ** (details["integer_bitwidth"] - 1) - 1, 8 * 8)
        self.assertNotRegex(generated, r"(?m)^\s*fact\b")

    def test_matching_frozen_evidence_passes(self):
        run, metadata, _ = self.fixture()
        result = scale.validate(run, metadata)
        self.assertTrue(result["validated"], result["errors"])
        self.assertEqual(result["observed"], "UNSAT")

    def test_windows_evidence_path_revalidates_on_any_platform(self):
        run, metadata, _ = self.fixture()
        metadata["original_source_file"] = "..\\original-model.als"
        result = scale.validate(run, metadata)
        self.assertTrue(result["validated"], result["errors"])

    def test_receipt_scope_mismatch_is_rejected(self):
        run, metadata, receipt = self.fixture()
        receipt["commands"]["RetrieveIsValid"]["source"] = metadata["command_source"].replace("6 SPC", "4 SPC")
        (run / "alloy/receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
        result = scale.validate(run, metadata)
        self.assertFalse(result["validated"])
        self.assertTrue(any("scope differs" in e for e in result["errors"]))

    def test_timeout_never_becomes_unsat_even_with_completed_evidence(self):
        run, metadata, _ = self.fixture()
        metadata["status"] = "timed_out"
        result = scale.validate(run, metadata)
        self.assertFalse(result["validated"])
        self.assertIsNone(result["observed"])

    def test_hash_mismatch_is_rejected(self):
        run, metadata, _ = self.fixture()
        (run / "telecommunications.als").write_text("// tampered\n", encoding="utf-8")
        self.assertFalse(scale.validate(run, metadata)["validated"])

    def test_scope_labels_cannot_relabel_existing_evidence(self):
        run, metadata, _ = self.fixture()
        for field, value in (("points_bound", 100), ("message_values_bound", 1),
                             ("states", 2), ("sequence_bound", 8),
                             ("integer_bitwidth", 9), ("representation", "ordered")):
            with self.subTest(field=field):
                altered = {**metadata, field: value}
                result = scale.validate(run, altered)
                self.assertFalse(result["validated"])
                self.assertTrue(any("regeneration" in error or "Derived execution detail" in error
                                    for error in result["errors"]), result["errors"])

    def test_generated_body_change_is_rejected_even_when_recorded_hash_is_updated(self):
        run, metadata, _ = self.fixture()
        model = run / "telecommunications.als"
        model.write_bytes(model.read_bytes() + b"\nfact hidden_assumption { all s: State | sectionInvariant[s] }\n")
        metadata["model_sha256"] = scale.digest(model)
        result = scale.validate(run, metadata)
        self.assertFalse(result["validated"])
        self.assertTrue(any("deterministic regeneration" in error for error in result["errors"]))

    def instance(self, count=6, ordered=False):
        instance = ET.Element("instance")
        sig = ET.SubElement(instance, "sig", label="this/State")
        ET.SubElement(sig, "atom", label="State$0")
        route = ET.SubElement(instance, "field", label="route")
        for i in range(count):
            row = ET.SubElement(route, "tuple")
            for value in (["State$0", f"SPC${i}"] if ordered else ["State$0", str(i), f"SPC${i}"]):
                ET.SubElement(row, "atom", label=value)
        pending = ET.SubElement(instance, "field", label="ins")
        row = ET.SubElement(pending, "tuple")
        for value in ["State$0", "SPC$0", "0", "Message$0"]:
            ET.SubElement(row, "atom", label=value)
        for name in ("ShowExactRouteWithTraffic", "ShowFullRouteWithTraffic"):
            skolem = ET.SubElement(instance, "skolem", label=f"${name}_s")
            row = ET.SubElement(skolem, "tuple")
            ET.SubElement(row, "atom", label="State$0")
        return instance

    def low_arity_instance(self, before_count=6, after_count=0, selected="Before", traffic="Before"):
        instance = ET.Element("instance")
        ET.SubElement(instance, "sig", label="this/State", ID="10", abstract="yes")
        for index, name in enumerate(("Before", "After"), 11):
            sig = ET.SubElement(instance, "sig", label=f"this/{name}", ID=str(index), parentID="10")
            ET.SubElement(sig, "atom", label=f"{name}$0")
        route = ET.SubElement(instance, "field", label="route")
        for name, count in (("Before", before_count), ("After", after_count)):
            for index in range(count):
                row = ET.SubElement(route, "tuple")
                for value in (f"{name}$0", f"SPC${index}"):
                    ET.SubElement(row, "atom", label=value)
            pending = ET.SubElement(instance, "field", label=f"ins{name}")
            if name == traffic:
                row = ET.SubElement(pending, "tuple")
                for value in ("SPC$0", "0", "Message$0"):
                    ET.SubElement(row, "atom", label=value)
        skolem = ET.SubElement(instance, "skolem", label="$ShowFullRouteWithTraffic_s")
        row = ET.SubElement(skolem, "tuple")
        ET.SubElement(row, "atom", label=f"{selected}$0")
        return instance

    def test_exact_witness_checks_active_route_not_available_pool(self):
        self.assertEqual(scale.exact_route_evidence(self.instance(), "ShowExactRouteWithTraffic", 6), [6])
        with self.assertRaisesRegex(ValueError, "route length differs"):
            scale.exact_route_evidence(self.instance(count=5), "ShowExactRouteWithTraffic", 6)
        self.assertEqual(scale.exact_route_evidence(self.instance(ordered=True), "ShowFullRouteWithTraffic", 6), [6])

    def test_exact_witness_requires_traffic(self):
        instance = self.instance()
        instance.find("field[@label='ins']").clear()
        with self.assertRaises(ValueError):
            scale.exact_route_evidence(instance, "ShowExactRouteWithTraffic", 6)

    def test_low_arity_witness_uses_before_after_pending_fields(self):
        instance = self.low_arity_instance()
        pending = instance.find("field[@label='insBefore']")
        self.assertEqual(scale.exact_route_evidence(instance, "ShowFullRouteWithTraffic", 6), [6])
        pending.remove(pending.find("tuple"))
        with self.assertRaisesRegex(ValueError, "no pending traffic"):
            scale.exact_route_evidence(instance, "ShowFullRouteWithTraffic", 6)

    def test_unused_empty_after_slot_does_not_invalidate_selected_full_before(self):
        instance = self.low_arity_instance(before_count=6, after_count=0)
        self.assertEqual(scale.exact_route_evidence(instance, "ShowFullRouteWithTraffic", 6), [6])
        instance = self.low_arity_instance(before_count=0, after_count=6, selected="After", traffic="After")
        self.assertEqual(scale.exact_route_evidence(instance, "ShowFullRouteWithTraffic", 6), [6])

    def test_unused_full_slot_cannot_replace_short_selected_slot(self):
        instance = self.low_arity_instance(before_count=5, after_count=6)
        with self.assertRaisesRegex(ValueError, "Selected active route length differs"):
            scale.exact_route_evidence(instance, "ShowFullRouteWithTraffic", 6)

    def test_pending_only_in_wrong_slot_is_rejected(self):
        instance = self.low_arity_instance(before_count=6, after_count=6, selected="Before", traffic="After")
        with self.assertRaisesRegex(ValueError, "no pending traffic"):
            scale.exact_route_evidence(instance, "ShowFullRouteWithTraffic", 6)

    def test_abstract_state_children_supply_before_and_after_atoms(self):
        instance = self.instance(ordered=True)
        parent = instance.find("sig")
        parent.set("ID", "10")
        parent.remove(parent.find("atom"))
        before = ET.SubElement(instance, "sig", label="this/Before", ID="11", parentID="10")
        ET.SubElement(before, "atom", label="State$0")
        after = ET.SubElement(instance, "sig", label="this/After", ID="12", parentID="10")
        # Exercise recursive descendants rather than depending on direct children.
        concrete = ET.SubElement(instance, "sig", label="this/ConcreteAfter", ID="13", parentID="12")
        ET.SubElement(concrete, "atom", label="State$1")
        route = instance.find("field[@label='route']")
        for row in list(route.findall("tuple")):
            duplicate = ET.fromstring(ET.tostring(row))
            duplicate.find("atom").set("label", "State$1")
            route.append(duplicate)
        self.assertEqual(scale.exact_route_evidence(instance, "ShowFullRouteReceive", 6), [6, 6])
        route.remove(route.findall("tuple")[-1])
        with self.assertRaisesRegex(ValueError, "route length differs"):
            scale.exact_route_evidence(instance, "ShowFullRouteReceive", 6)

    def test_timeout_terminates_child_and_records_unknown(self):
        generated, details = scale.generate(self.source, "RetrieveIsValid", 6, 4)
        original = self.root / "original.als"
        original.write_bytes(scale.MODEL.read_bytes())
        jar = self.root / "alloy.jar"
        jar.write_bytes(b"fixture")
        child = mock.Mock()
        child.returncode = -15
        child.wait.side_effect = [subprocess.TimeoutExpired("java", 0.01), -15]
        child.poll.return_value = None
        with mock.patch.object(scale.subprocess, "Popen", return_value=child):
            result = scale.run_command(self.root / "timeout-run", generated, details, original=original,
                                       java="java", jar=jar, solver="sat4j", timeout=0.01, heap_mb=128)
        child.terminate.assert_called_once()
        self.assertEqual(result["status"], "timed_out")
        self.assertIsNone(result["validation"]["observed"])
        self.assertFalse(result["validation"]["validated"])

    def test_ordered_mode_keeps_history_bound_independent_of_point_count(self):
        model = scale.ROOT / "telecommunications_scalable.als"
        source = model.read_text(encoding="utf-8")
        generated, details = scale.generate(source, "ShowFullRouteWithTraffic", 100, 4)
        self.assertEqual(details["representation"], "ordered")
        self.assertEqual(details["sequence_bound"], 4)
        self.assertEqual(details["integer_bitwidth"], 5)
        self.assertEqual(details["states"], 1)
        self.assertTrue(details["exact_route_witness"])
        self.assertIn("100 SPC", details["command_source"])
        self.assertNotIn("#s.route = 100", generated)

    def test_partial_suite_never_claims_all_planned_expectations_validated(self):
        suite = self.root / "suite"
        suite.mkdir()
        one = {"points_bound": 6, "command": "RetrieveIsValid", "sequence_bound": 6,
               "integer_bitwidth": 7, "expected": "UNSAT", "status": "completed", "elapsed_seconds": 1,
               "validation": {"validated": True, "observed": "UNSAT"}}
        metadata = {"original_sha256": "fixture", "representation": "sequence", "points": [6, 8],
                    "commands": ["RetrieveIsValid"], "runs": [one]}
        scale.summarize(suite, metadata)
        self.assertFalse(metadata["all_expectations_validated"])
        metadata["finished_at"] = "fixture"
        scale.summarize(suite, metadata)
        self.assertFalse(metadata["all_expectations_validated"])
        metadata["runs"].append({**one, "points_bound": 8})
        scale.summarize(suite, metadata)
        self.assertTrue(metadata["all_expectations_validated"])


if __name__ == "__main__":
    unittest.main()
