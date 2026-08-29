# BGK Unit 6 worklog

Status: Unit 6 and the cumulative BGK Units 1--6 boundary are complete,
deterministically verified, published in the existing Zenodo and GitHub
lineages, and anonymously read back byte-for-byte.  The source cursor advances
to Unit 7.  Resume from this file,
`CURRENT_GOAL_AND_WORKFLOW.md`, and `CURSOR.json`; conversation summaries are
not state.

## Corpus/count guard

The admitted source core is exactly 60 distinct units / 602 official-source
PDF pages: 30 *Algebraische Kurven* units (337 pages) plus 30 *Bündel, Garben
und Kohomologie* (BGK) units (265 pages).  `D100` is a curriculum-role code,
not a unit count.  The 19-unit learner route is only a view over BGK and adds
zero units.  Unit 6 contributes 14 source-witness pages (7 lecture + 7
worksheet).  With the classical 30 units and BGK Units 1--6 complete, the
source cursor is 36/60 units and 421/602 official pages; BGK Units 7--30 remain
exactly 24 units / 181 pages.  The 82-page cumulative Indonesian reader is a
retypeset reader count, not another source corpus.

## Frozen authority and rights

- Course: Holger Brenner, *Bündel, Garben und Kohomologie (Osnabrück
  2019--2020)*, Unit 6.  Lecture page 109010, revision 1003728,
  MediaWiki SHA-1 `0dfea13421076e8f6486836e9fc799822bf52053`; worksheet
  page 110211, revision 900086, MediaWiki SHA-1
  `619536dcd80063470e12de7a3ebb3fc9fe1aa5e5`.
- The semantic closure captures 136/136 lecture and 109/109 worksheet
  transclusions with no missing page.  Expanded TeX is 19,454 bytes / SHA-256
  `0bdf28cb69d063b1782b7b42eb2212241e109f66ba382368dcd8e782d5ae829d`
  for the lecture and 11,703 bytes / SHA-256
  `0de1911162df14c38fa00755cf67583fbdd9b101134314e6d47a546922e875c1`
  for the worksheet.
- Authority manifest
  `authority/wikiversity-bgk/unit-06/UNIT_AUTHORITY_MANIFEST.json`: 107,618
  bytes, SHA-256
  `69a10e682e853c6f386afbc68438605846e5096220b21bd1e827c07633a79244`;
  all 31 declared files passed two deterministic resume replays.  Authority
  freeze: 7,083 bytes, SHA-256
  `6d8c217580f71cd2840521d6f7ecbdc80415c566058f7848890011bb2d10d45c`.
  Authority QA: 6,217 bytes, SHA-256
  `c22f362a9b1bc71d4f8497ac06e8f1264935977a7d43584178c941de613306ed`.
- Official lecture and worksheet PDF witnesses are respectively 89,016 bytes,
  7 pages, SHA-256
  `55fbef2b5d9eae950ac7ab064a8029f2e2932c49280a98a4a7ec6ed16262c75d`
  and 61,587 bytes, 7 pages, SHA-256
  `7b4f4569e7ab749a9e6affac715592316c109507d91971fd1c7b82cefaa825b5`.
  Page 6 is intentionally blank on both witnesses and page 7 carries the
  embedded rights notice.  Current Commons metadata and the embedded PDF
  notice remain separate rights surfaces; no blanket relicensing claim is
  made.
- Unit 6 has zero substantive reader-media positions.  Asset closure is 6,061
  bytes, SHA-256
  `9efa26ce4f4d0c0f95af36b7bba1efef15b55af9dcbd7533353e20c64f8f83b3`;
  rights CSV is 1,051 bytes, SHA-256
  `87f9d56b1300a56ca68e4aa8f50e3d50ab622d7a4d05221089d49e1dba35981d`;
  Commons metadata is 7,059 bytes, SHA-256
  `681014a0999f21f8ae99a31ae35003e215dc34a7604bbe35b6a18dbf7598d619`.

## Exercise/solution, translation, and source findings

The ordered map contains exactly 19 exercises in source order and zero public
solutions.  All 19 solution candidates are frozen negative results; no
solution was invented.  Translation files are:

