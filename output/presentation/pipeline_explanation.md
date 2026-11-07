# Telecommunications protocol: the complete modelling and verification pipeline

This explanation follows the executable Alloy project in this workspace. The repository also contains a separate Bangla-English agent research PDF, but that document describes proposed research rather than the protocol pipeline explained here. The protocol project translates the telecommunications case study in Chapter 20 of Woodcock and Davies' *Using Z* into a bounded, executable model.

The central question is precise: **when a message travels through several internal queues, do the visible input and delivery histories still satisfy the promised ordering behaviour?** The project answers this with a mathematical state model, explicit transitions, bounded counterexample searches, positive examples, and saved evidence that ties each reported result to the source actually analysed.

## 1. The pipeline at a glance

The complete workflow has two connected parts.

1. **Protocol modelling:** understand the external service, choose an internal representation, define valid states, specify each operation, and connect the internal and external views through a retrieve relation.
2. **Verification and reporting:** declare checks and examples, freeze the model, run Alloy within explicit bounds, save raw evidence, validate that evidence, and generate readable results.

The protocol itself has a simpler operational path: submit a message at the first point, forward it through adjacent points, and deliver it from the final point. Insertion can add a new point between existing neighbours. These operations describe possible state changes. The verification workflow examines whether those changes respect the specification.

Source: [project overview](../../telecommunications_protocol/README.md), especially “What problem are we solving?” and “Implementation approach”.

## 2. The external specification

An external observer sees only two ordered histories:

- `input`: every submitted message occurrence.
- `output`: every delivered message occurrence.

Every sequence stores its **newest entry on the left**. If A arrives first and B arrives second, the input history is `[B,A]`. If only A has been delivered, the output history is `[A]`. The visible safety condition requires `output` to be a suffix of `input`.

For example, `[C,B,A]` with output `[B,A]` is valid. A and then B have been delivered, while C remains pending. Output `[C,A]` would violate the relationship because it skips B. An empty output is also a valid suffix: the safety property permits messages to remain pending.

`externalTransmit` prepends a message to the input and preserves output. `externalReceive` preserves input and allows either one additional delivered occurrence or no change. Both predicates require their before and after histories to satisfy the external invariant, matching the abstract schemas' contract.

Source: [external histories and operations, model lines 21–67](../../telecommunications_protocol/telecommunications.als).

## 3. The internal state representation

The implementation exposes the mechanism that the external observer cannot see. `Message` represents message values, while `SPC` represents signalling point codes. A `State` snapshot contains:

```text
route       an ordered sequence of active signalling points
rec[p]      the complete arrival history at point p
ins[p]      the messages still pending inside point p
sent[p]     the complete departure history from point p
```

The route is nonempty and contains no repeated point. Histories belong to the identity of a point, rather than its numeric position in the route. This matters during insertion: changing route positions does not change which existing point owns a history.

An operation relates explicit `pre` and `post` snapshots. These snapshots are Alloy atoms, not automatically consecutive moments on an implicit timeline. A scenario supplies the links between them. For example, the two-message demonstration names seven snapshots and specifies six operations connecting them.

A `Message` atom is a value, rather than a unique transmission identifier. Two occurrences can contain the same value. The sequence `[A,A]` has length two even though it uses only one distinct message atom. Sequence positions preserve repeated occurrences and their order.

Source: [signatures and state fields, model lines 9–25](../../telecommunications_protocol/telecommunications.als); [design decisions](../../telecommunications_protocol/design_notes.md).

## 4. The internal invariant

The state invariant has a structural part and an accounting part. `shape` requires properly formed sequences, a nonempty route without duplicate points, and no histories attached to inactive points.

The accounting relationship at every active point is:

```text
rec[p] = ins[p] concatenated with sent[p]
```

It says that a point's arrival history splits into its pending messages and its departed messages. This is equality of complete ordered sequences, so preserving only the number or set of messages would be insufficient.

Adjacent points must also agree about their shared boundary:

```text
sent[upstream] = rec[downstream]
```

