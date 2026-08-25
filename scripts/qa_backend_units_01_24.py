#!/usr/bin/env python3
"""Independently validate the cumulative native backend through Unit 24.

The accepted Unit 21 implementation remains the byte-pinned contract.  This
specializer checks its 16,114 serialized records byte-for-byte and validates
only the additive Units 22--24 records, shards, relations, evidence, and an
in-place deterministic exporter replay.  Set AG_BRIDGE_SPECIALIZE_ONLY=1 to
compile the generated validator without executing it.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "qa_backend_units_01_21.py"
TEMPLATE_SHA256 = "f8efc2b3953819852a1577e707b6870435d8a35371ceb35ff4176b154bccde53"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Unit 24 backend-QA specialization expected one occurrence, found {count}: {old!r}")
    return text.replace(old, new, 1)


if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
    raise SystemExit("Accepted Unit 21 backend-QA template is absent or has drifted")

specializer = TEMPLATE.read_text(encoding="utf-8")
for old, new in (
    ("units-01-21", "units-01-24"),
    ("UNITS_01_21", "UNITS_01_24"),
    ("UNIT_21", "UNIT_24"),
    ("units0121", "units0124"),
    ("units_01_21", "units_01_24"),
    ("unit-21", "unit-24"),
    ("unit21", "unit24"),
    ("Unit 21", "Unit 24"),
    ("Units 1--21", "Units 1--24"),
    ("Units 19--21", "Units 22--24"),
    ("Unit 19--21", "Unit 22--24"),
    ("units_19_21", "units_22_24"),
    ("unit_19_21", "unit_22_24"),
):
    specializer = specializer.replace(old, new)

injection = r"""
generated = replace_once(
    generated,
    'BASELINE = ROOT / "backend" / "units-01-18"',
    'BASELINE = ROOT / "backend" / "units-01-21"',
)
generated = generated.replace("Units 1--18", "Units 1--21")
generated = generated.replace("units_01_18", "units_01_21")
generated = generated.replace("Unit 18", "Unit 21")
generated = replace_once(
    generated,
    'BASELINE_MANIFEST_SHA256 = "fe9bfb98528d03d5d82f6d0ff66e3b15d2e28defd64190b3ec293f8dfd0ab96a"',
    'BASELINE_MANIFEST_SHA256 = "d2afc26b3c81c8b57e585c2a7bc4ac683a740403a527e9bfd203a88e45a3363d"',
)
generated = replace_once(
    generated,
    'BASELINE_RECORDS_SHA256 = "c952ca6c0a6b36f2138c0971161b11582bbb1479795bf36c9d1de23e4343e517"',
    'BASELINE_RECORDS_SHA256 = "ac9e40ad50e6dfdef977036999cebc5bc443d1064283c86eb30999b461a8872f"',
)
generated = replace_once(generated, "BASELINE_RECORD_COUNT = 13626", "BASELINE_RECORD_COUNT = 16114")
generated = replace_once(
    generated,
    'PREVIOUS_EDITION = "edition.algebraic-geometry-bridge-id.units-01-18.2026-08-25"',
    'PREVIOUS_EDITION = "edition.algebraic-geometry-bridge-id.units-01-21.2026-08-25"',
)

# Preserve Units 1--21 as the byte-frozen comparison baseline while advancing
# every cumulative manifest, edition, and QA boundary checked or emitted by
# this validator to Unit 24.
generated = replace_once(
    generated,
    'manifest.get("through_unit") == 21',
    'manifest.get("through_unit") == 24',
)
generated = replace_once(
    generated,
    'edition["payload"].get("through_unit") == 21',
    'edition["payload"].get("through_unit") == 24',
)
generated = replace_once(
    generated,
    '"through_unit": 21',
    '"through_unit": 24',
)

