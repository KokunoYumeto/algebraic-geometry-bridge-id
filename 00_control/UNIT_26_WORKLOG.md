# Unit 26 owner-production worklog

## Boundary and source identity

Unit 26 is the second internal unit in the substantial Units 25-27 milestone.
It is bound only to the official complete *Algebraische Kurven (Osnabrück
2012)* course and uses the `br-ak-2012-*` namespace. Units 1-24 and their
accepted public bytes remain unchanged; no per-unit publication transaction
occurred. The next cumulative reader/backend/publication boundary remains Unit
27.

- Course route: page 50687, revision 658236.
- Lecture: page 50732, revision 793526, MediaWiki SHA-1
  `57845c7bb535d0cccde6d289409a8dbbe684f2d8`; root plus 118 dependencies
  gives 119 identities, canonical-row SHA-256
  `f1a064c0531f9079633a57009c565f20a0520a0ef10cb2336ad3b52aa2d331b8`.
- Worksheet: page 50761, revision 793494, MediaWiki SHA-1
  `10aad7862403732dbaa5a05ae637a084c2758751`; root plus 57 dependencies
  gives 58 identities, canonical-row SHA-256
  `158fd9f6495ee9763d9e01cc1c0969a6be7c8b194dd88c4f8b12edbad900211f`.
- The worksheet has exactly 11 exercises: warm-up 1-4 and submitted 5-11.
  Exercise 3 displays 3 points. Submitted displayed points are 4, 4, 4, 4,
  4, 3, and 8 (31 total). Exercise 4 alone is starred and has the only public
  solution, page 21344, revision 1112503; its rooted closure has 10 identities
  and canonical-row SHA-256
  `8fd91e101676ccbe314c5905bb2ac8ccbf457c5d629962206124b6878c212d30`.
  The other ten exact candidate solution pages are proven absent.
- `authority/wikiversity/unit-26/UNIT_AUTHORITY_MANIFEST.json`: 118,791
  bytes, SHA-256
  `981fa3c86534514215c722b6d4f6d711c040a7829465f20ae18940373f94763c`.
  Its frozen time is preserved; a full replay regenerated the same bytes.
- `qa/UNIT_26_AUTHORITY_QA.json`: deterministic PASS, 2,621 bytes, SHA-256
  `f29ef929df95410f21752e5fc1c08ed01995cb94fc77cc5598b96dc04c1e2c1a`.
  Two additional owner replays were byte-identical. Final live identity replay
  covers 157 semantic pages, both official PDFs, and the Commons asset.

## Media, PDFs, and rights

Unit 26 adds one reader-media position, `Intersect3.png`. The selected 250 x
249 Commons thumbnail is 5,922 bytes with SHA-256
`b29c15edf6619632fe033e0b6064c1826226abce0be6219262ca028a2a157818`.
Michael Larsen is credited as creator and Maksim as Commons uploader; its
component licence remains CC BY-SA 3.0.

- `authority/RIGHTS-unit-26.csv`: 1,277 bytes, SHA-256
  `a03f4a998630ab426068253033abe3830cbb1d7a9caf03901b2254eb83d2e42b`.
- `authority/ASSET_CLOSURE-unit-26.json`: 5,850 bytes, SHA-256
  `18b1600f93fbd49a6d68f5d54ab45060f1911f3266da4b933dcbcd96b22f798f`.
- Official lecture PDF: 89,958 bytes, seven pages, SHA-256
  `9ec109463f2fe8f00ca9d3f6edb6f3a604d8c5c6f79ed5dd6584d41456da10c7`.
- Official worksheet PDF: 34,715 bytes, two pages, SHA-256
  `4b1dc786752f41daa80031e8563ba0446e2d1a6c039798779fd0681f617f1c92`.

Both PDFs are untagged authority witnesses. Their file surfaces retain the
legacy CC BY-SA 2.0 Germany notice alongside the current CC BY-SA 4.0
print/course route. No blanket relicensing claim is made.

## Translation and disclosed repairs

The complete natural Indonesian source preserves all 21 ordered lecture
entities, all 11 exercises, the sole public solution, one accessible image,
39 unique unit header IDs, and 346 Pandoc math nodes.

- `source/id-ID/lecture-26.md`: 21,417 bytes, SHA-256
  `1119ca7a9079dcc2bd1712c63067d08a32f74a031d6e140334208986461d51a6`.
- `source/id-ID/worksheet-26.md`: 7,267 bytes, SHA-256
  `e18bae8b225872c2cb3f9dffc91af5a9d7824282a2d74af55bba0934d08acfd8`.
- `source/id-ID/worksheet-26-solutions.md`: 3,349 bytes, SHA-256
  `4fe47d14fea117addf9256a9160d74afb0345c7ebe3adeb750ef531a609b610c`.
- `source/id-ID/media-credits-unit-26.md`: 2,446 bytes, SHA-256
  `65abf73c3a1d2555f577d97599080b5e9baa96a80c5f7cf5674961ff0f508c16`.
- `source/id-ID/frontmatter-units-01-26.md`: 4,616 bytes, SHA-256
  `b65af08094e4aa4031061ccf7a8359142dab032e28e9a2f051e9b652c92a3108`.

Nine terminology rows `AGT-0221` through `AGT-0229` and eleven disclosed
correction rows `AGC-CORR-0097` through `AGC-CORR-0107` are bound. The
repairs cover the eliminated-variable branch and one-variable localization,
the vertical-line proof case, the invalid transversality cross-reference,
the free point in the additivity theorem, the undefined global quotient
symbol, the missing no-common-component hypotheses, the degenerate line edge
case, the missing `V` in Exercise 11, the real-circle scope, and the duplicated
line classification in the public solution. No missing solution was invented.

At this frozen boundary `00_control/TERMINOLOGY.csv` is 35,577 bytes with
SHA-256 `d1305f559dcc00ac315f41905d1e672d557b30bc05aa3f6022b965a9b7f885a4`,
and `00_control/CORRECTIONS.csv` is 69,517 bytes with SHA-256
`9a73c0a59edd173732bf2c01d567c1912b427d402a2540b619ac948fc099d8a5`.

## Deterministic QA and next action

`scripts/qa_unit26_translation.py` is 46,829 bytes, SHA-256
`a7e55920eae0296a0d49d8f2a9a126466927c90d4a29b7d3925c39d092a5eb1d`.
Three consecutive executions, including two independent owner replays,
produced the same PASS receipt:
`qa/UNIT_26_TRANSLATION_QA.json`, 7,150 bytes, SHA-256
`c3de91128150957f17a0bd7d6b23ee588b0fcb8137f419588fdd2b2697bab762`.
It fails closed on authority, source/control identities, order, mathematics,
IDs, exercise/solution topology, image/accessibility/rights closure,
provenance, language residue, placeholders, Unicode dash characters, and
secret-like text.

Cumulative internal source coverage is now 26 lectures, 26 worksheets, 646
exercises, all 117 frozen public source solutions, and 84 reader-media
positions. The public reader remains the verified Unit 24 checkpoint. Next:
complete the already started official 2012 Unit 27 authority closure,
translate and verify Unit 27, then build, visually inspect, export, package,
publish, and anonymously read back the substantial Units 1-27 checkpoint in
the existing GitHub and Zenodo lineages.
