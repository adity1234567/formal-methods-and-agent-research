"""Decode and validate this project's demonstration XML witnesses."""
from pathlib import Path
import os
import xml.etree.ElementTree as ET


class Instance:
    def __init__(self, path: Path):
        try:
            root = ET.parse(path).getroot()
        except (OSError, ET.ParseError) as exc:
            raise ValueError(f"Cannot read XML witness {path.name}: {exc}") from exc
        instances = root.findall("instance")
        if len(instances) != 1:
            raise ValueError("Expected one explicit-snapshot instance, not multiple temporal states")
        self.fields = {}
        self.skolems = {}
        for field in instances[0].findall("field"):
            name = field.get("label")
            if name in self.fields:
                raise ValueError(f"Duplicate field {name}")
            self.fields[name] = [tuple(atom.attrib["label"] for atom in row.findall("atom"))
                                 for row in field.findall("tuple")]
        for skolem in instances[0].findall("skolem"):
            rows = skolem.findall("tuple")
            if len(rows) != 1 or len(rows[0].findall("atom")) != 1:
                raise ValueError(f"Expected a singleton atom for {skolem.get('label')}")
            self.skolems[skolem.attrib["label"]] = rows[0].find("atom").attrib["label"]
        if not {"route", "rec", "ins", "sent"}.issubset(self.fields):
            raise ValueError("Witness is missing one or more required state fields")

    def sequence(self, field: str, state: str, point: str | None = None):
        prefix = (state,) if point is None else (state, point)
        relation = self.fields[field]
        if any(len(row) != len(prefix) + 2 for row in relation):
            raise ValueError(f"Unexpected tuple arity in {field}")
        rows = [row for row in relation if row[:-2] == prefix]
        try:
            entries = sorted((int(row[-2]), row[-1]) for row in rows)
        except ValueError as exc:
            raise ValueError(f"Nonnumeric index in {field}") from exc
        indices = [index for index, _ in entries]
        if indices != list(range(len(indices))):
            raise ValueError(f"Missing, duplicate, negative, or nonfunctional sequence index in {field} at {prefix}")
        return [value for _, value in entries]


def export(run_dir: Path, *, analyzer_dir: Path | None = None):
    run_dir = run_dir.resolve()
    analyzer_dir = (analyzer_dir or run_dir).resolve()
    delivery_path = analyzer_dir / "ShowTwoMessageDelivery-solution-0.xml"
    bug_path = analyzer_dir / "BrokenReceiveWouldPreserveInvariant-solution-0.xml"
    if not delivery_path.is_file() or not bug_path.is_file():
        raise ValueError("Both delivery and intentional-bug demonstration witnesses are required")
    instance = Instance(delivery_path)
    prefix = "$ShowTwoMessageDelivery_"
    states = [instance.skolems[prefix + name] for name in "abcdefg"]
    route = instance.sequence("route", states[0])
    first_message, second_message = instance.skolems[prefix + "m1"], instance.skolems[prefix + "m2"]
    if len(route) != 2 or len(set(route)) != 2 or len(set(states)) != 7 or first_message == second_message:
        raise ValueError("Delivery witness must have two points, two distinct values, and seven snapshots")
    aliases = {first_message: "A", second_message: "B"}
    for state in states:
        if instance.sequence("route", state) != route:
            raise ValueError("Delivery route changes between snapshots")
        for point in route:
            rec, ins, sent = [instance.sequence(field, state, point) for field in ("rec", "ins", "sent")]
            if rec != ins + sent:
                raise ValueError("Displayed delivery snapshot violates local sequence accounting")
    if instance.sequence("sent", states[-2], route[-1]) != [first_message] or \
       instance.sequence("sent", states[-1], route[-1]) != [second_message, first_message]:
        raise ValueError("Witness output does not demonstrate A followed by B")

    def fmt(values, mapping=None):
        return "`[" + ", ".join((mapping or {}).get(value, value) for value in values) + "]`"

    relative_analyzer = Path(os.path.relpath(analyzer_dir, run_dir.parent)).as_posix()
    actions = ["Initialise", "Transmit A", "Transmit B", "Forward A", "Forward B", "Receive A", "Receive B"]
    lines = ["# Examples extracted from actual Alloy instances", "",
             f"Execution: `{run_dir.name}`. These tables were decoded from its XML witnesses. "
             "Every list is newest first. Snapshot names are the Analyzer's actual atom names.", "",
             "## Two-message delivery", "", f"Route: `{route[0]}` -> `{route[1]}`. A = `{first_message}`; B = `{second_message}`.", "",
             "| Step | Snapshot | Action | First queue | Last queue | Input | Output |",
             "|---|---|---|---|---|---|---|"]
    for i, state in enumerate(states):
        values = [instance.sequence("ins", state, route[0]), instance.sequence("ins", state, route[-1]),
                  instance.sequence("rec", state, route[0]), instance.sequence("sent", state, route[-1])]
        lines.append(f"| {i} | `{state}` | {actions[i]} | " + " | ".join(fmt(v, aliases) for v in values) + " |")
    lines += ["", "A is delivered before B. The final displayed output `[B,A]` records that delivery "
              "history with its newest entry first.", "", f"[Source XML]({relative_analyzer}/{delivery_path.name}).", "",
              "## Intentional newest-first bug", ""]
    bug = Instance(bug_path)
    bug_prefix = "$BrokenReceiveWouldPreserveInvariant_"
    pre, post = bug.skolems[bug_prefix + "pre"], bug.skolems[bug_prefix + "post"]
    bug_route = bug.sequence("route", pre)
    if not bug_route or bug.sequence("route", post) != bug_route:
        raise ValueError("Bug witness has no stable route")
    final_point = bug_route[-1]
    queue = bug.sequence("ins", pre, final_point)
    rec = bug.sequence("rec", pre, final_point)
    sent = bug.sequence("sent", pre, final_point)
    post_queue = bug.sequence("ins", post, final_point)
    post_sent = bug.sequence("sent", post, final_point)
    if not queue or rec != queue + sent or post_queue != queue[1:] or post_sent != [queue[0]] + sent or \
       bug.sequence("rec", post, final_point) != rec or rec == post_queue + post_sent:
        raise ValueError("Witness does not demonstrate the stated newest-first accounting failure")
    lines += [f"The correct rule removes the oldest pending occurrence (rightmost value `{queue[-1]}`). "
              f"The broken rule removes the newest occurrence (leftmost value `{queue[0]}`). "
              "Repeated values can make these endpoint values equal; their sequence positions still differ.", "",
              "| Snapshot | Received | Pending | Sent | Pending concatenated with sent |",
              "|---|---|---|---|---|"]
    for state in [pre, post]:
        received = bug.sequence("rec", state, final_point)
        pending = bug.sequence("ins", state, final_point)
        departed = bug.sequence("sent", state, final_point)
        lines.append(f"| `{state}` | {fmt(received)} | {fmt(pending)} | {fmt(departed)} | {fmt(pending + departed)} |")
    lines += ["", "The before-state satisfies received = pending concatenated with sent; the "
              "after-state violates it. This counterexample comes from the isolated buggy predicate. "
              "See [verification_summary.md](verification_summary.md) for recorded results of the correct operations.", "",
              f"[Source XML]({relative_analyzer}/{bug_path.name}).", ""]
    (run_dir.parent / "example_instances.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    import argparse
    import verify
    parser = argparse.ArgumentParser(description="Validate a recorded execution and regenerate example tables")
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    raise SystemExit(0 if verify.summarize(args.run_dir) else 1)
