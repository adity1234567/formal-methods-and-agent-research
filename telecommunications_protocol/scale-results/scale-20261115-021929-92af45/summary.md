# Scaling benchmark

Original model SHA-256: `1fa2fa4556b3ce3fec9d4286ba6b5d986bd1d2cd51192b381493f363c1b04181`.

Each command has its own wall-clock timeout. Timed-out or failed commands have no verified outcome. Heap values are JVM caps, not measurements of peak process memory. Native solver allocations are additional.

Scopes bound available SPC atoms. Only the separately named exact-route witnesses require the active route to reach the boundary. These witnesses demonstrate existence, not general initialised reachability.

Representation: `ordered`. In sequence mode the route and histories share a sequence bound. Ordered mode uses the selected independent history bound. All results remain finite-scope evidence.

External SAT solvers (Kissat, CaDiCaL) decide only UNSAT-expected checks from Alloy's CNF export. Witnesses and the expected bug use a built-in Alloy solver so their instances can be validated.

| SPC bound | seq | Int bits | Command | Solver | Expected | Observed | Status | Seconds | Validated |
|---|---|---|---|---|---|---|---|---|---|
| 10 | 4 | 5 | BrokenReceiveWouldPreserveInvariant | glucose | SAT | SAT | completed | 3.090 | yes |
| 10 | 4 | 5 | DaemonIsInvisible | kissat (CNF) + DRAT verified | UNSAT | UNSAT | completed | 686.418 (host asleep 78 s) | yes |
| 10 | 4 | 5 | DaemonPreservesInvariant | kissat (CNF) + DRAT verified | UNSAT | UNSAT | completed | 66.007 | yes |
| 10 | 4 | 5 | InitialIsValid | kissat (CNF) + DRAT verified | UNSAT | UNSAT | completed | 23.317 | yes |
| 10 | 4 | 5 | InsertionIsInvisible | kissat (CNF) | UNSAT | UNSAT | completed | 5009.140 (host asleep 4985 s) | no |
| 10 | 4 | 5 | InsertionPreservesInvariant | kissat (CNF) + DRAT verified | UNSAT | UNSAT | completed | 46.162 | yes |
| 10 | 4 | 5 | ReceivePreservesInvariant | kissat (CNF) + DRAT verified | UNSAT | UNSAT | completed | 22.862 | yes |
| 10 | 4 | 5 | ReceiveRefinesExternal | kissat (CNF) + DRAT verified | UNSAT | UNSAT | completed | 561.654 | yes |
| 10 | 4 | 5 | RetrieveIsValid | kissat (CNF) + DRAT verified | UNSAT | UNSAT | completed | 224.940 | yes |
| 10 | 4 | 5 | ShowDaemon | glucose | SAT | SAT | completed | 2.236 | yes |
| 10 | 4 | 5 | ShowFullRouteDaemon | glucose | SAT | SAT | completed | 3.878 | yes |
| 10 | 4 | 5 | ShowFullRouteInsertion | glucose | SAT | SAT | completed | 4.308 | yes |
| 10 | 4 | 5 | ShowFullRoutePendingPoll | glucose | SAT | SAT | completed | 3.733 | yes |
| 10 | 4 | 5 | ShowFullRouteReceive | glucose | SAT | SAT | completed | 3.971 | yes |
| 10 | 4 | 5 | ShowFullRouteTransmit | glucose | SAT | SAT | completed | 3.528 | yes |
| 10 | 4 | 5 | ShowFullRouteWithTraffic | glucose | SAT | SAT | completed | 2.726 | yes |
| 10 | 4 | 5 | ShowInsertionWithTraffic | glucose | SAT | SAT | completed | 2.570 | yes |
| 10 | 4 | 5 | ShowPendingPollCanStutter | glucose | SAT | SAT | completed | 2.262 | yes |
| 10 | 4 | 5 | ShowReceive | glucose | SAT | SAT | completed | 2.241 | yes |
| 10 | 4 | 5 | ShowTransmit | glucose | SAT | SAT | completed | 3.053 | yes |
| 10 | 4 | 5 | TransmitPreservesInvariant | kissat (CNF) + DRAT verified | UNSAT | UNSAT | completed | 18.494 | yes |
| 10 | 4 | 5 | TransmitRefinesExternal | kissat (CNF) + DRAT verified | UNSAT | UNSAT | completed | 33.055 | yes |
| 20 | 4 | 5 | InitialIsValid | kissat (CNF) + DRAT verified | UNSAT | UNSAT | completed | 7.992 (host asleep 8 s) | yes |
| 20 | 4 | 5 | RetrieveIsValid | kissat (CNF) | UNSAT | UNKNOWN | timed_out | 2142.874 (host asleep 2138 s) | no |
| 20 | 4 | 5 | TransmitPreservesInvariant | kissat (CNF) | UNSAT | UNKNOWN | interrupted | ? | no |

Per-command directories retain generated sources, execution metadata, raw logs and all available Analyzer evidence.
