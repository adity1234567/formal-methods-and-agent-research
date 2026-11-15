# Scaling benchmark

Original model SHA-256: `1395072cf94608a7d202ced6a66dfec9bdcda9f3a3ac2c857a477d8917f3169b`.

Each command has its own wall-clock timeout. Timed-out or failed commands have no verified outcome. Heap values are JVM caps, not measurements of peak process memory. Native solver allocations are additional.

Scopes bound available SPC atoms. Only the separately named exact-route witnesses require the active route to reach the boundary. These witnesses demonstrate existence, not general initialised reachability.

Representation: `ordered`. In sequence mode the route and histories share a sequence bound. Ordered mode uses the selected independent history bound. All results remain finite-scope evidence.

External SAT solvers (Kissat, CaDiCaL) decide only UNSAT-expected checks from Alloy's CNF export. Witnesses and the expected bug use a built-in Alloy solver so their instances can be validated.

| SPC bound | seq | Int bits | Command | Solver | Expected | Observed | Status | Seconds | Validated |
|---|---|---|---|---|---|---|---|---|---|
| 10 | 2 | 5 | BrokenReceiveWouldPreserveInvariant | glucose | SAT | SAT | completed | 1.788 | yes |
| 10 | 2 | 5 | DaemonIsInvisible | glucose | UNSAT | UNSAT | completed | 34.158 | yes |
| 10 | 2 | 5 | DaemonPreservesInvariant | glucose | UNSAT | UNSAT | completed | 31.469 | yes |
| 10 | 2 | 5 | InitialIsValid | glucose | UNSAT | UNSAT | completed | 1.127 | yes |
| 10 | 2 | 5 | InsertionIsInvisible | glucose | UNSAT | UNSAT | completed | 7.437 | yes |
| 10 | 2 | 5 | InsertionPreservesInvariant | glucose | UNSAT | UNSAT | completed | 23.312 | yes |
| 10 | 2 | 5 | ReceivePreservesInvariant | glucose | UNSAT | UNSAT | completed | 20.719 | yes |
| 10 | 2 | 5 | ReceiveRefinesExternal | glucose | UNSAT | UNSAT | completed | 14.236 | yes |
| 10 | 2 | 5 | RetrieveIsValid | glucose | UNSAT | UNKNOWN | timed_out | 45.019 | no |
| 10 | 2 | 5 | ShowDaemon | glucose | SAT | SAT | completed | 1.485 | yes |
| 10 | 2 | 5 | ShowFullRouteDaemon | glucose | SAT | SAT | completed | 2.148 | yes |
| 10 | 2 | 5 | ShowFullRouteInsertion | glucose | SAT | SAT | completed | 1.425 | yes |
| 10 | 2 | 5 | ShowFullRoutePendingPoll | glucose | SAT | SAT | completed | 2.085 | yes |
| 10 | 2 | 5 | ShowFullRouteReceive | glucose | SAT | SAT | completed | 1.649 | yes |
| 10 | 2 | 5 | ShowFullRouteTransmit | glucose | SAT | SAT | completed | 1.892 | yes |
| 10 | 2 | 5 | ShowFullRouteWithTraffic | glucose | SAT | SAT | completed | 1.573 | yes |
| 10 | 2 | 5 | ShowInsertionWithTraffic | glucose | SAT | SAT | completed | 1.620 | yes |
| 10 | 2 | 5 | ShowPendingPollCanStutter | glucose | SAT | SAT | completed | 1.574 | yes |
| 10 | 2 | 5 | ShowReceive | glucose | SAT | SAT | completed | 1.503 | yes |
| 10 | 2 | 5 | ShowTransmit | glucose | SAT | SAT | completed | 1.434 | yes |
| 10 | 2 | 5 | TransmitPreservesInvariant | glucose | UNSAT | UNSAT | completed | 13.100 | yes |
| 10 | 2 | 5 | TransmitRefinesExternal | glucose | UNSAT | UNSAT | completed | 1.894 | yes |
| 20 | 2 | 5 | BrokenReceiveWouldPreserveInvariant | glucose | SAT | SAT | completed | 1.813 | yes |
| 20 | 2 | 5 | DaemonIsInvisible | glucose | UNSAT | UNKNOWN | timed_out | 45.055 | no |
| 20 | 2 | 5 | DaemonPreservesInvariant | glucose | UNSAT | UNKNOWN | timed_out | 50.042 | no |
| 20 | 2 | 5 | InitialIsValid | glucose | UNSAT | UNSAT | completed | 8.184 | yes |
| 20 | 2 | 5 | InsertionIsInvisible | glucose | UNSAT | UNKNOWN | timed_out | 45.087 | no |
| 20 | 2 | 5 | InsertionPreservesInvariant | glucose | UNSAT | UNKNOWN | timed_out | 45.245 | no |
| 20 | 2 | 5 | ReceivePreservesInvariant | glucose | UNSAT | UNKNOWN | timed_out | 45.105 | no |
| 20 | 2 | 5 | ReceiveRefinesExternal | glucose | UNSAT | UNKNOWN | timed_out | 45.038 | no |
| 20 | 2 | 5 | RetrieveIsValid | glucose | UNSAT | UNKNOWN | timed_out | 45.092 | no |
| 20 | 2 | 5 | ShowDaemon | glucose | SAT | SAT | completed | 1.391 | yes |
| 20 | 2 | 5 | ShowFullRouteDaemon | glucose | SAT | SAT | completed | 1.471 | yes |
| 20 | 2 | 5 | ShowFullRouteInsertion | glucose | SAT | SAT | completed | 1.453 | yes |
| 20 | 2 | 5 | ShowFullRoutePendingPoll | glucose | SAT | SAT | completed | 1.707 | yes |
| 20 | 2 | 5 | ShowFullRouteReceive | glucose | SAT | SAT | completed | 1.407 | yes |
| 20 | 2 | 5 | ShowFullRouteTransmit | glucose | SAT | SAT | completed | 1.401 | yes |
| 20 | 2 | 5 | ShowFullRouteWithTraffic | glucose | SAT | SAT | completed | 1.665 | yes |
| 20 | 2 | 5 | ShowInsertionWithTraffic | glucose | SAT | SAT | completed | 1.599 | yes |
| 20 | 2 | 5 | ShowPendingPollCanStutter | glucose | SAT | SAT | completed | 1.467 | yes |
| 20 | 2 | 5 | ShowReceive | glucose | SAT | SAT | completed | 1.489 | yes |
| 20 | 2 | 5 | ShowTransmit | glucose | SAT | SAT | completed | 1.736 | yes |
| 20 | 2 | 5 | TransmitPreservesInvariant | glucose | UNSAT | UNSAT | completed | 30.561 | yes |
| 20 | 2 | 5 | TransmitRefinesExternal | glucose | UNSAT | UNSAT | completed | 5.957 | yes |

Per-command directories retain generated sources, execution metadata, raw logs and all available Analyzer evidence.
