# Larger-network verification results

Report generated: 2026-11-08T00:17:28+06:00 (Asia/Dhaka).

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

## What changed

The ordered models decouple route size from message-history length and compute pending sequence offsets from arrival-history lengths. The two-slot model reduces stored history relations from arity four to arity three. The fixed-route specialization uses direct neighbours on a full ordered route and deliberately omits insertion.

Ordered-pool models restrict a particular fresh point to its fixed position when inserting. Their safety correspondence uses compatible point renaming and does not establish every original insertion enabledness obligation. The two-slot models check states and individual transitions, not the three/seven-snapshot demonstrations. See [the design and mathematical argument](../scaling_design.md).

The earlier 1,000-point ordered model with four-column history fields hit Alloy's translation capacity before solving. Lower-arity variants address that representation limit, but remain subject to solver time and memory costs. Timeouts and translation/resource failures do not provide counterexamples.

## Bounded correspondence

The correspondence harnesses compare paired representations at three points, four-entry histories and six-bit integers. They compare validity, initialisation, retrieval and operation effects without assuming either post-state invariant. Their results are bounded evidence, not an unbounded equivalence theorem.

Coverage below combines matching-source retries; unsuccessful attempts remain linked.

| Harness | UNSAT comparison checks | SAT paired-operation witnesses |
|---|---:|---:|
| [scaling_correspondence.als](../scaling_correspondence.als) | 7/7 | 4/4 |
| [scaling_large_correspondence.als](../scaling_large_correspondence.als) | 7/7 | 4/4 |

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

All correspondence attempts:

- [correspondence-20261107-234959-f1e1a2](../scale-results/correspondence-20261107-234959-f1e1a2/summary.md): completed; all selected expectations validated: yes.
- [correspondence-large-20261107-235433-2b0d8f](../scale-results/correspondence-large-20261107-235433-2b0d8f/summary.md): failed_before_execution; all selected expectations validated: no.
- [correspondence-large-20261107-235506-d49938](../scale-results/correspondence-large-20261107-235506-d49938/summary.md): completed; all selected expectations validated: no.
- [correspondence-large-20261107-235757-f8d64c](../scale-results/correspondence-large-20261107-235757-f8d64c/summary.md): completed; all selected expectations validated: yes.

## Resource and interpretation limits

Commands have independent wall-clock deadlines. The recorded JVM heap cap is not a measurement of peak process memory, and native solver allocations are additional. Some experiments ran concurrently on the same machine, so elapsed times are execution records rather than a controlled performance comparison. Baseline and optimized runs also use different history bounds in several cases.

No completed finite scope proves eventual delivery, fairness, arbitrary network size, or complete SS7 conformance. Optional polling and idle steps still permit indefinite waiting.

## Detailed validated evidence

### Original sequence route: up to 6 points, history 6, message values 4, 7-bit Int

Frozen model SHA-256: `47d76e1f6c80954afd8b2ea0607486f4a410a80298a5d7bfd98573c4ade47621`.

Property coverage is incomplete. Missing validated checks: `DaemonIsInvisible`, `DaemonPreservesInvariant`, `InitialIsValid`, `InsertionIsInvisible`, `InsertionPreservesInvariant`, `ReceivePreservesInvariant`, `ReceiveRefinesExternal`, `RetrieveIsValid`, `TransmitPreservesInvariant`, `TransmitRefinesExternal`.

| Command | Validated outcome | Seconds | Exact active route lengths | Evidence |
|---|---|---:|---|---|
| `ShowExactRouteWithTraffic` | SAT | 2.375 | [6] | [record](../scale-results/scale-20261107-234635-73369e/points-6/ShowExactRouteWithTraffic/execution.json) |

Incomplete/failed attempts retained for this scope: 2.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-234635-73369e/summary.md)

### Fixed full route, two slots: exactly 100 points, history 2, message values 4, 5-bit Int

Frozen model SHA-256: `182c9179911ef07a62dc50d4592494e4adbbd7a35db9d146633de7c526df47c3`.

