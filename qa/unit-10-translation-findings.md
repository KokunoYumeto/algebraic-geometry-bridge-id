# Unit 10 translation findings

Status: **PASS — complete bounded id-ID translation boundary**

## Frozen authority used

- Lecture: page 165899, revision 1051326, MediaWiki SHA-1
  `2635c363f022af1e0603447bbac65bfe71e87a46`.
- Worksheet: page 165929, revision 1058833, MediaWiki SHA-1
  `48ce873997cecbd45efdceb3a7caa19ae7844876`.
- Authority manifest: 128,797 bytes, SHA-256
  `f8b4f8bf12a0613f774352df31941d79a35d9eed10f2d8fb5570f9ffe07bfb43`.
- Ordered exercise map: 12,935 bytes, SHA-256
  `972e36256d128916533a33be1d2feedfdecbd133a0dbba96193a85477cf7e92c`.
- Rights topology: zero substantive reader-media positions; translated course
  prose remains CC BY-SA 4.0. The stale `CC-by-sa 3.0` footer in the two
  official PDF witnesses remains documented in the immutable authority
  closure and was not imported as downstream rights metadata.

## Output closure

| File | Bytes | Lines | SHA-256 |
|---|---:|---:|---|
| `source/id-ID/lecture-10.md` | 14,540 | 418 | `08a496387da53cefb7e1f427fa8d762465d31c18618be7ea897fe8246da21e6d` |
| `source/id-ID/worksheet-10.md` | 13,115 | 424 | `aa3a60bf17308df5d07ae88941eaf3cda9171a17e4ddd9e9c8c84053ee1d0f62` |
| `source/id-ID/worksheet-10-solutions.md` | 7,794 | 233 | `1ccbbc4377c44889f4659a54c6cba8e5314eb32b2443a9d74352aeb631a56a08` |

No Unit 10 media-credit file was created because the frozen parse and rights
closure contains no substantive media position.

## Deterministic checks

- Lecture structure: source has 2 definitions and 8 proved facts; target has
  exactly 2 definitions, 3 lemmas, and 5 theorems. **PASS**
- Worksheet order and IDs: exactly 29 headings, numbered and identified
  contiguously from 10.1 / `ex-01` through 10.29 / `ex-29`. **PASS**
- Public-solution closure: exactly 6 solutions, and only for exercises
  1, 6, 9, 16, 17, and 20. **PASS**
- Source stars: exactly the same six exercises (1, 6, 9, 16, 17, 20) carry
  `★` in the target. **PASS**
- Assigned-point values: 10.25=3, 10.26=3, 10.27=5,
  10.28=4 (1+3), 10.29=3. **PASS**
- All six solution backlinks resolve to worksheet IDs. **PASS**
- Stable IDs across the three files: 60 total, 0 duplicates. **PASS**
- Placeholder scan (`TODO`, `TBD`, `PLACEHOLDER`, untranslated markers):
  0 hits. **PASS**
- German-fragment review: all matches are deliberate immutable
  `upstream_entity` / `upstream_solution` provenance strings; none occurs in
  reader prose. **PASS**
- Pandoc GFM parse for all three files: exit code 0. **PASS**

## Faithful normalization and terminology proposals

- In Soal 10.6, parentheses were made explicit as `R/(I\cap J)` and
  `R/(I+J)`; this resolves only the source typography's precedence ambiguity.
- In Solusi 10.17, the quotient-ring correspondence implicit in the source was
  stated explicitly so the displayed intersection is type-correct; the
  mathematical assertion and proof route are unchanged.
- Proposed additions for later shared-glossary review (not applied here, as
  required by the unit-local write boundary): `kurze exakte Sequenz` →
  `barisan eksak pendek`; `Nichtnullteiler` → `bukan pembagi nol`;
  `Nenneraufnahme` → `pelokalan`; `Punktideal` → `ideal titik`;
  `artinsch` → `Artin`; `algebraisch abhängig/unabhängig` →
  `bergantung/bebas secara aljabar`.

No source defect requiring an upstream report was inferred during this
translation boundary.
