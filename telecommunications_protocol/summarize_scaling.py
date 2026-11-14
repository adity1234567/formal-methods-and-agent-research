"""Revalidate saved scaling evidence and build the consolidated coverage report.

Run this after benchmark processes finish. A result is counted only against the
same frozen model hash and exact network/history/message/integer scopes.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path

import check_correspondence
import scale_verify
import verify

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "scale-results"
MODELS = {
    "telecommunications.als": "Original sequence route",
    "telecommunications_scalable.als": "Ordered active route",
    "telecommunications_large.als": "Ordered route, two slots",
    "telecommunications_fixed_route.als": "Fixed full route, two slots",
    "telecommunications_slots.als": "Ordered route, position fields (arity 2)",
}


def expected_result(run: dict, outcome: str, command_type: str | None = None) -> bool:
    """Count a result only when its expectation and validated outcome agree."""
    declaration = run.get("declaration", {})
    return (run["validation"]["validated"] and
            run["validation"].get("observed") == outcome and
            run.get("expected", declaration.get("expected")) == outcome and
            (command_type is None or
             run.get("command_type", declaration.get("type")) == command_type))


def correspondence_report(evidence: Path, link) -> list[str]:
    """Revalidate attempts; combine only identical current harness/dependency bytes."""
    coverage = defaultdict(dict)
    attempts = []
    current = {harness: {name: check_correspondence.digest(ROOT / name) for name in files}
               for harness, files in check_correspondence.HARNESSES.items()}
    for suite in sorted(evidence.glob("correspondence-*")):
        meta = json.loads((suite / "suite.json").read_text(encoding="utf-8"))
        runs = []
        for name in meta["commands"]:
            execution = suite / name / "execution.json"
            if not execution.is_file():
                continue
            run = json.loads(execution.read_text(encoding="utf-8"))
            run["validation"] = check_correspondence.validate(execution.parent, run)
            check_correspondence.save_json(execution, run)
            runs.append(run)
            harness = run.get("harness", check_correspondence.MODEL_FILES[0])
            if run["source_sha256"] != current.get(harness):
                continue
            if (expected_result(run, "UNSAT", "check") or
                    expected_result(run, "SAT", "run")):
                coverage[harness][run["command"]] = (run, execution)
        meta["results"] = runs
        check_correspondence.summarize(suite, meta)
        attempts.append(f"- [{suite.name}]({link(suite / 'summary.md')}): "
                        f"{meta['status']}; all selected expectations validated: "
                        f"{'yes' if meta['all_expectations_validated'] else 'no'}.")
    lines = ["Coverage below combines matching-source retries; unsuccessful attempts remain linked.", "",
             "| Harness | UNSAT comparison checks | SAT paired-operation witnesses |",
             "|---|---:|---:|"]
    details = []
    for harness in sorted(current):
        declarations = verify.declarations((ROOT / harness).read_text(encoding="utf-8"))
        checks = {d["name"] for d in declarations if d["type"] == "check" and d["expected"] == "UNSAT"}
        witnesses = {d["name"] for d in declarations if d["type"] == "run" and d["expected"] == "SAT"}
        passed = set(coverage[harness])
        lines.append(f"| [{harness}]({link(ROOT / harness)}) | {len(checks & passed)}/{len(checks)} | "
                     f"{len(witnesses & passed)}/{len(witnesses)} |")
        details += [f"### `{harness}`", ""]
        for name, (_, execution) in sorted(coverage[harness].items()):
            details.append(f"- [`{name}`]({link(execution)})")
        details.append("")
    return lines + ["", *details, "All correspondence attempts:", "", *attempts]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, default=EVIDENCE)
    parser.add_argument("--report", type=Path, default=ROOT / "results/scaling_summary.md")
    args = parser.parse_args()
    report_path = args.report.resolve()
    evidence = args.evidence.resolve()
    groups = defaultdict(list)
    suites = []
    excluded = []
    running = []
    sources = {}
    for name, label in MODELS.items():
        source = ROOT / name
        sources[scale_verify.digest(source)] = (name, label, source)

    for suite in sorted(evidence.glob("scale-*")):
        summary_path = suite / "summary.json"
        if not summary_path.is_file():
            running.append(suite.name)
            continue
        meta = json.loads(summary_path.read_text(encoding="utf-8"))
        runs = []
        for execution in sorted(suite.glob("points-*/*/execution.json")):
            run = json.loads(execution.read_text(encoding="utf-8"))
            if run["status"] == "running":
                running.append(str(execution.relative_to(evidence)))
                continue
            run["validation"] = scale_verify.validate(execution.parent, run)
            scale_verify.save_json(execution, run)
            runs.append(run)
            source_info = sources.get(run["original_sha256"])
            if source_info:
                key = (source_info[0], run["points_bound"], run["sequence_bound"],
                       run["message_values_bound"], run["integer_bitwidth"], run["states"])
                # State claims can use one slot while transitions use two. Both
                # remain distinct in detailed records; aggregate coverage omits
                # slot count because each named obligation defines it explicitly.
                groups[key[:-1]].append((run, execution, suite))
        meta["runs"] = runs
        scale_verify.summarize(suite, meta)
        if meta["original_sha256"] not in sources:
            excluded.append(suite)
        else:
            suites.append((suite, meta))

    import os
    def link(path: Path) -> str:
        return Path(os.path.relpath(path, report_path.parent)).as_posix()

    lines = ["# Larger-network verification results", "",
             f"Report generated: {scale_verify.now()} (Asia/Dhaka).", "",
             "This report distinguishes completed property checks from satisfiable examples. "
             "A witness with N active points shows that such a state or transition exists. "
             "It does not establish all protocol properties at N points. A timeout or translation "
             "failure remains UNKNOWN, even if another attempt later succeeds.", "",
             "## Coverage by model and scope", "",
             "Counts combine validated completed commands only when the frozen source hash and "
             "network/history/message/integer bounds match. Each command retains its declared "
             "snapshot count. The fixed-route model has eight property checks and excludes insertion. "
             "The other models have ten. History length bounds lifetime recorded occurrences, "
             "including repeated message values.", "",
             "| Representation | Points | History length | Message values | Int bits | Property checks completed | Expected bug found | Exact-size traffic witness |",
             "|---|---:|---:|---:|---:|---:|---|---|"]
    details = []
    for key, records in sorted(groups.items()):
        model, points, history, messages, bits = key
        model_path = ROOT / model
        commands = {c["name"] for c in verify.declarations(model_path.read_text(encoding="utf-8"))}
        required = set(scale_verify.CORRECT_CHECKS) & commands
        unsat_checks = {r["command"] for r, _, _ in records if expected_result(r, "UNSAT", "check")}
        sat_commands = {r["command"] for r, _, _ in records if expected_result(r, "SAT")}
        checks = required & unsat_checks
        bug = "yes" if "BrokenReceiveWouldPreserveInvariant" in sat_commands else "not established"
        traffic_names = {"ShowFullRouteWithTraffic", "ShowExactRouteWithTraffic"}
        traffic = "yes" if sat_commands & traffic_names else "not established"
        label = MODELS[model]
        topology = f"exactly {points}" if model == "telecommunications_fixed_route.als" else f"up to {points}"
        lines.append(f"| [{label}]({link(model_path)}) | {topology} | {history} | {messages} | {bits} | "
                     f"{len(checks)}/{len(required)} | {bug} | {traffic} |")
        heading = f"{label}: {topology} points, history {history}, message values {messages}, {bits}-bit Int"
        details += [f"### {heading}", "", f"Frozen model SHA-256: `{scale_verify.digest(model_path)}`.", ""]
        if checks == required and required:
            details.append("All property checks declared for this representation completed with validated UNSAT results.")
        else:
            details.append("Property coverage is incomplete. Missing validated checks: " +
                           ", ".join(f"`{x}`" for x in sorted(required - checks)) + ".")
        details += ["", "| Command | Validated outcome | Solver | Seconds | Exact active route lengths | Evidence |",
                    "|---|---|---|---:|---|---|"]
        # Keep the fastest validated successful attempt for a concise command
        # table, and link every suite below so timeouts and retries remain visible.
        best = {}
        for run, execution, suite in records:
            if run["validation"]["validated"]:
                prior = best.get(run["command"])
                if prior is None or run["elapsed_seconds"] < prior[0]["elapsed_seconds"]:
                    best[run["command"]] = (run, execution)
        for name, (run, execution) in sorted(best.items()):
            lengths = run["validation"].get("active_route_lengths")
            details.append(f"| `{name}` | {run['validation']['observed']} | {scale_verify.solver_label(run)} | "
                           f"{run['elapsed_seconds']:.3f} | "
                           f"{lengths if lengths is not None else 'not an exact-size witness'} | [record]({link(execution)}) |")
        unknowns = [run for run, _, _ in records if not run["validation"]["validated"]]
        details += ["", f"Incomplete/failed attempts retained for this scope: {len(unknowns)}.", ""]
        for suite in sorted({s for _, _, s in records}):
            details.append(f"- [Full suite including unsuccessful attempts]({link(suite / 'summary.md')})")
        details.append("")

    lines += ["", "## What changed", "",
              "The ordered models decouple route size from message-history length and compute pending "
              "sequence offsets from arrival-history lengths. The two-slot model reduces stored history "
              "relations from arity four to arity three. The fixed-route specialization uses direct "
              "neighbours on a full ordered route and deliberately omits insertion.", "",
              "Ordered-pool models restrict a particular fresh point to its fixed position when inserting. "
              "Their safety correspondence uses compatible point renaming and does not establish every "
              "original insertion enabledness obligation. The two-slot models check states and individual "
              "transitions, not the three/seven-snapshot demonstrations. See "
              f"[the design and mathematical argument]({link(ROOT / 'scaling_design.md')}).", "",
              "The earlier 1,000-point ordered model with four-column history fields hit Alloy's translation "
              "capacity before solving. Lower-arity variants address that representation limit, but remain "
              "subject to solver time and memory costs. Timeouts and translation/resource failures "
              "do not provide counterexamples.", "",
              "The position-field model (telecommunications_slots.als) stores every history position as its own arity-2 field and replaces "
              "lengths, offsets and concatenation by constant slot shifts, so its SAT problems contain no "
              "integer circuits and its relations stay far below the translation capacity. Its history "
              "bound is fixed at four entries. Some of its checks were decided by Kissat or CaDiCaL from "
              "Alloy's CNF export; the Solver column says which, and whether a DRAT proof was verified. "
              "External solvers only decide UNSAT-expected checks; witnesses use a built-in solver.", "",
              "## Unbounded safety argument", "",
              "Bounded network sizes are not the only evidence. A locality lemma reduces every safety "
              "obligation to a window of at most four adjacent sections, and Z3 proves the window "
              "obligations for histories of any length; see "
              f"[the unbounded argument]({link(ROOT / 'scaling_design.md')}#unbounded-argument) and "
              f"[its results]({link(ROOT / 'results' / 'unbounded_summary.md')}). The large-scope runs "
              "below are therefore capacity measurements and full-size examples, not the basis of the "
              "safety claim.", "",
              "## Bounded correspondence", "",
              "The correspondence harnesses compare paired representations at three points, four-entry "
              "histories and six-bit integers. They compare validity, initialisation, retrieval and operation "
              "effects without assuming either post-state invariant. Their results are bounded evidence, "
              "not an unbounded equivalence theorem.", ""]
    lines += correspondence_report(evidence, link)
    lines += ["", "## Resource and interpretation limits", "",
              "Commands have independent wall-clock deadlines. The recorded JVM heap cap is not a "
              "measurement of peak process memory, and native solver allocations are additional. "
              "Some experiments ran concurrently on the same machine, so elapsed times are execution "
              "records rather than a controlled performance comparison. Baseline and optimized runs "
              "also use different history bounds in several cases.", "",
              "No completed finite scope proves eventual delivery, fairness, or complete SS7 conformance. "
              "Arbitrary network size and history length are addressed only for safety, by the separate "
              "unbounded argument. Optional polling and idle steps still permit indefinite waiting.", "",
              "## Detailed validated evidence", "", *details]
    if excluded:
        lines += ["## Earlier development attempts", "",
                  "These sources differ from the current model and are excluded from coverage above.", ""]
        lines += [f"- [{suite.name}]({link(suite / 'summary.md')})" for suite in excluded]
    if running:
        lines += ["", "## Unfinished executions", "", *[f"- `{name}`" for name in running], ""]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    verify.write_text(report_path, "\n".join(lines) + "\n")
    print(f"Revalidated {sum(len(v) for v in groups.values())} current-source attempts. Report: {report_path}")
    return 1 if running else 0


if __name__ == "__main__":
    raise SystemExit(main())
