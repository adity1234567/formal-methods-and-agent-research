# Scaling benchmark

Original model SHA-256: `90d12093ed643ef65ed81ab470a26d0216c7ff245490d322c620d76a0b36a79f`.

Each command has its own wall-clock timeout. Timed-out or failed commands have no verified outcome. Heap values are JVM caps, not measurements of peak process memory. Native solver allocations are additional.

Scopes bound available SPC atoms. Only the separately named exact-route witnesses require the active route to reach the boundary. These witnesses demonstrate existence, not general initialised reachability.

Representation: `ordered`. In sequence mode the route and histories share a sequence bound. Ordered mode uses the selected independent history bound. All results remain finite-scope evidence.

External SAT solvers (Kissat, CaDiCaL) decide only UNSAT-expected checks from Alloy's CNF export. Witnesses and the expected bug use a built-in Alloy solver so their instances can be validated.

| SPC bound | seq | Int bits | Command | Solver | Expected | Observed | Status | Seconds | Validated |
|---|---|---|---|---|---|---|---|---|---|
| 6 | 4 | 5 | BrokenReceiveWouldPreserveInvariant | glucose | SAT | UNKNOWN | failed | 0.503 | no |
| 6 | 4 | 5 | DaemonIsInvisible | glucose | UNSAT | UNKNOWN | failed | 0.504 | no |
| 6 | 4 | 5 | DaemonPreservesInvariant | glucose | UNSAT | UNKNOWN | failed | 0.527 | no |
| 6 | 4 | 5 | InitialIsValid | glucose | UNSAT | UNKNOWN | failed | 0.596 | no |
| 6 | 4 | 5 | InsertionIsInvisible | glucose | UNSAT | UNKNOWN | failed | 0.487 | no |
| 6 | 4 | 5 | InsertionPreservesInvariant | glucose | UNSAT | UNKNOWN | failed | 0.539 | no |
| 6 | 4 | 5 | ReceivePreservesInvariant | glucose | UNSAT | UNKNOWN | failed | 0.669 | no |
| 6 | 4 | 5 | ReceiveRefinesExternal | glucose | UNSAT | UNKNOWN | failed | 0.500 | no |
| 6 | 4 | 5 | RetrieveIsValid | glucose | UNSAT | UNKNOWN | failed | 0.887 | no |
| 6 | 4 | 5 | ShowDaemon | glucose | SAT | UNKNOWN | failed | 0.598 | no |
| 6 | 4 | 5 | ShowFullRouteDaemon | glucose | SAT | UNKNOWN | failed | 0.528 | no |
| 6 | 4 | 5 | ShowFullRouteInsertion | glucose | SAT | UNKNOWN | failed | 0.629 | no |
| 6 | 4 | 5 | ShowFullRoutePendingPoll | glucose | SAT | UNKNOWN | failed | 0.515 | no |
| 6 | 4 | 5 | ShowFullRouteReceive | glucose | SAT | UNKNOWN | failed | 0.502 | no |
| 6 | 4 | 5 | ShowFullRouteTransmit | glucose | SAT | UNKNOWN | failed | 0.501 | no |
| 6 | 4 | 5 | ShowFullRouteWithTraffic | glucose | SAT | UNKNOWN | failed | 0.454 | no |
| 6 | 4 | 5 | ShowInsertionWithTraffic | glucose | SAT | UNKNOWN | failed | 0.627 | no |
| 6 | 4 | 5 | ShowPendingPollCanStutter | glucose | SAT | UNKNOWN | failed | 0.474 | no |
| 6 | 4 | 5 | ShowReceive | glucose | SAT | UNKNOWN | failed | 0.514 | no |
| 6 | 4 | 5 | ShowRepeatedMessageValue | glucose | SAT | UNKNOWN | failed | 0.647 | no |
| 6 | 4 | 5 | ShowTransmit | glucose | SAT | UNKNOWN | failed | 0.524 | no |
| 6 | 4 | 5 | ShowTwoMessageDelivery | glucose | SAT | UNKNOWN | failed | 0.501 | no |
| 6 | 4 | 5 | TransmitPreservesInvariant | glucose | UNSAT | UNKNOWN | failed | 0.980 | no |
| 6 | 4 | 5 | TransmitRefinesExternal | glucose | UNSAT | UNKNOWN | failed | 0.524 | no |
| 8 | 4 | 5 | InitialIsValid | glucose | UNSAT | UNKNOWN | abandoned | ? | no |

Per-command directories retain generated sources, execution metadata, raw logs and all available Analyzer evidence.
