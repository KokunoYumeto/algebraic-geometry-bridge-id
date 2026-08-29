# BGK Unit 5 worklog

Status: complete local Unit 5 translation and deterministic QA boundary.  This
is not a separate publication.  The next executable source action is to freeze
and translate BGK Unit 6; the next external release is the cumulative BGK
Units 1--6 checkpoint.  Resume from this file, `CURRENT_GOAL_AND_WORKFLOW.md`,
and `CURSOR.json`; do not use conversation text or compaction as state.

## Corpus/count guard

The admitted source core is 60 distinct units / 602 official-PDF pages: 30
*Algebraische Kurven* units (337 pages) plus 30 BGK units (265 pages).  The
19-unit learner route is only a view over BGK and adds no units.  Local BGK
coverage is now Units 1--5 (35 of 60 total source units overall); BGK Units
6--30 remain 25 units and 195 official-source PDF pages.  `D100` is a role
identifier, not a count.

## Frozen authority

- Course: Holger Brenner, *Bündel, Garben und Kohomologie (Osnabrück
  2019--2020)*, Unit 5.  Lecture page 109009, revision 1003725,
  timestamp `2025-06-08T15:27:50Z`, MediaWiki SHA-1
  `1697741995f2c7537d0b38edc16fe8df38024e13`; source URL
  `https://de.wikiversity.org/w/index.php?oldid=1003725`.
  Worksheet page 110210, revision 619386, timestamp
  `2020-02-17T12:38:11Z`, MediaWiki SHA-1
  `7ea9208cb3444aa48e23d1acbe66e27672d28d27`; source URL
  `https://de.wikiversity.org/w/index.php?oldid=619386`.
- The semantic closure is the complete 105/105 lecture and 68/68 worksheet
  transclusion capture.  Terminal `/latex` witnesses are lecture page 110013,
  revision 807072 and worksheet page 117160, revision 807042; both have
  MediaWiki SHA-1 `1d092e4f15139d9908d36c4d64a1f4fde570e1ba`.
- Expanded lecture TeX: 17,843 bytes, SHA-256
  `d5d29f43c3209ccf8c8f80290ba3e44e800552807d4975ae0e78cb2dcd73735f`.
  Expanded worksheet TeX: 6,490 bytes, SHA-256
  `af4235ab3c393b02ad8f081f8f8fb17c24067fa07af63ec7f9bb3f17e1526b86`.
- Authority manifest
  `authority/wikiversity-bgk/unit-05/UNIT_AUTHORITY_MANIFEST.json`: 78,720
  bytes, SHA-256
  `328774ffd66341ba8841b86935037a043067202dd10916d3e0be5082faeac35e`.
  All 30 declared file records were independently recomputed; two complete
  `--resume` replays reproduced that hash.  Capture identity is
  `authority/wikiversity-bgk/unit-05/CAPTURE_IDENTITY.json`, 672 bytes,
  SHA-256 `6da189a35c244dd920c72805d807ed639472d34a30ac7f8825857539142dcf15`.
- Official lecture PDF witness: 74,961 bytes, 7 pages, SHA-256
  `85be007896876a0717ef5eddfe64ed919aeb6559dce44ec2828ffe2b1d755085`.
  Official worksheet PDF witness: 38,216 bytes, 3 pages, SHA-256
  `206418f092c563128b3dbf893b8547dc6db727773d4e4ec88e07140886d79113`.
  Poppler and pypdf page counts/boxes agree; all 10 pages were visually
  reviewed.  Lecture page 6 is intentionally blank in the source.  Embedded
  PDF notices (CC-by-sa 3.0) and current Commons metadata (CC BY-SA 4.0) are
  preserved as separate surfaces; no blanket relicensing claim is made.

## Exercise, solution, media, and rights closure

