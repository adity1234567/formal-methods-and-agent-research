# Recorded Alloy verification

Report generated: 2026-11-04T15:47:33+06:00 (Asia/Dhaka, UTC+06:00).
Overall: **PASS - all declared expectations and evidence checks matched**.

Run: `run-20261103-215246-91a68f`. Execution status: `completed`. Process exit code: `0`.
Alloy version: `6.2.0`; solver: `glucose`.
Frozen model SHA-256: `47d76e1f6c80954afd8b2ea0607486f4a410a80298a5d7bfd98573c4ade47621`.
Live workspace model matches this saved source: **yes**.

Results below are checked against the source saved with this execution, process status, raw log, receipt, and SAT witness files. Arithmetic overflow prevention is confirmed.

| Command | Type | Expected | Observed | Interpretation |
|---|---|---|---|---|
| `InitialIsValid` | check | UNSAT | UNSAT | No counterexample in scope |
| `RetrieveIsValid` | check | UNSAT | UNSAT | No counterexample in scope |
| `TransmitPreservesInvariant` | check | UNSAT | UNSAT | No counterexample in scope |
| `ReceivePreservesInvariant` | check | UNSAT | UNSAT | No counterexample in scope |
| `DaemonPreservesInvariant` | check | UNSAT | UNSAT | No counterexample in scope |
| `InsertionPreservesInvariant` | check | UNSAT | UNSAT | No counterexample in scope |
| `TransmitRefinesExternal` | check | UNSAT | UNSAT | No counterexample in scope |
| `ReceiveRefinesExternal` | check | UNSAT | UNSAT | No counterexample in scope |
| `DaemonIsInvisible` | check | UNSAT | UNSAT | No counterexample in scope |
| `InsertionIsInvisible` | check | UNSAT | UNSAT | No counterexample in scope |
| `BrokenReceiveWouldPreserveInvariant` | check | SAT | SAT | Expected counterexample found |
| `ShowTransmit` | run | SAT | SAT | Witness found |
| `ShowReceive` | run | SAT | SAT | Witness found |
| `ShowDaemon` | run | SAT | SAT | Witness found |
| `ShowInsertionWithTraffic` | run | SAT | SAT | Witness found |
| `ShowRepeatedMessageValue` | run | SAT | SAT | Witness found |
| `ShowTwoMessageDelivery` | run | SAT | SAT | Witness found |
| `ShowPendingPollCanStutter` | run | SAT | SAT | Witness found |

## Exact commands and bounds

These commands are read from the saved model; their scopes are compared with the Analyzer receipt. A UNSAT check means no counterexample within its finite scope. A SAT run demonstrates a possible instance. Neither establishes an unbounded proof or eventual delivery.

```alloy
check InitialIsValid for 4 but exactly 1 State, 5 Int, 4 seq expect 0
check RetrieveIsValid for 4 but exactly 1 State, 5 Int, 4 seq expect 0
check TransmitPreservesInvariant for 4 but exactly 2 State, 5 Int, 4 seq expect 0
check ReceivePreservesInvariant for 4 but exactly 2 State, 5 Int, 4 seq expect 0
check DaemonPreservesInvariant for 4 but exactly 2 State, 5 Int, 4 seq expect 0
check InsertionPreservesInvariant for 4 but exactly 2 State, 5 Int, 4 seq expect 0
check TransmitRefinesExternal for 4 but exactly 2 State, 5 Int, 4 seq expect 0
check ReceiveRefinesExternal for 4 but exactly 2 State, 5 Int, 4 seq expect 0
check DaemonIsInvisible for 4 but exactly 2 State, 5 Int, 4 seq expect 0
check InsertionIsInvisible for 4 but exactly 2 State, 5 Int, 4 seq expect 0
check BrokenReceiveWouldPreserveInvariant for 3 but exactly 2 State, 5 Int, 4 seq expect 1
run ShowTransmit for 3 but exactly 2 State, 5 Int, 4 seq expect 1
run ShowReceive for 3 but exactly 2 State, 5 Int, 4 seq expect 1
run ShowDaemon for 3 but exactly 2 State, 5 Int, 4 seq expect 1
run ShowInsertionWithTraffic for 3 but exactly 2 State, 5 Int, 4 seq expect 1
run ShowRepeatedMessageValue for 3 but exactly 3 State, exactly 1 Message, 5 Int, 4 seq expect 1
run ShowTwoMessageDelivery for 2 but exactly 7 State, exactly 2 Message, exactly 2 SPC, 5 Int, 4 seq expect 1
run ShowPendingPollCanStutter for 3 but exactly 2 State, 5 Int, 4 seq expect 1
```

## Raw evidence

- [Analyzer log](run-20261103-215246-91a68f/analyzer.log)
- [Analyzer receipt](run-20261103-215246-91a68f/alloy/receipt.json)
- [Saved model](run-20261103-215246-91a68f/telecommunications.als)
- [Execution metadata](run-20261103-215246-91a68f/execution.json)

SAT commands have XML witnesses beside the receipt. [Readable demonstration instances](example_instances.md) are regenerated only after evidence validation succeeds.
