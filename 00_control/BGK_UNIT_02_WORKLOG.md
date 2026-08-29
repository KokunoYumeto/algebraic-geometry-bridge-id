# BGK Unit 2 worklog

Date: 2026-08-29  
Status: complete local cumulative boundary through BGK Unit 2; no micro-release  
Course: Holger Brenner, *Bündel, Garben und Kohomologie (Osnabrück 2019--2020)*  
Language: Bahasa Indonesia (`id-ID`)  
Provenance: OpenAI Codex gpt-5.6-sol, Ultra.

## Scope and authority

This boundary preserves Lecture 2 and Worksheet 2 in their complete semantic
order. The immutable authority manifest is
`authority/wikiversity-bgk/unit-02/UNIT_AUTHORITY_MANIFEST.json`, 106,216
bytes, SHA-256
`a348b56811fe98266feff9108a21a436a9b8f07a343321feab7d9fbb3b75e64d`.
Two consecutive resume captures were byte-identical.

- Lecture: page 109004, revision 1019972, `2025-08-09T13:35:26Z`,
  MediaWiki SHA-1 `d666b90510ef490f9a1d545df6394ebc55d5dcc5`.
- Worksheet: page 109933, revision 602852, `2019-11-07T19:47:37Z`,
  MediaWiki SHA-1 `2b4d2f17b77698aee7b936476560869c442ab30f`.
- Lecture `/latex`: page 110011, revision 807058; worksheet `/latex`: page
  117157, revision 807028. Both have MediaWiki SHA-1
  `1d092e4f15139d9908d36c4d64a1f4fde570e1ba`.
- Lecture closure: 116/116 transclusions; expanded TeX 20,219 bytes, SHA-256
  `ae973e45a0aa3228ac31a61dd71b995d7872bfaaf8adca164bd97bd045f000b3`.
- Worksheet closure: 113/113 transclusions; expanded TeX 13,510 bytes,
  SHA-256
  `6aaed409db9e572b53def3dd35c3b9a5cb6d4467d8d5c3a4360ac6b24d78ccdd`.
- The ordered map binds exactly 27 exercises. Exactly Exercise 2.4 has a
  frozen public solution: page 77727, revision 1096699, MediaWiki SHA-1
  `64a726dc965e322b03e5eb0797f109cb45ab5125`. The other 26 candidates are
  negative; no solution was invented.
- Official witnesses: lecture PDF 421,840 bytes / 9 pages / SHA-256
  `b898d226f1b680d4fe08873402847c9580d05aca8ca430ea8e6cca466cbbc391`;
  worksheet PDF 62,885 bytes / 7 pages / SHA-256
  `afb4cdbe2c089d7d26ba66be112a2222b84e0e1e5f862960a3707fb20708f6b2`.

Authority summary `authority/BGK_UNIT_02_AUTHORITY_FREEZE.md` is 3,421 bytes,
SHA-256 `f0942526a7e9669aa918820a587c82ee10e81de8a0622e583a66520ada606f4b`.
Receipt `qa/BGK_UNIT_02_AUTHORITY_QA.json` is 3,444 bytes, SHA-256
`56b4dec14089b86721ca8dfc7ec95c1593619d30433529f912e1f498aae0ef92`.
Independent audit found all 32 declared authority files, zero mismatches, and
zero undeclared extras.

## Component media and rights

The reader has three ordered media positions. The HTML keeps the original
24-frame Möbius-strip GIF; PDF uses only its deterministic first-frame
companion. The other assets are the 500-by-500 hairy-ball JPG and the
500-by-400 inclusion-exclusion PNG. Their distinct reuse terms remain bound:
CC BY-SA 3.0, Public Domain, and CC BY-SA 4.0 respectively. The source-inline
CC label / current Commons Public Domain discrepancy for the inclusion diagram
is preserved rather than silently collapsed.

- Closure: `authority/ASSET_CLOSURE-bgk-unit-02.json`, 12,436 bytes,
  SHA-256 `902522f5a7231d562dc09f30bbd13b76ed5c087b17fd533b7d5cc71c0fd4844d`.
- Rights: `authority/RIGHTS-bgk-unit-02.csv`, 5,766 bytes, SHA-256
  `bc85cef5f20150941f3a6492c67702bcddd3d23bdd6ac5939c0148e5d57dc9f6`.
- Commons metadata: `authority/commons-imageinfo-bgk-unit-02.json`, 16,255
  bytes, SHA-256
  `d35c85d8e57594b709d5a771a4322c27eb34ebac16f3244de9f5572bd465b5ea`.
- Reader credits: `source/id-ID/media-credits-bgk-unit-02.md`, 1,943 bytes,
  SHA-256 `cec28c3bd197ffb7aabadfa0d67ddf8945cc7899834c4470780618ca60008158`.

An owner resume replay reproduced the closure bytes. Static images, all GIF
frames, the PDF companion, and the official-PDF rights pages were visually
checked.

## Translation and disclosed repairs

- `source/id-ID/bgk/frontmatter-bgk-units-01-02.md`: 3,634 bytes, SHA-256
  `fcc4e32f33bc886b415e77c337af9507fc3789a5e27fc1bd72999ad975b11cac`.
- `source/id-ID/bgk/lecture-02.md`: 16,648 bytes, SHA-256
  `317fe26b62230198c445f630aba95124bd9ac10d8b3f677ebc395630379b2d81`.
- `source/id-ID/bgk/worksheet-02.md`: 14,314 bytes, SHA-256
  `65d5f040639d8e5b9afa87477d13f3cb96d79c6e52b54662fdb6d814d38ed51d`.
