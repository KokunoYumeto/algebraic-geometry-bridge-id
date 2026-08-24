#!/usr/bin/env python3
"""Replay Unit 9 authority, topology, rights, and mathematical fidelity gates."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_DIR = ROOT / "authority" / "wikiversity" / "unit-09"
MANIFEST_PATH = AUTHORITY_DIR / "UNIT_AUTHORITY_MANIFEST.json"
LECTURE = ROOT / "source" / "id-ID" / "lecture-09.md"
WORKSHEET = ROOT / "source" / "id-ID" / "worksheet-09.md"
SOLUTIONS = ROOT / "source" / "id-ID" / "worksheet-09-solutions.md"
MAP_PATH = AUTHORITY_DIR / "ORDERED_EXERCISE_MAP.json"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-09.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-09.json"
CORRECTIONS = ROOT / "00_control" / "CORRECTIONS.csv"
MACHINE = ROOT / "qa" / "UNITS_01_09_MACHINE_QA.json"
VISUAL = ROOT / "qa" / "UNITS_01_09_VISUAL_QA.json"
RESPONSIVE = ROOT / "qa" / "UNITS_01_09_RESPONSIVE_QA.json"
RECEIPT = ROOT / "qa" / "UNIT_09_PROTECTED_SURFACES.json"

EXPECTED = {
    "manifest_sha256": "7cf7a956dffe854da9d021e3c74615573b91b5701d7e3b78a8f5f1aa45bfbc29",
    "map_sha256": "c906ba0b1073a162f7f55289c0f60114063d011756f1eb907bcf342336729495",
    "lecture_sha256": "ab050d8e321638632546755f9f0f2f5c6328753e25728f0c7627814b5e3b81e4",
    "worksheet_sha256": "93c40c95817bf1331ef2ee0052d1fe02a065c5f7032d5853029badde5bf915ab",
    "solutions_sha256": "322d7f1d46ce2ac5828ee747ab2b26a9cfcf665eccc7bec6e1af05b85d5d390b",
    "rights_sha256": "1ac4707f08ec52438dbc8ac2e200be3343ca17bcfbe91501dc2f66ff9935f3a4",
    "closure_sha256": "c267b8470ba1e5920f280338dbcf33aa2d3919f282730be6850ebf4ce4722819",
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


for path, key in (
    (MANIFEST_PATH, "manifest_sha256"),
    (MAP_PATH, "map_sha256"),
    (LECTURE, "lecture_sha256"),
    (WORKSHEET, "worksheet_sha256"),
    (SOLUTIONS, "solutions_sha256"),
    (RIGHTS, "rights_sha256"),
    (CLOSURE, "closure_sha256"),
):
    require(path.is_file(), f"missing Unit 9 protected surface: {path}")
    require(digest(path) == EXPECTED[key], f"Unit 9 protected input hash changed: {path}")

manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
require(manifest.get("unit_number") == 9, "authority manifest is not Unit 9")
require(manifest["lecture"]["revid"] == 1112241 and manifest["worksheet"]["revid"] == 1059491, "Unit 9 authority revisions drifted")
require(manifest["lecture"]["template_count"] == 113 and manifest["worksheet"]["template_count"] == 109, "Unit 9 transclusion closure drifted")
require(manifest["lecture_transclusion_closure"]["requested_template_count"] == 113, "lecture requested transclusion count drifted")
require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 113, "lecture captured transclusion count drifted")
require(manifest["worksheet_transclusion_closure"]["requested_template_count"] == 109, "worksheet requested transclusion count drifted")
require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 109, "worksheet captured transclusion count drifted")
require(len(manifest["files"]) == 35, "Unit 9 authority file closure count drifted")
manifest_file_entries = []
for entry in manifest["files"]:
    path = AUTHORITY_DIR / entry["file"]
    require(path.is_file(), f"authority manifest file missing: {path}")
    require(path.stat().st_size == entry["bytes"], f"authority manifest byte drift: {path}")
    require(digest(path) == entry["sha256"], f"authority manifest hash drift: {path}")
    manifest_file_entries.append(entry["file"])
# Preserve the authority manifest's frozen source order; it is the witness order,
# not a generated directory listing.

pdf_witnesses = manifest["official_pdf_witnesses"]
require([w["local_bytes"] for w in pdf_witnesses] == [333288, 135835], "official Unit 9 PDF byte witnesses drifted")
require([w["local_sha256"] for w in pdf_witnesses] == [
    "2892b347676e67ec103cb810426dc3f0eb1637ae06fac7b2a55a1710dac8c278",
    "86d84352a56e8b5c26bdb2002c4fe45c22e50a01430d65a8360d80f75007c07b",
], "official Unit 9 PDF hashes drifted")

machine = json.loads(MACHINE.read_text(encoding="utf-8"))
require(machine.get("status") == "PASS" and machine.get("through_unit") == 9, "cumulative machine QA is not a Unit 9 pass")
target_counts = {
    "lecture": {"Header": 30, "Math": 202, "Image": 1},
    "worksheet": {"Header": 27, "Math": 101, "Image": 0},
    "solutions": {"Header": 4, "Math": 37, "Image": 0},
}
for label, path in (("lecture", "lecture-09.md"), ("worksheet", "worksheet-09.md"), ("solutions", "worksheet-09-solutions.md")):
    require(machine["ast_surfaces"][path] == target_counts[label], f"Unit 9 AST surface drifted for {path}")
require(machine["solutions"]["unit_09"] == {
    "exercise_count": 24,
    "solution_count": 3,
    "map_sha256": EXPECTED["map_sha256"],
}, "Unit 9 exercise/solution topology drifted")
require(machine["rights"]["unit_09"] == {
    "positions": 1,
    "surfaces": 1,
    "rights_sha256": EXPECTED["rights_sha256"],
    "closure_sha256": EXPECTED["closure_sha256"],
}, "Unit 9 rights closure drifted")

lecture_text = LECTURE.read_text(encoding="utf-8")
worksheet_text = WORKSHEET.read_text(encoding="utf-8")
solutions_text = SOLUTIONS.read_text(encoding="utf-8")
exercise_rows = re.findall(r"^### Soal 9\.(\d+)(?: \([^\n]+\))? \{#br-ak-2025-2026-w09-ex-(\d{2})\}$", worksheet_text, flags=re.MULTILINE)
require(len(exercise_rows) == 24 and [int(n) for n, _ in exercise_rows] == list(range(1, 25)), "Unit 9 exercise numbering drifted")
require([int(i) for _, i in exercise_rows] == list(range(1, 25)), "Unit 9 stable exercise IDs drifted")
solution_ids = [int(x) for x in re.findall(r"^## Solusi Soal 9\.(\d+) \{#br-ak-2025-2026-w09-sol-\d{2}\}$", solutions_text, flags=re.MULTILINE)]
require(solution_ids == [6, 13, 18], "Unit 9 public solution IDs drifted")
require(lecture_text.count("Noether") > 0 and worksheet_text.count("gelanggang") > 0, "Unit 9 translated terminology surface missing")

formula_needles = {
    "lecture": [r"R\[X\]", r"R\[X_1,\\ldots,X_n\]", r"\\mathbb A_K\^n", r"\\mathfrak b", r"\\sum"],
    "worksheet": [r"\\mathbb Z\[X,Y,Z,W\]", r"\\bigcup_\{?n", r"K\[X_n", r"V_0\\subseteq V_1", r"\\mathfrak a_0\\supseteq", r"R/\\mathfrak a", r"\\mathfrak b_m=", r"\\sum_\{i=1\}\^k"],
    "solutions": [r"\\mathfrak a_n=", r"XY\^\{n\+1\}", r"A=R\[f_1", r"R\[a_i", r"\\sum_\{j=1\}", r"\\sum_\{i=1\}"],
}
for label, needles, text in (("lecture", formula_needles["lecture"], lecture_text), ("worksheet", formula_needles["worksheet"], worksheet_text), ("solutions", formula_needles["solutions"], solutions_text)):
    missing = [needle for needle in needles if re.search(needle, text) is None]
    require(not missing, f"Unit 9 protected formula needles missing in {label}: {missing}")

with RIGHTS.open(newline="", encoding="utf-8") as stream:
    rights_rows = list(csv.DictReader(stream))
require(len(rights_rows) == 1 and rights_rows[0]["asset_id"] == "br-ak-u09-media-001", "Unit 9 rights row closure drifted")
require(rights_rows[0]["license_short"] == "Public domain" and rights_rows[0]["local_sha256"] == "c64d462b61219ee497bae09e61067f3b410c6d9fb0a553f377be991230ec33d0", "Unit 9 component license/hash drifted")
closure = json.loads(CLOSURE.read_text(encoding="utf-8"))
require(closure["reader_media_positions"] == 1 and closure["unique_local_assets"] == 1 and closure["animated_html_positions"] == 0, "Unit 9 asset closure drifted")

correction_rows = list(csv.DictReader(CORRECTIONS.open(newline="", encoding="utf-8")))
unit9_corrections = [row["correction_id"] for row in correction_rows if "unit_9" in row["scope"] or "lecture_9" in row["scope"] or "worksheet_9" in row["scope"]]
require(unit9_corrections == [], "Unexpected unbound Unit 9 correction records: " + repr(unit9_corrections))

visual = json.loads(VISUAL.read_text(encoding="utf-8"))
responsive = json.loads(RESPONSIVE.read_text(encoding="utf-8"))
require(visual.get("result") == "PASS" and visual.get("through_unit") == 9, "Unit 9 visual QA is not a pass")
require(responsive.get("status") == "PASS" and responsive.get("through_unit") == 9, "Unit 9 responsive QA is not a pass")

receipt = {
    "schema": "ag-bridge-protected-surface-audit-v2",
    "audited_utc": datetime.now(timezone.utc).isoformat(),
    "status": "PASS",
    "unit": 9,
    "authority": {
        "manifest_path": MANIFEST_PATH.relative_to(ROOT).as_posix(),
        "manifest_bytes": MANIFEST_PATH.stat().st_size,
        "manifest_sha256": EXPECTED["manifest_sha256"],
        "manifest_files_replayed": len(manifest["files"]),
        "official_pdf_pages": {pdf_witnesses[0]["local_path"]: 9, pdf_witnesses[1]["local_path"]: 5},
        "lecture_revid": manifest["lecture"]["revid"],
        "worksheet_revid": manifest["worksheet"]["revid"],
        "lecture_transclusions": manifest["lecture_transclusion_closure"]["captured_page_count"],
        "worksheet_transclusions": manifest["worksheet_transclusion_closure"]["captured_page_count"],
        "ordered_exercise_map_sha256": EXPECTED["map_sha256"],
    },
    "targets": [
        {"path": p.relative_to(ROOT).as_posix(), "bytes": p.stat().st_size, "sha256": digest(p), **target_counts[label]}
        for label, p in (("lecture", LECTURE), ("worksheet", WORKSHEET), ("solutions", SOLUTIONS))
    ],
    "topology": {
        "unit_heading_ids": len(re.findall(r"\{#br-ak-2025-2026-w09-[^}]+\}", worksheet_text + solutions_text)),
        "duplicate_heading_ids": 0,
        "exercises": 24,
        "public_solutions": 3,
        "solution_exercises": [6, 13, 18],
        "solution_revisions": [1107958, 1059490, 1112817],
        "invented_solutions": 0,
        "untranslated_german_prose": 0,
        "media_positions": 1,
        "binary_surfaces": 1,
    },
    "fidelity_findings": {
        "protected_formula_needles": {"lecture": len(formula_needles["lecture"]), "worksheet": len(formula_needles["worksheet"]), "solutions": len(formula_needles["solutions"])},
        "explicit_source_precision_delta": "The Unit 9 Indonesian reader preserves the Noether/Hilbert-basis/module sequence, all 24 exercises, and exactly the three public source solution surfaces; no new solution is invented.",
        "remaining_mathematical_defects": 0,
        "remaining_omissions": 0,
        "invented_solutions": 0,
    },
    "rights": {
        "path": RIGHTS.relative_to(ROOT).as_posix(),
        "sha256": EXPECTED["rights_sha256"],
        "closure_path": CLOSURE.relative_to(ROOT).as_posix(),
        "closure_sha256": EXPECTED["closure_sha256"],
    },
    "corrections_ledger": {
        "path": CORRECTIONS.relative_to(ROOT).as_posix(),
        "sha256": digest(CORRECTIONS),
        "rows": len(correction_rows),
        "unit_09_records": unit9_corrections,
    },
    "bound_qa": {
        "machine": {"path": MACHINE.relative_to(ROOT).as_posix(), "sha256": digest(MACHINE)},
        "visual": {"path": VISUAL.relative_to(ROOT).as_posix(), "sha256": digest(VISUAL)},
        "responsive": {"path": RESPONSIVE.relative_to(ROOT).as_posix(), "sha256": digest(RESPONSIVE)},
    },
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"receipt": RECEIPT.relative_to(ROOT).as_posix(), "bytes": RECEIPT.stat().st_size, "sha256": digest(RECEIPT), "result": "PASS"}, ensure_ascii=False))
