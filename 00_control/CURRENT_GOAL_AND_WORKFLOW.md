# O016/D100 — durable goal and corrected workflow

Status: active. Write only inside this repository's D100/O016 lane.
Recover from this file, `00_control/CURSOR.json`, the current unit worklog,
matching authority/rights/QA, and `qa/UNITS_01_24_HANDOFF.md`. Update them at
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

## Live boundary

Units 1–18 are the current verified and published cumulative reader: 18 lectures, 18
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
reader files, and both Pages files match the frozen bytes. Next: freeze the
official 2012 Unit 25 authority, then translate and verify Unit 25 in source
order without altering accepted Unit 1--24 bytes. This lane remains the sole
integrator, validator, and publisher.

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
