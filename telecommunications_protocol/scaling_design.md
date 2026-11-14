# Scaling the telecommunications model

`telecommunications_scalable.als` supplies a separate representation for larger
networks. It keeps the protocol's message histories and operations while making
the point-pool bound independent of the message-history bound. The original
`telecommunications.als` remains the reference representation. Command
declarations request analysis; completed results belong in the scaling report
and its saved execution evidence.

## Representation

The reference model stores `route` as a sequence of point identities. Alloy's
single `seq` bound consequently limits both route length and all message
histories. Increasing that bound enlarges every history's index domain, even
when the purpose is only to explore a longer route.

The scalable representation opens `util/ordering[SPC]` and stores `State.route`
as a set of active points. The total order of the point pool determines the
order of every active route. `firstPoint` selects its minimum, `lastPoint` its
maximum, and `nextPoint` selects the least active point later in the pool order.
All histories retain their original fields, newest-first convention and point
ownership. The sequence bound now applies only to message histories.

This changes the meaning of an `SPC` scope: `util/ordering` makes the **available
pool** exact. A pool of N points still admits valid active routes with any size
from 1 through N. The full-route witnesses require `active[s] = SPC` to show that
the requested boundary size is satisfiable. They do not infer it merely from an
upper bound on the command.

The order library supplies a global fact about the pool's order. It does **not**
assert `sectionInvariant` for all states. As in the reference model, preservation
checks assume a valid pre-state and examine the result of an operation without
assuming that the post-state is valid.

## Correspondence and its limits

For a scalable state, list its active points in increasing pool order. That
sequence is its reference-model route. Copy `rec`, `ins` and `sent` unchanged
after consistently renaming point and message atoms. Conversely, a reference
route can be embedded in a total order with the same active-point sequence.
Inactive points can fill unused positions in that order.

Transmission, reception, forwarding and stuttering preserve existing point
order. Insertion adds one point between existing neighbours and never reverses
their order. Therefore any finite reference behaviour containing only those
operations can be embedded into a pool order compatible with its final route,
provided the pool contains enough points. This explains why the new
representation can express longer versions of the same message-flow behaviour.

There is an enabledness qualification. In the scalable model, a particular
inactive point can be inserted into a particular gap only if its fixed pool
position lies inside that gap. A given assignment of inactive positions may
leave a gap unavailable even when another inactive point exists elsewhere.
The correspondence argument permits choosing a compatible pool order or
renaming the inactive points. It does not prove that every insertion is enabled
from every representation of a reference state. Claims of unrestricted
enabledness or a full unbounded refinement theorem would require further proof.

The companion `scaling_correspondence.als` checks a bounded relationship between
the reference and scalable representations. Its successful checks, if recorded,
remain bounded evidence. They complement the explanation here rather than
turning it into a mechanized theorem for arbitrary network sizes.

## Pending messages without a sum over the network

The reference `inFlight` function concatenates pending queues in route order by
summing the lengths of all queues before each point. The scalable function uses
an equivalent offset on states satisfying `sectionInvariant`:

```text
offset(p) = length(input) - length(rec[p])
```

It places each actual pending occurrence from `ins[p]` at that offset plus its
local queue index. It still reads message values from the pending queues. It
does not obtain them from the desired input/output equation.

To see why the offset works, write the active route as points 1 through n, with
arrival histories R, pending queues Q and departure histories S. The invariant
states:

```text
R_i = Q_i concatenated with S_i
S_i = R_(i+1) for adjacent points
```

For a single point, `R_1 = Q_1 ++ S_1` is exactly local conservation. Here `++`
denotes ordered sequence concatenation in mathematical prose, not Alloy's
relational override operator. For n points, substitute
`R_2 = Q_2 ++ ... ++ Q_n ++ S_n` into
`R_1 = Q_1 ++ R_2`. By associativity this gives:

```text
R_1 = Q_1 ++ Q_2 ++ ... ++ Q_n ++ S_n
```

The same substitution up to point p gives:

```text
length(R_1) - length(R_p)
    = length(Q_1) + ... + length(Q_(p-1))
```

Thus the direct offset equals the reference offset on every valid finite route.
Outside valid states, the scalable `inFlight` function need not represent
route-order concatenation. Its use as that abstraction has an explicit validity
contract. The operations and assertions preserve that contract in the same way
as the reference checks: they establish validity from a valid pre-state rather
than impose validity globally.