Property coverage is incomplete. Missing validated checks: `DaemonIsInvisible`, `DaemonPreservesInvariant`, `ReceivePreservesInvariant`, `RetrieveIsValid`.

| Command | Validated outcome | Seconds | Exact active route lengths | Evidence |
|---|---|---:|---|---|
| `BrokenReceiveWouldPreserveInvariant` | SAT | 22.050 | not an exact-size witness | [record](../scale-results/scale-20261108-000209-396a0b/points-100/BrokenReceiveWouldPreserveInvariant/execution.json) |
| `InitialIsValid` | UNSAT | 4.091 | not an exact-size witness | [record](../scale-results/scale-20261108-000209-396a0b/points-100/InitialIsValid/execution.json) |
| `ReceiveRefinesExternal` | UNSAT | 18.097 | not an exact-size witness | [record](../scale-results/scale-20261108-000209-396a0b/points-100/ReceiveRefinesExternal/execution.json) |
| `ShowDaemon` | SAT | 2.179 | not an exact-size witness | [record](../scale-results/scale-20261108-000209-396a0b/points-100/ShowDaemon/execution.json) |
| `ShowFullRouteDaemon` | SAT | 2.622 | [100, 100] | [record](../scale-results/scale-20261108-000209-396a0b/points-100/ShowFullRouteDaemon/execution.json) |
| `ShowFullRoutePendingPoll` | SAT | 2.615 | [100, 100] | [record](../scale-results/scale-20261108-000209-396a0b/points-100/ShowFullRoutePendingPoll/execution.json) |
| `ShowFullRouteReceive` | SAT | 2.654 | [100, 100] | [record](../scale-results/scale-20261108-000209-396a0b/points-100/ShowFullRouteReceive/execution.json) |
| `ShowFullRouteTransmit` | SAT | 2.533 | [100, 100] | [record](../scale-results/scale-20261108-000209-396a0b/points-100/ShowFullRouteTransmit/execution.json) |
| `ShowFullRouteWithTraffic` | SAT | 2.107 | [100] | [record](../scale-results/scale-20261108-000209-396a0b/points-100/ShowFullRouteWithTraffic/execution.json) |
| `ShowPendingPollCanStutter` | SAT | 2.510 | not an exact-size witness | [record](../scale-results/scale-20261108-000209-396a0b/points-100/ShowPendingPollCanStutter/execution.json) |
| `ShowReceive` | SAT | 2.119 | not an exact-size witness | [record](../scale-results/scale-20261108-000209-396a0b/points-100/ShowReceive/execution.json) |
| `ShowTransmit` | SAT | 1.903 | not an exact-size witness | [record](../scale-results/scale-20261108-000209-396a0b/points-100/ShowTransmit/execution.json) |
| `TransmitPreservesInvariant` | UNSAT | 33.914 | not an exact-size witness | [record](../scale-results/scale-20261108-000209-396a0b/points-100/TransmitPreservesInvariant/execution.json) |
| `TransmitRefinesExternal` | UNSAT | 8.410 | not an exact-size witness | [record](../scale-results/scale-20261108-000209-396a0b/points-100/TransmitRefinesExternal/execution.json) |

Incomplete/failed attempts retained for this scope: 4.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261108-000209-396a0b/summary.md)

### Fixed full route, two slots: exactly 1000 points, history 1, message values 1, 5-bit Int

Frozen model SHA-256: `182c9179911ef07a62dc50d4592494e4adbbd7a35db9d146633de7c526df47c3`.

Property coverage is incomplete. Missing validated checks: `DaemonIsInvisible`, `DaemonPreservesInvariant`, `ReceivePreservesInvariant`, `ReceiveRefinesExternal`, `RetrieveIsValid`, `TransmitPreservesInvariant`, `TransmitRefinesExternal`.

