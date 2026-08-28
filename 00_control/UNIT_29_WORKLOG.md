# Unit 29 owner worklog

Status: complete internal source boundary; authority and translation QA PASS.
Public cumulative boundary remains Unit 28. The next substantial release is
the complete 30-unit classical volume after Unit 30.

Date: 2026-08-28  
Lane: O016/D100 `algebraic-geometry-bridge-id`  
Source course: `Kurs:Algebraische Kurven (Osnabrück 2012)`  
Stable-ID namespace: `br-ak-2012-*`  
Provenance: `OpenAI Codex gpt-5.6-sol, Ultra.`

## Frozen authority

- Course surface: page 50687, revision 658236, MediaWiki SHA-1
  `2f2ede579cc59cdf7e93be763813704d6cb00b10`.
- Lecture: page 51996, revision 1069408, timestamp
  `2026-02-05T19:18:37Z`, MediaWiki SHA-1
  `6f0742211aeb307841634425937aad9037da51be`. Expanded TeX: 23,292 bytes,
  SHA-256 `7c06a1dbb12904bd5f89427955ef8bdae5781e402522cd70f09a0c6e1ef1e784`.
- Worksheet: page 50924, revision 1052757, timestamp
  `2025-08-27T18:11:31Z`, MediaWiki SHA-1
  `0e8dd5d1e5b9bf9552bdbd8f8c61c47ee2a0b726`. Expanded TeX: 5,439 bytes,
  SHA-256 `53a54b5b7e59be71c94d41dc791021c0b2d6165bf0b489670800b09387d560d2`.
- Lecture semantic closure: 106 dependencies plus root, canonical
  case-sensitive identity hash
  `87f4ba1e8fb06c51346d5d8fbb105bf2c48e7242a9de2e387906f9608380308b`.
- Worksheet semantic closure: 61 dependencies plus root, canonical hash
  `4b6d796d4888b94cfaa1c29811b60ea012118af4af993efd3fd4f23bc5f1229a`.
- Final live replay covers 150 distinct case-sensitive semantic identities in
  six batches of 25. This count deliberately does not collapse the two
  case-variant Wikiversity titles.
- Exercise map: 10 exercises; warm-up 1-5; submitted 6-10; source-authored
  points `2,4,3,3,4,3,3,3,3,5`; displayed submitted points total 17; stars
  2 and 3. Map SHA-256
  `75b07cabcb83cc12a6fd1259017f7e169c0ded461e7b7c94e65f033b71d12bc9`.
- Exactly two public solutions are frozen: Exercise 2, revision 1094621,
  XML SHA-256
  `2b468a1f7d9bebff884c001c3a475a212601b022896953c97e6a55026cf38f66`;
  Exercise 3, revision 1090273, XML SHA-256
  `50771bcf86505ee8429426f3488ef46af450a258629d4403a2bc16aa74abcaff`.
  Negative candidates are 1 and 4-10. No missing solution was invented.
- Official lecture PDF: 84,904 bytes, 6 pages, SHA-256
  `9f7082c66d493cd02a6e4f0579493ad1ba74ddec4b3777517c9ab6daa9610c6d`.
  Official worksheet PDF: 81,522 bytes, 3 pages, SHA-256
  `83986d2a9928c6e61ad7afa6d5a890e2b296c15a8706931c8c6da485b05079d2`.
- Authority manifest: 128,548 bytes, SHA-256
  `ec3b34ad387ae827ecaa365c4def3b0550f74b629d0db3873a7cc28dc0831bc5`.
  Freeze note: 3,828 bytes, SHA-256
  `f95d74fa5f43f72e52204c482bcc9fdc2ad4b50e109beef4ac602b3e27e81826`.
  Rights ledger: 2,939 bytes, SHA-256
  `4962c9a0a32e775a788f1098cf994d4e6714f67226ae30e155189778e826323c`.
  Asset closure: 10,549 bytes, SHA-256
  `d85f765a2ab195ed5c1ed12028c2558fcfadd227fa35ebf979267c4167e3f972`.
  Authority QA: PASS, 2,439 bytes, SHA-256
  `5632c075926fb6200d49c5f21d3425a5fed63dd67cf646128055fb96bf1afd00`.