This is a mathematical induction argument. The project does not present it as
an independently machine-checked unbounded proof.

## Why the operations preserve accounting

- **Transmission:** prepend the same value to the first point's R and Q. Its S
  remains fixed, so the local concatenation equation continues to hold.
- **Reception:** write the last pending queue as `Q' ++ [m]`, where m is oldest.
  The step replaces Q with Q' and S with `[m] ++ S`, preserving their
  concatenation and delivering the oldest pending occurrence.
- **Forwarding:** move the oldest value m from the upstream Q into upstream S,
  and prepend m to downstream R and Q. Both sides of the shared boundary gain
  the same occurrence. Other boundary histories remain unchanged.
- **Insertion:** the new point has `Q = []` and `R = S = H`, where H is the
  existing shared boundary history. Both new boundaries agree, and the inserted
  empty queue contributes nothing to the pending concatenation.
- **Stuttering:** every field retains its value.

These algebraic cases explain the assertions' intent. Actual Analyzer outcomes
are recorded separately, including the intentional newest-first receive fault
that should still produce a counterexample.

## Integer bounds

Let H be the maximum history length. Each `rec[p]`, `ins[p]` and `sent[p]` has at
most H entries because its index domain is `seq/Int` and each index maps to at
most one message. On valid states, local conservation and boundary agreement
imply that the total pending history also has at most H entries.

The direct offset lies between `-H` and `H` even before relying on conservation.
Adding a local sequence index reaches at most `2H - 1`. Local concatenation and
length comparisons need values up to `2H`. On valid states, the offset and total
pending length are actually between 0 and H. A signed bit width whose positive
range includes `2H` provides room for these history operations. The supplied
commands retain five-bit integers for H=4.

No arithmetic expression counts the large active route. Full-route witnesses
use set equality with the pool. The two-point delivery example uses equality
with a set containing two distinct named points instead of comparing a large
route cardinality. Consequently increasing N does not itself require increasing
the integer bit width in this representation. Any future change involving
route cardinalities, accumulated counters or more complex arithmetic requires
a new bound audit. Analyzer overflow prevention remains enabled in executions.

## Witness coverage and reporting

The additional scenarios make full-size behaviour explicit:

| Scenario | Required active route | Starting-state interpretation |
|---|---|---|
| `ShowFullRouteWithTraffic` | All pool points | Arbitrary valid state with pending traffic |
| `ShowFullRouteTransmit` | All pool points | Initialisation followed by transmission |
| `ShowFullRouteReceive` | All pool points | Successful reception from a valid state |
| `ShowFullRouteDaemon` | All pool points | Successful forwarding from a valid state |
| `ShowFullRouteInsertion` | All except one fresh point before, all after | Insertion with pending traffic and nonempty inherited history |
| `ShowFullRoutePendingPoll` | All pool points | Valid pending traffic survives a polling stutter |

An insertion into a pool of N points expands a route from N-1 to N. It does not
claim an N-to-N+1 insertion without an additional available point. Likewise,
the existing seven-snapshot two-message example still uses two active points.
It does not become an N-point end-to-end delivery trace merely by increasing a
command scope.

The scalable commands hold message histories at four occurrences by default.
Comparing their runtime with a reference command that increases both route and
history bounds must disclose that different workload. Report the network bound,
message-value bound, history bound, integer width, snapshot count, solver,
resource cap and completion status together. A timeout or resource failure is
an incomplete analysis, never an UNSAT result.

Large completed bounded checks still do not prove eventual delivery. The idle
and polling operations retain their stuttering alternatives. Progress requires
additional assumptions and a separate argument, regardless of network size.

## Low-arity representation for very large point pools

`telecommunications_large.als` is an optional two-snapshot encoding of the
ordered-pool model. In the ordinary scalable representation, a history field
has four columns: State, SPC, sequence index and Message. A large universe can
exceed the Analyzer backend's tuple-indexing capacity for such a relation before
the SAT solver even starts. This is an encoding-capacity failure rather than a
counterexample or a completed safety check.

The low-arity representation declares exactly two states, `Before` and `After`.
Each point owns six fields: `recBefore`, `insBefore`, `sentBefore`, `recAfter`,
`insAfter` and `sentAfter`. Each field has only three columns, SPC, sequence index
and Message. The functions `received[s]`, `pending[s]` and `departed[s]` select
the appropriate field for the singleton state s. Route membership remains a
field of State. Operations use these getter relations in exactly the places
where the ordinary scalable model uses `s.rec`, `s.ins` and `s.sent`.

