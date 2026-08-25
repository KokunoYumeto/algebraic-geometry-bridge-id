# Unit 21 authority freeze

Status: frozen and independently replay-verified on 2026-08-25.

## Official course surfaces

- Lecture: `Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 21`,
  page 165910, revision 1112312, timestamp `2026-08-21T09:27:05Z`,
  MediaWiki SHA-1 `05c51f6e29f6ec12aef400195396ca517924b094`.
- Worksheet: `Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Arbeitsblatt 21`,
  page 165940, revision 1062605, timestamp `2025-12-18T11:05:07Z`,
  MediaWiki SHA-1 `38a7856a5df3695eb80874194bc043dda3377f90`.
- Lecture and worksheet closures contain respectively 122 and 144 captured
  transclusions, with no missing page.
- The frozen `/latex` launchers are pages 165974/revision 1033020 and
  166034/revision 1033082. Each contains only `{{latex}}`; neither is an
  immutable expanded source. Their byte-bound dynamic Parsoid captures are
  retained as production aids: `lecture-21-expanded.tex` is 20,239 bytes,
  SHA-256
  `0a6fc74c8d01069d327fe25c5203bf4587b4564c8409ad57f625c3ac16ceb62f`;
  `worksheet-21-expanded.tex` is 17,259 bytes, SHA-256
  `d49d171f1e6dea766ba1ff7bca9fce1a44ef38fff87fc3064b4071cdfb1ce9a4`.
- `authority/wikiversity/unit-21/UNIT_AUTHORITY_MANIFEST.json` binds 54 local
  authority files totaling 848,227 bytes, is itself 142,834 bytes, and has
  SHA-256
  `d85444ddfc66c8e77d52db3f3abc0a186e5dd598789edaaf890b3c09cf00f923`.
  An independent replay found no local or external byte/hash mismatch. Its
  final live replay revalidated 223 Wikiversity identities and both Commons
  PDF identities.

## Exercise and solution closure

The ordered worksheet contains 26 exercises. Exercises 1--21 are practice;
Exercises 22--26 are submitted work worth respectively 4, 4, 4, 3, and 3
points. Public source solutions exist only for Exercises 3 and 8, at revisions
1068126 and 1113184. Neither is a wrapper. Their complete recursive
transclusion closures contain respectively 9 and 17 pages.

The 9,992-byte map
`authority/wikiversity/unit-21/ORDERED_EXERCISE_MAP.json` has SHA-256
`9329621bbdd62df63f01d7298dc2a4a65a296211db131f8d8730b7d308fd5f47`.
All solution XML, HTML, parse, and recursive transclusion witnesses replay
exactly. No other solution is admitted.

## PDFs, zero-media closure, and component rights

Unit 21 has no substantive reader-media position. Its page image inventories
contain only the two official PDFs.

- Official lecture PDF: 189,481 bytes, 7 pages, SHA-256
  `12c5dd813cd7d574aaeca33c02dbab1f8cbc4de131030c31dd9eba4007e14ebd`.
- Official worksheet PDF: 155,433 bytes, 7 pages, SHA-256
  `5457b23d9e4dfb6054fa0cdd1d7c823440307ed4d4710a9af244573b8bf89440`.
- `authority/RIGHTS-unit-21.csv` is the 443-byte zero-media rights header,
  SHA-256
  `6b8de6f5a63f32d9f22e7fb69c98ba2d787121a2437a392602571504c2a1c544`.
- `authority/ASSET_CLOSURE-unit-21.json` is 5,705 bytes, SHA-256
  `8708a399d7c950101609281c14fe4e48eb02aa70335a7ad6cf7ef4194e9bc483`.
  It binds zero media positions and the complete rights/identity records for
  both PDFs.

Both PDFs' internal boilerplate says CC BY-SA 3.0, while the frozen current
course and Commons records identify them as CC BY-SA 4.0 components. The
current lecture also postdates its official PDF. The PDFs are therefore
licensed visual witnesses, not current semantic clones. The translated course
text remains CC BY-SA 4.0; this freeze makes no broader rights claim.

## Recorded source defects and bridge boundaries

The manifest explicitly binds all eleven audit-critical semantic pages.
Production must disclose rather than silently inherit these six defects:

1. Exercise 1 indexes the positive-monomial ideal by all of `M`, thereby
   including `T^0=1`; the intended index is `M_+`.
2. The order lemma, its proof exercise, Exercise 8, and Solution 8 evaluate
   `ord(f+g)` or `nu(f+g)` even though their functions exclude zero; require
   `f+g` nonzero rather than silently extending the codomain.
3. Exercise 6 is false over an arbitrary field. In characteristic 2 its
   equation is a square and the coordinate ring is nonreduced; in
   characteristic not 2 the ring is factorial exactly when `-1` is a square.
   The minimal hypotheses making its four requested conclusions true are
   characteristic not 2 and, for the nonfactorial part, `-1` nonsquare.
4. Exercise 12 omits the premise that `a` is a root from the multiple-root
   criterion `F'(a)=0`.
5. The lecture transition before Nakayama suppresses the hypotheses under
   which a principal maximal ideal characterizes a DVR; retain the preceding
   theorem's nonfield one-dimensional Noetherian local-domain scope.
6. Exercise 20 uses `n` in `m^(n+1)=m^n` without quantifying it.

A preliminary audit suspected that the zero-dimensional nilpotence lemma
switched from `S` in its statement to `R` in its proof. Independent replay
disproved that suspicion: pages 15866/revision 1088079 and 15870/revision
1086502 both expose the parameter `{{{R|R}}}`, while enclosing page
95386/revision 944013 invokes the statement-and-proof template with `R=S`.
The frozen expanded TeX and rendered HTML consequently use `S` throughout.
This is not a source correction and must not be disclosed as one.

Three omissions are additive reader bridges rather than source corrections:
the nilpotence proof's unexplained external prime-ideal lemma, the explicit
application of the nilpotence lemma to `R/(f)` in the DVR-characterization
proof, and the standard Nakayama corollary connecting minimal generators with
a basis modulo the maximal ideal. Each bridge must be visibly labeled and
must not be attributed to the source.
