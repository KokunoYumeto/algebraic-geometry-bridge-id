# Handoff — Indonesian reader through Unit 9

Checkpoint: 2026-08-23. The contiguous Indonesian translation, authority
freeze, component-rights closure, reader build, machine QA, all-page visual QA,
desktop/mobile reflow QA, protected-surface audit, and native backend export are
complete through Lecture 9 and Worksheet 9. This is a verified local partial
checkpoint of the 30-unit classical volume, not a complete edition and not a
publication boundary. No Unit 9 package or public transaction is scheduled.
The next cumulative full reader/backend/package/publication milestone is
targeted through Unit 12 unless newly frozen authority evidence requires a
bounded adjustment.

## Unit 9 authority and translation

The frozen Wikiversity authority manifest is
`authority/wikiversity/unit-09/UNIT_AUTHORITY_MANIFEST.json` (102,154 bytes,
SHA-256 `7cf7a956dffe854da9d021e3c74615573b91b5701d7e3b78a8f5f1aa45bfbc29`).
It binds Lecture page 165898/revision 1112241 (MediaWiki SHA1
`2a702891ae21267751c7900639ef3828faf949c2`) and Worksheet page
165928/revision 1059491 (MediaWiki SHA1
`affd5b273368b8a02f7580671dc4b1431f7da9df`), with 113 and 109 captured
transclusions respectively. The ordered exercise map is 9,763 bytes, SHA-256
`c906ba0b1073a162f7f55289c0f60114063d011756f1eb907bcf342336729495`:
24 exercises and exactly three public source solutions, for Exercises 9.6
(revision 1107958), 9.13 (revision 1059490), and 9.18 (revision 1112817).

The official source PDF witnesses are nine pages/333,288 bytes, SHA-256
`2892b347676e67ec103cb810426dc3f0eb1637ae06fac7b2a55a1710dac8c278`
for the lecture and five pages/135,835 bytes, SHA-256
`86d84352a56e8b5c26bdb2002c4fe45c22e50a01430d65a8360d80f75007c07b`
for the worksheet. The one reader media position is the public-domain David
Hilbert 1886 image. Its local binary and attribution closure are bound by
`authority/RIGHTS-unit-09.csv` (1,580 bytes, SHA-256
`1ac4707f08ec52438dbc8ac2e200be3343ca17bcfbe91501dc2f66ff9935f3a4`)
and `authority/ASSET_CLOSURE-unit-09.json` (1,065 bytes, SHA-256
`c267b8470ba1e5920f280338dbcf33aa2d3919f282730be6850ebf4ce4722819`).

The complete Unit 9 source files are frozen as follows:

- `source/id-ID/lecture-09.md` — 17,091 bytes,
  `ab050d8e321638632546755f9f0f2f5c6328753e25728f0c7627814b5e3b81e4`;
- `source/id-ID/worksheet-09.md` — 10,408 bytes,
  `93c40c95817bf1331ef2ee0052d1fe02a065c5f7032d5853029badde5bf915ab`;
- `source/id-ID/worksheet-09-solutions.md` — 4,230 bytes,
  `322d7f1d46ce2ac5828ee747ab2b26a9cfcf665eccc7bec6e1af05b85d5d390b`.

All three sources declare `translation_status: complete`. The worksheet has
all 24 source exercises in order, and the solution file contains only the
three frozen public solutions; no solution was invented. The final change to
the solution file normalized the established revision-witness comments and
Indonesian backlinks without changing mathematics. The exact additive model
provenance is `OpenAI Codex gpt-5.6-sol, Ultra.` Source authorship,
contributor attribution, component rights, change disclosure, and
non-endorsement remain intact.

## Reader and QA boundary

The cumulative self-contained HTML is 8,888,051 bytes (SHA-256
`19f5612e4f5b102c61cfc63d6a51ea47062af6a66a22261cc4eef0af904ae777`).
The A4 PDF is 174 pages and 5,701,683 bytes (SHA-256
`8204b183766db010c6622096492604a30c61c82b7a3e6c632b9d43ed71df50bd`).
The build receipt is 20,178 bytes (SHA-256
`5c5c5f85b947803f7434dfe6141d96c5299d29ec0ed8d6c90dcd8a123970d1d8`),
and the build is warning-free. The cumulative reader contains 493 unique
stable heading IDs, 245 exercises, 45 public source solutions, 60 media
positions, and 3,262 MathML nodes.

All currently required local reader QA receipts report PASS:

