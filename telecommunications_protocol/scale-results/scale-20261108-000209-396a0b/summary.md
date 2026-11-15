# Scaling benchmark

Original model SHA-256: `182c9179911ef07a62dc50d4592494e4adbbd7a35db9d146633de7c526df47c3`.

Each command has its own wall-clock timeout. Timed-out or failed commands have no verified outcome. Heap values are JVM caps, not measurements of peak process memory. Native solver allocations are additional.

Scopes bound available SPC atoms. Only the separately named exact-route witnesses require the active route to reach the boundary. These witnesses demonstrate existence, not general initialised reachability.

Representation: `ordered`. In sequence mode the route and histories share a sequence bound. Ordered mode uses the selected independent history bound. All results remain finite-scope evidence.

External SAT solvers (Kissat, CaDiCaL) decide only UNSAT-expected checks from Alloy's CNF export. Witnesses and the expected bug use a built-in Alloy solver so their instances can be validated.

| SPC bound | seq | Int bits | Command | Solver | Expected | Observed | Status | Seconds | Validated |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 2 | 5 | BrokenReceiveWouldPreserveInvariant | glucose | SAT | SAT | completed | 22.050 | yes |
| 100 | 2 | 5 | DaemonIsInvisible | glucose | UNSAT | UNKNOWN | timed_out | 60.118 | no |
| 100 | 2 | 5 | DaemonPreservesInvariant | glucose | UNSAT | UNKNOWN | timed_out | 60.073 | no |
| 100 | 2 | 5 | InitialIsValid | glucose | UNSAT | UNSAT | completed | 4.091 | yes |
| 100 | 2 | 5 | ReceivePreservesInvariant | glucose | UNSAT | UNKNOWN | timed_out | 60.126 | no |
| 100 | 2 | 5 | ReceiveRefinesExternal | glucose | UNSAT | UNSAT | completed | 18.097 | yes |
| 100 | 2 | 5 | RetrieveIsValid | glucose | UNSAT | UNKNOWN | timed_out | 64.369 | no |
| 100 | 2 | 5 | ShowDaemon | glucose | SAT | SAT | completed | 2.179 | yes |
| 100 | 2 | 5 | ShowFullRouteDaemon | glucose | SAT | SAT | completed | 2.622 | yes |
| 100 | 2 | 5 | ShowFullRoutePendingPoll | glucose | SAT | SAT | completed | 2.615 | yes |
| 100 | 2 | 5 | ShowFullRouteReceive | glucose | SAT | SAT | completed | 2.654 | yes |
| 100 | 2 | 5 | ShowFullRouteTransmit | glucose | SAT | SAT | completed | 2.533 | yes |
| 100 | 2 | 5 | ShowFullRouteWithTraffic | glucose | SAT | SAT | completed | 2.107 | yes |
| 100 | 2 | 5 | ShowPendingPollCanStutter | glucose | SAT | SAT | completed | 2.510 | yes |
| 100 | 2 | 5 | ShowReceive | glucose | SAT | SAT | completed | 2.119 | yes |
| 100 | 2 | 5 | ShowTransmit | glucose | SAT | SAT | completed | 1.903 | yes |
| 100 | 2 | 5 | TransmitPreservesInvariant | glucose | UNSAT | UNSAT | completed | 33.914 | yes |
| 100 | 2 | 5 | TransmitRefinesExternal | glucose | UNSAT | UNSAT | completed | 8.410 | yes |

Per-command directories retain generated sources, execution metadata, raw logs and all available Analyzer evidence.
