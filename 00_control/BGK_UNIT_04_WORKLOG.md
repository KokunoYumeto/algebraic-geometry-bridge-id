# BGK Unit 4 worklog

Status: complete local Unit 4 and cumulative Units 1–4 production boundary.
The next executable source action is BGK Unit 5; the next external release is
the substantial cumulative Units 1–6 milestone. This file,
`CURRENT_GOAL_AND_WORKFLOW.md`, and `CURSOR.json` are the resumption controls.

## Frozen authority

- Course: Holger Brenner, *Bündel, Garben und Kohomologie (Osnabrück
  2019–2020)*, Unit 4.
- Lecture page 109008, revision 1003714, MediaWiki SHA-1
  `8eceb7ac307706e0858ffa278bd9d1235574a596`; complete 106/106 semantic
  transclusions. Worksheet page 110209, revision 1003857, MediaWiki SHA-1
  `879b20dfad7b078a205c00bf5e341035b8307f8e`; complete 60/60 semantic
  transclusions.
- `authority/wikiversity-bgk/unit-04/UNIT_AUTHORITY_MANIFEST.json`: 74,511
  bytes, SHA-256
  `3f26616ff7e9f4ac0d5bb0e64ad8435fefc18e32e4c91b16d780d4346498f680`.
  Root revisions plus those complete closures are semantic rebuild authority.
  The `/latex` wrapper/API/XML/HTML surfaces and expanded TeX are terminal-byte
  witnesses, not an overstated recursive template reconstruction.
- Expanded lecture TeX: 22,669 bytes, SHA-256
  `4dc55e0810888863946316396cff73ce5ef1a1bb9b46864b64b3ed80ba3a8ea1`.
  Expanded worksheet TeX: 4,953 bytes, SHA-256
  `7af2dce83605791269ba4fc1d5351100411b0a8081920cce8f1241724249f974`.
- Exactly nine ordered exercises and zero public source solutions; all nine
  candidate lookups are negative and no solution was invented.
- Official lecture PDF: 243,533 bytes / 7 pages / SHA-256
  `9e6dd93da57ae35f96568fc717442ac4c6fb209733527143068c34f32248d222`.
  Official worksheet PDF: 31,057 bytes / 3 pages / SHA-256
  `082b49c71d075c7bd137ff66ce20d1ec3a76fe2368e1a2c2f0141e774e270ed9`.
- One substantive source image is preserved at
  `authority/assets/bgk-u04-triticum-spelta.jpg`: 100,723 bytes, SHA-256
  `1050547eae3e7855001791da54dc8cd957b324cf38e5ef5b0955b4a596b0da7b`,
  André Karwath aka Aka, CC BY-SA 2.5. Semantic course text/translation remain
  CC BY-SA 4.0. Current Commons PDF metadata and embedded PDF notices are
  disclosed separately; no mixed-set blanket licence is claimed.
- `authority/BGK_UNIT_04_AUTHORITY_FREEZE.md`: 9,405 bytes, SHA-256
  `e0082362603d963a331f9f687164600ae499d45ee1ff8488dfd498f2ccd0ed0e`.
  `qa/BGK_UNIT_04_AUTHORITY_QA.json`: 13,521 bytes, SHA-256
  `94a997fd7e1be998512f6450d70bedc1c300e3b45882991a0350f4e44ae59428`.

## Translation and source treatment

- `source/id-ID/bgk/frontmatter-bgk-units-01-04.md`: 4,029 bytes, SHA-256
  `8eff29e7d764fb04c1577a17b4babbd3dc8e680999315a35f5fca645e1c30f11`.
- `source/id-ID/bgk/lecture-04.md`: 14,153 bytes, SHA-256
  `d85d039317df0d8d176b0c9db4b582e54e351d1bdf40083d5b5d9e6480e87f18`.
- `source/id-ID/bgk/worksheet-04.md`: 6,079 bytes, SHA-256
  `77e20f9f7e9fea2052277292df8ae81f0ecf9c69e756d2fb561c281290d41269`.
- `source/id-ID/bgk/worksheet-04-solutions.md`: 1,687 bytes, SHA-256
  `7e7d0842ba56a1d541577c2be4cef44afb5bee15529aa67cbfef99f0e086dfd0`.
- Translation QA proves all 11 numbered lecture entities, nine exercises,
  zero public/invented solutions, 33 unique source-heading IDs, 230 Pandoc
  math nodes, one correctly attributed image, and complete rights/provenance.
  Receipt `qa/BGK_UNIT_04_TRANSLATION_QA.json`: 5,661 bytes, SHA-256
  `f06586dbb166c7d305fbf29c77bd5831d4f119057296789a0ee9c0f1871b5817`.
