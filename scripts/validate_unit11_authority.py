#!/usr/bin/env python3
"""Fail-closed validation of the frozen Unit 11 authority-only boundary."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "authority" / "wikiversity" / "unit-11"
MANIFEST_PATH = UNIT / "UNIT_AUTHORITY_MANIFEST.json"
MAP_PATH = UNIT / "ORDERED_EXERCISE_MAP.json"
RIGHTS_PATH = ROOT / "authority" / "RIGHTS-unit-11.csv"
CLOSURE_PATH = ROOT / "authority" / "ASSET_CLOSURE-unit-11.json"
FREEZE_NOTE = ROOT / "authority" / "UNIT_11_AUTHORITY_FREEZE.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_fact(path: Path, fact: dict[str, Any], *, base: Path = UNIT) -> None:
    check(path.is_file() and not path.is_symlink(), f"missing/non-regular file: {path}")
    check(path.stat().st_size == int(fact["bytes"]), f"byte mismatch: {path}")
    check(sha256(path) == fact["sha256"], f"SHA-256 mismatch: {path}")
    expected_name = path.relative_to(base).as_posix()
    check(fact.get("file") == expected_name, f"relative path mismatch: {path}")


def validate_record_files(record: dict[str, Any]) -> None:
    for prefix in ("api", "xml", "html", "parse_api"):
        file_key = f"{prefix}_file"
        if file_key not in record:
            continue
        path = UNIT / record[file_key]
        check(path.is_file(), f"record file absent: {path}")
        check(path.stat().st_size == int(record[f"{prefix}_bytes"]), f"record bytes drift: {path}")
        check(sha256(path) == record[f"{prefix}_sha256"], f"record hash drift: {path}")


def validate_closure(name: str, closure: dict[str, Any]) -> None:
    requested = int(closure["requested_template_count"])
    captured = int(closure["captured_page_count"])
    pages = closure["pages"]
    check(requested == captured == len(pages), f"{name} transclusion count mismatch")
    check(int(closure["missing_page_count"]) == 0, f"{name} transclusion is incomplete")
    check(len(closure["batches"]) == (requested + 24) // 25, f"{name} batch count mismatch")
    requested_titles: list[str] = []
    for batch in closure["batches"]:
        path = UNIT / batch["file"]
        check(path.is_file(), f"missing transclusion batch: {path}")
        check(path.stat().st_size == int(batch["bytes"]), f"batch bytes drift: {path}")
        check(sha256(path) == batch["sha256"], f"batch hash drift: {path}")
        requested_titles.extend(batch["requested_titles"])
    page_titles = [page["title"] for page in pages]
    check(len(requested_titles) == len(set(requested_titles)) == requested, f"{name} request duplicates")
    check(set(requested_titles) == set(page_titles), f"{name} request/capture title mismatch")
    check(len(page_titles) == len(set(page_titles)), f"{name} captured title duplicates")
    for page in pages:
        for key in ("pageid", "revid", "timestamp", "mediawiki_sha1", "wikitext_bytes"):
            check(page.get(key) not in (None, ""), f"{name} transclusion lacks {key}: {page.get('title')}")
        check(bool(re.fullmatch(r"[0-9a-f]{40}", page["mediawiki_sha1"])), f"bad MediaWiki SHA-1: {page}")


def main() -> int:
    for path in (MANIFEST_PATH, MAP_PATH, RIGHTS_PATH, CLOSURE_PATH, FREEZE_NOTE):
        check(path.is_file() and not path.is_symlink(), f"required Unit 11 authority file absent: {path}")
    manifest = load_json(MANIFEST_PATH)
    ordered = load_json(MAP_PATH)
    closure = load_json(CLOSURE_PATH)
    check(manifest.get("schema") == "brenner-unit-authority-freeze-v2", "unexpected manifest schema")
    check(manifest.get("unit_number") == 11, "manifest is not Unit 11")

    listed = {fact["file"]: fact for fact in manifest["files"]}
    actual = {
        path.relative_to(UNIT).as_posix(): path
        for path in UNIT.iterdir()
        if path.is_file() and path != MANIFEST_PATH
    }
    check(set(listed) == set(actual), "manifest file inventory does not exactly match Unit 11 directory")
    for name, path in actual.items():
        validate_fact(path, listed[name])

    expected_entry = {
        "lecture": (165900, 1051329, "33f81e0bf65b5b23de1c5798adf4a93282354d82"),
        "worksheet": (165930, 1062657, "1b95cc02cb9d0260971c1fa369afc8969fa13262"),
        "lecture_latex_page": (165964, 1033010, "3034e92c1843eab298fb5f6f859d2c89cf824d61"),
        "worksheet_latex_page": (166024, 1033071, "3034e92c1843eab298fb5f6f859d2c89cf824d61"),
    }
    for key, expected in expected_entry.items():
        record = manifest[key]
        check(
            (record["pageid"], record["revid"], record["mediawiki_sha1"]) == expected,
            f"entry identity drift: {key}",
        )
        validate_record_files(record)

    validate_closure("lecture", manifest["lecture_transclusion_closure"])
    validate_closure("worksheet", manifest["worksheet_transclusion_closure"])
    check(manifest["lecture_transclusion_closure"]["captured_page_count"] == 115, "lecture closure drift")
    check(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 129, "worksheet closure drift")

    check(ordered.get("schema") == "brenner-worksheet-solution-map-v2", "unexpected map schema")
    check(ordered.get("unit") == 11, "ordered map is not Unit 11")
    entries = ordered["entries"]
    check(ordered["exercise_count"] == len(entries) == 26, "exercise topology mismatch")
    check([entry["exercise_number"] for entry in entries] == list(range(1, 27)), "exercise order drift")
    public = [entry for entry in entries if entry["has_public_solution"]]
    check(ordered["solution_count"] == len(public) == 2, "public-solution count mismatch")
    check([entry["exercise_number"] for entry in public] == [6, 7], "public-solution topology drift")
    check(
        [(entry["pageid"], entry["revid"], entry["mediawiki_sha1"]) for entry in public]
        == [
            (94452, 1094883, "f0fda003d418823f5e271cdede1aee887c498529"),
            (168417, 1112854, "6b4c0414ed689932274e3d77385607439dc7b0b3"),
        ],
        "public-solution identities drifted",
    )
    for entry in public:
        validate_record_files(entry)
    solution_manifest = manifest["solutions"]
    check(solution_manifest["exercise_count"] == 26 and solution_manifest["solution_count"] == 2, "manifest solution counts drifted")
    check(solution_manifest["map_bytes"] == MAP_PATH.stat().st_size, "map byte binding drifted")
    check(solution_manifest["map_sha256"] == sha256(MAP_PATH), "map hash binding drifted")
    check(solution_manifest["entries"] == entries, "manifest/map solution entries disagree")

    pdf_records = manifest["official_pdf_witnesses"]
    check(len(pdf_records) == 2, "official PDF witness count drifted")
    expected_pdfs = {
        "authority/artifacts/lecture-11-official.pdf": (181044, "5f608194d133bb71f94f52721ea3750711cf55af2bce576c8e80ac5255994250", 7),
        "authority/artifacts/worksheet-11-official.pdf": (141094, "c1a3247173b3b61820490e223e61871dfa06a15e9d51e202ca1f4f0259f647e8", 7),
    }
    for record in pdf_records:
        path = ROOT / record["local_path"]
        check(record["local_path"] in expected_pdfs, f"unexpected PDF witness: {path}")
        expected_bytes, expected_hash, expected_pages = expected_pdfs[record["local_path"]]
        check(path.stat().st_size == record["local_bytes"] == expected_bytes, f"PDF bytes drift: {path}")
        check(sha256(path) == record["local_sha256"] == expected_hash, f"PDF hash drift: {path}")
        check(path.read_bytes().startswith(b"%PDF-"), f"PDF signature absent: {path}")
        reader = PdfReader(path)
        check(len(reader.pages) == expected_pages and not reader.is_encrypted, f"PDF page/encryption drift: {path}")

    image_names = set(manifest["images"]["lecture"]) | set(manifest["images"]["worksheet"])
    check(
        {name for name in image_names if not name.lower().endswith(".pdf")} == {"Disjoint_ellipses.png"},
        "non-PDF media closure drifted",
    )
    with RIGHTS_PATH.open("r", encoding="utf-8", newline="") as stream:
        rights = list(csv.DictReader(stream))
    check(len(rights) == 1, "Unit 11 reader-media rights must have exactly one row")
    row = rights[0]
    asset = ROOT / row["local_path"]
    check(row["asset_id"] == "br-ak-u11-media-001", "reader-media stable ID drifted")
    check(row["resource_title"] == "File:Disjoint ellipses.png", "reader-media source title drifted")
    check(row["license_short"] == "Public domain", "reader-media licence drifted")
    check(row["selected_form"] == "commons-rendered-250px-thumbnail-at-source-native-width", "media form is not explicit")
    check(asset.stat().st_size == int(row["local_bytes"]), "local media bytes drifted")
    check(sha256(asset) == row["local_sha256"], "local media hash drifted")
    with Image.open(asset) as image:
        image.verify()
    with Image.open(asset) as image:
        check((image.width, image.height) == (250, 246), "local media dimensions drifted")

    check(closure.get("unit") == 11 and closure.get("authority_only_boundary") is True, "asset closure boundary drifted")
    check(closure["reader_media_positions"] == 1 and closure["unique_local_assets"] == 1, "asset closure counts drifted")
    check(closure["rights_bytes"] == RIGHTS_PATH.stat().st_size, "asset closure rights bytes drifted")
    check(closure["rights_sha256"] == sha256(RIGHTS_PATH), "asset closure rights hash drifted")
    check(len(closure["official_pdf_component_rights"]) == 2, "PDF rights closure count drifted")
    for item in closure["official_pdf_component_rights"]:
        check(item["license_short"] == "CC BY-SA 4.0", f"official PDF licence drifted: {item['title']}")
        path = ROOT / item["local_path"]
        check(path.stat().st_size == item["local_bytes"], f"PDF rights byte binding drifted: {path}")
        check(sha256(path) == item["local_sha256"], f"PDF rights hash binding drifted: {path}")
    for fact in closure["metadata_files"]:
        validate_fact(ROOT / fact["file"], fact, base=ROOT)

    textual = [*actual.values(), RIGHTS_PATH, CLOSURE_PATH, FREEZE_NOTE]
    forbidden = re.compile(r"(?i)c:\\users\\|bearer\s+[a-z0-9._-]+|(?:access[_-]?token|api[_-]?key|secret)\s*[=:]")
    for path in textual:
        if path.suffix.lower() in {".json", ".xml", ".html", ".tex", ".csv", ".md", ".wikitext"}:
            check(not forbidden.search(path.read_text(encoding="utf-8", errors="replace")), f"sanitization guard failed: {path}")

    unit_files = [path for path in UNIT.iterdir() if path.is_file()]
    result = {
        "status": "PASS",
        "unit": 11,
        "unit_directory_files": len(unit_files),
        "unit_directory_bytes": sum(path.stat().st_size for path in unit_files),
        "manifest_bytes": MANIFEST_PATH.stat().st_size,
        "manifest_sha256": sha256(MANIFEST_PATH),
        "lecture_transclusions": 115,
        "worksheet_transclusions": 129,
        "exercises": 26,
        "public_solutions": 2,
        "official_pdf_pages": {"lecture": 7, "worksheet": 7},
        "reader_media_positions": 1,
        "rights_sha256": sha256(RIGHTS_PATH),
        "asset_closure_sha256": sha256(CLOSURE_PATH),
        "freeze_note_sha256": sha256(FREEZE_NOTE),
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