| Command | Validated outcome | Seconds | Exact active route lengths | Evidence |
|---|---|---:|---|---|
| `InitialIsValid` | UNSAT | 42.337 | not an exact-size witness | [record](../scale-results/scale-20261108-000439-d89215/points-1000/InitialIsValid/execution.json) |
| `ShowFullRouteTransmit` | SAT | 44.363 | [1000, 1000] | [record](../scale-results/scale-20261108-000815-2b6381/points-1000/ShowFullRouteTransmit/execution.json) |
| `ShowFullRouteWithTraffic` | SAT | 59.052 | [1000] | [record](../scale-results/scale-20261108-000439-d89215/points-1000/ShowFullRouteWithTraffic/execution.json) |

Incomplete/failed attempts retained for this scope: 1.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261108-000439-d89215/summary.md)
- [Full suite including unsuccessful attempts](../scale-results/scale-20261108-000815-2b6381/summary.md)

### Fixed full route, two slots: exactly 1000 points, history 4, message values 4, 5-bit Int

Frozen model SHA-256: `182c9179911ef07a62dc50d4592494e4adbbd7a35db9d146633de7c526df47c3`.

Property coverage is incomplete. Missing validated checks: `DaemonIsInvisible`, `DaemonPreservesInvariant`, `InitialIsValid`, `ReceivePreservesInvariant`, `ReceiveRefinesExternal`, `RetrieveIsValid`, `TransmitPreservesInvariant`, `TransmitRefinesExternal`.

| Command | Validated outcome | Seconds | Exact active route lengths | Evidence |
|---|---|---:|---|---|

Incomplete/failed attempts retained for this scope: 2.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261108-000001-afc7d1/summary.md)

### Ordered route, two slots: up to 10 points, history 2, message values 4, 5-bit Int

Frozen model SHA-256: `1395072cf94608a7d202ced6a66dfec9bdcda9f3a3ac2c857a477d8917f3169b`.

All property checks declared for this representation completed with validated UNSAT results.

| Command | Validated outcome | Seconds | Exact active route lengths | Evidence |
|---|---|---:|---|---|
| `BrokenReceiveWouldPreserveInvariant` | SAT | 1.788 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/BrokenReceiveWouldPreserveInvariant/execution.json) |
| `DaemonIsInvisible` | UNSAT | 34.158 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/DaemonIsInvisible/execution.json) |
| `DaemonPreservesInvariant` | UNSAT | 31.469 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/DaemonPreservesInvariant/execution.json) |
| `InitialIsValid` | UNSAT | 1.127 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/InitialIsValid/execution.json) |
| `InsertionIsInvisible` | UNSAT | 7.437 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/InsertionIsInvisible/execution.json) |
| `InsertionPreservesInvariant` | UNSAT | 23.312 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/InsertionPreservesInvariant/execution.json) |
| `ReceivePreservesInvariant` | UNSAT | 20.719 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ReceivePreservesInvariant/execution.json) |
| `ReceiveRefinesExternal` | UNSAT | 14.236 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ReceiveRefinesExternal/execution.json) |
| `RetrieveIsValid` | UNSAT | 20.793 | not an exact-size witness | [record](../scale-results/scale-20261108-000209-aed205/points-10/RetrieveIsValid/execution.json) |
| `ShowDaemon` | SAT | 1.485 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowDaemon/execution.json) |
| `ShowFullRouteDaemon` | SAT | 2.148 | [10, 10] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowFullRouteDaemon/execution.json) |
| `ShowFullRouteInsertion` | SAT | 1.425 | [9, 10] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowFullRouteInsertion/execution.json) |
| `ShowFullRoutePendingPoll` | SAT | 2.085 | [10, 10] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowFullRoutePendingPoll/execution.json) |
| `ShowFullRouteReceive` | SAT | 1.649 | [10, 10] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowFullRouteReceive/execution.json) |
| `ShowFullRouteTransmit` | SAT | 1.892 | [10, 10] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowFullRouteTransmit/execution.json) |
| `ShowFullRouteWithTraffic` | SAT | 1.573 | [10] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowFullRouteWithTraffic/execution.json) |
| `ShowInsertionWithTraffic` | SAT | 1.620 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowInsertionWithTraffic/execution.json) |
| `ShowPendingPollCanStutter` | SAT | 1.574 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowPendingPollCanStutter/execution.json) |
| `ShowReceive` | SAT | 1.503 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowReceive/execution.json) |
| `ShowTransmit` | SAT | 1.434 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/ShowTransmit/execution.json) |
| `TransmitPreservesInvariant` | UNSAT | 13.100 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/TransmitPreservesInvariant/execution.json) |
| `TransmitRefinesExternal` | UNSAT | 1.894 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-10/TransmitRefinesExternal/execution.json) |

