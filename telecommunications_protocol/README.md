# Telecommunications Protocol in Alloy

Course project based on Jim Woodcock and Jim Davies, *Using Z: Specification,
Refinement, and Proof*, Chapter 20, “A Telecommunications Protocol,” printed
pages 321–329. Prepared 3 November 2026.

## Start here

- `telecommunications.als`: the executable Alloy model and its analysis commands.
- `presentation_notes.md`: slide outline, speaking notes, demonstration, and viva preparation.
- `results/verification_summary.md`: actual Analyzer results, scopes, and limitations.
- `results/example_instances.md`: readable delivery and bug examples extracted from the saved XML instances.
- `audit_report.md`: completed review, corrections, and validation evidence.
- `verify.py` / `verify.ps1`: repeat the analysis and save its evidence.
- [Source reference guide](references/README.md): links to the book used for this work.

This package was created for the assignment. Its completed work is recorded in
the verification summary; it does not establish what your group had completed
before this conversation. Add your group name and members before presenting.

## What problem are we solving?

Chapter 20 studies a small abstraction of Signalling System No. 7 (SS7), which
supports signalling between telephone exchanges. Messages enter a route, wait
inside sections, move between neighbouring sections, and leave at the other end.
The project asks whether that internal design respects the service described by
the external specification. This is a model of selected behaviour, rather than
an implementation of the complete SS7 standard.

The external state has input and output histories. Newest messages appear on
the **left**. Its invariant says that the output history is a suffix of the input
history. For example, input `[C,B,A]` and output `[B,A]` mean that A then B were
delivered, while C remains pending. The sectional model explains where pending
messages are held. A retrieve relation connects the two views. Section 20.4 adds
a new empty section between existing neighbours without changing the externally
visible histories.