generated = generated.replace("UNIT_19_QA_PATH", "UNIT_22_QA_PATH")
generated = generated.replace("UNIT_20_QA_PATH", "UNIT_23_QA_PATH")
generated = replace_region(
    generated,
    'MACHINE_QA_PATH = ROOT / "qa" / "UNITS_01_24_MACHINE_QA.json"',
    'CORRECTIONS_PATH = ROOT / "00_control" / "CORRECTIONS.csv"',
    '''MACHINE_QA_PATH = ROOT / "qa" / "UNITS_01_24_MACHINE_QA.json"
VISUAL_QA_PATH = ROOT / "qa" / "UNITS_01_24_VISUAL_QA.json"
RESPONSIVE_QA_PATH = ROOT / "qa" / "UNITS_01_24_RESPONSIVE_QA.json"
PROTECTED_QA_PATH = ROOT / "qa" / "UNIT_24_PROTECTED_SURFACES.json"
UNIT_22_QA_PATH = ROOT / "qa" / "UNIT_22_TRANSLATION_QA.json"
UNIT_23_QA_PATH = ROOT / "qa" / "UNIT_23_TRANSLATION_QA.json"
UNIT_24_QA_PATH = ROOT / "qa" / "UNIT_24_TRANSLATION_QA.json"
''',
)
generated = replace_region(
    generated,
    "SOURCE_FILES = [",
    "\n\nEXPECTED_SOURCE_SHA256 = {",
    '''SOURCE_FILES = [
    ROOT / "source" / "id-ID" / "frontmatter-units-01-24.md",
    *[
        ROOT / "source" / "id-ID" / name
        for unit in range(22, 25)
        for name in (
            f"lecture-{unit:02d}.md",
            f"worksheet-{unit:02d}.md",
            f"worksheet-{unit:02d}-solutions.md",
            f"media-credits-unit-{unit:02d}.md",
        )
    ],
]''',
)
generated = replace_region(
    generated,
    "EXPECTED_SOURCE_SHA256 = {",
    "\n\nTERMINOLOGY_CONCEPTS = {",
    "EXPECTED_SOURCE_SHA256: dict[str, str] = {}",
)
generated = replace_region(
    generated,
    "TERMINOLOGY_CONCEPTS = {",
    "\n\nCORRECTION_TARGETS = {",
    "TERMINOLOGY_CONCEPTS: dict[str, str] = {}",
)
generated = replace_region(
    generated,
    "CORRECTION_TARGETS = {",
    "\n\nUNIT_SPEC: dict[int, dict[str, Any]] = {",
    "CORRECTION_TARGETS: dict[str, str] = {}",
)
generated = replace_region(
    generated,
    "UNIT_SPEC: dict[int, dict[str, Any]] = {",
    "\n\nREQUIRED_CLASSES = {",
    '''UNIT_SPEC: dict[int, dict[str, Any]] = {
    unit: {
        "manifest": ROOT / "authority" / "wikiversity" / f"unit-{unit}" / "UNIT_AUTHORITY_MANIFEST.json",
        "map": ROOT / "authority" / "wikiversity" / f"unit-{unit}" / "ORDERED_EXERCISE_MAP.json",
        "rights": ROOT / "authority" / f"RIGHTS-unit-{unit}.csv",
        "closure": ROOT / "authority" / f"ASSET_CLOSURE-unit-{unit}.json",
    }
    for unit in range(22, 25)
}''',
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
UNIT_QA_PATHS = {22: UNIT_22_QA_PATH, 23: UNIT_23_QA_PATH, 24: UNIT_24_QA_PATH}
unit_qas: dict[int, tuple[Path, dict[str, Any]]] = {
    unit: (path, json.loads(path.read_text(encoding="utf-8")))
    for unit, path in UNIT_QA_PATHS.items()
}
require(build.get("schema") == "ag-bridge-build-receipt-v2" and build.get("through_unit") == 24, "Reader build receipt mismatch")
require(machine.get("status") == "PASS" and machine.get("through_unit") == 24, "Machine reader QA mismatch")
require(visual.get("result") == "PASS" and visual.get("through_unit") == 24, "Visual reader QA mismatch")
require(responsive.get("status") == "PASS" and responsive.get("through_unit") == 24, "Responsive reader QA mismatch")
require(protected.get("status") == "PASS" and protected.get("through_unit") == 24, "Protected Unit 24 release-boundary receipt mismatch")
for unit, (path, payload) in unit_qas.items():
    require(payload.get("status") == "PASS" and payload.get("unit") == unit, f"Unit QA mismatch: {rel(path)}")
    require(payload.get("provenance") == MODEL_PROVENANCE, f"Unit QA provenance mismatch: {rel(path)}")

def find_evidence(payload: dict[str, Any], relative: str) -> tuple[int, str]:
    stack: list[Any] = [payload]
    matches: list[tuple[int, str]] = []
    while stack:
        item = stack.pop()
        if isinstance(item, dict):
            if item.get("path") == relative and isinstance(item.get("bytes"), int) and isinstance(item.get("sha256"), str):
                matches.append((item["bytes"], item["sha256"]))
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)
    require(matches and len(set(matches)) == 1, f"Missing/ambiguous per-unit evidence: {relative}")
    return matches[0]

