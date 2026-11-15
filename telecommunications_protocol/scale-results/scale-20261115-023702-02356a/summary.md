# Scaling benchmark

Original model SHA-256: `1fa2fa4556b3ce3fec9d4286ba6b5d986bd1d2cd51192b381493f363c1b04181`.

Each command has its own wall-clock timeout. Timed-out or failed commands have no verified outcome. Heap values are JVM caps, not measurements of peak process memory. Native solver allocations are additional.

Scopes bound available SPC atoms. Only the separately named exact-route witnesses require the active route to reach the boundary. These witnesses demonstrate existence, not general initialised reachability.

Representation: `ordered`. In sequence mode the route and histories share a sequence bound. Ordered mode uses the selected independent history bound. All results remain finite-scope evidence.

External SAT solvers (Kissat, CaDiCaL) decide only UNSAT-expected checks from Alloy's CNF export. Witnesses and the expected bug use a built-in Alloy solver so their instances can be validated.

| SPC bound | seq | Int bits | Command | Solver | Expected | Observed | Status | Seconds | Validated |
|---|---|---|---|---|---|---|---|---|---|
| 10 | 4 | 5 | DaemonIsInvisible | glucose | UNSAT | UNSAT | completed | 136.196 | yes |
| 10 | 4 | 5 | DaemonPreservesInvariant | glucose | UNSAT | UNSAT | completed | 79.033 | yes |
| 10 | 4 | 5 | InitialIsValid | glucose | UNSAT | UNSAT | completed | 1.573 | yes |
| 10 | 4 | 5 | InsertionIsInvisible | glucose | UNSAT | UNSAT | completed | 18.047 | yes |
| 10 | 4 | 5 | InsertionPreservesInvariant | glucose | UNSAT | UNSAT | completed | 15.533 | yes |
| 10 | 4 | 5 | ReceivePreservesInvariant | glucose | UNSAT | UNSAT | completed | 27.028 | yes |
| 10 | 4 | 5 | ReceiveRefinesExternal | glucose | UNSAT | UNSAT | completed | 76.150 | yes |
| 10 | 4 | 5 | RetrieveIsValid | glucose | UNSAT | UNSAT | completed | 160.153 | yes |
| 10 | 4 | 5 | TransmitPreservesInvariant | glucose | UNSAT | UNSAT | completed | 16.009 | yes |
| 10 | 4 | 5 | TransmitRefinesExternal | glucose | UNSAT | UNSAT | completed | 11.391 | yes |

Per-command directories retain generated sources, execution metadata, raw logs and all available Analyzer evidence.
