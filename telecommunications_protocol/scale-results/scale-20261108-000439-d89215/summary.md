# Scaling benchmark

Original model SHA-256: `182c9179911ef07a62dc50d4592494e4adbbd7a35db9d146633de7c526df47c3`.

Each command has its own wall-clock timeout. Timed-out or failed commands have no verified outcome. Heap values are JVM caps, not measurements of peak process memory. Native solver allocations are additional.

Scopes bound available SPC atoms. Only the separately named exact-route witnesses require the active route to reach the boundary. These witnesses demonstrate existence, not general initialised reachability.

Representation: `ordered`. In sequence mode the route and histories share a sequence bound. Ordered mode uses the selected independent history bound. All results remain finite-scope evidence.

| SPC bound | seq | Int bits | Command | Expected | Observed | Status | Seconds | Validated |
|---|---|---|---|---|---|---|---|---|
| 1000 | 1 | 5 | InitialIsValid | UNSAT | UNSAT | completed | 42.337 | yes |
| 1000 | 1 | 5 | ShowFullRouteWithTraffic | SAT | SAT | completed | 59.052 | yes |

Per-command directories retain generated sources, execution metadata, raw logs and all available Analyzer evidence.
