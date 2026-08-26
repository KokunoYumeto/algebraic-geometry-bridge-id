# Unit 27 owner-production worklog

## Boundary and source identity

Unit 27 completes the internal Units 25-27 production tranche and is the next
substantial cumulative release boundary. It belongs only to the official
complete *Algebraische Kurven (Osnabrueck 2012)* course and uses the
`br-ak-2012-*` namespace. Units 1-24 and their accepted public bytes remain
unchanged while the cumulative Units 1-27 reader/backend release is built.

- Course route: page 50687, revision 658236.
- Lecture: page 50733, revision 1052572, MediaWiki SHA-1
  `9a396f3a601f0a0a0606657550a30b9a601da2f6`; root plus 120 dependencies
  gives 121 identities, canonical-row SHA-256
  `5ed97c57220d6379b672fd7b47a8cfca82c38ef4e84bafd3538e3cdf42f74ca8`.
- Worksheet: page 50762, revision 793496, MediaWiki SHA-1
  `eeac2c6881d4121e734bc2dffbe9621f03dfdc89`; root plus 60 dependencies
  gives 61 identities, canonical-row SHA-256
  `bea2d1bb50691139418ccf884928594f7658bc3bad1a0e22b8a4c99eb71c8b24`.
- The worksheet has exactly 11 exercises: warm-up 1-7 and submitted 8-11.
  Authored points are 2, 2, 2, 3, 2, 2, 2, 3, 3, 3, and 3; submitted
  exercises display 3 points each. No exercise is starred. All eleven exact
  solution-page candidates are proven absent, so no solution is invented.
- `authority/wikiversity/unit-27/UNIT_AUTHORITY_MANIFEST.json`: 135,052
  bytes, SHA-256
  `98f9ebcc0d3b41bb0b955c5190d416b9ebfc07433015732faaf7f38366a1d9b2`.
  A live replay covered 157 unique semantic identities in seven batches, both
  official PDFs, and ten Commons media identities.
- `authority/UNIT_27_AUTHORITY_FREEZE.md`: 4,838 bytes, SHA-256
  `76da6c76238a6b542848b42d32a897613c24e43f9a2dee52b90a7300fa8ebb3d`.
- `qa/UNIT_27_AUTHORITY_QA.json`: deterministic PASS, 1,430 bytes,
  SHA-256
  `60b4b2cce7cbd18bcfdbe7698d136bcee9e721dba631e525726ea8e185a4c139`.

## Media, PDFs, and rights

Unit 27 adds ten reader-media positions. Every reader reference is bound to
the frozen full-resolution original in `authority/assets`, not to an
unregistered thumbnail alias. Per-component creator, uploader, source,
licence, dimensions, bytes, and SHA-256 remain explicit.

- `authority/RIGHTS-unit-27.csv`: 11,564 bytes, SHA-256
  `df2fb8403ddef014500e81e2165e2d4e400a0573dd262ba3dba5ece6bcd46821`.
- `authority/ASSET_CLOSURE-unit-27.json`: 26,057 bytes, SHA-256
  `b08e53863d977899d9910d1b6f48e82237f590402e8450f2683b07a078c1ebc6`.
- Official lecture PDF: 171,996 bytes, nine pages, SHA-256
  `0d4402bfae46abd09cb4719110a006287b03de31b0e620e0157a4ef9a07817f2`.
- Official worksheet PDF: 41,952 bytes, two pages, SHA-256
  `e1fa608c2b54c988f16d0c0b2119f1d21440b37debbf87d89b7bbf228c6bdf9d`.

The PDFs are unencrypted and text-extractable but untagged, with no structure
tree, language metadata, outline, or bookmarks. The historical course and
file-description licence routes are preserved without a blanket mixed-set
relicensing claim. The text derivative remains on the CC BY-SA 4.0 route;
media retain their exact component licences.

## Translation, terminology, and disclosed repairs

The complete Indonesian source preserves 21 ordered lecture entities, all 11
exercises, the zero-solution closure, ten accessible images, 39 unique unit
header IDs, and 269 Pandoc math nodes.

