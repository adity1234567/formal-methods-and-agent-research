# Larger-network verification results

Report generated: 2026-11-15T08:55:37+06:00 (Asia/Dhaka).

This report distinguishes completed property checks from satisfiable examples. A witness with N active points shows that such a state or transition exists. It does not establish all protocol properties at N points. A timeout or translation failure remains UNKNOWN, even if another attempt later succeeds.

## Coverage by model and scope

Counts combine validated completed commands only when the frozen source hash and network/history/message/integer bounds match. Each command retains its declared snapshot count. The fixed-route model has eight property checks and excludes insertion. The other models have ten. History length bounds lifetime recorded occurrences, including repeated message values.

| Representation | Points | History length | Message values | Int bits | Property checks completed | Expected bug found | Exact-size traffic witness |
|---|---:|---:|---:|---:|---:|---|---|
| [Original sequence route](../telecommunications.als) | up to 6 | 6 | 4 | 7 | 0/10 | not established | yes |
| [Fixed full route, two slots](../telecommunications_fixed_route.als) | exactly 100 | 2 | 4 | 5 | 4/8 | yes | yes |
| [Fixed full route, two slots](../telecommunications_fixed_route.als) | exactly 1000 | 1 | 1 | 5 | 1/8 | not established | yes |
| [Fixed full route, two slots](../telecommunications_fixed_route.als) | exactly 1000 | 4 | 4 | 5 | 0/8 | not established | not established |
| [Ordered route, two slots](../telecommunications_large.als) | up to 10 | 2 | 4 | 5 | 10/10 | yes | yes |
| [Ordered route, two slots](../telecommunications_large.als) | up to 20 | 2 | 4 | 5 | 3/10 | yes | yes |
| [Ordered route, two slots](../telecommunications_large.als) | up to 1000 | 4 | 4 | 5 | 0/10 | not established | not established |
| [Ordered active route](../telecommunications_scalable.als) | up to 6 | 4 | 4 | 5 | 10/10 | yes | yes |
| [Ordered active route](../telecommunications_scalable.als) | up to 8 | 4 | 4 | 5 | 10/10 | yes | yes |
| [Ordered active route](../telecommunications_scalable.als) | up to 10 | 4 | 4 | 5 | 1/10 | yes | yes |
| [Ordered active route](../telecommunications_scalable.als) | up to 100 | 4 | 4 | 5 | 1/10 | not established | yes |
| [Ordered active route](../telecommunications_scalable.als) | up to 1000 | 4 | 4 | 5 | 0/10 | not established | not established |
| [Ordered route, position fields (arity 2)](../telecommunications_slots.als) | up to 10 | 4 | 4 | 5 | 10/10 | yes | yes |
| [Ordered route, position fields (arity 2)](../telecommunications_slots.als) | up to 20 | 4 | 4 | 5 | 4/10 | yes | yes |
| [Ordered route, position fields (arity 2)](../telecommunications_slots.als) | up to 100 | 4 | 4 | 5 | 1/10 | yes | yes |

## What changed

The ordered models decouple route size from message-history length and compute pending sequence offsets from arrival-history lengths. The two-slot model reduces stored history relations from arity four to arity three. The fixed-route specialization uses direct neighbours on a full ordered route and deliberately omits insertion.

Ordered-pool models restrict a particular fresh point to its fixed position when inserting. Their safety correspondence uses compatible point renaming and does not establish every original insertion enabledness obligation. The two-slot models check states and individual transitions, not the three/seven-snapshot demonstrations. See [the design and mathematical argument](../scaling_design.md).

The earlier 1,000-point ordered model with four-column history fields hit Alloy's translation capacity before solving. Lower-arity variants address that representation limit, but remain subject to solver time and memory costs. Timeouts and translation/resource failures do not provide counterexamples.

The position-field model (telecommunications_slots.als) stores every history position as its own arity-2 field and replaces lengths, offsets and concatenation by constant slot shifts, so its SAT problems contain no integer circuits and its relations stay far below the translation capacity. Its history bound is fixed at four entries. Some of its checks were decided by Kissat or CaDiCaL from Alloy's CNF export; the Solver column says which, and whether a DRAT proof was verified. External solvers only decide UNSAT-expected checks; witnesses use a built-in solver.

## Unbounded safety argument

