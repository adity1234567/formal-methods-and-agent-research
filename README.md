# Formal methods and agent research

This repository contains two parts of a coursework and research workspace:

- **Telecommunications Protocol in Alloy:** a model and explanation of Chapter 20
  of Woodcock and Davies' *Using Z*, with presentation notes, verification tools,
  and saved Analyzer evidence.
- **Bangla-English agent research notes:** feedback on a proposed multilingual
  agent reliability study and a survey of relevant dataset resources.

## Start here

| Material | File |
| --- | --- |
| Alloy project explanation and setup | [Project README](telecommunications_protocol/README.md) |
| Executable model | [telecommunications.als](telecommunications_protocol/telecommunications.als) |
| Presentation outline and speaking notes | [Presentation notes](telecommunications_protocol/presentation_notes.md) |
| Current verification report | [Verification summary](telecommunications_protocol/results/verification_summary.md) |
| Guide to current and historical runs | [Results guide](telecommunications_protocol/results/README.md) |
| Completed project review | [Audit report](telecommunications_protocol/audit_report.md) |
| Research feedback and dataset availability | [Research PDF](output/pdf/research_feedback_and_datasets.pdf) |
| Research PDF generation script | [generate_research_pdf.py](scripts/generate_research_pdf.py) |

The research PDF contains planning advice and dataset references. It does not
report completed Bangla-English agent experiments. Dataset availability and
coverage should be checked again before conducting a study.

## Run the Alloy project

Install Python 3.10 or later and Java suitable for Alloy 6.2.0. Download the
Alloy JAR from the [official 6.2.0 release](https://github.com/AlloyTools/org.alloytools.alloy/releases/tag/v6.2.0)
and save it as `telecommunications_protocol/tools/alloy-6.2.0.jar`.

From the repository root:

```shell
cd telecommunications_protocol
python -m unittest -v test_verification
python verify.py
```

The unit tests use committed historical evidence and do not require the JAR.
Running `verify.py` requires Java and the JAR, creates a new execution directory,
and updates the verification reports. For the pure Java solver, use
`python verify.py --solver sat4j`.

The saved evidence supports the stated finite scopes. It is not an unbounded
proof or a complete implementation of SS7. Consult the project README and
verification summary for the model's assumptions and limitations.

## Regenerate the research PDF

From the repository root:

```shell
python -m pip install -r scripts/requirements-pdf.txt
python scripts/generate_research_pdf.py
```

The script writes the PDF to `output/pdf/` and page previews to the ignored
`tmp/pdfs/` directory.

## External reference material

The textbook, reproduced chapter text and page images, downloaded Alloy JAR,
temporary previews, and duplicate ZIP archive are kept outside Git. Source
links and reference notes are available in the
[reference guide](telecommunications_protocol/references/README.md).
Saved results, including explicitly labelled incomplete and historical runs,
are retained so the evidence and regression tests can be inspected.
