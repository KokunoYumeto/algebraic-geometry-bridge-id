# O016/D100 — durable goal and corrected workflow

Status: active. Write only inside this repository's D100/O016 lane.
Recover from this file, `00_control/CURSOR.json`, the current unit worklog,
matching authority/rights/QA, and `qa/UNITS_01_30_HANDOFF.md`. Update them at
material boundaries; they—not chat, compaction, or a stale synopsis—control.

## Objective and architecture

Produce and publish a complete independent Bahasa Indonesia (`id-ID`)
Algebraic Geometry Bridge. Translate the 30-unit classical *Algebraische
Kurven* sequence in source order, binding Units 1–23 to the frozen official
Osnabrück 2025–2026 Wikiversity revisions and Units 24–30 to the official
complete Osnabrück 2012 course because the current course stops at Unit 23;
identify the edition transition explicitly and never merge or mislabel the
authorities. Then translate all 30 lectures and 30 worksheets of Brenner's
*Bündel, Garben und Kohomologie (Osnabrück 2019–2020)*. Keep both course
editions independently exportable and expose the BGK route through Units
2–15 and 23–27. Author only the missing seam, 57 worked mastery items (three
per route unit, counting source solutions), 12 solved integrative problems,
and one solved permanent-tag Stacks capstone with oral-proof rubric. Napkin
Part XX is optional evidence; Stacks pages are references, not translated
course pages.

Exact corpus accounting is 60 distinct source units and 602 official-PDF
pages: 30 *Algebraische Kurven* units / 337 pages plus 30 BGK units / 265
pages. The 19-unit BGK learner route is a view over those same BGK units and
must never be counted as 19 additional translations; `D100` is a curriculum
role identifier, not a unit count. At the complete classical Unit 30 boundary,
the source remainder is exactly all 30 BGK units / 265 official-source pages,
followed only by the finite original layer named above. The first course
renders to 504 Indonesian pages; applying the same density gives a planning
estimate of roughly 400 further reader pages for BGK, or about 900 pages for
the two-book core. That rendered estimate creates no additional source units.
This owner lane therefore completes the entire remaining BGK corpus directly,
with no packet split, overlap, or double-counting of the 19-unit learner-route
view.

## Live boundary

The current verified public boundary is the complete 30-unit classical volume,
described in the final paragraphs of this section; earlier boundary paragraphs
are retained only as historical provenance. The remaining production corpus is
exactly 30 BGK units / 265 official-source pages, followed by the finite
original layer. No split or second counting of the 19-unit learner route is
planned. BGK authority has not yet been frozen inside this lane: the admitted
course root is `Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)`,
observed revision 1052895, and the recorded official PDF witness is 265 pages,
2,104,862 bytes, SHA-256
`87655cf7e96dc0eaa185ca49a374dc9e25f4b739670495f423279aa332fce66c`.
The next action is to parameterize the classical freezer into a disjoint BGK
authority namespace, freeze the root and Unit 1 closure, verify that PDF witness
locally, and then translate BGK Unit 1.

Units 1–18 were the earlier verified and published cumulative reader: 18 lectures, 18
worksheets, 513 exercises, all 90 frozen public source solutions, 74 media
positions, 1,046 source/control IDs, 7,186 MathML nodes, a 320-page A4 PDF, and
a 13,626-record native backend. Every reader, visual, responsive, protected,
backend, deterministic-replay, terminology, and common-adapter gate passes;
all 10,938 Unit 15 baseline records remain byte-identical. Exact identities
are in `qa/UNIT_18_RELEASE_CANDIDATE.json`, `qa/UNITS_01_18_HANDOFF.md`, and
the Unit 16–18 worklogs.

The deterministic Unit 18 package is published to the existing Zenodo concept
`10.5281/zenodo.22059686` as record 22087566 / DOI
`10.5281/zenodo.22087566`; anonymous readback matched all eight files by byte
count and SHA-256. The identical checkpoint is published to the existing
GitHub repository, annotated `unit-18` tag, eight-file release, and Pages
reader at content commit `fb99904c2dce760fdb67ffff5f561b6ffa30541b`;
anonymous readback matched every release asset plus raw-commit and Pages
HTML/PDF bytes. Receipts are `qa/UNIT_18_ZENODO_PUBLICATION.json` and
`qa/UNIT_18_GITHUB_PUBLICATION.json`.