Source: [Using Z, Chapter 20](https://dsc.ufcg.edu.br/~dalton/bib/woodcock96.pdf#page=335).
The public PDF's page 335 is printed page 321. The author/title record is also
available from [Oxford](https://www.cs.ox.ac.uk/publications/publication2249-abstract.html).
For mathematical notation, consult the PDF. The plain-text extraction can
flatten symbols and grouping; it is a reading aid rather than an authoritative
transcription. See [extraction notes](references/extraction_notes.md).

## How to explain the model

Start with three boxes and a message moving from left to right:

```mermaid
flowchart LR
    User[Submit message] --> A[Section A]
    A -->|Daemon0| B[Section B]
    B -->|Daemon0| C[Section C]
    C -->|SReceive| Receiver[Delivered history]
```

Each box has three message sequences: two histories and a pending queue.
`rec` records arrivals, `ins` contains pending messages, and `sent` records
departures. A message leaves a box by taking the
**rightmost**, oldest pending element. It enters the next box at the **left**.
Adding on the left and removing on the right implements a FIFO queue.

The important relationships to point to in the implementation are:

| Relationship | Meaning in the implementation |
|---|---|
| `rec[p] = ins[p] ++ sent[p]` | A section's arrival history is its pending sequence followed by its departure history. `++` here denotes sequence concatenation, not Alloy override. |
| `sent[p] = rec[next]` | A departure from one section is the same arrival at its neighbour. |
| `input = rec[first]` | Observe the input boundary. |
| `output = sent[last]` | Observe the output boundary. |

These are ordered sequences, not sets: sets would discard order and repeated
occurrences. Two submissions may have the same `Message` value. A sound model
must retain both occurrences by their indices.

## Implementation approach

The `.als` file uses explicit `State` snapshots. An operation relates a before
state to an after state. This makes the Z before/after convention easy to trace
and avoids requiring temporal Alloy syntax to understand the project.

The route is a nonempty sequence of distinct signalling point codes. Histories
are indexed by point identity. Consequently, insertion changes the route order
while existing points retain their own histories. This is a deliberate change
of representation from the book's parallel, position-indexed sequences; the
route still determines which point is first, last, or adjacent to another.

The sectional state invariant is a named predicate. It is **not imposed on all states as
a global fact**. An invariant-preservation assertion assumes the predicate for
the before state, applies a sectional operation, and asks whether the predicate holds for
the after state. If it were assumed for every state, a broken operation could
be excluded from the search before the assertion examined it.

Operation predicates specify changes and frame conditions. A frame condition
states which fields retain their previous values. Alloy does not automatically
keep an unmentioned field unchanged. In a forwarding step, for example, moving
the pending message requires corresponding updates to the sender's departure
history and the receiver's arrival history.

The sectional operations have a **valid-before-state contract**: callers use
them together with `sectionInvariant[pre]`, or after `initial` and a sequence
of valid transitions. The predicates themselves deliberately omit that
invariant. In the Analyzer, run the supplied `Show*` scenarios rather than a
bare operation such as `transmit`, whose unconstrained inputs need not describe
a valid protocol state.

Finite sequences have a maximum length in an Alloy command. The operations use
capacity guards so that a sequence helper cannot silently discard data when a
history reaches that limit. These guards describe the finite analysis boundary;
they are not intended as a buffer-capacity requirement for SS7.
For example, `4 seq` limits the recorded input history to four submissions
even after all four have been delivered. It bounds the history explored by
this model; a reusable queue with four slots would behave differently.

## What the checks establish

Read `results/verification_summary.md` for the commands actually executed and
their results. Three different kinds of evidence matter:

1. **Witnesses:** a `run` command finds an example in which an operation or
   scenario really occurs. This helps detect an inconsistent or overconstrained
   model that would otherwise make assertions pass vacuously. The receive,
   forwarding, and insertion witnesses start from an arbitrary valid state;
   they demonstrate satisfiable transitions, not reachability from initialisation.
   The transmission, repeated-value, and two-message delivery scenarios explicitly
   begin with `initial`.
2. **Safety checks:** a `check` command searches for a state or transition that
   violates a claimed invariant or abstraction property. No counterexample
   means none was found within that command's specified bounds.
3. **A negative demonstration:** an intentionally incorrect delivery rule can
   show why choosing the oldest pending message matters. Such a counterexample
   is evidence that the check can detect that fault, not a failure of the correct
   delivery operation.

The abstraction checks compare observable endpoints before and after a step.
Internal forwarding and insertion should leave both endpoints unchanged.
Transmission and successful reception should have their corresponding external
effects. This is bounded evidence for these properties; it is not an unbounded
refinement proof.

## Important modelling choices to disclose

The implementation distinguishes successful operations from optional polling
or stuttering operations. An external receive may leave the output unchanged.
A successful sectional receive requires a pending message in the last section.
Those are different enabledness conditions. Do not claim that success-only
operations prove every applicability obligation in the book. The comments in
the model identify its explicit completions and checks.

The printed `SReceive` describes successful delivery. Our `receivePoll` adds an
**unconditional stuttering alternative**, including when delivery is available.
This is an explicit optional completion compatible with abstract `Receive`,
rather than a literal translation of the printed `SReceive`. `daemonOrIdle`
similarly adds an idle alternative to successful forwarding. The abstract
operation predicates include their before/after external invariants, as Z
schemas do; the sectional transition predicates omit the post-state invariant
so its preservation can be checked.

The insertion formula on printed page 328 displays `rec i + 1`. It is interpreted
as `rec(i+1)`, the following section's arrival history: adding the integer 1 to a
message sequence would be ill typed. The prose on that page supports the
neighbour interpretation. A new empty section inherits the shared history at
the boundary where it is inserted; “empty” does not require its entire history
to be empty.

Eventual delivery is a separate question. Repeated waiting can preserve safety
forever without delivering a pending message. A progress argument would need
additional assumptions or constraints. The current package does not claim
fairness, deadlock freedom of a complete protocol, network fault recovery,
retransmission, timing guarantees, or conformance to the full SS7 standard.

## Running the project

Open PowerShell in this directory and run:

```powershell
python .\verify.py
```

Download Alloy Analyzer 6.2.0 from the [official release](https://github.com/AlloyTools/org.alloytools.alloy/releases/tag/v6.2.0)
and save its executable JAR as `tools/alloy-6.2.0.jar`; the JAR is not committed
to this repository. Java and Python 3.10 or later must be installed. The script writes
each run to a new results directory, saves the raw Analyzer receipt and witness
files, and refreshes the human-readable verification summary. Read the script
for the exact command and selected solver. PowerShell users may also run
`.\verify.ps1`. The default solver is `glucose`; use `python .\verify.py --solver sat4j`
for the pure Java solver.

To check the verification and XML-reporting utilities without rerunning Alloy:

```powershell
python -m unittest -v test_verification
```

The tests use a preserved historical run as their fixture. The current reviewed
model's evidence is linked from [the verification summary](results/verification_summary.md).
See [the results guide](results/README.md) before interpreting an individual receipt.

To explore the model visually:

```powershell
java -jar .\tools\alloy-6.2.0.jar gui .\telecommunications.als
```

If the command-line GUI launcher is unavailable in another Alloy distribution,
launch its desktop application and open `telecommunications.als` using File →
Open. Select a `run` command for a witness or a `check` command for a
counterexample search. The same source includes both.

Alloy downloads and distribution notes:
[official AlloyTools releases](https://github.com/AlloyTools/org.alloytools.alloy/releases/tag/v6.2.0).
The installed JAR's `help exec` output is the reference for its command-line
options. The source book remains copyright Woodcock and Davies; this package's
model and teaching notes are a new translation and explanation.
