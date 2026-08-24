# Handoff — Indonesian reader through Unit 7

Checkpoint date: 2026-08-22

State: the cumulative Unit 1–7 translation, authority and rights closure,
self-contained reader build, all reader QA, corrected native stable-ID backend,
and additive common-backend-v1 adapter are complete and frozen. The corrected
architecture replay preserves all 5,179 prior IDs, adds three BGK architecture
records, and removes the stale Napkin dependency. The Unit 7 Zenodo version is
published in the existing concept and all seven public files passed anonymous
size/SHA-256 readback. The existing Figshare item is updated, remains lawfully
metadata-only, and is verified in Indonesian collection version 41. The exact
next transaction is the Unit 8 authority freeze and contiguous translation.
GitHub must not be retried while the confirmed account suspension and support
ticket remain unresolved.

## Completed reader boundary

The independent Indonesian edition now contains Brenner Lectures 1–7 and
Worksheets 1–7 in source order: all 197 exercises, all 40 solutions exposed by
the frozen public source, 388 stable reader heading IDs, and 53 reader-media
positions. No unavailable solution was invented. Formulae, identifiers, star
markers, point values, links, source order, attribution, component rights,
change notices, ShareAlike, and non-endorsement are preserved.

Unit 7 translation files are:

- `source/id-ID/lecture-07.md`: 22,411 bytes, SHA-256
  `45023a789b52b562d2fbcd0aaf680453cf3dbef60c41542a89a42be01f63ff52`;
- `source/id-ID/worksheet-07.md`: 16,757 bytes, SHA-256
  `8350ea75756c19a05e09f51074366e4ba85829819690b20a84122c6f9d0e94d3`;
- `source/id-ID/worksheet-07-solutions.md`: 5,326 bytes, SHA-256
  `8c6c52e4aa7e6be203be41235c2bb7a97c2689e4226738f78d62175fe770ecbf`;
- `source/id-ID/media-credits-unit-07.md`: 2,438 bytes, SHA-256
  `5f475ae90e97f737c608ea34a4ed37ddd8ad2d852e180186185f40cb554ee016`.

The exact tool provenance retained in the edition is
`OpenAI Codex gpt-5.6-sol, Ultra.` It is additive and does not replace source,
author, or human-contributor credit.

## Authority, solutions, and rights

Lecture 7 is Wikiversity page 165896, revision 1057689, MediaWiki SHA-1
`482eacab21b84870389c23a5faac8493768fd522`, with all 78 requested
transclusions captured. Worksheet 7 is page 165926, revision 1112363,
MediaWiki SHA-1 `55af227ec3c8f90e9deb857925dcc7725dcf94e1`, with all 136
requested transclusions captured.

The 35-file authority manifest is 103,034 bytes, SHA-256
`6423629ff600ffcfc5067ea139eef01843ece1ce907dd4bda1bfdb12f49de96e`.
The ordered map proves 33 exercises and exactly three public solutions, for
Exercises 7.10, 7.11, and 7.22; its SHA-256 is
`8dfcc09854b47d83eaf9179462449a0a1fa307a3a72e5d1f252cfce35858e0e1`.
The official lecture and worksheet PDF witnesses have SHA-256
`b5e128eb5c1d4b0798c11028b5f488b4f8033a78ce08777a7492d6be7e44a1c2`
and `b680b0385c549b4d3f54bf5418faff1632c880d2c8def4f5967cf321f3c35c20`.

Nine Unit 7 reader positions, including three animated HTML GIF positions,
close over 13 local binary surfaces. `authority/RIGHTS-unit-07.csv` is 8,111
bytes, SHA-256
`e7245bdc9f499fb5b0b71e8598773257b6147147f8f2fe08f82597338946f24f`;
`authority/ASSET_CLOSURE-unit-07.json` is 4,421 bytes, SHA-256
`2a9141295e9e8eae525917e5f6568823077aa67edd50383c431ad7146bde4130`.
The course text and Indonesian derivative are CC BY-SA 4.0; every media item
retains its recorded component status. The 35-row correction ledger is 18,076
bytes, SHA-256
`0c0e853ff6d418f607958a8f06bd0b190c86b41e5df0d7f3e52ef6aa7fb48e34`.

## Terminology QA

A bounded official arXiv check found no suitable Indonesian TeX/e-print and
did not treat HTTP 429 as evidence of zero results. The documented fallback
inspected two representative Indonesian primary PDFs without redistributing
them. The frozen Unit 1–7 source set migrated 117 uses of `medan` to
`lapangan` for field and 22 uses of `gelanggang hasil bagi` to
`gelanggang faktor` for quotient ring. The PASS receipt
`qa/TERMINOLOGY_QA_RECEIPT.json` is 8,742 bytes, SHA-256
`f04814705318b4d7d46623f4be28e55fa86a21cde91f754c24d3acc8680d4899`.

## Build and reader QA

The self-contained HTML is 7,733,142 bytes, SHA-256
`e960f925d718d897f3308deae2404679f2ea9baf95e70b4dc8387b02b242dcc2`.
The cumulative A4 PDF is 142 pages and 5,322,352 bytes, SHA-256
`729d1b4f5593d2695091fd72379df9df69cc3dccb3e6ca404fce705d3d834f56`.
The 17,228-byte build receipt has SHA-256
`ec37c31c30c354e3ebb2c5093ae6b5a7d4a89989cf2850574cffaa89db0b1156`.