- `source/id-ID/bgk/lecture-06.md`: 13,635 bytes, SHA-256
  `21307095f666ac32a57ce7413d3e7bb86ba2004856f79f1aaf7c1da16a9bbdbd`;
- `source/id-ID/bgk/worksheet-06.md`: 12,239 bytes, SHA-256
  `b7d99b21794723411f989fe8788bc6bff324f6c545fe24630fa0424f0d5fe1e5`;
- `source/id-ID/bgk/worksheet-06-solutions.md`: 1,848 bytes, SHA-256
  `29a48f9e3aef82d927f9c0b5bdd531882d894f5e0e646dfe581f2dab59cbdfd3`.

Translation QA is `qa/BGK_UNIT_06_TRANSLATION_QA.json`, 10,661 bytes,
SHA-256 `9b2c3c3a89f5ff48432d68ac26363b78d408e86ce9abfc42ad45b88d99b4fe9e`,
status PASS.  It proves 19/19 exercises, 0/0 solutions, 14 numbered lecture
entities, 5 proof bodies, 45 disjoint IDs, 5 source-anomaly classes, 7 visible
note placements, 5 correction rows (`AGC-CORR-0165`--`0169`), 10 terminology
rows (`AGT-0334`--`0343`), and Pandoc AST parses.  The five disclosed findings
are the worksheet grammar fault in 6.6; the `phi_1,phi_2` versus `p_1,p_2`
notation in 6.14--6.15; the worksheet grammar fault in 6.15; the
2014--2016 versus 2021--2023 year discrepancy; and the typed-section error
`F(V_i)` versus `F(phi^{-1}(V_i))` in the source proof of Lemma 6.10.  The
preferred Indonesian term is `funktor eksak-kiri`; the text and ledger have a
fail-closed spelling assertion.

Current append-only ledgers are `00_control/TERMINOLOGY.csv`, 54,358 bytes,
SHA-256 `eee5c52af4122e4a2ae4e14c8ef4df76302e388075ea73fb72e7a92fce80fc06`,
and `00_control/CORRECTIONS.csv`, 103,784 bytes, SHA-256
`23a2f4afa6955ecd729e1716dfa19610b7c0b728668b694f27af5aad409242b7`.

## Cumulative Units 1--6 reader and backend

The corrected reader frontmatter states the exact 101 exercises, three public
solutions (2.4, 3.1, 5.5), 98 negative solution results, and zero invented
solutions.  Two consecutive builds were byte-identical:

- HTML `build/reader-bgk-id/index.html`: 3,272,151 bytes, SHA-256
  `feb45d21d6168feaedf35719fdcb0b7f5532687846041d9fd75573c6d66fc5e9`;
- PDF `build/reader-bgk-id/bundel-berkas-dan-kohomologi-id-units-01-06.pdf`:
  896,202 bytes, 82 A4 pages, SHA-256
  `f89a622f15acab90f683fb2a0b72a150363fc71d0f41f971c48b8c8ee43c2c9b`;
- build receipt: 10,118 bytes, SHA-256
  `e69b24950f0d7ede5cf8c33b6bec32298c08555758936193e1bb4a002844937b`.

Machine reader QA is 6,369 bytes, SHA-256
`8c40f147451888e3ab4c2da95d164388c4f5725d37e121f020842da9488e250c`,
status `PASS_MACHINE_READER_82_A4_PAGES`.  All 82 pages were rasterized at
110 DPI and reviewed through five exhaustive contact sheets; pages 5, 6, 76,
77, 81, and 82 were also reviewed full-size.  Visual QA is 28,173 bytes,
SHA-256 `3c8ed7f411124cbeb3dbaeead04b768606caa4d0789a41235b52df80806b2c68`,
status PASS.  Responsive QA is 16,164 bytes, SHA-256
`755494a526f1d23e81ec797859a12dd9fb6bcea639b5dc53fada4136d7a5b0f0`,
status PASS: desktop content is centered at 972 px; mobile content reflows at
343 px with no document-level horizontal overflow; 31 intrinsically wide math
blocks use bounded local scrolling; all 237 internal anchors close.