for unit, spec in UNIT_SPEC.items():
    payload = unit_qas[unit][1]
    spec["expected"] = {}
    for key in ("manifest", "map", "rights", "closure"):
        path = spec[key]
        expected_bytes, expected_sha = find_evidence(payload, rel(path))
        require(path.is_file() and not path.is_symlink(), f"Missing/nonregular Unit {unit} authority file: {rel(path)}")
        require((path.stat().st_size, digest(path)) == (expected_bytes, expected_sha), f"Unit {unit} authority evidence drift: {key}")
        spec["expected"][key] = expected_sha
    map_payload = json.loads(spec["map"].read_text(encoding="utf-8"))
    closure_payload = json.loads(spec["closure"].read_text(encoding="utf-8"))
    spec["exercise_count"] = map_payload["exercise_count"]
    spec["solutions"] = tuple(row["exercise_number"] for row in map_payload["entries"] if row.get("has_public_solution"))
    spec["media_count"] = closure_payload["reader_media_positions"]
    spec["binary_surfaces"] = closure_payload["unique_local_assets"]
''',
)

old_source_gate = '''require(set(EXPECTED_SOURCE_SHA256) == {rel(path) for path in SOURCE_FILES}, "Final source-hash closure is incomplete")
for path in SOURCE_FILES:
    key = rel(path)
    require(path.is_file(), f"Missing source file: {key}")
    actual = digest(path)
    require(actual == EXPECTED_SOURCE_SHA256[key], f"Frozen source hash changed: {key}")
    witness = input_witnesses.get(key)
    require(witness is not None, f"Reader receipt does not bind source: {key}")
    require(witness.get("bytes") == path.stat().st_size and witness.get("sha256") == actual, f"Reader source witness mismatch: {key}")'''
new_source_gate = '''require(len(SOURCE_FILES) == 13 and len({rel(path) for path in SOURCE_FILES}) == 13, "Units 22--24 source closure")
for path in SOURCE_FILES:
    key = rel(path)
    require(path.is_file() and not path.is_symlink(), f"Missing/nonregular source file: {key}")
    actual = digest(path)
    witness = input_witnesses.get(key)
    require(witness is not None, f"Reader receipt does not bind source: {key}")
    require((witness.get("bytes"), witness.get("sha256")) == (path.stat().st_size, actual), f"Reader source witness mismatch: {key}")
    if path.name != "frontmatter-units-01-24.md":
        unit_match = re.search(r"(\\d{2})", path.name)
        require(unit_match is not None, f"Cannot derive source unit: {key}")
        require((path.stat().st_size, actual) == find_evidence(unit_qas[int(unit_match.group(1))][1], key), f"Per-unit QA/source identity mismatch: {key}")'''
generated = replace_once(generated, old_source_gate, new_source_gate)
generated = replace_once(
    generated,
    'require(source_heading_ids <= id_set, "Backend dropped a Unit 22--24 source heading")',
    '''require(source_heading_ids <= id_set, "Backend dropped a Unit 22--24 source heading")
