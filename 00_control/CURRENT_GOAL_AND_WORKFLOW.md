# O016 / D100 — Current goal and durable workflow

Status: active production lane | Language: `id-ID` | Opened: 2026-08-21

## Goal

Produce a complete independent Indonesian Algebraic Geometry Bridge. Holger
Brenner's *Algebraische Kurven (Osnabrück 2025–2026)* is the dominant classical
spine; preserve its 30 lectures and 30 worksheets in source order. Evan Chen's
*An Infinitely Large Napkin*, Part XX, is a donor for the compact affine-schemes
core only. Author an independently worded supplement for gluing and the
projective transition. Permanent Stacks tags are downstream references, not the
first textbook.

This is a translation/reader-production task, not a recommendation or QA loop.
QA gates the work but does not replace it. Maintain immutable authority,
component rights, reproducible HTML/PDF builds, and a dense locale-neutral
stable-ID backend so units can later move to another language without
reconstructing their meaning. Maintain one corpus-specific public GitHub.

## Exact opening authority

- Course root current revision: `1074230`; exact prefix census: 433 pages,
  including 30 lectures, 30 worksheets, their `/kontrolle` and `/latex`
  surfaces, and 252 course-local semantic/reference/control pages.
- Lecture 1: page 165889, revision 1108084,
  `2026-07-20T08:57:22Z`, MediaWiki SHA1
  `sbohlbklicv2bb3w2dxf1d2h6qa1ogt`.
- Worksheet 1: page 165920, revision 1108097,
  `2026-07-20T09:11:56Z`, MediaWiki SHA1
  `0mjykxzwclr5grw31fffi3f9ujy3vq8`.
- Official course PDF: 337 pages, 5,023,958 bytes, SHA-256
  `5a2fcc8b00c48056655ccbf68a3034c1a4fcf0114fef9f54a8eac8d42bb0b203`.
  Its 2026-02-03 build predates current wiki edits, so it is a visual/build
  witness rather than current textual authority.
- Napkin: commit `e50be9a0b2b12d080c273619424d0ee13372cc91`, tree
  `023467410bdf924c8fd38ac04009b4c887cbfb5e`; Part XX authored closure is
  `sheaves.tex`, `localization.tex`, `spec-zariski.tex`, `spec-sheaf.tex`,
  `spec-examples.tex`, and `mor-scheme.tex`. Archive/build hashes belong in the
  authority receipt after local verification.

## Rights and fidelity

Never edit authority witnesses. Preserve exact wiki XML/wikitext, rendered
semantic HTML, generated LaTeX, PDFs, assets, revision IDs, URLs, sizes, and
hashes. Brenner course prose is CC BY-SA 4.0 under its exact declaration;
Wikimedia media retain per-file creators and licences. Napkin text/PDF is CC
BY-SA 4.0 and distributed modified build source is GPLv3. Omit or replace
`calvin-hobbes-fly.png` and `mumforddrawing.jpg` unless their rights are proved.
Do not import community solutions without a separate licence freeze. Mark the
translation/change, preserve attribution and ShareAlike, and state
non-endorsement. Record every mathematical correction as an explicit,
source-backed delta; never correct silently.

## Ordered work and gates

1. Complete the 433-row Brenner authority manifest, course licence, first-unit
   XML/HTML/LaTeX, 24-image component-rights closure, and all seven public
   Worksheet 1 solution pages.
2. Acquire/hash the immutable Napkin archive and official 74-page Part XX PDF;
   validate/extract safely and replay the official exact-head build. Record a
   precise blocker if the published build is not hermetic.
3. Translate Lecture 1, all 28 Worksheet 1 exercises, and the seven source
   solutions completely. Preserve formulae, results, IDs, stars, point values,
   image positions, links, and source order; invent nothing.
4. Build self-contained Indonesian HTML with MathML and an A4 LuaLaTeX PDF.
   Record exact tool versions, input/output manifests, bytes, and SHA-256.
5. Verify source mapping, topology, IDs, mathematics, exercise/solution links,
   terminology, assets/rights, accessibility, links, language residue, PDF
   extraction, and representative/all-page visual layout as proportionate.
6. Export deterministic UTF-8 records for program, course, resources,
   editions, units, segments, concepts, terms, assets, relations, rights,
   corrections, QA events, and artifacts. IDs must survive title wording and
   locale changes; the backend may not mutate reader content.
7. After this bounded unit passes, push it to the corpus GitHub without asking
   again. Use the user's designated local credential notes only when required;
   never print/persist token values; verify the anonymous public result. The
   curriculum-wide hub is the coordinator's job.
8. Continue with Lecture 2/Worksheet 2 in order. Insert the schemes bridge only
   after its documented classical prerequisites. Its original supplement must
   cover affine gluing/cocycles, `P^1` from two affine lines, doubled origin,
   one Brenner projective curve in charts, and complete original exercises and
   solutions; check against Stacks tags `01HR`, `01HW`, `01JA`, `01JB`, `01JC`,
   `01JE`.

## Recovery and communication

Current cursor: Lecture 1 + Worksheet 1 solutions/build. Resume from this file,
`AUTHORITY_FREEZE.md`, `RIGHTS.csv`, `CURSOR.json`, and latest build/QA/backend
receipts, never from a compaction summary. Advance only after the current unit
is translated, built, verified, hash-bound, and pushed. Do not contact upstream
during production. After the full corpus only, send at most one concise,
high-confidence issue, signed `Codex — at the user's direction`; otherwise send
nothing.
