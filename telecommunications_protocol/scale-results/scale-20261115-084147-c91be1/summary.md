# Scaling benchmark

Original model SHA-256: `1fa2fa4556b3ce3fec9d4286ba6b5d986bd1d2cd51192b381493f363c1b04181`.

Each command has its own wall-clock timeout. Timed-out or failed commands have no verified outcome. Heap values are JVM caps, not measurements of peak process memory. Native solver allocations are additional.

Scopes bound available SPC atoms. Only the separately named exact-route witnesses require the active route to reach the boundary. These witnesses demonstrate existence, not general initialised reachability.

Representation: `ordered`. In sequence mode the route and histories share a sequence bound. Ordered mode uses the selected independent history bound. All results remain finite-scope evidence.

External SAT solvers (Kissat, CaDiCaL) decide only UNSAT-expected checks from Alloy's CNF export. Witnesses and the expected bug use a built-in Alloy solver so their instances can be validated.

| SPC bound | seq | Int bits | Command | Solver | Expected | Observed | Status | Seconds | Validated |
|---|---|---|---|---|---|---|---|---|---|
| 100 | 4 | 5 | BrokenReceiveWouldPreserveInvariant | glucose | SAT | SAT | completed | 32.825 | yes |
| 100 | 4 | 5 | DaemonIsInvisible | glucose | UNSAT | UNKNOWN | timed_out | 240.329 | no |
| 100 | 4 | 5 | DaemonPreservesInvariant | glucose | UNSAT | UNKNOWN | timed_out | 240.130 | no |
| 100 | 4 | 5 | InitialIsValid | glucose | UNSAT | UNSAT | completed | 10.410 | yes |
| 100 | 4 | 5 | InsertionIsInvisible | glucose | UNSAT | UNKNOWN | timed_out | 240.070 | no |
| 100 | 4 | 5 | InsertionPreservesInvariant | glucose | UNSAT | UNKNOWN | timed_out | 240.273 | no |
| 100 | 4 | 5 | ReceivePreservesInvariant | glucose | UNSAT | UNKNOWN | timed_out | 240.160 | no |
| 100 | 4 | 5 | ReceiveRefinesExternal | glucose | UNSAT | UNKNOWN | timed_out | 240.186 | no |
| 100 | 4 | 5 | RetrieveIsValid | glucose | UNSAT | UNKNOWN | timed_out | 240.146 | no |
| 100 | 4 | 5 | ShowDaemon | glucose | SAT | SAT | completed | 11.398 | yes |
| 100 | 4 | 5 | ShowFullRouteDaemon | glucose | SAT | SAT | completed | 10.319 | yes |
| 100 | 4 | 5 | ShowFullRouteInsertion | glucose | SAT | SAT | completed | 10.082 | yes |
| 100 | 4 | 5 | ShowFullRoutePendingPoll | glucose | SAT | SAT | completed | 8.686 | yes |
| 100 | 4 | 5 | ShowFullRouteReceive | glucose | SAT | SAT | completed | 10.393 | yes |
| 100 | 4 | 5 | ShowFullRouteTransmit | glucose | SAT | SAT | completed | 9.706 | yes |
| 100 | 4 | 5 | ShowFullRouteWithTraffic | glucose | SAT | SAT | completed | 11.388 | yes |
| 100 | 4 | 5 | ShowInsertionWithTraffic | glucose | SAT | SAT | completed | 13.928 | yes |
| 100 | 4 | 5 | ShowPendingPollCanStutter | glucose | SAT | SAT | completed | 13.482 | yes |
| 100 | 4 | 5 | ShowReceive | glucose | SAT | SAT | completed | 20.861 | yes |
| 100 | 4 | 5 | ShowTransmit | glucose | SAT | SAT | completed | 31.762 | yes |
| 100 | 4 | 5 | TransmitPreservesInvariant | glucose | UNSAT | UNKNOWN | timed_out | 240.178 | no |
| 100 | 4 | 5 | TransmitRefinesExternal | glucose | UNSAT | UNKNOWN | timed_out | 240.214 | no |

Per-command directories retain generated sources, execution metadata, raw logs and all available Analyzer evidence.
