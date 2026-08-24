# Unit 8 durable worklog — Indonesian Algebraic Geometry Bridge

Checkpoint: 2026-08-23. This log is the resumable record for the completed
Unit 8 boundary; it does not claim that the 30-unit classical volume is
complete.

## Scope and authority

- Frozen lecture page 165897, revision 1051293; frozen worksheet page 165927,
  revision 1057977. The complete Unit 8 authority manifest is
  `authority/wikiversity/unit-08/UNIT_AUTHORITY_MANIFEST.json`, 85,967 bytes,
  SHA-256 `f9089c78e81511bdbc24dc62d7c506a77c266426ea73b3e390f20ec30dabb40f`.
- Ordered map `authority/wikiversity/unit-08/ORDERED_EXERCISE_MAP.json` has
  24 exercises and public solutions for 8.9 and 8.17; SHA-256
  `000ee8da757d92c581bb49a4d0e5a23b06393d5af3028f2f97c979fabcf4553d`.
- Rights closure `authority/RIGHTS-unit-08.csv` is 6,107 bytes, SHA-256
  `5df7a3e76e42f9f481a0b7379a367905d91cc3ece501b3e158f1673aff663d69`;
  asset closure SHA-256 is
  `32e10f17fdd52797e718103b3f37ce98ce99c83bb25aa17f16fd4caa7d7c5daf`.
- Source hashes: lecture `a81665fbdc0ba82f6d5a490b64e9853a537c319b75b942a8dcbdc1e4a528dbe4`,
  worksheet `96a98b6767af0743b84078ddd75654a3bc9d054a7221c247a4de00091a555817`,
  solutions `aacfbdc5dd88f92c84b35448d930fc1e7524eff74bf817d08e5e4539b6628563`.

## Translation and terminology QA

The lecture, worksheet, and two public solutions are translated in source
order. The correction ledger records the reachable-bound precision, proof-gap
disclosure, animated-media/PDF companions, alternative descriptions, portable
definition notation, and PDF-only Latin transliteration. No source proof was
silently repaired. The exact tool provenance is `OpenAI Codex gpt-5.6-sol,
Ultra.`; source author, contributor, attribution, and non-endorsement notices
remain intact. The cumulative terminology receipt is
`qa/TERMINOLOGY_QA_RECEIPT.json`, 8,739 bytes, SHA-256
`2a2f0b0a4ddfd627ce79c4b5bc4d61f8c72a1039102fafefbfabd432cf1edfe4`, result
`pass`.

## Reader and QA evidence

The cumulative through-Unit-8 HTML is 8,582,322 bytes, SHA-256
`ab3dd639b882c127ec8a010cc9ce1f7dbf24bce876eb24146a0b8a519d63e6f8`; the A4
PDF is 161 pages, 5,491,421 bytes, SHA-256
`94d279d5748761cc1648d728451a80562cffaffeac9005d93220e980556d72b6`.
Build receipt SHA-256 is
`d442c80d9d0cd3a0bddf23401664d24722f6df8db5a19a7626bb76284ca08d24`, with
zero warnings. Machine, all-page visual, responsive desktop/mobile reflow,
and protected-surface QA all pass. The responsive check proves a centered
desktop body, no page-wide 390-pixel overflow, and local scrolling for wide
display mathematics.

## Backends and common adapter

Native `backend/units-01-08/MANIFEST.json` is 18,667 bytes, SHA-256
`b019122587e5bca0b2224e2cf9ac05a879e6b53e228ee09ca2e04a68c970b337`; canonical
`records.jsonl` is 8,264,170 bytes, SHA-256
`7ac2d40a553741648ef3e5136802247cd3004ea41e3733496aabb0d7c273f973`, with
5,787 records. The exact 5,182-record Unit 7 baseline is byte/payload
preserved. Native backend QA is `qa/UNITS_01_08_BACKEND_QA.json`, SHA-256
`e8a8c4a38771b53f9d968d89ce5864fb0060d8c6e640594f6dc92d3c6c2aef94`.

The public common-backend-v1 handoff and receipt schema were independently
read from the frozen `v0.42.0` raw URLs and match the local witnesses:
handoff SHA-256 `83de5379aa08f25fb3fb2774ed8bde99eca76e9a6ba80da9ccf2ee211e5e3a7a`,
receipt-schema SHA-256 `0147b14972dd562805b3b5f76fac453a9f32a6d298827d3f588316d4a8f5ffe0`.
The adapter is additive and zero-copy: 14,022 virtual records,
21,280,311 virtual JSONL bytes, SHA-256
`2c9ad5ea7700e307a27dd16273f941b28dec350a07743a9dd13e7c586520ed42`,
32,826 foreign keys, deterministic double replay, and exact native reverse.
The frozen sanitized receipt is
`backend/common-backend-v1/MIGRATION_RECEIPT.json`, 6,778 bytes, SHA-256
`603b923a2d914f0594bc9afd45eee80baa2001602723beac36968ad4452b73bd`; its
validation result is `pass`, credentials recorded `false`, and its publication
artifact list is the Zenodo Unit 8 release excluding the receipt itself.
For a later boundary, invoke `scripts/generate_common_backend_v1_receipts.py`
with an explicit `--native-backend backend/units-01-NN` and explicit public
record/DOI/files; its historical default still names the Unit 7 backend.