For any ordered-model instance with two states, choose a bijection from those
states to `Before` and `After` and copy its fields into the six corresponding
history fields. Conversely, combine each pair of history fields into a
state-indexed relation to recover the original two-state representation. These
transformations lose no history entries or route memberships. All two-state
operation constraints and the sectional invariant then have the same meaning
after replacing field access with getter selection. Neither state has an
assumed global sectional invariant, and the intentionally broken receive
operation remains available for the expected counterexample check.

The ten property assertions remain present. The state-only assertions quantify
over both available states, while each transition assertion can choose either
state as pre or post, including choosing the same state if its original
quantifiers permit that. The labels `Before` and `After` are storage slots,
not an extra temporal ordering constraint. Full-route witnesses still require
every pool point to be active in the designated snapshot, and insertion grows
the active set from N-1 to N within an N-point pool.

This model deliberately omits `ShowRepeatedMessageValue`, which requires three
distinct snapshots, and `ShowTwoMessageDelivery`, which requires seven. The
ordinary scalable model retains those examples. A successful low-arity check
does not certify an arbitrary-length execution trace. It establishes only the
declared state or two-state property at the recorded bounds. The fixed-pool
insertion-enabledness qualification and the recorded history bound also
remain in force.

Reducing relation arity addresses one representation limit. It does not promise
that every requested network size or property will solve within the available
time and memory. The scaling report must distinguish completed assertions,
full-size witnesses, timeouts, memory limits and translation-capacity errors.

## Fixed-route specialization

`telecommunications_fixed_route.als` specializes the low-arity model to a fixed
route that contains every available point in the ordered SPC pool. Its topology
fact is `all s: State | s.route = SPC`. The first and last points are therefore
the first and last pool elements, and an active point's successor is simply the
pool's next relation. This avoids repeatedly searching through a changing
active subset to identify the next point.

The specialization follows by substituting `SPC` for the active set in the
low-arity model. The minimum and maximum active points become the pool endpoints,
and the minimum later active point becomes the immediate pool successor. The
message fields, arithmetic, operation updates, frame conditions and validity
contract retain their meanings. The global fact fixes only the topology. It
does not assume that either snapshot satisfies `sectionInvariant` or that its
message histories obey the accounting equations.

An N-point scope in this model means **exactly N active points in one fixed
ordered route**, not arbitrary active subsets of up to N points. Successful
checks apply to that specialization. The eight retained correct-property
assertions cover initialisation, retrieval, transmission, reception and
forwarding, including their external effects or invisibility. The intentional
receive bug and the corresponding traffic and operation witnesses remain
available. Each state or transition still uses only the two storage slots,
with histories bounded independently of network size.

Insertion requires a topology change and is outside this specialization. The
model therefore removes `insertSection`, both insertion assertions, and both
insertion witnesses entirely. It cannot report a successful insertion check
merely because a fixed-route fact made insertion impossible. Insertion evidence
continues to come from the ordered-subset models and must be reported with those
models' actual completed bounds.

This fixed-route model provides a more focused large-network experiment. It
does not enlarge the scope of the dynamic-route or insertion claims, and it
does not establish unbounded correctness or eventual delivery. Its report must
name the fixed topology, exact active size, history bound and included command
set whenever it states a result.

## Arity-2 slot encoding

`telecommunications_slots.als` is a further encoding of the two-snapshot
ordered-pool model. It addresses the two costs that remained after reducing
history fields to arity three.

**Translation capacity.** Kodkod numbers the possible tuples of every relation
with a 32-bit integer, so a relation of arity k over a universe of U atoms can
only be represented when U^k is below about 2.1 × 10^9. With roughly 1,040 atoms
(1,000 points, 32 integers and a few others), arity four needs about 10^12 tuple
indices and fails; arity three needs about 1.1 × 10^9 and is already close to
the limit. The slot encoding stores every history position as its own field,
for example `ins2Before: lone Message` on `SPC`. Every declared relation then
has arity two, which allows universes of roughly 46,000 atoms.

**Arithmetic circuits.** The earlier encodings use `#`, `add` and `sub` for
lengths, prepending, concatenation and buffer offsets. Alloy translates each of
those into adder and counting circuits for every point. The slot encoding uses
five constant `Slot` atoms instead: `S0`..`S3` hold data, newest first, and `S4`
never holds a message. Constant shift relations replace arithmetic:

