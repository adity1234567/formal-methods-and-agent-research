# Bounded correspondence between protocol representations

Run: `correspondence-large-20261107-235506-d49938`. Status: `completed`.
All selected expectations and evidence validated: **no**.

Harness: `scaling_large_correspondence.als`.

These checks compare paired states under a point/message bijection and an explicit route-order relation. They do not assume either post-state invariant. SAT witnesses exercise paired operations.

Scope: three available points in each representation, up to three message values, four-entry histories, six-bit integers, and exactly two states per representation in each command.

This is bounded conditional representation correspondence. It does not establish arbitrary-size equivalence or full enabledness equivalence for a fixed ordered pool. The original insertion may choose a fresh point whose fixed pool position is incompatible with the requested gap.

Timeout per command: 60.0 seconds. JVM heap cap: 2048 MiB. Heap cap is not measured peak process memory.

| Command and evidence | Expected | Observed | Status | Seconds | Interpretation |
|---|---|---|---|---:|---|
| [SectionInvariantsCorrespond](SectionInvariantsCorrespond/execution.json) | UNSAT | UNSAT | completed | 6.947 | Matched |
| [InitialStatesCorrespond](InitialStatesCorrespond/execution.json) | UNSAT | UNSAT | completed | 2.499 | Matched |
| [RetrieveObservationsCorrespond](RetrieveObservationsCorrespond/execution.json) | UNSAT | UNSAT | completed | 5.983 | Matched |
| [TransmitEffectsCorrespond](TransmitEffectsCorrespond/execution.json) | UNSAT | UNSAT | completed | 2.923 | Matched |
| [ReceiveEffectsCorrespond](ReceiveEffectsCorrespond/execution.json) | UNSAT | UNSAT | completed | 3.708 | Matched |
| [DaemonEffectsCorrespond](DaemonEffectsCorrespond/execution.json) | UNSAT | UNKNOWN | timed_out | 60.142 | Incomplete or failed |
| [InsertionEffectsCorrespond](InsertionEffectsCorrespond/execution.json) | UNSAT | UNSAT | completed | 44.481 | Matched |
| [ShowCorrespondingTransmit](ShowCorrespondingTransmit/execution.json) | SAT | SAT | completed | 14.149 | Matched |
| [ShowCorrespondingInsertion](ShowCorrespondingInsertion/execution.json) | SAT | SAT | completed | 4.744 | Matched |
| [ShowCorrespondingReceive](ShowCorrespondingReceive/execution.json) | SAT | SAT | completed | 2.667 | Matched |
| [ShowCorrespondingDaemon](ShowCorrespondingDaemon/execution.json) | SAT | SAT | completed | 3.024 | Matched |

## Frozen sources

- [scaling_large_correspondence.als](sources/scaling_large_correspondence.als), SHA-256 `003230af788b7016363aef4c7d7c7f2233b917dabba1f5a5ce72e79a9088208a`
- [telecommunications.als](sources/telecommunications.als), SHA-256 `47d76e1f6c80954afd8b2ea0607486f4a410a80298a5d7bfd98573c4ade47621`
- [telecommunications_large.als](sources/telecommunications_large.als), SHA-256 `1395072cf94608a7d202ced6a66dfec9bdcda9f3a3ac2c857a477d8917f3169b`

## Evidence issues

- `DaemonEffectsCorrespond`: Execution not completed successfully: timed_out
