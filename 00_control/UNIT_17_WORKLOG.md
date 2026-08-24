# Unit 17 production worklog

## Boundary

Unit 17 is a complete verified internal checkpoint in the Units 16--18
production batch. The latest public cumulative boundary remains Unit 15;
there is intentionally no per-unit external publication transaction.

## Authority and rights

The immutable source closure is documented in
`authority/UNIT_17_AUTHORITY_FREEZE.md`. Its manifest binds lecture revision
1112301, worksheet revision 1068111, 249 captured transclusions, 39 exercises,
the only four public source solutions, both official PDFs, and 38 exact files.
It is 116,257 bytes with SHA-256
`c6747335c58fb3b4303cf3095705df7f991143f79d2d3598582a1cc8c99bef1a`.

There are no substantive reader-media positions. The empty-header rights
ledger is 443 bytes with SHA-256
`6b8de6f5a63f32d9f22e7fb69c98ba2d787121a2437a392602571504c2a1c544`.
The 3,013-byte closure, SHA-256
`87c3d88789d822210b388e0c21e0e25a7418e77930e245ab2bc32916a0508d4f`,
binds the two official PDF witnesses and their CC BY-SA 4.0 component rights.

## Indonesian production

- `source/id-ID/lecture-17.md`: 15,109 bytes, SHA-256
  `53bdc1f91f02a4b28dcc0c78247ef2ab9f5102377d8d0b6eedc88ed6879f37e8`.
- `source/id-ID/worksheet-17.md`: 15,940 bytes, SHA-256
  `2ec3c00332fad5683d56d9a608bf6544371732207312c4dc77c479621624efa0`.
- `source/id-ID/worksheet-17-solutions.md`: 5,104 bytes, SHA-256
  `5a56a15a9cb38ef4859a53ccd690309965c22a1fef54b018f162ec12fac6adef`.
- `source/id-ID/media-credits-unit-17.md`: 451 bytes, SHA-256
  `2647366a9bad10aff220f263a3a9c14d3620c43b42c0b4d2195e0c38d263f537`.

The unit preserves all 39 exercises, all four frozen public solutions, stars,
submitted-work points, source order, 71 unique stable IDs, and exact provenance
`OpenAI Codex gpt-5.6-sol, Ultra.` No missing solution was invented.

## Source corrections and QA

Six ledgered source deltas are disclosed in place:

- `AGC-CORR-0040` keeps the lecture's established monomial notation $X^m$
  after the source unexpectedly prints $T^m$ in the group-completion bridge.
- `AGC-CORR-0041` restores the commutative-group hypothesis declared by the
  Exercise 17.10 entity and required by the commutative monoid-ring context.
- `AGC-CORR-0042` restores the omitted coefficient modules in
  $R[I]=\bigoplus_{m\in I}RT^m$.
- `AGC-CORR-0043` replaces an invalid all-exponents claim in public Solution
  17.12 by the sufficient coefficient-of-$T^0$ argument.
- `AGC-CORR-0044` restores the final support index $b_{r_m}$ in public
  Solution 17.31.
- `AGC-CORR-0045` restores the type-correct intertwining identity
  $\varphi\circ\rho(g)=\rho(g)\circ\varphi$ in Exercise 17.39.

`qa/UNIT_17_TRANSLATION_QA.json` reports PASS. It is 3,630 bytes with SHA-256
`738a9d27d620c55770e17a0bcb089ae756cfa632262074a94f02393498a1d8be`.
The gate replays every authority/PDF hash, solution topology, rights and
source/control identity; validates the Pandoc AST, stable IDs, terminology,
protected mathematics, all six correction bindings, language residue,
placeholders, invisible Unicode, and secret-like strings.

Next executable action: freeze Unit 18's exact lecture/worksheet revisions,
transclusions, exercise/solution topology, official PDFs, media, and rights;
translate it contiguously; then build and publish the verified cumulative
Units 1--18 reader/backend milestone and anonymously read back every public
byte.
