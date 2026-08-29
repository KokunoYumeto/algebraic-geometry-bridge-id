# BGK Unit 1 worklog

Status: complete local source/reader/native-backend boundary; publication is
reserved for the cumulative BGK Units 1--3 milestone. The classical Unit 30
release remains the latest public boundary. Next source cursor: BGK Unit 2.

## Course and unit authority

- Course: Holger Brenner, *Bündel, Garben und Kohomologie (Osnabrück
  2019--2020)*, exactly 30 lectures and 30 worksheets.
- Frozen course root: page 108997, revision 1052895, MediaWiki SHA-1
  `e881e7c53531765849865454d4d0c643c2066c6d`.
- Course manifest:
  `authority/wikiversity-bgk/course/COURSE_AUTHORITY_MANIFEST.json`, 34,279
  bytes, SHA-256
  `ea0bf346e261db8ed80b7565f7746e95c79e0c376d25d9fbce5d96879dff7dd8`.
- Official complete-course PDF: 265 US-Letter pages, 2,104,862 bytes,
  SHA-256
  `87655cf7e96dc0eaa185ca49a374dc9e25f4b739670495f423279aa332fce66c`.
  Current Commons metadata offers CC BY-SA 4.0; the embedded final-page
  notice says CC BY-SA 3.0. Both witnesses are preserved rather than flattened
  into a false blanket claim.
- Unit 1 lecture: page 109003, revision 1069568, MediaWiki SHA-1
  `6e619f166a640629f33e73ac518faff6daff2810`, 126 frozen semantic pages
  counting the root, and a 13-page official PDF (128,370 bytes, SHA-256
  `be4103eb7f4631f300c8f5f895de82094d0cd5ffac603eff9d5c7b77aef3d3ce`).
- Unit 1 worksheet: page 110204, revision 1069465, MediaWiki SHA-1
  `a2c9deb62e10eb9942aac56cde2e33aed04823fd`, 93 frozen semantic pages
  counting the root, exactly 17 ordered exercises, zero public solutions, and
  a five-page official PDF (53,425 bytes, SHA-256
  `0f65dad0173f0ad40d22cf5f255f9379aca90a090d0c54cc268379f8628ee70a`).
- Unit manifest:
  `authority/wikiversity-bgk/unit-01/UNIT_AUTHORITY_MANIFEST.json`, 97,184
  bytes, SHA-256
  `ad271f5ad69f9990dbe3082c22f8c52b7a4c58494c8f6614350078535d4f2ba1`;
  deterministic double freeze replay passed.
- Authority summary and QA:
  `authority/BGK_UNIT_01_AUTHORITY_FREEZE.md` (3,219 bytes, SHA-256
  `c00a9941b0939f3c979f7024bc52a066218494d53f283bf967ea90f50ff799d9`)
  and `qa/BGK_UNIT_01_AUTHORITY_QA.json` (3,657 bytes, SHA-256
  `2c42a091e5d9e12f8078839e8c520a0c258676548a392986e5452f521b2cb5a0`).

## Media and component rights

The one reader media position is the public-domain `Tangent_bundle.svg` by
Oleg Alexandrov. The frozen local PNG is 109,428 bytes, SHA-256
`768dd5ac37c85fad14c6ede7ddc45988341c03924d5f7e33e9f7223dd9896578`.
The source inline `PD`, Commons `{{PD-self}}`, author, description, source
revision, and the reported-versus-decoded thumbnail-height discrepancy are
preserved in `authority/RIGHTS-bgk-unit-01.csv` (2,426 bytes, SHA-256
`531f261e77454f43abb2100022aa50ed6e0537683da2d45163e9bd75412037d9`)
and `authority/ASSET_CLOSURE-bgk-unit-01.json` (5,748 bytes, SHA-256
`dcae12b926bfc620ca3ea6d71dc05a322ee9fa57a8b83420ba83e5bbdb96c6fa`).

## Translation and corrections

Complete id-ID source files:

- `frontmatter-bgk-units-01.md`: 2,608 bytes, SHA-256
  `9af2e091d41ee9f859c8af4e3cca854f74135b13417ed66d0a6d658cfa9ba2f7`.
