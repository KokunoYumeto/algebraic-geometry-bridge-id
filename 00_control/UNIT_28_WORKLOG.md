# Unit 28 owner-production worklog

## Boundary and authority

Unit 28 is the fifth admitted unit from the official complete *Algebraische
Kurven (Osnabrück 2012)* course and remains in the `br-ak-2012-*` namespace.
Accepted Units 1–27 and their public bytes are the immutable baseline. This
checkpoint adds one lecture, one worksheet with 14 exercises, the sole public
source solution (Exercise 10), and four reader-media positions.

- Lecture: page 50734, revision 1052516, MediaWiki SHA-1
  `d037d0173bca4c443e06c7991d830568fa8dc0ea`.
- Worksheet: page 50763, revision 793497, MediaWiki SHA-1
  `7ee8f07ea803541b23e8e1fa686c7b2c17e6f67a`.
- Public solution 10: revision 1112869, MediaWiki SHA-1
  `85608d2ad2ee8515d39df596af6407dc0270b7f0`; all other 13 exact
  solution candidates are negatively closed.
- `authority/wikiversity/unit-28/UNIT_AUTHORITY_MANIFEST.json`: 134,460
  bytes, SHA-256
  `f2e34fc420c4beec300ea9e0accc52598e12c27f46c9022611996b1b43e29a99`.
- `authority/UNIT_28_AUTHORITY_FREEZE.md`: 5,425 bytes, SHA-256
  `acb9e2053e6f883953f05ff4f274f96aa70f7c6f8239667f47cc838627f313d2`.
- `qa/UNIT_28_AUTHORITY_QA.json`: PASS, 1,670 bytes, SHA-256
  `e6c5826d63697b57da35f2b3117652160ed2fd5652c7ec395554c1d9887c45b1`.

The interrupted bounded live replay completed before admission. It verified
164 unique semantic identities, both official PDFs, and all four Commons media
identities. The official lecture PDF is 106,537 bytes / 9 pages / SHA-256
`0d040f9a5663e6d0d7451f4de864a0712e35e08e961afc66d6742dfbee065609`;
the worksheet PDF is 45,643 bytes / 3 pages / SHA-256
`579b29f1250b346549522aadc465f7afa0c67b012b5d7ba76b4c6eb0c94a5d12`.

## Translation, mathematics, terminology, and rights

The final contiguous Indonesian source preserves all 19 lecture entities,
all 14 exercises in source order, the exact solution topology, four accessible
media positions, and 44 unique stable anchors.

- `source/id-ID/lecture-28.md`: 21,279 bytes, SHA-256
  `2a33c0e3049b0d2b140ee46b37f9fba452dca8f19c553317ddbee5c23f3768b7`.
- `source/id-ID/worksheet-28.md`: 7,393 bytes, SHA-256
  `fa6b7003de697739d3a03e00cb35b42119f1fff78836de536ba32584e33a361e`.
- `source/id-ID/worksheet-28-solutions.md`: 3,107 bytes, SHA-256
  `4428b2e180096f7ab719aa649f64e2caa3be03c71d1198a7c7747616b90dfbf5`.
- `source/id-ID/media-credits-unit-28.md`: 3,774 bytes, SHA-256
  `6155b47c596d97ea0af6f50f0c451453eca43231f8f04b4ad7617f36abfa1b52`.
- `source/id-ID/frontmatter-units-01-28.md`: 4,985 bytes, SHA-256
  `f2408d86b7eef190ca586c8041e3ac733784b91cf1bbf7445baed1b604b87d9c`.

Terminology rows `AGT-0250`–`AGT-0260` and correction rows
`AGC-CORR-0115`–`AGC-CORR-0125` are bound. Two proof expansions are visibly
labelled `Jembatan edisi`. The checked repairs include the `d=1` Fermat case,
the characteristic-two conic exception, the principal-open shrinking bridge,
lowest-term/smoothness detail in the public solution, and relative-versus-
ambient notation. Independent translation and math/rights audits closed with
no remaining actionables. `qa/UNIT_28_TRANSLATION_QA.json` is PASS, 6,913
bytes, SHA-256
`30095ba6d0621030c1a6d63d340ddb7d7d77fff424b2c28841d77e3e46da03ab`.

The translated text remains CC BY-SA 4.0; the four Unit 28 media items retain
their exact CC0/public-domain component rights. No blanket mixed-file-set
relicensing is claimed. `authority/RIGHTS-unit-28.csv` is 4,967 bytes,
SHA-256
`84e7132495c1f78bd71afb0c436e23322f90d05f81a74e2f088cb1b586321651`;
`authority/ASSET_CLOSURE-unit-28.json` is 12,939 bytes, SHA-256
`d7059564e2214dcafef6a8e0cd9cc43d7f2a86e70ca9e647719995cb0ef231b3`.

## Reader and deterministic QA

The cumulative reader covers 28 lectures, 28 worksheets, 671 exercises, 118
public source solutions, 98 media positions, 1,483 stable source IDs, and
10,717 MathML nodes.

- HTML: 23,412,216 bytes, SHA-256
  `b7cef9e6c08b696bde2f875a4766e6c35e975d4fd0901e414c3896014bbd9c10`.
- PDF: 15,820,212 bytes, 476 A4 pages, SHA-256
  `181b6fba2b5441fb7a5ab76a512e9d9ee2300e4201fd4632cac20a70bc703df6`.
