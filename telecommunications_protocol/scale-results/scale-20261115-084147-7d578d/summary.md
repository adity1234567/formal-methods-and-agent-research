# Scaling benchmark

Original model SHA-256: `1fa2fa4556b3ce3fec9d4286ba6b5d986bd1d2cd51192b381493f363c1b04181`.

Each command has its own wall-clock timeout. Timed-out or failed commands have no verified outcome. Heap values are JVM caps, not measurements of peak process memory. Native solver allocations are additional.

Scopes bound available SPC atoms. Only the separately named exact-route witnesses require the active route to reach the boundary. These witnesses demonstrate existence, not general initialised reachability.

Representation: `ordered`. In sequence mode the route and histories share a sequence bound. Ordered mode uses the selected independent history bound. All results remain finite-scope evidence.

External SAT solvers (Kissat, CaDiCaL) decide only UNSAT-expected checks from Alloy's CNF export. Witnesses and the expected bug use a built-in Alloy solver so their instances can be validated.

| SPC bound | seq | Int bits | Command | Solver | Expected | Observed | Status | Seconds | Validated |
|---|---|---|---|---|---|---|---|---|---|
| 20 | 4 | 5 | BrokenReceiveWouldPreserveInvariant | glucose | SAT | SAT | completed | 2.288 | yes |
| 20 | 4 | 5 | DaemonIsInvisible | glucose | UNSAT | UNKNOWN | timed_out | 240.076 | no |
| 20 | 4 | 5 | DaemonPreservesInvariant | glucose | UNSAT | UNKNOWN | timed_out | 240.143 | no |
| 20 | 4 | 5 | InitialIsValid | glucose | UNSAT | UNSAT | completed | 10.090 | yes |
| 20 | 4 | 5 | InsertionIsInvisible | glucose | UNSAT | UNKNOWN | timed_out | 240.085 | no |
| 20 | 4 | 5 | InsertionPreservesInvariant | glucose | UNSAT | UNKNOWN | timed_out | 240.132 | no |
| 20 | 4 | 5 | ReceivePreservesInvariant | glucose | UNSAT | UNSAT | completed | 190.782 | yes |
| 20 | 4 | 5 | ReceiveRefinesExternal | glucose | UNSAT | UNKNOWN | timed_out | 240.089 | no |
| 20 | 4 | 5 | RetrieveIsValid | glucose | UNSAT | UNKNOWN | timed_out | 240.144 | no |
| 20 | 4 | 5 | ShowDaemon | glucose | SAT | SAT | completed | 27.717 | yes |
| 20 | 4 | 5 | ShowFullRouteDaemon | glucose | SAT | SAT | completed | 14.035 | yes |
| 20 | 4 | 5 | ShowFullRouteInsertion | glucose | SAT | SAT | completed | 13.613 | yes |
| 20 | 4 | 5 | ShowFullRoutePendingPoll | glucose | SAT | SAT | completed | 5.878 | yes |
| 20 | 4 | 5 | ShowFullRouteReceive | glucose | SAT | SAT | completed | 13.724 | yes |
| 20 | 4 | 5 | ShowFullRouteTransmit | glucose | SAT | SAT | completed | 2.256 | yes |
| 20 | 4 | 5 | ShowFullRouteWithTraffic | glucose | SAT | SAT | completed | 1.839 | yes |
| 20 | 4 | 5 | ShowInsertionWithTraffic | glucose | SAT | SAT | completed | 26.474 | yes |
| 20 | 4 | 5 | ShowPendingPollCanStutter | glucose | SAT | SAT | completed | 29.983 | yes |
| 20 | 4 | 5 | ShowReceive | glucose | SAT | SAT | completed | 2.297 | yes |
| 20 | 4 | 5 | ShowTransmit | glucose | SAT | SAT | completed | 2.223 | yes |
| 20 | 4 | 5 | TransmitPreservesInvariant | glucose | UNSAT | UNSAT | completed | 59.174 | yes |
| 20 | 4 | 5 | TransmitRefinesExternal | glucose | UNSAT | UNSAT | completed | 96.917 | yes |

Per-command directories retain generated sources, execution metadata, raw logs and all available Analyzer evidence.
