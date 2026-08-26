#!/usr/bin/env python3
"""Verify protected mathematical surfaces for cumulative Units 25--27.

The accepted Unit 24 protected-surface receipt is the byte-pinned baseline.
Only the new Units 25--27 protected tokens and correction bindings are checked.
Set AG_BRIDGE_SPECIALIZE_ONLY=1 for an in-memory compile check.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "qa_protected_surfaces_units_22_24.py"
TEMPLATE_SHA256 = "a6c4fe4c352eaac0009f59fce11a9626561fe28038c544c8d17fb30e790c21c0"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Unit 27 protected-surface specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
    raise SystemExit("Accepted Unit 24 protected-surface template is absent or has drifted")

generated = TEMPLATE.read_text(encoding="utf-8")
for old, new in (
    ("cumulative Units 22--24", "cumulative Units 25--27"),
    ("algebraic-geometry-bridge-id-units-01-24.pdf", "algebraic-geometry-bridge-id-units-01-27.pdf"),
    ('OUT = ROOT / "qa" / "UNIT_24_PROTECTED_SURFACES.json"', 'OUT = ROOT / "qa" / "UNIT_27_PROTECTED_SURFACES.json"'),
    ('BASELINE = ROOT / "qa" / "UNIT_21_PROTECTED_SURFACES.json"', 'BASELINE = ROOT / "qa" / "UNIT_24_PROTECTED_SURFACES.json"'),
    ('MACHINE = ROOT / "qa" / "UNITS_01_24_MACHINE_QA.json"', 'MACHINE = ROOT / "qa" / "UNITS_01_27_MACHINE_QA.json"'),
    ('BASELINE_FACT = (1977, "35eee319508f364c73f32627ffb69b376bd15bb978e4d1694765dc06538eb6ba")', 'BASELINE_FACT = (4127, "afcb17362e90f8492b78eeaf5022f0bca1ee193c2ee1cff6ed0e33f235622580")'),
    ("range(22, 25)", "range(25, 28)"),
    ("units_22_24", "units_25_27"),
    ("Units 22--24", "Units 25--27"),
    ("Units 22-24", "Units 25-27"),
):
    generated = generated.replace(old, new)

generated = generated.replace(
    'baseline_payload.get("status") == "PASS" and baseline_payload.get("through_unit") == 21',
    'baseline_payload.get("status") == "PASS" and baseline_payload.get("through_unit") == 24',
)
generated = replace_once(
    generated,
    '''def protected_tokens(unit: int, expected_count: int) -> tuple[Path, list[str]]:
    script = ROOT / "scripts" / f"qa_unit{unit}_translation.py"
    require(script.is_file() and not script.is_symlink(), f"missing Unit {unit} translation QA implementation")
    matching = [tokens for tokens in literal_string_lists(script) if len(tokens) == expected_count]
    require(len(matching) == 1, f"Unit {unit} protected-token literal is absent or ambiguous")
    require(len(matching[0]) == len(set(matching[0])), f"Unit {unit} protected-token list contains duplicates")
    return script, matching[0]''',
    '''def protected_tokens(unit: int, expected_count: int) -> tuple[Path, list[str]]:
    script = ROOT / "scripts" / f"qa_unit{unit}_translation.py"
    require(script.is_file() and not script.is_symlink(), f"missing Unit {unit} translation QA implementation")
    names_by_unit = {
        25: ("lecture_protected", "worksheet_protected", "solution_protected"),
        26: ("lecture_math", "worksheet_math", "solution_math"),
        27: ("protected", "worksheet_surfaces"),
    }
    wanted = names_by_unit[unit]
    tree = ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
    found: dict[str, list[str]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or not isinstance(node.value, (ast.List, ast.Tuple)):
            continue
        names = [target.id for target in node.targets if isinstance(target, ast.Name)]
        for name in names:
            if name not in wanted:
                continue
            values = [item.value for item in node.value.elts if isinstance(item, ast.Constant) and isinstance(item.value, str)]
            require(len(values) == len(node.value.elts), f"Unit {unit} protected-token list is not literal: {name}")
            found[name] = values
    require(set(found) == set(wanted), f"Unit {unit} protected-token literals are incomplete")
    tokens = [token for name in wanted for token in found[name]]
    require(len(tokens) == expected_count, f"Unit {unit} protected-token count disagrees with translation QA")
    require(len(tokens) == len(set(tokens)), f"Unit {unit} protected-token list contains duplicates")
    return script, tokens''',
)
generated = replace_once(
    generated,
    '    rows = payload.get("translation", {}).get("source_and_control_facts", [])',
    '''    rows = payload.get("translation", {}).get("source_and_control_facts", [])
    if not rows:
        rows = list(payload.get("bound_facts", {}).values())''',
)
generated = replace_once(
    generated,
    '''        expected_count = payload.get("translation", {}).get("protected_math_checks")
        require(isinstance(expected_count, int) and expected_count > 0, f"Unit {unit} protected-math count")''',
    '''        translation = payload.get("translation", {})
        split_counts = [
            value
            for key, value in translation.items()
            if key.startswith("protected_") and key.endswith("_checks") and isinstance(value, int)
        ]
        expected_count = sum(split_counts) if split_counts else ({27: 13}.get(unit))
        require(isinstance(expected_count, int) and expected_count > 0, f"Unit {unit} protected-math count")''',
)
generated = generated.replace("Unit 21 protected baseline", "Unit 24 protected baseline")
generated = generated.replace('machine.get("status") == "PASS" and machine.get("through_unit") == 24', 'machine.get("status") == "PASS" and machine.get("through_unit") == 27')
generated = generated.replace("cumulative Unit 24 machine QA", "cumulative Unit 27 machine QA")
generated = generated.replace('"through_unit": 24', '"through_unit": 27')
generated = generated.replace('"verified_date": "2026-08-25"', '"verified_date": "2026-08-26"')
generated = generated.replace('"unit_21_baseline": baseline', '"unit_24_baseline": baseline')
generated = replace_once(
    generated,
    'edition_slug = "2012" if unit == 24 else "2025-2026"',
    'edition_slug = "2012"',
)
generated = replace_once(
    generated,
    'wrong_slug = "2025-2026" if unit == 24 else "2012"',
    'wrong_slug = "2025-2026"',
)
generated = replace_once(
    generated,
    '''    if all_corrections:
        numbers = sorted(int(value.rsplit("-", 1)[1]) for value in all_corrections)
        require(numbers == list(range(71, numbers[-1] + 1)), "Units 25--27 correction binding interval is not contiguous from AGC-CORR-0071")''',
    '''    if all_corrections:
        baseline_corrections = baseline_payload.get("correction_and_bridge_disclosures", [])
        require(baseline_corrections, "Unit 24 correction baseline is empty")
        baseline_numbers = sorted(int(value.rsplit("-", 1)[1]) for value in baseline_corrections)
        require(baseline_numbers == list(range(baseline_numbers[0], baseline_numbers[-1] + 1)), "Unit 24 correction baseline is not contiguous")
        numbers = sorted(int(value.rsplit("-", 1)[1]) for value in all_corrections)
        require(numbers == list(range(baseline_numbers[-1] + 1, numbers[-1] + 1)), "Units 25--27 correction bindings are not the contiguous suffix after Unit 24")''',
)

if os.environ.get("AG_BRIDGE_SPECIALIZE_ONLY") == "1":
    compile(generated, str(TEMPLATE), "exec")
    print("Unit 27 protected-surface specialization: COMPILE PASS")
else:
    namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
    exec(compile(generated, str(TEMPLATE), "exec"), namespace)