| Operation | Slot formulation |
|---|---|
| contiguous history | every occupied slot's predecessor is occupied |
| length n | the first unoccupied slot (`marker`) is `Sn` |
| prepend m | `post = S0 -> m + (~shift1).pre`, with `S3` free in `pre` |
| oldest value | the occupied slot without an occupied successor |
| a ++ b | `a + (~shift_len(a)).b`, with no entry of `b` shifted past `S3` |
| buffer offset `#input - #rec[p]` | the shift d with `marker(rec[p]).shift_d = marker(input)` |
| output grows by one | `marker(before).shift1 = marker(after)` |

The model therefore contains no cardinality, no integer arithmetic and no
sequence library. Its `Int` and `seq` scopes are unused and are kept only so the
scaling runner can apply its usual scope and receipt checks.

**Linear route navigation.** The ordered-pool models find the first, last and
next active point with `min`/`max` over transitive closures of the pool order.
Alloy grounds `sectionInvariant`'s boundary condition once per point, and each
grounding builds a closure-based minimum over the whole pool, so the circuit
grows roughly with N³. In a development version of the slot model that still
used closure-based navigation, translating `DaemonPreservesInvariant` at 1,000
points had not finished after more than ten minutes. The slot model instead derives route structure by recursion along the
constant pool order, with constant-size constraints per point:

- `earlier` and `later`: the pool points that have an active point strictly
  before or after them. Then `firstPoint = route - earlier` and
  `lastPoint = route - later`.
- `upcoming`: the first active point strictly after a point (used by the daemon
  and insertion).
- `carried`: the departure history of the nearest active point strictly before a
  point. Boundary agreement becomes "every non-first active point received what
  its predecessor sent", `received[p] = carried[p]`, which pairs the same
  adjacent points as `departed[p] = received[next p]`.

These fields are defined by the fact `derivedRouteStructure`. For any route and
histories exactly one valuation of the derived fields satisfies it, so the fact
does not restrict states or assume validity. Insertion's "fresh point lies in the
gap" condition becomes `nextPoint[post, upstream] = fresh`, which, given
`post.route = pre.route + fresh`, holds exactly when the fresh point lies strictly
between upstream and its old successor in the pool order.

**Fixed history bound.** The bound is four entries per history, matching the
reference model's `4 seq` and the default of the other scalable encodings. It
is declared by the comment `// slot-history-bound: 4`, and `scale_verify.py`
refuses any other `--history-bound` for this model. A different bound requires
adding or removing slot fields; it is not a command-line scope.

**Correspondence.** `scaling_slots_correspondence.als` maps sequence index i of
the reference model to slot `Si` and compares section invariants,
initialisation, retrieval observations and all operation effects, as the
earlier harnesses do. It also compares the external `suffix` predicate and the
"output grew by one" condition directly on arbitrary histories, because those
are the places where slot shifts replace integer arithmetic. The comparison is
bounded evidence at three points. The ordered-pool insertion-enabledness
qualification above applies unchanged.

The slot model, like the other two-snapshot encodings, checks states and
individual transitions. It omits the three- and seven-snapshot demonstrations.

## External SAT solvers and proof checking

Alloy 6.2 bundles SAT4J, MiniSat and Glucose. Its `CNF` transformer
(`-s CNF`) writes the translated problem as a DIMACS file instead of solving
it. `scale_verify.py --solver kissat` (or `cadical`) uses that export:

1. Alloy translates the command and writes `<command>.cnf`. Its receipt and log
   record the translation; the CNF's hash, variable and clause counts are
   recorded before solving.
2. The external solver decides the CNF. Exit code 20 with `s UNSATISFIABLE`
   is an UNSAT result; exit code 10 with `s SATISFIABLE` is SAT; anything else,
   including a timeout, is UNKNOWN. Translation and solving share one deadline.
3. With `--proof`, the solver writes a DRAT proof, and `drat-trim` checks it
   against the same CNF. A result recorded with a proof is accepted only when
   the checker reports `s VERIFIED`. The UNSAT answer then no longer depends on
   trusting the solver, only on Alloy's translation and the proof checker.
   Proof files are deleted after checking because they can be very large.

Two restrictions keep this sound:

- **Empty CNFs are inconclusive.** When Kodkod decides a formula during
  translation, the CNF transformer writes `p cnf 0 0`. That file is satisfiable
  even when the assertion holds, so the runner never interprets it. It reruns
  the command with the built-in fallback solver (`--fallback-solver`, default
  Glucose) and records both the empty translation and the built-in result.
