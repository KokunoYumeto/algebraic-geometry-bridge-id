# Unit 20 authority freeze

Status: frozen and independently replay-verified on 2026-08-25.

## Official course surfaces

- Lecture: `Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 20`,
  page 165909, revision 1112311, timestamp `2026-08-21T09:10:26Z`,
  MediaWiki SHA-1 `74eb303dc659cb8131aaaee6948962210f063f4e`.
- Worksheet: `Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Arbeitsblatt 20`,
  page 165939, revision 1062603, timestamp `2025-12-18T10:53:10Z`,
  MediaWiki SHA-1 `97db112f709b6ab16f89b88f6d4e3da127c7802a`.
- Lecture and worksheet closures contain respectively 118 and 120 captured
  transclusions, with no missing page. A final live-identity recheck against
  both entry revisions passed.
- `authority/wikiversity/unit-20/UNIT_AUTHORITY_MANIFEST.json` binds 56 files,
  is 129,387 bytes, and has SHA-256
  `b063e5edc556cd18598389083ea27ea7f255edfe2ae00e13ebf24de76e5b37d7`.
  An independent local replay found no byte-count or SHA-256 mismatch.

The official `/latex` pages are nine-byte `{{latex}}` launchers, not immutable
expanded source. The freeze therefore binds both launcher revisions, exact
entry XML/HTML, complete revision-resolved transclusion closures, and generated
expanded-TeX snapshots. `lecture-20-expanded.tex` is 20,917 bytes with SHA-256
`8d95abad821218ccc9a32b3b7d57f8696b57bb98991c707f4ef8e5a20a1bdecc`;
`worksheet-20-expanded.tex` is 10,753 bytes with SHA-256
`c8998ecb3b461041a25272e2e4849011103b66326a51bac1936d2a40f1423912`.
The expanded snapshots aid production, while the frozen revision and
transclusion witnesses remain the semantic authority.

## Exercise and solution closure

The ordered worksheet contains 23 exercises. Exercises 1--18 are practice;
Exercises 19--23 are submitted work worth respectively 3, 6, 5, 4, and 2
points. Public source solutions exist only for Exercises 1, 3, 4, 5, 12, 13,
14, and 17, at revisions 612937, 1113196, 1054377, 1090115, 1112402,
1095226, 1096447, and 1096446. The 13,502-byte map
`authority/wikiversity/unit-20/ORDERED_EXERCISE_MAP.json` has SHA-256
`c74da7b0627cf8c8c694c0a9f20e94b0c7dc00ecd6c95b72ad21ae4a6c5c07ea`.
No other solution is admitted.

Solutions 1 and 4 are wrapper pages. Their full proof bodies are separately
frozen with their recursive dependencies: revision 1108353, MediaWiki SHA-1
`9f6d9367645cdcd128634774c3252285ddd1601c`, 12 captured pages; and revision
1101325, MediaWiki SHA-1
`e40f2a19e4dd4db9b1b176d1032a1cb4e6cfbded`, 14 captured pages.

## PDFs, media, and component rights

- Official lecture PDF: 217,144 bytes, 7 pages, SHA-256
  `f9ee520ac2724e041eb8861e4648e59e6357b71d68bf73e7a634a91178d45f9a`.
- Official worksheet PDF: 164,793 bytes, 5 pages, SHA-256
  `d141d76231053dabe89e4af0113e080abd57ee7f7dfc74877bcaa7ad4d48ec9d`.
- The reader has one substantive media position, `File:Whitney unbrella.png`.
  Its exact frozen Commons original is
  `authority/assets/Whitney_unbrella.png`, 35,829 bytes, 267 by 209 pixels,
  SHA-256
  `5a469c4675d326a753dca7801524138e64689e476d38d867070f97983f8b07d2`.
- Frozen Commons metadata credits Claudio Rocchini and offers GFDL 1.2+, CC
  BY-SA 3.0, and CC BY 2.5. The Wikiversity inline label and lecture-PDF
  appendix instead say `CC-BY-SA-2.5`, which is not an option in the frozen
  Commons record. This edition binds reuse to the explicit Commons CC BY 2.5
  option and preserves the conflicting source label as provenance.
- The two official PDFs are current CC BY-SA 4.0 course components, although
  their internal boilerplate still says CC BY-SA 3.0. The discrepancy is
  retained, and the PDFs serve as visual witnesses rather than substitutes for
  the later semantic closure.
- `authority/RIGHTS-unit-20.csv` is 2,024 bytes, SHA-256
  `09b85688b10784cf2c7e7aec9d017eb4d0403faf0b96ef8561b789168d19f565`.
- `authority/ASSET_CLOSURE-unit-20.json` is 4,809 bytes, SHA-256
  `5ab57774999d4f293533a8fb14ad4e50d6caa1fba3d2664428c32d15f935c185`.
  It binds the exact original image, Indonesian caption and alt text, media
  credit, both discrepancy records, and both PDF component identities.

The translated course text remains CC BY-SA 4.0. Every media component keeps
its own recorded terms. This freeze makes no blanket rights claim beyond the
rights of each component.

## Recorded source anomalies

Production must disclose rather than silently inherit these frozen-source
defects:

1. The Whitney-umbrella example says that both exponent expressions map to
   `(1,1)`; with the displayed generators both map to `(2,2)`. Its relation
   `X^2Z=Y^2` remains correct.
2. Solution 14 twice uses dummy product index `eta` while the factor and prose
   use `zeta`; the coherent corrected product is indexed by `zeta`.
3. Exercise 18 refers to named maps `phi_1, phi_2` that the referenced example
   specifies only through inequalities. The displayed cone determines
   `phi_1(s,t)=t` and `phi_2(s,t)=t+2s`; any explanatory insertion must be
   identified as an editorial clarification.

