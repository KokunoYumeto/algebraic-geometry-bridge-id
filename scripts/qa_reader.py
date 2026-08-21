#!/usr/bin/env python3
"""Fail-closed structural QA for the bounded first Indonesian reader unit."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

from pypdf import PdfReader


LANE = Path(__file__).resolve().parents[1]
SOURCE_DIR = LANE / "source" / "id-ID"
BUILD_DIR = LANE / "build" / "reader-id"
FRONTMATTER = SOURCE_DIR / "frontmatter.md"
LECTURE = SOURCE_DIR / "lecture-01.md"
WORKSHEET = SOURCE_DIR / "worksheet-01.md"
SOLUTIONS = SOURCE_DIR / "worksheet-01-solutions.md"
CREDITS = SOURCE_DIR / "media-credits.md"
RIGHTS = LANE / "authority" / "RIGHTS.csv"
ASSET_CLOSURE = LANE / "authority" / "ASSET_CLOSURE.json"
SOLUTION_MAP = (
    LANE
    / "authority"
    / "wikiversity"
    / "worksheet-01-solutions"
    / "ORDERED_EXERCISE_MAP.json"
)
HTML = BUILD_DIR / "index.html"
PDF = BUILD_DIR / "algebraic-geometry-bridge-id-unit-01.pdf"
MACHINE_QA_RECEIPT = LANE / "qa" / "UNIT_01_MACHINE_QA.json"
EXPECTED = {
    FRONTMATTER: {},
    # The current Parsoid authority has 179 <math> nodes.  The translation has
    # 178 Pandoc Math nodes because adjacent source fragments are deliberately
    # coalesced; the protected-surface reconciliation receipt binds the
    # semantic mapping rather than pretending the serializations are isomorphic.
    LECTURE: {"Math": 178, "Image": 23},
    WORKSHEET: {"Math": 106, "exercise_headers": 28},
    SOLUTIONS: {"Math": 95, "solution_headers": 7},
    CREDITS: {},
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def pandoc_ast(path: Path) -> dict:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise RuntimeError("pandoc is not on PATH")
    proc = subprocess.run(
        [
            pandoc,
            "--from=markdown+yaml_metadata_block+tex_math_dollars+fenced_divs+bracketed_spans",
            "--to=json",
            str(path),
        ],
        cwd=LANE,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return json.loads(proc.stdout)


def ast_counts(ast: dict) -> tuple[dict[str, int], list[str], int, int]:
    counts: dict[str, int] = {}
    identifiers: list[str] = []
    exercise_headers = 0
    solution_headers = 0
    for node in walk(ast.get("blocks", [])):
        kind = node.get("t")
        if isinstance(kind, str):
            counts[kind] = counts.get(kind, 0) + 1
        if kind == "Header":
            attr = node.get("c", [None, ["", [], []]])[1]
            if attr and attr[0]:
                identifiers.append(attr[0])
                if attr[0].startswith("br-ak-2025-2026-w01-ex-"):
                    exercise_headers += 1
                if attr[0].startswith("br-ak-2025-2026-w01-sol-"):
                    solution_headers += 1
        elif kind == "Div":
            attr = node.get("c", [["", [], []]])[0]
            if attr and attr[0]:
                identifiers.append(attr[0])
    return counts, identifiers, exercise_headers, solution_headers


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    for path in (
        *EXPECTED,
        RIGHTS,
        ASSET_CLOSURE,
        SOLUTION_MAP,
        HTML,
        PDF,
        BUILD_DIR / "BUILD_RECEIPT.json",
    ):
        require(path.is_file() and not path.is_symlink(), f"missing/nonregular: {path}")

    all_ids: list[str] = []
    source_text = ""
    for path, expected in EXPECTED.items():
        raw = path.read_text(encoding="utf-8")
        source_text += "\n" + raw
        require("\t" not in raw, f"literal tab in Markdown source: {path}")
        require("pending_component_audit" not in raw, f"pending licence placeholder in {path}")
        require("<!-- QA:" not in raw, f"unresolved QA marker in {path}")
        ast = pandoc_ast(path)
        counts, identifiers, exercise_headers, solution_headers = ast_counts(ast)
        all_ids.extend(identifiers)
        if "Math" in expected:
            require(
                counts.get("Math", 0) == expected["Math"],
                f"{path.name}: Math {counts.get('Math', 0)} != {expected['Math']}",
            )
        if "Image" in expected:
            require(
                counts.get("Image", 0) == expected["Image"],
                f"{path.name}: Image {counts.get('Image', 0)} != {expected['Image']}",
            )
        if "exercise_headers" in expected:
            require(
                exercise_headers == expected["exercise_headers"],
                f"{path.name}: exercise headings {exercise_headers} != {expected['exercise_headers']}",
            )
        if "solution_headers" in expected:
            require(
                solution_headers == expected["solution_headers"],
                f"{path.name}: solution headings {solution_headers} != {expected['solution_headers']}",
            )

    require(
        all(all_id.startswith(("agc-", "br-ak-2025-2026-")) for all_id in all_ids),
        "noncanonical explicit ID",
    )
    require(len(all_ids) == len(set(all_ids)), "duplicate explicit source ID")
    require(not re.search(r"!\[[^\]]*\]\(https?://", source_text), "remote image in source")

    solution_map = json.loads(SOLUTION_MAP.read_text(encoding="utf-8"))
    require(solution_map.get("schema") == "brenner-worksheet-solution-map-v1", "wrong solution-map schema")
    require(solution_map.get("exercise_count") == 28, "wrong mapped exercise count")
    require(solution_map.get("solution_count") == 7, "wrong mapped solution count")
    entries = solution_map.get("entries", [])
    expected_solution_ids = [
        "br-ak-2025-2026-w01-ex-04",
        "br-ak-2025-2026-w01-ex-05",
        "br-ak-2025-2026-w01-ex-12",
        "br-ak-2025-2026-w01-ex-13",
        "br-ak-2025-2026-w01-ex-14",
        "br-ak-2025-2026-w01-ex-20",
        "br-ak-2025-2026-w01-ex-21",
    ]
    require(
        [entry.get("exercise_stable_id") for entry in entries] == expected_solution_ids,
        "solution-map order/IDs mismatch",
    )
    solution_dir = SOLUTION_MAP.parent
    for entry in entries:
        for prefix in ("export", "rendered_html"):
            path = solution_dir / entry[f"{prefix}_file"]
            require(path.is_file() and not path.is_symlink(), f"missing solution witness: {path}")
            require(path.stat().st_size == entry[f"{prefix}_bytes"], f"solution witness size mismatch: {path.name}")
            require(sha256(path) == entry[f"{prefix}_sha256"], f"solution witness hash mismatch: {path.name}")
    solution_raw = SOLUTIONS.read_text(encoding="utf-8")
    mapped_revids = [str(entry["revid"]) for entry in entries]
    source_revids = re.findall(r"upstream_solution_revid:\s*(\d+)", solution_raw)
    require(source_revids == mapped_revids, "translated solution revision sequence mismatch")
    require(solution_raw.count("Kembali ke Soal 1.") == 7, "solution backlink count mismatch")

    with RIGHTS.open("r", encoding="utf-8", newline="") as handle:
        rights_rows = list(csv.DictReader(handle))
    require(len(rights_rows) == 23, "component-rights row count mismatch")
    require([int(row["reader_order"]) for row in rights_rows] == list(range(1, 24)), "rights order mismatch")
    rights_paths = [row["local_path"] for row in rights_rows]
    require(len(rights_paths) == len(set(rights_paths)) == 23, "duplicate rights asset path")
    lecture_paths = re.findall(r"!\[[^\]]*\]\((authority/assets/[^)]+)\)", LECTURE.read_text(encoding="utf-8"))
    require(lecture_paths == rights_paths, "lecture image order differs from rights manifest")
    for row in rights_rows:
        path = LANE / row["local_path"]
        require(path.is_file() and not path.is_symlink(), f"missing rights-bound asset: {path}")
        require(path.stat().st_size == int(row["local_bytes"]), f"asset size mismatch: {path.name}")
        require(sha256(path) == row["local_sha256"], f"asset hash mismatch: {path.name}")
        if row["pdf_local_path"]:
            pdf_asset = LANE / row["pdf_local_path"]
            require(pdf_asset.is_file() and not pdf_asset.is_symlink(), f"missing PDF companion: {pdf_asset}")
            require(pdf_asset.stat().st_size == int(row["pdf_local_bytes"]), f"PDF companion size mismatch: {pdf_asset.name}")
            require(sha256(pdf_asset) == row["pdf_local_sha256"], f"PDF companion hash mismatch: {pdf_asset.name}")

    closure = json.loads(ASSET_CLOSURE.read_text(encoding="utf-8"))
    require(closure.get("schema") == "brenner-unit-media-closure-v1", "wrong media-closure schema")
    require(closure.get("reader_media_positions") == 23, "wrong media-closure position count")
    require(closure.get("unique_local_assets") == 26, "wrong media-closure asset count")
    require(closure.get("rights_sha256") == sha256(RIGHTS), "media-closure rights hash mismatch")
    require(closure.get("reader_credits_sha256") == sha256(CREDITS), "media-credit hash mismatch")

    html = HTML.read_text(encoding="utf-8")
    require(re.search(r"<html[^>]+lang=[\"']id-ID[\"']", html) is not None, "HTML lang is not id-ID")
    require("<title>Kurva Aljabar — Unit 1</title>" in html, "HTML document title mismatch")
    require("pending_component_audit" not in html, "pending licence placeholder in HTML")
    require("<!-- QA:" not in html, "unresolved QA marker in HTML")
    for identifier in all_ids:
        require(html.count(f'id="{identifier}"') == 1, f"HTML ID closure failed: {identifier}")
    require(re.search(r"<img[^>]+src=[\"']https?://", html) is None, "remote HTML image")
    require("Solusi Lembar Kerja 1" in html, "solutions absent from HTML")
    require("Kredit media" in html, "media credits absent from HTML")

    receipt = json.loads((BUILD_DIR / "BUILD_RECEIPT.json").read_text(encoding="utf-8"))
    require(receipt.get("schema") == "ag-bridge-build-receipt-v1", "wrong build receipt schema")
    output_names = {Path(row["path"]).name for row in receipt.get("outputs", [])}
    require(output_names == {HTML.name, PDF.name}, "receipt output set mismatch")
    for row in receipt["outputs"]:
        path = BUILD_DIR / Path(row["path"]).name
        require(path.stat().st_size == row["bytes"], f"receipt size mismatch: {path.name}")
        require(sha256(path) == row["sha256"], f"receipt hash mismatch: {path.name}")

    reader = PdfReader(PDF, strict=True)
    require(not reader.is_encrypted, "PDF is encrypted")
    require(reader.metadata is not None and reader.metadata.title == "Kurva Aljabar — Unit 1", "PDF title metadata mismatch")
    require(len(reader.pages) >= 10, "PDF page count is implausibly small")
    pdf_text = "\n".join((page.extract_text() or "") for page in reader.pages)
    require("Solusi Lembar Kerja 1" in pdf_text, "solutions absent from PDF text")
    require("Kredit media" in pdf_text, "media credits absent from PDF text")
    require("pending_component_audit" not in pdf_text, "pending marker in PDF text")

    result = {
        "schema": "ag-bridge-machine-qa-receipt-v1",
        "tested_build_utc": receipt["built_utc"],
        "status": "PASS",
        "source_ids": len(all_ids),
        "lecture_math": EXPECTED[LECTURE]["Math"],
        "lecture_images": EXPECTED[LECTURE]["Image"],
        "worksheet_math": EXPECTED[WORKSHEET]["Math"],
        "worksheet_exercises": EXPECTED[WORKSHEET]["exercise_headers"],
        "solution_math": EXPECTED[SOLUTIONS]["Math"],
        "solutions": EXPECTED[SOLUTIONS]["solution_headers"],
        "media_assets": len(rights_rows),
        "pdf_pages": len(reader.pages),
        "html_sha256": sha256(HTML),
        "pdf_sha256": sha256(PDF),
        "qa_script": {
            "path": Path(__file__).relative_to(LANE).as_posix(),
            "sha256": sha256(Path(__file__)),
        },
        "check_families": [
            "source_placeholders_and_ids",
            "pandoc_math_and_image_surfaces",
            "exercise_solution_mapping",
            "asset_rights_and_hashes",
            "html_language_links_and_local_assets",
            "build_receipt_replay",
            "pdf_structure_metadata_and_text",
        ],
    }
    MACHINE_QA_RECEIPT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
