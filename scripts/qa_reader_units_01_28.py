#!/usr/bin/env python3
"""Fail-closed cumulative reader QA through the Unit 28 checkpoint."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "qa_reader_units_01_24.py"
TEMPLATE_SHA256 = "4df75631de98470dcb089bd97290d7b809a05b41f3469acd592cb5e592c6c4b0"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Unit 28 reader-QA specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
    raise SystemExit("Accepted Unit 24 reader-QA template is absent or has drifted")

generated = TEMPLATE.read_text(encoding="utf-8")
generated = replace_once(
    generated,
    '''BASELINE_FACTS = {
    "qa/UNITS_01_21_MACHINE_QA.json": (7308, "adace78a568ecb84c97077965d82a4ca13a849b7455db0b8872546486dcabdd0"),
    "qa/UNIT_21_PROTECTED_SURFACES.json": (1977, "35eee319508f364c73f32627ffb69b376bd15bb978e4d1694765dc06538eb6ba"),
}''',
    '''BASELINE_FACTS = {
    "qa/UNITS_01_27_MACHINE_QA.json": (4254, "33fdf951354c620bbfeedc483338aa611ef577f0adcb8e509bca7361dc9bb074"),
    "qa/UNIT_27_PROTECTED_SURFACES.json": (4122, "ca04c18753768b6741073342d47e6ba9fb6535b20382a29b53af20cb4be840ec"),
}''',
)

for old, new in (
    ("algebraic-geometry-bridge-id-units-01-24.pdf", "algebraic-geometry-bridge-id-units-01-28.pdf"),
    ("frontmatter-units-01-24.md", "frontmatter-units-01-28.md"),
    ("Kurva Aljabar - Unit 1-24", "Kurva Aljabar - Unit 1-28"),
    ("authority_units_22_24", "authority_unit_28"),
    ("Units 22-24", "Unit 28"),
    ("Units 22--24", "Unit 28"),
):
    generated = generated.replace(old, new)

generated = replace_once(
    generated,
    'OUT = ROOT / "qa" / "UNITS_01_24_MACHINE_QA.json"',
    'OUT = ROOT / "qa" / "UNITS_01_28_MACHINE_QA.json"',
)
generated = generated.replace(
    'baseline = json.loads((ROOT / "qa" / "UNITS_01_21_MACHINE_QA.json").read_text(encoding="utf-8"))',
    'baseline = json.loads((ROOT / "qa" / "UNITS_01_27_MACHINE_QA.json").read_text(encoding="utf-8"))',
)
generated = generated.replace(
    'protected_baseline = json.loads((ROOT / "qa" / "UNIT_21_PROTECTED_SURFACES.json").read_text(encoding="utf-8"))',
    'protected_baseline = json.loads((ROOT / "qa" / "UNIT_27_PROTECTED_SURFACES.json").read_text(encoding="utf-8"))',
)
generated = generated.replace(
    'baseline.get("status") == "PASS" and baseline.get("through_unit") == 21',
    'baseline.get("status") == "PASS" and baseline.get("through_unit") == 27',
)
generated = generated.replace(
    'protected_baseline.get("status") == "PASS" and protected_baseline.get("through_unit") == 21',
    'protected_baseline.get("status") == "PASS" and protected_baseline.get("through_unit") == 27',
)
generated = generated.replace("Unit 21 machine baseline", "Unit 27 machine baseline")
generated = generated.replace("Unit 21 protected baseline", "Unit 27 protected baseline")
generated = generated.replace("exact Units 1-21 machine/protected baselines bound", "exact Units 1-27 machine/protected baselines bound")

generated = replace_once(
    generated,
    '''        translation = qa_payload["translation"]
        require(translation.get("exercises") == exercises, f"Unit {unit} translated exercise count")
        require(translation.get("public_solutions") == len(solutions), f"Unit {unit} translated solution count")
        require(translation.get("reader_images") == media, f"Unit {unit} translated media count")''',
    '''        translation = qa_payload["translation"]
        translated_exercises = translation.get("exercises", translation.get("worksheet_exercises"))
        translated_solutions = translation.get("public_solutions")
        translated_solution_count = len(translated_solutions) if isinstance(translated_solutions, list) else translated_solutions
        translated_media = translation.get("reader_images", translation.get("reader_media_positions"))
        require(translated_exercises == exercises, f"Unit {unit} translated exercise count")
        require(translated_solution_count == len(solutions), f"Unit {unit} translated solution count")
        require(translated_media == media, f"Unit {unit} translated media count")''',
)

generated = replace_once(
    generated,
    '''    for unit in range(22, 25):
        lecture_marker, exercise_marker, solution_marker, credit_marker = pdf_boundaries[unit]
        exercise_page = max(pdf_pages(pdf_text_parts, exercise_marker))
        lecture_candidates = [page for page in pdf_pages(pdf_text_parts, lecture_marker) if page <= exercise_page]
        require(lecture_candidates, f"PDF lecture boundary cannot be disambiguated: Unit {unit}")
        lecture_page = max(lecture_candidates)
        unit_sequence = [lecture_page, exercise_page]
        if solution_marker:
            solution_page = max(pdf_pages(pdf_text_parts, solution_marker))
            require(exercise_page <= solution_page, f"PDF solution precedes worksheet: Unit {unit}")
            marker_pages[solution_marker] = solution_page
            unit_sequence.append(solution_page)
        credit_page = max(pdf_pages(pdf_text_parts, credit_marker))
        marker_pages.update({lecture_marker: lecture_page, exercise_marker: exercise_page, credit_marker: credit_page})
        main_sequence.extend(unit_sequence)
        credit_sequence.append(credit_page)''',
    '''    for unit in range(28, 29):
        lecture_marker, exercise_marker, solution_marker, credit_marker = pdf_boundaries[unit]
        credit_page = max(pdf_pages(pdf_text_parts, credit_marker))
        solution_page = None
        if solution_marker:
            solution_candidates = [page for page in pdf_pages(pdf_text_parts, solution_marker) if page < credit_page]
            require(solution_candidates, f"PDF solution boundary cannot be disambiguated: Unit {unit}")
            solution_page = max(solution_candidates)
        exercise_limit = solution_page if solution_page is not None else credit_page
        exercise_candidates = [page for page in pdf_pages(pdf_text_parts, exercise_marker) if page <= exercise_limit]
        require(exercise_candidates, f"PDF worksheet boundary cannot be disambiguated: Unit {unit}")
        exercise_page = max(exercise_candidates)
        lecture_candidates = [page for page in pdf_pages(pdf_text_parts, lecture_marker) if page <= exercise_page]
        require(lecture_candidates, f"PDF lecture boundary cannot be disambiguated: Unit {unit}")
        lecture_page = max(lecture_candidates)
        unit_sequence = [lecture_page, exercise_page]
        if solution_marker:
            require(solution_page is not None and exercise_page <= solution_page, f"PDF solution precedes worksheet: Unit {unit}")
            marker_pages[solution_marker] = solution_page
            unit_sequence.append(solution_page)
        marker_pages.update({lecture_marker: lecture_page, exercise_marker: exercise_page, credit_marker: credit_page})
        main_sequence.extend(unit_sequence)
        credit_sequence.append(credit_page)''',
)

generated = generated.replace('build.get("through_unit") == 24', 'build.get("through_unit") == 28')
generated = generated.replace("set(range(1, 25))", "set(range(1, 29))")
generated = generated.replace("range(22, 25)", "range(28, 29)")
generated = generated.replace("pdf_boundaries[22]", "pdf_boundaries[28]")
generated = generated.replace('"through_unit": 24', '"through_unit": 28')
generated = generated.replace('"verified_date": "2026-08-25"', '"verified_date": "2026-08-26"')
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

if os.environ.get("AG_BRIDGE_SPECIALIZE_ONLY") == "1":
    compile(generated, str(TEMPLATE), "exec")
    print("Unit 28 reader-QA specialization: COMPILE PASS")
else:
    namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
    exec(compile(generated, str(TEMPLATE), "exec"), namespace)