- Five visible source treatments are ledgered as `AGC-CORR-0154` through
  `AGC-CORR-0158`: heading typo, completion of the Hom-sheaf proof over every
  open subset with restriction naturality, the missing cardinality hypothesis
  in Exercise 4.4, the stalk-index mismatch, and the Exercise 4.9 double typo.
  Original forms remain in the authority and visible edition notes.
- Nine new terms `AGT-0315`–`AGT-0323` and thirteen reused terms pass. Current
  `00_control/TERMINOLOGY.csv`: 51,230 bytes, SHA-256
  `db567eb87fa30247e747fe15c3c3b9fd0ef64bb55f4f776286b35491ad11c421`.
  Current `00_control/CORRECTIONS.csv`: 98,843 bytes, SHA-256
  `fe486065197a2839a0e341f4634154d47bb9a63db10ac3fa0c6e1ee00645edde`.

## Cumulative reader through Unit 4

- `build/reader-bgk-id/index.html`: 3,062,967 bytes, SHA-256
  `ca9d860f1b0dd68d18ffe4017efbf755ed7819aa0727d4194f880863bcd1609b`.
  It is self-contained semantic HTML/MathML with 1,274 MathML nodes, 348
  unique IDs, zero broken internal anchors, five images with nonempty alt text,
  one main landmark, and one skip link.
- Desktop 1280×720 and mobile 390×844 both have zero document-level horizontal
  overflow and a centered main region. All 24 wide phone formulas are locally
  scrollable; every image stays inside the mobile content region. Unit 4's
  image, opening, Exercise 4.9, and solution-scope ending were visually checked.
- `build/reader-bgk-id/bundel-berkas-dan-kohomologi-id-units-01-04.pdf`:
  774,444 bytes / 60 A4 pages / SHA-256
  `26db50d9ca0fc0b343e67025b1d2d6f17393703f30df586da03db059a0d02ea0`.
  All 60 pages were rendered and inspected; all 13 fonts are embedded/subset,
  all 176 links are in bounds, and there is no clipping, overlap, bad glyph,
  broken equation, or unintended blank page. The PDF is untagged, so semantic
  HTML remains the primary accessible surface.
- Two consecutive builds are byte-identical. `BUILD_RECEIPT.json`: 7,666
  bytes, SHA-256
  `7b3230d851f721350d830d5d61a8d1d2f86622186c91fa3991b78a61cfb31fba`.
  Reader QA `qa/BGK_UNITS_01_04_READER_QA.json`: 3,741 bytes, SHA-256
  `7fb3b518daf33afe71252fb01a73e382bd1d3e41de9752a0fc58124c797fe840`.

## Cumulative native and common backend

- Native backend: 2,919 records = the exact 2,370-record Units 1–3 byte
  prefix plus 549 Unit 4 records. It contains 71 exercises, exactly the two
  earlier public solutions, six assets, 180 source-heading IDs, all five Unit
  4 corrections, an explicit image relation, exact model provenance, and zero
  collisions with the 22,752 classical IDs.
- `backend/bgk-units-01-04/records.jsonl`: 3,275,124 bytes, SHA-256
  `f72ec15d7d036df7272d043968b888a61cffae8475ef8ce7206dbf1bcb3aeb04`.
  `MANIFEST.json`: 14,494 bytes, SHA-256
  `a72b3b274fa1fc1d21459b8de9e76c4c0d4cb949c14eb09df62bef9f9c3ac357`.
  QA receipt `qa/BGK_UNITS_01_04_BACKEND_QA.json`: 4,532 bytes, SHA-256
  `3473c17b988669337d4dbdb9042689b4ea7e5350d931bce32d08d0baae0cc7ef`.
- The additive common-backend preflight validates 7,011 common records, 1,134
  strict profiles, 22 witness files, 16,517 foreign keys, and a 9,838,994-byte
  virtual stream (SHA-256
  `2e0f6205584c1f3bd7e7d30cc9cad52c004cd05d68fb28a107112ed91394f8cb`).
  It reverses exactly to the native SHA-256; two runs have identical output.
  Receipt `qa/BGK_UNITS_01_04_COMMON_ADAPTER_PREFLIGHT_QA.json`: 2,266 bytes,
  SHA-256 `4034ad13ab0efa3385c7392f0a8d69954b0c6cf3dfcabc9004412eef0f7e6de5`.

## Cursor and next executable action

The complete selected core is 60 source units / 602 official pages, not 100
units. Exactly 34/60 source units are now complete: all 30 classical units and
BGK Units 1–4. BGK Units 5–30 remain: 26 units / 205 official-source PDF
pages. The 19-unit learner route is only a view and adds no translation work.
Unit 4 is deliberately not published alone; continue immediately with the
frozen Unit 5 authority and translation, then Unit 6, and publish/read back the
substantial cumulative Units 1–6 milestone in the existing lineages.

Model provenance: OpenAI Codex gpt-5.6-sol, Ultra.
