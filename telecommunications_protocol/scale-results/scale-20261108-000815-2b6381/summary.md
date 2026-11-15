# Scaling benchmark

Original model SHA-256: `182c9179911ef07a62dc50d4592494e4adbbd7a35db9d146633de7c526df47c3`.

Each command has its own wall-clock timeout. Timed-out or failed commands have no verified outcome. Heap values are JVM caps, not measurements of peak process memory. Native solver allocations are additional.

Scopes bound available SPC atoms. Only the separately named exact-route witnesses require the active route to reach the boundary. These witnesses demonstrate existence, not general initialised reachability.

Representation: `ordered`. In sequence mode the route and histories share a sequence bound. Ordered mode uses the selected independent history bound. All results remain finite-scope evidence.

External SAT solvers (Kissat, CaDiCaL) decide only UNSAT-expected checks from Alloy's CNF export. Witnesses and the expected bug use a built-in Alloy solver so their instances can be validated.

| SPC bound | seq | Int bits | Command | Solver | Expected | Observed | Status | Seconds | Validated |
|---|---|---|---|---|---|---|---|---|---|
| 1000 | 1 | 5 | ShowFullRouteDaemon | glucose | SAT | UNKNOWN | timed_out | 120.100 | no |
| 1000 | 1 | 5 | ShowFullRouteTransmit | glucose | SAT | SAT | completed | 44.363 | yes |

Per-command directories retain generated sources, execution metadata, raw logs and all available Analyzer evidence.
