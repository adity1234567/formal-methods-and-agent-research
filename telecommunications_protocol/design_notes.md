# Modeling decisions

This file describes the implementation in `telecommunications.als`; verification results belong in the generated results report.

- `State` is an explicit snapshot. A transition takes `pre` and `post` snapshots. The model does not rely on Alloy 6 temporal syntax, and the delivery demonstration names its seven snapshots explicitly.
- `route` is a sequence of distinct `SPC` atoms. Histories are indexed by their point identity rather than by their route position. Consequently, inserting a point preserves the histories associated with every existing point.
- Every message history has newest values at index zero. Sending the oldest buffered value therefore uses `seq/last` and `seq/butlast`, rather than `seq/first` and `seq/rest`.
- A `Message` atom is a value, not a unique transmission identifier. Two sequence indices may contain the same value. The repeated-value witness checks this explicitly.
- Sequence indices start at zero in Alloy; the chapter uses positions starting at one. There is no behavioral change.
- History fields use `seq/Int` as their index type, restricting the search to the command's finite sequence range. Contiguity and the accounting relationships still require the explicit invariant.
- `shape` states sequence typing, route injectivity, nonemptiness, and absence of histories on inactive points. `sectionInvariant` additionally states local conservation and agreement between adjacent boundaries.
- No global fact assumes `sectionInvariant`. The sectional operation predicates specify their field updates without assuming the post-state sectional invariant. Thus a preservation check can find an invalid post-state. The abstract `externalTransmit` and `externalReceive` predicates include their external before/after invariants, matching the Z schemas.
- Sectional operations also omit the pre-state invariant: their caller must supply `sectionInvariant[pre]` or a path established from `initial`. Use the supplied `Show*` scenarios for demonstrations; a bare operation predicate is not a complete valid-state scenario.
- Library sequence insertion and concatenation can truncate at the bounded sequence length. Length equations and capacity guards prevent such truncation from becoming an allowed message-loss behavior.
- The sequence bound limits lifetime recorded history as well as queue lengths. With `4 seq`, at most four submissions are represented in the first received history, even after delivery. This is a finite history bound, not the capacity of a reusable four-slot queue.
- `receive` implements the successful, partial sectional receive. `daemon` implements a successful internal transfer and explicitly updates upstream `sent` and downstream `rec`, including all unchanged fields.
- `receivePoll` and `daemonOrIdle` add an unconditional stuttering choice, including when a successful step is available. These wrappers are explicit optional modelling completions, kept separate from the chapter's successful schemas. In particular, `receivePoll` is not a literal translation of printed `SReceive`; its additional stutter is compatible with abstract `Receive`.
- `insertSection` inserts strictly between existing neighbors. Its new buffer is empty; the new point's received and sent histories both equal the existing boundary history.
- `inFlight` concatenates buffers in route order using offsets. The retrieve assertion checks both the external suffix property and the stronger equation `input = inFlight ++ output`, where `++` here denotes sequence concatenation in explanatory prose.
- Refinement assertions check operation effects and the retrieve equation within finite bounds. The project does not claim a mechanized unbounded data-refinement proof, full enabledness proof, or eventual delivery.
- The isolated `receiveNewestFirst_BUG` predicate is intentionally wrong and appears only in the expected counterexample check. It is an educational mutation to demonstrate that the invariant can reject an incorrect implementation.
- Receive, daemon, and insertion witnesses demonstrate satisfiable transitions from arbitrary valid states. They do not establish reachability from initialisation. The transmission, repeated-value, and two-message delivery scenarios explicitly begin with `initial` and demonstrate particular initialised paths.

For correct checks, the scope is at most four message values and four signalling points, with sequence length at most four, one or two snapshots, and signed five-bit integers. Five-bit arithmetic is sufficient on valid states because the retrieve conservation law limits total in-flight length to the first received history's length. The recorded results refer to these bounds; reassess integer width and rerun analysis when increasing them.

Source: Jim Woodcock and Jim Davies, *Using Z: Specification, Refinement, and Proof*, Chapter 20 (1996), printed pages 321–329 in the downloaded PDF. This implementation is an original Alloy translation of the chapter's abstract protocol model, not a full implementation of SS7.

The chapter starts on PDF page 335, printed page 321. The local raw extraction does
not preserve every mathematical symbol or grouping; consult the PDF and
[extraction notes](references/extraction_notes.md) for source interpretation.
