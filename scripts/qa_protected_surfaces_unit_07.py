#!/usr/bin/env python3
"""Bind Unit 7's human fidelity audit to replayable authority and reader evidence.

The Unit 6 checker supplies the audited implementation.  This wrapper replaces
only Unit-specific authority, topology, formula, rights, and correction
constants while preserving the established receipt shape.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "qa_protected_surfaces_unit_06.py"
source = TEMPLATE.read_text(encoding="utf-8")


def replace_exact(old: str, new: str, *, expected: int | None = None) -> None:
    global source
    count = source.count(old)
    if expected is not None and count != expected:
        raise SystemExit(f"Protected-QA template drift for {old!r}: expected {expected}, found {count}")
    if count == 0:
        raise SystemExit(f"Protected-QA template marker absent: {old!r}")
    source = source.replace(old, new)


for old, new in (
    ("Unit 6", "Unit 7"),
    ("unit-06", "unit-07"),
    ("lecture-06", "lecture-07"),
    ("worksheet-06", "worksheet-07"),
    ("UNITS_01_06", "UNITS_01_07"),
    ("UNIT_06", "UNIT_07"),
    ("w06", "w07"),
):
    replace_exact(old, new)

replace_exact('manifest["unit_number"] == 6', 'manifest["unit_number"] == 7', expected=1)
replace_exact('exercise_map["exercise_count"] == 30', 'exercise_map["exercise_count"] == 33', expected=1)
replace_exact('exercise_map["solution_count"] == 9', 'exercise_map["solution_count"] == 3', expected=1)
replace_exact('sorted(pdf_pages.values()) == [7, 9]', 'sorted(pdf_pages.values()) == [7, 13]', expected=1)
replace_exact(
    'target_counts[LECTURE.name] == {"headings": 17, "math_nodes": 142, "images": 3}',
    'target_counts[LECTURE.name] == {"headings": 13, "math_nodes": 221, "images": 9}',
    expected=1,
)
replace_exact(
    'target_counts[WORKSHEET.name] == {"headings": 33, "math_nodes": 109, "images": 0}',
    'target_counts[WORKSHEET.name] == {"headings": 36, "math_nodes": 148, "images": 0}',
    expected=1,
)
replace_exact(
    'target_counts[SOLUTIONS.name] == {"headings": 10, "math_nodes": 105, "images": 0}',
    'target_counts[SOLUTIONS.name] == {"headings": 4, "math_nodes": 61, "images": 0}',
    expected=1,
)
replace_exact(
    'r"^### Soal 6\\.(\\d+)( ★)?(?: - (\\d+) poin)? \\{#br-ak-2025-2026-w07-ex-(\\d{2})\\}$"',
    'r"^### Soal 7\\.(\\d+)( ★)?(?: - (\\d+) poin)? \\{#br-ak-2025-2026-w07-ex-(\\d{2})\\}$"',
    expected=1,
)
replace_exact("len(exercise_rows) == 30", "len(exercise_rows) == 33", expected=1)
replace_exact("list(range(1, 31))", "list(range(1, 34))", expected=1)
replace_exact(
    "starred == [3, 4, 8, 9, 17, 18, 21, 22, 25]",
    "starred == [10, 11, 22]",
    expected=1,
)
replace_exact("points == [3, 6, 5, 5, 4]", "points == [6, 9, 4, 6, 4, 6, 6]", expected=1)
replace_exact(
    'expected_solution_ids = [3, 4, 8, 9, 17, 18, 21, 22, 25]',
    'expected_solution_ids = [10, 11, 22]',
    expected=1,
)
replace_exact(
    'expected_solution_revids = [1112350, 958133, 1057120, 1112838, 1096769, 1024155, 1067921, 1096509, 1089645]',
    'expected_solution_revids = [1113188, 1112940, 1095499]',
    expected=1,
)
replace_exact("len(ids) == 60 and len(set(ids)) == 60", "len(ids) == 53 and len(set(ids)) == 53", expected=1)
replace_exact(
    'active_prose = "\\n".join(body_text(path) for path in (LECTURE, WORKSHEET, SOLUTIONS))',
    '''active_prose = "\\n".join(body_text(path) for path in (LECTURE, WORKSHEET, SOLUTIONS))
active_prose = re.sub(r"\\]\\([^)]*\\)", "]", active_prose)''',
    expected=1,
)

formula_block = r'''require_formulae(LECTURE, [
    r"Z^2=X^2+Y^2", r"C=V(Z^2-X^2-Y^2)\cap V(aX+bY+cZ+d)",
    r"F=\alpha X^2+\beta XY+\gamma Y^2+\delta X+\epsilon Y+\eta",
    r"\gamma\left(Y+\frac{\beta X+\epsilon}{2\gamma}\right)^2",
    r"\mathbb A_K^1\supseteq D(Q)&\longrightarrow\mathbb A_K^2",
    r"F(at,a)=(at)^2+\beta(at\,a)+\gamma a^2+\delta at+\epsilon a",
    r"a_2=\frac{-\delta t-\epsilon}{t^2+\beta t+\gamma}",
    r"Q(t)=t^2+\beta t+\gamma\ne0", r"P_1=-t(\delta t+\epsilon)",
    r"P_2=-\delta t-\epsilon", r"F=X^2+\beta XY+\gamma Y^2",
    r"t=\frac{P_1}{Q}\cdot\frac{Q}{P_2}",
])
require_formulae(WORKSHEET, [
    r"X^2+Y^2=1", r"4X^2+3Y^2=9", r"C=V\left(X^{d+1}-Y^d\right)",
    r"(x,y)\longmapsto\left(\frac{3x-y}{2},\frac{x+3y}{2}\right)",
    r"R=\mathbb Q[Y]", r"S=(\mathbb Q[Y])[X]/\left(X^2+Y^2-p\right)",
    r"(u,v)&\longmapsto(u^2+uv,v-u^2)=(x,y)",
    r"R=\mathbb R[X,Y]/(X^2+Y^2-1)",
    r"F=x^2+2xy-y^2+x-3y+4", r"C=V\left(X^4+Y^4-1\right)",
])
require_formulae(SOLUTIONS, [
    r"\widetilde X=\frac{2}{3}X", r"\widetilde Y=\frac{1}{\sqrt{3}}Y",
    r"b^2+e^2=\frac{1}{3}", r"3(r^2+s^2)=t^2",
    r"\widetilde C=V\left(U^2+V^2+2U+4V\right)",
    r"P_1=-t(2t+4)", r"P_2=-(2t+4)", r"Q=t^2+1",
    r"\mathbb Q\longrightarrow \widetilde C\subset\mathbb A^2_{\mathbb Q}",
    r"\frac{-t^2-4t+1}{t^2+1}", r"\frac{2t^2-2t-2}{t^2+1}",
])'''
source, count = re.subn(
    r"require_formulae\(LECTURE, \[\n.*?\n\]\)\nrequire_formulae\(WORKSHEET, \[\n.*?\n\]\)\nrequire_formulae\(SOLUTIONS, \[\n.*?\n\]\)",
    lambda _: formula_block,
    source,
    count=1,
    flags=re.DOTALL,
)
if count != 1:
    raise SystemExit("Protected-QA formula block drift")

replace_exact('len(rights_rows) == 3', 'len(rights_rows) == 9', expected=1)
replace_exact(
    'closure["reader_media_positions"] == 3 and closure["unique_local_assets"] == 4',
    'closure["reader_media_positions"] == 9 and closure["unique_local_assets"] == 13',
    expected=1,
)
replace_exact(
    'required_corrections = {"AGC-CORR-0010", "AGC-ADAPT-0008", "AGC-ADAPT-0009", "AGC-ADAPT-0010", "AGC-ADAPT-0011"}',
    '''required_corrections = {
    "AGC-CORR-0011", "AGC-CORR-0012", "AGC-CORR-0013", "AGC-CORR-0014",
    "AGC-CORR-0015", "AGC-CORR-0016", "AGC-CORR-0017", "AGC-CORR-0018",
    "AGC-CORR-0019", "AGC-ADAPT-0012", "AGC-ADAPT-0013", "AGC-ADAPT-0014",
    "AGC-ADAPT-0015", "AGC-ADAPT-0016",
}''',
    expected=1,
)
replace_exact(
    'source_math == {"lecture": 158, "worksheet": 111, "solutions": 116}',
    'source_math == {"lecture": 239, "worksheet": 129, "solutions": 57}',
    expected=1,
)
replace_exact('machine.get("through_unit") == 6', 'machine.get("through_unit") == 7', expected=1)
replace_exact('visual.get("through_unit") == 6', 'visual.get("through_unit") == 7', expected=1)
replace_exact('responsive.get("through_unit") == 6', 'responsive.get("through_unit") == 7', expected=1)
replace_exact('"unit": 6', '"unit": 7', expected=1)
replace_exact('"exercises": 30', '"exercises": 33', expected=1)
replace_exact('"public_solutions": 9', '"public_solutions": 3', expected=1)
replace_exact('"media_positions": 3, "binary_surfaces": 4', '"media_positions": 9, "binary_surfaces": 13', expected=1)
replace_exact(
    '"explanation": "Pandoc and MediaWiki split aligned formulae and renderer scaffolding differently. Exact hypotheses, elimination identities, homogeneous substitutions, exercise order, and all nine solution surfaces are protected by formula needles and revision bindings."',
    '"explanation": "Pandoc and MediaWiki split aligned formulae and renderer scaffolding differently. Exact conic and quadric identities, classification branches, parametrization formulae, exercise order, and all three public solution surfaces are protected by formula needles and revision bindings."',
    expected=1,
)
replace_exact(
    '"protected_formula_needles": {"lecture": 12, "worksheet": 7, "solutions": 5}',
    '"protected_formula_needles": {"lecture": 12, "worksheet": 10, "solutions": 11}',
    expected=1,
)
replace_exact(
    '"explicit_source_precision_delta": "The ternary homogeneous F is dehomogenized explicitly as G(X,Y)=F(X,Y,1) before the two-variable rational identity."',
    '"explicit_source_precision_delta": "The c=0 classification branches, ellipse misnomer, false universal exercise claim, field dependency, coordinate-ring hint, solution proof gap, and shifted-curve referent are disclosed or repaired explicitly without inventing source solutions."',
    expected=1,
)
replace_exact('"unit_06_records": sorted(required_corrections)', '"unit_07_records": sorted(required_corrections)', expected=1)

required_markers = [
    'AUTHORITY_DIR = ROOT / "authority" / "wikiversity" / "unit-07"',
    'MACHINE_QA = ROOT / "qa" / "UNITS_01_07_MACHINE_QA.json"',
    'expected_solution_ids = [10, 11, 22]',
    'target_counts[LECTURE.name] == {"headings": 13, "math_nodes": 221, "images": 9}',
    '"media_positions": 9, "binary_surfaces": 13',
    '"unit_07_records": sorted(required_corrections)',
]
missing = [marker for marker in required_markers if marker not in source]
if missing:
    raise SystemExit(f"Transformed protected-QA markers absent: {missing}")

exec(compile(source, str(Path(__file__).resolve()), "exec"), globals())
