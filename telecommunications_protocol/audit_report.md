# Completed project review

Review completed: **4 November 2026**.

The Alloy model, source interpretation, explanation, presentation notes,
verification tools, saved results, and package contents were reviewed. No
protocol-logic error was found in the correct transmit, receive, forwarding,
or insertion operations. The following issues and gaps were corrected.

| Finding | Correction |
|---|---|
| The old verifier copied and hashed the live model after analysis; later edits could be associated with earlier results. | Each new run saves the source before launching Alloy and analyses that copy. Reporting validates its recorded hash and separately identifies whether the live file matches. |
| Interrupted or failed runs could leave an earlier PASS or example report visible. | Logs are saved during execution; completion/failure/interruption is recorded. Incomplete executions produce an explicit incomplete report and replace stale example claims. |
| The old summary did not sufficiently cross-check log, receipt, scopes, and saved examples. | It checks command order and identities, expected results, receipt source/scopes, completion status, overflow settings, and SAT XML files. |
| The XML reader could turn a malformed indexed relation into an apparently valid list. | Missing, repeated, negative, or nonfunctional indices and missing fields are rejected. Demonstration data is validated before the tables are written. |
| Some notes called isolated valid transitions “reachable.” | They now distinguish transition satisfiability from paths that explicitly begin with initialisation. |
| Queue/history terminology and the scope limit could be misread. | The notes distinguish two histories from a pending queue and explain that `4 seq` bounds the recorded lifetime history, including delivered messages. |
| The insertion example did not require a nonempty history at the inserted boundary. | Its predicate now requires both pending traffic and a nonempty shared history, exercising the new section's inherited history. |

The notes also clarify the valid-before-state contract of sectional operations,
the explicitly added stuttering wrappers, and the difference between sectional
preservation checks and the abstract schemas' invariant constraints.

## Validation completed

- Source review used Chapter 20 of the locally downloaded source PDF, including visual
  inspection of the daemon and refinement-obligation schemas. The raw chapter
  extract matches text regenerated from that PDF. Its notation limitations are
  recorded in [extraction_notes.md](references/extraction_notes.md).
- The reviewed model has completed analysis with all **18 expected outcomes**:
  ten checks without a counterexample in scope, seven satisfiable examples,
  and the expected counterexample for the isolated intentional bug.
- On 4 November 2026, the selected completed run's evidence was revalidated
  using the corrected verifier. The selected run completed on 3 November 2026;
  it is `run-20261103-215246-91a68f`. Its saved model matches the workspace.
- **14 regression tests passed** for the verification/reporting utilities.
  They cover live-source edits, saved-source modification, duplicate/missing
  results, mismatched receipt scopes, missing witnesses, malformed sequences,
  launch failure, and interruption handling.
- Local Markdown links and the reviewed package's file contents were checked.

Reviewed model SHA-256:
`47d76e1f6c80954afd8b2ea0607486f4a410a80298a5d7bfd98573c4ade47621`

The authoritative command-by-command evidence is in
[verification_summary.md](results/verification_summary.md).
The open `preliminary-aborted/receipt.json` file is historical, incomplete output;
see [the results guide](results/README.md).

These checks support the stated finite model. They do not establish unbounded
correctness, eventual delivery, or implementation of the complete SS7 standard.
