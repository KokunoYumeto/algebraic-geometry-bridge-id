#!/usr/bin/env python3
"""Fail-closed validation for the bounded Brenner Unit 10 authority freeze."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "authority" / "wikiversity" / "unit-10"
MANIFEST = UNIT / "UNIT_AUTHORITY_MANIFEST.json"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-10.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-10.json"

EXPECTED_ENTRY_PAGES = {
    "lecture": (165899, 1051326, "2635c363f022af1e0603447bbac65bfe71e87a46"),
    "worksheet": (165929, 1058833, "48ce873997cecbd45efdceb3a7caa19ae7844876"),
    "lecture_latex_page": (165963, 1033009, "3034e92c1843eab298fb5f6f859d2c89cf824d61"),
    "worksheet_latex_page": (166023, 1033070, "3034e92c1843eab298fb5f6f859d2c89cf824d61"),
}
EXPECTED_SOLUTIONS = {
    1: (94256, 1028855, "ed7778bb9e4ae4c8143d0c5edfa33c8c35174e43"),
    6: (168416, 1068028, "ffd73f9cb31684103b33ed555d18ddedb77932dd"),
    9: (168494, 1068729, "bfc7a4368e1e7cf96765696334b203d54f07eeca"),
    16: (95372, 536882, "bacb8c40cce1f4a3ce263c1c81b99e22938bebba"),
    17: (140640, 743216, "645850e5fecf8070bedbcc98ff412c1ba55c2f2b"),
    20: (94501, 1112824, "50fbb7db8fd9440bfd88f11c0d88234c21d5d949"),
}
EXPECTED_PDFS = {
    "authority/artifacts/lecture-10-official.pdf":
        (173582, "50f5778d50807cf2e6516704f8a9014ffe1af636", 7),
    "authority/artifacts/worksheet-10-official.pdf":
        (149763, "7940beb2b3221802e3720ebd95f472c3054fd118", 7),
}
EXPECTED_PDF_DESCRIPTION_PAGES = {
    "Algebraische Kurven (Osnabrück 2025-2026)Arbeitsblatt10.pdf":
        (176180248, 1219479109, "216d99422baf871bb9ae231efa3e52b4cf705ab3"),
    "Algebraische Kurven (Osnabrück 2025-2026)Vorlesung10.pdf":
        (178261723, 1158228042, "1fe3471dd35b59a6cf6ab4ba5d9ff4922cde3439"),
}


def digest(path: Path, algorithm: str = "sha256") -> str:
    value = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def load(path: Path) -> dict:
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"Missing/non-regular required file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    manifest = load(MANIFEST)
    if manifest.get("schema") != "brenner-unit-authority-freeze-v2":
        raise RuntimeError("Unit 10 manifest schema is not v2")
    if manifest.get("unit_number") != 10:
        raise RuntimeError("Authority manifest is not Unit 10")
    if manifest.get("source_api") != "https://de.wikiversity.org/w/api.php":
        raise RuntimeError("Authority manifest source API drifted")

    for key, expected in EXPECTED_ENTRY_PAGES.items():
        row = manifest.get(key, {})
        actual = (row.get("pageid"), row.get("revid"), row.get("mediawiki_sha1"))
        if actual != expected:
            raise RuntimeError(f"Frozen {key} identity drifted: {actual!r}")

    for name, expected_count in (
        ("lecture_transclusion_closure", 124),
        ("worksheet_transclusion_closure", 154),
    ):
        row = manifest.get(name, {})
        counts = (
            row.get("requested_template_count"),
            row.get("captured_page_count"),
            row.get("missing_page_count"),
        )
        if counts != (expected_count, expected_count, 0):
            raise RuntimeError(f"Incomplete {name}: {counts!r}")
        titles = [item.get("title") for item in row.get("pages", [])]
        if len(titles) != len(set(titles)) or len(titles) != expected_count:
            raise RuntimeError(f"Non-unique {name} page closure")

    solutions = manifest.get("solutions", {})
    if solutions.get("exercise_count") != 29 or solutions.get("solution_count") != 6:
        raise RuntimeError("Unit 10 exercise/solution cardinality drifted")
    entries = solutions.get("entries", [])
    if [item.get("exercise_number") for item in entries] != list(range(1, 30)):
        raise RuntimeError("Unit 10 ordered exercise topology is not 1..29")
    public = {item["exercise_number"]: item for item in entries if item.get("has_public_solution")}
    if set(public) != set(EXPECTED_SOLUTIONS):
        raise RuntimeError(f"Unexpected public-solution set: {sorted(public)!r}")
    for number, expected in EXPECTED_SOLUTIONS.items():
        row = public[number]
        actual = (row.get("pageid"), row.get("revid"), row.get("mediawiki_sha1"))
        if actual != expected:
            raise RuntimeError(f"Public solution {number} identity drifted: {actual!r}")
        for file_key, bytes_key, hash_key in (
            ("xml_file", "xml_bytes", "xml_sha256"),
            ("html_file", "html_bytes", "html_sha256"),
        ):
            path = UNIT / row[file_key]
            if path.stat().st_size != row[bytes_key] or digest(path) != row[hash_key]:
                raise RuntimeError(f"Public solution {number} {file_key} mismatch")

    manifest_rows = manifest.get("files", [])
    row_by_name = {row.get("file"): row for row in manifest_rows}
    actual_names = {
        path.name for path in UNIT.iterdir()
        if path.is_file() and path != MANIFEST
    }
    if set(row_by_name) != actual_names or len(row_by_name) != len(manifest_rows):
        raise RuntimeError("Manifest file inventory is incomplete, duplicated, or stale")
    for name, row in row_by_name.items():
        path = UNIT / name
        if path.stat().st_size != row.get("bytes") or digest(path) != row.get("sha256"):
            raise RuntimeError(f"Manifest-bound witness mismatch: {name}")

    official = manifest.get("official_pdf_witnesses", [])
    official_by_path = {item.get("local_path"): item for item in official}
    if set(official_by_path) != set(EXPECTED_PDFS):
        raise RuntimeError("Official PDF manifest inventory drifted")
    pdf_summary: list[dict] = []
    for local_name, (expected_bytes, expected_sha1, expected_pages) in EXPECTED_PDFS.items():
        path = ROOT / local_name
        row = official_by_path[local_name]
        if path.stat().st_size != expected_bytes or digest(path, "sha1") != expected_sha1:
            raise RuntimeError(f"Official PDF Commons identity mismatch: {local_name}")
        if row.get("local_bytes") != expected_bytes or row.get("mediawiki_sha1") != expected_sha1:
            raise RuntimeError(f"Official PDF manifest facts mismatch: {local_name}")
        if digest(path) != row.get("local_sha256"):
            raise RuntimeError(f"Official PDF SHA-256 mismatch: {local_name}")
        page_count = len(PdfReader(path).pages)
        if page_count != expected_pages:
            raise RuntimeError(f"Official PDF page count mismatch: {local_name}")
        pdf_summary.append(
            {
                "file": local_name,
                "bytes": expected_bytes,
                "sha1": expected_sha1,
                "sha256": digest(path),
                "pages": page_count,
            }
        )

    closure = load(CLOSURE)
    if (
        closure.get("unit") != 10
        or closure.get("reader_media_positions") != 0
        or closure.get("unique_local_assets") != 0
        or closure.get("assets") != []
        or closure.get("rights_rows") != 0
    ):
        raise RuntimeError("Unit 10 zero-reader-media closure drifted")
    with RIGHTS.open("r", encoding="utf-8", newline="") as stream:
        rights_rows = list(csv.DictReader(stream))
    if rights_rows:
        raise RuntimeError("Unit 10 rights CSV must contain no reader-media rows")
    if closure.get("rights_bytes") != RIGHTS.stat().st_size or closure.get("rights_sha256") != digest(RIGHTS):
        raise RuntimeError("Unit 10 rights CSV binding drifted")
    rights_rows = closure.get("official_pdf_component_rights", [])
    rights_by_title = {row.get("source_file_title"): row for row in rights_rows}
    if set(rights_by_title) != set(EXPECTED_PDF_DESCRIPTION_PAGES):
        raise RuntimeError("Official PDF component-rights closure drifted")
    for title, expected in EXPECTED_PDF_DESCRIPTION_PAGES.items():
        row = rights_by_title[title]
        actual = (
            row.get("description_pageid"),
            row.get("description_revid"),
            row.get("description_mediawiki_sha1"),
        )
        if actual != expected:
            raise RuntimeError(f"Official PDF description-page identity drifted: {title!r}")
        if (
            row.get("license_short") != "CC BY-SA 4.0"
            or row.get("license_url") != "https://creativecommons.org/licenses/by-sa/4.0"
            or row.get("attribution_required") is not True
            or "Bocardodarapti" not in row.get("artist", "")
        ):
            raise RuntimeError(f"Official PDF component rights drifted: {title!r}")
        if row.get("printed_pdf_footer_license_text") != "CC-by-sa 3.0":
            raise RuntimeError(f"Printed PDF licence discrepancy was not preserved: {title!r}")
    discrepancy = closure.get("license_discrepancy", {})
    if (
        discrepancy.get("status") != "RECORDED"
        or discrepancy.get("downstream_component_license") != "CC BY-SA 4.0"
        or discrepancy.get("printed_pdf_footer") != "CC-by-sa 3.0"
    ):
        raise RuntimeError("Unit 10 PDF licence discrepancy resolution drifted")
    commons_metadata = ROOT / closure.get("commons_component_rights_metadata_file", "")
    if (
        commons_metadata.stat().st_size != closure.get("commons_component_rights_metadata_bytes")
        or digest(commons_metadata) != closure.get("commons_component_rights_metadata_sha256")
    ):
        raise RuntimeError("Commons PDF component-rights witness binding drifted")

    forbidden = ("access_token", "api_token", "bearer ", "github_pat_", "ghp_")
    manifest_text = MANIFEST.read_text(encoding="utf-8").lower()
    if any(marker in manifest_text for marker in forbidden):
        raise RuntimeError("Credential-like material appears in the authority manifest")

    unit_files = [path for path in UNIT.iterdir() if path.is_file()]
    result = {
        "result": "PASS",
        "unit": 10,
        "lecture_revid": 1051326,
        "worksheet_revid": 1058833,
        "lecture_transclusions": 124,
        "worksheet_transclusions": 154,
        "exercises": 29,
        "public_solutions": 6,
        "public_solution_exercises": sorted(EXPECTED_SOLUTIONS),
        "reader_media_positions": 0,
        "official_pdfs": pdf_summary,
        "unit_witness_files": len(unit_files),
        "unit_witness_bytes": sum(path.stat().st_size for path in unit_files),
        "manifest_bytes": MANIFEST.stat().st_size,
        "manifest_sha256": digest(MANIFEST),
        "ordered_map_bytes": (UNIT / "ORDERED_EXERCISE_MAP.json").stat().st_size,
        "ordered_map_sha256": digest(UNIT / "ORDERED_EXERCISE_MAP.json"),
        "rights_bytes": RIGHTS.stat().st_size,
        "rights_sha256": digest(RIGHTS),
        "asset_closure_bytes": CLOSURE.stat().st_size,
        "asset_closure_sha256": digest(CLOSURE),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