Bounded network sizes are not the only evidence. A locality lemma reduces every safety obligation to a window of at most four adjacent sections, and Z3 proves the window obligations for histories of any length; see [the unbounded argument](../scaling_design.md#unbounded-argument) and [its results](unbounded_summary.md). The large-scope runs below are therefore capacity measurements and full-size examples, not the basis of the safety claim.

## Bounded correspondence

The correspondence harnesses compare paired representations at three points, four-entry histories and six-bit integers. They compare validity, initialisation, retrieval and operation effects without assuming either post-state invariant. Their results are bounded evidence, not an unbounded equivalence theorem.

Coverage below combines matching-source retries; unsuccessful attempts remain linked.

| Harness | UNSAT comparison checks | SAT paired-operation witnesses |
|---|---:|---:|
| [scaling_correspondence.als](../scaling_correspondence.als) | 7/7 | 4/4 |
| [scaling_large_correspondence.als](../scaling_large_correspondence.als) | 7/7 | 4/4 |
| [scaling_slots_correspondence.als](../scaling_slots_correspondence.als) | 8/8 | 4/4 |

### `scaling_correspondence.als`

- [`DaemonEffectsCorrespond`](../scale-results/correspondence-20261107-234959-f1e1a2/DaemonEffectsCorrespond/execution.json)
- [`InitialStatesCorrespond`](../scale-results/correspondence-20261107-234959-f1e1a2/InitialStatesCorrespond/execution.json)
- [`InsertionEffectsCorrespond`](../scale-results/correspondence-20261107-234959-f1e1a2/InsertionEffectsCorrespond/execution.json)
- [`ReceiveEffectsCorrespond`](../scale-results/correspondence-20261107-234959-f1e1a2/ReceiveEffectsCorrespond/execution.json)
- [`RetrieveObservationsCorrespond`](../scale-results/correspondence-20261107-234959-f1e1a2/RetrieveObservationsCorrespond/execution.json)
- [`SectionInvariantsCorrespond`](../scale-results/correspondence-20261107-234959-f1e1a2/SectionInvariantsCorrespond/execution.json)
- [`ShowCorrespondingDaemon`](../scale-results/correspondence-20261107-234959-f1e1a2/ShowCorrespondingDaemon/execution.json)
- [`ShowCorrespondingInsertion`](../scale-results/correspondence-20261107-234959-f1e1a2/ShowCorrespondingInsertion/execution.json)
- [`ShowCorrespondingReceive`](../scale-results/correspondence-20261107-234959-f1e1a2/ShowCorrespondingReceive/execution.json)
- [`ShowCorrespondingTransmit`](../scale-results/correspondence-20261107-234959-f1e1a2/ShowCorrespondingTransmit/execution.json)
- [`TransmitEffectsCorrespond`](../scale-results/correspondence-20261107-234959-f1e1a2/TransmitEffectsCorrespond/execution.json)

### `scaling_large_correspondence.als`

- [`DaemonEffectsCorrespond`](../scale-results/correspondence-large-20261107-235757-f8d64c/DaemonEffectsCorrespond/execution.json)
- [`InitialStatesCorrespond`](../scale-results/correspondence-large-20261107-235506-d49938/InitialStatesCorrespond/execution.json)
- [`InsertionEffectsCorrespond`](../scale-results/correspondence-large-20261107-235506-d49938/InsertionEffectsCorrespond/execution.json)
- [`ReceiveEffectsCorrespond`](../scale-results/correspondence-large-20261107-235506-d49938/ReceiveEffectsCorrespond/execution.json)
- [`RetrieveObservationsCorrespond`](../scale-results/correspondence-large-20261107-235506-d49938/RetrieveObservationsCorrespond/execution.json)
- [`SectionInvariantsCorrespond`](../scale-results/correspondence-large-20261107-235506-d49938/SectionInvariantsCorrespond/execution.json)
- [`ShowCorrespondingDaemon`](../scale-results/correspondence-large-20261107-235506-d49938/ShowCorrespondingDaemon/execution.json)
- [`ShowCorrespondingInsertion`](../scale-results/correspondence-large-20261107-235506-d49938/ShowCorrespondingInsertion/execution.json)
- [`ShowCorrespondingReceive`](../scale-results/correspondence-large-20261107-235506-d49938/ShowCorrespondingReceive/execution.json)
- [`ShowCorrespondingTransmit`](../scale-results/correspondence-large-20261107-235506-d49938/ShowCorrespondingTransmit/execution.json)
- [`TransmitEffectsCorrespond`](../scale-results/correspondence-large-20261107-235506-d49938/TransmitEffectsCorrespond/execution.json)

### `scaling_slots_correspondence.als`

- [`DaemonEffectsCorrespond`](../scale-results/correspondence-slots-20261115-021530-4b9237/DaemonEffectsCorrespond/execution.json)
- [`ExternalPredicatesCorrespond`](../scale-results/correspondence-slots-20261115-021530-4b9237/ExternalPredicatesCorrespond/execution.json)
- [`InitialStatesCorrespond`](../scale-results/correspondence-slots-20261115-021530-4b9237/InitialStatesCorrespond/execution.json)
- [`InsertionEffectsCorrespond`](../scale-results/correspondence-slots-20261115-021530-4b9237/InsertionEffectsCorrespond/execution.json)
- [`ReceiveEffectsCorrespond`](../scale-results/correspondence-slots-20261115-021530-4b9237/ReceiveEffectsCorrespond/execution.json)
- [`RetrieveObservationsCorrespond`](../scale-results/correspondence-slots-20261115-021530-4b9237/RetrieveObservationsCorrespond/execution.json)
- [`SectionInvariantsCorrespond`](../scale-results/correspondence-slots-20261115-021530-4b9237/SectionInvariantsCorrespond/execution.json)
- [`ShowCorrespondingDaemon`](../scale-results/correspondence-slots-20261115-021530-4b9237/ShowCorrespondingDaemon/execution.json)
- [`ShowCorrespondingInsertion`](../scale-results/correspondence-slots-20261115-021530-4b9237/ShowCorrespondingInsertion/execution.json)
- [`ShowCorrespondingReceive`](../scale-results/correspondence-slots-20261115-021530-4b9237/ShowCorrespondingReceive/execution.json)
- [`ShowCorrespondingTransmit`](../scale-results/correspondence-slots-20261115-021530-4b9237/ShowCorrespondingTransmit/execution.json)
- [`TransmitEffectsCorrespond`](../scale-results/correspondence-slots-20261115-021530-4b9237/TransmitEffectsCorrespond/execution.json)

All correspondence attempts:

- [correspondence-20261107-234959-f1e1a2](../scale-results/correspondence-20261107-234959-f1e1a2/summary.md): completed; all selected expectations validated: yes.
- [correspondence-large-20261107-235433-2b0d8f](../scale-results/correspondence-large-20261107-235433-2b0d8f/summary.md): failed_before_execution; all selected expectations validated: no.
- [correspondence-large-20261107-235506-d49938](../scale-results/correspondence-large-20261107-235506-d49938/summary.md): completed; all selected expectations validated: no.
- [correspondence-large-20261107-235757-f8d64c](../scale-results/correspondence-large-20261107-235757-f8d64c/summary.md): completed; all selected expectations validated: yes.
- [correspondence-slots-20261115-021530-4b9237](../scale-results/correspondence-slots-20261115-021530-4b9237/summary.md): completed; all selected expectations validated: yes.

## Resource and interpretation limits

Commands have independent wall-clock deadlines. The recorded JVM heap cap is not a measurement of peak process memory, and native solver allocations are additional. Some experiments ran concurrently on the same machine, so elapsed times are execution records rather than a controlled performance comparison. Baseline and optimized runs also use different history bounds in several cases.

The benchmark host is a laptop with Modern Standby. Runs recorded from 15 November 2026 carry the time the host spent in standby during the command; a timing marked "host asleep" overstates the solving time and its deadline was not enforced in real time. Its outcome is still validated normally. The runner now keeps Windows and the display awake while a suite runs (disable with --allow-sleep). External solvers run inside WSL, which on this host is limited to 4 GB of memory and 4 processors.

No completed finite scope proves eventual delivery, fairness, or complete SS7 conformance. Arbitrary network size and history length are addressed only for safety, by the separate unbounded argument. Optional polling and idle steps still permit indefinite waiting.

## Detailed validated evidence

### Original sequence route: up to 6 points, history 6, message values 4, 7-bit Int

Frozen model SHA-256: `47d76e1f6c80954afd8b2ea0607486f4a410a80298a5d7bfd98573c4ade47621`.

Property coverage is incomplete. Missing validated checks: `DaemonIsInvisible`, `DaemonPreservesInvariant`, `InitialIsValid`, `InsertionIsInvisible`, `InsertionPreservesInvariant`, `ReceivePreservesInvariant`, `ReceiveRefinesExternal`, `RetrieveIsValid`, `TransmitPreservesInvariant`, `TransmitRefinesExternal`.

| Command | Validated outcome | Solver | Seconds | Exact active route lengths | Evidence |
|---|---|---|---:|---|---|
| `ShowExactRouteWithTraffic` | SAT | glucose | 2.375 | [6] | [record](../scale-results/scale-20261107-234635-73369e/points-6/ShowExactRouteWithTraffic/execution.json) |

Incomplete/failed attempts retained for this scope: 2.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-234635-73369e/summary.md)

### Fixed full route, two slots: exactly 100 points, history 2, message values 4, 5-bit Int

Frozen model SHA-256: `182c9179911ef07a62dc50d4592494e4adbbd7a35db9d146633de7c526df47c3`.