Units 19--21 are now independently frozen, translated, corrected, and verified.
The contiguous source contains 21 lectures, 21 worksheets, 577 exercises, all
102 frozen public solutions, 76 media positions, and 1,194 stable source IDs.
The cumulative self-contained HTML is 12,388,419 bytes (SHA-256
`ae658bee5191e4d0be529d38ec7eb9fd2e287295237be4bbb98a58b4709c6700`);
the 367-page A4 PDF is 7,409,373 bytes (SHA-256
`b95fd1ed0ea75294cd4562b7f2f36e920e247e2da5e1b039e99e975f9797a3e6`).
Machine, protected-surface, responsive, and all-page visual QA pass, including
8,521 matched MathML/TeX surfaces, all 76 embedded images with nonempty alt
text, no broken anchor, centered desktop layout, full mobile reflow, and local
scroll containment for 138 wide phone-width formulas. Exact evidence is in
`qa/UNITS_01_21_MACHINE_QA.json`, `qa/UNIT_21_PROTECTED_SURFACES.json`,
`qa/UNITS_01_21_RESPONSIVE_QA.json`, `qa/UNITS_01_21_VISUAL_QA.json`, and
`qa/UNITS_01_21_VISUAL_PAGE_MANIFEST.json`. The append-only native/common
backend and deterministic eight-file package pass. Zenodo record 22088753 / DOI
`10.5281/zenodo.22088753` and GitHub tag/release `unit-21` are public in their
existing lineages. Anonymous readback matched all 16 release-file surfaces,
the raw GitHub HTML/PDF, and live Pages HTML/PDF. Receipts are
`qa/UNIT_21_ZENODO_PUBLICATION.json` and
`qa/UNIT_21_GITHUB_PUBLICATION.json`.

Units 22--24 are frozen, translated, corrected, built, published, and
anonymously verified as the current cumulative checkpoint: 24 lectures, 24
worksheets, 622 exercises, all 114 frozen public solutions, 83 media positions,
1,330 stable source/control IDs, self-contained HTML, a 417-page A4 PDF, and an
18,488-record native backend. Unit 24 is explicitly bound to the official 2012
course and uses the `br-ak-2012-*` namespace. Every machine, protected,
responsive, all-page visual, native-backend, common-adapter, packaging, and
public-byte gate passes. The eight-file reader-first package is public in the
existing Zenodo concept as record 22102097 / DOI
`10.5281/zenodo.22102097`, and in the existing GitHub/Pages lineage at content
commit `fd8984aeb642de240af6a36aee4464d25791658a`, annotated tag `unit-24`.
Receipts are `qa/UNIT_24_ZENODO_PUBLICATION.json` and
`qa/UNIT_24_GITHUB_PUBLICATION.json`; every release asset, both raw-commit
reader files, and both Pages files match the frozen bytes. This published
baseline remains immutable. This lane remains the sole integrator, validator,
and publisher.

Units 25-27 are now independently frozen, translated, corrected, and
deterministically verified as internal source boundaries. Unit 25 preserves
nine ordered lecture entities, 13 exercises, exactly two frozen public
solutions, zero new media positions, 31 stable unit IDs, and 295 Pandoc math
nodes. Unit 26 preserves 21 ordered lecture entities, 11 exercises, exactly
one frozen public solution, one new media position, 39 stable unit IDs, and
346 Pandoc math nodes. Unit 27 preserves 21 ordered lecture entities, 11
exercises, zero public solutions, ten full-resolution media positions, 39
stable unit IDs, and 269 Pandoc math nodes. Cumulative internal source coverage
is 27 lectures, 27 worksheets, 657 exercises, all 117 frozen public solutions,
and 94 media positions. Exact identities are in
`00_control/UNIT_25_WORKLOG.md`, `00_control/UNIT_26_WORKLOG.md`,
`00_control/UNIT_27_WORKLOG.md`, their matching authority freezes, and the
three matching translation-QA receipts. The cumulative self-contained HTML is
22,205,344 bytes (SHA-256
`8edd2fc31c30e7e5454f31cf18b6f3f117e1a7108766c839a33cf896cdd24b66`);
the 464-page A4 PDF is 14,826,919 bytes (SHA-256
`766f6b8ccede9ecb1b6524d9652595f188d6f17ef22fab4bf6b886b03a9e0d65`).
All-page visual, machine, protected-surface, responsive, native-backend, and
common-adapter gates pass. The native backend has 20,570 records, preserving
all 18,488 Unit 1–24 records byte-for-byte; the additive common adapter
validates 48,882 virtual records and 116,400 foreign keys and reverses exactly
to the native bytes.

