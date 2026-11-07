"""Benchmark unchanged protocol predicates at larger finite scopes.

Each command gets a frozen generated model, timeout, heap cap, log, receipt,
XML evidence and independently validated outcome. Baseline reports are untouched.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import uuid
import xml.etree.ElementTree as ET

import verify

ROOT = Path(__file__).resolve().parent
MODEL = ROOT / "telecommunications.als"
JAR = ROOT / "tools" / "alloy-6.2.0.jar"
CORRECT_CHECKS = ["InitialIsValid", "RetrieveIsValid", "TransmitPreservesInvariant",
                  "ReceivePreservesInvariant", "DaemonPreservesInvariant", "InsertionPreservesInvariant",
                  "TransmitRefinesExternal", "ReceiveRefinesExternal", "DaemonIsInvisible", "InsertionIsInvisible"]
EXTRA_NAMES = ["ShowExactRouteWithTraffic", "ShowTransmitAtRouteLimit", "ShowReceiveAtRouteLimit",
               "ShowDaemonAtRouteLimit", "ShowInsertionAtRouteLimit"]


def now() -> str:
    return datetime.now(timezone(timedelta(hours=6))).isoformat(timespec="seconds")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path: Path, value: dict):
    verify.write_text(path, json.dumps(value, indent=2) + "\n")


def integer_width(points: int, sequence: int) -> tuple[int, str]:
    # Even unconstrained individually well-shaped queues can each have seq
    # entries. Cover raw offset sums, offsets plus an index and local concat.
    maximum = max(points * sequence, 2 * sequence, sequence + 1, points + 1)
    bits = max(5, maximum.bit_length() + 1)
    return bits, (f"Signed width covers raw point_count*sequence_bound={points * sequence}, "
                  f"two-sequence concatenation={2 * sequence}, and length+1. "
                  f"Required positive range >= {maximum}; chosen maximum {2 ** (bits - 1) - 1}. "
                  "This intentionally avoids relying on the invariant being proved to justify arithmetic range.")


def representation_of(source: str) -> str:
    return "ordered" if re.search(r"route\s*:\s*set\s+SPC", source) else "sequence"


def catalog(source: str, representation: str | None = None) -> dict[str, dict]:
    representation = representation or representation_of(source)
    result = {item["name"]: item for item in verify.declarations(source)}
    for name in EXTRA_NAMES if representation == "sequence" else []:
        result[name] = {"name": name, "type": "run", "expected": "SAT", "source": ""}
    return result


def additional_predicates(points: int) -> str:
    return f"""