Every departure recorded by the upstream point is the corresponding arrival recorded by the next point. Together these conditions make local queue operations compatible with the route's overall ordering.

The model deliberately does **not** impose `sectionInvariant` as a global fact. A preservation check assumes it for `pre`, applies an operation, and asks whether it holds for `post`. This lets Alloy examine an invalid post-state when an operation contains a mistake. Assuming the invariant for every state would remove those candidate counterexamples before the check could expose them.

The sectional predicates also omit a pre-state invariant. Their callers supply the valid-before-state contract. The provided checks use `sectionInvariant[pre]`, while initialized scenarios begin with `initial`. A bare operation predicate therefore does not constitute a complete valid-state demonstration.

Source: [shape and sectionInvariant, model lines 69–86](../../telecommunications_protocol/telecommunications.als); [preservation assertions, lines 207–229](../../telecommunications_protocol/telecommunications.als).

## 5. Initialisation and transmission

`initial` establishes a valid route shape and empty `rec`, `ins`, and `sent` relations. It does not require a particular number of route points beyond nonemptiness. `InitialIsValid` checks that this starting condition establishes the sectional invariant and empty external input and output.

`transmit[pre,post,m]` submits value `m` at the first point. It prepends `m` to that point's `rec` history and `ins` queue. It preserves the route, every other point's arrival history and queue, and all departure histories.

If the first queue is `[A]` and B arrives, it becomes `[B,A]`. The oldest pending occurrence remains A, at the right-hand end. The input history grows in the same way because input is the first point's arrival history.

These preserved-field requirements are frame conditions. They are essential because Alloy does not automatically preserve an unmentioned field. An operation must state both its intended changes and the surrounding state that remains equal.

Source: [initial and transmit, model lines 88–105](../../telecommunications_protocol/telecommunications.als).

## 6. Internal forwarding

`daemon` models one successful transfer from an active point to its immediate successor. It requires an upstream point that is not final and a nonempty upstream queue. Let `m` be the **last**, oldest element of that queue. The operation performs four coordinated updates:

1. Remove `m` from the upstream pending queue.
2. Prepend `m` to the upstream departure history.
3. Prepend `m` to the downstream pending queue.
4. Prepend `m` to the downstream arrival history.

It also preserves the route, upstream arrival history, downstream departure history, and all fields at other points. Updating just the two queues would leave the boundary and local accounting histories inconsistent.

For example, an upstream queue `[B,A]` and empty downstream queue become `[B]` and `[A]`. The transfer moves A first because A entered earlier. This step changes the internal placement of pending messages while preserving the two external histories.

`daemonOrIdle` permits either one such transfer or an unchanged snapshot. This idle choice is an explicit modelling completion separate from the successful forwarding operation.

Source: [daemon and idle wrapper, model lines 123–162](../../telecommunications_protocol/telecommunications.als).

## 7. Successful delivery and polling

`receive` acts only at the last route point and requires a nonempty pending queue. It removes the queue's rightmost, oldest occurrence and prepends it to the final departure history. It preserves all arrival histories, the route, and other points' pending and departure sequences.

If the final queue is `[B,A]` and output is empty, successful delivery produces queue `[B]` and output `[A]`. A subsequent delivery produces queue `[]` and output `[B,A]`. Chronologically, A arrived before B, even though the displayed final history lists B on the left.

The model separates successful delivery from `receivePoll`, which allows either `receive` or an unconditional `stutter`. Stuttering copies every state field unchanged. The polling wrapper may stutter even when delivery is available. It is compatible with the abstract receive's optional no-change behaviour, but it extends the printed successful sectional receive schema.

This distinction explains why safety alone cannot guarantee delivery. A pending message can remain pending across a poll that does no work. The provided stuttering witness demonstrates that possibility explicitly.

Source: [receive, stutter, and receivePoll, model lines 107–158](../../telecommunications_protocol/telecommunications.als); [pending-poll witness, lines 325–331](../../telecommunications_protocol/telecommunications.als).