- `source/id-ID/bgk/worksheet-02-solutions.md`: 4,299 bytes, SHA-256
  `8344276b9d613ef5ac55fabf82dafadb9b3385c93492b8508bdfd70a2b0ac12e`.

The translation preserves all 27 exercises, the sole public solution, 12
numbered lecture entities, 52 new cumulative-frontmatter/Unit-2 heading IDs,
27 closed cross-references, and all three media positions. Pandoc parsing
passes for all four source files. Nine new terminology rows `AGT-0290`--
`AGT-0298` were added and `AGT-0241` was reused.

Seven repairs are visibly disclosed and append-only in `CORRECTIONS.csv`:
`AGC-CORR-0142`--`AGC-CORR-0148`. They correct the gluing direction indices,
two ill-typed compositions, a vector-bundle map index, undefined variables in
the Möbius comparison, the swapped trigonometric parameterization in Exercise
2.23, the origin-singular denominator in public Solution 2.4, and duplicated
German/missing subscripts in that solution. Exact source forms remain in the
notes and ledger. Symbolic residual checks for Exercise 2.23 and the corrected
solution field are zero.

Translation QA script `scripts/qa_bgk_unit_02_translation.py` is 14,276 bytes,
SHA-256 `cc14406ed12d945521b7cb5e948f789aa064a92c2c74c5e5c9c445b21dba7c41`.
Receipt `qa/BGK_UNIT_02_TRANSLATION_QA.json` is 5,489 bytes, SHA-256
`285b29c9b4d9ebd938b1106f5b84e2fd6ad3509edbad79f66ebe10d29b42ffee`;
status `PASS`.

## Cumulative reader through Units 1--2

`scripts/build_bgk_reader.py` was generalized to take a cumulative unit
boundary while binding each frozen media closure. It preserves the GIF in
HTML and uses only an explicitly declared `pdf_local_path` in PDF. Unit 1
rebuilds byte-identically.

- HTML: `build/reader-bgk-id/index.html`, 2,701,882 bytes, SHA-256
  `2223059ff8faf23caa88cb14a365cf3e737fb32e36a017ec33d1a20a9f48aa14`.
- PDF: `build/reader-bgk-id/bundel-berkas-dan-kohomologi-id-units-01-02.pdf`,
  534,650 bytes / 36 A4 pages, SHA-256
  `8b85a8e025a349a1e68ba4ac7c9fe196f898e264bc8f7ec0eaab22bd6ecd3dae`.
- Build receipt: 4,938 bytes, SHA-256
  `aff0d30da72942538851629695bc5742a3e481c5f9da1f1e2a2b8dcd058c18f1`.
- Reader QA: `qa/BGK_UNITS_01_02_READER_QA.json`, 4,159 bytes, SHA-256
  `21b820e5cf2029c977d365dbb058db851fbf4411933e5abec9a9a9359db135b1`.

Two builds are byte-identical after fixed-width trailer-ID normalization. All
36 pages were rasterized and inspected. Fonts are embedded; there is no
clipping, overlap, broken glyph, unreadable formula, or broken builder markup.
Chromium checks pass at 1280-by-720 and 390-by-844: centered content, no
document overflow, four centered images with nonempty alternatives, no broken
internal link, zero console warnings/errors, and 15 wide phone formulas
contained by local horizontal scrolling.

## Cumulative native backend through Units 1--2

- Exporter `scripts/export_backend_bgk_units_01_02.py`: 42,905 bytes,
  SHA-256 `c4d1c3c7c65e5a391f97077cf1fe259441e9640007d8be3152abb2ececd407bf`.
- Manifest `backend/bgk-units-01-02/MANIFEST.json`: 14,360 bytes, SHA-256
  `148e2fe07927d9716b0f57b6ee4ca2543a1063e07f0599e8ec61fb4a1eab9285`.
- Records `backend/bgk-units-01-02/records.jsonl`: 1,735,219 bytes, 1,556
  records, SHA-256
  `e61150270d3470a554992da5d05d9e53f93d44bc4eb2887120c20b7ff403adf9`.
- QA script `scripts/qa_backend_bgk_units_01_02.py`: 12,920 bytes, SHA-256
  `a3e2961a91a864a71f6918ae32e98e688daa06bb53ce464061382b8888605a1e`.
- Receipt `qa/BGK_UNITS_01_02_BACKEND_QA.json`: 2,426 bytes, SHA-256
  `8c9fc8a6193a95dd195eeea0e6601fdf6577256657d59bd68b4085b5913e4c91`.

Owner and independent audits pass. The 1,556 rows comprise all 746 immutable
Unit 1 rows plus 810 Unit 2 rows. JSON Schema, stable-ID uniqueness, parent,
rights, concept and relation endpoint closure, class projection round-trip,
exact 44-exercise/one-solution topology, exact terminology/correction closure,
credential scan, and deterministic double replay pass. Every new row carries
the exact model provenance. Intersection with all 22,752 classical IDs is
empty. The common-backend adapter is intentionally deferred to the substantial
Units 1--3 release boundary.

## Commands and next action

The final independent backend replay was:

```text
python -m py_compile scripts\export_backend_bgk_units_01_02.py scripts\qa_backend_bgk_units_01_02.py
python scripts\qa_backend_bgk_units_01_02.py
```

No Git or external publication transaction occurred at this two-unit local
boundary. Preserve all accepted Unit 1--2 bytes. The next executable action is
to complete and independently audit the already-started BGK Unit 3
authority/media freeze, translate it completely in source order, extend the
cumulative reader/native backend/common adapter through Unit 3, then publish
that coherent checkpoint in the existing GitHub and Zenodo lineages and
anonymously read back every public artifact.
