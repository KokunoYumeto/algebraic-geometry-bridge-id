#!/usr/bin/env python3
"""Deterministically extend the frozen Units 1--15 backend through Unit 18.

The mature Unit 15 exporter is a frozen implementation template.  This thin,
fail-closed specialization verifies that template byte-for-byte, replaces only
the release constants and the bounded Units 16--18 data tables, and executes
the resulting exporter with this file as its identity.  The emitted manifest
binds both this specialization and the frozen template.  Every baseline JSONL
record is carried forward with its canonical serialized payload unchanged.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_EXPORTER = ROOT / "scripts" / "export_backend_units_01_15.py"
TEMPLATE_SHA256 = "0372ed27ac3f36879b611662b35aaf8340939e79a90291d3dfe9cdefc05cc165"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Exporter specialization expected one occurrence, found {count}: {old!r}")
    return text.replace(old, new, 1)


def replace_region(text: str, start: str, end: str, replacement: str) -> str:
    first = text.find(start)
    if first < 0:
        raise SystemExit(f"Exporter specialization start marker absent: {start!r}")
    last = text.find(end, first)
    if last < 0:
        raise SystemExit(f"Exporter specialization end marker absent: {end!r}")
    if text.find(start, first + 1) >= 0:
        raise SystemExit(f"Exporter specialization start marker is not unique: {start!r}")
    return text[:first] + replacement + text[last:]


if not TEMPLATE_EXPORTER.is_file() or digest(TEMPLATE_EXPORTER) != TEMPLATE_SHA256:
    raise SystemExit("Frozen Unit 15 exporter template is absent or has drifted")

generated = TEMPLATE_EXPORTER.read_text(encoding="utf-8")

# Current-boundary names are replaced before the new Unit 15 baseline is
# introduced, so the baseline path cannot be accidentally advanced to 18.
for old, new in (
    ("units-01-15", "units-01-18"),
    ("UNITS_01_15", "UNITS_01_18"),
    ("UNIT_15", "UNIT_18"),
    ("units0115", "units0118"),
    ("units_01_15", "units_01_18"),
    ("unit-15", "unit-18"),
    ("unit15", "unit18"),
    ("Unit 15", "Unit 18"),
    ("Units 1--15", "Units 1--18"),
    ("Units 13--15", "Units 16--18"),
    ("Unit 13--15", "Unit 16--18"),
    ("units_13_15", "units_16_18"),
    ("unit_13_15", "unit_16_18"),
):
    generated = generated.replace(old, new)

generated = replace_once(
    generated,
    'BASELINE = ROOT / "backend" / "units-01-12"',
    'BASELINE = ROOT / "backend" / "units-01-15"',
)
generated = generated.replace("backend/units-01-12", "backend/units-01-15")
generated = generated.replace("Units 1--12", "Units 1--15")
generated = generated.replace("units_01_12", "units_01_15")
generated = replace_once(
    generated,
    'BASELINE_MANIFEST_SHA256 = "9c22a4eb308fd5d50cca9151f3617b833fe800749de8087038386af952a683ce"',
    'BASELINE_MANIFEST_SHA256 = "5d8d6afec1a6fac89dbcbc396a374648a08e7493350aa876bfe6ac9b4684f571"',
)
generated = replace_once(
    generated,
    'BASELINE_RECORDS_SHA256 = "914d659bde3a32bce7f10b39f3f0ec12f852cffdfb6f83c12ca150d0ba1d3925"',
    'BASELINE_RECORDS_SHA256 = "0ec98ae73421c04ab7ff62387de35cd5f7cb9721ff8c4aff56ac47048e262ca8"',
)
generated = replace_once(
    generated,
    'BASELINE_SCHEMA_SHA256 = "4dbb0acff7e301420250f30cbe9457fd2df4469d820c82d3a30c7f09b7c2bc41"',
    'BASELINE_SCHEMA_SHA256 = "72f6249b930de994c31ac6bbbd6e3d8de86a2ae6eaa15b50f47f254b1fe22df1"',
)
generated = replace_once(generated, "BASELINE_RECORD_COUNT = 8491", "BASELINE_RECORD_COUNT = 10938")
generated = replace_once(
    generated,
    'PREVIOUS_EDITION = "edition.algebraic-geometry-bridge-id.units-01-12.2026-08-24"',
    'PREVIOUS_EDITION = "edition.algebraic-geometry-bridge-id.units-01-15.2026-08-24"',
)
generated = replace_once(
    generated,
    'CUMULATIVE_EDITION = "edition.algebraic-geometry-bridge-id.units-01-18.2026-08-24"',
    'CUMULATIVE_EDITION = "edition.algebraic-geometry-bridge-id.units-01-18.2026-08-25"',
)
generated = generated.replace('get("through_unit") == 15', 'get("through_unit") == 18')
generated = generated.replace('get("unit") == 15', 'get("unit") == 18')
generated = generated.replace('"through_unit": 15', '"through_unit": 18')
generated = generated.replace('payload.get("unit") == 18', 'payload.get("through_unit") == 18')
generated = replace_once(
    generated,
    '    rights_rows[unit] = read_csv(spec["rights"])',
    '    rights_rows[unit] = read_csv(spec["rights"])\n'
    '    for rights_row in rights_rows[unit]:\n'
    '        for optional_key in ("pdf_local_path", "pdf_local_bytes", "pdf_local_sha256"):\n'
    '            rights_row.setdefault(optional_key, "")',
)

generated = replace_region(
    generated,
    "SOURCE_FILES = [",
    "\n\n# Filled only",
    '''SOURCE_FILES = [
    ROOT / "source" / "id-ID" / "frontmatter-units-01-18.md",
    ROOT / "source" / "id-ID" / "lecture-16.md",
    ROOT / "source" / "id-ID" / "worksheet-16.md",
    ROOT / "source" / "id-ID" / "worksheet-16-solutions.md",
    ROOT / "source" / "id-ID" / "media-credits-unit-16.md",
    ROOT / "source" / "id-ID" / "lecture-17.md",
    ROOT / "source" / "id-ID" / "worksheet-17.md",
    ROOT / "source" / "id-ID" / "worksheet-17-solutions.md",
    ROOT / "source" / "id-ID" / "media-credits-unit-17.md",
    ROOT / "source" / "id-ID" / "lecture-18.md",
    ROOT / "source" / "id-ID" / "worksheet-18.md",
    ROOT / "source" / "id-ID" / "worksheet-18-solutions.md",
    ROOT / "source" / "id-ID" / "media-credits-unit-18.md",
]''',
)

generated = replace_region(
    generated,
    "EXPECTED_SOURCE_SHA256 = {",
    "\n\nTERMINOLOGY_CONCEPTS = {",
    '''EXPECTED_SOURCE_SHA256 = {
    "source/id-ID/frontmatter-units-01-18.md": "2b24a7d9c28a311768f206a270191598b6a233a0338f237628c2bac80437c4be",
    "source/id-ID/lecture-16.md": "c7cb0a1bc34e2003db18024d206c87d522a8df2082d186456d7a987cf0775d39",
    "source/id-ID/worksheet-16.md": "871ea30f571ebc9e0e2a7b1e4d30cddfe719822f48b2bdbe97bd6d8a52a5268a",
    "source/id-ID/worksheet-16-solutions.md": "5df1b9f46ba65622644feed0bf99191d5737d2edc2cc887c3b00efd2b50f8860",
    "source/id-ID/media-credits-unit-16.md": "4a5bc83795b780ad26bffe425924bb010b966ed49dcbd0c3b073bc3be77f7a99",
    "source/id-ID/lecture-17.md": "53bdc1f91f02a4b28dcc0c78247ef2ab9f5102377d8d0b6eedc88ed6879f37e8",
    "source/id-ID/worksheet-17.md": "2ec3c00332fad5683d56d9a608bf6544371732207312c4dc77c479621624efa0",
    "source/id-ID/worksheet-17-solutions.md": "5a56a15a9cb38ef4859a53ccd690309965c22a1fef54b018f162ec12fac6adef",
    "source/id-ID/media-credits-unit-17.md": "2647366a9bad10aff220f263a3a9c14d3620c43b42c0b4d2195e0c38d263f537",
    "source/id-ID/lecture-18.md": "319cca4f08a3a4ee0bf0fa2a9d525e0adcd2f6f639705dd1c2eb06580b7bfcd3",
    "source/id-ID/worksheet-18.md": "ec760a90d6f7462dbe71f755149886006e144bedc8ce11d09f72452472ee641e",
    "source/id-ID/worksheet-18-solutions.md": "10fcda87b4613fdf6bd037b8428ee46b82ffbfa73c182dbb3732602d0f683db4",
    "source/id-ID/media-credits-unit-18.md": "9e1f8c342873acbe70a43ab88718bba67cbe4ed10672afb77f2ed5c41a78f0c5",
}''',
)

generated = replace_region(
    generated,
    "TERMINOLOGY_CONCEPTS = {",
    "\n\nCORRECTION_TARGETS = {",
    '''TERMINOLOGY_CONCEPTS = {
    "AGT-0106": ("concept.irreducible-filter", "irreducible filter"),
    "AGT-0107": ("concept.generic-filter", "generic filter"),
    "AGT-0108": ("concept.generic-stalk", "generic stalk"),
    "AGT-0109": ("concept.morphism", "morphism"),
    "AGT-0110": ("concept.fiber", "fiber"),
    "AGT-0111": ("concept.forcing-algebra", "forcing algebra"),
    "AGT-0112": ("concept.monoid", "monoid"),
    "AGT-0113": ("concept.monoid-ring", "monoid ring"),
    "AGT-0114": ("concept.monoid-homomorphism", "monoid homomorphism"),
    "AGT-0115": ("concept.base-ring", "base ring"),
    "AGT-0116": ("concept.laurent-ring", "Laurent ring"),
    "AGT-0117": ("concept.r-valued-point", "R-valued point"),
    "AGT-0118": ("concept.difference-group", "difference group"),
    "AGT-0119": ("concept.cancellation-law", "cancellation law"),
    "AGT-0120": ("concept.unit-group", "unit group"),
    "AGT-0121": ("concept.divisor-stable", "divisor-stable"),
    "AGT-0122": ("concept.group-representation", "group representation"),
    "AGT-0123": ("concept.monomial-curve", "monomial curve"),
    "AGT-0124": ("concept.numerical-monoid", "numerical monoid"),
    "AGT-0125": ("concept.conductor", "conductor"),
    "AGT-0126": ("concept.embedding-dimension", "embedding dimension"),
    "AGT-0127": ("concept.multiplicity", "multiplicity"),
    "AGT-0128": ("concept.singularity-degree", "singularity degree"),
    "AGT-0129": ("concept.coprime", "coprime"),
}''',
)

generated = replace_region(
    generated,
    "CORRECTION_TARGETS = {",
    "\n\nUNIT_SPEC: dict[int, dict[str, Any]] = {",
    '''CORRECTION_TARGETS = {
    "AGC-CORR-0034": "br-ak-2025-2026-l16-rem-01",
    "AGC-CORR-0035": "br-ak-2025-2026-w16-sol-11",
    "AGC-CORR-0036": "br-ak-2025-2026-w16-sol-12",
    "AGC-CORR-0037": "br-ak-2025-2026-w16-sol-12",
    "AGC-CORR-0038": "br-ak-2025-2026-w16-sol-13",
    "AGC-CORR-0039": "br-ak-2025-2026-w16-ex-23",
    "AGC-CORR-0040": "br-ak-2025-2026-l17-s03",
    "AGC-CORR-0041": "br-ak-2025-2026-w17-ex-10",
    "AGC-CORR-0042": "br-ak-2025-2026-w17-ex-17",
    "AGC-CORR-0043": "br-ak-2025-2026-w17-sol-12",
    "AGC-CORR-0044": "br-ak-2025-2026-w17-sol-31",
    "AGC-CORR-0045": "br-ak-2025-2026-w17-ex-39",
    "AGC-CORR-0046": "br-ak-2025-2026-l18-def-01",
    "AGC-CORR-0047": "br-ak-2025-2026-l18-rem-01",
    "AGC-CORR-0048": "br-ak-2025-2026-l18-rem-02",
    "AGC-CORR-0049": "br-ak-2025-2026-l18-lem-02-proof",
    "AGC-CORR-0050": "br-ak-2025-2026-w18-sol-10",
}''',
)

generated = replace_region(
    generated,
    "UNIT_SPEC: dict[int, dict[str, Any]] = {",
    "\n\nREQUIRED_CLASSES = {",
    '''UNIT_SPEC: dict[int, dict[str, Any]] = {
    16: {
        "manifest": ROOT / "authority" / "wikiversity" / "unit-16" / "UNIT_AUTHORITY_MANIFEST.json",
        "map": ROOT / "authority" / "wikiversity" / "unit-16" / "ORDERED_EXERCISE_MAP.json",
        "rights": ROOT / "authority" / "RIGHTS-unit-16.csv",
        "closure": ROOT / "authority" / "ASSET_CLOSURE-unit-16.json",
        "exercise_count": 23,
        "solutions": (1, 10, 11, 12, 13, 15),
        "media_count": 4,
        "binary_surfaces": 4,
        "expected": {
            "manifest": "54c823b4aa99c6e37e1fd3f84754f290bb54500847800906569704c3b4d49da0",
            "map": "835029f5f5f46dea23486bd62edec6f4ab64667192c44504fee3af259e5b5266",
            "rights": "f7472100f99256c04367f0c8f6f41fa7eef361fbb60044a13fcd0c8f76a019ea",
            "closure": "561184965af9c75ee6812a103a435af9cf74f1c1b60ac7007b851ce66b5df555",
        },
    },
    17: {
        "manifest": ROOT / "authority" / "wikiversity" / "unit-17" / "UNIT_AUTHORITY_MANIFEST.json",
        "map": ROOT / "authority" / "wikiversity" / "unit-17" / "ORDERED_EXERCISE_MAP.json",
        "rights": ROOT / "authority" / "RIGHTS-unit-17.csv",
        "closure": ROOT / "authority" / "ASSET_CLOSURE-unit-17.json",
        "exercise_count": 39,
        "solutions": (3, 12, 31, 32),
        "media_count": 0,
        "binary_surfaces": 0,
        "expected": {
            "manifest": "c6747335c58fb3b4303cf3095705df7f991143f79d2d3598582a1cc8c99bef1a",
            "map": "f329f9d1a6fc2e862009acd4761ed8289da2cf4c8b42e057db275642c05a700e",
            "rights": "6b8de6f5a63f32d9f22e7fb69c98ba2d787121a2437a392602571504c2a1c544",
            "closure": "87c3d88789d822210b388e0c21e0e25a7418e77930e245ab2bc32916a0508d4f",
        },
    },
    18: {
        "manifest": ROOT / "authority" / "wikiversity" / "unit-18" / "UNIT_AUTHORITY_MANIFEST.json",
        "map": ROOT / "authority" / "wikiversity" / "unit-18" / "ORDERED_EXERCISE_MAP.json",
        "rights": ROOT / "authority" / "RIGHTS-unit-18.csv",
        "closure": ROOT / "authority" / "ASSET_CLOSURE-unit-18.json",
        "exercise_count": 28,
        "solutions": (3, 4, 10, 11, 15),
        "media_count": 1,
        "binary_surfaces": 1,
        "expected": {
            "manifest": "26a56a0ccad60414bf09320dc008d438ccf84b3dd11c12c31e80fa6088437033",
            "map": "8b55ef14cccbcab93ba99882d16e0f9888780353f7290eff8e1d2d6cd6bc4cd9",
            "rights": "8cbf29b0063c2463fe89f9dec67bda671f9ee366db2c91176e37d4ef3532fbb0",
            "closure": "69bfe604847dbb57fa21e07f8308901f02b87fba92c668b2b0fec27e3c2e8ad3",
        },
    },
}''',
)

# Bind the verified frozen implementation template as an explicit exporter
# source dependency in addition to this specialization and its independent QA.
generated = replace_once(
    generated,
    '    Path(__file__),\n    ROOT / "scripts" / "qa_backend_units_01_18.py",',
    '    Path(__file__),\n    TEMPLATE_EXPORTER,\n    ROOT / "scripts" / "qa_backend_units_01_18.py",',
)

namespace = {
    "__file__": str(Path(__file__).resolve()),
    "__name__": "__main__",
    "TEMPLATE_EXPORTER": TEMPLATE_EXPORTER,
}
exec(compile(generated, str(TEMPLATE_EXPORTER), "exec"), namespace)