All final receipts pass: machine QA
`f0b243aa83440fd295742947bbfec75085581bb183857815635f2a5be7c21ad6`;
visual QA
`7f9915130e4ec89a01f49ff337281d7545e082b668325c5b60cb9c9aa05a9757`;
responsive QA
`08e52316a9523f7bb0c3a4baedc61b6fc3d719e6f9153f6fa62da070a2146653`;
protected-surface QA
`05ebb1dfe3751cd7a9307347cdc04f607fa0eee3073a5c43246fb42e0bbfa6e8`;
and backend QA
`670fdb5be09ca2fcbcb9c7f0f8ae0d8d603eb67e579dcc1256370b577a6ec0c7`.
Visual QA rendered and reviewed all 142 pages, with full-size checks on pages
116, 117, 118, 124, 128, 129, 130, 137, and 142; all defect counts are zero.
All 15 PDF font rows are embedded and no Type 3 font is present. Browser QA
proves a centered 1,224-pixel reader at a 1,440-pixel viewport and no page-wide
overflow at 390 pixels; all 57 over-wide display-math blocks scroll locally,
with zero uncontained nodes outside the viewport.

## Native and common backends

The final locale-neutral native export contains 5,182 canonical records,
including
197 exercises, 40 solutions, 53 assets, 54 concepts, 54 terms, and their
structural, rights, correction, QA, artifact, and relation records. Its
298,913-byte manifest has SHA-256
`8b482971c444a4e5d90695f084234924a873b671885428d98e9db447e4924967`;
the 7,301,025-byte canonical JSONL has SHA-256
`663713a128a0e673a4daf9edd67f9c3dd10ebae02039f8e0c2044c0ca0fa14be`.
Deterministic double replay passes. All 5,179 prior stable IDs are preserved,
three BGK course/resource/rights records are added, and the stale Napkin
dependency is corrected. The 279,800-byte backend-QA receipt has SHA-256
`670fdb5be09ca2fcbcb9c7f0f8ae0d8d603eb67e579dcc1256370b577a6ec0c7`.

The common-backend-v1 layer is additive: it leaves the native backend and
reader unchanged, preserves all 5,182 native IDs, and deterministically exposes
a virtual 12,496-record stream. The virtual JSONL is 18,829,519 bytes with
SHA-256
`e4b3def75472c9eee06cdcf4ef6482f8f12913bd7ee7fc478b111b18df335d7f`.
Exact native reverse reconstruction reproduces SHA-256
`663713a128a0e673a4daf9edd67f9c3dd10ebae02039f8e0c2044c0ca0fa14be`,
and 29,223 foreign keys close. Its validated migration receipt is
`backend/common-backend-v1/MIGRATION_RECEIPT.json`, 5,356 bytes, SHA-256
`c7da3c77e226eec93cc2df286e96258097c3e7b45e2549ac77eafa5cdb354b16`.

## Publication state and exact continuation

Zenodo record 22062319 and DOI `10.5281/zenodo.22062319` are public as version
`unit-07` under unchanged concept DOI `10.5281/zenodo.22059686` and the clean
title *Kurva Aljabar — Edisi Bahasa Indonesia*. The public seven-file payload
contains the PDF (5,322,352 bytes; SHA-256
`729d1b4f5593d2695091fd72379df9df69cc3dccb3e6ca404fce705d3d834f56`),
HTML (7,733,142 bytes; SHA-256
`e960f925d718d897f3308deae2404679f2ea9baf95e70b4dc8387b02b242dcc2`),
source/backend ZIP (6,945,957 bytes; SHA-256
`fc3707fca505e7c980be7071b78d4f955a2b521265ed3235345fe787e4744948`),
authority ZIP (9,984,382 bytes; SHA-256
`fce50ece70181afd3fdcac2f65233c10866f3d5f743973282162befbfb700133`),
build receipt, licence, and manifest. Anonymous readback matched all seven.
The PASS receipt is `qa/UNIT_07_ZENODO_PUBLICATION.json`, 3,465 bytes,
SHA-256 `70f9f422062844f768b38ecbeb0e1ea8b50d49783d43ebaa6ae2f8c9d1b525f2`.

Figshare item 33314856 remains the existing public metadata-only work record
because the live licence menu exposes no exact CC BY-SA/mixed-rights choice.
It points to the Unit 7 Zenodo DOI and is verified in Indonesian collection
version 41 (`10.6084/m9.figshare.c.8668413.v41`). The PASS receipt is
`qa/UNIT_07_FIGSHARE_PUBLICATION.json`, 2,366 bytes, SHA-256
`c49440d47aba995af3d8b7f05600f09f8d69ba247f3622611d9b162d2f2c92df`.

Resume from `00_control/CURRENT_GOAL_AND_WORKFLOW.md`, `00_control/CURSOR.json`,
`qa/UNIT_07_RELEASE_CANDIDATE.json`, the two final publication receipts, and
this handoff. The release-candidate JSON is intentionally retained as the
historical prepublication snapshot; its stale reservation-hash suffix is
superseded by the verified reservation SHA-256 ending `...18b27` and the final
publication receipts. The next executable action is to freeze Lecture 8 and
Worksheet 8 authority, solutions, transclusions, media, PDFs, and component
rights, then translate the complete contiguous unit and extend the
reader/backend in source order.

The full production scope is unchanged: finish all 30 classical Brenner units,
then freeze/admit and translate all 30 units of Brenner's *Bündel, Garben und
Kohomologie* as the required second volume, while exposing the documented
19-unit learner route plus its original seam, mastery, integration, and
Stacks-navigation layer. Napkin remains optional reference evidence only;
Stacks remains downstream.