## 8. Inserting a new route point

`insertSection` inserts a fresh point strictly between two existing neighbours. Suppose the route changes from `[P0,P1]` to `[P0,X,P1]`. X starts with an empty pending queue, while its received and sent histories equal the history that has already crossed the old P0/P1 boundary.

Under the before-state invariant, `sent[P0]` already equals `rec[P1]`. Giving both histories of X that same value preserves the accounting equation because an empty sequence concatenated with that history equals the history itself. It also preserves agreement on both new boundaries.

For a worked illustration, if `[A]` has already crossed the boundary, X receives `rec[X]=[A]`, `ins[X]=[]`, and `sent[X]=[A]`. “Empty section” describes its current pending queue, not an absence of historical traffic. Existing points keep all their sequences.

Insertion requires an unused point and enough room under the finite route sequence bound. The checks examine both invariant preservation and external invisibility. The supplied insertion witness also requires pending traffic and a nonempty inherited boundary history, so it exercises the important historical case.

Source: [insertSection, model lines 164–183](../../telecommunications_protocol/telecommunications.als); [insertion witness, lines 300–305](../../telecommunications_protocol/telecommunications.als).

## 9. The retrieve relation and abstraction checks

The retrieve relation selects externally visible histories from a concrete snapshot:

```text
input[s]  = rec[firstPoint[s]]
output[s] = sent[lastPoint[s]]
```

`inFlight[s]` concatenates all pending queues in route order, with index offsets placing their elements in one sequence. `RetrieveIsValid` checks a stronger accounting relationship:

```text
input = inFlight concatenated with output
```

Consequently, output is a suffix of input. The concrete model accounts for every submitted occurrence as either pending or already delivered, while preserving its ordered position.

The abstraction assertions compare observable effects. `TransmitRefinesExternal` checks that a concrete transmission has the abstract transmission effect. `ReceiveRefinesExternal` checks the polling wrapper against abstract receive. `DaemonIsInvisible` and `InsertionIsInvisible` require unchanged input, output, and total in-flight sequence.

These are finite checks of operation effects and the retrieve equation. The project does not claim a complete, unbounded data refinement proof or every applicability obligation of the original mathematical development.

Source: [inFlight and retrieve assertion, model lines 185–205](../../telecommunications_protocol/telecommunications.als); [abstraction assertions, lines 231–255](../../telecommunications_protocol/telecommunications.als).

## 10. A complete saved two-message execution

The following table comes from the saved Alloy witness, rather than a hypothetical animation. Its actual route uses two points. A and B are readable aliases for the witness's two distinct message values. All lists are newest first.

| Step | Action | First pending queue | Last pending queue | Input | Output |
|---|---|---|---|---|---|
| 0 | Initialise | `[]` | `[]` | `[]` | `[]` |
| 1 | Transmit A | `[A]` | `[]` | `[A]` | `[]` |
| 2 | Transmit B | `[B,A]` | `[]` | `[B,A]` | `[]` |
| 3 | Forward A | `[B]` | `[A]` | `[B,A]` | `[]` |
| 4 | Forward B | `[]` | `[B,A]` | `[B,A]` | `[]` |
| 5 | Receive A | `[]` | `[B]` | `[B,A]` | `[A]` |
| 6 | Receive B | `[]` | `[]` | `[B,A]` | `[B,A]` |

The forwarding rows leave the visible histories unchanged. The receive rows deliver A before B. At the end, no message remains in flight and output equals input. The scenario explicitly links all seven snapshots from initialization, so it demonstrates one initialized path. Other standalone transition witnesses begin from arbitrary valid states and make a narrower claim of satisfiability.

Source: [decoded saved examples, lines 5–21](../../telecommunications_protocol/results/example_instances.md); [scenario predicate, model lines 313–323](../../telecommunications_protocol/telecommunications.als).

## 11. Checks, witnesses, and the intentional bug

