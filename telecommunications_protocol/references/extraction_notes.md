# Reading the source extract

The source PDF, chapter extraction, and page images described below are local
review materials and are excluded from the public Git repository. The
[reference guide](README.md) links to the source publication.

`chapter20_extracted.txt` is raw text extracted from the accompanying
`Using_Z_Woodcock_Davies.pdf`. During the review on 3 November 2026, regenerating
that text from the PDF produced the same contents. It has been retained without
editorial changes.

The chapter occupies PDF pages 335–343, corresponding to printed pages 321–329.
The extract also includes the marker for blank PDF page 344. The PDF remains
the source for interpreting mathematical layout, schema boxes, and notation.
Text extraction flattens that layout and can make a formula ambiguous.

The implementation makes these choices explicit:

- The displayed insertion formula on printed page 328 contains `rec i + 1`.
  It is read as `rec(i+1)`, the next section's received history. The prose and
  the types support this interpretation; `rec(i) + 1` would add an integer to
  a sequence. This ambiguity exists in the printed notation too.
- The successful `Daemon0` schema on printed page 325 specifies queue changes.
  The Alloy implementation also spells out the necessary received/sent history
  updates and fixes the route. These explicit frame conditions implement the
  intended movement of one message to its neighbour.
- The printed sectional receive describes successful delivery. The Alloy
  `receivePoll` wrapper adds an unconditional stuttering choice. The successful
  operation is retained separately as `receive`; the wrapper is an explicit
  modelling completion, not a literal transcription of that schema.

Source: Jim Woodcock and Jim Davies, *Using Z: Specification, Refinement, and
Proof*, Prentice Hall International, 1996, Chapter 20.

Public PDF: https://dsc.ufcg.edu.br/~dalton/bib/woodcock96.pdf

PDF SHA-256: `cd39e5de41630dfdb7c8a4f73965c97f2437ed9b1cfbc9321247d6f900a33973`
