# Unit 16 production worklog

## Boundary

Unit 16 is a complete verified internal checkpoint in the Units 16–18
production batch. The latest public cumulative boundary remains Unit 15;
there is intentionally no per-unit external publication transaction.

## Authority and rights

The immutable source closure is documented in
`authority/UNIT_16_AUTHORITY_FREEZE.md`. Its manifest binds lecture revision
1060232, worksheet revision 1067952, 258 captured transclusions, 23 exercises,
the only six public source solutions, both official PDFs, and 43 exact files.

Four Commons reader positions are frozen locally: three lecture images and
the `Draft0.svg` sketch in public Solution 16.12. The rights ledger records
three CC BY-SA 3.0 components and one public-domain component, while the
translated course text remains CC BY-SA 4.0. The Commons SVG thumbnail's
reported 500-by-500 size differs from its decoded 500-by-501 pixels; exact
returned bytes and both dimensions are retained.

## Indonesian production

- `source/id-ID/lecture-16.md`: 16,456 bytes, SHA-256
  `c7cb0a1bc34e2003db18024d206c87d522a8df2082d186456d7a987cf0775d39`.
- `source/id-ID/worksheet-16.md`: 11,252 bytes, SHA-256
  `871ea30f571ebc9e0e2a7b1e4d30cddfe719822f48b2bdbe97bd6d8a52a5268a`.
- `source/id-ID/worksheet-16-solutions.md`: 9,286 bytes, SHA-256
  `5df1b9f46ba65622644feed0bf99191d5737d2edc2cc887c3b00efd2b50f8860`.
- `source/id-ID/media-credits-unit-16.md`: 1,316 bytes, SHA-256
  `4a5bc83795b780ad26bffe425924bb010b966ed49dcbd0c3b073bc3be77f7a99`.

The unit preserves all 23 exercises, all six frozen public solutions, stars,
points, source order, four media positions, 53 unique stable IDs, and exact
provenance `OpenAI Codex gpt-5.6-sol, Ultra.` No missing solution was invented;
the source stopping point of Solution 16.13 is explicit.

## Source corrections and QA

Six ledgered source deltas are disclosed in place:

- `AGC-CORR-0034` restores $U_i\subseteq X$ in the morphism pullback diagrams.
- `AGC-CORR-0035` restores the defined coordinate $(bx+ay)^2$ in Solution 16.11.
- `AGC-CORR-0036` restores the three-axis decomposition in Solution 16.12.
- `AGC-CORR-0037` restores the substitution sign in Solution 16.12 without
  changing the generated ideal.
- `AGC-CORR-0038` records that public Solution 16.13 omits the problem's
  two-point-fiber clause.
- `AGC-CORR-0039` restores $f=g_i/h_i$ in Soal 16.23 after the source prints
  an undefined $q$.

`qa/UNIT_16_TRANSLATION_QA.json` reports PASS. It is 4,373 bytes with SHA-256
`02ff081cd808172438262846944763e25871f6805a6a6f59bee933e3bf1fda19`.
The gate replays every authority/media/PDF hash, solution topology, rights,
source/control identity, Pandoc AST, stable IDs, terminology, protected
mathematics, all six correction bindings, language residue, placeholders,
and secret-like strings.

Next executable action: freeze Unit 17's exact lecture/worksheet revisions,
transclusions, exercise/solution topology, official PDFs, media, and rights;
then translate it contiguously. After Unit 18, run the next full cumulative
reader/backend/common-adapter/release/public-readback cycle.
