# Bounded correspondence between protocol representations

Run: `correspondence-slots-20261115-021530-4b9237`. Status: `completed`.
All selected expectations and evidence validated: **yes**.

Harness: `scaling_slots_correspondence.als`.

These checks compare paired states under a point/message bijection and an explicit route-order relation. They do not assume either post-state invariant. SAT witnesses exercise paired operations.

Scope: three available points in each representation, up to three message values, four-entry histories, six-bit integers, and exactly two states per representation in each command.

This is bounded conditional representation correspondence. It does not establish arbitrary-size equivalence or full enabledness equivalence for a fixed ordered pool. The original insertion may choose a fresh point whose fixed pool position is incompatible with the requested gap.

Timeout per command: 900.0 seconds. JVM heap cap: 3072 MiB. Heap cap is not measured peak process memory.

| Command and evidence | Expected | Observed | Status | Seconds | Interpretation |
|---|---|---|---|---:|---|
| [SectionInvariantsCorrespond](SectionInvariantsCorrespond/execution.json) | UNSAT | UNSAT | completed | 3.613 | Matched |
| [InitialStatesCorrespond](InitialStatesCorrespond/execution.json) | UNSAT | UNSAT | completed | 1.902 | Matched |
| [RetrieveObservationsCorrespond](RetrieveObservationsCorrespond/execution.json) | UNSAT | UNSAT | completed | 2.835 | Matched |
| [TransmitEffectsCorrespond](TransmitEffectsCorrespond/execution.json) | UNSAT | UNSAT | completed | 4.966 | Matched |
| [ReceiveEffectsCorrespond](ReceiveEffectsCorrespond/execution.json) | UNSAT | UNSAT | completed | 16.306 | Matched |
| [DaemonEffectsCorrespond](DaemonEffectsCorrespond/execution.json) | UNSAT | UNSAT | completed | 71.228 | Matched |
| [InsertionEffectsCorrespond](InsertionEffectsCorrespond/execution.json) | UNSAT | UNSAT | completed | 2.223 | Matched |
| [ExternalPredicatesCorrespond](ExternalPredicatesCorrespond/execution.json) | UNSAT | UNSAT | completed | 14.893 | Matched |
| [ShowCorrespondingTransmit](ShowCorrespondingTransmit/execution.json) | SAT | SAT | completed | 2.149 | Matched |
| [ShowCorrespondingInsertion](ShowCorrespondingInsertion/execution.json) | SAT | SAT | completed | 2.169 | Matched |
| [ShowCorrespondingReceive](ShowCorrespondingReceive/execution.json) | SAT | SAT | completed | 2.206 | Matched |
| [ShowCorrespondingDaemon](ShowCorrespondingDaemon/execution.json) | SAT | SAT | completed | 2.276 | Matched |

## Frozen sources

- [scaling_slots_correspondence.als](sources/scaling_slots_correspondence.als), SHA-256 `259fe45a1df6e74cea3276c2ef06239c304e1cfb7512e06de22c7f40e9a4b600`
- [telecommunications.als](sources/telecommunications.als), SHA-256 `47d76e1f6c80954afd8b2ea0607486f4a410a80298a5d7bfd98573c4ade47621`
- [telecommunications_slots.als](sources/telecommunications_slots.als), SHA-256 `1fa2fa4556b3ce3fec9d4286ba6b5d986bd1d2cd51192b381493f363c1b04181`