Property coverage is incomplete. Missing validated checks: `DaemonIsInvisible`, `DaemonPreservesInvariant`, `ReceivePreservesInvariant`, `RetrieveIsValid`.

| Command | Validated outcome | Solver | Seconds | Exact active route lengths | Evidence |
|---|---|---|---:|---|---|
| `BrokenReceiveWouldPreserveInvariant` | SAT | glucose | 22.050 | not an exact-size witness | [record](../scale-results/scale-20261108-000209-396a0b/points-100/BrokenReceiveWouldPreserveInvariant/execution.json) |
| `InitialIsValid` | UNSAT | glucose | 4.091 | not an exact-size witness | [record](../scale-results/scale-20261108-000209-396a0b/points-100/InitialIsValid/execution.json) |
| `ReceiveRefinesExternal` | UNSAT | glucose | 18.097 | not an exact-size witness | [record](../scale-results/scale-20261108-000209-396a0b/points-100/ReceiveRefinesExternal/execution.json) |
| `ShowDaemon` | SAT | glucose | 2.179 | not an exact-size witness | [record](../scale-results/scale-20261108-000209-396a0b/points-100/ShowDaemon/execution.json) |
| `ShowFullRouteDaemon` | SAT | glucose | 2.622 | [100, 100] | [record](../scale-results/scale-20261108-000209-396a0b/points-100/ShowFullRouteDaemon/execution.json) |
| `ShowFullRoutePendingPoll` | SAT | glucose | 2.615 | [100, 100] | [record](../scale-results/scale-20261108-000209-396a0b/points-100/ShowFullRoutePendingPoll/execution.json) |
| `ShowFullRouteReceive` | SAT | glucose | 2.654 | [100, 100] | [record](../scale-results/scale-20261108-000209-396a0b/points-100/ShowFullRouteReceive/execution.json) |
| `ShowFullRouteTransmit` | SAT | glucose | 2.533 | [100, 100] | [record](../scale-results/scale-20261108-000209-396a0b/points-100/ShowFullRouteTransmit/execution.json) |
| `ShowFullRouteWithTraffic` | SAT | glucose | 2.107 | [100] | [record](../scale-results/scale-20261108-000209-396a0b/points-100/ShowFullRouteWithTraffic/execution.json) |
| `ShowPendingPollCanStutter` | SAT | glucose | 2.510 | not an exact-size witness | [record](../scale-results/scale-20261108-000209-396a0b/points-100/ShowPendingPollCanStutter/execution.json) |
| `ShowReceive` | SAT | glucose | 2.119 | not an exact-size witness | [record](../scale-results/scale-20261108-000209-396a0b/points-100/ShowReceive/execution.json) |
| `ShowTransmit` | SAT | glucose | 1.903 | not an exact-size witness | [record](../scale-results/scale-20261108-000209-396a0b/points-100/ShowTransmit/execution.json) |
| `TransmitPreservesInvariant` | UNSAT | glucose | 33.914 | not an exact-size witness | [record](../scale-results/scale-20261108-000209-396a0b/points-100/TransmitPreservesInvariant/execution.json) |
| `TransmitRefinesExternal` | UNSAT | glucose | 8.410 | not an exact-size witness | [record](../scale-results/scale-20261108-000209-396a0b/points-100/TransmitRefinesExternal/execution.json) |

Incomplete/failed attempts retained for this scope: 4.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261108-000209-396a0b/summary.md)

### Fixed full route, two slots: exactly 1000 points, history 1, message values 1, 5-bit Int

Frozen model SHA-256: `182c9179911ef07a62dc50d4592494e4adbbd7a35db9d146633de7c526df47c3`.

Property coverage is incomplete. Missing validated checks: `DaemonIsInvisible`, `DaemonPreservesInvariant`, `ReceivePreservesInvariant`, `ReceiveRefinesExternal`, `RetrieveIsValid`, `TransmitPreservesInvariant`, `TransmitRefinesExternal`.

| Command | Validated outcome | Solver | Seconds | Exact active route lengths | Evidence |
|---|---|---|---:|---|---|
| `InitialIsValid` | UNSAT | glucose | 42.337 | not an exact-size witness | [record](../scale-results/scale-20261108-000439-d89215/points-1000/InitialIsValid/execution.json) |
| `ShowFullRouteTransmit` | SAT | glucose | 44.363 | [1000, 1000] | [record](../scale-results/scale-20261108-000815-2b6381/points-1000/ShowFullRouteTransmit/execution.json) |
| `ShowFullRouteWithTraffic` | SAT | glucose | 59.052 | [1000] | [record](../scale-results/scale-20261108-000439-d89215/points-1000/ShowFullRouteWithTraffic/execution.json) |

Incomplete/failed attempts retained for this scope: 1.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261108-000439-d89215/summary.md)
- [Full suite including unsuccessful attempts](../scale-results/scale-20261108-000815-2b6381/summary.md)

### Fixed full route, two slots: exactly 1000 points, history 4, message values 4, 5-bit Int

Frozen model SHA-256: `182c9179911ef07a62dc50d4592494e4adbbd7a35db9d146633de7c526df47c3`.

Property coverage is incomplete. Missing validated checks: `DaemonIsInvisible`, `DaemonPreservesInvariant`, `InitialIsValid`, `ReceivePreservesInvariant`, `ReceiveRefinesExternal`, `RetrieveIsValid`, `TransmitPreservesInvariant`, `TransmitRefinesExternal`.

| Command | Validated outcome | Solver | Seconds | Exact active route lengths | Evidence |
|---|---|---|---:|---|---|

Incomplete/failed attempts retained for this scope: 2.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261108-000001-afc7d1/summary.md)

### Ordered route, two slots: up to 10 points, history 2, message values 4, 5-bit Int

Frozen model SHA-256: `1395072cf94608a7d202ced6a66dfec9bdcda9f3a3ac2c857a477d8917f3169b`.

All property checks declared for this representation completed with validated UNSAT results.

