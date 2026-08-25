#!/usr/bin/env python3
"""Deterministically extend the byte-frozen Units 1--21 backend through Unit 24.

This bounded specializer reuses the accepted Unit 21 implementation chain.  It
pins every Unit 21 baseline byte and derives only Units 22--24 authority,
source, terminology, correction, and QA facts from their fail-closed PASS
receipts.  Set AG_BRIDGE_SPECIALIZE_ONLY=1 to compile the generated exporter
without executing it or writing backend outputs.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "export_backend_units_01_21.py"
TEMPLATE_SHA256 = "17c442a732b8992be715f524b5cd2ddb5c678764a7cad5aa26c9a0ae5ece5ca9"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Unit 24 exporter specialization expected one occurrence, found {count}: {old!r}")
    return text.replace(old, new, 1)


if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
    raise SystemExit("Accepted Unit 21 exporter template is absent or has drifted")

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
# Final Unit 24 specialization: preserve the complete accepted Unit 21 backend
# as the byte baseline and admit only the three new units.
generated = replace_once(
    generated,
    'BASELINE = ROOT / "backend" / "units-01-18"',
    'BASELINE = ROOT / "backend" / "units-01-21"',
)
generated = generated.replace("backend/units-01-18", "backend/units-01-21")
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

# The accepted Unit 21 implementation correctly pins Units 1--21 as the
# immutable baseline, but its cumulative runtime boundary is also 21.  Change
# only those runtime gates and emitted cumulative facts; do not rewrite any
# baseline path, count, hash, or previous-edition identity.
generated = replace_once(
    generated,
    'build_receipt.get("through_unit") == 21',
    'build_receipt.get("through_unit") == 24',
)
generated = replace_once(
    generated,
    'payload.get("through_unit") == 21',
    'payload.get("through_unit") == 24',
)
stale_boundary_literal = '"through_unit": 21'
if generated.count(stale_boundary_literal) != 3:
    raise SystemExit(
        "Unit 24 exporter specialization expected exactly three emitted "
        "through_unit=21 boundary literals"
    )
generated = generated.replace(stale_boundary_literal, '"through_unit": 24')

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
    "\n\n# Filled only",
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
    "TERMINOLOGY_CONCEPTS: dict[str, tuple[str, str]] = {}",
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

old_authority_gate = '''for unit, spec in UNIT_SPEC.items():
    for key in ("manifest", "map", "rights", "closure"):
        path = spec[key]
        require(path.is_file(), f"Missing Unit {unit} authority input: {rel(path)}")
        require(digest(path) == spec["expected"][key], f"Unit {unit} {key} frozen hash mismatch")

build_receipt = json.loads(BUILD_RECEIPT_PATH.read_text(encoding="utf-8"))'''
new_authority_gate = '''UNIT_QA_PATHS = {22: UNIT_22_QA_PATH, 23: UNIT_23_QA_PATH, 24: UNIT_24_QA_PATH}
unit_qa_payloads: dict[int, dict[str, Any]] = {}

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
    qa_path = UNIT_QA_PATHS[unit]
    require(qa_path.is_file(), f"Missing Unit {unit} translation QA")
    qa_payload = json.loads(qa_path.read_text(encoding="utf-8"))
    require(qa_payload.get("status") == "PASS" and qa_payload.get("unit") == unit, f"Unit {unit} translation QA did not pass")
    require(qa_payload.get("provenance") == MODEL_PROVENANCE, f"Unit {unit} translation QA provenance mismatch")
    unit_qa_payloads[unit] = qa_payload
    spec["expected"] = {}
    for key in ("manifest", "map", "rights", "closure"):
        path = spec[key]
        require(path.is_file() and not path.is_symlink(), f"Missing/nonregular Unit {unit} authority input: {rel(path)}")
        expected_bytes, expected_sha = find_evidence(qa_payload, rel(path))
        require((path.stat().st_size, digest(path)) == (expected_bytes, expected_sha), f"Unit {unit} {key} evidence drift")
        spec["expected"][key] = expected_sha
    map_payload = json.loads(spec["map"].read_text(encoding="utf-8"))
    closure_payload = json.loads(spec["closure"].read_text(encoding="utf-8"))
    spec["exercise_count"] = map_payload["exercise_count"]
    spec["solutions"] = tuple(row["exercise_number"] for row in map_payload["entries"] if row.get("has_public_solution"))
    spec["media_count"] = closure_payload["reader_media_positions"]
    spec["binary_surfaces"] = closure_payload["unique_local_assets"]

build_receipt = json.loads(BUILD_RECEIPT_PATH.read_text(encoding="utf-8"))'''
generated = replace_once(generated, old_authority_gate, new_authority_gate)

old_source_gate = '''require(set(EXPECTED_SOURCE_SHA256) == {rel(path) for path in SOURCE_FILES}, "Final source-hash closure is incomplete or contains an unexpected path")
for path in SOURCE_FILES:
    path_key = rel(path)
    require(path.is_file(), f"Missing Unit 22--24 source input: {path_key}")
    actual = digest(path)
    require(actual == EXPECTED_SOURCE_SHA256[path_key], f"Final source hash changed: {path_key}")
    witness = receipt_inputs.get(path_key)
    require(witness is not None, f"Reader build receipt does not bind {path_key}")
    require(witness.get("bytes") == path.stat().st_size, f"Reader input byte count changed: {path_key}")
    require(witness.get("sha256") == actual, f"Reader input hash changed: {path_key}")'''
new_source_gate = '''require(len(SOURCE_FILES) == 13 and len({rel(path) for path in SOURCE_FILES}) == 13, "Units 22--24 source-path closure")
for path in SOURCE_FILES:
    path_key = rel(path)
    require(path.is_file() and not path.is_symlink(), f"Missing/nonregular Unit 22--24 source input: {path_key}")
    actual = digest(path)
    witness = receipt_inputs.get(path_key)
    require(witness is not None, f"Reader build receipt does not bind {path_key}")
    require((witness.get("bytes"), witness.get("sha256")) == (path.stat().st_size, actual), f"Reader input identity changed: {path_key}")
    match = re.search(r"unit-(\\d{2})|(?:lecture|worksheet|media-credits-unit)-(\\d{2})", path.name)
    if path.name != "frontmatter-units-01-24.md":
        unit_match = re.search(r"(\\d{2})", path.name)
        require(unit_match is not None, f"Cannot derive source unit: {path_key}")
        unit = int(unit_match.group(1))
        require((path.stat().st_size, actual) == find_evidence(unit_qa_payloads[unit], path_key), f"Per-unit QA/source identity mismatch: {path_key}")
new_source_ids = set()
for source_path in SOURCE_FILES[1:]:
    new_source_ids.update(re.findall(r"\\{#([A-Za-z][A-Za-z0-9_.:-]*)\\}", source_path.read_text(encoding="utf-8")))
for unit in range(22, 25):
    edition_slug = "2012" if unit == 24 else "2025-2026"
    required_roots = {
        f"br-ak-{edition_slug}-l{unit:02d}",
        f"br-ak-{edition_slug}-w{unit:02d}",
        f"br-ak-{edition_slug}-w{unit:02d}-solutions",
    }
    require(required_roots <= new_source_ids, f"Unit {unit} source-edition stable-root transition")
    wrong_slug = "2025-2026" if unit == 24 else "2012"
    require(not any(identifier.startswith(f"br-ak-{wrong_slug}-") and re.search(rf"-(?:l|w){unit:02d}(?:-|$)", identifier) for identifier in new_source_ids), f"Unit {unit} wrong source-edition stable-ID namespace")'''
generated = replace_once(generated, old_source_gate, new_source_gate)

# Derive new terminology records from the exact IDs admitted by each per-unit
# PASS receipt.  The term ledger ID itself is the durable concept namespace;
# this avoids inventing an unstable English slug before publication.
old_ledger_gate = '''terminology_rows = {
    row["term_id"]: row
    for row in read_csv(TERMINOLOGY_PATH)
    if row.get("term_id") in TERMINOLOGY_CONCEPTS
}
require(set(terminology_rows) == set(TERMINOLOGY_CONCEPTS), "Units 22--24 terminology ledger closure mismatch")

correction_rows = {
    row["correction_id"]: row
    for row in read_csv(CORRECTIONS_PATH)
    if row.get("correction_id") in CORRECTION_TARGETS
}
require(set(correction_rows) == set(CORRECTION_TARGETS), "Units 22--24 correction ledger closure mismatch")'''
new_ledger_gate = '''all_terminology_rows = {row["term_id"]: row for row in read_csv(TERMINOLOGY_PATH)}
bound_term_ids: list[str] = []
for unit in range(22, 25):
    bindings = unit_qa_payloads[unit].get("translation", {}).get("terminology_bindings", [])
    require(isinstance(bindings, list) and bindings, f"Unit {unit} terminology bindings absent")
    bound_term_ids.extend(bindings)
require(len(bound_term_ids) == len(set(bound_term_ids)), "Units 22--24 terminology bindings overlap")
require(set(bound_term_ids) <= set(all_terminology_rows), "Units 22--24 terminology ledger rows absent")
TERMINOLOGY_CONCEPTS.update({
    term_id: (f"concept.{term_id.casefold()}", all_terminology_rows[term_id]["preferred_target"])
    for term_id in sorted(bound_term_ids)
})
terminology_rows = {term_id: all_terminology_rows[term_id] for term_id in TERMINOLOGY_CONCEPTS}

all_correction_rows = {row["correction_id"]: row for row in read_csv(CORRECTIONS_PATH)}
bound_correction_ids: list[str] = []
for unit in range(22, 25):
    translation = unit_qa_payloads[unit].get("translation", {})
    for key, value in translation.items():
        if "binding" in key.casefold() and isinstance(value, list):
            bound_correction_ids.extend(item for item in value if isinstance(item, str) and item.startswith("AGC-CORR-"))
require(len(bound_correction_ids) == len(set(bound_correction_ids)), "Units 22--24 correction bindings overlap")
require(set(bound_correction_ids) <= set(all_correction_rows), "Units 22--24 correction ledger rows absent")
source_id_pool = set()
for source_path in SOURCE_FILES[1:]:
    source_id_pool.update(re.findall(r"\\{#([A-Za-z][A-Za-z0-9_.:-]*)\\}", source_path.read_text(encoding="utf-8")))

def resolve_correction_target(correction_id: str) -> str:
    row = all_correction_rows[correction_id]
    for unit in range(22, 25):
        explicit = unit_qa_payloads[unit].get("translation", {}).get("correction_targets", {})
        if correction_id in explicit:
            require(explicit[correction_id] in source_id_pool, f"Explicit correction target absent: {correction_id}")
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
            candidates = sorted(identifier for identifier in source_id_pool if re.search(rf"-{family}{unit:02d}-{kind}-{number:02d}$", identifier))
            if len(candidates) == 1:
                return candidates[0]
    unit_match = re.search(r"(?:lecture|worksheet)(?:_solution)?_(\\d+)", scope)
    if unit_match:
        unit = int(unit_match.group(1))
        family = "l" if scope.startswith("lecture") else "w"
        candidates = sorted(identifier for identifier in source_id_pool if re.search(rf"-{family}{unit:02d}$", identifier))
        if len(candidates) == 1:
            return candidates[0]
    raise RuntimeError(f"Cannot resolve a unique source target for {correction_id}; add translation.correction_targets to its per-unit QA receipt")

CORRECTION_TARGETS.update({correction_id: resolve_correction_target(correction_id) for correction_id in sorted(bound_correction_ids)})
correction_rows = {correction_id: all_correction_rows[correction_id] for correction_id in CORRECTION_TARGETS}'''
generated = replace_once(generated, old_ledger_gate, new_ledger_gate)

old_exercise_gate = '''for unit, spec in UNIT_SPEC.items():
    exercise_ids = {
        row["stable_id"] for row in all_new_units
        if row["payload"].get("unit_type") == "exercise" and f"-w{unit:02d}-ex-" in row["stable_id"]
    }
    solution_ids = {
        row["stable_id"] for row in all_new_units
        if row["payload"].get("unit_type") == "solution" and f"-w{unit:02d}-sol-" in row["stable_id"]
    }
    expected_exercises = {f"br-ak-2025-2026-w{unit:02d}-ex-{number:02d}" for number in range(1, spec["exercise_count"] + 1)}
    expected_solutions = {f"br-ak-2025-2026-w{unit:02d}-sol-{number:02d}" for number in spec["solutions"]}
    require(exercise_ids == expected_exercises, f"Unit {unit} translated exercise stable-ID closure mismatch")
    require(solution_ids == expected_solutions, f"Unit {unit} translated solution stable-ID closure mismatch")'''
new_exercise_gate = '''exercise_id_by_unit_number: dict[int, dict[int, str]] = {}
solution_id_by_unit_number: dict[int, dict[int, str]] = {}
for unit, spec in UNIT_SPEC.items():
    exercise_rows = {
        int(match.group(1)): row["stable_id"]
        for row in all_new_units
        if row["payload"].get("unit_type") == "exercise"
        and (match := re.search(rf"-w{unit:02d}-ex-(\\d+)$", row["stable_id"]))
    }
    solution_rows = {
        int(match.group(1)): row["stable_id"]
        for row in all_new_units
        if row["payload"].get("unit_type") == "solution"
        and (match := re.search(rf"-w{unit:02d}-sol-(\\d+)$", row["stable_id"]))
    }
    require(set(exercise_rows) == set(range(1, spec["exercise_count"] + 1)), f"Unit {unit} translated exercise stable-ID closure mismatch")
    require(set(solution_rows) == set(spec["solutions"]), f"Unit {unit} translated solution stable-ID closure mismatch")
    exercise_id_by_unit_number[unit] = exercise_rows
    solution_id_by_unit_number[unit] = solution_rows'''
generated = replace_once(generated, old_exercise_gate, new_exercise_gate)
generated = replace_once(
    generated,
    '''        add_relation("solves", f"br-ak-2025-2026-w{unit:02d}-sol-{number:02d}", f"br-ak-2025-2026-w{unit:02d}-ex-{number:02d}", source_locator=rel(UNIT_SPEC[unit]["map"]))
        add_relation("solves", f"solution.br-ak-2025-2026-w{unit:02d}-sol-{number:02d}", f"exercise.br-ak-2025-2026-w{unit:02d}-ex-{number:02d}", source_locator=rel(UNIT_SPEC[unit]["map"]), payload={"typed_family_projection": True})''',
    '''        solution_id = solution_id_by_unit_number[unit][number]
        exercise_id = exercise_id_by_unit_number[unit][number]
        add_relation("solves", solution_id, exercise_id, source_locator=rel(UNIT_SPEC[unit]["map"]))
        add_relation("solves", f"solution.{solution_id}", f"exercise.{exercise_id}", source_locator=rel(UNIT_SPEC[unit]["map"]), payload={"typed_family_projection": True})''',
)

# Per-unit receipts are source evidence in addition to the four cumulative QA
# events, and the Unit 21 schema remains byte-identical.
generated = generated.replace("Unit 21 record schema bytes", "Unit 21 record schema bytes")
"""

marker = 'namespace = {\n    "__file__": str(Path(__file__).resolve()),\n    "__name__": "__main__",\n    "TEMPLATE_EXPORTER": TEMPLATE_EXPORTER,\n}'
specializer = replace_once(specializer, marker, injection + "\n\n" + marker)
specializer = replace_once(
    specializer,
    'exec(compile(generated, str(TEMPLATE_EXPORTER), "exec"), namespace)',
    '''if __import__("os").environ.get("AG_BRIDGE_SPECIALIZE_ONLY") == "1":
    compile(generated, str(TEMPLATE_EXPORTER), "exec")
    print("Unit 24 exporter specialization: COMPILE PASS")
else:
    exec(compile(generated, str(TEMPLATE_EXPORTER), "exec"), namespace)''',
)

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(specializer, str(TEMPLATE), "exec"), namespace)