## Publication boundary

Reader-first release files were packaged and verified before publication.
The package manifest is `release/unit-08/ZENODO_FILE_MANIFEST-unit-08.json`:
PDF 5,491,421 bytes (`94d279d5748761cc1648d728451a80562cffaffeac9005d93220e980556d72b6`),
HTML 8,582,322 (`ab3dd639b882c127ec8a010cc9ce1f7dbf24bce876eb24146a0b8a519d63e6f8`),
source ZIP 7,592,593 (`89faa5f776a9c7e9b197dbc488191051802282701c155bcee7678db4225a5ec7`,
274 verified entries), authority-witness ZIP 10,494,193
(`305d47b67056c8bd64173e594d3fdeadb3db2d221e92bb4900606ad34579ca47`, 323
verified entries), build receipt 19,332
(`d442c80d9d0cd3a0bddf23401664d24722f6df8db5a19a7626bb76284ca08d24`), licence
3,445 (`6f6e91a9ad0bc29da479af84b361aeba1976d79d0f7462e7f0b7b7522d0d6054`),
and manifest 3,677
(`9dbc4256055b84b699729790b1844c644abbbff7ed7c2038938423053e2f4f5b`). The migration receipt
is intentionally separate to avoid a self-referential manifest hash cycle.
The uploaded source ZIP is the immutable package snapshot assembled immediately
before the Zenodo transaction; the local README/CITATION and this worklog were
advanced afterward to bind the public record and next cursor. Do not silently
rewrite the published bytes; if a future release needs a refreshed source
snapshot, issue it as a clearly labelled subsequent version.
Zenodo concept `10.5281/zenodo.22059686` now has public Unit 8 record
22070936, DOI `10.5281/zenodo.22070936`, URL
`https://zenodo.org/records/22070936`. Anonymous API readback verified all
8 public files, sizes, and SHA-256 values; receipt
`qa/UNIT_08_ZENODO_PUBLICATION.json` is 3,794 bytes, SHA-256
`f3ca56bded40bc96d3779ffd584ef2480926b52f7126e01edeea3c95c5982963`.
The public title and description contain no organization prefix; the required
organization entry appears once in contributor metadata, and the exact
translated-text/per-component-rights and non-endorsement statements remain.
GitHub was not retried because the user-confirmed suspension persists.
An independent anonymous API/file recheck on this checkpoint returned HTTP 200,
found eight files, and matched every receipt byte count and SHA-256; the
migration receipt also validates against the frozen Draft 2020-12 receipt
schema with zero errors.

The Figshare route made no mutation: the designated authenticated license
preflight returned HTTP 403 `InactiveAccount`. Anonymous project/collection
checks were recorded without claiming deletion or creating a duplicate.
Receipt `qa/UNIT_08_FIGSHARE_PUBLICATION.json` is 2,405 bytes, SHA-256
`979aaf61fea1bc32227aa98559f013afeb0aef35e7c8a40ae5f2aaaa28a4633f`, status
`BLOCKED_EXTERNAL_STATE`; no edition bytes were uploaded and no false CC0
substitution was made. Retry only after Figshare account/API restoration.

## Exact next executable work

1. Reconstruct from this log, `CURRENT_GOAL_AND_WORKFLOW.md`, and
   `CURSOR.json`; do not use conversation summaries as state.
2. Freeze Unit 9 authority, rights, source, and complete exercise/solution
   closure; translate lecture, worksheet, and public solutions contiguously.
3. Rebuild cumulative HTML/PDF, run machine, protected-surface, visual,
   responsive, terminology, native-backend, and common-adapter gates; record
   hashes and a bounded release manifest.
4. Publish the verified Unit 9 boundary to the existing Zenodo concept and
   anonymously read back every public byte. Do not retry GitHub or Figshare
   while their recorded external blocks persist.
5. Continue Units 10–30, then freeze/translate all 30 BGK units and add the
   separately authored schemes/cohomology bridge, solved mastery layer,
   integrative problems, and Stacks-tag capstone. Mark the finite goal complete
   only after all required corpus, QA, rights, and publication gates pass.