An Alloy `run` searches for a satisfying example. A SAT result demonstrates that the requested scenario is possible within its scope. A `check` searches for a counterexample to an assertion. For an intended safety property, UNSAT means no counterexample exists within the command's finite search bounds.

Positive witnesses matter because an implication can pass vacuously when its operation is impossible. The project therefore runs examples of successful operations, insertion, repeated message values, a complete initialized delivery path, and polling stutter.

The isolated `receiveNewestFirst_BUG` deliberately removes the first, newest queue entry instead of the last, oldest entry. Its preservation check expects SAT, meaning a counterexample should exist. A simple teaching example is `rec=[B,A]`, `ins=[B,A]`, `sent=[]`. Delivering B first gives `ins=[A]` and `sent=[B]`, whose concatenation `[A,B]` differs from `rec`.

That simple example explains the fault. The actual saved counterexample contains repeated values and is printed in the example report. Its before-state satisfies local accounting and its after-state violates it. No correct operation or delivery scenario invokes the buggy predicate.

Source: [intentional bug, model lines 257–280](../../telecommunications_protocol/telecommunications.als); [actual counterexample, example report lines 23–36](../../telecommunications_protocol/results/example_instances.md).

## 12. Recorded verification results and bounds

The selected completed execution is `run-20261103-215246-91a68f`, using Alloy 6.2.0 and the `glucose` solver. It completed on 3 November 2026 with process exit code zero. The report was regenerated and the evidence revalidated on 4 November 2026. The record reports **18 matching expected outcomes**:

- Ten correct assertions returned UNSAT, finding no counterexample within scope.
- Seven example runs returned SAT and saved witnesses.
- The intentional bug check returned SAT and saved its expected counterexample.

Correctness checks use at most four message values and four point codes, maximum sequence length four, one or two snapshots, and signed five-bit integers. The delivery witness instead requests exactly seven snapshots, two message values, and two points. Each command records its own bounds.

`4 seq` bounds recorded lifetime history as well as pending queue length. Delivering a message does not remove it from the first received history, so delivery does not create capacity for a fifth recorded submission. Capacity guards and length equations stop bounded sequence helpers from silently truncating data. Overflow prevention is also confirmed in the saved execution evidence.

Source: [verification summary, lines 3–57](../../telecommunications_protocol/results/verification_summary.md); [sequence guards, model lines 27–38](../../telecommunications_protocol/telecommunications.als).

## 13. Reproducible execution and evidence validation

The Python runner first creates a unique results directory, copies the live model into it, and calculates that frozen copy's SHA-256 hash. It executes the saved copy, preventing later workspace edits from being associated with an earlier analysis. Metadata records the command, solver, source hash, JAR hash, tool versions, timestamps, execution status, and exit code.

During execution it streams Analyzer output into `analyzer.log`. Alloy writes its receipt and SAT XML instances under the run's `alloy` directory. Interruption and startup failure receive explicit statuses. Pending reports replace earlier results before a new execution begins, reducing the risk that a stale PASS appears to describe an incomplete run.

The `summarize` stage validates the source hash and successful completion. It compares command identities, order, types, expected outcomes, and scopes across the saved source, log, and receipt. It verifies solver agreement and overflow settings, and requires XML evidence for every SAT result.

Only after validation does `export_instances.py` decode demonstrations. It rejects missing fields and malformed sequence indices rather than quietly turning a damaged relation into a plausible list. It checks the delivery example's route and local accounting, confirms its A-before-B output, and verifies that the bug example actually demonstrates the stated accounting failure. Failed validation replaces example claims with an explicit unavailable message.

The reviewed model hash is `47d76e1f6c80954afd8b2ea0607486f4a410a80298a5d7bfd98573c4ade47621`. The workspace model matches that saved source. This hash identifies the model associated with the evidence, rather than proving the model's correctness.

Source: [runner and source freezing, verify.py lines 217–280](../../telecommunications_protocol/verify.py); [evidence validation, lines 81–207](../../telecommunications_protocol/verify.py); [XML decoder and example checks, export_instances.py lines 7–121](../../telecommunications_protocol/export_instances.py).