// Scaling witnesses add scenario constraints, never a global invariant fact.
// They show satisfiability at the active-route boundary, not general reachability.
pred ShowExactRouteWithTraffic {{
  some s: State | sectionInvariant[s] and #s.route = {points} and some s.ins
}}
pred ShowTransmitAtRouteLimit {{
  some disj a,b: State, m: Message |
    #a.route = {points} and initial[a] and transmit[a,b,m] and sectionInvariant[b]
}}
pred ShowReceiveAtRouteLimit {{
  some disj a,b: State |
    #a.route = {points} and sectionInvariant[a] and receive[a,b] and sectionInvariant[b]
}}
pred ShowDaemonAtRouteLimit {{
  some disj a,b: State, p: SPC |
    #a.route = {points} and sectionInvariant[a] and daemon[a,b,p] and sectionInvariant[b]
}}
pred ShowInsertionAtRouteLimit {{
  some disj a,b: State, p,fresh: SPC |
    #a.route = {points - 1} and #b.route = {points} and sectionInvariant[a] and
    some a.ins and insertSection[a,b,p,fresh] and sectionInvariant[b]
}}
"""


def generate(source: str, name: str, points: int, messages: int, *, representation: str | None = None,
             history_bound: int = 4) -> tuple[str, dict]:
    representation = representation or representation_of(source)
    declarations = catalog(source, representation)
    item = declarations[name]
    seq = max(points, history_bound) if representation == "sequence" else history_bound
    if representation == "sequence":
        bits, rationale = integer_width(points, seq)
    else:
        bits = max(5, (2 * seq + 1).bit_length() + 1)
        rationale = (f"Ordered SPC atoms do not use integer route positions or cardinality. "
                     f"History length is {seq}; signed range covers local concatenation up to {2 * seq} "
                     "and history length+1. The model's telescoping offset uses history lengths, not point count.")
    declared_states = re.search(r"exactly\s+(\d+)\s+State", item["source"])
    if declared_states:
        states = int(declared_states.group(1))
    elif name in {"InitialIsValid", "RetrieveIsValid", "ShowExactRouteWithTraffic"}:
        states = 1
    elif name == "ShowRepeatedMessageValue":
        states = 3
    elif name == "ShowTwoMessageDelivery":
        states = 7
    else:
        states = 2
    message_scope = "exactly 1 Message" if name == "ShowRepeatedMessageValue" else (
        "exactly 2 Message" if name == "ShowTwoMessageDelivery" else f"{messages} Message")
    if name == "ShowTwoMessageDelivery" and messages < 2:
        raise ValueError("ShowTwoMessageDelivery requires --messages at least 2")
    scope = f"for {messages} but {points} SPC, {message_scope}, exactly {states} State, {bits} Int, {seq} seq"
    command = f"{item['type']} {name} {scope}"
    body = "\n".join(line for line in source.splitlines()
                     if not verify.COMMAND.fullmatch(line.strip()) and
                     not line.startswith("// Bounds:") and not line.startswith("// signed 5-bit"))
    generated = ("// Generated scaling experiment. Scope below replaces the baseline analysis commands.\n" +
                 body + "\n" + (additional_predicates(points) if representation == "sequence" else "") + "\n" +
                 command + (" expect 1\n" if item["expected"] == "SAT" else " expect 0\n"))
    details = {"command": name, "command_type": item["type"], "expected": item["expected"],
               "command_source": command, "points_bound": points, "message_values_bound": messages,
               "sequence_bound": seq, "integer_bitwidth": bits, "integer_width_rationale": rationale,
               "states": states, "representation": representation,
               "exact_route_witness": name in EXTRA_NAMES or name.startswith("ShowFullRoute")}
    return generated, details


def exact_route_evidence(instance: ET.Element, name: str, points: int) -> list[int]:
    fields = {field.get("label"): field for field in instance.findall("field")}
    pending_fields = [fields[label] for label in ("ins", "insBefore", "insAfter") if label in fields]
    if "route" not in fields or not pending_fields:
        raise ValueError("Exact-size witness is missing route or pending fields")
    signatures = instance.findall("sig")
    def signature_atoms(label: str) -> list[str]:
        selected = [sig for sig in signatures if sig.get("label", "").split("/")[-1] == label]
        ids = {sig.get("ID") for sig in selected if sig.get("ID") is not None}
        # Alloy can put atoms only on descendants of abstract signatures.
        while True:
            children = [sig for sig in signatures if sig not in selected and
                        sig.get("parentID") is not None and sig.get("parentID") in ids]
            if not children:
                break
            selected.extend(children)
            ids.update(sig.get("ID") for sig in children if sig.get("ID") is not None)
        return list(dict.fromkeys(atom.get("label") for sig in selected for atom in sig.findall("atom")
                                  if atom.get("label") is not None))

    states = signature_atoms("State")
    if not states:
        raise ValueError("Exact-size witness has no State atoms")
    routes = {state: [] for state in states}
    for row in fields["route"].findall("tuple"):
        atoms = [atom.get("label") for atom in row.findall("atom")]
        if len(atoms) not in {2, 3} or atoms[0] not in routes:
            raise ValueError("Malformed route tuple")
        routes[atoms[0]].append((int(atoms[1]), atoms[2]) if len(atoms) == 3 else
                                (len(routes[atoms[0]]), atoms[1]))
    for route in routes.values():
        route.sort()
        if [index for index, _ in route] != list(range(len(route))) or len({p for _, p in route}) != len(route):
            raise ValueError("Exact route is noncontiguous or contains repeated points")

    # These predicates choose one s even in a model with mandatory Before and
    # After slots. Validate the actual skolem, never an unused full-size slot.
    if name in {"ShowExactRouteWithTraffic", "ShowFullRouteWithTraffic"}:
        skolems = [skolem for skolem in instance.findall("skolem") if skolem.get("label") == f"${name}_s"]
        rows = skolems[0].findall("tuple") if len(skolems) == 1 else []
        atoms = rows[0].findall("atom") if len(rows) == 1 else []
        state = atoms[0].get("label") if len(atoms) == 1 else None
        if state not in routes:
            raise ValueError("Exact-size witness has no unique selected-state skolem")
        route = routes[state]
        if len(route) != points:
            raise ValueError(f"Selected active route length differs: {len(route)}, expected {points}")
        active_points = {point for _, point in route}
        if "ins" in fields:
            has_traffic = any(len(row.findall("atom")) == 4 and
                              row.findall("atom")[0].get("label") == state and
                              row.findall("atom")[1].get("label") in active_points
                              for row in fields["ins"].findall("tuple"))
        else:
            slots = [slot for slot in ("Before", "After") if state in signature_atoms(slot)]
            if len(slots) != 1 or f"ins{slots[0]}" not in fields:
                raise ValueError("Cannot map selected State to its Before/After pending field")
            has_traffic = any(len(row.findall("atom")) == 3 and
                              row.findall("atom")[0].get("label") in active_points
                              for row in fields[f"ins{slots[0]}"].findall("tuple"))
        if not has_traffic:
            raise ValueError("Selected exact-size traffic witness contains no pending traffic")
        return [len(route)]

    lengths = [len(routes[state]) for state in states]
    expected = [points - 1, points] if name in {"ShowInsertionAtRouteLimit", "ShowFullRouteInsertion"} else [points] * len(states)
    if sorted(lengths) != sorted(expected):
        raise ValueError(f"Active route length differs: {lengths}, expected {expected}")
    if name in {"ShowExactRouteWithTraffic", "ShowInsertionAtRouteLimit", "ShowFullRouteWithTraffic",
                "ShowFullRouteInsertion", "ShowFullRoutePendingPoll"} and not any(
                    field.findall("tuple") for field in pending_fields):
        raise ValueError("Exact-size traffic witness contains no pending traffic")
    return lengths


def validate(run_dir: Path, metadata: dict) -> dict:
    errors = []
    observed = None
    lengths = None
    source_path = run_dir / "telecommunications.als"
    try:
        if digest(source_path) != metadata["model_sha256"]:
            errors.append("Generated model hash differs")
        # Saved Windows evidence must also revalidate on POSIX checkouts.
        original_path = run_dir / metadata["original_source_file"].replace("\\", "/")
        if digest(original_path) != metadata["original_sha256"]:
            errors.append("Frozen original hash differs")
        declarations = verify.declarations(source_path.read_text(encoding="utf-8"))
        if len(declarations) != 1 or declarations[0]["source"] != verify.normalize(metadata["command_source"]):
            errors.append("Generated command differs from execution metadata")
        if len(declarations) != 1 or declarations[0]["expected"] != metadata["expected"]:
            errors.append("Generated expectation differs from execution metadata")
        # A file matching its recorded hash is insufficient: scope labels could
        # be stale, or both an altered generated file and its hash could agree.
        # Rebuild from the frozen original, deriving representation from that
        # source, and bind every reported scope/detail to the actual generated
        # model. This also rejects silently injected facts or changed predicates.
        original_source = original_path.read_text(encoding="utf-8")
        regenerated, derived = generate(original_source, metadata["command"], metadata["points_bound"],
                                        metadata["message_values_bound"],
                                        representation=representation_of(original_source),
                                        history_bound=metadata["sequence_bound"])
        if source_path.read_bytes() != regenerated.encode("utf-8"):
            errors.append("Generated model differs from deterministic regeneration of frozen original and scopes")
        for field, value in derived.items():
            if metadata.get(field) != value:
                errors.append(f"Derived execution detail differs: {field}")
    except (OSError, ValueError, KeyError, TypeError, OverflowError) as exc:
        errors.append(f"Cannot validate frozen sources: {exc}")
    if metadata.get("status") != "completed" or metadata.get("process_exit_code") != 0:
        return {"validated": False, "observed": None, "errors": errors + [
            f"Execution not completed successfully: {metadata.get('status')}"], "active_route_lengths": None}
    if metadata.get("no_overflow") is not True:
        errors.append("Execution metadata does not confirm overflow prevention")
    try:
        receipt = json.loads((run_dir / "alloy" / "receipt.json").read_text(encoding="utf-8"))
        if receipt.get("solver") != metadata["solver"] or receipt.get("noOverflow") is not True:
            errors.append("Receipt solver or overflow-prevention setting differs")
        commands = receipt.get("commands", {})
        name = metadata["command"]
        if set(commands) != {name}:
            errors.append("Receipt command identities differ")
        record = commands.get(name, {})
        if (record.get("name") != name or record.get("type") != metadata["command_type"] or
                verify.normalize(record.get("source", "")) != verify.normalize(metadata["command_source"])):
            errors.append("Receipt command/type/scope differs")
        if record.get("bitwidth") != metadata["integer_bitwidth"] or record.get("maxseq") != metadata["sequence_bound"]:
            errors.append("Receipt sequence or integer scope differs")
        log = (run_dir / "analyzer.log").read_text(encoding="utf-8")
        outcomes = verify.OUTCOME.findall(log)
        if len(outcomes) != 1 or int(outcomes[0][0]) != 0 or outcomes[0][1:3] != (metadata["command_type"], name):
            errors.append("Log has missing, duplicate or wrong command outcomes")
        else:
            observed = outcomes[0][3]
        receipt_outcome = "SAT" if record.get("solution") else "UNSAT"
        if receipt_outcome != observed:
            errors.append("Receipt and log outcomes disagree")
        if observed != metadata["expected"]:
            errors.append("Outcome differs from declared expectation")
        if observed == "SAT":
            xml = run_dir / "alloy" / f"{name}-solution-0.xml"
            instances = ET.parse(xml).getroot().findall("instance")
            if len(instances) != 1:
                raise ValueError("Expected one explicit-snapshot XML instance")
            instance = instances[0]
            if not re.match(rf"^{metadata['command_type']}\s+{re.escape(name)}(?:\s|$)", instance.get("command", ""), re.I):
                errors.append("SAT XML command identity differs")
            if int(instance.get("bitwidth", "-1")) != metadata["integer_bitwidth"] or int(instance.get("maxseq", "-1")) != metadata["sequence_bound"]:
                errors.append("SAT XML integer or sequence scope differs")
            if metadata.get("exact_route_witness"):
                lengths = exact_route_evidence(instance, name, metadata["points_bound"])
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as exc:
        errors.append(f"Cannot validate Analyzer evidence: {exc}")
    return {"validated": not errors, "observed": observed, "errors": errors, "active_route_lengths": lengths}


def run_command(run_dir: Path, generated: str, details: dict, *, original: Path, java: str,
                jar: Path, solver: str, timeout: float, heap_mb: int) -> dict:
    run_dir.mkdir(parents=True, exist_ok=False)
    model = run_dir / "telecommunications.als"
    model.write_text(generated, encoding="utf-8", newline="\n")
    argv = [java, f"-Xmx{heap_mb}m", "-jar", str(jar), "exec", "-c", "0", "-n", "-s", solver,
            "-t", "xml", "-o", str(run_dir / "alloy"), str(model)]
    import os
    original_relative = Path(os.path.relpath(original, run_dir)).as_posix()
    metadata = {"format_version": 1, **details, "status": "running", "started_at": now(),
                "solver": solver, "no_overflow": True, "argv": argv, "timeout_seconds": timeout,
                "jvm_heap_cap_mb": heap_mb, "peak_process_memory_bytes": None,
                "memory_note": "Heap cap is configured, not measured peak process memory; native solver allocation is additional.",
                "model_sha256": digest(model), "original_sha256": digest(original),
                "original_source_file": original_relative, "jar_sha256": digest(jar), "process_exit_code": None}
    save_json(run_dir / "execution.json", metadata)
    start = time.monotonic()
    process = None
    with (run_dir / "analyzer.log").open("w", encoding="utf-8", newline="\n") as log:
        try:
            process = subprocess.Popen(argv, stdout=log, stderr=subprocess.STDOUT, cwd=ROOT)
            metadata["process_exit_code"] = process.wait(timeout=timeout)
            metadata["status"] = "completed" if process.returncode == 0 else "failed"
        except subprocess.TimeoutExpired:
            metadata["status"] = "timed_out"
        except KeyboardInterrupt:
            metadata["status"] = "interrupted"
        except OSError as exc:
            metadata.update(status="failed", error=f"{type(exc).__name__}: {exc}")
        finally:
            if process is not None and process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
            if process is not None:
                metadata["process_exit_code"] = process.returncode
            metadata.update(elapsed_seconds=round(time.monotonic() - start, 3), finished_at=now())
    metadata["validation"] = validate(run_dir, metadata)
    save_json(run_dir / "execution.json", metadata)
    return metadata


def summarize(suite: Path, metadata: dict):
    runs = metadata["runs"]
    planned = {(points, command) for points in metadata["points"] for command in metadata["commands"]}
    observed = {(r["points_bound"], r["command"]) for r in runs}
    metadata["planned_run_count"] = len(planned)
    metadata["recorded_run_count"] = len(runs)
    metadata["all_expectations_validated"] = (bool(metadata.get("finished_at")) and
        not metadata.get("dry_run", False) and len(runs) == len(planned) and observed == planned and
        all(r["validation"]["validated"] for r in runs))
    save_json(suite / "summary.json", metadata)
    lines = ["# Scaling benchmark", "", f"Original model SHA-256: `{metadata['original_sha256']}`.", "",
             "Each command has its own wall-clock timeout. Timed-out or failed commands have no verified outcome. "
             "Heap values are JVM caps, not measurements of peak process memory. Native solver allocations are additional.", "",
             "Scopes bound available SPC atoms. Only the separately named exact-route witnesses require the active "
             "route to reach the boundary. These witnesses demonstrate existence, not general initialised reachability.", "",
             f"Representation: `{metadata['representation']}`. In sequence mode the route and histories share a "
             "sequence bound. Ordered mode uses the selected independent history bound. All results remain finite-scope evidence.", "",
             "| SPC bound | seq | Int bits | Command | Expected | Observed | Status | Seconds | Validated |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in runs:
        v = r["validation"]
        lines.append(f"| {r['points_bound']} | {r['sequence_bound']} | {r['integer_bitwidth']} | {r['command']} | "
                     f"{r['expected']} | {v['observed'] or 'UNKNOWN'} | {r['status']} | {r['elapsed_seconds']} | "
                     f"{'yes' if v['validated'] else 'no'} |")
    lines += ["", "Per-command directories retain generated sources, execution metadata, raw logs and all available Analyzer evidence.", ""]
    verify.write_text(suite / "summary.md", "\n".join(lines))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--points", type=int, nargs="+", default=[6, 8, 10])
    parser.add_argument("--messages", type=int, default=4)
    parser.add_argument("--model", type=Path, default=MODEL)
    parser.add_argument("--representation", choices=["auto", "sequence", "ordered"], default="auto")
    parser.add_argument("--history-bound", type=int, default=4, help="Independent history length in ordered mode; minimum shared length in sequence mode")
    parser.add_argument("--commands", nargs="+", default=["all"], help="Names, all, or checks")
    parser.add_argument("--timeout", type=float, default=60, help="Seconds per command, default 60")
    parser.add_argument("--heap-mb", type=int, default=2048, help="JVM heap cap, default 2048 MiB")
    parser.add_argument("--solver", default="sat4j", help="Default sat4j; glucose also supported")
    parser.add_argument("--output", type=Path, default=ROOT / "scale-results")
    parser.add_argument("--dry-run", action="store_true", help="Generate sources and plan without running Java")
    args = parser.parse_args(argv)
    if (min(args.points) < 3 or len(set(args.points)) != len(args.points) or args.messages < 1 or
            args.history_bound < 1 or args.timeout <= 0 or args.heap_mb < 128):
        parser.error("points must be >=3, messages/history-bound >=1, timeout >0 and heap-mb >=128")
    original_bytes = args.model.resolve().read_bytes()
    source = original_bytes.decode("utf-8")
    representation = representation_of(source)
    if args.representation != "auto" and args.representation != representation:
        parser.error("Selected representation differs from the model's route declaration")
    available = catalog(source, representation)
    selected = list(available) if args.commands == ["all"] else (
        [name for name in CORRECT_CHECKS if name in available] if args.commands == ["checks"] else args.commands)
    if any(name not in available for name in selected) or len(set(selected)) != len(selected):
        parser.error("Unknown or duplicate command. Available: " + ", ".join(available))
    java = shutil.which("java")
    if not args.dry_run and (not java or not JAR.is_file()):
        parser.error("Java and tools/alloy-6.2.0.jar are required")
    suite = args.output.resolve() / f"scale-{datetime.now(timezone(timedelta(hours=6))):%Y%m%d-%H%M%S}-{uuid.uuid4().hex[:6]}"
    suite.mkdir(parents=True)
    original = suite / "original-model.als"
    original.write_bytes(original_bytes)
    suite_meta = {"format_version": 1, "started_at": now(), "original_sha256": digest(original),
                  "model": str(args.model.resolve()), "representation": representation,
                  "points": args.points, "commands": selected, "solver": args.solver,
                  "timeout_seconds": args.timeout, "jvm_heap_cap_mb": args.heap_mb, "runs": []}
    print(f"Scaling suite: {suite}", flush=True)
    for points in args.points:
        for name in selected:
            generated, details = generate(source, name, points, args.messages,
                                          representation=representation, history_bound=args.history_bound)
            target = suite / f"points-{points}" / name
            if args.dry_run:
                target.mkdir(parents=True)
                (target / "telecommunications.als").write_text(generated, encoding="utf-8", newline="\n")
                save_json(target / "plan.json", details)
                print(details["command_source"], flush=True)
                continue
            result = run_command(target, generated, details, original=original, java=java, jar=JAR,
                                 solver=args.solver, timeout=args.timeout, heap_mb=args.heap_mb)
            suite_meta["runs"].append(result)
            summarize(suite, suite_meta)
            print(f"{points:4} SPC {name}: {result['status']}, "
                  f"{result['validation']['observed'] or 'UNKNOWN'}, {result['elapsed_seconds']}s, "
                  f"validated={result['validation']['validated']}", flush=True)
            if result["status"] == "interrupted":
                suite_meta["finished_at"] = now()
                summarize(suite, suite_meta)
                return 130
    suite_meta.update(finished_at=now(), dry_run=args.dry_run)
    summarize(suite, suite_meta)
    print(f"Summary: {suite / 'summary.md'}", flush=True)
    return 0 if args.dry_run or suite_meta["all_expectations_validated"] else 1


if __name__ == "__main__":
    sys.exit(main())
