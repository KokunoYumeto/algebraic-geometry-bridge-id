# Unit 13 production worklog

## Boundary

Unit 13 is a verified internal translation checkpoint, not a new external
release. The existing public boundary remains Unit 12. Work continues in
source order at Unit 14; publication bookkeeping must not outrun reader
coverage.

## Authority and rights

The official lecture/worksheet authority closure is recorded in
`authority/UNIT_13_AUTHORITY_FREEZE.md`. Its 149,341-byte manifest has SHA-256
`dc86b4d124c7e775fb635a1f9672a8b8faadc4ff2259b0779f7bac6302d18848`.
It binds revisions 1112285 and 1065092, 313 transclusions, 37 exercises, 14
public solutions, and both official PDFs. All 60 manifest file identities
replay exactly.

Two substantive Commons SVGs and their PDF-safe PNG companions are frozen.
`authority/RIGHTS-unit-13.csv` is 3,677 bytes with SHA-256
`cdf370a6e3d7b80e137e6eb98a1180519b0cb97865ee39197de07c37e1a3c825`;
`authority/ASSET_CLOSURE-unit-13.json` is 4,489 bytes with SHA-256
`771a8f09fd262838873e1390c43cae7da1f3989b74d8d2a7f67a856da9ea5e23`.
Component rights and non-blank attribution are preserved.

## Indonesian translation

- `source/id-ID/lecture-13.md`: 14,295 bytes, SHA-256
  `6b2c8a6aac3c80a3bf45cdb83db085e59f72f09bb7829528f2719c6b7af178fa`.
- `source/id-ID/worksheet-13.md`: 16,401 bytes, SHA-256
  `b9dbf3ee514c8e7d59bdf60ba4617cb0b8a38b5e299cc65af53cdd8e7f56adcd`.
- `source/id-ID/worksheet-13-solutions.md`: 15,292 bytes, SHA-256
  `787b24f616ac7823c88b7f45ea827df5bbdea34be111bb36822d542121e89774`.
- `source/id-ID/media-credits-unit-13.md`: 742 bytes, SHA-256
  `f5aa7d11bb7fd29860bdaec51fdb03790fdd6361e6f0ef2b4fbac72040de1341`.

The translation contains every lecture block, all 37 exercises, all 14 frozen
public solutions, both media positions, 74 unique stable IDs, exact model
provenance `OpenAI Codex gpt-5.6-sol, Ultra.`, and no invented solution.
Terminology was extended for pelokalan, sistem multiplikatif, unsur idempoten,
gelanggang produk, clopen, and saturation.

Three source issues are disclosed and bound in `00_control/CORRECTIONS.csv`:
AGC-CORR-0028 corrects the contextual index in the quotient chain;
AGC-CORR-0029 repairs the false displayed identity
`V(g)=A_R^1=V(1)` to the intended empty zero loci; AGC-CORR-0030 replaces an
overstrong valuation equality with the equivalent coprimality argument.

## Deterministic QA and next action

`qa/UNIT_13_TRANSLATION_QA.json` reports PASS; it is 4,441 bytes with SHA-256
`f10a5fa657c17c17619edaaab7caa35a703c6c9f4b44e31ce7019aa28fbcc083`.
It validates all authority hashes, solution topology/revisions, official PDFs,
media/rights closure, source/control hashes, Pandoc AST parsing, stable IDs,
links, terminology, protected mathematics, corrections, German residue,
placeholders, and secret-like strings.

Next executable action: freeze Unit 14 lecture, worksheet, transclusions,
ordered exercises, all public solutions, official PDFs, media, and rights;
then translate and run the same bounded per-unit checks. Defer the next full
cumulative HTML/PDF/backend/publication transaction until the coherent Unit 15
milestone.