for unit in range(22, 25):
    edition_slug = "2012" if unit == 24 else "2025-2026"
    required_roots = {
        f"br-ak-{edition_slug}-l{unit:02d}",
        f"br-ak-{edition_slug}-w{unit:02d}",
        f"br-ak-{edition_slug}-w{unit:02d}-solutions",
    }
    require(required_roots <= source_heading_ids, f"Unit {unit} source-edition stable-root transition")
    wrong_slug = "2025-2026" if unit == 24 else "2012"
    require(not any(identifier.startswith(f"br-ak-{wrong_slug}-") and re.search(rf"-(?:l|w){unit:02d}(?:-|$)", identifier) for identifier in source_heading_ids), f"Unit {unit} wrong source-edition stable-ID namespace")''',
)

old_term_open = '''with TERMINOLOGY_PATH.open("r", encoding="utf-8", newline="") as stream:
    terminology_rows = {
        row["term_id"]: row
        for row in csv.DictReader(stream)
        if row.get("term_id") in TERMINOLOGY_CONCEPTS
    }
require(set(terminology_rows) == set(TERMINOLOGY_CONCEPTS), "Units 22--24 terminology ledger closure mismatch")'''
new_term_open = '''with TERMINOLOGY_PATH.open("r", encoding="utf-8", newline="") as stream:
    all_terminology_rows = {row["term_id"]: row for row in csv.DictReader(stream)}
bound_term_ids: list[str] = []
for unit in range(22, 25):
    bindings = unit_qas[unit][1].get("translation", {}).get("terminology_bindings", [])
    require(isinstance(bindings, list) and bindings, f"Unit {unit} terminology bindings absent")
    bound_term_ids.extend(bindings)
require(len(bound_term_ids) == len(set(bound_term_ids)), "Units 22--24 terminology bindings overlap")
require(set(bound_term_ids) <= set(all_terminology_rows), "Units 22--24 terminology ledger rows absent")
TERMINOLOGY_CONCEPTS.update({term_id: f"concept.{term_id.casefold()}" for term_id in sorted(bound_term_ids)})
terminology_rows = {term_id: all_terminology_rows[term_id] for term_id in TERMINOLOGY_CONCEPTS}'''
generated = replace_once(generated, old_term_open, new_term_open)

old_correction_open = '''with CORRECTIONS_PATH.open("r", encoding="utf-8", newline="") as stream:
    correction_rows = {
        row["correction_id"]: row
        for row in csv.DictReader(stream)
        if row.get("correction_id") in CORRECTION_TARGETS
    }
require(set(correction_rows) == set(CORRECTION_TARGETS), "Units 22--24 correction ledger closure mismatch")'''
new_correction_open = '''with CORRECTIONS_PATH.open("r", encoding="utf-8", newline="") as stream:
    all_correction_rows = {row["correction_id"]: row for row in csv.DictReader(stream)}
bound_correction_ids: list[str] = []
for unit in range(22, 25):
    translation = unit_qas[unit][1].get("translation", {})
    for key, value in translation.items():
        if "binding" in key.casefold() and isinstance(value, list):
            bound_correction_ids.extend(item for item in value if isinstance(item, str) and item.startswith("AGC-CORR-"))
require(len(bound_correction_ids) == len(set(bound_correction_ids)), "Units 22--24 correction bindings overlap")
require(set(bound_correction_ids) <= set(all_correction_rows), "Units 22--24 correction ledger rows absent")