The deterministic eight-file reader-first Unit 27 package is public in the
existing Zenodo concept as record 22104692 / DOI
`10.5281/zenodo.22104692`; anonymous streaming readback matched all eight
files by byte count and SHA-256. The sanitized receipt is
`qa/UNIT_27_ZENODO_PUBLICATION.json`. The same package is public in the
existing GitHub lineage at content commit
`07b22e59c546bf9c29995cded0aff37e696b2d02`, annotated tag `unit-27`, and
release `https://github.com/KokunoYumeto/algebraic-geometry-bridge-id/releases/tag/unit-27`.
Anonymous readback matched all eight release assets, raw-commit HTML/PDF and
README/CITATION/LICENSE metadata, and Pages HTML/PDF. The sanitized GitHub
receipt is `qa/UNIT_27_GITHUB_PUBLICATION.json` (6,687 bytes, SHA-256
`63a25c2408388c8af35d510fc88d0e1813ef499ba05d11a2724a4f2c978da277`).
A bounded in-app-browser retry was blocked by the browser's local-file URL
policy; no workaround was attempted. The already frozen responsive receipt
binds the identical HTML SHA-256, and public Pages readback now matches it.
Unit 28 is now frozen, translated, corrected, built, published, and
anonymously verified as the current cumulative checkpoint. It preserves 19
ordered lecture entities, all 14 exercises, the sole frozen public source
solution (Exercise 10), 13 negative solution candidates, four media positions,
and 44 stable source IDs. Cumulative coverage is 28 lectures, 28 worksheets,
671 exercises, 118 public source solutions, 98 media positions, 1,483 stable
source IDs, and 10,717 MathML nodes. The self-contained HTML is 23,412,216
bytes (SHA-256
`b7cef9e6c08b696bde2f875a4766e6c35e975d4fd0901e414c3896014bbd9c10`);
the 476-page A4 PDF is 15,820,212 bytes (SHA-256
`181b6fba2b5441fb7a5ab76a512e9d9ee2300e4201fd4632cac20a70bc703df6`).
All-page visual, machine, protected-surface, responsive, native-backend, and
common-adapter gates pass. The native backend has 21,358 records and preserves
all 20,570 Unit 27 rows byte-for-byte; the common adapter validates 50,672
virtual records and 120,703 foreign keys and reverses exactly to native bytes.

The reader-first package is public in the existing Zenodo concept as record
22105836 / DOI `10.5281/zenodo.22105836`; anonymous readback matched all eight
files. It is also public at GitHub content commit
`915558629641eb894c43ff5ce67dd935c4168711`, annotated tag/release `unit-28`,
and Pages. Because the anonymous REST core limit was exhausted, the GitHub
receipt independently proves public branch/tag identity through credential-free
smart HTTP, the release and commit HTML surfaces, all eight fixed release
downloads, fixed-commit HTML/PDF plus README/CITATION/LICENSE, and live Pages
HTML/PDF. Receipt `qa/UNIT_28_GITHUB_PUBLICATION.json` is 9,243 bytes,
SHA-256
`ba3cb54876941cc754c54921761d60f8622b144d1f4bc084770b7ce1ea90adb4`;
  the final bounded anonymous replay passed at `2026-08-27T17:50:28Z`.

Units 29 and 30 are now independently frozen, translated, corrected, and
source-verified, completing the entire classical course. Cumulative source
coverage is exactly 30 lectures, 30 worksheets, 693 exercises, all 122 frozen
public source solutions, 101 media positions, and 1,554 stable source IDs.
Unit 30 preserves all seven lecture entities, twelve exercises, exactly the
two public solutions to Exercises 3 and 4, one public-domain media position,
and 35 stable IDs. Six repairs are visibly disclosed as `AGC-CORR-0130`
through `AGC-CORR-0135`; the Exercise 4 title/formula discrepancy is preserved
as a separate source note. Exact identities are in
`00_control/UNIT_29_WORKLOG.md`, `00_control/UNIT_30_WORKLOG.md`, the matching
authority freezes, and `qa/UNIT_29_TRANSLATION_QA.json` plus
`qa/UNIT_30_TRANSLATION_QA.json`.