Incomplete/failed attempts retained for this scope: 1.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-235628-5c0dd7/summary.md)
- [Full suite including unsuccessful attempts](../scale-results/scale-20261108-000209-aed205/summary.md)

### Ordered route, two slots: up to 20 points, history 2, message values 4, 5-bit Int

Frozen model SHA-256: `1395072cf94608a7d202ced6a66dfec9bdcda9f3a3ac2c857a477d8917f3169b`.

Property coverage is incomplete. Missing validated checks: `DaemonIsInvisible`, `DaemonPreservesInvariant`, `InsertionIsInvisible`, `InsertionPreservesInvariant`, `ReceivePreservesInvariant`, `ReceiveRefinesExternal`, `RetrieveIsValid`.

| Command | Validated outcome | Seconds | Exact active route lengths | Evidence |
|---|---|---:|---|---|
| `BrokenReceiveWouldPreserveInvariant` | SAT | 1.813 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/BrokenReceiveWouldPreserveInvariant/execution.json) |
| `InitialIsValid` | UNSAT | 8.184 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/InitialIsValid/execution.json) |
| `ShowDaemon` | SAT | 1.391 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowDaemon/execution.json) |
| `ShowFullRouteDaemon` | SAT | 1.471 | [20, 20] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowFullRouteDaemon/execution.json) |
| `ShowFullRouteInsertion` | SAT | 1.453 | [19, 20] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowFullRouteInsertion/execution.json) |
| `ShowFullRoutePendingPoll` | SAT | 1.707 | [20, 20] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowFullRoutePendingPoll/execution.json) |
| `ShowFullRouteReceive` | SAT | 1.407 | [20, 20] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowFullRouteReceive/execution.json) |
| `ShowFullRouteTransmit` | SAT | 1.401 | [20, 20] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowFullRouteTransmit/execution.json) |
| `ShowFullRouteWithTraffic` | SAT | 1.665 | [20] | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowFullRouteWithTraffic/execution.json) |
| `ShowInsertionWithTraffic` | SAT | 1.599 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowInsertionWithTraffic/execution.json) |
| `ShowPendingPollCanStutter` | SAT | 1.467 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowPendingPollCanStutter/execution.json) |
| `ShowReceive` | SAT | 1.489 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowReceive/execution.json) |
| `ShowTransmit` | SAT | 1.736 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/ShowTransmit/execution.json) |
| `TransmitPreservesInvariant` | UNSAT | 30.561 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/TransmitPreservesInvariant/execution.json) |
| `TransmitRefinesExternal` | UNSAT | 5.957 | not an exact-size witness | [record](../scale-results/scale-20261107-235628-5c0dd7/points-20/TransmitRefinesExternal/execution.json) |

Incomplete/failed attempts retained for this scope: 7.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-235628-5c0dd7/summary.md)

### Ordered route, two slots: up to 1000 points, history 4, message values 4, 5-bit Int

Frozen model SHA-256: `1395072cf94608a7d202ced6a66dfec9bdcda9f3a3ac2c857a477d8917f3169b`.

Property coverage is incomplete. Missing validated checks: `DaemonIsInvisible`, `DaemonPreservesInvariant`, `InitialIsValid`, `InsertionIsInvisible`, `InsertionPreservesInvariant`, `ReceivePreservesInvariant`, `ReceiveRefinesExternal`, `RetrieveIsValid`, `TransmitPreservesInvariant`, `TransmitRefinesExternal`.

| Command | Validated outcome | Seconds | Exact active route lengths | Evidence |
|---|---|---:|---|---|

Incomplete/failed attempts retained for this scope: 2.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-235427-e46017/summary.md)

