# Scaling benchmark

Original model SHA-256: `182c9179911ef07a62dc50d4592494e4adbbd7a35db9d146633de7c526df47c3`.

Each command has its own wall-clock timeout. Timed-out or failed commands have no verified outcome. Heap values are JVM caps, not measurements of peak process memory. Native solver allocations are additional.

Scopes bound available SPC atoms. Only the separately named exact-route witnesses require the active route to reach the boundary. These witnesses demonstrate existence, not general initialised reachability.

Representation: `ordered`. In sequence mode the route and histories share a sequence bound. Ordered mode uses the selected independent history bound. All results remain finite-scope evidence.

| SPC bound | seq | Int bits | Command | Expected | Observed | Status | Seconds | Validated |
|---|---|---|---|---|---|---|---|---|
| 100 | 2 | 5 | BrokenReceiveWouldPreserveInvariant | SAT | SAT | completed | 22.05 | yes |
| 100 | 2 | 5 | DaemonIsInvisible | UNSAT | UNKNOWN | timed_out | 60.118 | no |
| 100 | 2 | 5 | DaemonPreservesInvariant | UNSAT | UNKNOWN | timed_out | 60.073 | no |
| 100 | 2 | 5 | InitialIsValid | UNSAT | UNSAT | completed | 4.091 | yes |
| 100 | 2 | 5 | ReceivePreservesInvariant | UNSAT | UNKNOWN | timed_out | 60.126 | no |
| 100 | 2 | 5 | ReceiveRefinesExternal | UNSAT | UNSAT | completed | 18.097 | yes |
| 100 | 2 | 5 | RetrieveIsValid | UNSAT | UNKNOWN | timed_out | 64.369 | no |
| 100 | 2 | 5 | ShowDaemon | SAT | SAT | completed | 2.179 | yes |
| 100 | 2 | 5 | ShowFullRouteDaemon | SAT | SAT | completed | 2.622 | yes |
| 100 | 2 | 5 | ShowFullRoutePendingPoll | SAT | SAT | completed | 2.615 | yes |
| 100 | 2 | 5 | ShowFullRouteReceive | SAT | SAT | completed | 2.654 | yes |
| 100 | 2 | 5 | ShowFullRouteTransmit | SAT | SAT | completed | 2.533 | yes |
| 100 | 2 | 5 | ShowFullRouteWithTraffic | SAT | SAT | completed | 2.107 | yes |
| 100 | 2 | 5 | ShowPendingPollCanStutter | SAT | SAT | completed | 2.51 | yes |
| 100 | 2 | 5 | ShowReceive | SAT | SAT | completed | 2.119 | yes |
| 100 | 2 | 5 | ShowTransmit | SAT | SAT | completed | 1.903 | yes |
| 100 | 2 | 5 | TransmitPreservesInvariant | UNSAT | UNSAT | completed | 33.914 | yes |
| 100 | 2 | 5 | TransmitRefinesExternal | UNSAT | UNSAT | completed | 8.41 | yes |

Per-command directories retain generated sources, execution metadata, raw logs and all available Analyzer evidence.
