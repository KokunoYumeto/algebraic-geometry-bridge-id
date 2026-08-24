#!/usr/bin/env python3
"""Protect the cumulative Unit 15 release boundary for Units 13--15.

This audit binds the immutable Unit 12 baseline, replays the three new source
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
import qa_reader_units_01_15 as readerqa  # noqa: E402


base = readerqa.base
SOURCE = readerqa.SOURCE
QA = ROOT / "qa"
MACHINE = QA / "UNITS_01_15_MACHINE_QA.json"
VISUAL = QA / "UNITS_01_15_VISUAL_QA.json"
RESPONSIVE = QA / "UNITS_01_15_RESPONSIVE_QA.json"
RECEIPT = QA / "UNIT_15_PROTECTED_SURFACES.json"

FINDINGS = {
    13: (QA / "UNIT_13_TRANSLATION_QA.json", 4441, "f10a5fa657c17c17619edaaab7caa35a703c6c9f4b44e31ce7019aa28fbcc083"),
    14: (QA / "UNIT_14_TRANSLATION_QA.json", 3689, "ed727071ce0c91a334230049ee5f9eaa3d7fc42b54a64941c0da8c1fcc682e1d"),
    15: (QA / "UNIT_15_TRANSLATION_QA.json", 3905, "ed3425ed0c4b71ce9841e897eaf43e358aa468b38618306a94843a6a35da0ba4"),
}

UNIT_FILES = {
    13: (SOURCE / "lecture-13.md", SOURCE / "worksheet-13.md", SOURCE / "worksheet-13-solutions.md", SOURCE / "media-credits-unit-13.md"),
    14: (SOURCE / "lecture-14.md", SOURCE / "worksheet-14.md", SOURCE / "worksheet-14-solutions.md", SOURCE / "media-credits-unit-14.md"),
    15: (SOURCE / "lecture-15.md", SOURCE / "worksheet-15.md", SOURCE / "worksheet-15-solutions.md", SOURCE / "media-credits-unit-15.md"),
}
EXPECTED_UNIT_IDS = {13: 75, 14: 55, 15: 61}
EXPECTED_STARS = {
    13: [3, 6, 8, 9, 11, 14, 15, 17, 20, 21, 24, 27, 28, 31],
    14: [2, 7],
    15: [6, 9, 19, 22],
}


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
    u13_worksheet = (SOURCE / "worksheet-13.md").read_text(encoding="utf-8")
    u13_solutions = (SOURCE / "worksheet-13-solutions.md").read_text(encoding="utf-8")
    u14_solutions = (SOURCE / "worksheet-14-solutions.md").read_text(encoding="utf-8")
    u15_lecture = (SOURCE / "lecture-15.md").read_text(encoding="utf-8")
    u15_solutions = (SOURCE / "worksheet-15-solutions.md").read_text(encoding="utf-8")

    base.require("$R_i\\to R_i/(x_i)$" in u13_worksheet and "mengikuti konteks barisan" in u13_worksheet, "AGC-CORR-0028 indexed residue-map correction absent")
    base.require("V(g)=\\varnothing=V(1)" in u13_solutions and "Kedua himpunan nol yang dimaksud adalah" in u13_solutions, "AGC-CORR-0029 empty-zero-set correction absent")
    base.require("tanpa mengandaikan bahwa valuasi hasil kali tepat $n$" in u13_solutions, "AGC-CORR-0030 valuation correction absent")
    base.require("$t^2/(t-1)$ tanpa tanda minus" in u14_solutions and "Kutub di $t=1$" in u14_solutions, "AGC-CORR-0031 sign correction absent")
    base.require("sumber menulis $s_i\\in M$" in u15_lecture and "$s_i\\in M_i$" in u15_lecture, "AGC-CORR-0032 indexed-colimit correction absent")
    base.require("h_i\\bigl(\\varphi(r_i)-\\varphi(g_i)x_i\\bigr)=0" in u15_solutions, "AGC-CORR-0033 localization equality absent")
    base.require("langkah pembatalan $h_i$" in u15_solutions and "karena hipotesis menyatakan bahwa $S$ integral" in u15_solutions, "AGC-CORR-0033 integrality cancellation note absent")

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
        "protected_correction_surfaces_replayed": 6,
    }


def verify_findings() -> dict:
    result = {}
    for unit, (path, expected_bytes, expected_hash) in FINDINGS.items():
        require_regular(path)
        base.require(path.stat().st_size == expected_bytes, f"Unit {unit} finding bytes")
        base.require(base.digest(path) == expected_hash, f"Unit {unit} finding hash")
        evidence = json.loads(path.read_text(encoding="utf-8"))
        base.require(evidence.get("status") == "PASS" and evidence.get("unit") == unit, f"Unit {unit} translation receipt status/scope")
        base.require(evidence.get("provenance") == "OpenAI Codex gpt-5.6-sol, Ultra.", f"Unit {unit} exact provenance")
        base.require(evidence.get("authority", {}).get("manifest_sha256") == readerqa.UNIT_SPEC[unit]["manifest_sha256"], f"Unit {unit} translation/authority binding")
        base.require(evidence.get("translation", {}).get("exercises") == readerqa.UNIT_SPEC[unit]["exercises"], f"Unit {unit} translation exercise topology")
        base.require(evidence.get("translation", {}).get("public_solutions") == readerqa.UNIT_SPEC[unit]["solutions"], f"Unit {unit} translation solution topology")
        result[f"unit_{unit:02d}"] = {"path": rel(path), "bytes": expected_bytes, "sha256": expected_hash}
    return result


def verify_machine() -> dict:
    require_regular(MACHINE)
    machine = json.loads(MACHINE.read_text(encoding="utf-8"))
    base.require(machine.get("schema") == "ag-bridge-machine-qa-receipt-v4", "Unit 15 machine schema")
    base.require(machine.get("status") == "PASS" and machine.get("through_unit") == 15, "Unit 15 machine QA is not PASS")
    base.require(machine.get("stable_ids") == 861 and machine.get("exercise_count") == 423 and machine.get("public_solution_count") == 75, "machine cumulative topology")
    base.require(machine.get("units_01_12_baseline", {}).get("protected_sha256") == readerqa.BASELINE_WITNESSES[QA / "UNIT_12_PROTECTED_SURFACES.json"][1], "machine Unit 12 baseline binding")
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
    base.require(machine["html"]["images"] == 69 and machine["html"]["mathml_nodes"] == 5989, "machine HTML topology")
    base.require(machine["pdf"]["sha256"] == readerqa.FROZEN_BUILD["pdf"]["sha256"] and machine["pdf"]["bytes"] == readerqa.FROZEN_BUILD["pdf"]["bytes"], "machine PDF identity")
    base.require(machine["pdf"]["pages"] == readerqa.EXPECTED_PDF_PAGES, "machine PDF page count")
    base.require(machine["build_receipt"]["sha256"] == readerqa.FROZEN_BUILD["receipt"]["sha256"], "machine build-receipt identity")
    current_script_hash = base.digest(ROOT / "scripts" / "qa_reader_units_01_15.py")
    base.require(machine["qa_script"] == {"path": "scripts/qa_reader_units_01_15.py", "sha256": current_script_hash}, "machine QA script identity")
    return machine


def verify_visual(machine: dict) -> dict:
    require_regular(VISUAL)
    visual = json.loads(VISUAL.read_text(encoding="utf-8"))
    base.require(visual.get("schema") == "ag-bridge-visual-qa-v1" and visual.get("status") == "PASS", "Unit 15 visual QA is not PASS")
    scope = visual.get("scope", {})
    base.require(scope.get("through_unit") == 15 and scope.get("language") == "id-ID", "visual scope/language")
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
    base.require(len(contact_sheets) == 14 and contact_sheets[0] == "pages 1-20" and contact_sheets[-1] == "pages 261-267", "visual contact-sheet all-page review absent")
    full_size = set(review.get("full_size_pages_checked", []))
    base.require({216, 220, 238, 249, 252, 261, 267} <= full_size, "visual affected-page full-size review absent")
    resolved = json.dumps(visual.get("findings_resolved_before_freeze", []), ensure_ascii=False)
    base.require("solution 15.6" in resolved and "page 261" in resolved, "visual resolved-finding binding absent")
    visual["_page_manifest_binding"] = manifest_row
    return visual


def verify_responsive(machine: dict) -> dict:
    require_regular(RESPONSIVE)
    responsive = json.loads(RESPONSIVE.read_text(encoding="utf-8"))
    base.require(responsive.get("status") == "PASS" and responsive.get("through_unit") == 15, "Unit 15 responsive QA is not PASS")
    artifact = responsive.get("artifact", {})
    base.require(artifact.get("path") == rel(readerqa.HTML), "responsive HTML path")
    base.require(artifact.get("bytes") == machine["html"]["bytes"] and artifact.get("sha256") == machine["html"]["sha256"], "responsive HTML byte identity")
    base.require(artifact.get("title") == "Kurva Aljabar - Unit 1-15" and artifact.get("language") == "id-ID", "responsive HTML title/language")
    base.require(artifact.get("mathml_nodes") == 5989 and artifact.get("images") == 69, "responsive HTML topology")
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
        "desktop_body_centered", "mobile_math_overflow_is_contained", "desktop_unit_15_screenshot_reviewed", "mobile_unit_15_screenshot_reviewed",
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
    base.require(len(all_new_ids) == len(set(all_new_ids)) == 191, "Units 13--15 stable-ID closure")
    units = {f"unit_{unit:02d}": topology_for_unit(unit, spec) for unit, spec in readerqa.UNIT_SPEC.items()}
    base.require(sum(row["exercises"] for row in units.values()) == 93, "Units 13--15 exercise count")
    base.require(sum(row["public_solutions"] for row in units.values()) == 20, "Units 13--15 public-solution count")
    base.require(sum(row["media_positions"] for row in units.values()) == 4, "Units 13--15 media-position count")

    corrections = verify_source_quirks()
    findings = verify_findings()
    machine = verify_machine()
    visual = verify_visual(machine)
    responsive = verify_responsive(machine)

    build = json.loads(readerqa.BUILD_RECEIPT.read_text(encoding="utf-8"))
    base.require(build.get("through_unit") == 15 and base.digest(readerqa.BUILD_RECEIPT) == readerqa.FROZEN_BUILD["receipt"]["sha256"], "protected build receipt boundary")
    outputs = {row["path"]: row for row in build["outputs"]}
    base.require(outputs[rel(readerqa.HTML)]["sha256"] == machine["html"]["sha256"] == responsive["artifact"]["sha256"], "HTML cross-receipt identity")
    base.require(outputs[rel(readerqa.PDF)]["sha256"] == machine["pdf"]["sha256"] == visual["scope"]["pdf_sha256"], "PDF cross-receipt identity")

    receipt = {
        "schema": "ag-bridge-protected-surface-audit-v3",
        "status": "PASS",
        "unit": 15,
        "scope": "cumulative release boundary; direct replay of Units 13--15 over frozen Units 1--12 baseline",
        "units_01_12_baseline": {
            "machine_sha256": readerqa.BASELINE_WITNESSES[QA / "UNITS_01_12_MACHINE_QA.json"][1],
            "visual_sha256": readerqa.BASELINE_WITNESSES[QA / "UNITS_01_12_VISUAL_QA.json"][1],
            "responsive_sha256": readerqa.BASELINE_WITNESSES[QA / "UNITS_01_12_RESPONSIVE_QA.json"][1],
            "protected_sha256": readerqa.BASELINE_WITNESSES[QA / "UNIT_12_PROTECTED_SURFACES.json"][1],
            "qa_script_sha256": readerqa.BASELINE_WITNESSES[ROOT / "scripts" / "qa_reader_units_01_12.py"][1],
        },
        "units_13_15": units,
        "topology": {
            "new_source_ids": len(all_new_ids),
            "duplicate_new_source_ids": 0,
            "cumulative_source_ids": machine["stable_ids"],
            "new_exercises": 93,
            "cumulative_exercises": machine["exercise_count"],
            "new_public_solutions": 20,
            "cumulative_public_solutions": machine["public_solution_count"],
            "invented_solutions": 0,
            "untranslated_german_prose": 0,
            "placeholder_markers": 0,
            "credential_markers": 0,
            "new_media_positions": 4,
            "new_binary_surfaces": 7,
        },
        "source_findings": findings,
        "corrections_ledger": corrections,
        "artifacts": {
            "build_receipt": {"path": rel(readerqa.BUILD_RECEIPT), "bytes": readerqa.BUILD_RECEIPT.stat().st_size, "sha256": base.digest(readerqa.BUILD_RECEIPT)},
            "html": {"path": rel(readerqa.HTML), "bytes": readerqa.HTML.stat().st_size, "sha256": base.digest(readerqa.HTML), "images": 69, "mathml_nodes": 5989},
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
