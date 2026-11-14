# Unbounded proof obligations (Z3)

Report generated: 2026-11-15T02:19:49+06:00 (Asia/Dhaka). Z3 5.4.1. Script: [unbounded_check.py](../unbounded_check.py).

Each proof obligation holds for histories of any length, any number of message values, and, through the locality lemma in [scaling_design.md](../scaling_design.md#unbounded-argument), any number of signalling points. PROVED means Z3 found the negated goal unsatisfiable.

| Obligation | Kind | Expected | Observed | Seconds | Meaning |
|---|---|---|---|---:|---|
| `InitialIsValid` | proof | UNSAT | PROVED | 0.0087 | Empty histories satisfy local conservation; input and output are empty. |
| `RetrieveBase` | proof | UNSAT | PROVED | 0.0033 | Claim holds at the last section (local conservation). |
| `RetrieveStep` | proof | UNSAT | PROVED | 0.0009 | If the claim holds at the next section, it holds here (boundary agreement). |
| `TransmitPreservesInvariant` | proof | UNSAT | PROVED | 0.0014 | Conservation at the first section and its boundary with the next survive transmit. |
| `TransmitRefinesExternal` | proof | UNSAT | PROVED | 0.001 | input' = <m> ++ input, output' = output, and output' remains a suffix of input'. |
| `ReceivePreservesInvariant` | proof | UNSAT | PROVED | 0.001 | Delivering the oldest pending message keeps conservation and the incoming boundary. |
| `ReceiveRefinesExternal` | proof | UNSAT | PROVED | 0.0019 | input' = input, output grows by one, and output' remains a suffix of input'. |
| `DaemonPreservesInvariant` | proof | UNSAT | PROVED | 0.0022 | Both changed sections conserve, and all three affected boundaries agree. |
| `DaemonIsInvisible` | proof | UNSAT | PROVED | 0.0017 | input, output and the route-order concatenation of buffers are unchanged. |
| `InsertionPreservesInvariant` | proof | UNSAT | PROVED | 0.0009 | The fresh section conserves and agrees with both neighbours. |
| `InsertionIsInvisible` | proof | UNSAT | PROVED | 0.0003 | Inserting an empty buffer leaves the concatenation of buffers unchanged. |
| `IdleStepsAreInvisible` | proof | UNSAT | PROVED | 0.0012 | The optional idle/poll stutter changes nothing, so it preserves everything. |
| `BrokenReceiveWouldPreserveInvariant` | counterexample | SAT | counterexample found | 0.0412 | Delivering the NEWEST pending message breaks conservation (mutation is caught). |
| `DaemonWitness` | witness | SAT | satisfiable | 0.0028 | A valid window where the daemon moves the oldest of two distinct values. |
| `ReceiveWitness` | witness | SAT | satisfiable | 0.0052 | A valid last section with two pending messages can deliver one. |

## Scope of the claim

- The obligations are stated on the sequence-level protocol of `telecommunications.als`. Their correspondence with the Alloy predicates and the locality lemma are argued in scaling_design.md; they are not mechanically checked.
- Results rely on the soundness of Z3's sequence solver.
- Safety only. Eventual delivery needs a fairness assumption; see the liveness section of scaling_design.md.
