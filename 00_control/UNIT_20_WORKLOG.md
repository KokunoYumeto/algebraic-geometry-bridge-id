# Unit 20 owner-production worklog

## Boundary

Unit 20 is a complete, independently owner-verified internal source checkpoint.
It extends the contiguous Indonesian source through Lecture 20 and Worksheet
20 without changing the published Units 1--18 reader, backend, or release
bytes. Under the substantial-milestone cadence, it will be folded into the
cumulative Unit 21 build and publication rather than released alone.

## Frozen authority and rights

- Lecture page 165909, revision 1112311, MediaWiki SHA-1
  `74eb303dc659cb8131aaaee6948962210f063f4e`; 118 captured transclusions.
- Worksheet page 165939, revision 1062603, MediaWiki SHA-1
  `97db112f709b6ab16f89b88f6d4e3da127c7802a`; 120 captured transclusions.
- `authority/wikiversity/unit-20/UNIT_AUTHORITY_MANIFEST.json`: 129,387
  bytes, 56 bound files, SHA-256
  `b063e5edc556cd18598389083ea27ea7f255edfe2ae00e13ebf24de76e5b37d7`.
  The final entry-revision check and an independent byte/hash replay passed.
- The worksheet contains 23 ordered exercises. Exercises 1--18 are practice;
  Exercises 19--23 carry 3, 6, 5, 4, and 2 points. Public source solutions
  exist only for Exercises 1, 3, 4, 5, 12, 13, 14, and 17. Wrapper solutions
  1 and 4 include the complete separately frozen proof bodies.
- The exact Commons original `authority/assets/Whitney_unbrella.png` is
  35,829 bytes with SHA-256
  `5a469c4675d326a753dca7801524138e64689e476d38d867070f97983f8b07d2`.
  Claudio Rocchini's explicit CC BY 2.5 option governs reuse. The source's
  incompatible `CC-BY-SA-2.5` label is retained only as a documented
  discrepancy.
- `authority/RIGHTS-unit-20.csv`: 2,024 bytes, SHA-256
  `09b85688b10784cf2c7e7aec9d017eb4d0403faf0b96ef8561b789168d19f565`.
  `authority/ASSET_CLOSURE-unit-20.json`: 4,809 bytes, SHA-256
  `5ab57774999d4f293533a8fb14ad4e50d6caa1fba3d2664428c32d15f935c185`.
- Official lecture PDF: 217,144 bytes, 7 pages, SHA-256
  `f9ee520ac2724e041eb8861e4648e59e6357b71d68bf73e7a634a91178d45f9a`.
  Official worksheet PDF: 164,793 bytes, 5 pages, SHA-256
  `d141d76231053dabe89e4af0113e080abd57ee7f7dfc74877bcaa7ad4d48ec9d`.
  Their internal CC BY-SA 3.0 boilerplate is recorded against the current
  CC BY-SA 4.0 course/Commons component status.

## Complete Indonesian source

- `source/id-ID/lecture-20.md`: 16,602 bytes, SHA-256
  `ccedeb464364a71f98f7450359ec6baa2c5135651e9e6e098de2772bf337ce66`.
- `source/id-ID/worksheet-20.md`: 10,529 bytes, SHA-256
  `50418f12f8f620736db8a6c9689902addc21308ebd4a0ebccfc18266a4156a99`.
- `source/id-ID/worksheet-20-solutions.md`: 12,722 bytes, SHA-256
  `2b1d9e9bee2c9285b50c52128d20a4e769379ccb51193192bdf9567ca16d064a`.
- `source/id-ID/media-credits-unit-20.md`: 794 bytes, SHA-256
  `02c00101d4e11df536c49ec6ffcaedc2f4a03215e867daa86c6bb81686704f1a`.

The unit preserves 13 lecture entities, all 23 exercise entities, all eight
and only eight frozen public solutions, both wrapper-proof dependencies, one
accessible local figure, 58 unique stable IDs, all stars and points, and exact
provenance `OpenAI Codex gpt-5.6-sol, Ultra.`

## Corrections, terminology, and QA

Seven source deltas are disclosed in the reader and bound as
`AGC-CORR-0055` through `AGC-CORR-0061`: the Whitney coordinate, `rm` set
membership, coefficient-ring switch, solution product index, exponent versus
monomial membership, integral-equation variable, and unnamed functionals in
the Exercise 20.18 cross-reference. None changes a source problem's requested
scope or invents a solution.

Ten newly required terms are admitted as `AGT-0140` through `AGT-0149`.
`00_control/TERMINOLOGY.csv` is 22,469 bytes with SHA-256
`61c5ef9da1bafb922a6dda68334550f09f59dffc239963010158b531e287d7b7`;
`00_control/CORRECTIONS.csv` is 40,697 bytes with SHA-256
`1fd95ef7745746e26575870575f6148ddb01fecdfbbfeb5c288ae55dfb8a86d9`.

`qa/UNIT_20_TRANSLATION_QA.json` reports PASS. It is 3,748 bytes with
SHA-256
`6c4bc4eb66feccf91d0d53f81c08726857a6edb3dbee93b66b0487b83a4b2725`.
The fail-closed gate replays all 56 authority files and both PDFs; verifies
the exact source, control, media, exercise, solution, wrapper, rights, link,
and attribution identities; parses all four Markdown files with no Pandoc
warning; checks 58 stable IDs, 434 math AST nodes, 20 protected mathematical
surfaces, terminology, disclosures, language residue, placeholders,
invisible Unicode, and secret-like strings.

Next executable action: freeze, translate, and per-unit verify Unit 21 in
source order. Then build, visually inspect, backend-export, package, publish,
and anonymously read back the cumulative Units 1--21 checkpoint in the
existing lineages.

