# Scaling benchmark

Original model SHA-256: `05cb357750fabcac8b6ec7e5d2f8ddbd1d74d6896856162bd48f507b87d2dba9`.

Each command has its own wall-clock timeout. Timed-out or failed commands have no verified outcome. Heap values are JVM caps, not measurements of peak process memory. Native solver allocations are additional.

Scopes bound available SPC atoms. Only the separately named exact-route witnesses require the active route to reach the boundary. These witnesses demonstrate existence, not general initialised reachability.

Representation: `ordered`. In sequence mode the route and histories share a sequence bound. Ordered mode uses the selected independent history bound. All results remain finite-scope evidence.

External SAT solvers (Kissat, CaDiCaL) decide only UNSAT-expected checks from Alloy's CNF export. Witnesses and the expected bug use a built-in Alloy solver so their instances can be validated.

| SPC bound | seq | Int bits | Command | Solver | Expected | Observed | Status | Seconds | Validated |
|---|---|---|---|---|---|---|---|---|---|
| 10 | 4 | 5 | BrokenReceiveWouldPreserveInvariant | glucose | SAT | SAT | completed | 3.948 | yes |
| 10 | 4 | 5 | DaemonIsInvisible | glucose | UNSAT | UNKNOWN | timed_out | 45.083 | no |
| 10 | 4 | 5 | DaemonPreservesInvariant | glucose | UNSAT | UNKNOWN | timed_out | 45.053 | no |
| 10 | 4 | 5 | InitialIsValid | glucose | UNSAT | UNSAT | completed | 1.755 | yes |
| 10 | 4 | 5 | InsertionIsInvisible | glucose | UNSAT | UNKNOWN | timed_out | 50.049 | no |
| 10 | 4 | 5 | InsertionPreservesInvariant | glucose | UNSAT | UNKNOWN | timed_out | 45.050 | no |
| 10 | 4 | 5 | ReceivePreservesInvariant | glucose | UNSAT | UNKNOWN | timed_out | 45.055 | no |
| 10 | 4 | 5 | ReceiveRefinesExternal | glucose | UNSAT | UNKNOWN | timed_out | 45.074 | no |
| 10 | 4 | 5 | RetrieveIsValid | glucose | UNSAT | UNKNOWN | timed_out | 50.088 | no |
| 10 | 4 | 5 | ShowDaemon | glucose | SAT | SAT | completed | 2.453 | yes |
| 10 | 4 | 5 | ShowFullRouteDaemon | glucose | SAT | SAT | completed | 2.411 | yes |
| 10 | 4 | 5 | ShowFullRouteInsertion | glucose | SAT | SAT | completed | 2.441 | yes |
| 10 | 4 | 5 | ShowFullRoutePendingPoll | glucose | SAT | SAT | completed | 3.483 | yes |
| 10 | 4 | 5 | ShowFullRouteReceive | glucose | SAT | SAT | completed | 2.454 | yes |
| 10 | 4 | 5 | ShowFullRouteTransmit | glucose | SAT | SAT | completed | 2.250 | yes |
| 10 | 4 | 5 | ShowFullRouteWithTraffic | glucose | SAT | SAT | completed | 2.180 | yes |
| 10 | 4 | 5 | ShowInsertionWithTraffic | glucose | SAT | SAT | completed | 2.485 | yes |
| 10 | 4 | 5 | ShowPendingPollCanStutter | glucose | SAT | SAT | completed | 2.403 | yes |
| 10 | 4 | 5 | ShowReceive | glucose | SAT | SAT | completed | 2.526 | yes |
| 10 | 4 | 5 | ShowRepeatedMessageValue | glucose | SAT | SAT | completed | 2.028 | yes |
| 10 | 4 | 5 | ShowTransmit | glucose | SAT | SAT | completed | 3.292 | yes |
| 10 | 4 | 5 | ShowTwoMessageDelivery | glucose | SAT | SAT | completed | 3.020 | yes |
| 10 | 4 | 5 | TransmitPreservesInvariant | glucose | UNSAT | UNKNOWN | timed_out | 45.076 | no |
| 10 | 4 | 5 | TransmitRefinesExternal | glucose | UNSAT | UNKNOWN | timed_out | 45.049 | no |
| 6 | 4 | 5 | BrokenReceiveWouldPreserveInvariant | glucose | SAT | SAT | completed | 1.554 | yes |
| 6 | 4 | 5 | DaemonIsInvisible | glucose | UNSAT | UNSAT | completed | 35.030 | yes |
| 6 | 4 | 5 | DaemonPreservesInvariant | glucose | UNSAT | UNSAT | completed | 26.902 | yes |
| 6 | 4 | 5 | InitialIsValid | glucose | UNSAT | UNSAT | completed | 1.222 | yes |
| 6 | 4 | 5 | InsertionIsInvisible | glucose | UNSAT | UNSAT | completed | 15.001 | yes |
| 6 | 4 | 5 | InsertionPreservesInvariant | glucose | UNSAT | UNSAT | completed | 12.491 | yes |
| 6 | 4 | 5 | ReceivePreservesInvariant | glucose | UNSAT | UNSAT | completed | 15.483 | yes |
| 6 | 4 | 5 | ReceiveRefinesExternal | glucose | UNSAT | UNSAT | completed | 13.448 | yes |
| 6 | 4 | 5 | RetrieveIsValid | glucose | UNSAT | UNSAT | completed | 11.640 | yes |
| 6 | 4 | 5 | ShowDaemon | glucose | SAT | SAT | completed | 2.078 | yes |
| 6 | 4 | 5 | ShowFullRouteDaemon | glucose | SAT | SAT | completed | 2.647 | yes |
| 6 | 4 | 5 | ShowFullRouteInsertion | glucose | SAT | SAT | completed | 1.746 | yes |
| 6 | 4 | 5 | ShowFullRoutePendingPoll | glucose | SAT | SAT | completed | 2.331 | yes |
| 6 | 4 | 5 | ShowFullRouteReceive | glucose | SAT | SAT | completed | 1.939 | yes |
| 6 | 4 | 5 | ShowFullRouteTransmit | glucose | SAT | SAT | completed | 1.437 | yes |
| 6 | 4 | 5 | ShowFullRouteWithTraffic | glucose | SAT | SAT | completed | 1.531 | yes |
| 6 | 4 | 5 | ShowInsertionWithTraffic | glucose | SAT | SAT | completed | 1.720 | yes |
| 6 | 4 | 5 | ShowPendingPollCanStutter | glucose | SAT | SAT | completed | 1.815 | yes |
| 6 | 4 | 5 | ShowReceive | glucose | SAT | SAT | completed | 2.048 | yes |
| 6 | 4 | 5 | ShowRepeatedMessageValue | glucose | SAT | SAT | completed | 1.446 | yes |
| 6 | 4 | 5 | ShowTransmit | glucose | SAT | SAT | completed | 1.542 | yes |
| 6 | 4 | 5 | ShowTwoMessageDelivery | glucose | SAT | SAT | completed | 2.380 | yes |
| 6 | 4 | 5 | TransmitPreservesInvariant | glucose | UNSAT | UNSAT | completed | 7.373 | yes |
| 6 | 4 | 5 | TransmitRefinesExternal | glucose | UNSAT | UNSAT | completed | 5.242 | yes |
| 8 | 4 | 5 | BrokenReceiveWouldPreserveInvariant | glucose | SAT | SAT | completed | 2.064 | yes |
| 8 | 4 | 5 | DaemonIsInvisible | glucose | UNSAT | UNKNOWN | timed_out | 45.056 | no |
| 8 | 4 | 5 | DaemonPreservesInvariant | glucose | UNSAT | UNKNOWN | timed_out | 45.051 | no |
| 8 | 4 | 5 | InitialIsValid | glucose | UNSAT | UNSAT | completed | 2.048 | yes |
| 8 | 4 | 5 | InsertionIsInvisible | glucose | UNSAT | UNKNOWN | timed_out | 45.090 | no |
| 8 | 4 | 5 | InsertionPreservesInvariant | glucose | UNSAT | UNSAT | completed | 40.590 | yes |
| 8 | 4 | 5 | ReceivePreservesInvariant | glucose | UNSAT | UNSAT | completed | 38.962 | yes |
| 8 | 4 | 5 | ReceiveRefinesExternal | glucose | UNSAT | UNKNOWN | timed_out | 45.036 | no |
| 8 | 4 | 5 | RetrieveIsValid | glucose | UNSAT | UNSAT | completed | 24.324 | yes |
| 8 | 4 | 5 | ShowDaemon | glucose | SAT | SAT | completed | 2.087 | yes |
| 8 | 4 | 5 | ShowFullRouteDaemon | glucose | SAT | SAT | completed | 2.421 | yes |
| 8 | 4 | 5 | ShowFullRouteInsertion | glucose | SAT | SAT | completed | 2.431 | yes |
| 8 | 4 | 5 | ShowFullRoutePendingPoll | glucose | SAT | SAT | completed | 2.313 | yes |
| 8 | 4 | 5 | ShowFullRouteReceive | glucose | SAT | SAT | completed | 2.984 | yes |
| 8 | 4 | 5 | ShowFullRouteTransmit | glucose | SAT | SAT | completed | 2.576 | yes |
| 8 | 4 | 5 | ShowFullRouteWithTraffic | glucose | SAT | SAT | completed | 1.894 | yes |
| 8 | 4 | 5 | ShowInsertionWithTraffic | glucose | SAT | SAT | completed | 2.276 | yes |
| 8 | 4 | 5 | ShowPendingPollCanStutter | glucose | SAT | SAT | completed | 2.345 | yes |
| 8 | 4 | 5 | ShowReceive | glucose | SAT | SAT | completed | 2.142 | yes |
| 8 | 4 | 5 | ShowRepeatedMessageValue | glucose | SAT | SAT | completed | 1.941 | yes |
| 8 | 4 | 5 | ShowTransmit | glucose | SAT | SAT | completed | 1.917 | yes |
| 8 | 4 | 5 | ShowTwoMessageDelivery | glucose | SAT | SAT | completed | 2.624 | yes |
| 8 | 4 | 5 | TransmitPreservesInvariant | glucose | UNSAT | UNSAT | completed | 16.877 | yes |
| 8 | 4 | 5 | TransmitRefinesExternal | glucose | UNSAT | UNSAT | completed | 21.405 | yes |

Per-command directories retain generated sources, execution metadata, raw logs and all available Analyzer evidence.