- `source/id-ID/lecture-27.md`: 24,844 bytes, SHA-256
  `81ed14c582b9b181cb9dfe1795c9f0bf95cf894f3af66935dd4912b397f446b9`.
- `source/id-ID/worksheet-27.md`: 5,728 bytes, SHA-256
  `2ccf9879d8bad546a21e100fec700c49b49f5fdf98aa8a598c274827700487ee`.
- `source/id-ID/worksheet-27-solutions.md`: 1,723 bytes, SHA-256
  `fe9b9dd6ced41c2ccbea06bd99e3dfba2708d68290c8763d1c9152cd25ab2733`.
- `source/id-ID/media-credits-unit-27.md`: 5,048 bytes, SHA-256
  `4e46a14420118be7ad665a59ae39787d6dc29d6c8ca3df1c3bffb6f01dca1e55`.
- `source/id-ID/frontmatter-units-01-27.md`: 4,806 bytes, SHA-256
  `66e9e4bfb31c24cb131e05c02c8b19509d9cfd44c9d222c3d75d312b5a95e280`.

Primary Indonesian mathematical usage supports `proyektif`; the three-source
terminology decision is recorded in `qa/UNIT_27_TERMINOLOGY_QA.md` (2,156
bytes, SHA-256
`2af64f71732f7d2ee7bf8e163c2d097701471377e56472d4ab850ccbaba79035`).
Terminology rows `AGT-0230` through `AGT-0249` and disclosed correction rows
`AGC-CORR-0108` through `AGC-CORR-0114` are bound. At this boundary:

- `00_control/TERMINOLOGY.csv`: 39,202 bytes, SHA-256
  `8f0bfb467b935a34350e56a038d166a48ad89a2e656044563ac4a5c2aee0f11e`.
- `00_control/CORRECTIONS.csv`: 73,728 bytes, SHA-256
  `e9f5aef207253e30badcfd095a3bc3cf5d465b18a6f700a82b1e32422183acc8`.

The seven repairs disclose the chart-coordinate ambiguity, malformed
dehomogenization notation, `a_1X_0` typo, false homogeneous-maximality claim,
dangling fact marker, false common-fixed-chart assertion in the Hausdorff
proof, and missing cone-openness hypothesis. No repair is silent.

## Deterministic QA and next action

`scripts/qa_unit27_translation.py` is 16,256 bytes, SHA-256
`79e88e76e45172a025e0905f97b9feefbb1f26edcc532c1c8d51d2c5148f5377`.
Two consecutive executions produced the same PASS receipt:
`qa/UNIT_27_TRANSLATION_QA.json`, 6,416 bytes, SHA-256
`8070ae0e936af520c6b6cfca42847fbe6d2b3473caa411f3be1a47594416edcb`.
It fails closed on authority, source/control identities, entity order,
mathematics, IDs, exercise/solution topology, media/accessibility/rights
closure, provenance, language residue, placeholders, Unicode dash characters,
and secret-like text.

Cumulative source coverage is now 27 lectures, 27 worksheets, 657 exercises,
117 frozen public source solutions, and 94 reader-media positions. The
cumulative reader/backend package passed all deterministic gates and is public
in both existing lineages. Zenodo record 22104692 / DOI
`10.5281/zenodo.22104692` and GitHub content commit
`07b22e59c546bf9c29995cded0aff37e696b2d02`, annotated tag `unit-27`, and
eight-asset release were anonymously read back. The GitHub receipt
`qa/UNIT_27_GITHUB_PUBLICATION.json` is 6,687 bytes, SHA-256
`63a25c2408388c8af35d510fc88d0e1813ef499ba05d11a2724a4f2c978da277`;
it proves all eight release assets, raw commit HTML/PDF and public metadata,
and Pages HTML/PDF. A bounded local browser retry was blocked by the browser's
local-file URL policy, so no workaround was attempted; the hash-bound
responsive receipt and matching public Pages bytes remain the controlling QA
evidence.

Next: freeze official 2012 Unit 28 authority and continue contiguous
translation and bounded per-unit QA through Units 28–30. Then run the complete
30-unit classical reader, backend, visual/responsive QA, release, and public
readback cycle.
