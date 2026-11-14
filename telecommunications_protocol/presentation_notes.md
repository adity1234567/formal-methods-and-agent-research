# Telecommunications Protocol in Alloy: presentation notes

Use this as a 10–12 minute presentation outline. Add your group name and members on Slide 1. These notes describe the supplied project package; they do not claim that your group completed work before this package was created. Use the recorded results in [verification_summary.md](results/verification_summary.md) when reporting completed checks.

## Slide 1 — Project and question

**On the slide**

- Telecommunications Protocol — *Using Z*, Chapter 20
- Group: **[group name and members]**
- Main question: does a design with intermediate message queues preserve the promised delivery behaviour?
- Deliverables: Alloy model, bounded analysis, and a demonstration trace.

**Speaker notes**

“We take a mathematical specification and make it executable in the Alloy Analyzer. We explain the visible service, model the internal state changes, and ask Alloy to find examples or counterexamples. Our implementation is a formal model, rather than a deployed telephone network.”

## Slide 2 — The assigned case study

**On the slide**

- The chapter studies an abstraction of SS7 signalling between telephone exchanges.
- The external view records incoming and delivered message histories.
- The sectional view explains forwarding along a route.
- The project concerns abstraction and refinement, with deliberately limited protocol detail.

**Speaker notes**

“We follow the particular case study assigned in the book. The route and its queues give us enough detail to investigate ordering. We do not need to reproduce every feature of the SS7 standard to study this question.”