- Build receipt: 43,674 bytes, SHA-256
  `5a843fdc6cb79ab3329e1f316027968e14ab2a0b765ff3505ad2af85003df5c3`.
- Machine QA: PASS, SHA-256
  `c666cb1186f516cead5ebd1a16de616856c99013cd94983826c974aebbdf776f`.
- Protected-surface QA: PASS, SHA-256
  `d9e737e3319f62d7560cbad20737c27b80b40c27536e3dca36d4632c98f18b2e`.
- Responsive QA: PASS, SHA-256
  `87358e05adf0530caab368ac60d98bbc4513d86412970996092d47b21ed7c204`.
- Visual QA: PASS, 9,055 bytes, SHA-256
  `859c16ec814bbe6243b40dde9d1760b88ada4fe763f739c824da7c3ca3b0fe1f`.

All 476 PDF pages were rasterized at 90 dpi and reviewed in 24 contact sheets;
pages 457, 462, and 463 were additionally inspected at full resolution after
the final repair. The proof marker is inline with its bridge paragraph, and
each topology figure is centered and immediately paired with its own credit.
The HTML is centered and page-filling on a 1440 px desktop viewport, reflows
without pagewide overflow at 390 px, contains all internal anchors, and loads
all 98 images with nonempty alt text. The deterministic writer binds the exact
PDF, page manifest, and all 24 reviewed contact sheets and reproduces the same
receipt on replay.

## Native backend

The cumulative native export contains 21,358 records. All 20,570 Unit 27
baseline records are preserved byte-for-byte; Unit 28 adds 788 records without
renaming its frozen `ex01`–`ex14` source IDs. The bounded parser accepts both
historical exercise-ID spellings while emitting the exact source spelling.

- `backend/units-01-28/MANIFEST.json`: 10,649 bytes, SHA-256
  `52ce204f9f0843bb8c7598a66073699ba2a139d29cfa741d8dc6a0d509a9c4a2`.
- `backend/units-01-28/records.jsonl`: 34,195,566 bytes, SHA-256
  `94e9c9d0859fc30cfa46a9cc08ed2babb7db07b586a3b5985a91130b096261ef`.
- `backend/units-01-28/record.schema.json`: SHA-256
  `3158825c0bd1c0da54c1c670630e7a8a2299b2b0d82e0f905042e76d7630906a`.
- `qa/UNITS_01_28_BACKEND_QA.json`: PASS, 5,766 bytes, SHA-256
  `af422532c47b1126dc776af923c9da4903deee2ba22a485ff048c96796150509`.

The QA gate independently regenerates the complete export and compares every
manifest and JSONL byte, validates global ordering/CRLF, all foreign endpoints,
source/authority/rights/ledger bindings, and exact model provenance.

The additive common-backend-v1 preflight also passes: 50,672 virtual records,
81,258,596 virtual JSONL bytes, SHA-256
`3bcebd137c6dca1a4705f6c1660043f9198faeef42faa1485a93e2686bf33b9c`,
120,703 foreign keys, 56 witness files, 7,790 strict profiles, and a lossless
reverse SHA-256 identical to the native records. The frozen migration receipt
is emitted only after the next Zenodo version identity is reserved.

## Remaining transaction

The release candidate is PASS (7,768 bytes, SHA-256
`38344286ddc85b7b18e1f66eef284bf47de277499883daae25da0bd4d9737cfd`).
Zenodo record 22105836 / DOI `10.5281/zenodo.22105836` is reserved as the next
version after record 22104692 in the existing concept; reservation receipt
`qa/UNIT_28_ZENODO_RESERVATION.json` is 1,090 bytes, SHA-256
`e0b70191dfe9613766cca9e38561ccf0dbbf353e8a20a12ace450502138cb3c1`.
The DOI-bound common migration receipt is PASS, 6,945 bytes, SHA-256
`39138e4eb6dbb5dee9698605dfa73a3f572b53d19e882b3a392a12111565786d`.

The reader-first eight-file package is published and anonymously verified on
both existing lineages. Zenodo record 22105836 matched all eight files by bytes
and SHA-256; `qa/UNIT_28_ZENODO_PUBLICATION.json` is 4,232 bytes, SHA-256
`c38838925c266a3b5a8d29fd2e31bbef1d0547e775b91f2ec532dc0093f9192a`.
GitHub content commit `915558629641eb894c43ff5ce67dd935c4168711`, annotated
tag object `9b79106e95013fee2558e30a0a11e743c34c4b87`, release `unit-28`,
and Pages are public. Credential-free smart HTTP verifies main and the tag;
anonymous direct downloads match all eight assets, fixed-commit raw readback
matches HTML/PDF and README/CITATION/LICENSE, and Pages matches HTML/PDF.
The final bounded anonymous replay passed at `2026-08-27T17:50:28Z`.
`qa/UNIT_28_GITHUB_PUBLICATION.json` is PASS, 9,243 bytes, SHA-256
`ba3cb54876941cc754c54921761d60f8622b144d1f4bc084770b7ce1ea90adb4`.

Next: preserve all accepted Unit 28/public bytes; freeze the official 2012 Unit
29 authority, then translate and verify Unit 29 in source order.

Provenance: OpenAI Codex gpt-5.6-sol, Ultra.
