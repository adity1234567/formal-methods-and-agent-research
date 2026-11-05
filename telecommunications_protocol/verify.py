"""Run Alloy against a frozen source copy and retain verifiable evidence.

Each run saves source before launching Alloy, streams its log to disk, and
records completion, interruption, or failure. No third-party packages required.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parent
MODEL = ROOT / "telecommunications.als"
JAR = ROOT / "tools" / "alloy-6.2.0.jar"
RESULTS = ROOT / "results"
COMMAND = re.compile(r"^\s*(check|run)\s+(\w+)\s+(.+?)\s+expect\s+([01])\s*$")
# SAT progress contains backspaces and a counter such as 1/1 before the result.
OUTCOME = re.compile(r"^\s*(\d+)\.\s+(check|run)\s+(\w+)[^\r\n]*?\b(UNSAT|SAT)\b", re.M)


def now() -> str:
    return datetime.now(timezone(timedelta(hours=6))).isoformat(timespec="seconds")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_text(path: Path, text: str):
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def save_metadata(run_dir: Path, metadata: dict):
    write_text(run_dir / "execution.json", json.dumps(metadata, indent=2))


def normalize(text: str) -> str:
    return " ".join(text.split())


def declarations(source: str) -> list[dict]:
    commands = []
    # Project convention: one named command per line with an explicit expect.
    # Reject unsupported declarations rather than silently skipping them.
    without_comments = re.sub(r"/\*.*?\*/", "", source, flags=re.S)
    for number, line in enumerate(without_comments.splitlines(), 1):
        line = line.split("//", 1)[0].strip()
        if not re.match(r"^(check|run)\b", line):
            continue
        match = COMMAND.fullmatch(line)
        if not match:
            raise ValueError(f"Unsupported command at line {number}: use a named, single-line command with expect 0 or 1")
        kind, name, scope, expectation = match.groups()
        commands.append({"type": kind, "name": name, "expected": "SAT" if expectation == "1" else "UNSAT",
                         "source": normalize(f"{kind} {name} {scope}")})
    if not commands or len({item["name"] for item in commands}) != len(commands):
        raise ValueError("Commands must have unique names and at least one command is required")
    return commands


def read_json(path: Path, errors: list[str], description: str) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError("expected a JSON object")
        return value
    except (OSError, ValueError) as exc:
        errors.append(f"Cannot read {description}: {exc}")
        return {}


def summarize(run_dir: Path) -> bool:
    """Validate a saved execution; never attribute it to the live model."""
    run_dir = run_dir.resolve()
    errors: list[str] = []
    metadata = read_json(run_dir / "execution.json", errors, "execution metadata")
    snapshot = run_dir / metadata.get("source_file", "telecommunications.als")
    analyzer_dir = run_dir / metadata.get("analyzer_output", ".")
    receipt = read_json(analyzer_dir / "receipt.json", errors, "Analyzer receipt")
    recorded = receipt.get("commands", {})
    if not isinstance(recorded, dict):
        errors.append("Receipt commands are not an object")
        recorded = {}
    commands = []
    digest = "unavailable"
    try:
        digest = sha256(snapshot)
        commands = declarations(snapshot.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        errors.append(f"Cannot validate frozen source: {exc}")
    if digest != metadata.get("model_sha256"):
        errors.append("Frozen source hash does not match the hash recorded for execution")
    # Legacy evidence lacks a status field but has an exit code and saved hash.
    status = metadata.get("status", "completed" if metadata.get("process_exit_code") == 0 else "failed")
    if status != "completed" or metadata.get("process_exit_code") != 0:
        errors.append(f"Execution was not completed successfully (status={status}, exit={metadata.get('process_exit_code')})")
    if metadata.get("error"):
        errors.append(str(metadata["error"]))
    if receipt.get("solver") != metadata.get("solver"):
        errors.append("Receipt solver does not match execution metadata")
    if receipt.get("noOverflow") is not True or metadata.get("no_overflow") is not True:
        errors.append("Overflow prevention is not confirmed in both receipt and metadata")
    try:
        log = (run_dir / "analyzer.log").read_text(encoding="utf-8")
    except OSError as exc:
        log = ""
        errors.append(f"Cannot read Analyzer log: {exc}")
    outcomes = OUTCOME.findall(log)
    actual: dict[str, tuple[str, str]] = {}
    for index, kind, name, result in outcomes:
        if name in actual:
            errors.append(f"Duplicate outcome for {name}")
        actual[name] = (kind, result)
    expected_names = [command["name"] for command in commands]
    if [name for _, _, name, _ in outcomes] != expected_names:
        errors.append("Completed log commands do not match the frozen source's command sequence")
    if [int(index) for index, _, _, _ in outcomes] != list(range(len(commands))):
        errors.append("Log command indices are missing, duplicated, or out of order")
    if set(recorded) != set(expected_names):
        errors.append("Receipt command names do not match the frozen source")

    rows = []
    for command in commands:
        name, kind, expected = command["name"], command["type"], command["expected"]
        actual_kind, result = actual.get(name, ("", "NOT COMPLETED"))
        record = recorded.get(name, {})
        command_errors = []
        if actual_kind != kind or result != expected:
            command_errors.append("result/type does not match expectation")
        if not isinstance(record, dict):
            record = {}
        if record.get("type") != kind or record.get("name") != name:
            command_errors.append("receipt identity/type differs")
        if normalize(record.get("source", "")) != command["source"]:
            command_errors.append("receipt command or scope differs from frozen source")
        receipt_result = "SAT" if record.get("solution") else "UNSAT"
        if result in {"SAT", "UNSAT"} and receipt_result != result:
            command_errors.append("receipt and log disagree on satisfiability")
        if result == "SAT":
            witness = analyzer_dir / f"{name}-solution-0.xml"
            if not witness.is_file():
                command_errors.append("SAT result has no saved XML witness")
            else:
                try:
                    import xml.etree.ElementTree as ET
                    instance = ET.parse(witness).getroot().find("instance")
                    if instance is None or not re.match(rf"^{kind}\s+{re.escape(name)}(?:\s|$)", instance.get("command", ""), re.I):
                        raise ValueError("XML command identity differs")
                except (OSError, ValueError, ET.ParseError) as exc:
                    command_errors.append(f"invalid XML witness: {exc}")
        errors.extend(f"{name}: {message}" for message in command_errors)
        meaning = "Expected counterexample found" if kind == "check" and expected == "SAT" else (
            "No counterexample in scope" if kind == "check" else "Witness found")
        if command_errors:
            meaning = "Incomplete or inconsistent evidence"
        rows.append(f"| `{name}` | {kind} | {expected} | {result} | {meaning} |")

    relative_run = Path(os.path.relpath(run_dir, RESULTS)).as_posix()
    relative_analyzer = Path(os.path.relpath(analyzer_dir, RESULTS)).as_posix()
    if not errors:
        try:
            from export_instances import export
            export(run_dir, analyzer_dir=analyzer_dir)
        except (OSError, ValueError, KeyError) as exc:
            errors.append(f"Cannot validate/export demonstration instances: {exc}")
    all_ok = not errors
    if not all_ok:
        write_text(RESULTS / "example_instances.md", "# Example instances unavailable for this execution\n\n"
                   f"Run: `{run_dir.name}`. Execution or evidence validation is incomplete. "
                   "No previous example table is being presented as output of this run. "
                   "See [verification_summary.md](verification_summary.md).\n")
    live_matches = MODEL.is_file() and sha256(MODEL) == digest
    report = ["# Recorded Alloy verification", "", f"Report generated: {now()} (Asia/Dhaka, UTC+06:00).",
              f"Overall: **{'PASS - all declared expectations and evidence checks matched' if all_ok else 'INCOMPLETE OR FAILED - inspect the issues below'}**.", "",
              f"Run: `{run_dir.name}`. Execution status: `{status}`. Process exit code: `{metadata.get('process_exit_code')}`.",
              f"Alloy version: `{metadata.get('alloy_version', 'unknown')}`; solver: `{metadata.get('solver', 'unknown')}`.",
              f"Frozen model SHA-256: `{digest}`.",
              f"Live workspace model matches this saved source: **{'yes' if live_matches else 'no; results apply only to the saved source'}**.", "",
              "Results below are checked against the source saved with this execution, process status, raw log, "
              "receipt, and SAT witness files. Arithmetic overflow prevention "
              f"is {'confirmed' if receipt.get('noOverflow') is True and metadata.get('no_overflow') is True else 'not confirmed'}.", "",
              "| Command | Type | Expected | Observed | Interpretation |", "|---|---|---|---|---|", *rows, "",
              "## Exact commands and bounds", "",
              "These commands are read from the saved model; their scopes are compared with the Analyzer receipt. "
              "A UNSAT check means no counterexample within its finite scope. A SAT run demonstrates a possible "
              "instance. Neither establishes an unbounded proof or eventual delivery.", "", "```alloy",
              *[command["source"] + (" expect 1" if command["expected"] == "SAT" else " expect 0") for command in commands],
              "```", ""]
    if errors:
        report += ["## Evidence issues", "", *[f"- {error}" for error in dict.fromkeys(errors)], ""]
    report += ["## Raw evidence", "", f"- [Analyzer log]({relative_run}/analyzer.log)",
               f"- [Analyzer receipt]({relative_analyzer}/receipt.json)",
               f"- [Saved model]({relative_run}/{snapshot.name})",
               f"- [Execution metadata]({relative_run}/execution.json)", "",
               "SAT commands have XML witnesses beside the receipt. "
               "[Readable demonstration instances](example_instances.md) are regenerated only after evidence validation succeeds.", ""]
    write_text(RESULTS / "verification_summary.md", "\n".join(report))
    return all_ok


def invocation(argv: list[str]) -> str | list[str]:
    if os.name != "nt":
        return argv
    # Preserve quotes around * for Windows Java; no shell is used.
    return " ".join('"*"' if arg == "*" else subprocess.list2cmdline([arg]) for arg in argv)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", default="glucose", help="Alloy solver ID; sat4j uses the pure Java solver")
    parser.add_argument("--summarize", type=Path, help="Validate/regenerate reports from an existing execution directory")
    args = parser.parse_args()
    RESULTS.mkdir(exist_ok=True)
    if args.summarize is not None:
        return 0 if summarize(args.summarize) else 1
    java = shutil.which("java")
    if not java or not JAR.is_file() or not MODEL.is_file():
        parser.error("Java, tools/alloy-6.2.0.jar, and telecommunications.als must be available")
    stamp = datetime.now(timezone(timedelta(hours=6))).strftime("%Y%m%d-%H%M%S")
    run_dir = RESULTS / f"run-{stamp}-{uuid.uuid4().hex[:6]}"
    run_dir.mkdir()
    snapshot = run_dir / "telecommunications.als"
    snapshot.write_bytes(MODEL.read_bytes())
    argv = [java, "-jar", str(JAR), "exec", "-c", "*", "-n", "-s", args.solver,
            "-t", "xml", "-o", str(run_dir / "alloy"), str(snapshot)]
    metadata = {"format_version": 2, "status": "running", "started_at": now(), "argv": argv,
                "process_exit_code": None, "solver": args.solver, "no_overflow": True,
                "source_file": snapshot.name, "analyzer_output": "alloy", "model_sha256": sha256(snapshot),
                "jar_sha256": sha256(JAR)}
    save_metadata(run_dir, metadata)
    write_text(RESULTS / "verification_summary.md", f"# Verification in progress\n\nRun: `{run_dir.name}`. "
               "No final result is available for this execution yet.\n")
    write_text(RESULTS / "example_instances.md", "# Examples pending\n\nThe current execution has not completed.\n")
    print(f"Running frozen source; saving evidence in {run_dir}", flush=True)
    process = None
    with (run_dir / "analyzer.log").open("w", encoding="utf-8") as log:
        try:
            declarations(snapshot.read_text(encoding="utf-8"))
            metadata["java_version"] = subprocess.run([java, "-version"], capture_output=True, text=True,
                                                      check=True, timeout=30).stderr.strip()
            metadata["alloy_version"] = subprocess.run([java, "-jar", str(JAR), "version"], capture_output=True,
                                                       text=True, check=True, timeout=30).stdout.strip()
            save_metadata(run_dir, metadata)
            process = subprocess.Popen(invocation(argv), cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       text=True, encoding="utf-8", errors="replace")
            assert process.stdout is not None
            for line in process.stdout:
                log.write(line)
                log.flush()
                print(line, end="", flush=True)
            metadata["process_exit_code"] = process.wait()
            metadata["status"] = "completed" if process.returncode == 0 else "failed"
        except KeyboardInterrupt:
            metadata["status"] = "interrupted"
            metadata["error"] = "Verification was interrupted before completion"
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            metadata["status"] = "failed"
            metadata["error"] = f"{type(exc).__name__}: {exc}"
        finally:
            if process is not None and process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=10)
                metadata["process_exit_code"] = process.returncode
            metadata["finished_at"] = now()
            save_metadata(run_dir, metadata)
    ok = summarize(run_dir)
    print(f"\n{'PASS' if ok else 'INCOMPLETE/FAIL'}: {RESULTS / 'verification_summary.md'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