| Command | Validated outcome | Solver | Seconds | Exact active route lengths | Evidence |
|---|---|---|---:|---|---|
| `BrokenReceiveWouldPreserveInvariant` | SAT | glucose | 1.788 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/BrokenReceiveWouldPreserveInvariant/execution.json) |
| `DaemonIsInvisible` | UNSAT | glucose | 34.158 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/DaemonIsInvisible/execution.json) |
| `DaemonPreservesInvariant` | UNSAT | glucose | 31.469 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/DaemonPreservesInvariant/execution.json) |
| `InitialIsValid` | UNSAT | glucose | 1.127 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/InitialIsValid/execution.json) |
| `InsertionIsInvisible` | UNSAT | glucose | 7.437 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/InsertionIsInvisible/execution.json) |
| `InsertionPreservesInvariant` | UNSAT | glucose | 23.312 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/InsertionPreservesInvariant/execution.json) |
| `ReceivePreservesInvariant` | UNSAT | glucose | 20.719 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ReceivePreservesInvariant/execution.json) |
| `ReceiveRefinesExternal` | UNSAT | glucose | 14.236 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ReceiveRefinesExternal/execution.json) |
| `RetrieveIsValid` | UNSAT | glucose | 20.793 | not an exact-size witness | [record](../scale-results/scale-20261108-000209-aed205/points-10/RetrieveIsValid/execution.json) |
| `ShowDaemon` | SAT | glucose | 1.485 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowDaemon/execution.json) |
| `ShowFullRouteDaemon` | SAT | glucose | 2.148 | [10, 10] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowFullRouteDaemon/execution.json) |
| `ShowFullRouteInsertion` | SAT | glucose | 1.425 | [9, 10] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowFullRouteInsertion/execution.json) |
| `ShowFullRoutePendingPoll` | SAT | glucose | 2.085 | [10, 10] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowFullRoutePendingPoll/execution.json) |
| `ShowFullRouteReceive` | SAT | glucose | 1.649 | [10, 10] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowFullRouteReceive/execution.json) |
| `ShowFullRouteTransmit` | SAT | glucose | 1.892 | [10, 10] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowFullRouteTransmit/execution.json) |
| `ShowFullRouteWithTraffic` | SAT | glucose | 1.573 | [10] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowFullRouteWithTraffic/execution.json) |
| `ShowInsertionWithTraffic` | SAT | glucose | 1.620 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowInsertionWithTraffic/execution.json) |
| `ShowPendingPollCanStutter` | SAT | glucose | 1.574 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowPendingPollCanStutter/execution.json) |
| `ShowReceive` | SAT | glucose | 1.503 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowReceive/execution.json) |
| `ShowTransmit` | SAT | glucose | 1.434 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowTransmit/execution.json) |
| `TransmitPreservesInvariant` | UNSAT | glucose | 13.100 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/TransmitPreservesInvariant/execution.json) |
| `TransmitRefinesExternal` | UNSAT | glucose | 1.894 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/TransmitRefinesExternal/execution.json) |

Incomplete/failed attempts retained for this scope: 1.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-235628-5c0dd7/summary.md)
- [Full suite including unsuccessful attempts](../scale-results/scale-20261108-000209-aed205/summary.md)

### Ordered route, two slots: up to 20 points, history 2, message values 4, 5-bit Int

Frozen model SHA-256: `1395072cf94608a7d202ced6a66dfec9bdcda9f3a3ac2c857a477d8917f3169b`.

Property coverage is incomplete. Missing validated checks: `DaemonIsInvisible`, `DaemonPreservesInvariant`, `InsertionIsInvisible`, `InsertionPreservesInvariant`, `ReceivePreservesInvariant`, `ReceiveRefinesExternal`, `RetrieveIsValid`.

| Command | Validated outcome | Solver | Seconds | Exact active route lengths | Evidence |
|---|---|---|---:|---|---|
| `BrokenReceiveWouldPreserveInvariant` | SAT | glucose | 1.813 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/BrokenReceiveWouldPreserveInvariant/execution.json) |
| `InitialIsValid` | UNSAT | glucose | 8.184 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/InitialIsValid/execution.json) |
| `ShowDaemon` | SAT | glucose | 1.391 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowDaemon/execution.json) |
| `ShowFullRouteDaemon` | SAT | glucose | 1.471 | [20, 20] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowFullRouteDaemon/execution.json) |
| `ShowFullRouteInsertion` | SAT | glucose | 1.453 | [19, 20] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowFullRouteInsertion/execution.json) |
| `ShowFullRoutePendingPoll` | SAT | glucose | 1.707 | [20, 20] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowFullRoutePendingPoll/execution.json) |
| `ShowFullRouteReceive` | SAT | glucose | 1.407 | [20, 20] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowFullRouteReceive/execution.json) |
| `ShowFullRouteTransmit` | SAT | glucose | 1.401 | [20, 20] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowFullRouteTransmit/execution.json) |
| `ShowFullRouteWithTraffic` | SAT | glucose | 1.665 | [20] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowFullRouteWithTraffic/execution.json) |
| `ShowInsertionWithTraffic` | SAT | glucose | 1.599 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowInsertionWithTraffic/execution.json) |
| `ShowPendingPollCanStutter` | SAT | glucose | 1.467 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowPendingPollCanStutter/execution.json) |
| `ShowReceive` | SAT | glucose | 1.489 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowReceive/execution.json) |
| `ShowTransmit` | SAT | glucose | 1.736 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowTransmit/execution.json) |
| `TransmitPreservesInvariant` | UNSAT | glucose | 30.561 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/TransmitPreservesInvariant/execution.json) |
| `TransmitRefinesExternal` | UNSAT | glucose | 5.957 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/TransmitRefinesExternal/execution.json) |

Incomplete/failed attempts retained for this scope: 7.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-235628-5c0dd7/summary.md)

### Ordered route, two slots: up to 1000 points, history 4, message values 4, 5-bit Int

Frozen model SHA-256: `1395072cf94608a7d202ced6a66dfec9bdcda9f3a3ac2c857a477d8917f3169b`.

Property coverage is incomplete. Missing validated checks: `DaemonIsInvisible`, `DaemonPreservesInvariant`, `InitialIsValid`, `InsertionIsInvisible`, `InsertionPreservesInvariant`, `ReceivePreservesInvariant`, `ReceiveRefinesExternal`, `RetrieveIsValid`, `TransmitPreservesInvariant`, `TransmitRefinesExternal`.

| Command | Validated outcome | Solver | Seconds | Exact active route lengths | Evidence |
|---|---|---|---:|---|---|

Incomplete/failed attempts retained for this scope: 2.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-235427-e46017/summary.md)

### Ordered active route: up to 6 points, history 4, message values 4, 5-bit Int

Frozen model SHA-256: `05cb357750fabcac8b6ec7e5d2f8ddbd1d74d6896856162bd48f507b87d2dba9`.

All property checks declared for this representation completed with validated UNSAT results.

