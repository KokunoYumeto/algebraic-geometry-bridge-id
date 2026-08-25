# Unit 21 owner-production worklog

## Boundary

Unit 21 is a complete, independently owner-verified internal source
checkpoint. It extends the contiguous Indonesian source through Lecture 21
and Worksheet 21 without changing the published Units 1--18 bytes. Together
with the verified internal Units 19--20 checkpoint it is the terminal source
input for the substantial cumulative Units 1--21 reader, backend, and release
cycle.

## Frozen authority and rights

- Lecture page 165910, revision 1112312, MediaWiki SHA-1
  `05c51f6e29f6ec12aef400195396ca517924b094`; 122 captured
  transclusions.
- Worksheet page 165940, revision 1062605, MediaWiki SHA-1
  `38a7856a5df3695eb80874194bc043dda3377f90`; 144 captured
  transclusions.
- `authority/wikiversity/unit-21/UNIT_AUTHORITY_MANIFEST.json`: 142,834
  bytes, 54 bound local files totaling 848,227 bytes, SHA-256
  `d85444ddfc66c8e77d52db3f3abc0a186e5dd598789edaaf890b3c09cf00f923`.
  Independent replay verified those 54 files, five bounded external files,
  223 final Wikiversity identities, and two final Commons PDF identities
  without mismatch.
- The worksheet contains 26 ordered exercises. Exercises 1--21 are practice;
  Exercises 22--26 carry 4, 4, 4, 3, and 3 points. Public source solutions
  exist only for Exercises 3 and 8, at revisions 1068126 and 1113184. They
  are complete bodies rather than wrappers; their recursive closures contain
  9 and 17 pages. No other solution is admitted.
- Unit 21 has zero substantive reader-media positions and zero binary media
  assets. `authority/RIGHTS-unit-21.csv` is 443 bytes, SHA-256
  `6b8de6f5a63f32d9f22e7fb69c98ba2d787121a2437a392602571504c2a1c544`;
  `authority/ASSET_CLOSURE-unit-21.json` is 5,705 bytes, SHA-256
  `8708a399d7c950101609281c14fe4e48eb02aa70335a7ad6cf7ef4194e9bc483`.
- Official lecture PDF: 189,481 bytes, 7 pages, SHA-256
  `12c5dd813cd7d574aaeca33c02dbab1f8cbc4de131030c31dd9eba4007e14ebd`.
  Official worksheet PDF: 155,433 bytes, 7 pages, SHA-256
  `5457b23d9e4dfb6054fa0cdd1d7c823440307ed4d4710a9af244573b8bf89440`.
  Internal CC BY-SA 3.0 boilerplate is preserved as provenance against the
  current CC BY-SA 4.0 course/Commons component records.
- The amended `authority/UNIT_21_AUTHORITY_FREEZE.md` is 5,585 bytes,
  SHA-256
  `d60f85cc2f8394ca5c1735e9ecf0424c883036c4e2a8ab6ae5271daacf8bffc7`.

## Complete Indonesian source

- `source/id-ID/lecture-21.md`: 17,276 bytes, SHA-256
  `4bfbb794483fdc0466acda10c7e63fa09891ad8da435888b2b59a0e051c7b8a6`.
- `source/id-ID/worksheet-21.md`: 14,505 bytes, SHA-256
  `9fe5a9e27c5de0b17ec1e0512c1d4368d21ad886c7bc5f4d4a27b6a27bf089f9`.
- `source/id-ID/worksheet-21-solutions.md`: 5,662 bytes, SHA-256
  `e872b5002fa8bf278e907b8247a74a23f9efb09eeba1f4610df655dd5d25c4bc`.
- `source/id-ID/media-credits-unit-21.md`: 935 bytes, SHA-256
  `e4076d9aa394dd6901e49dd9c73216eb80d8f0938ea7571f4d6cc30d87e44f67`.
- Cumulative frontmatter `source/id-ID/frontmatter-units-01-21.md`: 3,370
  bytes, SHA-256
  `560b34060b3a2dc083d5a97238483c3f542c2928db9a435df63cea4db5d1c7aa`.

The unit preserves all 13 lecture entities, all 26 exercise entities, both
and only both frozen public solutions, exact stars and submitted-work points,
48 unique source/control IDs, no reader images, and exact provenance
`OpenAI Codex gpt-5.6-sol, Ultra.`

## Corrections, bridges, terminology, and QA

Six genuine source defects are visibly corrected and bound as
`AGC-CORR-0062` through `AGC-CORR-0067`: the positive-monomial ideal index;
the nonzero-sum domain proviso for order/valuation; the field hypotheses in
Exercise 6; the root premise in Exercise 12; the suppressed theorem scope in
the Nakayama transition; and the unquantified exponent in Exercise 20.
Three additive, visibly labeled `Jembatan edisi` entries are bound as
`AGC-CORR-0068` through `AGC-CORR-0070`: a self-contained prime-ideal lemma,
the quotient step in the DVR characterization, and the Nakayama generator
corollary. They do not masquerade as source text or supply exercise solutions.

An earlier audit suspected an `S`/`R` inconsistency in Lemma 21.7. Exact
replay disproved it: generic statement page 15866/revision 1088079 and proof
page 15870/revision 1086502 both parameterize the ring as `R`, while enclosing
page 95386/revision 944013 passes `R=S`; expanded TeX and rendered HTML use
`S` throughout. No false correction note was admitted.

Eighteen new terms are admitted as `AGT-0150` through `AGT-0167`.
`00_control/TERMINOLOGY.csv` is 25,187 bytes with SHA-256
`db3184ec04fe01f6712e46b3b7b36131f1a5838574e3dd07d6bdc36d02493590`;
`00_control/CORRECTIONS.csv` is 46,027 bytes with SHA-256
`ae31d9a7ef70c031e84e524dc129454705b1fa87d8a21a91bc3dc631949a39bc`.

`qa/UNIT_21_TRANSLATION_QA.json` reports PASS. It is 5,436 bytes with
SHA-256
`a999af2ab40124cbe8bb593239ce17b9e99515d70253ac1869f2934426a7ff75`.
The independently rerun fail-closed gate replays authority, solutions,
rights, PDFs, source, ledgers, freeze, identities, exercise topology, 48 IDs,
28 protected mathematical surfaces, all correction/bridge disclosures, and
Pandoc ASTs with zero warnings, visible German residue, placeholders,
invisible controls, or secret-like strings.

Next executable action: build, visually inspect, backend-export, package,
publish, and anonymously read back the cumulative Units 1--21 checkpoint in
the existing GitHub and Zenodo lineages. After verification, advance the
source cursor to Unit 22.
