# Unit 11 translation findings

Date: 2026-08-24  
Scope: frozen Unit 11 only; no shared control, glossary, build, cursor, Git, or
publication mutation.

## Frozen authority used

- Lecture page 165900, revision 1051329, MediaWiki SHA-1
  `33f81e0bf65b5b23de1c5798adf4a93282354d82`.
- Worksheet page 165930, revision 1062657, MediaWiki SHA-1
  `1b95cc02cb9d0260971c1fa369afc8969fa13262`.
- Authority manifest SHA-256
  `ea2d4936bb27e88b2863f8fecbddd5570992c432aee66c72066597709da65a47`.
- Ordered exercise map SHA-256
  `6298bafd7656e4653b504706b437e89de7faa92a75fac10c31d51ad9644a20cf`.
- Public solutions: only Exercise 11.6, revision 1094883, and Exercise 11.7,
  revision 1112854.

## Unit-local outputs frozen by this pass

| File | Bytes | SHA-256 |
|---|---:|---|
| `source/id-ID/lecture-11.md` | 15,657 | `268324606509f055a70c35d782982108763d58ccc2993e33e42d80e54aea4dcb` |
| `source/id-ID/worksheet-11.md` | 12,609 | `92f97d3eb40474184b678ba80c4f804b1d81600380fe14a322a19143905ecb39` |
| `source/id-ID/worksheet-11-solutions.md` | 2,636 | `9799331d7eb1ed32b3d9c092b54d5e77bad71dab831090065f347a0d50c3b2a2` |
| `source/id-ID/media-credits-unit-11.md` | 723 | `423cdad2e676539994766627b9ff48aa20f337ea4b6ed806bee565481c50f7a3` |

## Deterministic parity and structure checks

- Lecture closure: 13 source-linked semantic blocks retained: 9 theorem/
  proposition/corollary blocks, 1 definition, and 3 examples, across all 3
  source sections. Every displayed formula and proof topology is retained.
- Worksheet closure: exactly 26 sequential exercise headings and exactly 26
  `upstream_entity` bindings. Exercises 1-20 remain practice exercises;
  Exercises 21-26 remain submission exercises. Point values `4,3,7,3,5,4`
  and the source's starred Exercises 6-7 are retained with the reader's
  established literal `★` marker.
- Solution closure: exactly 2 solution headings, for 11.6 and 11.7, with
  exact frozen revision IDs and XML hashes; no solution was inferred for the
  other 24 exercises.
- Media closure: the one reader position resolves to
  `authority/assets/Disjoint_ellipses.png`, 11,115 bytes, SHA-256
  `c6f71e6f2ecf41be4a3fa66536b5efd4cc33a92b3962c45e95884be7b7a8fddc`.
  Alt text and a unit-local public-domain credit are present; the credit does
  not falsely call the selected Commons render byte-identical to the original.
- Stable-ID scan found no duplicate Unit 11 IDs. Pandoc parsed all four output
  files successfully (exit 0). Placeholder/mojibake scan was clean; German
  text remains only inside immutable provenance entity names.

## Source quirks preserved transparently

1. The lecture's expanded TeX writes the linear term in the $X_n$ expansion
   as `P_1X_0`. The reader uses the mathematically consistent `P_1X_n` and
   records the source form in an explicit edition note.
2. Exercise 11.19 prints `+ \mathfrak a` outside the quotient denominator. The
   reader adds parentheses around the sum in the denominator and records this
   typographic normalization in an explicit edition note.

## Terminology proposals for later shared-glossary integration

No shared glossary was changed in this pass. The following choices are
consistent with earlier translated units and should be considered at the next
single-owner glossary boundary:

- `Hilbertscher Nullstellensatz` -> `Nullstellensatz Hilbert` (already used in
  Units 2, 3, and 10).
- `Koordinatenring` -> `gelanggang koordinat` (already introduced in Unit 5).
- `Einheitsideal` -> `ideal satuan`.
- `Restekörper` -> `lapangan residu` (matches Unit 10).
- `Erweiterungsideal` -> `ideal perluasan`.
- `D(f)` / `hauptoffene Menge` -> `himpunan terbuka utama` when named.

Unit 11 is ready for the parent lane's cumulative Units 1-12 build and QA.
