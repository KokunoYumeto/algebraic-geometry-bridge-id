# Unit 18 production worklog

## Boundary

Unit 18 is a complete verified internal checkpoint and closes the Units
16--18 translation batch. The latest public cumulative boundary remains Unit
15 until the deterministic cumulative Units 1--18 reader/backend build,
visual QA, release, and anonymous public-byte readback finish.

## Authority and rights

The immutable source closure is documented in
`authority/UNIT_18_AUTHORITY_FREEZE.md`, 2,860 bytes, SHA-256
`8154a612a53cba1f738a18d04d9893e8db455f4add1c2ae443311a5af52a20a4`.
Its manifest binds lecture revision 1051383, worksheet revision 1062146, 227
captured transclusions, 28 exercises, the only five public source solutions,
both official PDFs, and 39 exact files. The manifest is 106,298 bytes with
SHA-256
`26a56a0ccad60414bf09320dc008d438ccf84b3dd11c12c31e80fa6088437033`.

One substantive reader figure is frozen locally. The component-rights ledger
is 1,998 bytes with SHA-256
`8cbf29b0063c2463fe89f9dec67bda671f9ee366db2c91176e37d4ef3532fbb0`;
the 4,025-byte closure has SHA-256
`69bfe604847dbb57fa21e07f8308901f02b87fba92c668b2b0fec27e3c2e8ad3`.
The Wikiversity inline PD label conflicts with the current frozen Commons
description; the edition binds the figure to the Commons CC BY-SA 3.0 option,
credits Georg-Johann, and makes no public-domain claim.

## Indonesian production

- `source/id-ID/lecture-18.md`: 14,716 bytes, SHA-256
  `319cca4f08a3a4ee0bf0fa2a9d525e0adcd2f6f639705dd1c2eb06580b7bfcd3`.
- `source/id-ID/worksheet-18.md`: 14,530 bytes, SHA-256
  `ec760a90d6f7462dbe71f755149886006e144bedc8ce11d09f72452472ee641e`.
- `source/id-ID/worksheet-18-solutions.md`: 9,027 bytes, SHA-256
  `10fcda87b4613fdf6bd037b8428ee46b82ffbfa73c182dbb3732602d0f683db4`.

During full-resolution cumulative-reader inspection, three intended `\qquad`
spacing commands in Solution 18.3 were found without their leading backslashes,
which exposed `qquad` as reader text. The edition source was corrected before
release; the mathematical equalities and source-solution scope are unchanged.
- `source/id-ID/media-credits-unit-18.md`: 789 bytes, SHA-256
  `9e1f8c342873acbe70a43ab88718bba67cbe4ed10672afb77f2ed5c41a78f0c5`.

The unit preserves all 28 exercises, all five frozen public solutions, stars,
submitted-work points, the source hint, source order, 58 unique stable IDs,
and exact provenance `OpenAI Codex gpt-5.6-sol, Ultra.` No missing solution
was invented.

## Source corrections and QA

Five ledgered source deltas are disclosed in place:

- `AGC-CORR-0046` restores scalar powers $s^{f_i}$ in the factored monomial
  map where the source prints undefined indexed variables $s_i$.
- `AGC-CORR-0047` restores scalar powers $t^{e_i}$ where the source prints
  undefined indexed variables $t_i$.
- `AGC-CORR-0048` names the universal property of the group completion
  actually used by the alternative surjectivity proof.
- `AGC-CORR-0049` restores $x_1,x_2\in M_+$ in the minimal-generator proof.
- `AGC-CORR-0050` retains the necessary nonzero scalar in
  $\varphi(f)=c(T-1)^n$ in public Solution 18.10.

`qa/UNIT_18_TRANSLATION_QA.json` reports PASS. It is 3,610 bytes with SHA-256
`9a0d480dc799bb53669e324a324f43f89d9672a7d3bf5a5cdae9cd45e3dd669c`.
The 19,368-byte deterministic gate has SHA-256
`eadbe6ab946e04563379481a958b412cd96ee0b69b142e5572669670ffc1bd49`.
It replays every authority/PDF hash, solution topology, rights and
source/control identity; validates the Pandoc AST, stable IDs, terminology,
protected mathematics, all five correction bindings, language residue,
placeholders, invisible Unicode, and secret-like strings.

## Cumulative Units 1--18 release boundary

The rebuilt standalone HTML is 11,555,390 bytes, SHA-256
`fab05aac5a84b45ee36260d895dcf89e2ad2d13fd6b7545eba2ae4c2e3db2f0a`.
The A4 PDF is 320 pages and 6,905,745 bytes, SHA-256
`ba62b61759a50925dcefa1a3a0153c8b597ee1386dd2033b610dae622e33ed99`.
Machine, protected-surface, responsive, and all-page visual QA pass; all 320
page PNGs were bound by `qa/UNITS_01_18_VISUAL_PAGE_MANIFEST.json`.

The append-only native backend contains 13,626 canonical records, SHA-256
`c952ca6c0a6b36f2138c0971161b11582bbb1479795bf36c9d1de23e4343e517`.
All 10,938 prior records are byte-identical. Independent backend QA is PASS.
The strict common adapter validates 32,473 virtual records, 77,291 foreign
keys, and exact reverse replay to the native hash.

The deterministic eight-file reader-first package is frozen under
`release/unit-18`. Zenodo record 22087566 / DOI
`10.5281/zenodo.22087566` is published in the existing concept; all eight
files passed anonymous byte readback. The sanitized receipt is
`qa/UNIT_18_ZENODO_PUBLICATION.json`, 3,927 bytes, SHA-256
`da3f18c473b8d64c986b871426b5f605b7f8fdb74bef6b67c634ef7b4df4af91`.

Next executable action: publish the same frozen checkpoint to the existing
GitHub main/tag/release/Pages lineage, anonymously verify the eight release
assets plus raw commit and Pages reader bytes, then bind both receipts. Unit 19
remains reserved as `HP-D100-001`; do not translate it while the reservation is
active, and three-way review any schema-clean helper return before integration.