| Command | Validated outcome | Solver | Seconds | Exact active route lengths | Evidence |
|---|---|---|---:|---|---|
| `BrokenReceiveWouldPreserveInvariant` | SAT | glucose | 1.554 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/BrokenReceiveWouldPreserveInvariant/execution.json) |
| `DaemonIsInvisible` | UNSAT | glucose | 35.030 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/DaemonIsInvisible/execution.json) |
| `DaemonPreservesInvariant` | UNSAT | glucose | 26.902 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/DaemonPreservesInvariant/execution.json) |
| `InitialIsValid` | UNSAT | glucose | 1.222 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/InitialIsValid/execution.json) |
| `InsertionIsInvisible` | UNSAT | glucose | 15.001 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/InsertionIsInvisible/execution.json) |
| `InsertionPreservesInvariant` | UNSAT | glucose | 12.491 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/InsertionPreservesInvariant/execution.json) |
| `ReceivePreservesInvariant` | UNSAT | glucose | 15.483 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/ReceivePreservesInvariant/execution.json) |
| `ReceiveRefinesExternal` | UNSAT | glucose | 13.448 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/ReceiveRefinesExternal/execution.json) |
| `RetrieveIsValid` | UNSAT | glucose | 11.640 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/RetrieveIsValid/execution.json) |
| `ShowDaemon` | SAT | glucose | 2.078 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowDaemon/execution.json) |
| `ShowFullRouteDaemon` | SAT | glucose | 2.647 | [6, 6] | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowFullRouteDaemon/execution.json) |
| `ShowFullRouteInsertion` | SAT | glucose | 1.746 | [6, 5] | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowFullRouteInsertion/execution.json) |
| `ShowFullRoutePendingPoll` | SAT | glucose | 2.331 | [6, 6] | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowFullRoutePendingPoll/execution.json) |
| `ShowFullRouteReceive` | SAT | glucose | 1.939 | [6, 6] | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowFullRouteReceive/execution.json) |
| `ShowFullRouteTransmit` | SAT | glucose | 1.437 | [6, 6] | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowFullRouteTransmit/execution.json) |
| `ShowFullRouteWithTraffic` | SAT | glucose | 1.531 | [6] | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowFullRouteWithTraffic/execution.json) |
| `ShowInsertionWithTraffic` | SAT | glucose | 1.720 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowInsertionWithTraffic/execution.json) |
| `ShowPendingPollCanStutter` | SAT | glucose | 1.815 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowPendingPollCanStutter/execution.json) |
| `ShowReceive` | SAT | glucose | 2.048 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowReceive/execution.json) |
| `ShowRepeatedMessageValue` | SAT | glucose | 1.446 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowRepeatedMessageValue/execution.json) |
| `ShowTransmit` | SAT | glucose | 1.542 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowTransmit/execution.json) |
| `ShowTwoMessageDelivery` | SAT | glucose | 2.380 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowTwoMessageDelivery/execution.json) |
| `TransmitPreservesInvariant` | UNSAT | glucose | 7.373 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/TransmitPreservesInvariant/execution.json) |
| `TransmitRefinesExternal` | UNSAT | glucose | 5.242 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/TransmitRefinesExternal/execution.json) |

Incomplete/failed attempts retained for this scope: 0.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-234711-010fee/summary.md)

### Ordered active route: up to 8 points, history 4, message values 4, 5-bit Int

Frozen model SHA-256: `05cb357750fabcac8b6ec7e5d2f8ddbd1d74d6896856162bd48f507b87d2dba9`.

All property checks declared for this representation completed with validated UNSAT results.

| Command | Validated outcome | Solver | Seconds | Exact active route lengths | Evidence |
|---|---|---|---:|---|---|
| `BrokenReceiveWouldPreserveInvariant` | SAT | glucose | 2.064 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/BrokenReceiveWouldPreserveInvariant/execution.json) |
| `DaemonIsInvisible` | UNSAT | glucose | 214.057 | not an exact-size witness | [record](../scale-results/scale-20261108-000508-0b544b/points-8/DaemonIsInvisible/execution.json) |
| `DaemonPreservesInvariant` | UNSAT | glucose | 133.894 | not an exact-size witness | [record](../scale-results/scale-20261107-235347-e17c94/points-8/DaemonPreservesInvariant/execution.json) |
| `InitialIsValid` | UNSAT | glucose | 2.048 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/InitialIsValid/execution.json) |
| `InsertionIsInvisible` | UNSAT | glucose | 94.232 | not an exact-size witness | [record](../scale-results/scale-20261107-235942-c5fbcf/points-8/InsertionIsInvisible/execution.json) |
| `InsertionPreservesInvariant` | UNSAT | glucose | 40.590 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/InsertionPreservesInvariant/execution.json) |
| `ReceivePreservesInvariant` | UNSAT | glucose | 38.962 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/ReceivePreservesInvariant/execution.json) |
| `ReceiveRefinesExternal` | UNSAT | glucose | 89.359 | not an exact-size witness | [record](../scale-results/scale-20261107-235942-c5fbcf/points-8/ReceiveRefinesExternal/execution.json) |
| `RetrieveIsValid` | UNSAT | glucose | 24.324 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/RetrieveIsValid/execution.json) |
| `ShowDaemon` | SAT | glucose | 2.087 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowDaemon/execution.json) |
| `ShowFullRouteDaemon` | SAT | glucose | 2.421 | [8, 8] | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowFullRouteDaemon/execution.json) |
| `ShowFullRouteInsertion` | SAT | glucose | 2.431 | [7, 8] | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowFullRouteInsertion/execution.json) |
| `ShowFullRoutePendingPoll` | SAT | glucose | 2.313 | [8, 8] | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowFullRoutePendingPoll/execution.json) |
| `ShowFullRouteReceive` | SAT | glucose | 2.984 | [8, 8] | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowFullRouteReceive/execution.json) |
| `ShowFullRouteTransmit` | SAT | glucose | 2.576 | [8, 8] | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowFullRouteTransmit/execution.json) |
| `ShowFullRouteWithTraffic` | SAT | glucose | 1.894 | [8] | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowFullRouteWithTraffic/execution.json) |
| `ShowInsertionWithTraffic` | SAT | glucose | 2.276 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowInsertionWithTraffic/execution.json) |
| `ShowPendingPollCanStutter` | SAT | glucose | 2.345 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowPendingPollCanStutter/execution.json) |
| `ShowReceive` | SAT | glucose | 2.142 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowReceive/execution.json) |
| `ShowRepeatedMessageValue` | SAT | glucose | 1.941 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowRepeatedMessageValue/execution.json) |
| `ShowTransmit` | SAT | glucose | 1.917 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowTransmit/execution.json) |
| `ShowTwoMessageDelivery` | SAT | glucose | 2.624 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowTwoMessageDelivery/execution.json) |
| `TransmitPreservesInvariant` | UNSAT | glucose | 16.877 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/TransmitPreservesInvariant/execution.json) |
| `TransmitRefinesExternal` | UNSAT | glucose | 21.405 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/TransmitRefinesExternal/execution.json) |

Incomplete/failed attempts retained for this scope: 5.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-234711-010fee/summary.md)
- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-235347-e17c94/summary.md)
- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-235942-c5fbcf/summary.md)
- [Full suite including unsuccessful attempts](../scale-results/scale-20261108-000508-0b544b/summary.md)

### Ordered active route: up to 10 points, history 4, message values 4, 5-bit Int

Frozen model SHA-256: `05cb357750fabcac8b6ec7e5d2f8ddbd1d74d6896856162bd48f507b87d2dba9`.

Property coverage is incomplete. Missing validated checks: `DaemonIsInvisible`, `DaemonPreservesInvariant`, `InsertionIsInvisible`, `InsertionPreservesInvariant`, `ReceivePreservesInvariant`, `ReceiveRefinesExternal`, `RetrieveIsValid`, `TransmitPreservesInvariant`, `TransmitRefinesExternal`.

