#!/usr/bin/env python3
"""Freeze the fail-closed cumulative Unit 28 release candidate.

The script is deliberately offline.  ``--self-check`` validates and renders the
candidate in memory; ``--write`` is the only mode that mutates the candidate
receipt.  It never reads credentials and never performs a network operation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "qa" / "UNIT_28_RELEASE_CANDIDATE.json"
TITLE = "Kurva Aljabar — Edisi Bahasa Indonesia"
PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."
THROUGH_UNIT = 28
PLANNED_UNITS = 30
PREVIOUS_ZENODO_RECORD = 22104692
CONCEPT_DOI = "10.5281/zenodo.22059686"
TARGET_TAG = "unit-28"

PDF_PATH = "build/reader-id/algebraic-geometry-bridge-id-units-01-28.pdf"
HTML_PATH = "build/reader-id/index.html"
BUILD_RECEIPT_PATH = "build/reader-id/BUILD_RECEIPT.json"
MACHINE_QA_PATH = "qa/UNITS_01_28_MACHINE_QA.json"
VISUAL_QA_PATH = "qa/UNITS_01_28_VISUAL_QA.json"
RESPONSIVE_QA_PATH = "qa/UNITS_01_28_RESPONSIVE_QA.json"
PROTECTED_QA_PATH = "qa/UNIT_28_PROTECTED_SURFACES.json"
BACKEND_QA_PATH = "qa/UNITS_01_28_BACKEND_QA.json"
TRANSLATION_QA_PATH = "qa/UNIT_28_TRANSLATION_QA.json"
BACKEND_MANIFEST_PATH = "backend/units-01-28/MANIFEST.json"
BACKEND_RECORDS_PATH = "backend/units-01-28/records.jsonl"
COMMON_GENERATOR_PATH = "scripts/generate_common_backend_v1_receipts.py"
COMMON_GENERATOR_SHA256 = "cd868864d84479238ef27b8475ada68bcf20cac0cd2c154dabadcd68f6089574"

EXPECTED_READER = {
    "pdf_pages": 476,
    "exercises": 671,
    "public_source_solutions": 118,
    "reader_media_positions": 98,
    "stable_source_ids": 1483,
    "mathml_nodes": 10717,
}
EXPECTED_PDF = {
    "bytes": 15820212,
    "sha256": "181b6fba2b5441fb7a5ab76a512e9d9ee2300e4201fd4632cac20a70bc703df6",
}
EXPECTED_HTML = {
    "bytes": 23412216,
    "sha256": "b7cef9e6c08b696bde2f875a4766e6c35e975d4fd0901e414c3896014bbd9c10",
}
EXPECTED_BUILD = {
    "bytes": 43674,
    "sha256": "5a843fdc6cb79ab3329e1f316027968e14ab2a0b765ff3505ad2af85003df5c3",
}
UNIT_27_BASELINE_RECORDS = 20570


def exact(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise RuntimeError(f"Path escapes the task root: {relative}") from exc
    if not path.is_file():
        raise FileNotFoundError(path)
    return path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def descriptor(relative: str) -> dict[str, object]:
    path = exact(relative)
    return {"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)}


def load_json(relative: str) -> dict:
    path = exact(relative)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Invalid JSON object at {relative}: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"Expected a JSON object at {relative}")
    return value


def require_equal(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise RuntimeError(f"{label}: {actual!r} != {expected!r}")


def require_pass(value: dict, label: str) -> None:
    status = value.get("status", value.get("result"))
    if not isinstance(status, str) or not status.upper().startswith("PASS"):
        raise RuntimeError(f"{label} is not PASS: {status!r}")


def require_descriptor(value: object, relative: str, label: str) -> None:
    if not isinstance(value, dict):
        raise RuntimeError(f"{label} descriptor is missing")
    wanted = descriptor(relative)
    for key in ("path", "bytes", "sha256"):
        require_equal(value.get(key), wanted[key], f"{label} {key}")


def authority_descriptor(number: int) -> dict[str, object]:
    prefix = f"authority/wikiversity/unit-{number:02d}"
    manifest_path = f"{prefix}/UNIT_AUTHORITY_MANIFEST.json"
    manifest = load_json(manifest_path)
    lecture = manifest.get("lecture")
    worksheet = manifest.get("worksheet")
    if not isinstance(lecture, dict) or not isinstance(worksheet, dict):
        raise RuntimeError(f"Unit {number} authority roots are missing")
    for label, root in (("lecture", lecture), ("worksheet", worksheet)):
        revid = root.get("revid")
        if not isinstance(revid, int) or isinstance(revid, bool) or revid <= 0:
            raise RuntimeError(f"Unit {number} {label} revision is invalid")
    return {
        "manifest": {
            **descriptor(manifest_path),
            "lecture_revid": lecture["revid"],
            "worksheet_revid": worksheet["revid"],
        },
        "exercise_map_sha256": descriptor(f"{prefix}/ORDERED_EXERCISE_MAP.json")["sha256"],
        "rights_sha256": descriptor(f"authority/RIGHTS-unit-{number:02d}.csv")["sha256"],
        "asset_closure_sha256": descriptor(
            f"authority/ASSET_CLOSURE-unit-{number:02d}.json"
        )["sha256"],
    }


def common_preflight(record_count: int) -> dict:
    """Run the accepted adapter's no-write preflight against Unit 28.

    The frozen migration receipt deliberately requires a reserved public DOI,
    so it cannot be an input to the pre-reservation release candidate.  This
    direct deterministic preflight proves the same adapter/reverse/FK facts
    without reading credentials, touching the network, or writing receipts.
    """

    generator = descriptor(COMMON_GENERATOR_PATH)
    require_equal(generator["sha256"], COMMON_GENERATOR_SHA256, "common-adapter generator hash")
    command = [
        sys.executable,
        str(exact(COMMON_GENERATOR_PATH)),
        "--native-backend",
        str((ROOT / "backend" / "units-01-28").resolve()),
        "--preflight",
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=300,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise RuntimeError(f"Common-backend Unit 28 preflight failed: {detail[-2000:]}")
    try:
        value = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Common-backend preflight returned invalid JSON") from exc
    if not isinstance(value, dict):
        raise RuntimeError("Common-backend preflight did not return an object")
    require_equal(value.get("status"), "PASS", "common-backend preflight status")
    require_equal(value.get("native_records"), record_count, "common-backend native records")
    common_records = value.get("common_records")
    virtual_bytes = value.get("virtual_bytes")
    virtual_sha = value.get("virtual_sha256")
    foreign_keys = value.get("foreign_keys_checked")
    if not isinstance(common_records, int) or isinstance(common_records, bool) or common_records <= record_count:
        raise RuntimeError("Common-backend preflight record count is invalid")
    if not isinstance(virtual_bytes, int) or isinstance(virtual_bytes, bool) or virtual_bytes <= 0:
        raise RuntimeError("Common-backend preflight virtual byte count is invalid")
    if not isinstance(virtual_sha, str) or len(virtual_sha) != 64:
        raise RuntimeError("Common-backend preflight virtual hash is invalid")
    require_equal(value.get("reverse_sha256"), descriptor(BACKEND_RECORDS_PATH)["sha256"], "common-backend reverse hash")
    if not isinstance(foreign_keys, int) or isinstance(foreign_keys, bool) or foreign_keys <= 0:
        raise RuntimeError("Common-backend preflight foreign-key count is invalid")
    if not isinstance(value.get("strict_profiles"), int) or value["strict_profiles"] <= 0:
        raise RuntimeError("Common-backend strict source-profile coverage is empty")
    return {**value, "generator": generator}


def assemble() -> dict:
    build = load_json(BUILD_RECEIPT_PATH)
    require_equal(build.get("through_unit"), THROUGH_UNIT, "build boundary")
    require_equal(build.get("language"), "id-ID", "build language")
    require_equal(descriptor(BUILD_RECEIPT_PATH)["bytes"], EXPECTED_BUILD["bytes"], "build bytes")
    require_equal(descriptor(BUILD_RECEIPT_PATH)["sha256"], EXPECTED_BUILD["sha256"], "build sha256")

    pdf = descriptor(PDF_PATH)
    html = descriptor(HTML_PATH)
    for key, wanted in EXPECTED_PDF.items():
        require_equal(pdf[key], wanted, f"PDF {key}")
    for key, wanted in EXPECTED_HTML.items():
        require_equal(html[key], wanted, f"HTML {key}")

    machine = load_json(MACHINE_QA_PATH)
    require_pass(machine, "machine QA")
    require_equal(machine.get("through_unit"), THROUGH_UNIT, "machine QA boundary")
    require_equal(machine.get("language"), "id-ID", "machine QA language")
    require_descriptor(machine.get("pdf"), PDF_PATH, "machine PDF")
    require_descriptor(machine.get("html"), HTML_PATH, "machine HTML")
    require_descriptor(machine.get("build_receipt"), BUILD_RECEIPT_PATH, "machine build receipt")
    machine_coverage = machine.get("coverage")
    if not isinstance(machine_coverage, dict):
        raise RuntimeError("Machine QA coverage is missing")
    for key in (
        "exercises",
        "public_source_solutions",
        "reader_media_positions",
        "stable_source_ids",
        "mathml_nodes",
    ):
        require_equal(machine_coverage.get(key), EXPECTED_READER[key], f"machine coverage {key}")
    require_equal(((machine.get("pdf") or {}).get("pages")), EXPECTED_READER["pdf_pages"], "PDF pages")

    qa_specs = (
        ("visual", VISUAL_QA_PATH),
        ("responsive", RESPONSIVE_QA_PATH),
        ("protected_surfaces", PROTECTED_QA_PATH),
        ("backend", BACKEND_QA_PATH),
        ("translation", TRANSLATION_QA_PATH),
    )
    qa_values: dict[str, dict] = {}
    for key, relative in qa_specs:
        value = load_json(relative)
        require_pass(value, f"{key} QA")
        boundary = value.get("through_unit", value.get("unit"))
        require_equal(boundary, THROUGH_UNIT, f"{key} QA boundary")
        qa_values[key] = value

    visual = qa_values["visual"]
    require_descriptor(visual.get("pdf"), PDF_PATH, "visual PDF")
    require_equal(((visual.get("pdf") or {}).get("pages")), EXPECTED_READER["pdf_pages"], "visual pages")
    raster = visual.get("deterministic_raster")
    inspection = visual.get("visual_inspection")
    if not isinstance(raster, dict) or not isinstance(inspection, dict):
        raise RuntimeError("Visual QA lacks raster or inspection evidence")
    require_equal(raster.get("page_png_count"), EXPECTED_READER["pdf_pages"], "visual raster page count")
    require_equal(inspection.get("contact_sheet_count"), 24, "visual contact-sheet count")
    sheets = inspection.get("all_page_contact_sheets")
    if not isinstance(sheets, list) or len(sheets) != 24:
        raise RuntimeError("Visual QA must bind all 24 contact sheets")

    translation = qa_values["translation"]
    cumulative = translation.get("cumulative_source")
    if not isinstance(cumulative, dict):
        raise RuntimeError("Translation QA cumulative coverage is missing")
    for key in ("exercises", "public_solutions", "media_positions"):
        wanted_key = {
            "exercises": "exercises",
            "public_solutions": "public_source_solutions",
            "media_positions": "reader_media_positions",
        }[key]
        require_equal(cumulative.get(key), EXPECTED_READER[wanted_key], f"translation coverage {key}")

    backend_manifest = load_json(BACKEND_MANIFEST_PATH)
    backend_qa = qa_values["backend"]
    require_equal(backend_manifest.get("through_unit"), THROUGH_UNIT, "backend manifest boundary")
    record_count = backend_manifest.get("record_count")
    if not isinstance(record_count, int) or isinstance(record_count, bool) or record_count <= UNIT_27_BASELINE_RECORDS:
        raise RuntimeError("Unit 28 backend record count does not extend the Unit 27 baseline")
    backend_section = backend_qa.get("backend")
    if not isinstance(backend_section, dict):
        raise RuntimeError("Backend QA descriptor is missing")
    require_equal(backend_section.get("record_count"), record_count, "backend QA record count")
    require_equal(
        backend_section.get("units_01_27_baseline_record_count"),
        UNIT_27_BASELINE_RECORDS,
        "Unit 27 backend baseline count",
    )
    require_equal(
        backend_section.get("units_01_27_baseline_records_exactly_preserved"),
        True,
        "Unit 27 backend byte preservation",
    )
    require_equal(backend_section.get("manifest_sha256"), descriptor(BACKEND_MANIFEST_PATH)["sha256"], "backend manifest hash")
    require_equal(backend_section.get("records_sha256"), descriptor(BACKEND_RECORDS_PATH)["sha256"], "backend records hash")

    preflight = common_preflight(record_count)

    authority = {
        f"unit_{number:02d}": authority_descriptor(number)
        for number in (25, 26, 27, 28)
    }
    qa = {
        key: {
            **descriptor(relative),
            "status": "PASS",
        }
        for key, relative in (
            ("machine", MACHINE_QA_PATH),
            ("visual", VISUAL_QA_PATH),
            ("responsive", RESPONSIVE_QA_PATH),
            ("protected_surfaces", PROTECTED_QA_PATH),
            ("backend", BACKEND_QA_PATH),
            ("translation", TRANSLATION_QA_PATH),
        )
    }
    return {
        "schema": "ag-bridge-release-candidate-v3",
        "frozen_date": "2026-08-26",
        "status": "PASS_RELEASE_READY",
        "release_state": "verified_cumulative_checkpoint_ready_for_existing_github_and_zenodo_lineages",
        "through_unit": THROUGH_UNIT,
        "planned_classical_units": PLANNED_UNITS,
        "classical_volume_complete": False,
        "full_two_volume_edition_complete": False,
        "language": "id-ID",
        "title": TITLE,
        "model_provenance": PROVENANCE,
        "source_course_boundary": {
            "units_01_23": "Algebraische Kurven (Osnabrück 2025–2026)",
            "units_24_28": "Algebraische Kurven (Osnabrück 2012)",
        },
        "authority": authority,
        "reader": {
            "html": html,
            "pdf": {**pdf, "pages": EXPECTED_READER["pdf_pages"]},
            "build_receipt": descriptor(BUILD_RECEIPT_PATH),
        },
        "coverage": {
            "lectures": THROUGH_UNIT,
            "worksheets": THROUGH_UNIT,
            "exercises": EXPECTED_READER["exercises"],
            "public_source_solutions": EXPECTED_READER["public_source_solutions"],
            "reader_media_positions": EXPECTED_READER["reader_media_positions"],
            "native_backend_records": record_count,
            "stable_source_ids": EXPECTED_READER["stable_source_ids"],
            "mathml_nodes": EXPECTED_READER["mathml_nodes"],
        },
        "qa": qa,
        "backend": {
            "native_manifest": descriptor(BACKEND_MANIFEST_PATH),
            "native_records": {**descriptor(BACKEND_RECORDS_PATH), "records": record_count},
            "unit_27_records_preserved": UNIT_27_BASELINE_RECORDS,
            "deterministic_double_replay": True,
            "common_adapter_preflight": {
                "status": "PASS",
                "virtual_records": preflight["common_records"],
                "virtual_bytes": preflight["virtual_bytes"],
                "virtual_sha256": preflight["virtual_sha256"],
                "foreign_keys_checked": preflight["foreign_keys_checked"],
                "native_reverse_sha256": preflight["reverse_sha256"],
                "strict_profiles": preflight["strict_profiles"],
                "generator": preflight["generator"],
            },
        },
        "rights": {
            "translated_text": "CC BY-SA 4.0",
            "units_24_28_pdf_component_notices": [
                "CC BY-SA 4.0 course route",
                "CC BY-SA 2.0 Germany file notice",
            ],
            "media": "per-component rights in authority/RIGHTS*.csv and reader credits",
            "blanket_file_set_license_claimed": False,
            "license_notice": "LICENSE.md",
            "non_endorsed_independent_derivative": True,
        },
        "publication": {
            "zenodo": {
                "state": "publication_due_to_existing_concept",
                "concept_doi": CONCEPT_DOI,
                "previous_record_id": PREVIOUS_ZENODO_RECORD,
            },
            "github": {
                "state": "publication_due_after_package",
                "repository": "https://github.com/KokunoYumeto/algebraic-geometry-bridge-id",
                "reader": "https://kokunoyumeto.github.io/algebraic-geometry-bridge-id/",
                "target_tag": TARGET_TAG,
            },
        },
        "checks": {
            "authority_solution_media_rights_closure": True,
            "translation_and_math_fidelity": True,
            "machine_visual_responsive_and_accessibility_qa": True,
            "native_backend_schema_closure_and_replay": True,
            "common_backend_v1_adapter_preflight": True,
            "credential_findings": 0,
            "ready_for_packaging": True,
            "ready_for_publication": True,
        },
        "next_action": (
            "Reserve the Unit 28 identity in the existing Zenodo concept, update public metadata "
            "to the reserved DOI, finalize the common-adapter receipt, create the deterministic "
            "eight-file reader-first package, publish in the existing Zenodo and GitHub lineages, "
            "and anonymously verify every public byte."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if sum((args.self_check, args.write)) != 1:
        raise SystemExit("Choose exactly one of --self-check or --write")
    candidate = assemble()
    if args.write:
        encoded = (json.dumps(candidate, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        OUT.write_bytes(encoded)
        reread = json.loads(OUT.read_text(encoding="utf-8"))
        require_equal(reread, candidate, "release-candidate readback")
    print(
        json.dumps(
            {
                "status": candidate["status"],
                "mode": "write" if args.write else "offline_self_check",
                "through_unit": candidate["through_unit"],
                "pdf_pages": candidate["reader"]["pdf"]["pages"],
                "backend_records": candidate["coverage"]["native_backend_records"],
                "credential_read": False,
                "network_called": False,
                "written": args.write,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
