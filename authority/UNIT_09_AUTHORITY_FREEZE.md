# Unit 9 authority freeze

Freeze date: 2026-08-23 | Status: complete immutable authority closure

## Boundary and provenance

This Unit 9 boundary is the raw Wikiversity witness set in
`authority/wikiversity/unit-09/`. The final v2 manifest pass reused and
independently hash-verified every raw witness; no witness was deleted. Because
the shared lane can expose concurrent task work, this note records the bytes
and source identities rather than assigning authorship to a session. The source
authority is the German Wikiversity course, not GitHub or a generated
translation.

The binding lecture is page 165898,
`Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 9`, revision
1112241, timestamp `2026-08-20T16:29:07Z`, MediaWiki SHA-1
`2a702891ae21267751c7900639ef3828faf949c2`.
Its immutable revision URL is
<https://de.wikiversity.org/w/index.php?oldid=1112241>.

The binding worksheet is page 165928,
`Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Arbeitsblatt 9`, revision
1059491, timestamp `2025-11-21T13:53:14Z`, MediaWiki SHA-1
`affd5b273368b8a02f7580671dc4b1431f7da9df`.
Its immutable revision URL is
<https://de.wikiversity.org/w/index.php?oldid=1059491>.

The `/latex` witnesses are lecture page 165962, revision 1033008, and
worksheet page 166022, revision 1033069. Both carry MediaWiki SHA-1
`3034e92c1843eab298fb5f6f859d2c89cf824d61`; their exact XML/HTML and derived
expanded-TeX surfaces are retained beside the entry witnesses.

`authority/wikiversity/unit-09/UNIT_AUTHORITY_MANIFEST.json` binds 35 raw and
derived files, is 102,154 bytes, and has SHA-256
`7cf7a956dffe854da9d021e3c74615573b91b5701d7e3b78a8f5f1aa45bfbc29`.
The ordered exercise map is 9,763 bytes, SHA-256
`c906ba0b1073a162f7f55289c0f60114063d011756f1eb907bcf342336729495`.

## Closure: transclusions, exercises, and public solutions

The lecture requests 113 unique transclusion titles (five API batches); all
113 current revisions were captured and none is missing. The worksheet
requests 109 unique titles (five batches); all 109 were captured and none is
missing. Every captured record retains page ID, revision ID, timestamp,
MediaWiki SHA-1, and source byte count.

The worksheet contains 24 ordered exercises. Exactly three public solutions
were present at this freeze; no solution is invented for the other 21:

- Exercise 9.6: page 100296, revision 1107958, MediaWiki SHA-1
  `bf77f16bf5c2f5e34c338f46636514e6615528cd`, immutable URL
  <https://de.wikiversity.org/w/index.php?oldid=1107958>.
- Exercise 9.13: page 167639, revision 1059490, MediaWiki SHA-1
  `307cf5074050c81bb7f2086ec79778a5430722cc`, immutable URL
  <https://de.wikiversity.org/w/index.php?oldid=1059490>.
- Exercise 9.18: page 94177, revision 1112817, MediaWiki SHA-1
  `8e05ddd8dd0211034c9ade13df4701c820ed88d0`, immutable URL
  <https://de.wikiversity.org/w/index.php?oldid=1112817>.

Their XML/HTML witnesses and exact hashes are recorded in the ordered map and
manifest. The three solution pages are source evidence only; translation may
not imply that the remaining exercises have public source solutions.

## Official PDF build witnesses

The official Lecture 9 PDF is a 9-page letter-size witness, 333,288 bytes,
SHA-256
`2892b347676e67ec103cb810426dc3f0eb1637ae06fac7b2a55a1710dac8c278`;
Commons MediaWiki SHA-1 `a64b654a70bb13da69848695df7d15af9e715ffc`, timestamp
`2026-02-02T15:50:36Z`, description URL
<https://commons.wikimedia.org/wiki/File:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)Vorlesung9.pdf>.

The official Worksheet 9 PDF is a 5-page letter-size witness, 135,835 bytes,
SHA-256
`86d84352a56e8b5c26bdb2002c4fe45c22e50a01430d65a8360d80f75007c07b`;
Commons MediaWiki SHA-1 `5208e5b9903df9f81fe7412d6b49b2fe3b85d001`, timestamp
`2026-02-03T11:46:25Z`, description URL
<https://commons.wikimedia.org/wiki/File:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)Arbeitsblatt9.pdf>.

Both PDFs are layout/build witnesses and do not override the binding textual
revisions. They are preserved under `authority/artifacts/` and are not counted
as reader-media positions.

## Media and component rights

The parse surfaces contain one substantive reader-media position,
`File:David Hilbert 1886.jpg`; the other four image references are the two
official PDF icons repeated across lecture and worksheet surfaces. The image is
346 by 479 pixels, 131,401 bytes, Commons SHA-1
`4137086db6ffdac418da54a84a7fd574d9fadbb9`, local SHA-256
`c64d462b61219ee497bae09e61067f3b410c6d9fb0a553f377be991230ec33d0`, uploaded
by Jacek Halicki, and marked **Public domain** in the frozen Commons
extmetadata. Its description is
<https://commons.wikimedia.org/wiki/File:David_Hilbert_1886.jpg>.

The exact metadata witness is `authority/commons-imageinfo-unit-09.json`,
2,793 bytes, SHA-256 `4ae52df0d68e315a4270011812ee0f69305ffa14aa06ea8d5615a8b77525ffc5`.
The rights CSV is `authority/RIGHTS-unit-09.csv`, 1,580 bytes, SHA-256
`1ac4707f08ec52438dbc8ac2e200be3343ca17bcfbe91501dc2f66ff9935f3a4`; the
asset closure is `authority/ASSET_CLOSURE-unit-09.json`, 1,065 bytes, SHA-256
`c267b8470ba1e5920f280338dbcf33aa2d3919f282730be6850ebf4ce4722819`; and the
reader credit note is `source/id-ID/media-credits-unit-09.md`, 471 bytes,
SHA-256 `f51ff5450b2822d80688e473a1b83f78cf7980b2f96ac39e1632bab01bdc7490`.
Course prose remains CC BY-SA 4.0; the image retains its independent public-
domain status and attribution provenance.

## Resume boundary

This is an authority/rights freeze only. No Indonesian translation or
publication is included. The next executable action is to translate the
complete Unit 9 lecture, worksheet, and exactly the three captured public
solutions in source order, preserving the 24-exercise topology and all IDs.
