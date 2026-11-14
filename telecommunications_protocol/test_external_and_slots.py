"""Regressions for the external-solver backend, slot model and Z3 obligations.

No SAT solver or Java process is launched, except Z3 when it is installed.
"""
import json
import os
from pathlib import Path
import re
import tempfile
import unittest
from unittest import mock
import xml.etree.ElementTree as ET

import scale_verify as scale

SLOTS = scale.ROOT / "telecommunications_slots.als"


class ExternalSolverEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = SLOTS.read_text(encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def fixture(self, name="DaemonPreservesInvariant", clauses=1234, status=("s UNSATISFIABLE", 20)):
        generated, details = scale.generate(self.source, name, 100, 4, history_bound=4)
        original = self.root / "original-model.als"
        original.write_bytes(SLOTS.read_bytes())
        run = self.root / "run"
        (run / "alloy").mkdir(parents=True)
        model = run / "telecommunications.als"
        model.write_text(generated, encoding="utf-8", newline="\n")
        cnf = run / "alloy" / f"{name}.cnf"
        cnf.write_text(f"p cnf 10 {clauses}\n1 0\n", encoding="ascii")
        metadata = {**details, "status": "completed", "process_exit_code": 0, "backend": "external",
                    "solver": "CNF", "requested_solver": "kissat", "no_overflow": True,
                    "original_source_file": "../original-model.als", "original_sha256": scale.digest(original),
                    "model_sha256": scale.digest(model),
                    "external": {"solver": "kissat", "cnf_sha256": scale.digest(cnf), "cnf_clauses": clauses,
                                 "status_line": status[0], "exit_code": status[1], "proof": None}}
        receipt = {"solver": "CNF", "noOverflow": True, "commands": {name: {
            "name": name, "type": details["command_type"], "source": details["command_source"],
            "bitwidth": details["integer_bitwidth"], "maxseq": details["sequence_bound"],
            "transformPath": f"{name}.cnf"}}}
        (run / "alloy" / "receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
        (run / "analyzer.log").write_text(f"00. check {name}   {name}.cnf\n", encoding="utf-8")
        return run, metadata

    def test_external_unsat_with_matching_translation_validates(self):
        run, metadata = self.fixture()
        result = scale.validate(run, metadata)
        self.assertTrue(result["validated"], result["errors"])
        self.assertEqual(result["observed"], "UNSAT")

    def test_empty_cnf_is_never_accepted_as_unsat(self):
        # Kodkod writes "p cnf 0 0" when it decides a formula during translation;
        # that file is satisfiable even when the assertion holds.
        run, metadata = self.fixture(clauses=0)
        result = scale.validate(run, metadata)
        self.assertFalse(result["validated"])
        self.assertTrue(any("Empty CNF" in e for e in result["errors"]))

    def test_unknown_solver_answer_is_rejected(self):
        run, metadata = self.fixture(status=("s UNKNOWN", 0))
        self.assertFalse(scale.validate(run, metadata)["validated"])

    def test_external_sat_contradicts_unsat_expectation(self):
        run, metadata = self.fixture(status=("s SATISFIABLE", 10))
        result = scale.validate(run, metadata)
        self.assertFalse(result["validated"])
        self.assertEqual(result["observed"], "SAT")

    def test_modified_retained_cnf_is_rejected(self):
        run, metadata = self.fixture()
        (run / "alloy" / "DaemonPreservesInvariant.cnf").write_text("p cnf 1 1\n-1 0\n", encoding="ascii")
        self.assertFalse(scale.validate(run, metadata)["validated"])

    def test_requested_proof_must_be_verified(self):
        run, metadata = self.fixture()
        metadata["external"]["proof"] = {"status_line": "s NOT VERIFIED"}
        self.assertFalse(scale.validate(run, metadata)["validated"])
        metadata["external"]["proof"] = {"status_line": "s VERIFIED"}
        self.assertTrue(scale.validate(run, metadata)["validated"])

    def test_external_backend_cannot_decide_witnesses(self):
        run, metadata = self.fixture(name="ShowDaemon", status=("s SATISFIABLE", 10))
        result = scale.validate(run, metadata)
        self.assertFalse(result["validated"])
        self.assertTrue(any("only accepted for UNSAT-expected checks" in e for e in result["errors"]))

    def test_witness_commands_route_to_builtin_solver(self):
        generated, details = scale.generate(self.source, "ShowDaemon", 10, 4, history_bound=4)
        original = self.root / "original.als"
        original.write_bytes(SLOTS.read_bytes())
        jar = self.root / "alloy.jar"
        jar.write_bytes(b"fixture")
        child = mock.Mock(returncode=1)
        child.wait.return_value = 1
        child.poll.return_value = 1
        with mock.patch.object(scale.subprocess, "Popen", return_value=child) as popen:
            result = scale.run_command(self.root / "witness", generated, details, original=original,
                                       java="java", jar=jar, solver="kissat", timeout=5, heap_mb=128)
        argv = popen.call_args[0][0]
        self.assertEqual(argv[argv.index("-s") + 1], "glucose")
        self.assertEqual(result["backend"], "alloy")

    def test_cnf_header(self):
        cnf = self.root / "x.cnf"
        cnf.write_text("c comment\np cnf 7 3\n1 0\n", encoding="ascii")
        self.assertEqual(scale.cnf_header(cnf), (7, 3))

    @unittest.skipUnless(os.name == "nt", "Windows drive-letter paths")
    def test_wsl_path_translation(self):
        self.assertEqual(scale.to_wsl_path(Path("D:/formal method/x.cnf")), "/mnt/d/formal method/x.cnf")

    def test_status_line_uses_last_solution_line(self):
        self.assertEqual(scale.status_line("c x\ns UNSATISFIABLE\n"), "s UNSATISFIABLE")
        self.assertIsNone(scale.status_line("c nothing\n"))


class SlotModelTests(unittest.TestCase):
    def test_slot_model_has_all_ten_checks_and_no_wide_relations(self):
        source = SLOTS.read_text(encoding="utf-8")
        names = {item["name"] for item in scale.verify.declarations(source)}
        self.assertTrue(set(scale.CORRECT_CHECKS) <= names)
        code = "\n".join(line.split("//")[0] for line in source.splitlines()
                         if not scale.verify.COMMAND.fullmatch(line.strip()))
        # No sequence library, cardinality or integer arithmetic in the encoding.
        # ... and no closure-based route navigation over the point pool.
        for token in ("seq/", "seqLib", "#", "add[", "sub[", "Int",
                      "nexts", "prevs", "pointOrder/min", "pointOrder/max"):
            self.assertNotIn(token, code)
        # The only fact defines derived route structure; it must not assume validity.
        facts = re.findall(r"(?ms)^fact\s+(\w+)\s*\{(.*?)^\}", code)
        self.assertEqual([name for name, _ in facts], ["derivedRouteStructure"])
        for forbidden in ("sectionInvariant", "shape", "concat", "isSeq"):
            self.assertNotIn(forbidden, facts[0][1])
        self.assertEqual(scale.SLOT_BOUND.search(source).group(1), "4")

    def test_slot_history_bound_is_enforced(self):
        with self.assertRaises(SystemExit):
            scale.main(["--model", str(SLOTS), "--points", "10", "--history-bound", "2", "--dry-run"])

    def test_slot_witness_reads_per_slot_pending_fields(self):
        instance = ET.Element("instance")
        ET.SubElement(instance, "sig", label="this/State", ID="10", abstract="yes")
        for index, name in enumerate(("Before", "After"), 11):
            sig = ET.SubElement(instance, "sig", label=f"this/{name}", ID=str(index), parentID="10")
            ET.SubElement(sig, "atom", label=f"{name}$0")
        route = ET.SubElement(instance, "field", label="route")
        for index in range(6):
            row = ET.SubElement(route, "tuple")
            for value in ("Before$0", f"SPC${index}"):
                ET.SubElement(row, "atom", label=value)
        for k in range(4):
            ET.SubElement(instance, "field", label=f"ins{k}Before")
            ET.SubElement(instance, "field", label=f"ins{k}After")
        row = ET.SubElement(instance.find("field[@label='ins2Before']"), "tuple")
        for value in ("SPC$3", "Message$0"):
            ET.SubElement(row, "atom", label=value)
        skolem = ET.SubElement(instance, "skolem", label="$ShowFullRouteWithTraffic_s")
        ET.SubElement(ET.SubElement(skolem, "tuple"), "atom", label="Before$0")
        self.assertEqual(scale.exact_route_evidence(instance, "ShowFullRouteWithTraffic", 6), [6])
        instance.find("field[@label='ins2Before']").clear()
        with self.assertRaisesRegex(ValueError, "no pending traffic"):
            scale.exact_route_evidence(instance, "ShowFullRouteWithTraffic", 6)


class UnboundedObligationTests(unittest.TestCase):
    def setUp(self):
        import unbounded_check
        if unbounded_check.z3 is None:
            self.skipTest("z3-solver is not installed")
        self.module = unbounded_check

    def test_all_obligations_have_expected_outcomes(self):
        results = self.module.Obligations(timeout_ms=60_000).run_all()
        failures = [(r.name, r.observed) for r in results if not r.ok]
        self.assertEqual(failures, [])
        kinds = {r.kind for r in results}
        self.assertEqual(kinds, {"proof", "counterexample", "witness"})

    def test_a_wrong_daemon_is_not_proved(self):
        # Mutation: forward the NEWEST message instead of the oldest.
        z3 = self.module.z3
        ob = self.module.Obligations(timeout_ms=60_000)
        u, d = ob.section("U"), ob.section("D")
        up, dp = ob.section("U_post"), ob.section("D_post")
        m, kept = ob.msg("m"), ob.seq("kept")
        pre = [u.conserves(), d.conserves(), u.sent == d.rec]
        bad = [u.ins == z3.Concat(ob.unit(m), kept), up.ins == kept, up.sent == ob.prepend(m, u.sent),
               up.rec == u.rec, dp.ins == ob.prepend(m, d.ins), dp.rec == ob.prepend(m, d.rec), dp.sent == d.sent]
        ob.prove("BadDaemon", pre + bad, up.conserves(), "mutation")
        self.assertEqual(ob.results[-1].observed, "sat")


if __name__ == "__main__":
    unittest.main()
