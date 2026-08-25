# Unit 23 owner-production worklog

## Boundary

Unit 23 is a complete, independently owner-verified internal source
checkpoint. It extends the contiguous source through Lecture 23 and Worksheet
23 without changing accepted Units 1--22 or the public Units 1--21 bytes. It
is the second of the three source units for the substantial Units 1--24
reader, backend, and publication cycle; no per-unit external publication
transaction has been started.

## Frozen authority and rights

- Lecture page `165912`, revision `1112318`, MediaWiki SHA-1
  `a38160a106cf39298b3f2cb23f7880e05a5a86f7`; its recursive parser closure
  contains 142 exact identities from 142 occurrences. The 141 case-folded
  comparison keys reflect one genuine case-sensitive title pair, not a missing
  page.
- Worksheet page `165942`, revision `1062659`, MediaWiki SHA-1
  `19554b41098b4f02ac6e558145036ca293e4bbc9`; its recursive parser closure
  contains 102 exact identities from 102 occurrences. The 101 case-folded
  comparison keys likewise retain one genuine case-sensitive title pair.
- `authority/wikiversity/unit-23/UNIT_AUTHORITY_MANIFEST.json`: 161,310
  bytes, SHA-256
  `f7ee49a4bfa589b831c1fdb69e6f091ac1762d9da019a133670e4e0d723d34ae`.
  Final replay verified 208 Wikiversity revision identities and both Commons
  PDF identities without mismatch.
- The worksheet contains 12 ordered exercises: practice Exercises 1--7 and
  submitted Exercises 8--12. Displayed submitted points are 4, 3, 5, 5, and 3
  (total 20). Only Exercises 4 and 5 have public source solutions, at revisions
  `1090216` and `1096444`; their recursive closures contain 19 and 13 exact
  identities. No other solution was invented or admitted.
- The substantive reader-media closure is empty. The header-only
  `authority/RIGHTS-unit-23.csv` is 443 bytes, SHA-256
  `6b8de6f5a63f32d9f22e7fb69c98ba2d787121a2437a392602571504c2a1c544`;
  `authority/ASSET_CLOSURE-unit-23.json` is 33,083 bytes, SHA-256
  `d6bd0435e6c24d3085e8b4282d89bc263c4957b699d92d5c8409f7c16a43da64`.
- Official lecture PDF: 191,471 bytes, seven pages, SHA-256
  `96fc99009c2f4640ba99db6203c06bd59e03bdc2927c1bf81302625431302724`.
  Official worksheet PDF: 159,393 bytes, five pages, SHA-256
  `6494630aba1d79f238c762b30cb382918444b19a82de3d96d66c4d6e3108d15b`;
  page 4 is genuinely blank. Both are untagged witnesses rather than current
  semantic clones.
- `authority/UNIT_23_AUTHORITY_FREEZE.md`: 4,776 bytes, SHA-256
  `353d0b922f69caf330571a271c2ca6bf5c031c27062f82366ab01b87dd475c36`.
  `qa/UNIT_23_AUTHORITY_QA.json` reports deterministic PASS and is 2,366
  bytes, SHA-256
  `6a55326eec4079a0000dcc7d449e92e9213254b2b16a8400ed7b784b200805ac`.

## Complete Indonesian source

- `source/id-ID/lecture-23.md`: 16,697 bytes, SHA-256
  `8f143de32c72078c7d9e09d5a9837584589068740d7702f857ec4183047c82ed`.
- `source/id-ID/worksheet-23.md`: 8,157 bytes, SHA-256
  `011f5bb26e81002d262ffe0425ad290bdb2a287cb88864f080ea46554d2c8b19`.
- `source/id-ID/worksheet-23-solutions.md`: 4,580 bytes, SHA-256
  `d817803e00f5df55473330608847a4664845c67c1319bbd73c12f1d5dd1bb939`.
- `source/id-ID/media-credits-unit-23.md`: 1,131 bytes, SHA-256
  `bef7b4083c04fb72e7b17ad27657a730f8d48b72317714478489d6ebd3c74553`.

The source preserves all 17 lecture components, all 12 exercises, both and
only the two frozen public solutions, exact stars and submitted-work points,
42 unique source/control IDs, and exact provenance
`OpenAI Codex gpt-5.6-sol, Ultra.` All four Markdown files parse through
Pandoc. Their ASTs contain 42 headers, 327 math nodes, and zero images.

## Corrections, terminology, and verification state

Six source repairs are visibly disclosed and bound as `AGC-CORR-0077` through
`AGC-CORR-0082`: explicit quotient classes modulo `m^2`; a positive conductor
bound and `M_+` summands; monomial-ideal rather than false monoid-ring
notation; the uniform localized nilpotence condition and finite field product
in Exercise 11; the correct degree bound and cancellation-safe lowest-term
argument in Solution 4; and the corrected index plus vector-space basis in
Solution 5. Upstream authority bytes remain unchanged.

Eleven terms are admitted as `AGT-0182` through `AGT-0192`, including
`derivasi`, `aturan Leibniz`, `multiplisitas Hilbert-Samuel`, `dimensi Krull`,
`rantai ideal prima`, `ideal monoid`, and `dekomposisi homogen`.
`00_control/TERMINOLOGY.csv` is 29,219 bytes, SHA-256
`f4c115caaad530456c541d61bb9b7567226869437cd5ceab2ebf29951731e12e`;
`00_control/CORRECTIONS.csv` is 54,444 bytes, SHA-256
`d1b1fae8c947773eb9ed6e3a027d139b4c1b4f03af80e543bb5f88ee15b19737`.

An independent read-only mathematical/source-order audit passed the complete
lecture, worksheet, public-solution boundary, 42-link/ID closure, and all six
repairs. `scripts/qa_unit23_translation.py` is 31,947 bytes, SHA-256
`a04e30fc40d5b9f47707d490740436475a97d6ca659d81574a5aca218d86b419`.
Two consecutive executions produced the identical PASS receipt
`qa/UNIT_23_TRANSLATION_QA.json`: 5,842 bytes, SHA-256
`f0acd4d9693492c995f74db28e5d5f35833f25213181a514252409c64c097d9a`.
The fail-closed gate replays the frozen authority and rights, exact primary
and solution identities, all source/control hashes, complete exercise and
solution topology, 42 unique IDs, protected mathematical surfaces, the six
visible corrections, terminology rows, and all four Pandoc ASTs. It reports
zero warnings, German residue, placeholders, invisible controls, disallowed
Unicode dashes, or secret-like strings.

## Next executable action

Advance to the already bounded official 2012 Unit 24 authority. Translate its
lecture, ten exercises, and sole public Solution 24.4 with the three mandatory
live-source repairs, then execute the cumulative Units 1--24 reader/backend/
publication cycle. Do not alter accepted Units 1--23 or start an external
transaction before the Unit 24 milestone.