The native backend contains 4,239 records, the exact 2,919-record Units 1--4
byte prefix plus 1,320 new records.  It contains 101 exercises and exactly
three public solutions.  Manifest: 25,100 bytes, SHA-256
`35438f7b9a1c3a833f5f6090041d3ee125fcbbc28c5ef5660579362ac2292e06`;
records: 4,762,198 bytes, SHA-256
`23e326a4a6c33abb1a4a0b10b91a673a74b056d8eb48e15a7681310d07c86986`;
backend QA: 4,164 bytes, SHA-256
`9ea9da9846590730d34ef4dc69749d0538972fef52b0f964fcefdfe9fbc80214`,
status PASS.  Schema, foreign-key, rights, projection, prefix, credential,
provenance, and classical/BGK namespace-disjointness gates pass.

Rights statement: the frozen semantic course and Indonesian derivative are
CC BY-SA 4.0 with attribution, changes, ShareAlike, and non-endorsement
preserved; every component retains its own recorded notice.  Provenance is
exactly `OpenAI Codex gpt-5.6-sol, Ultra.`

## Adapter, package, and public preservation

The additive common-backend preflight is 6,011 bytes, SHA-256
`204045f5b43ca0e695e6706ac7f5884063ac0835c6e29ae4b6cd1e65fe33f246`,
status PASS. It validates 10,167 common records, 1,621 strict profiles, 33
witness files, and 23,900 foreign keys; the 14,274,006-byte virtual stream has
SHA-256 `505e386794750902497e1847333bb153402d4da544ab19e4424ee6a6471b36ae`
and reverses exactly to the native records hash. The final migration receipt
is 6,966 bytes, SHA-256
`2f634414e965b2e392e578c2bbb6fe61ab4c0bc97a9f2e4883846fe8e85e29b7`;
the terminology receipt is 8,419 bytes, SHA-256
`407c0a77c8a40db496b4e4fda81becef507d3fb6aee6c9b809d98342157f5e80`.

The deterministic reader-first package contains nine files totaling
7,528,796 bytes. Its manifest is 5,287 bytes, SHA-256
`73f3fc58c1f0add8e0b2e1925f0ed725298aa97100c3eb9d4ff848acff630fe8`;
checksums are 774 bytes, SHA-256
`e80494c2ea9de3cf28a1215a3418afe9da6c9828ab3e0717f8ff788ff3d34b9a`;
release QA is 37,175 bytes, SHA-256
`c68187d17287c4776ad74da827c18b6cff49c2e304a2469c3beba4232ba7d46f`,
status PASS.

Zenodo record 22164552 / DOI `10.5281/zenodo.22164552`, version
`ak-unit-30+bgk-unit-06`, is public in concept `10.5281/zenodo.22059686`.
Anonymous readback matched all 18 files; receipt
`qa/BGK_UNITS_01_06_ZENODO_PUBLICATION.json` is 6,345 bytes, SHA-256
`a97ac072e4d2f433fbec802c6c1ce4b13ba1a7cd449b275066ca2edee86ce4f1`.
The identical checkpoint is public at GitHub content commit
`bfcdba0f48f88295720faada442df1ffc914095c`, annotated tag object
`0fbc0661739eddb21ab57a250f4121482864ae65`, tag/release `bgk-unit-06`, and
Pages `/bgk/`. Anonymous public web/Git transport matched the repository,
annotated-tag peel, all ten release assets, five fixed-commit files, and both
Pages files. Receipt `qa/BGK_UNITS_01_06_GITHUB_PUBLICATION.json` is 8,892
bytes, SHA-256
`29cc2672a76bb2253b7b3ef767b41b122cdf7df736bfe31e6fa7f0b27567f4f1`.

## Next executable action

Freeze BGK Unit 7's exact official lecture/worksheet revisions, semantic
closures, exercise and public-solution map, PDF witnesses, media and component
rights. Then translate its lecture, worksheet, and frozen solution scope in
source order without altering accepted Units 1--6. Run the bounded per-unit
authority, mathematics, identifiers, terminology, rights, and translation
gates before continuing to the next substantial cumulative release milestone.