### Ordered active route: up to 6 points, history 4, message values 4, 5-bit Int

Frozen model SHA-256: `05cb357750fabcac8b6ec7e5d2f8ddbd1d74d6896856162bd48f507b87d2dba9`.

All property checks declared for this representation completed with validated UNSAT results.

| Command | Validated outcome | Seconds | Exact active route lengths | Evidence |
|---|---|---:|---|---|
| `BrokenReceiveWouldPreserveInvariant` | SAT | 1.554 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/BrokenReceiveWouldPreserveInvariant/execution.json) |
| `DaemonIsInvisible` | UNSAT | 35.030 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/DaemonIsInvisible/execution.json) |
| `DaemonPreservesInvariant` | UNSAT | 26.902 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/DaemonPreservesInvariant/execution.json) |
| `InitialIsValid` | UNSAT | 1.222 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/InitialIsValid/execution.json) |
| `InsertionIsInvisible` | UNSAT | 15.001 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/InsertionIsInvisible/execution.json) |
| `InsertionPreservesInvariant` | UNSAT | 12.491 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/InsertionPreservesInvariant/execution.json) |
| `ReceivePreservesInvariant` | UNSAT | 15.483 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/ReceivePreservesInvariant/execution.json) |
| `ReceiveRefinesExternal` | UNSAT | 13.448 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/ReceiveRefinesExternal/execution.json) |
| `RetrieveIsValid` | UNSAT | 11.640 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/RetrieveIsValid/execution.json) |
| `ShowDaemon` | SAT | 2.078 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowDaemon/execution.json) |
| `ShowFullRouteDaemon` | SAT | 2.647 | [6, 6] | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowFullRouteDaemon/execution.json) |
| `ShowFullRouteInsertion` | SAT | 1.746 | [6, 5] | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowFullRouteInsertion/execution.json) |
| `ShowFullRoutePendingPoll` | SAT | 2.331 | [6, 6] | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowFullRoutePendingPoll/execution.json) |
| `ShowFullRouteReceive` | SAT | 1.939 | [6, 6] | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowFullRouteReceive/execution.json) |
| `ShowFullRouteTransmit` | SAT | 1.437 | [6, 6] | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowFullRouteTransmit/execution.json) |
| `ShowFullRouteWithTraffic` | SAT | 1.531 | [6] | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowFullRouteWithTraffic/execution.json) |
| `ShowInsertionWithTraffic` | SAT | 1.720 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowInsertionWithTraffic/execution.json) |
| `ShowPendingPollCanStutter` | SAT | 1.815 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowPendingPollCanStutter/execution.json) |
| `ShowReceive` | SAT | 2.048 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowReceive/execution.json) |
| `ShowRepeatedMessageValue` | SAT | 1.446 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowRepeatedMessageValue/execution.json) |
| `ShowTransmit` | SAT | 1.542 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowTransmit/execution.json) |
| `ShowTwoMessageDelivery` | SAT | 2.380 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/ShowTwoMessageDelivery/execution.json) |
| `TransmitPreservesInvariant` | UNSAT | 7.373 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/TransmitPreservesInvariant/execution.json) |
| `TransmitRefinesExternal` | UNSAT | 5.242 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-6/TransmitRefinesExternal/execution.json) |

Incomplete/failed attempts retained for this scope: 0.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-234711-010fee/summary.md)

### Ordered active route: up to 8 points, history 4, message values 4, 5-bit Int

Frozen model SHA-256: `05cb357750fabcac8b6ec7e5d2f8ddbd1d74d6896856162bd48f507b87d2dba9`.

All property checks declared for this representation completed with validated UNSAT results.