## Media closure

The reader has two media positions, both public domain. The original
Lemniscate SVG is local at 1,087 bytes, SHA-256
`3e1753bdbf9a9e0068892d1c10c445c104033e2a100d2d0b68f349fc8e1324f4`.
The Commons original endpoint for `Tschirnhausen_cubic.png` returned HTTP 429
during the bounded capture, so no original-byte archive is claimed. Its
metadata identity is 64,767 bytes, SHA-1
`44a9bbaa597b2fce69ca491335199890546cfb3d`, 1100 by 1638. The selected
official 500-pixel Commons thumbnail is local at
`authority/assets/Tschirnhausen_cubic-500.png`, 83,502 bytes, 500 by 745,
SHA-256 `f3dda9da65db9e431f25ea77eb83f51aed2eff1c191dc1206e0759561ee613c7`.
The reader also preserves the Commons warning that the pictured curve is not
actually a Tschirnhausen cubic despite the filename.

## Translation and disclosed source handling

The lecture preserves all eight semantic entities and all proofs in source
order. The worksheet preserves all ten exercises, points, stars, media, and
the intentionally unresolved blank matrix/repeated-vector defect in Exercise
29.7 (`AGC-U29-SRC-002`). The solution file contains only Exercises 29.2 and
29.3. Five terminology bindings (`AGT-0261` through `AGT-0265`) were admitted.

Four source repairs are explicit in the reader and in
`00_control/CORRECTIONS.csv`:

1. `AGC-CORR-0126` changes the undefined `g >= 3` to the defined degree
   `d >= 3` in the polynomial-graph multiplicity proof.
2. `AGC-CORR-0127` assigns zeros and poles to the rational function `g/h`,
   rather than to the glued morphism.
3. `AGC-CORR-0128` uses `V_+` for the homogeneous projective graph equation.
4. `AGC-CORR-0129` uses `V_+` for the projective monomial-curve closure while
   retaining `V` on affine charts.

Canonical translations:

- `source/id-ID/lecture-29.md`: 19,163 bytes, SHA-256
  `3ed412b4c719d3ac03574013d5acc2bf8316ecc9a09ef33d286433400d5da951`.
- `source/id-ID/worksheet-29.md`: 7,831 bytes, SHA-256
  `d061f5fb7132fa7e3c427f77ea3efce3dc07f4234c3cd4fa9389b03eff95d26b`.
- `source/id-ID/worksheet-29-solutions.md`: 4,232 bytes, SHA-256
  `6ef42d1bdc9fab47fa0c2685b8754d3f9be14f0738c6c280f0f8ada89c6bd505`.
- `source/id-ID/media-credits-unit-29.md`: 2,734 bytes, SHA-256
  `757ce4a42a2bdea04e8410609e68be7b5939d636cc72e26ae40007093d5fd7ae`.
- `source/id-ID/frontmatter-units-01-29.md`: 5,324 bytes, SHA-256
  `fe21529faf5781ddbbacd58acc87e80bb9fcdabc1d32ec06f9050e2283de7c6c`.

## Deterministic gate and next action

`scripts/qa_unit29_translation.py` validates exact authority/source/control
hashes; semantic/exercise/solution topology; protected formulas; Pandoc AST
and stable IDs; terminology and corrections; Indonesian/German residue;
placeholders, secrets, invisible controls; media bytes/alt text/rights; and
cumulative counts. Result: PASS. The receipt
`qa/UNIT_29_TRANSLATION_QA.json` is 6,802 bytes, SHA-256
`7789a7a131bcf44946204f52c328e24fa96fee0c1e24383994d4485437bffb81`.

The cumulative internal source boundary is now 29 lectures, 29 worksheets,
681 exercises, all 120 frozen public solutions, and 100 media positions.
Unit 28 remains the latest built and public reader/backend boundary. Next
executable action: freeze official 2012 Unit 30 authority, translate and
verify it, then run the complete 30-unit classical reader, PDF, visual,
responsive, protected-surface, native-backend, common-adapter, packaging,
GitHub/Pages, Zenodo, and anonymous public-byte gates.