Source: Woodcock and Davies, [*Using Z*, Chapter 20, pp. 321–329](https://dsc.ufcg.edu.br/~dalton/bib/woodcock96.pdf#page=335).

## Slide 3 — Read the histories correctly

**On the slide**

```text
Newest entries are on the LEFT.

incoming  = [B, A]      chronological input: A, then B
delivered = [A]         A has arrived; B is still travelling

incoming = pending ++ delivered
```

- The delivered history is a suffix of the incoming history.
- Empty output is compatible with safety: eventual delivery is a separate question.

**Speaker notes**

“This direction is easy to misread. We prepend each newly submitted message. To deliver the oldest pending entry we remove the rightmost entry from its queue. The equation compares complete sequences, so it retains both ordering and repeated occurrences.”

## Slide 4 — Internal state that the model tracks

**On the slide**

```text
route:   P0  →  P1  →  P2

at each route point p:
  rec[p]  : history received
  ins[p]  : queue currently inside
  sent[p] : history forwarded or delivered

rec[p] = ins[p] ++ sent[p]
sent[P0] = rec[P1]; sent[P1] = rec[P2]
```

- Route points do not repeat.
- Histories and queues are indexed sequences, rather than unordered sets.

**Speaker notes**

“For the implementation, each snapshot contains the route and the three message sequences at its active points. The first equation accounts for a point’s received messages. The second joins neighbouring points: whatever one has forwarded must be what the next has received.”

## Slide 5 — State changes in the implementation

**On the slide**

| Action | Main update | External effect |
|---|---|---|
| Transmit | Prepend a message to the first point’s received history and queue | Incoming history grows |
| Forward / daemon | Move the oldest queued message to the next point; update the boundary histories | None |
| Receive | Move the final point’s oldest queued message to its sent history | Delivered history grows |
| Stutter | Keep the snapshot unchanged | None |

**Speaker notes**

“Every sectional action includes frame conditions: all fields not involved in the action retain their values. Forwarding requires a nonempty source queue and a following point. Successful receipt requires a nonempty final queue. Our `receivePoll` wrapper also permits an unconditional no-change step. That optional completion agrees with the abstract receive; it is additional to the printed successful `SReceive` schema.”

## Slide 6 — How Z becomes Alloy

**On the slide**

| Specification concept | Alloy implementation choice |
|---|---|
| Given sets for messages and point codes | `Message` and `SPC` signatures |
| Sequence | Relation from sequence index to element |
| State schema | `State` and `sectionInvariant` |
| Before/after state | Two explicit snapshot parameters |
| Operation schema | Predicate relating the snapshots |
| Retrieve relation | `input` and `output` functions |
| Correctness obligation | `assert` with a bounded `check` |
| Example behaviour | Predicate with a `run` command |

**Speaker notes**

“Explicit snapshots make this model readable without temporal syntax. Each action uses `pre` and `post` snapshot parameters. Alloy searches for finite relational structures satisfying the predicates. Sequence indices start at zero in this implementation; that differs from the book’s sequence indexing without changing the queue behaviour.”

The sectional operation predicates assume their caller supplies a valid
before-state. The supplied `Show*` scenarios and checks provide that context;
running a bare operation does not enforce the state invariant automatically.

## Slide 7 — Demonstrate two messages across three points

**On the slide**

Route: `P0 → P1 → P2`. All lists below show newest first.

| Step | Action | `ins[P0]` | `ins[P1]` | `ins[P2]` | Incoming | Delivered |
|---|---|---|---|---|---|---|
| 0 | Initialise | `[]` | `[]` | `[]` | `[]` | `[]` |
| 1 | Transmit A | `[A]` | `[]` | `[]` | `[A]` | `[]` |
| 2 | Transmit B | `[B,A]` | `[]` | `[]` | `[B,A]` | `[]` |
| 3 | Forward A from P0 | `[B]` | `[A]` | `[]` | `[B,A]` | `[]` |
| 4 | Forward A from P1 | `[B]` | `[]` | `[A]` | `[B,A]` | `[]` |
| 5 | Forward B from P0 | `[]` | `[B]` | `[A]` | `[B,A]` | `[]` |
| 6 | Receive A | `[]` | `[B]` | `[]` | `[B,A]` | `[A]` |
| 7 | Forward B from P1 | `[]` | `[]` | `[B]` | `[B,A]` | `[A]` |
| 8 | Receive B | `[]` | `[]` | `[]` | `[B,A]` | `[B,A]` |

**Speaker notes**

“At step 2, A is on the right, so A moves first. Step 5 demonstrates two messages in different queues. The external observer cannot see the forwarding steps. At the end the displayed history is B,A, but the actual delivery order was A, then B. The table is a worked explanation; use the saved Alloy instance for the executable demonstration.”

For a table decoded from the actual two-point Alloy witness, open [example_instances.md](results/example_instances.md). It also shows the intentional bug counterexample.

## Slide 8 — What the checks need to establish

**On the slide**

```text
external incoming  = received history at the FIRST route point
external delivered = sent history at the LAST route point

valid before-state + operation  ⇒  valid after-state
```

- Initialisation establishes the invariants.
- Each correct sectional action is checked for preservation of the invariant.
- Transmit and successful receive have their specified external effects.
- Forwarding changes neither external history.

**Speaker notes**

“We check preservation without assuming the sectional invariant for the after-state inside the sectional operation. Otherwise a faulty action could be excluded by assumption and the check could pass for the wrong reason. The abstract operation predicates do include their external before/after invariants, following the Z schemas. We also run positive examples so that an impossible operation is less likely to hide behind an implication with a false premise.”

## Slide 9 — Route insertion

**On the slide**

```text
Before: P0 → P1
After:  P0 → X → P1

X has an empty queue.
X's received and sent histories match the existing boundary history.
```

- Insert a fresh point between existing neighbours.
- Preserve the old points’ queues and histories.
- Check that insertion leaves the external histories unchanged.

**Speaker notes**

“Insertion implements the enrichment in Section 20.4. Giving the new point an empty queue does not mean its entire history is empty: messages may already have crossed this boundary before insertion. The model initialises those historical fields consistently. The recorded run found an insertion example, and its invariant-preservation and invisibility checks found no counterexample within their bounds.”

## Slide 10 — Live demonstration

**On the slide**

1. Open [telecommunications.als](telecommunications.als) in Alloy Analyzer.
2. Run `ShowTransmit`, `ShowDaemon`, and `ShowReceive`.
3. Inspect queue order and the first/last histories in the instance.
4. Run the invariant and external-effect assertions.
5. Run `ShowTwoMessageDelivery`, `ShowRepeatedMessageValue`, and `ShowInsertionWithTraffic`.
6. Check `BrokenReceiveWouldPreserveInvariant`: its expected counterexample demonstrates the deliberately incorrect newest-first delivery rule.

**Speaker notes**

“A `run` searches for an instance. A `check` searches for a counterexample. Report the scope and sequence bounds shown in the command, along with the result. For example, `DaemonIsInvisible` checks that forwarding preserves the external histories, and `ReceivePreservesInvariant` checks the internal accounting. The recorded CLI output makes the demonstration reproducible.”

Reference for Alloy usage and language: [official Alloy documentation](https://alloytools.org/documentation.html).

## Slide 11 — Implementation progress, supported by evidence

**On the slide**

| Work item | Evidence to show |
|---|---|
| Source understood | External/internal state explanation and the sequence convention |
| Model implemented | Signatures, invariant predicates, and operation predicates in the `.als` file |
| Successful transitions satisfiable | Seven example runs produced satisfying instances; some begin with arbitrary valid states |
| Initialised scenarios demonstrated | Transmission, repeated-value submission, and two-message delivery explicitly start from `initial` |
| Safety/abstraction checked | Ten checks found no counterexample within their stated bounds |
| Fault detection demonstrated | The intentional newest-first bug produced the expected counterexample |
| Route insertion checked | Insertion witness found; preservation and invisibility checks found no counterexample |

**Speaker notes**

“All 18 commands matched their expectations in the recorded analysis. A valid before/after pair demonstrates that a transition is satisfiable; it does not by itself establish a path to that state from initialisation. The explicitly initialised scenarios provide that additional evidence for their particular paths. Our group’s own reading, contribution allocation, and rehearsal progress should be added separately. The verification summary records the exact scopes and results.”

## Slide 12 — Limits and next work

**On the slide**

- A passing bounded check covers the stated finite scope.
- Safety beyond the bounds rests on a separate argument: a locality lemma plus Z3 proofs (`results/unbounded_summary.md`).
- Successful example traces demonstrate possibility, not inevitable progress.
- `4 seq` limits the recorded submission history to four entries, including entries already delivered.
- Future extension: temporal behaviour and delivery under explicit progress assumptions.
- Additional SS7 features require additional requirements and modelling.

**Speaker notes**

“Our result is an executable, analysable account of this abstraction. We can show the internal steps and check their relationship to the visible histories. We should not claim universal correctness, guaranteed eventual delivery, or full SS7 compliance from this model.”

“The sequence bound limits how much lifetime history we analyse. Delivering a
message does not remove it from the input history, so it does not free space
for a fifth submission in a `4 seq` analysis.”

## Viva preparation

**Why use sequences instead of sets?** A set loses position and repeated occurrences. An indexed sequence can distinguish `[A,B]`, `[B,A]`, and `[A,A]`.

**Why is the output a suffix rather than a prefix?** New entries are stored on the left. Earlier delivered entries therefore occupy the right-hand part of the input history.

**Does an empty delivered history violate safety?** No. It satisfies the history relationship, even if pending messages wait indefinitely. Progress needs a separate requirement.

**What is refinement here?** Selecting the two external histories from each concrete snapshot lets us compare the concrete actions with the abstract behaviour. Forwarding and insertion should be invisible under this selection.

**Why update `rec` and `sent` during forwarding?** They record the crossing of a boundary. Updating only the two queues would leave the accounting histories inconsistent.

**Why allow a stuttering receive?** An external observation may find that no delivery happened. In the implementation, `receive` is the successful delivery action with a queue-availability condition; `receivePoll` explicitly supplies the optional stuttering observation.

**Why are positive runs necessary?** A preservation implication can hold vacuously if the operation has no satisfying before/after pair. A witness demonstrates satisfiability within the chosen scope. Reachability from initialisation additionally requires an explicitly initialised path, which only some supplied scenarios include.

**Can two messages have identical content?** Repeating the same message atom in different sequence positions models repeated values. Avoid claiming that a set of message atoms alone counts transmission occurrences.

**Does “no counterexample” mean proved correct?** In Alloy it means none was found in the stated bounds. For the safety properties we add an unbounded argument: every operation changes at most two adjacent sections, so a counterexample on any route shrinks to one on a window of at most four sections, and Z3 proves each window obligation for histories of any length. The lemma is a paper argument and the Z3 encoding is a hand translation, so we call this strong supporting evidence, not a mechanised refinement proof.

**How did you push Alloy to larger networks?** Three changes. First, every history position became its own arity-2 field, because Kodkod cannot index relations whose universe-to-the-arity exceeds about 2.1 billion tuples. Second, lengths, prepending and offsets became constant slot shifts, so the SAT problem has no integer adder circuits. Third, first/last/next active point are computed by a linear recursion along the pool order instead of closure-based minimums, which grew roughly with N cubed. The report records which sizes then completed.

**Why trust an UNSAT answer from Kissat?** With `--proof`, Kissat writes a DRAT proof and the independent checker drat-trim verifies it against the same CNF. An empty CNF from Alloy is never interpreted, because Alloy writes one when it has already decided the formula, and an empty CNF is satisfiable. Witnesses still use Alloy's own solver so their instances can be inspected.

**What did your group contribute?** Describe the work you actually performed: interpreting the requirements, reviewing the model, explaining operations, running checks, investigating any counterexample, and preparing the demonstration. Do not present generated package contents as a history of work you did not do.

## References

1. Jim Woodcock and Jim Davies. *Using Z: Specification, Refinement, and Proof*. Prentice Hall International, 1996. Chapter 20, printed pp. 321–329; [public PDF](https://dsc.ufcg.edu.br/~dalton/bib/woodcock96.pdf#page=335).
2. AlloyTools. [Alloy documentation](https://alloytools.org/documentation.html).
3. Supplied project model: [telecommunications.als](telecommunications.als). Actual verification record: [results/verification_summary.md](results/verification_summary.md).

In the linked source PDF, Chapter 20 starts at PDF page 335, printed page 321.
The local raw text extraction is a reading aid; use the PDF to resolve mathematical
symbols and grouping. See [extraction notes](references/extraction_notes.md).
