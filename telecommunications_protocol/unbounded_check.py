"""Unbounded proof obligations for the Chapter 20 sectional protocol (Z3).

Alloy checks every property only up to a finite number of signalling points
and a finite history length. This script discharges the same obligations for
histories of ANY length and ANY number of message values, using Z3's theory of
sequences over an uninterpreted message sort. Network size is handled by the
locality lemma in scaling_design.md ("Unbounded argument"): every operation
changes the histories of at most two adjacent sections (or adds one), the
frame keeps every other section unchanged, and the rest of the route enters
only through arbitrary context sequences. Each obligation below is therefore
stated over a fixed window of sections plus arbitrary context, which covers
every route length.

Encoding (mirrors telecommunications.als):
  * newest message at index 0, so "prepend m to s" is <m> ++ s and the oldest
    pending message is the LAST element of a buffer;
  * local conservation  rec = ins ++ sent  for every active section;
  * boundary agreement  sent[p] = rec[next p]  for adjacent sections;
  * input = rec[first], output = sent[last], inFlight = ins[first] ++ ... ++ ins[last].

A check is PROVED when Z3 reports the negated goal UNSAT. The intentional
receive bug must instead be SAT (a counterexample), and witnesses must be SAT,
so the premises are known not to be contradictory.

These are machine-checked proofs relative to the soundness of Z3 and to the
correspondence between this encoding and the Alloy predicates, which is
argued in scaling_design.md rather than mechanically checked.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
import time

try:
    import z3
except ImportError:  # pragma: no cover - exercised only without the dependency
    z3 = None

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "results" / "unbounded_summary.md"


@dataclass
class Result:
    name: str
    kind: str          # "proof", "counterexample" or "witness"
    expected: str      # "unsat" or "sat"
    observed: str
    seconds: float
    meaning: str

    @property
    def ok(self) -> bool:
        return self.observed == self.expected


class Obligations:
    def __init__(self, timeout_ms: int = 60_000):
        self.timeout_ms = timeout_ms
        self.Msg = z3.DeclareSort("Msg")
        self.S = z3.SeqSort(self.Msg)
        self.results: list[Result] = []

    # -- helpers ---------------------------------------------------------
    def seq(self, name):
        return z3.Const(name, self.S)

    def msg(self, name):
        return z3.Const(name, self.Msg)

    def section(self, tag):
        return Section(self, tag)

    def unit(self, m):
        return z3.Unit(m)

    def prepend(self, m, s):
        return z3.Concat(z3.Unit(m), s)

    def empty(self):
        return z3.Empty(self.S)

    def _solve(self, constraints):
        solver = z3.Solver()
        solver.set("timeout", self.timeout_ms)
        solver.add(*constraints)
        start = time.perf_counter()
        observed = str(solver.check())
        return observed, round(time.perf_counter() - start, 4)

    def prove(self, name, premises, goal, meaning):
        observed, seconds = self._solve(list(premises) + [z3.Not(goal)])
        self.results.append(Result(name, "proof", "unsat", observed, seconds, meaning))

    def refute(self, name, premises, goal, meaning):
        observed, seconds = self._solve(list(premises) + [z3.Not(goal)])
        self.results.append(Result(name, "counterexample", "sat", observed, seconds, meaning))

    def witness(self, name, constraints, meaning):
        observed, seconds = self._solve(list(constraints))
        self.results.append(Result(name, "witness", "sat", observed, seconds, meaning))

    # -- obligations -----------------------------------------------------
    def run_all(self) -> list[Result]:
        self.initial()
        self.retrieve()
        self.transmit()
        self.receive()
        self.daemon()
        self.insertion()
        self.stutter()
        self.broken_receive()
        self.witnesses()
        return self.results

    def initial(self):
        s = self.section("init")
        e = self.empty()
        self.prove("InitialIsValid", [s.rec == e, s.ins == e, s.sent == e],
                   z3.And(s.conserves(), s.rec == e, s.sent == e),
                   "Empty histories satisfy local conservation; input and output are empty.")

    def retrieve(self):
        # By induction from the last section back to the first:
        #   Claim(i): rec[i] = ins[i] ++ ... ++ ins[last] ++ output.
        last = self.section("last")
        output = self.seq("output")
        self.prove("RetrieveBase", [last.conserves(), last.sent == output],
                   last.rec == z3.Concat(last.ins, output),
                   "Claim holds at the last section (local conservation).")
        sec, tail, rec_next = self.section("i"), self.seq("tail_buffers"), self.seq("rec_next")
        self.prove("RetrieveStep",
                   [sec.conserves(), sec.sent == rec_next, rec_next == z3.Concat(tail, output)],
                   sec.rec == z3.Concat(sec.ins, tail, output),
                   "If the claim holds at the next section, it holds here (boundary agreement).")
        # Consequence: input = inFlight ++ output, so output is a suffix of input.

    def transmit(self):
        f, fp, n = self.section("F"), self.section("F_post"), self.section("N")
        m = self.msg("m")
        rest_buffers, output = self.seq("later_buffers"), self.seq("output")
        pre = [f.conserves(), n.conserves(), f.sent == n.rec]
        op = [fp.rec == self.prepend(m, f.rec), fp.ins == self.prepend(m, f.ins), fp.sent == f.sent]
        self.prove("TransmitPreservesInvariant", pre + op,
                   z3.And(fp.conserves(), fp.sent == n.rec),
                   "Conservation at the first section and its boundary with the next survive transmit.")
        retrieve = f.rec == z3.Concat(f.ins, rest_buffers, output)
        self.prove("TransmitRefinesExternal", pre + op + [retrieve],
                   z3.And(fp.rec == self.prepend(m, f.rec),
                          fp.rec == z3.Concat(fp.ins, rest_buffers, output)),
                   "input' = <m> ++ input, output' = output, and output' remains a suffix of input'.")

    def receive(self):
        p, last, lp = self.section("P"), self.section("L"), self.section("L_post")
        m, kept = self.msg("m"), self.seq("ins_L_without_oldest")
        earlier, inp = self.seq("earlier_buffers"), self.seq("input")
        pre = [p.conserves(), last.conserves(), p.sent == last.rec]
        op = [last.ins == z3.Concat(kept, self.unit(m)), lp.ins == kept,
              lp.sent == self.prepend(m, last.sent), lp.rec == last.rec]
        self.prove("ReceivePreservesInvariant", pre + op,
                   z3.And(lp.conserves(), p.sent == lp.rec),
                   "Delivering the oldest pending message keeps conservation and the incoming boundary.")
        retrieve = inp == z3.Concat(earlier, last.ins, last.sent)
        self.prove("ReceiveRefinesExternal", pre + op + [retrieve],
                   z3.And(inp == z3.Concat(earlier, lp.ins, lp.sent),
                          z3.Length(lp.sent) == z3.Length(last.sent) + 1),
                   "input' = input, output grows by one, and output' remains a suffix of input'.")

    def daemon(self):
        pr, u, d, nx = (self.section(t) for t in ("Prev", "U", "D", "Next"))
        up, dp = self.section("U_post"), self.section("D_post")
        m, kept = self.msg("m"), self.seq("ins_U_without_oldest")
        before, after = self.seq("buffers_before_U"), self.seq("buffers_after_D")
        pre = [pr.conserves(), u.conserves(), d.conserves(), nx.conserves(),
               pr.sent == u.rec, u.sent == d.rec, d.sent == nx.rec]
        op = [u.ins == z3.Concat(kept, self.unit(m)), up.ins == kept,
              up.sent == self.prepend(m, u.sent), up.rec == u.rec,
              dp.ins == self.prepend(m, d.ins), dp.rec == self.prepend(m, d.rec), dp.sent == d.sent]
        self.prove("DaemonPreservesInvariant", pre + op,
                   z3.And(up.conserves(), dp.conserves(), pr.sent == up.rec,
                          up.sent == dp.rec, dp.sent == nx.rec),
                   "Both changed sections conserve, and all three affected boundaries agree.")
        self.prove("DaemonIsInvisible", pre + op,
                   z3.And(up.rec == u.rec, dp.sent == d.sent,
                          z3.Concat(before, u.ins, d.ins, after) ==
                          z3.Concat(before, up.ins, dp.ins, after)),
                   "input, output and the route-order concatenation of buffers are unchanged.")

    def insertion(self):
        u, d, x = self.section("U"), self.section("D"), self.section("X")
        before, after = self.seq("buffers_before_U"), self.seq("buffers_after_D")
        pre = [u.conserves(), d.conserves(), u.sent == d.rec]
        op = [x.rec == u.sent, x.ins == self.empty(), x.sent == d.rec]
        self.prove("InsertionPreservesInvariant", pre + op,
                   z3.And(x.conserves(), u.sent == x.rec, x.sent == d.rec),
                   "The fresh section conserves and agrees with both neighbours.")
        self.prove("InsertionIsInvisible", pre + op,
                   z3.Concat(before, u.ins, d.ins, after) ==
                   z3.Concat(before, u.ins, x.ins, d.ins, after),
                   "Inserting an empty buffer leaves the concatenation of buffers unchanged.")

    def stutter(self):
        s, sp = self.section("s"), self.section("s_post")
        self.prove("IdleStepsAreInvisible",
                   [s.conserves(), sp.rec == s.rec, sp.ins == s.ins, sp.sent == s.sent],
                   sp.conserves(),
                   "The optional idle/poll stutter changes nothing, so it preserves everything.")

    def broken_receive(self):
        p, last, lp = self.section("P"), self.section("L"), self.section("L_post")
        m, kept = self.msg("m"), self.seq("ins_L_without_newest")
        pre = [p.conserves(), last.conserves(), p.sent == last.rec]
        bug = [last.ins == z3.Concat(self.unit(m), kept), lp.ins == kept,
               lp.sent == self.prepend(m, last.sent), lp.rec == last.rec]
        self.refute("BrokenReceiveWouldPreserveInvariant", pre + bug, lp.conserves(),
                    "Delivering the NEWEST pending message breaks conservation (mutation is caught).")

    def witnesses(self):
        pr, u, d, nx = (self.section(t) for t in ("Prev", "U", "D", "Next"))
        up, dp = self.section("U_post"), self.section("D_post")
        m, m2 = self.msg("m"), self.msg("m2")
        self.witness("DaemonWitness",
                     [pr.conserves(), u.conserves(), d.conserves(), nx.conserves(),
                      pr.sent == u.rec, u.sent == d.rec, d.sent == nx.rec, z3.Distinct(m, m2),
                      u.ins == z3.Concat(self.unit(m2), self.unit(m)), up.ins == self.unit(m2),
                      up.sent == self.prepend(m, u.sent), up.rec == u.rec,
                      dp.ins == self.prepend(m, d.ins), dp.rec == self.prepend(m, d.rec),
                      dp.sent == d.sent],
                     "A valid window where the daemon moves the oldest of two distinct values.")
        last, lp, kept = self.section("L"), self.section("L_post"), self.seq("kept")
        self.witness("ReceiveWitness",
                     [last.conserves(), z3.Length(last.ins) >= 2,
                      last.ins == z3.Concat(kept, self.unit(m)), lp.ins == kept,
                      lp.sent == self.prepend(m, last.sent), lp.rec == last.rec],
                     "A valid last section with two pending messages can deliver one.")


class Section:
    def __init__(self, owner: Obligations, tag: str):
        self.rec = owner.seq(f"rec_{tag}")
        self.ins = owner.seq(f"ins_{tag}")
        self.sent = owner.seq(f"sent_{tag}")

    def conserves(self):
        return self.rec == z3.Concat(self.ins, self.sent)


def report(results: list[Result], version: str) -> str:
    stamp = datetime.now(timezone(timedelta(hours=6))).isoformat(timespec="seconds")
    lines = ["# Unbounded proof obligations (Z3)", "",
             f"Report generated: {stamp} (Asia/Dhaka). Z3 {version}. Script: [unbounded_check.py](../unbounded_check.py).", "",
             "Each proof obligation holds for histories of any length, any number of message values, "
             "and, through the locality lemma in [scaling_design.md](../scaling_design.md#unbounded-argument), "
             "any number of signalling points. PROVED means Z3 found the negated goal unsatisfiable.", "",
             "| Obligation | Kind | Expected | Observed | Seconds | Meaning |",
             "|---|---|---|---|---:|---|"]
    for r in results:
        verdict = {"proof": "PROVED", "counterexample": "counterexample found",
                   "witness": "satisfiable"}[r.kind] if r.ok else f"UNEXPECTED ({r.observed})"
        lines.append(f"| `{r.name}` | {r.kind} | {r.expected.upper()} | {verdict} | {r.seconds} | {r.meaning} |")
    lines += ["", "## Scope of the claim", "",
              "- The obligations are stated on the sequence-level protocol of `telecommunications.als`. "
              "Their correspondence with the Alloy predicates and the locality lemma are argued in "
              "scaling_design.md; they are not mechanically checked.",
              "- Results rely on the soundness of Z3's sequence solver.",
              "- Safety only. Eventual delivery needs a fairness assumption; see the liveness section of scaling_design.md.",
              ""]
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--timeout-ms", type=int, default=60_000)
    parser.add_argument("--no-report", action="store_true", help="Print results without writing the report")
    args = parser.parse_args(argv)
    if z3 is None:
        print("z3-solver is not installed: python -m pip install -r requirements-unbounded.txt", file=sys.stderr)
        return 2
    results = Obligations(args.timeout_ms).run_all()
    width = max(len(r.name) for r in results)
    for r in results:
        print(f"{r.name:<{width}}  expected {r.expected:<5} observed {r.observed:<7} "
              f"{'ok' if r.ok else 'MISMATCH'}  {r.seconds}s")
    if not args.no_report:
        REPORT.write_text(report(results, z3.get_version_string()), encoding="utf-8", newline="\n")
        print(f"Report: {REPORT}")
    return 0 if all(r.ok for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
