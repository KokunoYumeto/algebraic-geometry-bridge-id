#!/usr/bin/env python3
"""Fail-closed structural, mathematical-surface, and artifact QA through Unit 3."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source" / "id-ID"
BUILD = ROOT / "build" / "reader-id"
PDF = BUILD / "algebraic-geometry-bridge-id-units-01-03.pdf"
HTML = BUILD / "index.html"
RECEIPT = BUILD / "BUILD_RECEIPT.json"
OUT = ROOT / "qa" / "UNITS_01_03_MACHINE_QA.json"

SOURCES = (
    SOURCE / "frontmatter-units-01-03.md",
    SOURCE / "lecture-01.md",
    SOURCE / "worksheet-01.md",
    SOURCE / "worksheet-01-solutions.md",
    SOURCE / "lecture-02.md",
    SOURCE / "worksheet-02.md",
    SOURCE / "worksheet-02-solutions.md",
    SOURCE / "lecture-03.md",
    SOURCE / "worksheet-03.md",
    SOURCE / "worksheet-03-solutions.md",
    SOURCE / "media-credits.md",
    SOURCE / "media-credits-unit-02.md",
    SOURCE / "media-credits-unit-03.md",
)

EXPECTED = {
    SOURCE / "lecture-01.md": {"math": 178, "images": 23, "headers": 12},
    SOURCE / "worksheet-01.md": {"math": 106, "images": 0, "exercises": 28, "headers": 31},
    SOURCE / "worksheet-01-solutions.md": {"math": 95, "images": 0, "solutions": 7, "headers": 8},
    SOURCE / "lecture-02.md": {"math": 178, "images": 2, "headers": 14},
    SOURCE / "worksheet-02.md": {"math": 96, "images": 0, "exercises": 27, "headers": 30},
    SOURCE / "worksheet-02-solutions.md": {"math": 145, "images": 0, "solutions": 9, "headers": 10},
    SOURCE / "lecture-03.md": {"math": 157, "images": 4, "headers": 23},
    SOURCE / "worksheet-03.md": {"math": 89, "images": 0, "exercises": 22, "headers": 27},
    SOURCE / "worksheet-03-solutions.md": {"math": 23, "images": 0, "solutions": 2, "headers": 3},
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


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
    require(bool(pandoc), "pandoc is not on PATH")
    result = subprocess.run(
        [
            pandoc,
            "--from=markdown+yaml_metadata_block+tex_math_dollars+fenced_divs+bracketed_spans",
            "--to=json",
            str(path),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return json.loads(result.stdout)


def ast_counts(ast: dict) -> dict[str, int]:
    counts: dict[str, int] = {}
    for node in walk(ast):
        kind = node.get("t")
        if kind:
            counts[kind] = counts.get(kind, 0) + 1
    return counts


def source_ids(path: Path) -> list[str]:
    return re.findall(r"\{#([^}]+)\}", path.read_text(encoding="utf-8"))


def solution_map(number: int) -> tuple[dict, Path]:
    if number == 1:
        path = ROOT / "authority" / "wikiversity" / "worksheet-01-solutions" / "ORDERED_EXERCISE_MAP.json"
    else:
        path = ROOT / "authority" / "wikiversity" / f"unit-{number:02d}" / "ORDERED_EXERCISE_MAP.json"
    return json.loads(path.read_text(encoding="utf-8")), path


def verify_solution_map(number: int, translated: Path, expected_exercises: int, expected_solutions: int) -> dict:
    mapping, path = solution_map(number)
    require(mapping["exercise_count"] == expected_exercises, f"Unit {number} exercise-map count")
    require(mapping["solution_count"] == expected_solutions, f"Unit {number} solution-map count")
    entries = mapping["entries"]
    if number == 1:
        solution_entries = entries
        directory = path.parent
        xml_key, html_key = "export_file", "rendered_html_file"
        xml_bytes, html_bytes = "export_bytes", "rendered_html_bytes"
        xml_hash, html_hash = "export_sha256", "rendered_html_sha256"
    else:
        solution_entries = [entry for entry in entries if entry["has_public_solution"]]
        directory = path.parent
        xml_key, html_key = "xml_file", "html_file"
        xml_bytes, html_bytes = "xml_bytes", "html_bytes"
        xml_hash, html_hash = "xml_sha256", "html_sha256"
        require(len(entries) == expected_exercises, f"Unit {number} map enumerates every exercise")
    require(len(solution_entries) == expected_solutions, f"Unit {number} public-solution closure")
    for entry in solution_entries:
        for key, byte_key, hash_key in (
            (xml_key, xml_bytes, xml_hash),
            (html_key, html_bytes, html_hash),
        ):
            witness = directory / entry[key]
            require(witness.is_file() and not witness.is_symlink(), f"missing solution witness {witness}")
            require(witness.stat().st_size == int(entry[byte_key]), f"solution witness bytes {witness.name}")
            require(digest(witness) == entry[hash_key], f"solution witness hash {witness.name}")
    translated_text = translated.read_text(encoding="utf-8")
    source_revids = re.findall(r"upstream_solution_revid:\s*(\d+)", translated_text)
    expected_revids = [str(entry["revid"]) for entry in solution_entries]
    require(source_revids == expected_revids, f"Unit {number} translated solution revision sequence")
    require(translated_text.count(f"Kembali ke Soal {number}.") == expected_solutions, f"Unit {number} solution backlinks")
    return {"exercise_count": expected_exercises, "solution_count": expected_solutions, "map_sha256": digest(path)}


def verify_rights(csv_name: str, closure_name: str, expected_positions: int, expected_surfaces: int) -> dict:
    rights_path = ROOT / "authority" / csv_name
    closure_path = ROOT / "authority" / closure_name
    with rights_path.open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == expected_positions, f"{csv_name} row count")
    require([int(row["reader_order"]) for row in rows] == list(range(1, expected_positions + 1)), f"{csv_name} order")
    local_paths = []
    for row in rows:
        for prefix in ("local", "pdf_local"):
            value = row[f"{prefix}_path"]
            if not value:
                continue
            asset = ROOT / value
            local_paths.append(value)
            require(asset.is_file() and not asset.is_symlink(), f"missing rights-bound asset {asset}")
            require(asset.stat().st_size == int(row[f"{prefix}_bytes"]), f"asset bytes {asset.name}")
            require(digest(asset) == row[f"{prefix}_sha256"], f"asset hash {asset.name}")
        require(bool(row["license_short"] or row["usage_terms"]), f"missing component licence {row['asset_id']}")
        require(bool(row["description_url"]), f"missing component source {row['asset_id']}")
    require(len(set(local_paths)) == expected_surfaces, f"{csv_name} binary-surface closure")
    closure = json.loads(closure_path.read_text(encoding="utf-8"))
    require(closure["reader_media_positions"] == expected_positions, f"{closure_name} positions")
    require(closure["unique_local_assets"] == expected_surfaces, f"{closure_name} surfaces")
    require(closure["rights_sha256"] == digest(rights_path), f"{closure_name} rights binding")
    return {"positions": expected_positions, "surfaces": expected_surfaces, "rights_sha256": digest(rights_path), "closure_sha256": digest(closure_path)}


def verify_unit3_authority() -> dict:
    path = ROOT / "authority" / "wikiversity" / "unit-03" / "UNIT_AUTHORITY_MANIFEST.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    require(manifest["unit_number"] == 3, "Unit 3 manifest unit")
    require(manifest["lecture"]["revid"] == 1052207, "Unit 3 lecture revision")
    require(manifest["worksheet"]["revid"] == 1061785, "Unit 3 worksheet revision")
    require(manifest["lecture_transclusion_closure"]["requested_template_count"] == 96, "Unit 3 lecture template count")
    require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "Unit 3 lecture missing transclusion")
    require(manifest["worksheet_transclusion_closure"]["requested_template_count"] == 117, "Unit 3 worksheet template count")
    require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "Unit 3 worksheet missing transclusion")
    for row in manifest["files"]:
        witness = path.parent / row["file"]
        require(witness.stat().st_size == row["bytes"] and digest(witness) == row["sha256"], f"Unit 3 authority replay {row['file']}")
    return {"manifest_sha256": digest(path), "file_count": len(manifest["files"]), "lecture_revid": 1052207, "worksheet_revid": 1061785}


def main() -> int:
    for path in (*SOURCES, HTML, PDF, RECEIPT):
        require(path.is_file() and not path.is_symlink(), f"missing/nonregular input {path}")

    combined = "\n".join(path.read_text(encoding="utf-8") for path in SOURCES)
    require("<!-- QA:" not in combined, "unresolved QA marker")
    require("pending_component_audit" not in combined, "pending rights marker")
    require("translation_status: draft" not in combined, "draft translation marker")
    require("\t" not in combined, "tab in reader source")
    visible = re.sub(r"<!--.*?-->", "", combined, flags=re.S)
    visible = re.sub(r"^---\n.*?\n---$", "", visible, flags=re.S | re.M)
    require(
        re.search(r"\b(Es sei|Zeige|Bestimme|Somit|Damit|Nullstellengebilde|Aufgaben zum Abgeben)\b", visible) is None,
        "active untranslated German prose marker",
    )
    require(re.search(r"github_pat_|ghp_[A-Za-z0-9]{20,}|ZENODO_ACCESS_TOKEN", combined) is None, "credential-shaped text")
    require("Petunjuk sumber" in combined and "Jangan gunakan Soal 3.18" in combined, "Unit 3 source hint")
    require("Definisi pengantar: unsur nilpoten" in combined, "Unit 3 nilpotent definition")
    require("Definisi pengantar: gelanggang tereduksi" in combined, "Unit 3 reduced-ring definition")

    ids = []
    ast_summary = {}
    for path in SOURCES:
        ids.extend(source_ids(path))
        if path in EXPECTED:
            ast = pandoc_ast(path)
            counts = ast_counts(ast)
            expectation = EXPECTED[path]
            require(counts.get("Math", 0) == expectation["math"], f"{path.name} math count")
            require(counts.get("Image", 0) == expectation["images"], f"{path.name} image count")
            require(counts.get("Header", 0) == expectation["headers"], f"{path.name} header count")
            if "exercises" in expectation:
                count = len(re.findall(r"^### Soal \d+\.\d+", path.read_text(encoding="utf-8"), flags=re.M))
                require(count == expectation["exercises"], f"{path.name} exercise count")
            if "solutions" in expectation:
                count = len(re.findall(r"^## Solusi Soal \d+\.\d+", path.read_text(encoding="utf-8"), flags=re.M))
                require(count == expectation["solutions"], f"{path.name} solution count")
            ast_summary[path.name] = {key: counts.get(key, 0) for key in ("Header", "Math", "Image")}
    require(len(ids) == len(set(ids)) == 163, f"stable ID closure: {len(ids)}")
    require(all(identifier.startswith(("agc-", "br-ak-2025-2026-")) for identifier in ids), "noncanonical stable ID")

    solution_summary = {
        "unit_01": verify_solution_map(1, SOURCE / "worksheet-01-solutions.md", 28, 7),
        "unit_02": verify_solution_map(2, SOURCE / "worksheet-02-solutions.md", 27, 9),
        "unit_03": verify_solution_map(3, SOURCE / "worksheet-03-solutions.md", 22, 2),
    }
    rights_summary = {
        "unit_01": verify_rights("RIGHTS.csv", "ASSET_CLOSURE.json", 23, 26),
        "unit_02": verify_rights("RIGHTS-unit-02.csv", "ASSET_CLOSURE-unit-02.json", 2, 3),
        "unit_03": verify_rights("RIGHTS-unit-03.csv", "ASSET_CLOSURE-unit-03.json", 4, 4),
    }
    authority_summary = verify_unit3_authority()

    html_bytes = HTML.read_bytes()
    soup = BeautifulSoup(html_bytes, "html.parser")
    require(soup.html is not None and soup.html.get("lang") == "id-ID", "HTML language")
    require(soup.title is not None and soup.title.get_text(strip=True) == "Kurva Aljabar — Unit 1–3", "HTML title")
    for identifier in ids:
        require(len(soup.select(f"[id='{identifier}']")) == 1, f"HTML ID closure {identifier}")
    html_ids = {node.get("id") for node in soup.find_all(id=True)}
    missing_internal = sorted(
        href[1:]
        for node in soup.find_all(href=True)
        if (href := node.get("href", "")).startswith("#") and href[1:] not in html_ids
    )
    require(not missing_internal, f"broken internal HTML links: {missing_internal[:5]}")
    images = soup.find_all("img")
    require(len(images) == 29, f"HTML image count {len(images)}")
    require(all(image.get("alt", "").strip() for image in images), "missing HTML image alt text")
    require(all(not re.match(r"https?://", image.get("src", "")) for image in images), "remote HTML image")
    require(len(soup.find_all("math")) == 1067, f"HTML MathML count {len(soup.find_all('math'))}")
    html_text = soup.get_text(" ", strip=True)
    require("Solusi Publik Lembar Kerja 3" in html_text, "Unit 3 solutions absent from HTML")
    require("Kredit media Unit 3" in html_text, "Unit 3 media credits absent from HTML")
    require(re.search(rb"github_pat_|ghp_[A-Za-z0-9]{20,}", html_bytes) is None, "credential in HTML")

    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    require(receipt["schema"] == "ag-bridge-build-receipt-v2", "build receipt schema")
    require(receipt["through_unit"] == 3, "build receipt scope")
    for row in receipt["inputs"]:
        path = ROOT / row["path"]
        require(path.stat().st_size == row["bytes"] and digest(path) == row["sha256"], f"build input replay {row['path']}")
    output_names = {Path(row["path"]).name for row in receipt["outputs"]}
    require(output_names == {HTML.name, PDF.name}, "build output closure")
    for row in receipt["outputs"]:
        path = BUILD / Path(row["path"]).name
        require(path.stat().st_size == row["bytes"] and digest(path) == row["sha256"], f"build output replay {row['path']}")

    reader = PdfReader(PDF, strict=True)
    require(not reader.is_encrypted, "PDF encrypted")
    require(len(reader.pages) == 60, f"PDF pages {len(reader.pages)}")
    require(reader.metadata is not None and reader.metadata.title == "Kurva Aljabar — Unit 1–3", "PDF title metadata")
    pdf_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    for marker in (
        "Kuliah 3: Topologi Zariski",
        "Soal 3.22",
        "Solusi Soal 3.13",
        "Kredit media Unit 3",
    ):
        require(marker in pdf_text, f"PDF text marker absent: {marker}")
    require("pending_component_audit" not in pdf_text, "pending marker in PDF")

    pdffonts = shutil.which("pdffonts")
    require(bool(pdffonts), "pdffonts unavailable")
    fonts = subprocess.run([pdffonts, str(PDF)], capture_output=True, text=True, encoding="utf-8", check=True).stdout
    font_rows = [line.split() for line in fonts.splitlines()[2:] if line.strip()]
    require(font_rows and all("yes" in row for row in font_rows), "PDF contains an unembedded font")
    require(all("Type 3" not in line for line in fonts.splitlines()), "PDF contains Type 3 font")

    result = {
        "schema": "ag-bridge-machine-qa-receipt-v3",
        "tested_build_utc": receipt["built_utc"],
        "status": "PASS",
        "through_unit": 3,
        "stable_ids": len(ids),
        "ast_surfaces": ast_summary,
        "solutions": solution_summary,
        "rights": rights_summary,
        "authority": {"unit_03": authority_summary},
        "html": {
            "bytes": HTML.stat().st_size,
            "sha256": digest(HTML),
            "images": len(images),
            "mathml_nodes": len(soup.find_all("math")),
            "broken_internal_links": 0,
            "remote_images": 0,
        },
        "pdf": {
            "bytes": PDF.stat().st_size,
            "sha256": digest(PDF),
            "pages": len(reader.pages),
            "encrypted": False,
            "font_rows": len(font_rows),
            "unembedded_fonts": 0,
            "type3_fonts": 0,
        },
        "build_receipt": {"bytes": RECEIPT.stat().st_size, "sha256": digest(RECEIPT)},
        "qa_script": {"path": Path(__file__).relative_to(ROOT).as_posix(), "sha256": digest(Path(__file__))},
        "check_families": [
            "source_placeholders_language_hints_and_secrets",
            "pandoc_math_image_heading_and_stable_id_surfaces",
            "exercise_solution_revision_and_witness_closure",
            "component_rights_and_asset_hash_closure",
            "unit3_revision_authority_manifest_and_file_hash_replay",
            "html_language_alt_mathml_internal_links_and_local_assets",
            "build_input_and_output_receipt_replay",
            "pdf_structure_metadata_text_and_fonts",
        ],
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
