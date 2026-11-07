# Bounded correspondence between protocol representations

Run: `correspondence-20261107-234959-f1e1a2`. Status: `completed`.
All selected expectations and evidence validated: **yes**.

Harness: `scaling_correspondence.als`.

These checks compare paired states under a point/message bijection and an explicit route-order relation. They do not assume either post-state invariant. SAT witnesses exercise paired operations.

Scope: three available points in each representation, up to three message values, four-entry histories, six-bit integers, and one or two states per representation as declared in each command.

This is bounded conditional representation correspondence. It does not establish arbitrary-size equivalence or full enabledness equivalence for a fixed ordered pool. The original insertion may choose a fresh point whose fixed pool position is incompatible with the requested gap.

Timeout per command: 60.0 seconds. JVM heap cap: 2048 MiB. Heap cap is not measured peak process memory.

| Command and evidence | Expected | Observed | Status | Seconds | Interpretation |
|---|---|---|---|---:|---|
| [SectionInvariantsCorrespond](SectionInvariantsCorrespond/execution.json) | UNSAT | UNSAT | completed | 5.731 | Matched |
| [InitialStatesCorrespond](InitialStatesCorrespond/execution.json) | UNSAT | UNSAT | completed | 2.519 | Matched |
| [RetrieveObservationsCorrespond](RetrieveObservationsCorrespond/execution.json) | UNSAT | UNSAT | completed | 4.198 | Matched |
| [TransmitEffectsCorrespond](TransmitEffectsCorrespond/execution.json) | UNSAT | UNSAT | completed | 2.968 | Matched |
| [ReceiveEffectsCorrespond](ReceiveEffectsCorrespond/execution.json) | UNSAT | UNSAT | completed | 3.526 | Matched |
| [DaemonEffectsCorrespond](DaemonEffectsCorrespond/execution.json) | UNSAT | UNSAT | completed | 28.916 | Matched |
| [InsertionEffectsCorrespond](InsertionEffectsCorrespond/execution.json) | UNSAT | UNSAT | completed | 8.169 | Matched |
| [ShowCorrespondingTransmit](ShowCorrespondingTransmit/execution.json) | SAT | SAT | completed | 3.010 | Matched |
| [ShowCorrespondingInsertion](ShowCorrespondingInsertion/execution.json) | SAT | SAT | completed | 4.911 | Matched |
| [ShowCorrespondingReceive](ShowCorrespondingReceive/execution.json) | SAT | SAT | completed | 3.883 | Matched |
| [ShowCorrespondingDaemon](ShowCorrespondingDaemon/execution.json) | SAT | SAT | completed | 5.000 | Matched |

## Frozen sources

- [scaling_correspondence.als](sources/scaling_correspondence.als), SHA-256 `8b12ff9645637d1eea3a8c0275cc15d74626eadd687bd03eadf9b9e21ff32b3d`
- [telecommunications.als](sources/telecommunications.als), SHA-256 `47d76e1f6c80954afd8b2ea0607486f4a410a80298a5d7bfd98573c4ade47621`
- [telecommunications_scalable.als](sources/telecommunications_scalable.als), SHA-256 `05cb357750fabcac8b6ec7e5d2f8ddbd1d74d6896856162bd48f507b87d2dba9`
