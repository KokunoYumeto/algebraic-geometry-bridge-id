# Unit 24 owner-production worklog

## Boundary and source-edition transition

Unit 24 is the third source unit for the substantial Units 1--24 cumulative
reader/backend/publication milestone. Units 1--23 remain bound to the frozen
official *Algebraische Kurven (Osnabrück 2025--2026)* revisions. Because that
course currently stops at Unit 23, Unit 24 is explicitly and independently
bound to the official complete older *Algebraische Kurven (Osnabrück 2012)*
course. It uses `br-ak-2012-*` IDs and must never be described as Unit 24 of
the 2025--2026 source edition. Accepted Units 1--23 and all public Units 1--21
bytes remain unchanged.

## Frozen authority, topology, and rights

- Lecture page `50730`, revision `933672`, MediaWiki SHA-1
  `af86fa9893c96376f910495b9a5d0c8be417b09e`; root plus 121 exact recursive
  dependencies gives 122 identities, canonical-row SHA-256
  `861c2d4566a137c9c3d791480bfa2f1f36a7885798f54f34c8e60557d34e75b2`.
- Worksheet page `50759`, revision `793492`, MediaWiki SHA-1
  `507a5966770c007e813734ca85da4e85f8a93b60`; root plus 64 exact recursive
  dependencies gives 65 identities, canonical-row SHA-256
  `b02b815554f0c5dbb4e8f5aceb6b7cc7faa747d9c7c1aa136facd1f62d1831f1`.
- The worksheet has ten exercises: practice 1--5 and submitted 6--10.
  Displayed submitted points are 5, 3, 3, 3, and 6 (total 20). Only Exercise
  4 is starred and has a public solution, page `168447`, revision `1068135`,
  MediaWiki SHA-1 `c7d3afd4c8e56433e1d4b12c4ebb8e10b460bec0`. Its root plus 17 exact
  dependencies gives 18 identities, canonical-row SHA-256
  `df98d341ed63b4cbd1b0051d725bfc8606937f489203941525b21bdfd54df7af`.
- `authority/wikiversity/unit-24/UNIT_AUTHORITY_MANIFEST.json`: 119,762 bytes,
  SHA-256
  `3731896a5980c565d9d69a2e01eee497f13b6f449f2f9c701fce726271c026a5`.
  Final live replay passed for 159 unique semantic Wikiversity identities and
  both local Wikiversity PDF identities.
- Expanded lecture TeX: 21,889 bytes, SHA-256
  `b391d18cc0cea33afedfff5e6db46842d2ef6504843336b71f44eda448f12f5e`.
  Expanded worksheet TeX: 3,771 bytes, SHA-256
  `37b53c3b6049ba45ff4aa1f4b7b4c4f0666e8a97248ba3c6c34a38061b758a4f`.
  Ordered exercise map: 10,121 bytes, SHA-256
  `250744d177bc2d5cf2a1cc506a99e05f1250c771de88b214a0e8d5cabfe7b9b8`.
- Reader-media closure is zero. `authority/RIGHTS-unit-24.csv` is a
  header-only 443-byte file with SHA-256
  `6b8de6f5a63f32d9f22e7fb69c98ba2d787121a2437a392602571504c2a1c544`;
  `authority/ASSET_CLOSURE-unit-24.json` is 5,802 bytes, SHA-256
  `6fe01774a095a6ed24549b8972fc1447d938a5d8868bd3bcc55691e88afea579`.
- Official lecture PDF: 90,541 bytes, six pages, SHA-256
  `916b8d41a946cdf8ac978112a46e4f6d1dfb6c70fc0efc65a689cb8ff7205df1`.
  Official worksheet PDF: 33,474 bytes, two pages, SHA-256
  `733135d556513d01148333551693db2713915ee82ac8faa8ce745e966c073102`.
  Both are untagged and preserve current CC BY-SA 4.0 print/course notices
  alongside legacy CC BY-SA 2.0 Germany file notices; no blanket relicensing
  claim is made.
- `scripts/freeze_unit24_authority.py`: 48,373 bytes, SHA-256
  `1b5af3021886bf5660bc25e80343d59882f65bbe3e4c636be212b691c5dff9ea`.
  `scripts/qa_unit24_authority.py`: 16,237 bytes, SHA-256
  `939a7ecbe048d0a8d5829615f74916c08d2ff2b0b5d94ddfc3f0bc2fe4ea14f2`.
  `authority/UNIT_24_AUTHORITY_FREEZE.md`: 3,945 bytes, SHA-256
  `0313f42a7716e4c918f2531cf927e3bff4b136712284fab13740c4610237e20e`.
  `qa/UNIT_24_AUTHORITY_QA.json` reports deterministic PASS and is 2,673
  bytes, SHA-256
  `60b99b9e90a96d1a7a049050b1e0a3c41220f365e61ca758472a01b7668f6ca7`.

## Mandatory reader repairs

1. Exercise 24.7 must use `C=V(Y^2-X^2-X^3)`, agreeing with its cited
   parametrization and object category, instead of the live displayed
   `X^2-Y^2-Y^3`; the change and characteristic-zero scope must be visible.