| Command | Validated outcome | Seconds | Exact active route lengths | Evidence |
|---|---|---:|---|---|
| `BrokenReceiveWouldPreserveInvariant` | SAT | 2.064 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/BrokenReceiveWouldPreserveInvariant/execution.json) |
| `DaemonIsInvisible` | UNSAT | 214.057 | not an exact-size witness | [record](../scale-results/scale-20261108-000508-0b544b/points-8/DaemonIsInvisible/execution.json) |
| `DaemonPreservesInvariant` | UNSAT | 133.894 | not an exact-size witness | [record](../scale-results/scale-20261107-235347-e17c94/points-8/DaemonPreservesInvariant/execution.json) |
| `InitialIsValid` | UNSAT | 2.048 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/InitialIsValid/execution.json) |
| `InsertionIsInvisible` | UNSAT | 94.232 | not an exact-size witness | [record](../scale-results/scale-20261107-235942-c5fbcf/points-8/InsertionIsInvisible/execution.json) |
| `InsertionPreservesInvariant` | UNSAT | 40.590 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/InsertionPreservesInvariant/execution.json) |
| `ReceivePreservesInvariant` | UNSAT | 38.962 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/ReceivePreservesInvariant/execution.json) |
| `ReceiveRefinesExternal` | UNSAT | 89.359 | not an exact-size witness | [record](../scale-results/scale-20261107-235942-c5fbcf/points-8/ReceiveRefinesExternal/execution.json) |
| `RetrieveIsValid` | UNSAT | 24.324 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/RetrieveIsValid/execution.json) |
| `ShowDaemon` | SAT | 2.087 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowDaemon/execution.json) |
| `ShowFullRouteDaemon` | SAT | 2.421 | [8, 8] | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowFullRouteDaemon/execution.json) |
| `ShowFullRouteInsertion` | SAT | 2.431 | [7, 8] | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowFullRouteInsertion/execution.json) |
| `ShowFullRoutePendingPoll` | SAT | 2.313 | [8, 8] | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowFullRoutePendingPoll/execution.json) |
| `ShowFullRouteReceive` | SAT | 2.984 | [8, 8] | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowFullRouteReceive/execution.json) |
| `ShowFullRouteTransmit` | SAT | 2.576 | [8, 8] | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowFullRouteTransmit/execution.json) |
| `ShowFullRouteWithTraffic` | SAT | 1.894 | [8] | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowFullRouteWithTraffic/execution.json) |
| `ShowInsertionWithTraffic` | SAT | 2.276 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowInsertionWithTraffic/execution.json) |
| `ShowPendingPollCanStutter` | SAT | 2.345 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowPendingPollCanStutter/execution.json) |
| `ShowReceive` | SAT | 2.142 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowReceive/execution.json) |
| `ShowRepeatedMessageValue` | SAT | 1.941 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowRepeatedMessageValue/execution.json) |
| `ShowTransmit` | SAT | 1.917 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowTransmit/execution.json) |
| `ShowTwoMessageDelivery` | SAT | 2.624 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/ShowTwoMessageDelivery/execution.json) |
| `TransmitPreservesInvariant` | UNSAT | 16.877 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/TransmitPreservesInvariant/execution.json) |
| `TransmitRefinesExternal` | UNSAT | 21.405 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-8/TransmitRefinesExternal/execution.json) |

Incomplete/failed attempts retained for this scope: 5.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-234711-010fee/summary.md)
- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-235347-e17c94/summary.md)
- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-235942-c5fbcf/summary.md)
- [Full suite including unsuccessful attempts](../scale-results/scale-20261108-000508-0b544b/summary.md)

### Ordered active route: up to 10 points, history 4, message values 4, 5-bit Int

Frozen model SHA-256: `05cb357750fabcac8b6ec7e5d2f8ddbd1d74d6896856162bd48f507b87d2dba9`.

Property coverage is incomplete. Missing validated checks: `DaemonIsInvisible`, `DaemonPreservesInvariant`, `InsertionIsInvisible`, `InsertionPreservesInvariant`, `ReceivePreservesInvariant`, `ReceiveRefinesExternal`, `RetrieveIsValid`, `TransmitPreservesInvariant`, `TransmitRefinesExternal`.