- `lecture-01.md`: 26,365 bytes, SHA-256
  `ec8d58667fc732c63a5985942b46c7166856d07df48d97d2a79ab68065318658`.
- `worksheet-01.md`: 9,574 bytes, SHA-256
  `b5434601ae3ea24f7b580d59bad2b992383b840c7a2bdcdb4cbbfb92a40de7e9`.
- `worksheet-01-solutions.md`: 1,685 bytes, SHA-256
  `26f41e58dbb471de0a710c2bb7463f887834ce1994f6d53c94a8eeac807b8bb5`.

All 17 exercises preserve source order and identifiers; no solution was
invented. Thirty-seven `br-bgk-2019-*` heading IDs are unique and disjoint
from the 22,752 classical backend IDs. Six mathematically forced source
repairs are visibly disclosed and ledgered as `AGC-CORR-0136`--`0141`:
factor order and base-space errors in Example 1.1, the deleted-origin/product
notation in Example 1.2, the coordinate-name and cross-product-component
errors in Example 1.3, and the rank-symbol mismatch in Definition 1.4. The
source's cross-product reference to Lema 33.3 is retained. Thirteen BGK terms
are admitted as `AGT-0277`--`0289`. Exact provenance is
`OpenAI Codex gpt-5.6-sol, Ultra.` Translation receipt
`qa/BGK_UNIT_01_TRANSLATION_QA.json` is 3,595 bytes, SHA-256
`c1b815046172ebe42c07d3e1780c1ea4ccc9b510bb5da5430f90c1445fc9612a`.

## Reader and backend

The isolated self-contained reader passes deterministic double replay:

- HTML: 318,215 bytes, 357 browser MathML nodes, 37 stable anchors, one
  embedded rights-bound image, SHA-256
  `b36367d724ff2ac91f893f2ec07907a36e74cd5ab8d07e2d689a234dd7f7c447`.
- PDF: 18 A4 pages, 244,200 bytes, SHA-256
  `5e8529a77ad987dc1b7bc81bd621fc261f595f91e844a335cfd2b4799de5ad42`.
  All 18 pages were rendered and inspected; no clipping, overlap, broken
  glyph, or literal builder markup remains. The diagram is centered and
  legible. LuaTeX's sole random trailer ID is replaced by a fixed-width
  content-derived ID, making the PDF byte-stable.
- Desktop 1280x720 and phone 390x844 HTML checks pass with centered equal
  desktop margins, full-width mobile reflow, no document-level horizontal
  overflow, and internal scroll containment for 12 of 103 wide display-math
  blocks. The temporary viewport override was reset.
- Reader receipt: `qa/BGK_UNIT_01_READER_QA.json`, 3,324 bytes, SHA-256
  `8e65903c06f0f37b43227b0ff1498dbbadf956786b6256e9bbecba72541978e0`.
- Isolated native backend: `backend/bgk-units-01`, 746 records / 808,645
  bytes, records SHA-256
  `5700bfea56e5cb52de82d0cd23c5439348298f7112efdd3f58f36b14b392902e`;
  manifest SHA-256
  `451c4cc0ea4caf7a45aeef1edc1d7a9cc8c9e47026d843127020a40ba16177a6`.
  It contains 17 exercises, zero solutions, 294 semantic segments, six
  corrections, thirteen terms, one asset, and zero classical-ID collisions.
  Schema, graph closure, rights, source hashes, credential scan, canonical
  projection, and deterministic double replay pass. Receipt
  `qa/BGK_UNITS_01_BACKEND_QA.json` is 1,924 bytes, SHA-256
  `fef9809fdffef2f067fa08813b45e0b26b464538e801273d21996999ca33cf6e`.

## Next executable action

Freeze BGK Unit 2 into `authority/wikiversity-bgk/unit-02`, close its exact
exercise/solution/media/rights graph, translate the complete lecture and
worksheet in source order against the admitted BGK terminology, and run the
same bounded translation gates. Extend the cumulative reader/native backend
through Unit 2. Publish neither a one-unit Zenodo version nor a duplicate
concept; release the existing GitHub/Zenodo lineages at the substantial
BGK Units 1--3 checkpoint after cumulative reader/backend/common-adapter QA.
