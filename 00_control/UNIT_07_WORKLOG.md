# Unit 7 production worklog

Checkpoint: 2026-08-22 | State: translation, authority/media, terminology,
cumulative build, all reader QA, corrected native backend, additive common
backend, packaging, publication, and public readback closed

## Closed surfaces

- Binding lecture: page 165896, revision 1057689, MediaWiki SHA-1
  `482eacab21b84870389c23a5faac8493768fd522`.
- Binding worksheet: page 165926, revision 1112363, MediaWiki SHA-1
  `55af227ec3c8f90e9deb857925dcc7725dcf94e1`.
- Authority manifest: 103,034 bytes, SHA-256
  `6423629ff600ffcfc5067ea139eef01843ece1ce907dd4bda1bfdb12f49de96e`.
- Ordered 33-exercise map: 12,293 bytes, SHA-256
  `8dfcc09854b47d83eaf9179462449a0a1fa307a3a72e5d1f252cfce35858e0e1`.
- Three source solutions: Exercises 7.10/revision 1113188,
  7.11/revision 1112940, and 7.22/revision 1095499; no others invented.
- Nine reader-media positions, including three animated HTML GIFs, close over
  13 local binary surfaces. Rights SHA-256
  `e7245bdc9f499fb5b0b71e8598773257b6147147f8f2fe08f82597338946f24f`;
  closure SHA-256
  `2a9141295e9e8eae525917e5f6568823077aa67edd50383c431ad7146bde4130`.
- Authority narrative: `authority/UNIT_07_AUTHORITY_FREEZE.md`, 5,885 bytes,
  SHA-256
  `048b17280add22cd5d67d66a469b11cf3eb22bffc3c24c662741ca3c2e253f22`.

## Translated surfaces

- `source/id-ID/lecture-07.md`: 22,411 bytes, SHA-256
  `45023a789b52b562d2fbcd0aaf680453cf3dbef60c41542a89a42be01f63ff52`.
- `source/id-ID/worksheet-07.md`: 16,757 bytes, SHA-256
  `8350ea75756c19a05e09f51074366e4ba85829819690b20a84122c6f9d0e94d3`.
- `source/id-ID/worksheet-07-solutions.md`: 5,326 bytes, SHA-256
  `8c6c52e4aa7e6be203be41235c2bb7a97c2689e4226738f78d62175fe770ecbf`.
- Worksheet/solution re-audit PASS: 33 ordered entities, stars exactly 7.10,
  7.11, 7.22; seven submission values `6,9,4,6,4,6,6`; unique anchors and
  all internal links resolve; no active German prose.
- Corrections through `AGC-CORR-0019` and adaptations through
  `AGC-ADAPT-0016` are explicit in `00_control/CORRECTIONS.csv`, 18,076 bytes,
  SHA-256
  `0c0e853ff6d418f607958a8f06bd0b190c86b41e5df0d7f3e52ef6aa7fb48e34`.
- Cumulative frontmatter now preserves the source/human credit chain and
  records the exact tool provenance `OpenAI Codex gpt-5.6-sol, Ultra.`

## Terminology gate closed

The bounded official arXiv search found no suitable Indonesian TeX/e-print and
did not treat HTTP 429 responses as zero results. The honest fallback inspected
an Indonesian algebraic-curve PDF and an Indonesian commutative-algebra PDF.
`00_control/TERMINOLOGY_QA_20260822.md` records the sources and decision.
The exact frozen Unit 1-7 set now uses `lapangan` instead of `medan` at 117
occurrences and `gelanggang faktor` instead of `gelanggang hasil bagi` at 22
occurrences. The deterministic receipt is
`qa/TERMINOLOGY_MIGRATION_UNIT_07.json`, 8,933 bytes, SHA-256
`d290dff2d248ece69202ac1ebbe7cb386c280e46ce8f2f868ec6bfdbfba27de3`.
`00_control/TERMINOLOGY.csv` now has 54 unique term IDs, 7,688 bytes, SHA-256
`652c49d8a538fe1c82128b23f33c2f9fd8c38f35f52d5390129ade63c69e21c4`.

## Build and reader QA closed

- HTML: 7,733,142 bytes, SHA-256
  `e960f925d718d897f3308deae2404679f2ea9baf95e70b4dc8387b02b242dcc2`.
- PDF: 142 A4 pages, 5,322,352 bytes, SHA-256
  `729d1b4f5593d2695091fd72379df9df69cc3dccb3e6ca404fce705d3d834f56`.
- Build receipt: 17,228 bytes, SHA-256
  `ec37c31c30c354e3ebb2c5093ae6b5a7d4a89989cf2850574cffaa89db0b1156`.
