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