- **External solvers decide only UNSAT-expected checks.** A SAT answer from a
  CNF carries no Alloy instance. Witnesses and the expected bug counterexample
  therefore always use the built-in solver, so their XML instances can still be
  validated (for example, the exact active route length of full-route witnesses).

Kissat, CaDiCaL and drat-trim are not bundled. On Windows the runner calls them
inside WSL when they are not on `PATH`; see [tools/README.md](tools/README.md).

## Unbounded argument

Every Alloy result above is bounded twice: by the number of points and by the
history length. The protocol's structure allows both bounds to be removed for
the safety properties, without enlarging any Alloy scope.

### Locality lemma

`sectionInvariant` (apart from shape conditions) is a conjunction of local terms:

- `C(p)`: `rec[p] = ins[p] ++ sent[p]` for each active point p;
- `B(p, q)`: `sent[p] = rec[q]` for each pair of adjacent active points.

A term's truth depends only on the fields it mentions and, for `B`, on p and q
being adjacent. Each operation's frame condition keeps every other point's
fields unchanged and keeps the route order, so a term that mentions only
unchanged fields of points whose adjacency is unchanged has the same value in
the post-state as in the pre-state. The terms that can change are:

| Operation | Terms that can change |
|---|---|
| transmit | `C(first)`, `B(first, next)` |
| receive | `C(last)`, `B(prev, last)` |
| daemon from U to D | `C(U)`, `C(D)`, `B(prev, U)`, `B(U, D)`, `B(D, next)` |
| insert X between U and D | `C(X)`, `B(U, X)`, `B(X, D)` (and `B(U, D)` disappears) |

So a valid pre-state violates the invariant after a step if and only if one of
these terms fails, and each term mentions at most two points beyond the ones the
operation touches. Missing neighbours (for example a daemon whose upstream point
is first) only remove terms. A counterexample on a route of any length therefore
restricts to a counterexample on a window of at most four adjacent sections.

The external observations are handled the same way. `input` is `rec[first]`,
`output` is `sent[last]`, and `inFlight` is the concatenation of all pending
buffers in route order. Writing that concatenation as `A ++ (window buffers) ++ B`
with arbitrary sequences A and B covers every route length. The retrieve theorem
`input = inFlight ++ output` follows by induction from the last point to the
first, using C at the last point as the base and `C(p)` plus `B(p, next)` as the
step, as already shown in "Pending messages without a sum over the network".

### Machine-checked obligations

`unbounded_check.py` states each window obligation over Z3's theory of
sequences with an uninterpreted message sort, so it covers histories of every
length and any number of message values. It proves invariant preservation and
the external effect (or invisibility) of transmit, receive, daemon, insertion
and the idle stutter, initial validity, and the base and step of the retrieve
induction. It also requires a counterexample for the newest-first receive bug
and satisfiable witnesses, so the premises are not contradictory. The latest
results are in [results/unbounded_summary.md](results/unbounded_summary.md).

The Alloy small-scope checks and the Z3 obligations support each other:

- Z3 removes both bounds, but its encoding is a hand translation of the Alloy
  predicates, and the locality lemma above is a paper argument.
- Alloy checks the actual predicates, including their frame conditions, but only
  up to a bound. The lemma shows a window of at most four sections suffices for
  network size, and the reference model's completed checks at four points, and
  the ordered models' completed checks at six and eight points, exceed it.

Remaining qualifications: Z3's soundness is assumed; the encoding and lemma are
not mechanically connected to the Alloy source; the ordered-pool insertion
enabledness caveat still applies to the ordered models.

### Liveness is a separate question

Eventual delivery is not a safety property and none of the above implies it.
`receivePoll` and `daemonOrIdle` deliberately permit idle steps forever, and the
model does not need to make progress. A delivery argument requires:

1. a **fairness assumption**: if a successful daemon step (respectively receive)
   stays enabled, it eventually happens; and
2. a **variant**: for each pending occurrence, the number of sections it still
   has to traverse. Each successful daemon or receive step that moves the
   occurrence decreases it, transmit does not increase it, and insertion can
   increase it only finitely often if insertions are finite.

With finitely many insertions, fairness forces every pending occurrence to reach
the output. Bounded lasso checks of this argument are possible with Alloy 6
temporal operators (fairness written as facts over traces), or in TLA+ with
weak fairness. The project does not currently mechanize it.
