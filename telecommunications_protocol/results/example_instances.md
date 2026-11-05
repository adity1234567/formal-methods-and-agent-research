# Examples extracted from actual Alloy instances

Execution: `run-20261103-215246-91a68f`. These tables were decoded from its XML witnesses. Every list is newest first. Snapshot names are the Analyzer's actual atom names.

## Two-message delivery

Route: `SPC$0` -> `SPC$1`. A = `Message$1`; B = `Message$0`.

| Step | Snapshot | Action | First queue | Last queue | Input | Output |
|---|---|---|---|---|---|---|
| 0 | `State$4` | Initialise | `[]` | `[]` | `[]` | `[]` |
| 1 | `State$6` | Transmit A | `[A]` | `[]` | `[A]` | `[]` |
| 2 | `State$0` | Transmit B | `[B, A]` | `[]` | `[B, A]` | `[]` |
| 3 | `State$1` | Forward A | `[B]` | `[A]` | `[B, A]` | `[]` |
| 4 | `State$5` | Forward B | `[]` | `[B, A]` | `[B, A]` | `[]` |
| 5 | `State$3` | Receive A | `[]` | `[B]` | `[B, A]` | `[A]` |
| 6 | `State$2` | Receive B | `[]` | `[]` | `[B, A]` | `[B, A]` |

A is delivered before B. The final displayed output `[B,A]` records that delivery history with its newest entry first.

[Source XML](run-20261103-215246-91a68f/alloy/ShowTwoMessageDelivery-solution-0.xml).

## Intentional newest-first bug

The correct rule removes the oldest pending occurrence (rightmost value `Message$0`). The broken rule removes the newest occurrence (leftmost value `Message$1`). Repeated values can make these endpoint values equal; their sequence positions still differ.

| Snapshot | Received | Pending | Sent | Pending concatenated with sent |
|---|---|---|---|---|
| `State$1` | `[Message$1, Message$1, Message$0, Message$1]` | `[Message$1, Message$1, Message$0]` | `[Message$1]` | `[Message$1, Message$1, Message$0, Message$1]` |
| `State$0` | `[Message$1, Message$1, Message$0, Message$1]` | `[Message$1, Message$0]` | `[Message$1, Message$1]` | `[Message$1, Message$0, Message$1, Message$1]` |

The before-state satisfies received = pending concatenated with sent; the after-state violates it. This counterexample comes from the isolated buggy predicate. See [verification_summary.md](verification_summary.md) for recorded results of the correct operations.

[Source XML](run-20261103-215246-91a68f/alloy/BrokenReceiveWouldPreserveInvariant-solution-0.xml).