The deterministic complete-classical build is 504 A4 pages. Its self-contained
HTML is 23,805,465 bytes, SHA-256
`1ca69127dbbf8aa86d8d3f238488686a145ad2dd99ee417c329a5bd9516ca677`;
its PDF is 16,019,237 bytes, SHA-256
`6383d3b9804a059e76dc643da5974b8809649707e177ba191a69220fa7ea0e5d`.
The three previously split duplicate figure captions were replaced by single
semantic captions plus separate accessibility descriptions. Machine,
protected-surface, responsive, all-page visual, and font gates pass across all
504 pages and both desktop/phone layouts. The 22,752-record native backend
preserves all 21,358 Unit 1–28 records byte-for-byte. The additive common
adapter validates 53,953 virtual records, 8,268 strict source profiles, and
128,541 foreign keys and reverses exactly to the native bytes.

The deterministic eight-file complete-classical package is public in the
existing Zenodo concept as record 22150273 / DOI
`10.5281/zenodo.22150273`; anonymous readback matched every file. Receipt
`qa/UNIT_30_ZENODO_PUBLICATION.json` is 4,273 bytes, SHA-256
`dcd2c4574081a4462627b5775480b27de4d5959e76442bc7d409979480e4bcea`.
The identical package is also public at GitHub content commit
`9ffc8932d51ad1f41c0170ab05443f19e7fa55dc`, annotated tag/release `unit-30`,
and Pages. Anonymous readback matched all eight release assets, fixed-commit
HTML/PDF plus metadata, and live Pages HTML/PDF; receipt
`qa/UNIT_30_GITHUB_PUBLICATION.json` is 8,634 bytes, SHA-256
`0e1374c3ef7bafc94430018b29d525c0e84fb5b3f1fe885fb4ac3212a8d3e12e`.
The exact next executable action is to freeze and translate BGK Unit 1.

## Finite workflow

1. Freeze each MediaWiki lecture/worksheet revision, SHA-1, XML/wikitext,
HTML, TeX, transclusions, exercise order, lawful solutions, PDFs, URLs, bytes,
and SHA-256. Freeze assets with creator, source, licence, attribution,
dimensions, bytes, and hash. Authority is immutable.
2. Translate lecture, worksheet, hints, and frozen solutions completely.
Preserve math, proof scope, IDs, numbering, stars, points, links, structure,
code, and media. Invent no solution or silent proof repair. Record deltas in
`00_control/CORRECTIONS.csv`, maintain `00_control/TERMINOLOGY.csv`, keep all
credit, and add exact provenance
`OpenAI Codex gpt-5.6-sol, Ultra.`
3. Per unit verify mapping, math, exercise/solution topology, terminology,
rights, language residue, links, accessibility, and secrets. At milestones
build semantic self-contained HTML/MathML and A4 PDF; bind tools, inputs,
outputs, pages, bytes, and hashes. Inspect all pages and actual centered
desktop/mobile reflow, fonts, metadata, math overflow, and media.
4. At milestones export deterministic locale-neutral program/course/resource,
edition/unit/segment, exercise/solution, concept/term, asset/relation/rights,
correction/QA/artifact records. Preserve prior IDs/payloads. Validate schema,
uniqueness, closure, hashes, exact reverse replay, and the additive
common-backend-v1 adapter; it never replaces native data or reader bytes.
5. Publish only substantial milestones to the existing Zenodo concept and
   GitHub edition/Pages lineage with truthful status/rights, checksums,
   reader-first PDF/HTML, and resumable source. Anonymously hash every public
   file. Do not probe `InactiveAccount` Figshare until its state changes. No
   upstream contact during production; after completion, at most one concise
   report may be sent, signed `Codex — at the user's direction`.

## Rights and terminal condition

Brenner text/derivative are CC BY-SA 4.0; media retain component rights. Never
claim a mixed-set blanket licence. State attribution, change, ShareAlike, and
non-endorsement. Never expose credentials, run broad scans, or edit another lane.

Complete only when both full Brenner courses, the finite original layer,
rights, reproducible HTML/PDF, stable-ID native/common backends, QA, durable
controls, milestone releases, and anonymous public-byte verification are all
complete. Otherwise keep the goal active and continue from the exact cursor.
