# Unit 12 translation findings

Status: **PASS — complete unit-local translation boundary**

This receipt covers only frozen Brenner Unit 12. It does not advance the shared
cursor, edit the shared glossary, invoke a build, perform Git operations, or
publish anything.

## Frozen authority consumed

- Lecture: page 165901, revision 1112280, MediaWiki SHA-1
  7273d05cc557ce9421f7cc42b6f70b8b28ba57e2.
- Worksheet: page 165931, revision 1067822, MediaWiki SHA-1
  c65053c29d4a96d478740742ae6d7157b48019fe.
- authority/wikiversity/unit-12/UNIT_AUTHORITY_MANIFEST.json — 122,858
  bytes; SHA-256
  181ce377bd68639b12511a9b1402ca03fd76c6107325195d3aa51a81b7286559.
- lecture-12.xml — 8,244 bytes; SHA-256
  5c7011a57a38a83222a6f5ea0001d00a5a811000510bea8ebcf00754457ec81d.
- lecture-12.html — 156,052 bytes; SHA-256
  be294d828d26708ed5524fffd6b89b8b858bc0104627d34b00c4ea68857fccf7.
- lecture-12-expanded.tex — 24,795 bytes; SHA-256
  1cbd13d735c9eade611094b6ab0eb7b3d1678abe589bb9b1e8b5a7d25d218b07.
- worksheet-12.xml — 7,430 bytes; SHA-256
  c9eabfdb542ec4a1cf6743eea85848e337bec0a82f37a6fce7f18ef2e33df858.
- worksheet-12.html — 106,541 bytes; SHA-256
  d0064ebc90c4c1d5298300bfe78b8e80672fc25b067a499bc20f38ddd209cc11.
- worksheet-12-expanded.tex — 15,306 bytes; SHA-256
  fce614601e7d40ba07b65692d0233ed93019a237444e4263aef2ab289ac9c961.
- ORDERED_EXERCISE_MAP.json — 11,288 bytes; SHA-256
  a37f874ffa17dd35ed4375f2956786793e475fcd5e2ded0333207c546e7e91db.
- Public solution witnesses: exercise 6 XML/HTML SHA-256
  501ac61733a2cb317b0195407b74729e5f09beace36a9da8764708e036ea11c6 /
  9a2e814ae1d08a3c0b56498135db9665031acb19c900bcb051f6f62c96016994;
  exercise 12 XML/HTML SHA-256
  e59d798d41b83bf59e9fb4931a5f122ffb538ee3f8341669ab8b07db9a632894 /
  46c5b70d1ff3b020b1050d6b38c5759a15cb9f6ca0895adb6177084f0c804cf8.

## Unit-local outputs

- source/id-ID/lecture-12.md — 18,692 bytes; SHA-256
  bab84765bec69ceef42a658579aa02162b45d4e1b2cdf55331031b1663596cd4.
- source/id-ID/worksheet-12.md — 13,722 bytes; SHA-256
  e4228a331ce1471dbef7e8f408ceaab309b8b92f51400a011998944e347fea99.
- source/id-ID/worksheet-12-solutions.md — 3,244 bytes; SHA-256
  aea4ad61cfc3bb7412f6690a850377c9418021aa5ff226173b51f9fb9b06d516.
  Blok LaTeX khusus-PDF `\\clearpage` mempertahankan HTML dan isi matematika,
  sekaligus mencegah judul solusi terbelah pada batas halaman pembaca kumulatif.
- source/id-ID/media-credits-unit-12.md — 1,622 bytes; SHA-256
  aefe17911251cd292ae4431441f122003a5307b2b9205918809e5c077de593c0.

## Deterministic parity checks

- Exercise sequence is exactly 1–30: 26 practice exercises followed by four
  submitted exercises, with point values, both source hints, and literal `★`
  markers on the two solution-bearing source exercises retained.
- All 30 upstream_entity comments match the ordered authority-map titles in
  exact order.
- Public-solution headings are exactly 12.6 and 12.12; no solution was
  invented for the other 28 exercises.
- The lecture retains all definitions, examples, lemmas, theorem/corollary,
  proposition items, proofs, warnings, tensor-product remark, displayed maps,
  ideals, zero loci, and functorial direction.
- Formula review covered every displayed source surface, including both
  quotient presentations, the three line/graph models, the definition of
  \(V(\mathfrak a)\), the spectrum–zero-locus bijection and its proof chain,
  \((\varphi^*)^{-1}D(f)=D(\varphi(f))\), all five proposition cases,
  the product/tensor formulas, every worksheet formula, and both solutions.
- Four image references occur in the frozen order and resolve to the four
  exact local binaries. Their byte counts and SHA-256 values match
  authority/ASSET_CLOSURE-unit-12.json; component rights are stated in the
  unit media-credit file.
- Markdown/YAML parsing with Pandoc returned exit 0 for all four substantive
  files.
- Across those four files, 57 explicit heading IDs were found and all 57 are
  unique.
- Placeholder scan, control-character scan, and bounded German-residual scan
  all returned zero findings.

## Source quirks handled without silent mathematical change

- The lecture uses \(X_i\) in both quotient presentations despite different
  ambient dimensions; this harmless reuse remains.
- The final lemma states \(R[X]\) but proves the result using \(R[T]\). These
  are dummy polynomial variables and both source choices remain visible.
- The source entity title speaks of “isomorphic” zero loci, while the theorem
  actually asserts only a homeomorphism. The Indonesian text preserves the
  theorem’s homeomorphism claim and does not silently strengthen it.
- The public solution to 12.6 calls the algebra \(A\), whereas the worksheet
  calls it \(R\). The solution retains \(A\) and carries an explicit edition
  note.
- In the injection proof, “differ on a variable” is rendered as “differ on at
  least one image of a variable,” making the quotient-generator meaning
  explicit without changing the argument.

## Terminology proposals for shared integration

These are proposed additions only; no shared glossary was edited:

- K-Spektrum → **spektrum-\(K\)**
- Spektrumsabbildung → **pemetaan spektrum**
- abgeschlossene Einbettung → **pembenaman tertutup**
- Einsetzungshomomorphismus → **homomorfisme substitusi** (already used in
  earlier admitted units)
- Tensorprodukt → **hasil kali tensor**
- Produkttopologie → **topologi produk**
- Identitätssatz → **teorema identitas**
- Funktor → **funktor**