def resolve_correction_target(correction_id: str) -> str:
    row = all_correction_rows[correction_id]
    for unit in range(22, 25):
        explicit = unit_qas[unit][1].get("translation", {}).get("correction_targets", {})
        if correction_id in explicit:
            require(explicit[correction_id] in source_heading_ids, f"Explicit correction target absent: {correction_id}")
            return explicit[correction_id]
    scope = row.get("scope", "")
    patterns = (
        (r"worksheet(?:_solution)?_(\\d+)_exercise_(?:and_solution_)?(\\d+)", "w", "ex"),
        (r"worksheet_solution_(\\d+)_(\\d+)", "w", "sol"),
        (r"worksheet_(\\d+)_exercise_(\\d+)", "w", "ex"),
    )
    for pattern, family, kind in patterns:
        match = re.search(pattern, scope)
        if match:
            unit, number = map(int, match.groups())
            candidates = sorted(identifier for identifier in source_heading_ids if re.search(rf"-{family}{unit:02d}-{kind}-{number:02d}$", identifier))
            if len(candidates) == 1:
                return candidates[0]
    unit_match = re.search(r"(?:lecture|worksheet)(?:_solution)?_(\\d+)", scope)
    if unit_match:
        unit = int(unit_match.group(1))
        family = "l" if scope.startswith("lecture") else "w"
        candidates = sorted(identifier for identifier in source_heading_ids if re.search(rf"-{family}{unit:02d}$", identifier))
        if len(candidates) == 1:
            return candidates[0]
    raise SystemExit(f"Cannot resolve a unique source target for {correction_id}; add translation.correction_targets to its per-unit QA receipt")

CORRECTION_TARGETS.update({correction_id: resolve_correction_target(correction_id) for correction_id in sorted(bound_correction_ids)})
correction_rows = {correction_id: all_correction_rows[correction_id] for correction_id in CORRECTION_TARGETS}'''
generated = replace_once(generated, old_correction_open, new_correction_open)

generated = replace_once(
    generated,
    '''    expected_exercise_ids.update(f"exercise.br-ak-2025-2026-w{unit:02d}-ex-{number:02d}" for number in range(1, spec["exercise_count"] + 1))
    expected_solution_ids.update(f"solution.br-ak-2025-2026-w{unit:02d}-sol-{number:02d}" for number in spec["solutions"])''',
    '''    unit_exercise_ids = {
        f"exercise.{identifier}" for identifier in source_heading_ids
        if re.search(rf"-w{unit:02d}-ex-\\d+$", identifier)
    }
    unit_solution_ids = {
        f"solution.{identifier}" for identifier in source_heading_ids
        if re.search(rf"-w{unit:02d}-sol-\\d+$", identifier)
    }
    require(len(unit_exercise_ids) == spec["exercise_count"], f"Unit {unit} source exercise-ID count")
    require(len(unit_solution_ids) == len(spec["solutions"]), f"Unit {unit} source solution-ID count")
    expected_exercise_ids.update(unit_exercise_ids)
    expected_solution_ids.update(unit_solution_ids)''',
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
        "unit_22_translation_qa_sha256": digest(UNIT_22_QA_PATH),
        "unit_23_translation_qa_sha256": digest(UNIT_23_QA_PATH),
        "unit_24_translation_qa_sha256": digest(UNIT_24_QA_PATH),
        "deterministic_replay_outputs": before_replay,
    },
''',
)
"""

marker = 'namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}'
specializer = replace_once(specializer, marker, injection + "\n\n" + marker)
specializer = replace_once(
    specializer,
    'exec(compile(generated, str(TEMPLATE_QA), "exec"), namespace)',
    '''if __import__("os").environ.get("AG_BRIDGE_SPECIALIZE_ONLY") == "1":
    compile(generated, str(TEMPLATE_QA), "exec")
    print("Unit 24 backend-QA specialization: COMPILE PASS")
else:
    exec(compile(generated, str(TEMPLATE_QA), "exec"), namespace)''',
)

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(specializer, str(TEMPLATE), "exec"), namespace)
