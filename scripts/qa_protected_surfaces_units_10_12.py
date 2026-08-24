#!/usr/bin/env python3
"""Protect the cumulative Unit 12 release boundary for Units 10--12.

This audit binds the immutable Unit 9 baseline, replays the three new source
units and their primary authority closure, and requires the final machine,
visual, and responsive receipts to describe the same public reader bytes.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import qa_reader_units_01_12 as readerqa  # noqa: E402


base = readerqa.base
SOURCE = readerqa.SOURCE
QA = ROOT / "qa"
MACHINE = QA / "UNITS_01_12_MACHINE_QA.json"
VISUAL = QA / "UNITS_01_12_VISUAL_QA.json"
RESPONSIVE = QA / "UNITS_01_12_RESPONSIVE_QA.json"
RECEIPT = QA / "UNIT_12_PROTECTED_SURFACES.json"

FINDINGS = {
    10: (QA / "unit-10-translation-findings.md", 3361, "a329cf204c90f1a576fdcc7a9bcdad777aa653e804d4fdb206f1116cc136c4b4"),
    11: (QA / "unit-11-translation-findings.md", 3747, "f734268c5488acb6af5f7e6d82b9a1e5145cf0add438ac9a1c062a11cf4fe487"),
    12: (QA / "unit-12-translation-findings.md", 5532, "122545250dc00a8d14cee730d2754f865389abdd423a0e6d1f4f71afe2a5530d"),
}

UNIT_FILES = {
    10: (SOURCE / "lecture-10.md", SOURCE / "worksheet-10.md", SOURCE / "worksheet-10-solutions.md"),
    11: (SOURCE / "lecture-11.md", SOURCE / "worksheet-11.md", SOURCE / "worksheet-11-solutions.md", SOURCE / "media-credits-unit-11.md"),
    12: (SOURCE / "lecture-12.md", SOURCE / "worksheet-12.md", SOURCE / "worksheet-12-solutions.md", SOURCE / "media-credits-unit-12.md"),
}
EXPECTED_UNIT_IDS = {10: 60, 11: 60, 12: 57}
EXPECTED_STARS = {10: [1, 6, 9, 16, 17, 20], 11: [6, 7], 12: [6, 12]}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def require_regular(path: Path) -> None:
    base.require(path.is_file() and not path.is_symlink(), f"missing/nonregular protected input: {rel(path)}")


def replay_receipted_file(row: dict, label: str) -> Path:
    for field in ("path", "bytes", "sha256"):
        base.require(field in row, f"{label} lacks {field}")
    root_resolved = ROOT.resolve()
    path = (ROOT / row["path"]).resolve()
    base.require(path.is_relative_to(root_resolved), f"{label} path escapes lane: {row['path']}")
    require_regular(path)
    base.require(path.stat().st_size == row["bytes"], f"{label} byte replay: {row['path']}")
    base.require(base.digest(path) == row["sha256"], f"{label} hash replay: {row['path']}")
    return path


def topology_for_unit(unit: int, spec: dict) -> dict:
    lecture = SOURCE / f"lecture-{unit:02d}.md"
    worksheet = SOURCE / f"worksheet-{unit:02d}.md"
    solutions = SOURCE / f"worksheet-{unit:02d}-solutions.md"
    lecture_text = lecture.read_text(encoding="utf-8")
    worksheet_text = worksheet.read_text(encoding="utf-8")
    solutions_text = solutions.read_text(encoding="utf-8")

    exercise_rows = re.findall(
        rf"^### Soal {unit}\.(\d+)(.*?)\{{#br-ak-2025-2026-w{unit:02d}-ex-(\d{{2}})\}}\s*$",
        worksheet_text,
        flags=re.MULTILINE,
    )
    exercise_numbers = [int(number) for number, _, _ in exercise_rows]
    stable_numbers = [int(stable) for _, _, stable in exercise_rows]
    star_numbers = [int(number) for number, middle, _ in exercise_rows if "★" in middle]
    base.require(exercise_numbers == list(range(1, spec["exercises"] + 1)), f"Unit {unit} exercise order")
    base.require(stable_numbers == exercise_numbers, f"Unit {unit} exercise stable-ID order")
    base.require(star_numbers == EXPECTED_STARS[unit] == spec["solution_numbers"], f"Unit {unit} literal source-star set")
    base.require(all(middle.count("★") <= 1 for _, middle, _ in exercise_rows), f"Unit {unit} duplicate source star")

    solution_rows = re.findall(
        rf"^## Solusi Soal {unit}\.(\d+) \{{#br-ak-2025-2026-w{unit:02d}-sol-(\d{{2}})\}}\s*$",
        solutions_text,
        flags=re.MULTILINE,
    )
    solution_numbers = [int(number) for number, _ in solution_rows]
    solution_stable_numbers = [int(stable) for _, stable in solution_rows]
    base.require(solution_numbers == spec["solution_numbers"], f"Unit {unit} translated public-solution order")
    base.require(solution_stable_numbers == solution_numbers, f"Unit {unit} solution stable-ID order")

    map_path = ROOT / "authority" / "wikiversity" / f"unit-{unit:02d}" / "ORDERED_EXERCISE_MAP.json"
    mapping = json.loads(map_path.read_text(encoding="utf-8"))
    public = [row for row in mapping["entries"] if row.get("has_public_solution")]
    base.require(mapping["exercise_count"] == spec["exercises"] and len(mapping["entries"]) == spec["exercises"], f"Unit {unit} full map topology")
    base.require(mapping["solution_count"] == spec["solutions"], f"Unit {unit} map solution count")
    base.require([row["exercise_number"] for row in public] == solution_numbers, f"Unit {unit} map/source solution identity")
    base.require([row["revid"] for row in public] == spec["solution_revids"], f"Unit {unit} solution revision identity")
    solution_summary = base.verify_solution_map(unit, solutions, spec["exercises"], spec["solutions"])

    unit_ids: list[str] = []
    for path in UNIT_FILES[unit]:
        unit_ids.extend(base.source_ids(path))
    base.require(len(unit_ids) == len(set(unit_ids)) == EXPECTED_UNIT_IDS[unit], f"Unit {unit} stable-ID closure")

    rights_path = ROOT / "authority" / f"RIGHTS-unit-{unit:02d}.csv"
    closure_path = ROOT / "authority" / f"ASSET_CLOSURE-unit-{unit:02d}.json"
    rights_summary = base.verify_rights(
        rights_path.name, closure_path.name, spec["positions"], spec["surfaces"]
    )
    with rights_path.open("r", encoding="utf-8", newline="") as stream:
        rights_rows = list(csv.DictReader(stream))
    image_rows = re.findall(r"!\[([^\]]*)\]\((authority/assets/[^)]+)\)", lecture_text)
    base.require(len(image_rows) == spec["positions"], f"Unit {unit} reader image-position count")
    base.require(all(alt.strip() for alt, _ in image_rows), f"Unit {unit} source image alt text")
    base.require([path for _, path in image_rows] == [row["local_path"] for row in rights_rows], f"Unit {unit} source/rights asset order")
    base.require(base.digest(rights_path) == spec["rights_sha256"], f"Unit {unit} rights frozen hash")
    base.require(base.digest(closure_path) == spec["closure_sha256"], f"Unit {unit} asset-closure frozen hash")

    authority = readerqa.verify_authority(unit, spec)
    return {
        "source_ids": len(unit_ids),
        "exercises": len(exercise_rows),
        "public_solutions": len(solution_rows),
        "solution_exercises": solution_numbers,
        "solution_revisions": spec["solution_revids"],
        "literal_source_stars": star_numbers,
        "invented_solutions": 0,
        "media_positions": len(image_rows),
        "binary_surfaces": spec["surfaces"],
        "solution_map": solution_summary,
        "rights": rights_summary,
        "authority": authority,
    }


def verify_source_quirks() -> dict:
    u10 = (SOURCE / "worksheet-10-solutions.md").read_text(encoding="utf-8")
    u11_lecture = (SOURCE / "lecture-11.md").read_text(encoding="utf-8")
    u11_worksheet = (SOURCE / "worksheet-11.md").read_text(encoding="utf-8")
    u12_lecture = (SOURCE / "lecture-12.md").read_text(encoding="utf-8")
    u12_solutions = (SOURCE / "worksheet-12-solutions.md").read_text(encoding="utf-8")

    base.require("R/(I\\cap J)" in u10 and "$s-t\\in I+J$" in u10, "AGC-ADAPT-0021 quotient grouping absent")
    base.require("a\\in I,\\quad b\\in J" in u10, "Unit 10 TeX spacing correction absent")
    base.require("korespondensi antara ideal-ideal $R/\\mathfrak a$" in u10, "AGC-ADAPT-0022 quotient correspondence absent")
    base.require("$P_1X_0$" in u11_lecture and "$P_1X_n$" in u11_lecture, "AGC-CORR-0023 source/corrected indices absent")
    base.require("Konteks ekspansi menurut variabel $X_n$" in u11_lecture, "AGC-CORR-0023 edition note absent")
    base.require("luar penyebut gelanggang faktor" in u11_worksheet and "Tanda kurung di atas" in u11_worksheet, "AGC-ADAPT-0024 edition note absent")
    base.require("soal menamai aljabar dengan $R$" in u12_solutions and "memakai $A$" in u12_solutions, "AGC-ADAPT-0025 notation note absent")
    base.require("setidaknya satu citra variabel" in u12_lecture, "AGC-ADAPT-0026 generator clarification absent")
    base.require(u12_solutions.count("```{=latex}\n\\clearpage\n```") == 1, "Unit 12 PDF-only pagination guard absent/drifted")

    with readerqa.CORRECTIONS.open("r", encoding="utf-8", newline="") as stream:
        correction_rows = list(csv.DictReader(stream))
    by_id = {row["correction_id"]: row for row in correction_rows}
    base.require(len(by_id) == len(correction_rows), "duplicate correction ID")
    bound = {}
    for correction_id, (scope, status) in readerqa.CORRECTION_BINDINGS.items():
        row = by_id.get(correction_id)
        base.require(row is not None, f"missing correction binding: {correction_id}")
        base.require(row["scope"] == scope and row["status"] == status, f"correction binding drift: {correction_id}")
        bound[correction_id] = {"scope": scope, "status": status}
    return {
        "path": rel(readerqa.CORRECTIONS),
        "bytes": readerqa.CORRECTIONS.stat().st_size,
        "sha256": base.digest(readerqa.CORRECTIONS),
        "rows": len(correction_rows),
        "bindings": bound,
        "protected_correction_surfaces_replayed": 7,
        "pdf_only_pagination_guard_replayed": True,
    }


def verify_findings() -> dict:
    result = {}
    required_phrases = {
        10: ("R/(I\\cap J)", "quotient-ring correspondence", "six exercises"),
        11: ("P_1X_0", "P_1X_n", "Exercise 11.19"),
        12: ("khusus-PDF", "3,244 bytes", "aea4ad61cfc3bb7412f6690a850377c9418021aa5ff226173b51f9fb9b06d516"),
    }
    for unit, (path, expected_bytes, expected_hash) in FINDINGS.items():
        require_regular(path)
        base.require(path.stat().st_size == expected_bytes, f"Unit {unit} finding bytes")
        base.require(base.digest(path) == expected_hash, f"Unit {unit} finding hash")
        text = path.read_text(encoding="utf-8")
        for phrase in required_phrases[unit]:
            base.require(phrase in text, f"Unit {unit} finding lacks bound phrase: {phrase}")
        result[f"unit_{unit:02d}"] = {"path": rel(path), "bytes": expected_bytes, "sha256": expected_hash}
    return result


def verify_machine() -> dict:
    require_regular(MACHINE)
    machine = json.loads(MACHINE.read_text(encoding="utf-8"))
    base.require(machine.get("schema") == "ag-bridge-machine-qa-receipt-v4", "Unit 12 machine schema")
    base.require(machine.get("status") == "PASS" and machine.get("through_unit") == 12, "Unit 12 machine QA is not PASS")
    base.require(machine.get("stable_ids") == 670 and machine.get("exercise_count") == 330 and machine.get("public_solution_count") == 55, "machine cumulative topology")
    base.require(machine.get("units_01_09_baseline", {}).get("protected_sha256") == readerqa.BASELINE_WITNESSES[QA / "UNIT_09_PROTECTED_SURFACES.json"][1], "machine Unit 9 baseline binding")
    for path, (expected_bytes, expected_hash) in readerqa.NEW_SOURCE_HASHES.items():
        row = machine["frozen_source_hashes"].get(rel(path))
        base.require(row == {"bytes": expected_bytes, "sha256": expected_hash}, f"machine frozen-source binding: {rel(path)}")
    for path, expected in readerqa.NEW_AST.items():
        observed = machine["ast_surfaces"].get(path.name)
        base.require(observed == {"Header": expected["headers"], "Math": expected["math"], "Image": expected["images"]}, f"machine AST binding: {path.name}")
    for unit, spec in readerqa.UNIT_SPEC.items():
        key = f"unit_{unit:02d}"
        base.require(machine["solutions"][key]["exercise_count"] == spec["exercises"] and machine["solutions"][key]["solution_count"] == spec["solutions"], f"machine Unit {unit} solution topology")
        base.require(machine["solutions"][key]["map_sha256"] == spec["map_sha256"], f"machine Unit {unit} solution-map binding")
        base.require(machine["rights"][key]["positions"] == spec["positions"] and machine["rights"][key]["surfaces"] == spec["surfaces"], f"machine Unit {unit} rights topology")
        base.require(machine["authority"][key]["manifest_sha256"] == spec["manifest_sha256"], f"machine Unit {unit} authority binding")
    base.require(machine["html"]["sha256"] == readerqa.FROZEN_BUILD["html"]["sha256"] and machine["html"]["bytes"] == readerqa.FROZEN_BUILD["html"]["bytes"], "machine HTML identity")
    base.require(machine["html"]["images"] == 65 and machine["html"]["mathml_nodes"] == 4499, "machine HTML topology")
    base.require(machine["pdf"]["sha256"] == readerqa.FROZEN_BUILD["pdf"]["sha256"] and machine["pdf"]["bytes"] == readerqa.FROZEN_BUILD["pdf"]["bytes"], "machine PDF identity")
    base.require(machine["pdf"]["pages"] == readerqa.EXPECTED_PDF_PAGES, "machine PDF page count")
    base.require(machine["build_receipt"]["sha256"] == readerqa.FROZEN_BUILD["receipt"]["sha256"], "machine build-receipt identity")
    current_script_hash = base.digest(ROOT / "scripts" / "qa_reader_units_01_12.py")
    base.require(machine["qa_script"] == {"path": "scripts/qa_reader_units_01_12.py", "sha256": current_script_hash}, "machine QA script identity")
    return machine


def verify_visual(machine: dict) -> dict:
    require_regular(VISUAL)
    visual = json.loads(VISUAL.read_text(encoding="utf-8"))
    base.require(visual.get("schema") == "ag-bridge-visual-qa-v1" and visual.get("status") == "PASS", "Unit 12 visual QA is not PASS")
    scope = visual.get("scope", {})
    base.require(scope.get("through_unit") == 12 and scope.get("language") == "id-ID", "visual scope/language")
    base.require(scope.get("pdf") == rel(readerqa.PDF), "visual PDF path")
    base.require(scope.get("pdf_bytes") == machine["pdf"]["bytes"] and scope.get("pdf_sha256") == machine["pdf"]["sha256"], "visual PDF byte identity")
    base.require(scope.get("pages") == readerqa.EXPECTED_PDF_PAGES and scope.get("page_size") == "A4", "visual PDF pages/size")
    base.require(scope.get("encrypted") is False, "visual PDF encrypted")
    replay_receipted_file(
        {"path": scope["pdf"], "bytes": scope["pdf_bytes"], "sha256": scope["pdf_sha256"]},
        "visual PDF",
    )

    raster = visual.get("deterministic_raster", {})
    manifest_row = {
        "path": raster.get("page_manifest"),
        "bytes": raster.get("page_manifest_bytes"),
        "sha256": raster.get("page_manifest_sha256"),
    }
    manifest_path = replay_receipted_file(manifest_row, "visual page manifest")
    page_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    base.require(page_manifest.get("schema") == "ag-bridge-visual-page-manifest-v1" and page_manifest.get("status") == "PASS", "visual page-manifest schema/status")
    base.require(page_manifest.get("pdf") == {"path": rel(readerqa.PDF), "bytes": machine["pdf"]["bytes"], "sha256": machine["pdf"]["sha256"], "pages": readerqa.EXPECTED_PDF_PAGES}, "visual page-manifest PDF binding")
    render = page_manifest.get("render", {})
    pages = render.get("pages", [])
    base.require(len(pages) == readerqa.EXPECTED_PDF_PAGES, "visual all-page render count")
    base.require([row.get("page") for row in pages] == list(range(1, readerqa.EXPECTED_PDF_PAGES + 1)), "visual all-page render order")
    page_paths = []
    for row in pages:
        path = replay_receipted_file(row, f"visual page {row.get('page')}")
        page_paths.append(path)
    base.require(len(page_paths) == len(set(page_paths)), "duplicate visual page render path")
    base.require(render.get("page_count") == len(pages) == raster.get("page_png_count"), "visual page-count cross-binding")
    base.require(render.get("total_bytes") == sum(row["bytes"] for row in pages) == raster.get("total_png_bytes"), "visual render-byte cross-binding")
    base.require(render.get("resolution_dpi") == raster.get("resolution_dpi") > 0, "visual render resolution")
    dimensions = raster.get("dimensions_px", [])
    base.require(dimensions == [794, 1123], "visual render dimensions")
    base.require(all([row.get("width_px"), row.get("height_px")] == dimensions for row in pages), "visual page-dimension mismatch")
    base.require(raster.get("blank_pages_detected") == 0 and raster.get("dimension_mismatches") == 0, "visual raster defect")

    review = visual.get("visual_inspection", {})
    checks = review.get("checks", {})
    base.require(checks and all(value == "PASS" for value in checks.values()), "visual review check failed")
    contact_sheets = review.get("all_page_contact_sheets", [])
    base.require(len(contact_sheets) == 11 and contact_sheets[0] == "pages 1-20" and contact_sheets[-1] == "pages 201-215", "visual contact-sheet all-page review absent")
    full_size = set(review.get("full_size_pages_checked", []))
    base.require({183, 210, 211, 215} <= full_size, "visual affected-page full-size review absent")
    resolved = json.dumps(visual.get("findings_resolved_before_freeze", []), ensure_ascii=False)
    base.require("AGC-CORR-0027" in resolved and "clearpage" in resolved, "visual resolved-finding binding absent")
    visual["_page_manifest_binding"] = manifest_row
    return visual


def verify_responsive(machine: dict) -> dict:
    require_regular(RESPONSIVE)
    responsive = json.loads(RESPONSIVE.read_text(encoding="utf-8"))
    base.require(responsive.get("status") == "PASS" and responsive.get("through_unit") == 12, "Unit 12 responsive QA is not PASS")
    artifact = responsive.get("artifact", {})
    base.require(artifact.get("path") == rel(readerqa.HTML), "responsive HTML path")
    base.require(artifact.get("bytes") == machine["html"]["bytes"] and artifact.get("sha256") == machine["html"]["sha256"], "responsive HTML byte identity")
    base.require(artifact.get("title") == "Kurva Aljabar - Unit 1-12" and artifact.get("language") == "id-ID", "responsive HTML title/language")
    base.require(artifact.get("mathml_nodes") == 4499 and artifact.get("images") == 65, "responsive HTML topology")
    base.require(artifact.get("broken_images") == 0 and artifact.get("browser_console_warnings_or_errors") == 0, "responsive browser defect")
    replay_receipted_file(artifact, "responsive HTML")

    responsive_source = responsive.get("responsive_source", {})
    base.require(responsive_source.get("path") == rel(readerqa.CSS), "responsive CSS path")
    base.require(responsive_source.get("bytes") == readerqa.CSS.stat().st_size and responsive_source.get("sha256") == base.digest(readerqa.CSS), "responsive CSS identity")
    desktop = responsive.get("desktop", {})
    mobile = responsive.get("mobile", {})
    base.require(desktop.get("visual_result") == "PASS" and desktop.get("centered_reader") is True, "desktop reader not centered/PASS")
    base.require(desktop.get("page_horizontal_overflow") is False and desktop.get("rendered_elements_outside_viewport") == 0, "desktop overflow")
    base.require(mobile.get("visual_result") == "PASS" and mobile.get("page_horizontal_overflow") is False, "mobile reader overflow/PASS")
    base.require(mobile.get("images_over_content") == 0 and mobile.get("overflow_blocks_without_auto") == 0, "mobile content overflow")
    verification = responsive.get("verification", {})
    boolean_checks = [value for value in verification.values() if isinstance(value, bool)]
    base.require(boolean_checks and all(boolean_checks), "responsive verification contains a false check")
    required_checks = {
        "all_images_local_and_loaded", "all_image_alt_text_nonempty", "desktop_and_mobile_title_and_language_match",
        "desktop_body_centered", "mobile_math_overflow_is_contained", "desktop_screenshot_reviewed", "mobile_screenshot_reviewed",
    }
    base.require(required_checks <= set(verification), "responsive verification closure")
    return responsive


def main() -> int:
    for path in (*readerqa.NEW_SOURCE_HASHES, *[item[0] for item in FINDINGS.values()], readerqa.CORRECTIONS, readerqa.BUILD_RECEIPT, readerqa.HTML, readerqa.PDF):
        require_regular(path)
    for path, (expected_bytes, expected_hash) in readerqa.NEW_SOURCE_HASHES.items():
        base.require(path.stat().st_size == expected_bytes and base.digest(path) == expected_hash, f"protected frozen source identity: {rel(path)}")

    new_source_text = "\n".join(path.read_text(encoding="utf-8") for unit_paths in UNIT_FILES.values() for path in unit_paths)
    visible = readerqa.visible_markdown(new_source_text)
    placeholder_re = re.compile(r"\b(?:TODO|TBD|FIXME|XXX|PLACEHOLDER|TRANSLATE)\b|pending_component_audit|<!--\s*QA:", re.I)
    secret_re = re.compile(r"github_pat_|ghp_[A-Za-z0-9]{20,}|ZENODO_ACCESS_TOKEN|access_token\s*[:=]", re.I)
    german_re = re.compile(r"\b(Es sei|Zeige|Beweise|Wir betrachten|Dann gilt|genau dann|Aufgabe|Beweis|Körper|Ring|Polynomring|Koordinatenring)\b")
    base.require(placeholder_re.search(new_source_text) is None, "placeholder in protected sources")
    base.require(secret_re.search(new_source_text) is None, "credential-shaped text in protected sources")
    base.require(german_re.search(visible) is None, "active German prose in protected sources")
    base.require("\ufffd" not in new_source_text and "\x00" not in new_source_text, "mojibake/NUL in protected sources")

    all_new_ids = [identifier for unit_paths in UNIT_FILES.values() for path in unit_paths for identifier in base.source_ids(path)]
    base.require(len(all_new_ids) == len(set(all_new_ids)) == 177, "Units 10--12 stable-ID closure")
    units = {f"unit_{unit:02d}": topology_for_unit(unit, spec) for unit, spec in readerqa.UNIT_SPEC.items()}
    base.require(sum(row["exercises"] for row in units.values()) == 85, "Units 10--12 exercise count")
    base.require(sum(row["public_solutions"] for row in units.values()) == 10, "Units 10--12 public-solution count")
    base.require(sum(row["media_positions"] for row in units.values()) == 5, "Units 10--12 media-position count")

    corrections = verify_source_quirks()
    findings = verify_findings()
    machine = verify_machine()
    visual = verify_visual(machine)
    responsive = verify_responsive(machine)

    build = json.loads(readerqa.BUILD_RECEIPT.read_text(encoding="utf-8"))
    base.require(build.get("through_unit") == 12 and base.digest(readerqa.BUILD_RECEIPT) == readerqa.FROZEN_BUILD["receipt"]["sha256"], "protected build receipt boundary")
    outputs = {row["path"]: row for row in build["outputs"]}
    base.require(outputs[rel(readerqa.HTML)]["sha256"] == machine["html"]["sha256"] == responsive["artifact"]["sha256"], "HTML cross-receipt identity")
    base.require(outputs[rel(readerqa.PDF)]["sha256"] == machine["pdf"]["sha256"] == visual["scope"]["pdf_sha256"], "PDF cross-receipt identity")

    receipt = {
        "schema": "ag-bridge-protected-surface-audit-v3",
        "status": "PASS",
        "unit": 12,
        "scope": "cumulative release boundary; direct replay of Units 10--12 over frozen Units 1--9 baseline",
        "units_01_09_baseline": {
            "machine_sha256": readerqa.BASELINE_WITNESSES[QA / "UNITS_01_09_MACHINE_QA.json"][1],
            "visual_sha256": readerqa.BASELINE_WITNESSES[QA / "UNITS_01_09_VISUAL_QA.json"][1],
            "responsive_sha256": readerqa.BASELINE_WITNESSES[QA / "UNITS_01_09_RESPONSIVE_QA.json"][1],
            "protected_sha256": readerqa.BASELINE_WITNESSES[QA / "UNIT_09_PROTECTED_SURFACES.json"][1],
            "qa_script_sha256": readerqa.BASELINE_WITNESSES[ROOT / "scripts" / "qa_reader_units_01_09.py"][1],
        },
        "units_10_12": units,
        "topology": {
            "new_source_ids": len(all_new_ids),
            "duplicate_new_source_ids": 0,
            "cumulative_source_ids": machine["stable_ids"],
            "new_exercises": 85,
            "cumulative_exercises": machine["exercise_count"],
            "new_public_solutions": 10,
            "cumulative_public_solutions": machine["public_solution_count"],
            "invented_solutions": 0,
            "untranslated_german_prose": 0,
            "placeholder_markers": 0,
            "credential_markers": 0,
            "new_media_positions": 5,
            "new_binary_surfaces": 5,
        },
        "source_findings": findings,
        "corrections_ledger": corrections,
        "artifacts": {
            "build_receipt": {"path": rel(readerqa.BUILD_RECEIPT), "bytes": readerqa.BUILD_RECEIPT.stat().st_size, "sha256": base.digest(readerqa.BUILD_RECEIPT)},
            "html": {"path": rel(readerqa.HTML), "bytes": readerqa.HTML.stat().st_size, "sha256": base.digest(readerqa.HTML), "images": 65, "mathml_nodes": 4499},
            "pdf": {"path": rel(readerqa.PDF), "bytes": readerqa.PDF.stat().st_size, "sha256": base.digest(readerqa.PDF), "pages": readerqa.EXPECTED_PDF_PAGES},
        },
        "bound_qa": {
            "machine": {"path": rel(MACHINE), "bytes": MACHINE.stat().st_size, "sha256": base.digest(MACHINE)},
            "visual": {"path": rel(VISUAL), "bytes": VISUAL.stat().st_size, "sha256": base.digest(VISUAL)},
            "visual_page_manifest": visual["_page_manifest_binding"],
            "responsive": {"path": rel(RESPONSIVE), "bytes": RESPONSIVE.stat().st_size, "sha256": base.digest(RESPONSIVE)},
        },
        "qa_script": {"path": rel(Path(__file__)), "sha256": base.digest(Path(__file__))},
        "validation": {
            "authority_revision_transclusion_file_and_official_pdf_replay": True,
            "exercise_map_solution_witness_literal_star_and_no_invention_closure": True,
            "rights_asset_position_alt_text_credit_and_binary_hash_closure": True,
            "source_hash_ast_language_placeholder_secret_quirk_and_correction_binding": True,
            "stable_id_html_mathml_image_heading_link_alt_and_build_receipt_closure": True,
            "pdf_page_a4_font_text_and_all_page_visual_render_closure": True,
            "responsive_desktop_centering_mobile_overflow_and_browser_console_closure": True,
        },
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "receipt": rel(RECEIPT), "bytes": RECEIPT.stat().st_size, "sha256": base.digest(RECEIPT)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