| Command | Validated outcome | Solver | Seconds | Exact active route lengths | Evidence |
|---|---|---|---:|---|---|
| `BrokenReceiveWouldPreserveInvariant` | SAT | glucose | 3.948 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-10/BrokenReceiveWouldPreserveInvariant/execution.json) |
| `InitialIsValid` | UNSAT | glucose | 1.755 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-10/InitialIsValid/execution.json) |
| `ShowDaemon` | SAT | glucose | 2.453 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowDaemon/execution.json) |
| `ShowFullRouteDaemon` | SAT | glucose | 2.411 | [10, 10] | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowFullRouteDaemon/execution.json) |
| `ShowFullRouteInsertion` | SAT | glucose | 2.441 | [10, 9] | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowFullRouteInsertion/execution.json) |
| `ShowFullRoutePendingPoll` | SAT | glucose | 3.483 | [10, 10] | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowFullRoutePendingPoll/execution.json) |
| `ShowFullRouteReceive` | SAT | glucose | 2.454 | [10, 10] | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowFullRouteReceive/execution.json) |
| `ShowFullRouteTransmit` | SAT | glucose | 2.250 | [10, 10] | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowFullRouteTransmit/execution.json) |
| `ShowFullRouteWithTraffic` | SAT | glucose | 2.180 | [10] | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowFullRouteWithTraffic/execution.json) |
| `ShowInsertionWithTraffic` | SAT | glucose | 2.485 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowInsertionWithTraffic/execution.json) |
| `ShowPendingPollCanStutter` | SAT | glucose | 2.403 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowPendingPollCanStutter/execution.json) |
| `ShowReceive` | SAT | glucose | 2.526 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowReceive/execution.json) |
| `ShowRepeatedMessageValue` | SAT | glucose | 2.028 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowRepeatedMessageValue/execution.json) |
| `ShowTransmit` | SAT | glucose | 3.292 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowTransmit/execution.json) |
| `ShowTwoMessageDelivery` | SAT | glucose | 3.020 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowTwoMessageDelivery/execution.json) |

Incomplete/failed attempts retained for this scope: 9.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-234711-010fee/summary.md)

### Ordered active route: up to 100 points, history 4, message values 4, 5-bit Int

Frozen model SHA-256: `05cb357750fabcac8b6ec7e5d2f8ddbd1d74d6896856162bd48f507b87d2dba9`.

Property coverage is incomplete. Missing validated checks: `DaemonIsInvisible`, `DaemonPreservesInvariant`, `InsertionIsInvisible`, `InsertionPreservesInvariant`, `ReceivePreservesInvariant`, `ReceiveRefinesExternal`, `RetrieveIsValid`, `TransmitPreservesInvariant`, `TransmitRefinesExternal`.

| Command | Validated outcome | Solver | Seconds | Exact active route lengths | Evidence |
|---|---|---|---:|---|---|
| `InitialIsValid` | UNSAT | glucose | 6.509 | not an exact-size witness | [record](../scale-results/scale-20261107-234921-bf180e/points-100/InitialIsValid/execution.json) |
| `ShowFullRouteWithTraffic` | SAT | glucose | 12.999 | [100] | [record](../scale-results/scale-20261107-234921-bf180e/points-100/ShowFullRouteWithTraffic/execution.json) |

Incomplete/failed attempts retained for this scope: 0.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-234921-bf180e/summary.md)

### Ordered active route: up to 1000 points, history 4, message values 4, 5-bit Int

Frozen model SHA-256: `05cb357750fabcac8b6ec7e5d2f8ddbd1d74d6896856162bd48f507b87d2dba9`.

Property coverage is incomplete. Missing validated checks: `DaemonIsInvisible`, `DaemonPreservesInvariant`, `InitialIsValid`, `InsertionIsInvisible`, `InsertionPreservesInvariant`, `ReceivePreservesInvariant`, `ReceiveRefinesExternal`, `RetrieveIsValid`, `TransmitPreservesInvariant`, `TransmitRefinesExternal`.

| Command | Validated outcome | Solver | Seconds | Exact active route lengths | Evidence |
|---|---|---|---:|---|---|

Incomplete/failed attempts retained for this scope: 2.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-234921-bf180e/summary.md)

### Ordered route, position fields (arity 2): up to 10 points, history 4, message values 4, 5-bit Int

Frozen model SHA-256: `1fa2fa4556b3ce3fec9d4286ba6b5d986bd1d2cd51192b381493f363c1b04181`.

All property checks declared for this representation completed with validated UNSAT results.