The ordered map `authority/wikiversity-bgk/unit-05/ORDERED_EXERCISE_MAP.json`
is 4,769 bytes, SHA-256
`b6bf28ef883ac91c07d0c50526ff655b2bcf7fc1b0d45773f0543092d463cadf` and
contains exactly 11 exercises in source order.  Exactly one public source
solution exists (Exercise 5.5): XML 4,856 bytes, SHA-256
`95fa2f0799fb9bfbfe0d9475a42c061ea805618e25e31560a6004da4672c5c86`, HTML
9,298 bytes, SHA-256
`04c72e340da0acd5220449d60b5bc1d18e30d2808f549600b5288910de26d406`, page
116432 revision 1112696, MediaWiki SHA-1
`0d2b14ff95268801b6ec1fdea9771b8e505725c8`.  Candidate evidence records the
other ten as absent; no solution was invented.  The media closure,
`authority/ASSET_CLOSURE-bgk-unit-05.json`, is 6,060 bytes, SHA-256
`c1e2145df10a647b185cbdb79f4d8d215a253604242fb694aa057b08cf3c34a3`; rights
CSV is 1,051 bytes, SHA-256
`87f9d56b1300a56ca68e4aa8f50e3d50ab622d7a4d05221089d49e1dba35981d`; Commons
metadata is 7,059 bytes, SHA-256
`09fff01c6ed1a153c4970265001b0251c705e51142ca022a9c7260cfff74edf2`; and
the Indonesian media-credit file is 666 bytes, SHA-256
`c2e2db42f0ad4479c84ab0c00b1cb72f3fafd2e6e0ce291d32cbc03e10fcdf9`.  There
are zero substantive reader-media positions (the two PDFs are authority
witnesses only).

## Translation and QA

- Lecture `source/id-ID/bgk/lecture-05.md`: 16,159 bytes, SHA-256
  `bd2a9242bce613ad95f3d7c99bdcb5d94c007722673c9c1facef57833725b22c`.
- Worksheet `source/id-ID/bgk/worksheet-05.md`: 6,303 bytes, SHA-256
  `0acb297084d14bd202bffcce31fe760d04ed2017a58565233cea78aa9d2f8932`.
- Public-solution scope file `source/id-ID/bgk/worksheet-05-solutions.md`:
  3,693 bytes, SHA-256
  `9045107729977f6f3169b198e603a19bf0072d23ada39b8f4b06655e421c2c9b`.
- Translation receipt `qa/BGK_UNIT_05_TRANSLATION_QA.json`: 6,137 bytes,
  SHA-256 `95735e6853026cd7c6a4eea0ccd9d53dfdd22d25cea017ae3297cc9c35668f68`,
  status `PASS`.  It proves 9 numbered lecture entities, 2 proof positions,
  29 heading IDs with no collisions, 11/11 exercises, 1 public solution,
  10 negative solution candidates, 6 visible source-anomaly classes with 5
  note placements, 6 correction rows, 10 terminology rows, zero reader media,
  stable-ID disjointness, exact formula/source witnesses, and Pandoc AST
  parses for all three files (153/57/25 math nodes respectively).  Authority
  QA is `qa/BGK_UNIT_05_AUTHORITY_QA.json`, 13,621 bytes, SHA-256
  `ecb9560bcbf866043e7c6602f2852dc21cc5aeadfae6fa889048ed89fc12408f`.
- Six source findings remain visibly disclosed rather than silently repaired:
  the omitted open qualifier, two matrix/type issues, section-versus-germ
  typing, the solution's section/germ wording, and the German article typo.
  Their Indonesian treatment is recorded in correction IDs
  `AGC-CORR-0159`--`AGC-CORR-0164`.  New admitted terms are
  `AGT-0324`--`AGT-0333` (including *berkasisasi*, *subberkas*, and *berkas
  hasil bagi*).  Current ledger hashes are TERMINOLOGY.csv 52,726 bytes,
  SHA-256 `581ee3786c9d1c2f958ae29f516dcca18dbc0a460bbdb4f14e2f7fd97da9314a`,
  and CORRECTIONS.csv 101,380 bytes, SHA-256
  `d4b682709a4bc0fe28bf20b3b9e6389bacea4ac6da52d1161f462b2b01f8b21c`.
- Rights statement: the frozen semantic course and Indonesian derivative are
  CC BY-SA 4.0, with attribution, share-alike, and non-endorsement preserved;
  component notices remain explicit and are not collapsed into a false
  uniform licence.  Provenance is exactly `OpenAI Codex gpt-5.6-sol, Ultra.`

## Next action

Bind this completed Unit 5 boundary into `CURSOR.json` and the current section
of `CURRENT_GOAL_AND_WORKFLOW.md`, setting the live next unit to 6 and the
remaining BGK count to 25 units / 195 official pages.  Then freeze Unit 6 from
the same course root, translate it in source order, and run its authority,
rights, exercise/solution, terminology, correction, reader, and backend gates.
Do not publish a Unit 5 micro-release; after Unit 6 passes, build and visually
inspect the cumulative Units 1--6 HTML/PDF, export and validate the native and
additive common backend, package reader-first files, publish to the existing
Zenodo/GitHub lineages under standing authorization, anonymously read back all
new public bytes, and record the sanitized receipts before advancing to Unit 7.
