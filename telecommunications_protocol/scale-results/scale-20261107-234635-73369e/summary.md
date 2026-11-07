# Scaling benchmark

Original model SHA-256: `47d76e1f6c80954afd8b2ea0607486f4a410a80298a5d7bfd98573c4ade47621`.

Each command has its own wall-clock timeout. Timed-out or failed commands have no verified outcome. Heap values are JVM caps, not measurements of peak process memory. Native solver allocations are additional.

Scopes bound available SPC atoms. Only the separately named exact-route witnesses require the active route to reach the boundary. These witnesses demonstrate existence, not general initialised reachability.

Representation: `sequence`. In sequence mode the route and histories share a sequence bound. Ordered mode uses the selected independent history bound. All results remain finite-scope evidence.

| SPC bound | seq | Int bits | Command | Expected | Observed | Status | Seconds | Validated |
|---|---|---|---|---|---|---|---|---|
| 6 | 6 | 7 | DaemonPreservesInvariant | UNSAT | UNKNOWN | timed_out | 30.044 | no |
| 6 | 6 | 7 | RetrieveIsValid | UNSAT | UNKNOWN | timed_out | 30.035 | no |
| 6 | 6 | 7 | ShowExactRouteWithTraffic | SAT | SAT | completed | 2.375 | yes |

Per-command directories retain generated sources, execution metadata, raw logs and all available Analyzer evidence.