| Command | Validated outcome | Solver | Seconds | Exact active route lengths | Evidence |
|---|---|---|---:|---|---|
| `BrokenReceiveWouldPreserveInvariant` | SAT | glucose | 3.090 | not an exact-size witness | [record](../scale-results/scale-20261115-021929-92af45/points-10/BrokenReceiveWouldPreserveInvariant/execution.json) |
| `DaemonIsInvisible` | UNSAT | glucose | 136.196 | not an exact-size witness | [record](../scale-results/scale-20261115-023702-02356a/points-10/DaemonIsInvisible/execution.json) |
| `DaemonIsInvisible` | UNSAT | kissat (CNF) + DRAT verified | 686.418 (host asleep 78 s) | not an exact-size witness | [record](../scale-results/scale-20261115-021929-92af45/points-10/DaemonIsInvisible/execution.json) |
| `DaemonPreservesInvariant` | UNSAT | glucose | 79.033 | not an exact-size witness | [record](../scale-results/scale-20261115-023702-02356a/points-10/DaemonPreservesInvariant/execution.json) |
| `DaemonPreservesInvariant` | UNSAT | kissat (CNF) + DRAT verified | 66.007 | not an exact-size witness | [record](../scale-results/scale-20261115-021929-92af45/points-10/DaemonPreservesInvariant/execution.json) |
| `InitialIsValid` | UNSAT | glucose | 1.573 | not an exact-size witness | [record](../scale-results/scale-20261115-023702-02356a/points-10/InitialIsValid/execution.json) |
| `InitialIsValid` | UNSAT | kissat (CNF) + DRAT verified | 23.317 | not an exact-size witness | [record](../scale-results/scale-20261115-021929-92af45/points-10/InitialIsValid/execution.json) |
| `InsertionIsInvisible` | UNSAT | glucose | 18.047 | not an exact-size witness | [record](../scale-results/scale-20261115-023702-02356a/points-10/InsertionIsInvisible/execution.json) |
| `InsertionPreservesInvariant` | UNSAT | glucose | 15.533 | not an exact-size witness | [record](../scale-results/scale-20261115-023702-02356a/points-10/InsertionPreservesInvariant/execution.json) |
| `InsertionPreservesInvariant` | UNSAT | kissat (CNF) + DRAT verified | 46.162 | not an exact-size witness | [record](../scale-results/scale-20261115-021929-92af45/points-10/InsertionPreservesInvariant/execution.json) |
| `ReceivePreservesInvariant` | UNSAT | glucose | 27.028 | not an exact-size witness | [record](../scale-results/scale-20261115-023702-02356a/points-10/ReceivePreservesInvariant/execution.json) |
| `ReceivePreservesInvariant` | UNSAT | kissat (CNF) + DRAT verified | 22.862 | not an exact-size witness | [record](../scale-results/scale-20261115-021929-92af45/points-10/ReceivePreservesInvariant/execution.json) |
| `ReceiveRefinesExternal` | UNSAT | glucose | 76.150 | not an exact-size witness | [record](../scale-results/scale-20261115-023702-02356a/points-10/ReceiveRefinesExternal/execution.json) |
| `ReceiveRefinesExternal` | UNSAT | kissat (CNF) | 353.615 | not an exact-size witness | [record](../scale-results/scale-20261115-045106-4c10ae/points-10/ReceiveRefinesExternal/execution.json) |
| `ReceiveRefinesExternal` | UNSAT | kissat (CNF) + DRAT verified | 561.654 | not an exact-size witness | [record](../scale-results/scale-20261115-021929-92af45/points-10/ReceiveRefinesExternal/execution.json) |
| `RetrieveIsValid` | UNSAT | glucose | 160.153 | not an exact-size witness | [record](../scale-results/scale-20261115-023702-02356a/points-10/RetrieveIsValid/execution.json) |
| `RetrieveIsValid` | UNSAT | kissat (CNF) + DRAT verified | 224.940 | not an exact-size witness | [record](../scale-results/scale-20261115-021929-92af45/points-10/RetrieveIsValid/execution.json) |
| `ShowDaemon` | SAT | glucose | 2.236 | not an exact-size witness | [record](../scale-results/scale-20261115-021929-92af45/points-10/ShowDaemon/execution.json) |
| `ShowFullRouteDaemon` | SAT | glucose | 3.878 | [10, 10] | [record](../scale-results/scale-20261115-021929-92af45/points-10/ShowFullRouteDaemon/execution.json) |
| `ShowFullRouteInsertion` | SAT | glucose | 4.308 | [9, 10] | [record](../scale-results/scale-20261115-021929-92af45/points-10/ShowFullRouteInsertion/execution.json) |
| `ShowFullRoutePendingPoll` | SAT | glucose | 3.733 | [10, 10] | [record](../scale-results/scale-20261115-021929-92af45/points-10/ShowFullRoutePendingPoll/execution.json) |
| `ShowFullRouteReceive` | SAT | glucose | 3.971 | [10, 10] | [record](../scale-results/scale-20261115-021929-92af45/points-10/ShowFullRouteReceive/execution.json) |
| `ShowFullRouteTransmit` | SAT | glucose | 3.528 | [10, 10] | [record](../scale-results/scale-20261115-021929-92af45/points-10/ShowFullRouteTransmit/execution.json) |
| `ShowFullRouteWithTraffic` | SAT | glucose | 2.726 | [10] | [record](../scale-results/scale-20261115-021929-92af45/points-10/ShowFullRouteWithTraffic/execution.json) |
| `ShowInsertionWithTraffic` | SAT | glucose | 2.570 | not an exact-size witness | [record](../scale-results/scale-20261115-021929-92af45/points-10/ShowInsertionWithTraffic/execution.json) |
| `ShowPendingPollCanStutter` | SAT | glucose | 2.262 | not an exact-size witness | [record](../scale-results/scale-20261115-021929-92af45/points-10/ShowPendingPollCanStutter/execution.json) |
| `ShowReceive` | SAT | glucose | 2.241 | not an exact-size witness | [record](../scale-results/scale-20261115-021929-92af45/points-10/ShowReceive/execution.json) |
| `ShowTransmit` | SAT | glucose | 3.053 | not an exact-size witness | [record](../scale-results/scale-20261115-021929-92af45/points-10/ShowTransmit/execution.json) |
| `TransmitPreservesInvariant` | UNSAT | glucose | 16.009 | not an exact-size witness | [record](../scale-results/scale-20261115-023702-02356a/points-10/TransmitPreservesInvariant/execution.json) |
| `TransmitPreservesInvariant` | UNSAT | kissat (CNF) + DRAT verified | 18.494 | not an exact-size witness | [record](../scale-results/scale-20261115-021929-92af45/points-10/TransmitPreservesInvariant/execution.json) |
| `TransmitRefinesExternal` | UNSAT | glucose | 11.391 | not an exact-size witness | [record](../scale-results/scale-20261115-023702-02356a/points-10/TransmitRefinesExternal/execution.json) |
| `TransmitRefinesExternal` | UNSAT | kissat (CNF) + DRAT verified | 33.055 | not an exact-size witness | [record](../scale-results/scale-20261115-021929-92af45/points-10/TransmitRefinesExternal/execution.json) |

Incomplete/failed attempts retained for this scope: 3.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261115-021929-92af45/summary.md)
- [Full suite including unsuccessful attempts](../scale-results/scale-20261115-023702-02356a/summary.md)
- [Full suite including unsuccessful attempts](../scale-results/scale-20261115-024808-729a9d/summary.md)
- [Full suite including unsuccessful attempts](../scale-results/scale-20261115-045106-4c10ae/summary.md)

### Ordered route, position fields (arity 2): up to 20 points, history 4, message values 4, 5-bit Int

Frozen model SHA-256: `1fa2fa4556b3ce3fec9d4286ba6b5d986bd1d2cd51192b381493f363c1b04181`.

Property coverage is incomplete. Missing validated checks: `DaemonIsInvisible`, `DaemonPreservesInvariant`, `InsertionIsInvisible`, `InsertionPreservesInvariant`, `ReceiveRefinesExternal`, `RetrieveIsValid`.

