#!/usr/bin/env python3
"""Independently validate the cumulative native backend through Unit 21.

The frozen Unit 15 QA is the byte-pinned implementation template.  This
specialization independently checks the Unit 18 raw-byte baseline and schema,
Units 19--21 source/authority/ledger closure, the four cumulative milestone
PASS receipts, three per-unit evidence receipts, global tuple order, canonical
CRLF JSONL, typed shards, and an in-place deterministic replay.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_QA = ROOT / "scripts" / "qa_backend_units_01_15.py"
TEMPLATE_SHA256 = "4d444b164487fabdea28c7ff6efff13f0a5155e475115e385d08735abb692e11"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Backend-QA specialization expected one occurrence, found {count}: {old!r}")
    return text.replace(old, new, 1)


def replace_region(text: str, start: str, end: str, replacement: str) -> str:
    first = text.find(start)
    if first < 0:
        raise SystemExit(f"Backend-QA specialization start marker absent: {start!r}")
    last = text.find(end, first)
    if last < 0:
        raise SystemExit(f"Backend-QA specialization end marker absent: {end!r}")
    if text.find(start, first + 1) >= 0:
        raise SystemExit(f"Backend-QA specialization start marker is not unique: {start!r}")
    return text[:first] + replacement + text[last:]


if not TEMPLATE_QA.is_file() or digest(TEMPLATE_QA) != TEMPLATE_SHA256:
    raise SystemExit("Frozen Unit 15 backend-QA template is absent or has drifted")

generated = TEMPLATE_QA.read_text(encoding="utf-8")
for old, new in (
    ("units-01-15", "units-01-21"),
    ("UNITS_01_15", "UNITS_01_21"),
    ("UNIT_15", "UNIT_21"),
    ("units0115", "units0121"),
    ("units_01_15", "units_01_21"),
    ("unit-15", "unit-21"),
    ("unit15", "unit21"),
    ("Unit 15", "Unit 21"),
    ("Units 1--15", "Units 1--21"),
    ("Units 13--15", "Units 19--21"),
    ("Unit 13--15", "Unit 19--21"),
    ("units_13_15", "units_19_21"),
    ("unit_13_15", "unit_19_21"),
):
    generated = generated.replace(old, new)

generated = replace_once(generated, "import re\n", "import re\nimport subprocess\nimport sys\n")
generated = replace_once(
    generated,
    'BASELINE = ROOT / "backend" / "units-01-12"',
    'BASELINE = ROOT / "backend" / "units-01-18"',
)
generated = generated.replace("Units 1--12", "Units 1--18")
generated = generated.replace("units_01_12", "units_01_18")
generated = replace_once(
    generated,
    'BASELINE_MANIFEST_SHA256 = "9c22a4eb308fd5d50cca9151f3617b833fe800749de8087038386af952a683ce"',
    'BASELINE_MANIFEST_SHA256 = "fe9bfb98528d03d5d82f6d0ff66e3b15d2e28defd64190b3ec293f8dfd0ab96a"',
)
generated = replace_once(
    generated,
    'BASELINE_RECORDS_SHA256 = "914d659bde3a32bce7f10b39f3f0ec12f852cffdfb6f83c12ca150d0ba1d3925"',
    'BASELINE_RECORDS_SHA256 = "c952ca6c0a6b36f2138c0971161b11582bbb1479795bf36c9d1de23e4343e517"',
)
generated = replace_once(
    generated,
    'BASELINE_SCHEMA_SHA256 = "4dbb0acff7e301420250f30cbe9457fd2df4469d820c82d3a30c7f09b7c2bc41"',
    'BASELINE_SCHEMA_SHA256 = "3158825c0bd1c0da54c1c670630e7a8a2299b2b0d82e0f905042e76d7630906a"',
)
generated = replace_once(generated, "BASELINE_RECORD_COUNT = 8491", "BASELINE_RECORD_COUNT = 13626")
generated = replace_once(
    generated,
    'PREVIOUS_EDITION = "edition.algebraic-geometry-bridge-id.units-01-12.2026-08-24"',
    'PREVIOUS_EDITION = "edition.algebraic-geometry-bridge-id.units-01-18.2026-08-25"',
)
generated = replace_once(
    generated,
    'CUMULATIVE_EDITION = "edition.algebraic-geometry-bridge-id.units-01-21.2026-08-24"',
    'CUMULATIVE_EDITION = "edition.algebraic-geometry-bridge-id.units-01-21.2026-08-25"',
)
generated = generated.replace('get("through_unit") == 15', 'get("through_unit") == 21')
generated = generated.replace('["payload"].get("through_unit") == 15', '["payload"].get("through_unit") == 21')
generated = generated.replace('"through_unit": 15', '"through_unit": 21')
generated = generated.replace('relation_counts["corrects"] == 6', 'relation_counts["corrects"] == len(CORRECTION_TARGETS)')
generated = replace_once(
    generated,
    'require(schema.get("title", "").endswith("Units 1--21"), "Backend record schema title is stale")',
    'require(digest(SCHEMA_PATH) == BASELINE_SCHEMA_SHA256, "Unit 18 record schema bytes were not preserved")',
)

generated = replace_region(
    generated,
    'MACHINE_QA_PATH = ROOT / "qa" / "UNITS_01_21_MACHINE_QA.json"',
    'CORRECTIONS_PATH = ROOT / "00_control" / "CORRECTIONS.csv"',
    '''MACHINE_QA_PATH = ROOT / "qa" / "UNITS_01_21_MACHINE_QA.json"
VISUAL_QA_PATH = ROOT / "qa" / "UNITS_01_21_VISUAL_QA.json"
RESPONSIVE_QA_PATH = ROOT / "qa" / "UNITS_01_21_RESPONSIVE_QA.json"
PROTECTED_QA_PATH = ROOT / "qa" / "UNIT_21_PROTECTED_SURFACES.json"
UNIT_19_QA_PATH = ROOT / "qa" / "UNIT_19_INTEGRATION_QA.json"
UNIT_20_QA_PATH = ROOT / "qa" / "UNIT_20_TRANSLATION_QA.json"
UNIT_21_QA_PATH = ROOT / "qa" / "UNIT_21_TRANSLATION_QA.json"
''',
)
generated = replace_once(
    generated,
    '        rights_rows = list(csv.DictReader(stream))',
    '        rights_rows = list(csv.DictReader(stream))\n'
    '        for rights_row in rights_rows:\n'
    '            for optional_key in ("pdf_local_path", "pdf_local_bytes", "pdf_local_sha256"):\n'
    '                rights_row.setdefault(optional_key, "")',
)
generated = replace_once(
    generated,
    '        for row in csv.DictReader(stream):\n            asset = next(record for record in records if record["stable_id"] == row["asset_id"])',
    '        for row in csv.DictReader(stream):\n'
    '            for optional_key in ("pdf_local_path", "pdf_local_bytes", "pdf_local_sha256"):\n'
    '                row.setdefault(optional_key, "")\n'
    '            asset = next(record for record in records if record["stable_id"] == row["asset_id"])',
)

generated = replace_region(
    generated,
    "SOURCE_FILES = [",
    "\n\nEXPECTED_SOURCE_SHA256 = {",
    '''SOURCE_FILES = [
    ROOT / "source" / "id-ID" / "frontmatter-units-01-21.md",
    ROOT / "source" / "id-ID" / "lecture-19.md",
    ROOT / "source" / "id-ID" / "worksheet-19.md",
    ROOT / "source" / "id-ID" / "worksheet-19-solutions.md",
    ROOT / "source" / "id-ID" / "media-credits-unit-19.md",
    ROOT / "source" / "id-ID" / "lecture-20.md",
    ROOT / "source" / "id-ID" / "worksheet-20.md",
    ROOT / "source" / "id-ID" / "worksheet-20-solutions.md",
    ROOT / "source" / "id-ID" / "media-credits-unit-20.md",
    ROOT / "source" / "id-ID" / "lecture-21.md",
    ROOT / "source" / "id-ID" / "worksheet-21.md",
    ROOT / "source" / "id-ID" / "worksheet-21-solutions.md",
    ROOT / "source" / "id-ID" / "media-credits-unit-21.md",
]''',
)
generated = replace_region(
    generated,
    "EXPECTED_SOURCE_SHA256 = {",
    "\n\nTERMINOLOGY_CONCEPTS = {",
    '''EXPECTED_SOURCE_SHA256 = {
    "source/id-ID/frontmatter-units-01-21.md": "560b34060b3a2dc083d5a97238483c3f542c2928db9a435df63cea4db5d1c7aa",
    "source/id-ID/lecture-19.md": "7c364a2364aaa5b5980e4a113bb903831b4ade4af813658357a50e1a757021af",
    "source/id-ID/worksheet-19.md": "23d8218f94d8a29b2c6bd0ed471c56f760fe00e824e9d70a19edfaa22adfb86f",
    "source/id-ID/worksheet-19-solutions.md": "eaae6e95ecc909693bd2622136d9812497343dde81ac8617eb2f6a079beb3216",
    "source/id-ID/media-credits-unit-19.md": "498212f6e34bba635ac89a320b207ac65cb3093d4bbeb04998f193e56429e21e",
    "source/id-ID/lecture-20.md": "ccedeb464364a71f98f7450359ec6baa2c5135651e9e6e098de2772bf337ce66",
    "source/id-ID/worksheet-20.md": "50418f12f8f620736db8a6c9689902addc21308ebd4a0ebccfc18266a4156a99",
    "source/id-ID/worksheet-20-solutions.md": "2b1d9e9bee2c9285b50c52128d20a4e769379ccb51193192bdf9567ca16d064a",
    "source/id-ID/media-credits-unit-20.md": "02c00101d4e11df536c49ec6ffcaedc2f4a03215e867daa86c6bb81686704f1a",
    "source/id-ID/lecture-21.md": "4bfbb794483fdc0466acda10c7e63fa09891ad8da435888b2b59a0e051c7b8a6",
    "source/id-ID/worksheet-21.md": "9fe5a9e27c5de0b17ec1e0512c1d4368d21ad886c7bc5f4d4a27b6a27bf089f9",
    "source/id-ID/worksheet-21-solutions.md": "e872b5002fa8bf278e907b8247a74a23f9efb09eeba1f4610df655dd5d25c4bc",
    "source/id-ID/media-credits-unit-21.md": "e4076d9aa394dd6901e49dd9c73216eb80d8f0938ea7571f4d6cc30d87e44f67",
}''',
)

generated = replace_region(
    generated,
    "TERMINOLOGY_CONCEPTS = {",
    "\n\nCORRECTION_TARGETS = {",
    '''TERMINOLOGY_CONCEPTS = {
    "AGT-0130": "concept.quotient-ring-presentation",
    "AGT-0131": "concept.integrality",
    "AGT-0132": "concept.integrality-equation",
    "AGT-0133": "concept.integral-element",
    "AGT-0134": "concept.integral-closure",
    "AGT-0135": "concept.integrally-closed",
    "AGT-0136": "concept.integral-ring-homomorphism",
    "AGT-0137": "concept.adjugate-matrix",
    "AGT-0138": "concept.binomial-equation",
    "AGT-0139": "concept.twisted-cubic",
    "AGT-0140": "concept.normalization",
    "AGT-0141": "concept.normal-integral-domain",
    "AGT-0142": "concept.torsion-free",
    "AGT-0143": "concept.polyhedral-cone",
    "AGT-0144": "concept.half-space",
    "AGT-0145": "concept.conductor-ideal",
    "AGT-0146": "concept.dual-monoid",
    "AGT-0147": "concept.divisor-class-group",
    "AGT-0148": "concept.local-property",
    "AGT-0149": "concept.root-of-unity",
    "AGT-0150": "concept.discrete-valuation-ring",
    "AGT-0151": "concept.discrete-valuation",
    "AGT-0152": "concept.valuation-order",
    "AGT-0153": "concept.vanishing-order",
    "AGT-0154": "concept.uniformizer",
    "AGT-0155": "concept.formal-derivative",
    "AGT-0156": "concept.formal-differentiation",
    "AGT-0157": "concept.multiple-root",
    "AGT-0158": "concept.power-series",
    "AGT-0159": "concept.power-series-ring",
    "AGT-0160": "concept.ideal-product",
    "AGT-0161": "concept.total-divisibility-relation",
    "AGT-0162": "concept.prime-element",
    "AGT-0163": "concept.associate-relation",
    "AGT-0164": "concept.noetherian",
    "AGT-0165": "concept.submodule",
    "AGT-0166": "concept.quotient-module",
    "AGT-0167": "concept.residue-field",
}''',
)
generated = replace_region(
    generated,
    "CORRECTION_TARGETS = {",
    "\n\nUNIT_SPEC: dict[int, dict[str, Any]] = {",
    '''CORRECTION_TARGETS = {
    "AGC-CORR-0051": "br-ak-2025-2026-l19-thm-01-proof",
    "AGC-CORR-0052": "br-ak-2025-2026-l19-thm-01-proof",
    "AGC-CORR-0053": "br-ak-2025-2026-l19-exa-02",
    "AGC-CORR-0054": "br-ak-2025-2026-w19-sol-12",
    "AGC-CORR-0055": "br-ak-2025-2026-l20-exa-02",
    "AGC-CORR-0056": "br-ak-2025-2026-l20-thm-03-proof",
    "AGC-CORR-0057": "br-ak-2025-2026-l20-thm-03-proof",
    "AGC-CORR-0058": "br-ak-2025-2026-w20-sol-14",
    "AGC-CORR-0059": "br-ak-2025-2026-w20-sol-17",
    "AGC-CORR-0060": "br-ak-2025-2026-l20-thm-04-proof",
    "AGC-CORR-0061": "br-ak-2025-2026-w20-ex-18",
    "AGC-CORR-0062": "br-ak-2025-2026-w21-ex-01",
    "AGC-CORR-0063": "br-ak-2025-2026-l21-lem-02",
    "AGC-CORR-0064": "br-ak-2025-2026-w21-ex-06",
    "AGC-CORR-0065": "br-ak-2025-2026-w21-ex-12",
    "AGC-CORR-0066": "br-ak-2025-2026-l21-thm-01",
    "AGC-CORR-0067": "br-ak-2025-2026-w21-ex-20",
    "AGC-CORR-0068": "br-ak-2025-2026-l21-lem-03-proof",
    "AGC-CORR-0069": "br-ak-2025-2026-l21-thm-01-proof",
    "AGC-CORR-0070": "br-ak-2025-2026-l21-lem-04-proof",
}''',
)

generated = replace_region(
    generated,
    "UNIT_SPEC: dict[int, dict[str, Any]] = {",
    "\n\nREQUIRED_CLASSES = {",
    '''UNIT_SPEC: dict[int, dict[str, Any]] = {
    19: {
        "manifest": ROOT / "authority" / "wikiversity" / "unit-19" / "UNIT_AUTHORITY_MANIFEST.json",
        "map": ROOT / "authority" / "wikiversity" / "unit-19" / "ORDERED_EXERCISE_MAP.json",
        "rights": ROOT / "authority" / "RIGHTS-unit-19.csv",
        "closure": ROOT / "authority" / "ASSET_CLOSURE-unit-19.json",
        "exercise_count": 15, "solutions": (4, 12), "media_count": 1, "binary_surfaces": 1,
        "expected": {
            "manifest": "52245060a54f973b4fba19878eec234904430b9e5058defdbd9feaa7a868080e",
            "map": "f75bcc8e564cef327687b486bb074fa8c799b065994f4a1d79e7abf2b78b30dd",
            "rights": "1feb699d361be0379de5c785cc6c073adf3d47d31c8b07df3db1d3fc6ed7bdb1",
            "closure": "4ee0c05610b30f25038484a4dc147bdcddda9ebb29cfbded53d4e72a5b32be4e",
        },
    },
    20: {
        "manifest": ROOT / "authority" / "wikiversity" / "unit-20" / "UNIT_AUTHORITY_MANIFEST.json",
        "map": ROOT / "authority" / "wikiversity" / "unit-20" / "ORDERED_EXERCISE_MAP.json",
        "rights": ROOT / "authority" / "RIGHTS-unit-20.csv",
        "closure": ROOT / "authority" / "ASSET_CLOSURE-unit-20.json",
        "exercise_count": 23, "solutions": (1, 3, 4, 5, 12, 13, 14, 17), "media_count": 1, "binary_surfaces": 1,
        "expected": {
            "manifest": "b063e5edc556cd18598389083ea27ea7f255edfe2ae00e13ebf24de76e5b37d7",
            "map": "c74da7b0627cf8c8c694c0a9f20e94b0c7dc00ecd6c95b72ad21ae4a6c5c07ea",
            "rights": "09b85688b10784cf2c7e7aec9d017eb4d0403faf0b96ef8561b789168d19f565",
            "closure": "5ab57774999d4f293533a8fb14ad4e50d6caa1fba3d2664428c32d15f935c185",
        },
    },
    21: {
        "manifest": ROOT / "authority" / "wikiversity" / "unit-21" / "UNIT_AUTHORITY_MANIFEST.json",
        "map": ROOT / "authority" / "wikiversity" / "unit-21" / "ORDERED_EXERCISE_MAP.json",
        "rights": ROOT / "authority" / "RIGHTS-unit-21.csv",
        "closure": ROOT / "authority" / "ASSET_CLOSURE-unit-21.json",
        "exercise_count": 26, "solutions": (3, 8), "media_count": 0, "binary_surfaces": 0,
        "expected": {
            "manifest": "d85444ddfc66c8e77d52db3f3abc0a186e5dd598789edaaf890b3c09cf00f923",
            "map": "9329621bbdd62df63f01d7298dc2a4a65a296211db131f8d8730b7d308fd5f47",
            "rights": "6b8de6f5a63f32d9f22e7fb69c98ba2d787121a2437a392602571504c2a1c544",
            "closure": "8708a399d7c950101609281c14fe4e48eb02aa70335a7ad6cf7ef4194e9bc483",
        },
    },
}''',
)

# Re-run the exporter once and require every native output hash to remain
# unchanged. This is a real deterministic replay, not a manifest assertion.
generated = replace_once(
    generated,
    'manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))',
    '''require(MANIFEST_PATH.is_file(), "Missing initial Unit 21 backend manifest for deterministic replay")
initial_manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
replay_paths = [MANIFEST_PATH] + [ROOT / row["path"] for row in initial_manifest.get("files", [])]
require(all(path.is_file() for path in replay_paths), "Initial Unit 21 backend output closure is incomplete")
before_replay = {rel(path): digest(path) for path in replay_paths}
replay = subprocess.run(
    [sys.executable, "-B", str(ROOT / "scripts" / "export_backend_units_01_21.py")],
    cwd=ROOT,
    capture_output=True,
    text=True,
)
require(replay.returncode == 0, f"Deterministic exporter replay failed: {replay.stderr.strip()}")
after_replay = {rel(path): digest(path) for path in replay_paths}
require(before_replay == after_replay, "Unit 21 backend changed across an identical deterministic replay")
manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))''',
)

# Strengthen the inherited validator with exact CRLF raw-line identity and
# global tuple ordering, including canonical bytes for every newly added line.
generated = replace_once(
    generated,
    'require(len(records) == manifest["record_count"], "Manifest record count mismatch")',
    '''require(len(records) == manifest["record_count"], "Manifest record count mismatch")
require(
    [(row["entity_class"], row["stable_id"]) for row in records]
    == sorted((row["entity_class"], row["stable_id"]) for row in records),
    "Backend records are not globally ordered by (entity_class, stable_id)",
)

def raw_crlf_map(path: Path) -> dict[str, bytes]:
    data = path.read_bytes()
    require(data.endswith(b"\\r\\n"), f"JSONL lacks terminal CRLF: {rel(path)}")
    require(b"\\n" not in data.replace(b"\\r\\n", b""), f"JSONL contains lone LF: {rel(path)}")
    require(b"\\r" not in data.replace(b"\\r\\n", b""), f"JSONL contains lone CR: {rel(path)}")
    result: dict[str, bytes] = {}
    for raw in data[:-2].split(b"\\r\\n"):
        row = json.loads(raw.decode("utf-8"))
        require(row["stable_id"] not in result, f"Duplicate raw stable ID: {row['stable_id']}")
        result[row["stable_id"]] = raw
    return result

baseline_raw_bytes = raw_crlf_map(BASELINE / "records.jsonl")
candidate_raw_bytes = raw_crlf_map(RECORDS_PATH)
require(len(baseline_raw_bytes) == BASELINE_RECORD_COUNT, "Unit 18 raw-byte baseline count mismatch")
require(set(baseline_raw_bytes) <= set(candidate_raw_bytes), "Unit 21 backend dropped a Unit 18 raw stable ID")
require(
    all(candidate_raw_bytes[key] == raw for key, raw in baseline_raw_bytes.items()),
    "A Unit 18 serialized record byte changed",
)
require(
    all(
        raw == canonical(json.loads(raw.decode("utf-8"))).encode("utf-8")
        for key, raw in candidate_raw_bytes.items()
        if key not in baseline_raw_bytes
    ),
    "A new Unit 19--21 record is not canonical UTF-8 JSON",
)
for entity_class in sorted(REQUIRED_CLASSES):
    shard_path = BACKEND / f"{entity_class}.jsonl"
    require(shard_path.is_file(), f"Missing typed backend shard: {rel(shard_path)}")
    expected_shard = b"".join(
        candidate_raw_bytes[row["stable_id"]] + b"\\r\\n"
        for row in records
        if row["entity_class"] == entity_class
    )
    require(shard_path.read_bytes() == expected_shard, f"Typed shard diverges from combined JSONL: {entity_class}")
expected_backend_names = {
    "MANIFEST.json",
    "record.schema.json",
    "records.jsonl",
    *(f"{entity_class}.jsonl" for entity_class in REQUIRED_CLASSES),
}
actual_backend_names = {path.name for path in BACKEND.iterdir() if path.is_file()}
require(actual_backend_names == expected_backend_names, "Backend directory has missing or unexpected file outputs")''',
)

generated = replace_region(
    generated,
    'build = json.loads(BUILD_RECEIPT_PATH.read_text(encoding="utf-8"))',
    '\ninput_witnesses = {row["path"]: row for row in build.get("inputs", [])}',
    '''build = json.loads(BUILD_RECEIPT_PATH.read_text(encoding="utf-8"))
machine = json.loads(MACHINE_QA_PATH.read_text(encoding="utf-8"))
visual = json.loads(VISUAL_QA_PATH.read_text(encoding="utf-8"))
responsive = json.loads(RESPONSIVE_QA_PATH.read_text(encoding="utf-8"))
protected = json.loads(PROTECTED_QA_PATH.read_text(encoding="utf-8"))
unit_qas = {
    19: (UNIT_19_QA_PATH, json.loads(UNIT_19_QA_PATH.read_text(encoding="utf-8"))),
    20: (UNIT_20_QA_PATH, json.loads(UNIT_20_QA_PATH.read_text(encoding="utf-8"))),
    21: (UNIT_21_QA_PATH, json.loads(UNIT_21_QA_PATH.read_text(encoding="utf-8"))),
}
require(build.get("schema") == "ag-bridge-build-receipt-v2" and build.get("through_unit") == 21, "Reader build receipt mismatch")
require(machine.get("status") == "PASS" and machine.get("through_unit") == 21, "Machine reader QA mismatch")
require(visual.get("result") == "PASS" and visual.get("through_unit") == 21, "Visual reader QA mismatch")
require(responsive.get("status") == "PASS" and responsive.get("through_unit") == 21, "Responsive reader QA mismatch")
require(protected.get("status") == "PASS" and protected.get("through_unit") == 21, "Protected Unit 21 release-boundary receipt mismatch")
for unit, (path, payload) in unit_qas.items():
    require(payload.get("status") == "PASS" and payload.get("unit") == unit, f"Unit QA mismatch: {rel(path)}")
''',
)
generated = replace_region(
    generated,
    '    "reader_evidence": {',
    '    "ledger_evidence": {',
    '''    "reader_evidence": {
        "build_receipt_sha256": digest(BUILD_RECEIPT_PATH),
        "machine_qa_sha256": digest(MACHINE_QA_PATH),
        "visual_qa_sha256": digest(VISUAL_QA_PATH),
        "responsive_qa_sha256": digest(RESPONSIVE_QA_PATH),
        "protected_surfaces_sha256": digest(PROTECTED_QA_PATH),
        "unit_19_integration_qa_sha256": digest(UNIT_19_QA_PATH),
        "unit_20_translation_qa_sha256": digest(UNIT_20_QA_PATH),
        "unit_21_translation_qa_sha256": digest(UNIT_21_QA_PATH),
        "deterministic_replay_outputs": before_replay,
    },
''',
)
generated = generated.replace(
    '"reader_build_machine_visual_responsive_and_protected_qa": True',
    '"reader_build_machine_visual_responsive_and_protected_qa": True,\n'
    '        "per_unit_19_21_translation_integration_evidence": True,\n'
    '        "unit_18_schema_bytes_preserved": True,\n'
    '        "global_tuple_order_and_crlf_raw_byte_identity": True,\n'
    '        "deterministic_exporter_replay": True',
)

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE_QA), "exec"), namespace)
