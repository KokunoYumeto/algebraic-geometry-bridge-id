# Unit 25 owner-production worklog

## Boundary and source edition

Unit 25 is the first internal source unit after the public Units 1-24
milestone and the second admitted unit from the complete official
*Algebraische Kurven (Osnabrück 2012)* course. Units 1-23 remain bound to the
separate 2025-2026 course; Unit 24 onward uses `br-ak-2012-*` IDs and must not
be described as part of that newer source edition. Accepted Units 1-24 and all
public release bytes remain unchanged. No external publication transaction is
performed at this per-unit boundary; the next cumulative release remains Unit
27.

## Frozen authority, topology, and rights

- Lecture page `50731`, revision `793525`, MediaWiki SHA-1
  `c589c3b9586e551eb81d7d941d79a9bc1461fe06`; root plus 69 recursive
  dependencies gives 70 identities, canonical-row SHA-256
  `aa14c07698e5e2911790457bee99f6e58a47b68fd5e75520c175ecc2756df8b1`.
- Worksheet page `50760`, revision `793493`, MediaWiki SHA-1
  `1418cec6171ff8fd056dda7e6461f5ca4d91d910`; root plus 61 recursive
  dependencies gives 62 identities, canonical-row SHA-256
  `92727348e69deb229c952710318393751f99b09fea0b41b4c855daeadcb62828`.
- The worksheet has 13 exercises: warm-up 1-5, submitted 6-12, and upload 13.
  Displayed submitted points are 4, 4, 4, 3, 4, 4, and 5 (total 28); upload
  Exercise 13 displays 4 points although its semantic component records 3.
  Exercises 1-2 are starred and are the only exercises with public solutions.
- Public Solution 1 is page `21296`, revision `1112930`, MediaWiki SHA-1
  `a388a7f91dd1a2c6759186a6c63de83eb93ba8e9`; root plus 11 dependencies gives
  12 identities, canonical-row SHA-256
  `cf8713fe21f8f85b327439235147d91ea4be82422f56750a3e70d51fd17e22fe`.
  Public Solution 2 is page `21581`, revision `1022975`, MediaWiki SHA-1
  `4e9bc137ff33d63de0728b6b9c40093ba7e95e46`; root plus eight dependencies
  gives nine identities, canonical-row SHA-256
  `9c6d058cb3adb20f94624e47caaf62847655243262aeda7d497cceae5a079e51`.
  Explicit API negative evidence closes candidate solutions 3-13.
- `authority/wikiversity/unit-25/UNIT_AUTHORITY_MANIFEST.json`: 108,049 bytes,
  SHA-256
  `7cafbca7b5fd080529c2019967647ef8ffa823539b2113caaf0ad65e56d6afc1`.
  Final live replay passed for 120 semantic identities and both official PDFs.
  The ordered exercise map is 16,373 bytes, SHA-256
  `1a887b81de9ccf9707e1e4835e477f9c9fb4a4358ab697242b17fd29873e8370`.
- Expanded lecture TeX is 22,932 bytes, SHA-256
  `47cd10c4b01ead8e51b1fa6e1e020900032bae6517030efd4cc116ef0ba1fe5e`;
  expanded worksheet TeX is 7,379 bytes, SHA-256
  `40661bb4202b74ed245da30306df0456c3b60d17ee62e054871386a70300514e`.
  Each `/latex` page is only the dynamic `{{Latex}}` launcher, so these
  expanded TeX files are byte-bound captures rather than immutable standalone
  revision bodies.
- Reader-media closure is zero. `authority/RIGHTS-unit-25.csv` is a
  header-only 443-byte file, SHA-256
  `6b8de6f5a63f32d9f22e7fb69c98ba2d787121a2437a392602571504c2a1c544`;
  `authority/ASSET_CLOSURE-unit-25.json` is 3,927 bytes, SHA-256
  `d177f9ca04beb707935ffa8695bbd9913b0fd081cbdbf2d8e77866c0c609b96f`.
- Official lecture PDF: 83,406 bytes, seven pages, SHA-256
  `2543659400dcdeae70e7b088ebd2acc3298444af944812a10e1ae87cc939c449`.
  Official worksheet PDF: 47,791 bytes, three pages, SHA-256
  `e111513289034c75da657a778b7ca699e1a5fda55749477e5696aa5afa00a8d5`.
  Both are untagged and retain the current CC BY-SA 4.0 course/print route
  alongside the legacy CC BY-SA 2.0 Germany file notice; no blanket
  relicensing claim is made.
