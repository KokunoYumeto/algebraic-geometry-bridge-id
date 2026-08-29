# BGK Unit 6 authority freeze

Status: complete, bounded, and reproducible semantic/source authority for
Unit 6 of Holger Brenner's *Bündel, Garben und Kohomologie (Osnabrück
2019–2020)*.  This document freezes source identity and component surfaces;
it is not a translated reader and is not a publication by itself.  The
deterministic authority QA receipt is
`qa/BGK_UNIT_06_AUTHORITY_QA.json` (6,217 bytes, SHA-256
`c22f362a9b1bc71d4f8497ac06e8f1264935977a7d43584178c941de613306ed`).

## Semantic source identity

- Source project/API: German Wikiversity, namespace `Kurs`,
  `https://de.wikiversity.org/w/api.php`.
- Lecture: *Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019–2020)/Vorlesung
  6*, page 109010, revision 1003728, timestamp
  `2025-06-08T15:29:32Z`, MediaWiki SHA-1
  `0dfea13421076e8f6486836e9fc799822bf52053`, oldid URL
  `https://de.wikiversity.org/w/index.php?oldid=1003728`.
- Worksheet: *Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019–2020)/
  Arbeitsblatt 6*, page 110211, revision 900086, timestamp
  `2023-06-27T11:07:09Z`, MediaWiki SHA-1
  `619536dcd80063470e12de7a3ebb3fc9fe1aa5e5`, oldid URL
  `https://de.wikiversity.org/w/index.php?oldid=900086`.
- The complete recursive semantic closures contain 136/136 requested lecture
  transclusions and 109/109 requested worksheet transclusions, with zero
  missing pages.  The exact XML, API, HTML, parse, and five-batch transclusion
  witnesses are under `authority/wikiversity-bgk/unit-06/`.
- Terminal `/latex` witnesses are lecture page 110014 revision 807073 and
  worksheet page 117161 revision 807043, each carrying MediaWiki SHA-1
  `1d092e4f15139d9908d36c4d64a1f4fde570e1ba`.  Expanded TeX is
  `lecture-06-expanded.tex` (19,454 bytes, SHA-256
  `0bdf28cb69d063b1782b7b42eb2212241e109f66ba382368dcd8e782d5ae829d`) and
  `worksheet-06-expanded.tex` (11,703 bytes, SHA-256
  `0de1911162df14c38fa00755cf67583fbdd9b101134314e6d47a546922e875c1`).
  These are terminal-byte witnesses; no recursive wrapper-template rebuild is
  claimed.
- Manifest:
  `authority/wikiversity-bgk/unit-06/UNIT_AUTHORITY_MANIFEST.json`, 107,618
  bytes, SHA-256
  `69a10e682e853c6f386afbc68438605846e5096220b21bd1e827c07633a79244`.
  It declares 31 files.  Every declared byte count and SHA-256 was recomputed
  and matched.  Two complete `--resume` captures reproduced this same manifest
  hash.  Capture identity is
  `authority/wikiversity-bgk/unit-06/CAPTURE_IDENTITY.json`, 672 bytes,
  SHA-256 `02e62660d25cc025acc0c30fdac58cd9bdfbc87c72c23e467672f58ba0389c3d`.

## Exercises and lawful solutions

`ORDERED_EXERCISE_MAP.json` is 6,302 bytes, SHA-256
`ea15e1f79b4dfc0928fe132eb83e8d20d10fbc84837de153da2b4e345e5a04a0`.  It
contains exactly 19 worksheet exercises in source order.  The candidate API
evidence is 1,940 bytes, SHA-256
`d735bc437898b9f33e90a163164dd5bab85c534b080c632aedb441fbef9acf55`; all 19
corresponding `/Lösung` pages are explicitly missing at the frozen query.  No
solution is carried into the Indonesian edition and none may be invented.

## Official PDF witnesses and visual boundary

- Lecture PDF `authority/artifacts/bgk-lecture-06-official.pdf`: 89,016 bytes,
  SHA-256
  `55fbef2b5d9eae950ac7ab064a8029f2e2932c49280a98a4a7ec6ed16262c75d`;
  Commons source SHA-1 `fe3558459f5e48cd7dc73aa98b88a414479db6fb`; 7 Letter
  pages (612 × 792 points).