| receipt | bytes | SHA-256 |
|---|---:|---|
| `qa/UNITS_01_09_MACHINE_QA.json` | 10,003 | `da948c9c375a1f0e7e9e5ab8d0528b8ae6e0b38de7fb403b247d44a5ae76e3f7` |
| `qa/UNITS_01_09_VISUAL_QA.json` | 45,835 | `adda6de86647d48deeebc3ac44ae638bf9d2fb4fa2c7e8cf82db6c7e113bd4e3` |
| `qa/UNITS_01_09_RESPONSIVE_QA.json` | 2,140 | `25a3deddf8cf8b7f2830a843c6a6c4a7d0bf398641b6d4b49f8acc8911c9530a` |
| `qa/UNIT_09_PROTECTED_SURFACES.json` | 3,402 | `0deab1dbe378cfc7cbc0061e210146250671749cff8ed84ee3c88667fe7fb5b0` |
| `qa/UNITS_01_09_BACKEND_QA.json` | 1,945 | `eafcb0851ee3a8d2bfa769e15e4b8fd0e7463800e4121bc8a2d41acd41fe423a` |

All 174 PDF pages were rendered and reviewed. Unit 9 pages 162–174 received a
separate contact-sheet review, with full-size checks on pages 162, 165, 168,
170, 171, and 174; no visible clipping, overlap, broken glyph, unresolved
marker, missing content, or transition error was found. The browser audit
proves centered desktop layout, no page-wide mobile overflow, locally
scrollable wide mathematics, 60/60 loaded local images with nonempty alt text,
and zero browser-console warnings or errors.

## Native backend and deferred common adapter

`backend/units-01-09/MANIFEST.json` is 20,139 bytes, SHA-256
`54b87a82373b5ba0660fe204141a50602875942e5a9f1a9dc98c760f5b382eac`;
its canonical JSONL is 9,179,355 bytes, SHA-256
`40f7cf1747ea8e62829594e5d01af7db827820d39a3377b5c4e105d82411bbd6`,
with 6,393 unique records. The exact 5,787-record Unit 8 baseline is carried
forward byte/payload-identically. Native schema closure, parent/relation
closure, authority/build bindings, two-volume architecture records, and
deterministic replay all pass the independent backend QA named above.

The official common-backend-v1 v0.42.0 handoff and receipt schema witnesses
are frozen under `backend/common-backend-v1-contract/upstream/`. The handoff
witness is 5,320 bytes, SHA-256
`83de5379aa08f25fb3fb2774ed8bde99eca76e9a6ba80da9ccf2ee211e5e3a7a`;
the receipt schema witness is 2,563 bytes, SHA-256
`0147b14972dd562805b3b5f76fac453a9f32a6d298827d3f588316d4a8f5ffe0`.
The Unit 9 additive/zero-copy adapter preflight passed without writing a
receipt: 15,476 virtual records, 23,592,348 virtual JSONL bytes, SHA-256
`dc04148522a3ef78c73a02a82c6a2d34d39ce9689d3816da07d15b689d7e7844`,
36,325 checked foreign keys, and exact reverse native SHA-256
`40f7cf1747ea8e62829594e5d01af7db827820d39a3377b5c4e105d82411bbd6`.
The public-identity-bound migration receipt is deferred to the next cumulative
publication boundary, so there is deliberately no Unit 9 receipt path or
receipt hash and no implied imminent Unit 9 release gate.

## Rights, publication disposition, and next cursor

The translated course text and derivative editorial layer remain CC BY-SA
4.0; media retain their per-component rights and attribution. No blanket
licence is claimed for the mixed file set. No Unit 9 release directory,
manifest, source archive, authority archive, Zenodo reservation, Zenodo
publication, DOI, or anonymous public-byte receipt exists because Unit 9 is an
internal checkpoint rather than a publication boundary. The public Zenodo
lineage remains at the previously verified Unit 8 record. GitHub remains
externally suspended and must not be retried. Figshare remains externally
blocked by the previously recorded inactive-account state and has not received
Unit 9 edition bytes.

The next executable sequence is finite: freeze, translate, and locally verify
Lectures/Worksheets 10, 11, and 12 in source order, preserving each unit's
authority, solutions, formulas, identifiers, media, and component rights. At
the targeted Unit 12 cumulative boundary, rebuild and replay the full reader
and native backend; generate and schema-validate the additive common-backend-v1
receipt; package the reader-first payload; publish the next version in the
existing Zenodo concept `10.5281/zenodo.22059686`; and anonymously read back
every public file. The complete corpus architecture remains all 30 lectures
and 30 worksheets of Holger Brenner's *Algebraische Kurven*, followed by the
required Brenner *Bündel, Garben und Kohomologie* second volume and the bounded
original connective bridge. Napkin is optional reference evidence only;
Stacks is used only through downstream permanent-tag references.