| Command | Validated outcome | Solver | Seconds | Exact active route lengths | Evidence |
|---|---|---|---:|---|---|
| `BrokenReceiveWouldPreserveInvariant` | SAT | glucose | 2.288 | not an exact-size witness | [record](../scale-results/scale-20261115-084147-7d578d/points-20/BrokenReceiveWouldPreserveInvariant/execution.json) |
| `InitialIsValid` | UNSAT | glucose | 4.017 | not an exact-size witness | [record](../scale-results/scale-20261115-045106-54a256/points-20/InitialIsValid/execution.json) |
| `InitialIsValid` | UNSAT | kissat (CNF) + DRAT verified | 7.992 (host asleep 8 s) | not an exact-size witness | [record](../scale-results/scale-20261115-021929-92af45/points-20/InitialIsValid/execution.json) |
| `ReceivePreservesInvariant` | UNSAT | glucose | 190.782 | not an exact-size witness | [record](../scale-results/scale-20261115-084147-7d578d/points-20/ReceivePreservesInvariant/execution.json) |
| `ShowDaemon` | SAT | glucose | 27.717 | not an exact-size witness | [record](../scale-results/scale-20261115-084147-7d578d/points-20/ShowDaemon/execution.json) |
| `ShowFullRouteDaemon` | SAT | glucose | 14.035 | [20, 20] | [record](../scale-results/scale-20261115-084147-7d578d/points-20/ShowFullRouteDaemon/execution.json) |
| `ShowFullRouteInsertion` | SAT | glucose | 13.613 | [19, 20] | [record](../scale-results/scale-20261115-084147-7d578d/points-20/ShowFullRouteInsertion/execution.json) |
| `ShowFullRoutePendingPoll` | SAT | glucose | 5.878 | [20, 20] | [record](../scale-results/scale-20261115-084147-7d578d/points-20/ShowFullRoutePendingPoll/execution.json) |
| `ShowFullRouteReceive` | SAT | glucose | 13.724 | [20, 20] | [record](../scale-results/scale-20261115-084147-7d578d/points-20/ShowFullRouteReceive/execution.json) |
| `ShowFullRouteTransmit` | SAT | glucose | 2.256 | [20, 20] | [record](../scale-results/scale-20261115-084147-7d578d/points-20/ShowFullRouteTransmit/execution.json) |
| `ShowFullRouteWithTraffic` | SAT | glucose | 1.839 | [20] | [record](../scale-results/scale-20261115-084147-7d578d/points-20/ShowFullRouteWithTraffic/execution.json) |
| `ShowInsertionWithTraffic` | SAT | glucose | 26.474 | not an exact-size witness | [record](../scale-results/scale-20261115-084147-7d578d/points-20/ShowInsertionWithTraffic/execution.json) |
| `ShowPendingPollCanStutter` | SAT | glucose | 29.983 | not an exact-size witness | [record](../scale-results/scale-20261115-084147-7d578d/points-20/ShowPendingPollCanStutter/execution.json) |
| `ShowReceive` | SAT | glucose | 2.297 | not an exact-size witness | [record](../scale-results/scale-20261115-084147-7d578d/points-20/ShowReceive/execution.json) |
| `ShowTransmit` | SAT | glucose | 2.223 | not an exact-size witness | [record](../scale-results/scale-20261115-084147-7d578d/points-20/ShowTransmit/execution.json) |
| `TransmitPreservesInvariant` | UNSAT | glucose | 59.174 | not an exact-size witness | [record](../scale-results/scale-20261115-084147-7d578d/points-20/TransmitPreservesInvariant/execution.json) |
| `TransmitRefinesExternal` | UNSAT | glucose | 96.917 | not an exact-size witness | [record](../scale-results/scale-20261115-084147-7d578d/points-20/TransmitRefinesExternal/execution.json) |

Incomplete/failed attempts retained for this scope: 10.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261115-021929-92af45/summary.md)
- [Full suite including unsuccessful attempts](../scale-results/scale-20261115-024808-d1ef69/summary.md)
- [Full suite including unsuccessful attempts](../scale-results/scale-20261115-045106-54a256/summary.md)
- [Full suite including unsuccessful attempts](../scale-results/scale-20261115-084147-7d578d/summary.md)

### Ordered route, position fields (arity 2): up to 100 points, history 4, message values 4, 5-bit Int

Frozen model SHA-256: `1fa2fa4556b3ce3fec9d4286ba6b5d986bd1d2cd51192b381493f363c1b04181`.

Property coverage is incomplete. Missing validated checks: `DaemonIsInvisible`, `DaemonPreservesInvariant`, `InsertionIsInvisible`, `InsertionPreservesInvariant`, `ReceivePreservesInvariant`, `ReceiveRefinesExternal`, `RetrieveIsValid`, `TransmitPreservesInvariant`, `TransmitRefinesExternal`.

| Command | Validated outcome | Solver | Seconds | Exact active route lengths | Evidence |
|---|---|---|---:|---|---|
| `BrokenReceiveWouldPreserveInvariant` | SAT | glucose | 32.825 | not an exact-size witness | [record](../scale-results/scale-20261115-084147-c91be1/points-100/BrokenReceiveWouldPreserveInvariant/execution.json) |
| `InitialIsValid` | UNSAT | glucose | 10.410 | not an exact-size witness | [record](../scale-results/scale-20261115-084147-c91be1/points-100/InitialIsValid/execution.json) |
| `ShowDaemon` | SAT | glucose | 11.398 | not an exact-size witness | [record](../scale-results/scale-20261115-084147-c91be1/points-100/ShowDaemon/execution.json) |
| `ShowFullRouteDaemon` | SAT | glucose | 10.319 | [100, 100] | [record](../scale-results/scale-20261115-084147-c91be1/points-100/ShowFullRouteDaemon/execution.json) |
| `ShowFullRouteInsertion` | SAT | glucose | 10.082 | [99, 100] | [record](../scale-results/scale-20261115-084147-c91be1/points-100/ShowFullRouteInsertion/execution.json) |
| `ShowFullRoutePendingPoll` | SAT | glucose | 8.686 | [100, 100] | [record](../scale-results/scale-20261115-084147-c91be1/points-100/ShowFullRoutePendingPoll/execution.json) |
| `ShowFullRouteReceive` | SAT | glucose | 10.393 | [100, 100] | [record](../scale-results/scale-20261115-084147-c91be1/points-100/ShowFullRouteReceive/execution.json) |
| `ShowFullRouteTransmit` | SAT | glucose | 9.706 | [100, 100] | [record](../scale-results/scale-20261115-084147-c91be1/points-100/ShowFullRouteTransmit/execution.json) |
| `ShowFullRouteWithTraffic` | SAT | glucose | 11.388 | [100] | [record](../scale-results/scale-20261115-084147-c91be1/points-100/ShowFullRouteWithTraffic/execution.json) |
| `ShowInsertionWithTraffic` | SAT | glucose | 13.928 | not an exact-size witness | [record](../scale-results/scale-20261115-084147-c91be1/points-100/ShowInsertionWithTraffic/execution.json) |
| `ShowPendingPollCanStutter` | SAT | glucose | 13.482 | not an exact-size witness | [record](../scale-results/scale-20261115-084147-c91be1/points-100/ShowPendingPollCanStutter/execution.json) |
| `ShowReceive` | SAT | glucose | 20.861 | not an exact-size witness | [record](../scale-results/scale-20261115-084147-c91be1/points-100/ShowReceive/execution.json) |
| `ShowTransmit` | SAT | glucose | 31.762 | not an exact-size witness | [record](../scale-results/scale-20261115-084147-c91be1/points-100/ShowTransmit/execution.json) |

Incomplete/failed attempts retained for this scope: 9.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261115-084147-c91be1/summary.md)

## Earlier development attempts

These sources differ from the current model and are excluded from coverage above.

- [scale-20261107-234635-aa4735](../scale-results/scale-20261107-234635-aa4735/summary.md)