- `scripts/freeze_unit25_authority.py`: 44,537 bytes, SHA-256
  `cec95599110021cfcfe3b49158a4f6edecd49bc6ed5fcd6151814cefffc64956`.
  It preserves the first-bound `frozen_utc` on replay rather than regenerating
  an unstable timestamp. `scripts/qa_unit25_authority.py`: 19,103 bytes,
  SHA-256
  `d0506ee1504bc6f363182d2ab21f8ad280c886e8ba6ab4c29adc2659b6090e88`.
  `authority/UNIT_25_AUTHORITY_FREEZE.md`: 2,883 bytes, SHA-256
  `753109fa305eb1e9815a4bd4cd6dcf747b824e21b25ab8fd55898cf90622d7bb`.
  Repeated QA executions reproduce `qa/UNIT_25_AUTHORITY_QA.json`, 2,857
  bytes, SHA-256
  `252b8beea4aa11575727b639da03ddba2a47f95b86945cbd13519a3db3e91252`.

## Disclosed source repairs and scope decisions

1. The graph-solution transition now uses `G(U(T))=T` and
   `H(U(T))=H-tilde(T)`, matching the displayed postcomposition by
   `T -> U(T)`, rather than the source's reversed `U(G(T))` and `U(H(T))`.
2. The theorem's ambiguous `a_0,b_0=0` is written explicitly as
   `a_0=b_0=0`.
3. The implicit-function remark restores the missing subject in the second
   field alternative: `K=R` or `K=C`.
4. Exercise 25.6 is explicitly interpreted over the real, characteristic-zero
   geometric setting because the source names a cardioid and tangent parameter
   without specifying a base field.
5. Exercise 25.7 requires `char(K) != 2`; in characteristic 2 its requested
   initial data make the coefficient of `T^2` equal to 1, so no solution can
   exist.
6. Exercise 25.13 visibly preserves the worksheet's displayed 4 points and
   the transcluded exercise component's authored 3 points.

These decisions are bound as `AGC-CORR-0091` through `AGC-CORR-0096`.

## Indonesian source and deterministic QA

- `source/id-ID/lecture-25.md`: 16,861 bytes, SHA-256
  `7cc97947851f8e81d94f4c95ff8698be3d68883f4437a2c9ea3668984fb71916`.
- `source/id-ID/worksheet-25.md`: 9,017 bytes, SHA-256
  `b14e559e69eef11553922ff521f5619edd2d2aae7bb160e989c23a52d72aef64`.
- `source/id-ID/worksheet-25-solutions.md`: 3,865 bytes, SHA-256
  `7480af475102a439bcb381911ddb32351a16505c4e5485e90ddfcd4252845fc8`.
- `source/id-ID/media-credits-unit-25.md`: 1,856 bytes, SHA-256
  `c6ccf54878cb00c9331d32dc4dbe36df88aea3e4962251509ace3d2b7529e9d7`.
- `source/id-ID/frontmatter-units-01-25.md`: 4,446 bytes, SHA-256
  `3e255ea40161fc49fbc98974ea1571efc91bdbc2a8d50ebe990535f644be4560`.

The sources preserve all nine ordered lecture entities, 13 exercises, exactly
two public solutions, 31 unique unit source/control IDs, 295 Pandoc math
nodes, the point/star/role topology, and zero media positions. Revision-credit
metadata distinguishes course authorship from root contributor Arbota and
solution-revision contributors Bocardodarapti and Arbota. Exact provenance is
`OpenAI Codex gpt-5.6-sol, Ultra.` No solution is invented.

Twelve terminology rows `AGT-0209` through `AGT-0220` are bound.
`00_control/TERMINOLOGY.csv` is 33,838 bytes, SHA-256
`8eda4f9055604bc6aaa529249869fb70e01c0fa464838a051020f6f0c247a1f0`;
`00_control/CORRECTIONS.csv` is 62,788 bytes, SHA-256
`b2cc62424c71e8540e435779236401c77fbd61ff6466eb5a0c2cc68483579c33`.

`scripts/qa_unit25_translation.py` is 44,818 bytes, SHA-256
`2e388f7d5bee289aa810445e311dbed50476151951335266ec34b753374bd50e`.
Independent consecutive executions reproduce a PASS receipt:
`qa/UNIT_25_TRANSLATION_QA.json`, 6,667 bytes, SHA-256
`07302ecb8be5a826f0423e773147c46a8a1b6485ced2e134f762be4e9d3bc81a`.
The gate replays all authority and external bytes, rights, topology, formulas,
IDs, corrections, terminology, Pandoc structure, Indonesian prose,
attribution, provenance, placeholders, unsafe Unicode controls, and
secret-like content.

## Current state and next executable action

Unit 25 is internally frozen, translated, corrected, independently audited,
and deterministically verified. Cumulative source coverage is now 25 lectures,
25 worksheets, 635 exercises, all 116 frozen public source solutions, and 83
media positions. The public reader remains the verified Unit 24 checkpoint;
publication cadence intentionally waits for the substantial Unit 27 boundary.

Next: complete the official 2012 Unit 26 authority freeze, translate its full
lecture, worksheet, every exercise, every lawful public solution, and media
credits, run the same per-unit gates, then repeat for Unit 27 before the
cumulative reader/backend/build/publication cycle.