2. The proof of Corollary 24.8 must write the next coefficient of `G` as
   `b_{ell+1}`, not the live/PDF `a_{ell+1}`, and disclose the repair.
3. Public Solution 24.4 must restore the omitted operand as `P(0) != 0`,
   then use the localization universal property explicitly.

The reader follows the frozen live semantic `G=y^2+z^2-1` in the cylinder
example rather than the historical PDF's inconsistent `x^2` form. Additional
visible scope notes keep constancy on `K`-rational points, formal polynomial
chain rule, squared-radius parameters, and characteristic-zero tangent claims
mathematically precise.

## Current production state and next executable action

The authority freeze and deterministic authority QA are complete. All four
Indonesian sources are complete and an independent read-only audit passes:

- `source/id-ID/lecture-24.md`: 21,016 bytes, SHA-256
  `c57dbf838e6e83f2111654b2b35a11da8a63bd4d549676f1b4cc6b25a7692a62`.
- `source/id-ID/worksheet-24.md`: 5,482 bytes, SHA-256
  `8d4e1e91890d24f5724dc8c5ae8c62c50e09815f8ded388c42091e9604e41b1a`.
- `source/id-ID/worksheet-24-solutions.md`: 2,342 bytes, SHA-256
  `a824bb03e09d251cb006daa017d7034f6a1794f0496b07ad64c2b6110af868b7`.
- `source/id-ID/media-credits-unit-24.md`: 1,593 bytes, SHA-256
  `e63177d420cbb485f255dd5e54059ab4150c388391001c35ea61cb3a3085ec5e`.

The sources preserve all 22 ordered lecture components, ten exercises, the
sole public Solution 4, 36 unique `br-ak-2012-*` source/control IDs, exact
exercise stars and points, 276 Pandoc math nodes, and zero media positions.
`source/id-ID/frontmatter-units-01-24.md` truthfully identifies the edition
transition and cumulative coverage; it is 4,526 bytes, SHA-256
`aef9a6cd385233f1bdaae1075527d587b705e1e5b57e01c3a8bde376f0517a2c`.

Sixteen terminology rows `AGT-0193`--`AGT-0208` and eight correction rows
`AGC-CORR-0083`--`AGC-CORR-0090` are bound. `00_control/TERMINOLOGY.csv` is
31,718 bytes, SHA-256
`6193cbff180864b2cff942f9f99a79c24aab473c71f70c160ade356d34ef079d`;
`00_control/CORRECTIONS.csv` is 59,424 bytes, SHA-256
`4e06c3954eb1fb9845479a207626005ac4c1d21e909149b60b7a7ba4d3071579`.

`scripts/qa_unit24_translation.py` is 35,522 bytes, SHA-256
`3daf48aab28beb24eb3d2cf8e31336b5b84706f70822210f45d8b666848622af`.
It replayed the frozen authority, all source/control identities, 22 lecture
components, ten exercises, sole public solution, 36 IDs, 276 Pandoc math
nodes, zero-media rights closure, sixteen terminology rows, eight correction
rows, protected formulas, Indonesian residue, placeholders, Unicode controls,
and secret-like content. Three consecutive executions produced the same PASS
receipt: `qa/UNIT_24_TRANSLATION_QA.json`, 6,340 bytes, SHA-256
`bb7e2716cd1a6438e7e3ccfbec412c5e838c118f88a22d0090c41f0ca24a9011`.

## Frozen cumulative release and public readback

The cumulative self-contained HTML is 13,156,471 bytes, SHA-256
`3753f3a8dc15d8aa1916ecd461b555c3b854139e216cef18d92e6c699258d61f`.
The 417-page A4 PDF is 8,130,610 bytes, SHA-256
`407343d0a203e25cb6d5357907da4b6a66c6a4836c5e5fcf17b4599621d1a473`.
All-page visual review, desktop/mobile reflow, machine, protected-surface, and
accessibility gates pass. The native backend contains 18,488 records, SHA-256
`b2550dc11285eec35e1e08eef58284fcf5d88ea9206eabac9fd4b921df43f0c7`;
the additive common adapter validates 43,917 virtual records and reverses to
those exact native bytes.

The deterministic eight-file package is public in the existing Zenodo concept
as record 22102097 / DOI `10.5281/zenodo.22102097`; anonymous readback matched
all eight files. It is also public in the existing GitHub lineage at content
commit `fd8984aeb642de240af6a36aee4464d25791658a`, annotated tag object
`34f257cf2880d578bf0aa36748810ecbc8abd3ca`, and release `unit-24`;
anonymous readback matched all eight assets, raw-commit HTML/PDF, and live
Pages HTML/PDF. The sanitized receipts are
`qa/UNIT_24_ZENODO_PUBLICATION.json` and
`qa/UNIT_24_GITHUB_PUBLICATION.json`.

Next: freeze the official 2012 Unit 25 lecture, worksheet, two lawful public
solutions, PDF witnesses, recursive closure, and component-rights evidence;
run deterministic authority QA, then translate and verify Unit 25 in source
order without altering accepted Unit 1--24 bytes.