## 14. Reproduction and the limits of the conclusion

From the protocol directory, the supporting commands are:

```powershell
python -m unittest -v test_verification
python .\verify.py
python .\verify.py --solver sat4j
java -jar .\tools\alloy-6.2.0.jar gui .\telecommunications.als
```

The first command tests verification/reporting utilities against preserved evidence without rerunning Alloy. The next two are alternative analysis invocations, using the default solver or the pure Java `sat4j` solver. Java, Python 3.10 or later, and the Alloy 6.2.0 JAR at the documented location are prerequisites. The GUI command opens the model for inspecting examples and counterexamples.

An existing execution can be revalidated without launching a new analysis:

```powershell
python .\verify.py --summarize .\results\run-20261103-215246-91a68f
```

This command refreshes the summary and examples for that selected run. The audit records 14 passing regression tests for the reporting utilities, covering altered source, missing or duplicate outcomes, mismatched scopes, missing witnesses, malformed sequences, failure, and interruption. Those utility tests support trustworthy reporting, while the Alloy checks examine the protocol model.

The justified conclusion is that the selected finite model has satisfiable demonstrations and that its ten intended safety and abstraction checks found no counterexample within their recorded bounds. A witness establishes possibility, not inevitability. In particular, optional stuttering permits waiting without delivery. The package therefore makes no claim of fairness, eventual delivery, complete protocol deadlock freedom, timing guarantees, fault recovery, retransmission, full SS7 conformance, or universal correctness for every route and history size.

Source: [setup and running instructions](../../telecommunications_protocol/README.md); [runner options, verify.py lines 217–227](../../telecommunications_protocol/verify.py); [completed review and validation](../../telecommunications_protocol/audit_report.md); [design limitations](../../telecommunications_protocol/design_notes.md).

## 15. Larger-network extension, 8 November 2026

The four-point results described above remain the original recorded baseline.
A later extension separates network size from message-history length and adds
three representations: an active subset of an ordered point pool, a version
with explicit Before/After history fields, and a specialization for a fixed
full route. The last version excludes insertion. The Before/After encoding
supports state and individual-transition checks rather than the seven-snapshot
delivery demonstration.

The extension completed all ten property checks at ten active-route points with
two-entry histories, and found the expected intentional-bug counterexample and
exact-size operation witnesses. It also completed all ten checks at eight points
with four-entry histories. Read the [current scaling results](../../telecommunications_protocol/results/scaling_summary.md)
for additional successful scopes and the full record of unsuccessful attempts.

The fixed-route model additionally produced validated traffic and transmission
witnesses with exactly 1,000 active points and completed its initialisation
check using one message value and a one-entry history. Its full-route forwarding
witness timed out after 120 seconds. These results are narrower evidence than completing
all properties with multiple pending occurrences. General 1,000-point attempts
with longer histories hit translation or time limits. UNKNOWN results remain
explicitly labelled and are never counted as successful checks.

The `scale_verify.py` workflow freezes each experiment, applies a deadline to
each Java process, and validates logs, receipts and SAT XML evidence. It also
checks actual active-route sizes in the named full-route witnesses. Bounded
correspondence harnesses compare the new encodings with the reference model
without assuming post-state validity. Their successful results support the
representation changes at the checked small scopes, while the mathematical
explanation describes why the accounting identities telescope along a route.

The ordered pool fixes the positions available for insertion, so a particular
fresh point must fit the selected gap. This enabledness qualification, the
snapshot limits, and the distinction between a witness and a property check
remain part of the conclusion. None of these extensions establishes fairness,
eventual delivery or a machine-checked theorem for arbitrary network size.

Sources: [scaling design](../../telecommunications_protocol/scaling_design.md),
[validated coverage and raw evidence](../../telecommunications_protocol/results/scaling_summary.md),
[benchmark runner](../../telecommunications_protocol/scale_verify.py), and
[correspondence runner](../../telecommunications_protocol/check_correspondence.py).
