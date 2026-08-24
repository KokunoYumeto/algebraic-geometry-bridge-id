# Handoff — Indonesian reader through Unit 8

Checkpoint: 2026-08-23. The contiguous Indonesian translation, authority
freeze, rights closure, reader build, visual/reflow QA, native backend export,
and additive common-backend-v1 preflight are complete through Lecture 8 and
Worksheet 8. This is a partial 30-unit classical volume, not a complete
edition. GitHub publication remains deferred because the account suspension is
user-confirmed; Zenodo and the existing Figshare lineage are the active public
preservation routes.

## Unit 8 authority and translation

The frozen Wikiversity manifest is
`authority/wikiversity/unit-08/UNIT_AUTHORITY_MANIFEST.json` (85,967 bytes,
SHA-256 `f9089c78e81511bdbc24dc62d7c506a77c266426ea73b3e390f20ec30dabb40f`).
Lecture page 165897/revision 1051293 and Worksheet page 165927/revision
1057977 are complete with all requested transclusions. The ordered exercise
map is 9,170 bytes, SHA-256
`000ee8da757d92c581bb49a4d0e5a23b06393d5af3028f2f97c979fabcf4553d`: 24
exercises and the two public solutions for Exercises 8.9 and 8.17. Six media
positions and their eight binary/accessibility surfaces are closed by
`authority/RIGHTS-unit-08.csv` (6,107 bytes, SHA-256
`5df7a3e76e42f9f481a0b7379a367905d91cc3ece501b3e158f1673aff663d69`) and
`authority/ASSET_CLOSURE-unit-08.json` (SHA-256
`32e10f17fdd52797e718103b3f37ce98ce99c83bb25aa17f16fd4caa7d7c5daf`).

The Unit 8 source files are frozen as follows:

- `source/id-ID/lecture-08.md` — 22,707 bytes,
  `a81665fbdc0ba82f6d5a490b64e9853a537c319b75b942a8dcbdc1e4a528dbe4`;
- `source/id-ID/worksheet-08.md` — 11,853 bytes,
  `96a98b6767af0743b84078ddd75654a3bc9d054a7221c247a4de00091a555817`;
- `source/id-ID/worksheet-08-solutions.md` — 3,899 bytes,
  `aacfbdc5dd88f92c84b35448d930fc1e7524eff74bf817d08e5e4539b6628563`.

The exact model identification `OpenAI Codex gpt-5.6-sol, Ultra.` is additive
provenance; source author, contributor, attribution, and non-endorsement
information remain intact. The correction ledger records the reachable-bound
precision, source proof-gap disclosure, animated-media/PDF companions,
alternative descriptions, portable definition notation, and PDF-only Latin
transliteration. No source proof was silently repaired.

## Reader and QA boundary

The self-contained HTML is 8,582,322 bytes (SHA-256
`ab3dd639b882c127ec8a010cc9ce1f7dbf24bce876eb24146a0b8a519d63e6f8`). The A4
PDF is 161 pages and 5,491,421 bytes (SHA-256
`94d279d5748761cc1648d728451a80562cffaffeac9005d93220e980556d72b6`). The
build receipt is 19,332 bytes (SHA-256
`d442c80d9d0cd3a0bddf23401664d24722f6df8db5a19a7626bb76284ca08d24`), with
zero build warnings. Machine QA, all-page visual QA, responsive HTML QA, and
protected-surface QA all report PASS:

| receipt | bytes | SHA-256 |
|---|---:|---|
| `qa/UNITS_01_08_MACHINE_QA.json` | 9,016 | `02f629596e8746c1346eedf9eb6302ef8dd739543971f31be5385248e09e9230` |
| `qa/UNITS_01_08_VISUAL_QA.json` | 44,103 | `0fe7cf2de5980b40e8e3f57a49b93975581fbe9d4240c6b934f697b2601bee31` |
| `qa/UNITS_01_08_RESPONSIVE_QA.json` | 1,944 | `31cc70d55d8d0930a5946bbb7e1954b1c678c930abbbce8d16a3090aa8cba4c9` |
| `qa/UNIT_08_PROTECTED_SURFACES.json` | 3,270 | `98231acc366bd33fc17bba490b25553e2bc95c5f89ccfe4b397a3be8555ddbfd` |

The browser check proves centered desktop layout, no page-wide mobile
overflow, locally scrollable wide mathematics, and no broken remote images.

## Native and common backends

`backend/units-01-08/MANIFEST.json` is 18,667 bytes, SHA-256
`b019122587e5bca0b2224e2cf9ac05a879e6b53e228ee09ca2e04a68c970b337`; its
canonical JSONL is 8,264,170 bytes, SHA-256
`7ac2d40a553741648ef3e5136802247cd3004ea41e3733496aabb0d7c273f973`, with
5,787 records and unique IDs. The exact Unit 7 baseline (5,182 records) is
carried forward byte/payload-identically. Independent backend QA is
`qa/UNITS_01_08_BACKEND_QA.json` (2,042 bytes, SHA-256
`e8a8c4a38771b53f9d968d89ce5864fb0060d8c6e640594f6dc92d3c6c2aef94`).

The common-backend-v1 adapter is additive and zero-copy: 14,022 virtual
records, 21,280,311 virtual JSONL bytes, SHA-256
`2c9ad5ea7700e307a27dd16273f941b28dec350a07743a9dd13e7c586520ed42`, 32,826
foreign keys checked, and exact native reverse SHA-256
`7ac2d40a553741648ef3e5136802247cd3004ea41e3733496aabb0d7c273f973`. Its
validated migration receipt is
`backend/common-backend-v1/MIGRATION_RECEIPT.json` (6,778 bytes, SHA-256
`603b923a2d914f0594bc9afd45eee80baa2001602723beac36968ad4452b73bd`), with
schema validation `pass` and `credentials_recorded: false`. The frozen
upstream handoff/schema witnesses are under
`backend/common-backend-v1-contract/upstream/`; their public raw identities
are recorded in the Unit 8 worklog.

## Rights, publication, and next cursor

The translated course text and derivative editorial layer remain CC BY-SA 4.0;
media retain per-component licences and attribution. No blanket licence is
claimed for the mixed file set. The release is reader-first: PDF, HTML, a
resumable source/backend archive, authority witnesses, manifest, licence, QA,
and migration receipt are preserved. The existing Zenodo concept
`10.5281/zenodo.22059686` is the sole version lineage. Unit 8 is public as
record 22070936, DOI `10.5281/zenodo.22070936`, URL
`https://zenodo.org/records/22070936`; receipt
`qa/UNIT_08_ZENODO_PUBLICATION.json` (3,794 bytes, SHA-256
`f3ca56bded40bc96d3779ffd584ef2480926b52f7126e01edeea3c95c5982963`)
anonymously verifies all eight public files. Figshare made no mutation because
the authenticated license preflight returned HTTP 403 `InactiveAccount`;
`qa/UNIT_08_FIGSHARE_PUBLICATION.json` (2,405 bytes, SHA-256
`979aaf61fea1bc32227aa98559f013afeb0aef35e7c8a40ae5f2aaaa28a4633f`) records
the external block, no uploaded edition bytes, and no false CC0 substitution.

Resume from `00_control/CURRENT_GOAL_AND_WORKFLOW.md`,
`00_control/CURSOR.json`, and `00_control/UNIT_08_WORKLOG.md`; freeze and
translate Unit 9 in source order. The complete finite goal remains all 30
Brenner classical units followed by the required complete BGK volume; Napkin
is optional reference evidence only and Stacks is downstream.