- Machine, all-page visual, responsive-browser, and Unit 7 protected-surface
  QA all pass. Their receipt SHA-256 values are, respectively,
  `f0b243aa83440fd295742947bbfec75085581bb183857815635f2a5be7c21ad6`,
  `7f9915130e4ec89a01f49ff337281d7545e082b668325c5b60cb9c9aa05a9757`,
  `08e52316a9523f7bb0c3a4baedc61b6fc3d719e6f9153f6fa62da070a2146653`,
  and
  `05ebb1dfe3751cd7a9307347cdc04f607fa0eee3073a5c43246fb42e0bbfa6e8`.
- Coverage is seven lectures and worksheets, 197 exercises, 40 public source
  solutions, 53 reader-media positions, and 388 stable reader heading IDs.

## Backend gates closed

- Native backend: 5,182 records; 298,913-byte manifest SHA-256
  `8b482971c444a4e5d90695f084234924a873b671885428d98e9db447e4924967`;
  7,301,025-byte canonical JSONL SHA-256
  `663713a128a0e673a4daf9edd67f9c3dd10ebae02039f8e0c2044c0ca0fa14be`;
  279,800-byte backend-QA receipt SHA-256
  `670fdb5be09ca2fcbcb9c7f0f8ae0d8d603eb67e579dcc1256370b577a6ec0c7`.
  Deterministic double replay passes; all 5,179 prior IDs are preserved, three
  BGK architecture records are added, and the stale Napkin dependency is
  corrected.
- The additive common-backend-v1 adapter leaves the reader and native backend
  unchanged. It preserves all 5,182 native IDs and validates a virtual
  12,496-record, 18,829,519-byte stream with SHA-256
  `e4b3def75472c9eee06cdcf4ef6482f8f12913bd7ee7fc478b111b18df335d7f`.
  Exact reverse reconstruction reproduces the native JSONL hash and 29,223
  foreign keys close. `backend/common-backend-v1/MIGRATION_RECEIPT.json` is
  5,356 bytes, SHA-256
  `c7da3c77e226eec93cc2df286e96258097c3e7b45e2549ac77eafa5cdb354b16`.

## Packaging and public preservation closed

Zenodo record 22062319, DOI `10.5281/zenodo.22062319`, is public as `unit-07`
under concept DOI `10.5281/zenodo.22059686`. Its seven-file payload is:

- PDF: 5,322,352 bytes, SHA-256
  `729d1b4f5593d2695091fd72379df9df69cc3dccb3e6ca404fce705d3d834f56`;
- HTML: 7,733,142 bytes, SHA-256
  `e960f925d718d897f3308deae2404679f2ea9baf95e70b4dc8387b02b242dcc2`;
- source/backend ZIP: 6,945,957 bytes, SHA-256
  `fc3707fca505e7c980be7071b78d4f955a2b521265ed3235345fe787e4744948`;
- authority-witness ZIP: 9,984,382 bytes, SHA-256
  `fce50ece70181afd3fdcac2f65233c10866f3d5f743973282162befbfb700133`;
- build receipt, licence, and manifest with SHA-256, respectively,
  `ec37c31c30c354e3ebb2c5093ae6b5a7d4a89989cf2850574cffaa89db0b1156`,
  `6f6e91a9ad0bc29da479af84b361aeba1976d79d0f7462e7f0b7b7522d0d6054`,
  and `785adb3764463132fcdcebece3c6d4d69c9b8694ac298c8614ab775cd311618a`.

Anonymous readback reproduced all seven filenames, sizes, and SHA-256 values.
The sanitized PASS receipt is `qa/UNIT_07_ZENODO_PUBLICATION.json`, 3,465
bytes, SHA-256
`70f9f422062844f768b38ecbeb0e1ea8b50d49783d43ebaa6ae2f8c9d1b525f2`.

Figshare item 33314856 remains correctly metadata-only because its live
licence menu cannot represent CC BY-SA 4.0 text plus component media rights.
It points to the public Unit 7 DOI and is present in Indonesian collection
version 41, DOI `10.6084/m9.figshare.c.8668413.v41`. Its sanitized PASS receipt
is `qa/UNIT_07_FIGSHARE_PUBLICATION.json`, 2,366 bytes, SHA-256
`c49440d47aba995af3d8b7f05600f09f8d69ba247f3622611d9b162d2f2c92df`.

## Next executable action

Begin Lecture 8 and Worksheet 8 in source order: freeze exact revisions,
transclusions, solutions, official PDF witnesses, media and component rights;
then translate the complete contiguous unit and repeat the build/QA/backend
gates at the next cumulative boundary.

GitHub remains externally suspended; do not retry it. Do not contact upstream
during production.
