# Reading the results

Start with [verification_summary.md](verification_summary.md). It identifies
the selected completed execution, reports the source hash, and states whether
the workspace model matches that saved source. The
[example tables](example_instances.md) come from that same execution.

At completion of the review on 4 November 2026, the selected execution is
`run-20261103-215246-91a68f`, completed on 3 November 2026. Its 18 commands match
all declared expectations. The evidence was revalidated during the review;
the model did not need another identical solver run.

Each `run-*` directory preserves its own model, execution metadata, log, and
available Analyzer outputs. Later-format runs put their receipt and XML files
in an `alloy` subdirectory. Older runs store them directly in the run directory.

`preliminary-aborted/receipt.json` belongs to an unfinished early analysis. It
does not certify the final model. Its neighbouring README documents why it was
stopped. The oldest completed run is also retained as the input fixture for
`test_verification.py`; tests mutate temporary copies rather than these files.

A SAT result is expected for the seven example runs and the deliberately
broken receive check. UNSAT is expected for the ten checks of the correct model.
These results apply to the finite scopes shown in the summary.