| Command | Validated outcome | Seconds | Exact active route lengths | Evidence |
|---|---|---:|---|---|
| `BrokenReceiveWouldPreserveInvariant` | SAT | 3.948 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-10/BrokenReceiveWouldPreserveInvariant/execution.json) |
| `InitialIsValid` | UNSAT | 1.755 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-10/InitialIsValid/execution.json) |
| `ShowDaemon` | SAT | 2.453 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowDaemon/execution.json) |
| `ShowFullRouteDaemon` | SAT | 2.411 | [10, 10] | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowFullRouteDaemon/execution.json) |
| `ShowFullRouteInsertion` | SAT | 2.441 | [10, 9] | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowFullRouteInsertion/execution.json) |
| `ShowFullRoutePendingPoll` | SAT | 3.483 | [10, 10] | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowFullRoutePendingPoll/execution.json) |
| `ShowFullRouteReceive` | SAT | 2.454 | [10, 10] | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowFullRouteReceive/execution.json) |
| `ShowFullRouteTransmit` | SAT | 2.250 | [10, 10] | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowFullRouteTransmit/execution.json) |
| `ShowFullRouteWithTraffic` | SAT | 2.180 | [10] | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowFullRouteWithTraffic/execution.json) |
| `ShowInsertionWithTraffic` | SAT | 2.485 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowInsertionWithTraffic/execution.json) |
| `ShowPendingPollCanStutter` | SAT | 2.403 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowPendingPollCanStutter/execution.json) |
| `ShowReceive` | SAT | 2.526 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowReceive/execution.json) |
| `ShowRepeatedMessageValue` | SAT | 2.028 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowRepeatedMessageValue/execution.json) |
| `ShowTransmit` | SAT | 3.292 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowTransmit/execution.json) |
| `ShowTwoMessageDelivery` | SAT | 3.020 | not an exact-size witness | [record](../scale-results/scale-20261107-234711-010fee/points-10/ShowTwoMessageDelivery/execution.json) |

Incomplete/failed attempts retained for this scope: 9.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-234711-010fee/summary.md)

### Ordered active route: up to 100 points, history 4, message values 4, 5-bit Int

Frozen model SHA-256: `05cb357750fabcac8b6ec7e5d2f8ddbd1d74d6896856162bd48f507b87d2dba9`.

Property coverage is incomplete. Missing validated checks: `DaemonIsInvisible`, `DaemonPreservesInvariant`, `InsertionIsInvisible`, `InsertionPreservesInvariant`, `ReceivePreservesInvariant`, `ReceiveRefinesExternal`, `RetrieveIsValid`, `TransmitPreservesInvariant`, `TransmitRefinesExternal`.

| Command | Validated outcome | Seconds | Exact active route lengths | Evidence |
|---|---|---:|---|---|
| `InitialIsValid` | UNSAT | 6.509 | not an exact-size witness | [record](../scale-results/scale-20261107-234921-bf180e/points-100/InitialIsValid/execution.json) |
| `ShowFullRouteWithTraffic` | SAT | 12.999 | [100] | [record](../scale-results/scale-20261107-234921-bf180e/points-100/ShowFullRouteWithTraffic/execution.json) |

Incomplete/failed attempts retained for this scope: 0.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-234921-bf180e/summary.md)

### Ordered active route: up to 1000 points, history 4, message values 4, 5-bit Int

Frozen model SHA-256: `05cb357750fabcac8b6ec7e5d2f8ddbd1d74d6896856162bd48f507b87d2dba9`.

Property coverage is incomplete. Missing validated checks: `DaemonIsInvisible`, `DaemonPreservesInvariant`, `InitialIsValid`, `InsertionIsInvisible`, `InsertionPreservesInvariant`, `ReceivePreservesInvariant`, `ReceiveRefinesExternal`, `RetrieveIsValid`, `TransmitPreservesInvariant`, `TransmitRefinesExternal`.

| Command | Validated outcome | Seconds | Exact active route lengths | Evidence |
|---|---|---:|---|---|

Incomplete/failed attempts retained for this scope: 2.

- [Full suite including unsuccessful attempts](../scale-results/scale-20261107-234921-bf180e/summary.md)

## Earlier development attempts

These sources differ from the current model and are excluded from coverage above.

- [scale-20261107-234635-aa4735](../scale-results/scale-20261107-234635-aa4735/summary.md)
