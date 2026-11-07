# Scaling benchmark

Original model SHA-256: `1395072cf94608a7d202ced6a66dfec9bdcda9f3a3ac2c857a477d8917f3169b`.

Each command has its own wall-clock timeout. Timed-out or failed commands have no verified outcome. Heap values are JVM caps, not measurements of peak process memory. Native solver allocations are additional.

Scopes bound available SPC atoms. Only the separately named exact-route witnesses require the active route to reach the boundary. These witnesses demonstrate existence, not general initialised reachability.

Representation: `ordered`. In sequence mode the route and histories share a sequence bound. Ordered mode uses the selected independent history bound. All results remain finite-scope evidence.

| SPC bound | seq | Int bits | Command | Expected | Observed | Status | Seconds | Validated |
|---|---|---|---|---|---|---|---|---|
| 1000 | 4 | 5 | InitialIsValid | UNSAT | UNKNOWN | timed_out | 90.127 | no |
| 1000 | 4 | 5 | ShowFullRouteWithTraffic | SAT | UNKNOWN | timed_out | 91.652 | no |

Per-command directories retain generated sources, execution metadata, raw logs and all available Analyzer evidence.
