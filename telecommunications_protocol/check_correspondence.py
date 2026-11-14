"""Run the small-scope comparison between the original and scalable models.

The runner freezes the harness and both imported models, validates each command
against its exact source and Analyzer evidence, and never overwrites baseline
reports. Timeout is an unknown result, never a successful UNSAT check.
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
MODEL_FILES = ("scaling_correspondence.als", "telecommunications.als", "telecommunications_scalable.als")
HARNESSES = {
    MODEL_FILES[0]: MODEL_FILES,
    "scaling_large_correspondence.als": ("scaling_large_correspondence.als", "telecommunications.als", "telecommunications_large.als"),
    "scaling_slots_correspondence.als": ("scaling_slots_correspondence.als", "telecommunications.als", "telecommunications_slots.als"),
}
PREFIXES = {"scaling_large_correspondence.als": "correspondence-large",
            "scaling_slots_correspondence.als": "correspondence-slots"}
JAR = ROOT / "tools" / "alloy-6.2.0.jar"


def now() -> str:
    return datetime.now(timezone(timedelta(hours=6))).isoformat(timespec="seconds")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path: Path, value: dict):
    verify.write_text(path, json.dumps(value, indent=2) + "\n")


def validate(run_dir: Path, metadata: dict) -> dict:
    errors = []
    observed = None
    source_dir = run_dir.parent / "sources"
    try:
        model_files = HARNESSES[metadata.get("harness", MODEL_FILES[0])]
        expected_files = set(model_files)
        if set(metadata.get("source_sha256", {})) != expected_files:
            errors.append("Frozen dependency hash inventory differs")
        for filename in model_files:
            if digest(source_dir / filename) != metadata.get("source_sha256", {}).get(filename):
                errors.append(f"Frozen source hash differs: {filename}")
        commands = verify.declarations((source_dir / model_files[0]).read_text(encoding="utf-8"))
        selected = [command for command in commands if command["name"] == metadata["command"]]
        if len(selected) != 1 or selected[0] != metadata["declaration"]:
            errors.append("Selected command differs from frozen harness")
    except (OSError, ValueError, KeyError) as exc:
        errors.append(f"Cannot validate source: {exc}")
    if metadata.get("status") != "completed" or metadata.get("process_exit_code") != 0:
        return {"validated": False, "observed": None, "errors": errors + [
            f"Execution not completed successfully: {metadata.get('status')}"]}
    if metadata.get("no_overflow") is not True:
        errors.append("Overflow prevention missing from execution metadata")
    try:
        receipt = json.loads((run_dir / "alloy" / "receipt.json").read_text(encoding="utf-8"))
        if receipt.get("solver") != metadata["solver"] or receipt.get("noOverflow") is not True:
            errors.append("Receipt solver or overflow setting differs")
        name = metadata["command"]
        declaration = metadata["declaration"]
        records = receipt.get("commands", {})
        if set(records) != {name}:
            errors.append("Receipt command identity differs")
        record = records.get(name, {})
        if (record.get("name") != name or record.get("type") != declaration["type"] or
                verify.normalize(record.get("source", "")) != declaration["source"]):
            errors.append("Receipt declaration or scope differs")
        width = re.search(r"\b(\d+)\s+Int\b", declaration["source"])
        sequence = re.search(r"\b(\d+)\s+seq\b", declaration["source"])
        if (not width or not sequence or record.get("bitwidth") != int(width.group(1)) or
                record.get("maxseq") != int(sequence.group(1))):
            errors.append("Receipt numeric integer or sequence scope differs")
        outcomes = verify.OUTCOME.findall((run_dir / "analyzer.log").read_text(encoding="utf-8"))
        if len(outcomes) != 1 or outcomes[0][1:3] != (declaration["type"], name):
            errors.append("Log has missing, duplicate or different command outcomes")
        else:
            observed = outcomes[0][3]
        receipt_outcome = "SAT" if record.get("solution") else "UNSAT"
        if observed != receipt_outcome:
            errors.append("Log and receipt satisfiability disagree")
        if observed != declaration["expected"]:
            errors.append("Outcome differs from declared expectation")
        if observed == "SAT":
            instances = ET.parse(run_dir / "alloy" / f"{name}-solution-0.xml").getroot().findall("instance")
            if len(instances) != 1:
                raise ValueError("Expected a single explicit-snapshot instance")
            instance = instances[0]
            if not re.match(rf"^{declaration['type']}\s+{re.escape(name)}(?:\s|$)", instance.get("command", ""), re.I):
                errors.append("Witness command identity differs")
            if int(instance.get("bitwidth", "-1")) != record.get("bitwidth") or int(instance.get("maxseq", "-1")) != record.get("maxseq"):
                errors.append("Witness integer or sequence scope differs")
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError) as exc:
        errors.append(f"Cannot validate Analyzer evidence: {exc}")
    return {"validated": not errors, "observed": observed, "errors": errors}


def run_one(suite: Path, declaration: dict, configuration: dict) -> dict:
    run_dir = suite / declaration["name"]
    run_dir.mkdir()
    model = suite / "sources" / configuration.get("harness", MODEL_FILES[0])
    argv = [configuration["java"], f"-Xmx{configuration['jvm_heap_cap_mb']}m", "-jar", str(JAR),
            "exec", "-c", declaration["name"], "-n", "-s", configuration["solver"],
            "-t", "xml", "-o", str(run_dir / "alloy"), str(model)]
    metadata = {**configuration, "format_version": 1, "command": declaration["name"],
                "declaration": declaration, "argv": argv, "status": "running", "started_at": now(),
                "process_exit_code": None, "no_overflow": True,
                "memory_note": "The JVM heap cap is configured, not measured peak memory. Native solver memory is additional."}
    save_json(run_dir / "execution.json", metadata)
    start = time.monotonic()
    process = None
    with (run_dir / "analyzer.log").open("w", encoding="utf-8", newline="\n") as log:
        try:
            process = subprocess.Popen(argv, stdout=log, stderr=subprocess.STDOUT, cwd=ROOT)
            process.wait(timeout=configuration["timeout_seconds"])
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
    rows = []
    completed = metadata["results"]
    for result in completed:
        validation = result["validation"]
        evidence = f"[{result['command']}]({result['command']}/execution.json)"
        observed = validation["observed"] or "UNKNOWN"
        verdict = "Matched" if validation["validated"] else "Incomplete or failed"
        rows.append(f"| {evidence} | {result['declaration']['expected']} | {observed} | "
                    f"{result['status']} | {result['elapsed_seconds']:.3f} | {verdict} |")
    all_ok = ([result["command"] for result in completed] == metadata["commands"] and
              all(result["validation"]["validated"] for result in completed))
    metadata["all_expectations_validated"] = all_ok
    save_json(suite / "suite.json", metadata)
    report = ["# Bounded correspondence between protocol representations", "",
              f"Run: `{suite.name}`. Status: `{metadata['status']}`.",
              f"All selected expectations and evidence validated: **{'yes' if all_ok else 'no'}**.", "",
              f"Harness: `{metadata.get('harness', MODEL_FILES[0])}`.", "",
              "These checks compare paired states under a point/message bijection and an explicit route-order relation. "
              "They do not assume either post-state invariant. SAT witnesses exercise paired operations.", "",
              "Scope: three available points in each representation, up to three message values, four-entry histories, " +
              ("six-bit integers, and exactly two states per representation in each command." if
               metadata.get("harness") in PREFIXES else
               "six-bit integers, and one or two states per representation as declared in each command."), "",
              "This is bounded conditional representation correspondence. It does not establish arbitrary-size equivalence "
              "or full enabledness equivalence for a fixed ordered pool. The original insertion may choose a fresh point "
              "whose fixed pool position is incompatible with the requested gap.", "",
              f"Timeout per command: {metadata['timeout_seconds']} seconds. JVM heap cap: {metadata['jvm_heap_cap_mb']} MiB. "
              "Heap cap is not measured peak process memory.", "",
              "| Command and evidence | Expected | Observed | Status | Seconds | Interpretation |",
              "|---|---|---|---|---:|---|", *rows, "", "## Frozen sources", ""]
    report += [f"- [{name}](sources/{name}), SHA-256 `{digest_value}`" for name, digest_value in metadata["source_sha256"].items()]
    if metadata.get("error"):
        report += ["", "## Execution issue", "", metadata["error"]]
    issues = [(result["command"], result["validation"]["errors"]) for result in completed if result["validation"]["errors"]]
    if issues:
        report += ["", "## Evidence issues", ""]
        report += [f"- `{name}`: {'; '.join(errors)}" for name, errors in issues]
    verify.write_text(suite / "summary.md", "\n".join(report) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=60)
    parser.add_argument("--heap-mb", type=int, default=2048)
    parser.add_argument("--solver", default="glucose")
    parser.add_argument("--harness", choices=sorted(HARNESSES), default=MODEL_FILES[0],
                        help="Choose the ordinary, low-arity or slot representation comparison")
    parser.add_argument("--commands", nargs="+", help="Select command names from the correspondence harness")
    parser.add_argument("--summarize", type=Path, help="Revalidate and regenerate a saved suite without running Alloy")
    args = parser.parse_args()
    if args.summarize:
        suite = args.summarize.resolve()
        metadata = json.loads((suite / "suite.json").read_text(encoding="utf-8"))
        for result in metadata["results"]:
            path = suite / result["command"]
            saved = json.loads((path / "execution.json").read_text(encoding="utf-8"))
            saved["validation"] = validate(path, saved)
            result.clear()
            result.update(saved)
            save_json(path / "execution.json", saved)
        summarize(suite, metadata)
        return 0 if metadata["all_expectations_validated"] else 1
    if args.timeout <= 0 or args.heap_mb < 128:
        parser.error("Timeout must be positive and heap cap at least 128 MiB")
    model_files = HARNESSES[args.harness]
    java = shutil.which("java")
    if not java or not JAR.is_file() or not all((ROOT / name).is_file() for name in model_files):
        parser.error("Java, Alloy JAR and all three model files are required")
    commands = verify.declarations((ROOT / model_files[0]).read_text(encoding="utf-8"))
    if args.commands:
        lookup = {item["name"]: item for item in commands}
        if len(set(args.commands)) != len(args.commands) or any(name not in lookup for name in args.commands):
            parser.error("Command names must be unique and present in the harness")
        commands = [lookup[name] for name in args.commands]
    stamp = datetime.now(timezone(timedelta(hours=6))).strftime("%Y%m%d-%H%M%S")
    prefix = PREFIXES.get(args.harness, "correspondence")
    suite = ROOT / "scale-results" / f"{prefix}-{stamp}-{uuid.uuid4().hex[:6]}"
    source_dir = suite / "sources"
    source_dir.mkdir(parents=True)
    for name in model_files:
        (source_dir / name).write_bytes((ROOT / name).read_bytes())
    configuration = {"java": java, "solver": args.solver, "timeout_seconds": args.timeout, "harness": args.harness,
                     "jvm_heap_cap_mb": args.heap_mb, "source_sha256": {name: digest(source_dir / name) for name in model_files},
                     "jar_sha256": digest(JAR)}
    configuration["java_version"] = subprocess.run([java, "-version"], capture_output=True, text=True, check=True, timeout=30).stderr.strip()
    configuration["alloy_version"] = subprocess.run([java, "-jar", str(JAR), "version"], capture_output=True, text=True, check=True, timeout=30).stdout.strip()
    metadata = {**configuration, "status": "running", "started_at": now(), "commands": [item["name"] for item in commands], "results": []}
    summarize(suite, metadata)
    print(f"Correspondence evidence: {suite}", flush=True)
    for declaration in commands:
        print(f"Running {declaration['name']}", flush=True)
        result = run_one(suite, declaration, configuration)
        metadata["results"].append(result)
        summarize(suite, metadata)
        valid = result["validation"]
        print(f"{declaration['name']}: {valid['observed'] or 'UNKNOWN'} "
              f"({result['status']}, {result['elapsed_seconds']:.3f}s, validated={valid['validated']})", flush=True)
        if result["status"] == "interrupted":
            break
    metadata.update(status="completed" if len(metadata["results"]) == len(commands) else "interrupted", finished_at=now())
    summarize(suite, metadata)
    print(f"Report: {suite / 'summary.md'}", flush=True)
    return 0 if metadata["all_expectations_validated"] else 1


if __name__ == "__main__":
    sys.exit(main())