- Worksheet PDF `authority/artifacts/bgk-worksheet-06-official.pdf`: 61,587
  bytes, SHA-256
  `7b4f4569e7ab749a9e6affac715592316c109507d91971fd1c7b82cefaa825b5`;
  Commons source SHA-1 `0ae41707620c7a624a8e2092c3b741e971c9bafc`; 7 Letter
  pages (612 × 792 points).
- pypdf and Poppler agree on page counts and boxes.  All 14 pages were
  rendered with Poppler and visually reviewed.  Page 6 of each witness is an
  intentionally blank source page; page 7 contains the source image index and
  rights notice.  The embedded notice reads `CC-by-sa 3.0`.

## Media and component rights

The official PDFs are authority witnesses, not reader-media positions.  The
Commons rights freezer produced a zero-media closure:

- `authority/commons-imageinfo-bgk-unit-06.json`: 7,059 bytes, SHA-256
  `681014a0999f21f8ae99a31ae35003e215dc34a7604bbe35b6a18dbf7598d619`.
- `authority/RIGHTS-bgk-unit-06.csv`: 1,051 bytes, SHA-256
  `87f9d56b1300a56ca68e4aa8f50e3d50ab622d7a4d05221089d49e1dba35981d`.
- `authority/ASSET_CLOSURE-bgk-unit-06.json`: 6,061 bytes, SHA-256
  `9efa26ce4f4d0c0f95af36b7bba1efef15b55af9dcbd7533353e20c64f8f83b3`;
  `reader_media_positions=0`, `assets=[]`.
- `source/id-ID/media-credits-bgk-unit-06.md`: 666 bytes, SHA-256
  `0d5b052a4346e8a56770798f3882417eaae2ea7e815f1947c289d9785e1c2af7`.

Current Commons descriptions identify the PDF components as CC BY-SA 4.0;
the embedded PDF notices identify the course PDF surface as CC-by-sa 3.0.
Both surfaces are retained and disclosed separately.  The semantic course
and the Indonesian derivative remain bound to CC BY-SA 4.0 with attribution,
share-alike, and non-endorsement; no blanket relicensing or endorsement claim
is made.

## Bounded source findings for translation

Four high-confidence source-surface findings are recorded for visible
translation treatment rather than silent normalization:

1. Worksheet Exercise 6.6 prints *einer stetige Abbildung*; the grammatical
   form is *eine stetige Abbildung*.
2. The defining displays in Exercises 6.14 and 6.15 use `φ₁(x₁)=φ₂(x₂)`
   although the maps introduced immediately above are `p₁` and `p₂`.
3. Exercise 6.15 prints *eine weiterer topologischer Raum*; the grammatical
   form is *ein weiterer topologischer Raum*.
4. The terminal PDF's Example 6.6 cites the Analysis 2014–2016 course while
   the current semantic TeX witness cites 2021–2023.  Both are preserved as
   source surfaces; the edition must not silently rewrite either citation.
5. The proof of Lemma 6.10 writes $s_i\in\mathcal F(V_i)$ although
   $V_i\subseteq Y$ and $\mathcal F$ is a presheaf on $X$.  The translated
   proof uses the well-typed $s_i\in\mathcal F(\varphi^{-1}(V_i))$ and
   discloses the source expression.

The correction ledger and Indonesian notes must retain the original forms,
their source revisions, and the mathematical reason for any reader-facing
clarification.

## Reproducibility checks

The offline QA receipt records: exact source identity; complete transclusion
closure; terminal LaTeX witness boundary; 19 ordered exercises and zero public
solutions; exact PDF bytes, page geometry, blank-page and rights-page checks;
zero substantive reader media and separate component rights; two identical
authority `--resume` replays; five source findings; and `git_used=false` /
`upstream_contacted=false`.  Model provenance for the receipt and subsequent
translation is exactly `OpenAI Codex gpt-5.6-sol, Ultra.`

Next action: translate this frozen Unit 6 in source order, preserving all 19
exercises, the zero-solution topology, formulas, IDs, rights, and the five
visible source treatments.  Then run the per-unit translation gate before the
cumulative Units 1–6 reader/backend/release cycle.
