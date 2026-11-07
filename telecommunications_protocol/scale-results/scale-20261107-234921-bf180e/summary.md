# Scaling benchmark

Original model SHA-256: `05cb357750fabcac8b6ec7e5d2f8ddbd1d74d6896856162bd48f507b87d2dba9`.

Each command has its own wall-clock timeout. Timed-out or failed commands have no verified outcome. Heap values are JVM caps, not measurements of peak process memory. Native solver allocations are additional.

Scopes bound available SPC atoms. Only the separately named exact-route witnesses require the active route to reach the boundary. These witnesses demonstrate existence, not general initialised reachability.

Representation: `ordered`. In sequence mode the route and histories share a sequence bound. Ordered mode uses the selected independent history bound. All results remain finite-scope evidence.

| SPC bound | seq | Int bits | Command | Expected | Observed | Status | Seconds | Validated |
|---|---|---|---|---|---|---|---|---|
| 100 | 4 | 5 | InitialIsValid | UNSAT | UNSAT | completed | 6.509 | yes |
| 100 | 4 | 5 | ShowFullRouteWithTraffic | SAT | SAT | completed | 12.999 | yes |
| 1000 | 4 | 5 | InitialIsValid | UNSAT | UNKNOWN | failed | 0.901 | no |
| 1000 | 4 | 5 | ShowFullRouteWithTraffic | SAT | UNKNOWN | failed | 1.416 | no |

Per-command directories retain generated sources, execution metadata, raw logs and all available Analyzer evidence.
