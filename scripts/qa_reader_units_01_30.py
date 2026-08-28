#!/usr/bin/env python3
"""Fail-closed cumulative reader QA for the complete 30-unit classical course."""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote

from bs4 import BeautifulSoup
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "build" / "reader-id" / "index.html"
PDF = ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-30.pdf"
BUILD = ROOT / "build" / "reader-id" / "BUILD_RECEIPT.json"
PDF_LOG = ROOT / "build" / "reader-id" / "pandoc-pdf.log"
BASELINE_MACHINE = ROOT / "qa" / "UNITS_01_28_MACHINE_QA.json"
BASELINE_PROTECTED = ROOT / "qa" / "UNIT_28_PROTECTED_SURFACES.json"
TRANSLATION = {
    29: ROOT / "qa" / "UNIT_29_TRANSLATION_QA.json",
    30: ROOT / "qa" / "UNIT_30_TRANSLATION_QA.json",
}
OUT = ROOT / "qa" / "UNITS_01_30_MACHINE_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra."

EXPECTED_FACTS = {
    BASELINE_MACHINE: (3083, "c666cb1186f516cead5ebd1a16de616856c99013cd94983826c974aebbdf776f"),
    BASELINE_PROTECTED: (2533, "d9e737e3319f62d7560cbad20737c27b80b40c27536e3dca36d4632c98f18b2e"),
    TRANSLATION[29]: (6802, "7789a7a131bcf44946204f52c328e24fa96fee0c1e24383994d4485437bffb81"),
    TRANSLATION[30]: (6973, "788f6cb2245c5daef6a70fad25879c35d2234e43240e83be1bca1fc32c976916"),
    BUILD: (45373, "1e90f2791e813319f95095b8be40b698e7dacd548f0e5e51c39be413d7846c19"),
    HTML: (23805465, "1ca69127dbbf8aa86d8d3f238488686a145ad2dd99ee417c329a5bd9516ca677"),
    PDF: (16019237, "6383d3b9804a059e76dc643da5974b8809649707e177ba191a69220fa7ea0e5d"),
    PDF_LOG: (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def fact(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), f"missing/nonregular file: {path}")
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }


def require_fact(path: Path) -> dict[str, Any]:
    row = fact(path)
    require((row["bytes"], row["sha256"]) == EXPECTED_FACTS[path], f"identity drift: {row['path']}")
    return row


def normalized(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def marker_pages(page_texts: list[str], marker: str) -> list[int]:
    target = normalized(marker)
    return [index + 1 for index, text in enumerate(page_texts) if target in normalized(text)]


def main() -> int:
    bound = {path.relative_to(ROOT).as_posix(): require_fact(path) for path in EXPECTED_FACTS}

    baseline_machine = json.loads(BASELINE_MACHINE.read_text(encoding="utf-8"))
    baseline_protected = json.loads(BASELINE_PROTECTED.read_text(encoding="utf-8"))
    require(baseline_machine.get("status") == "PASS" and baseline_machine.get("through_unit") == 28,
            "Unit 28 machine baseline status/scope")
    require(baseline_protected.get("status") == "PASS" and baseline_protected.get("through_unit") == 28,
            "Unit 28 protected baseline status/scope")

    translations: dict[int, dict[str, Any]] = {}
    for unit, path in TRANSLATION.items():
        payload = json.loads(path.read_text(encoding="utf-8"))
        require(payload.get("status") == "PASS" and payload.get("unit") == unit, f"Unit {unit} translation status/scope")
        require(payload.get("provenance") == MODEL, f"Unit {unit} translation provenance")
        translations[unit] = payload
    cumulative = translations[30]["cumulative_source"]
    require(cumulative == {
        "lectures": 30,
        "worksheets": 30,
        "exercises": 693,
        "public_solutions": 122,
        "media_positions": 101,
        "stable_source_ids": 1554,
    }, "complete classical cumulative source counts")

    build = json.loads(BUILD.read_text(encoding="utf-8"))
    require(build.get("schema") == "ag-bridge-build-receipt-v2", "build receipt schema")
    require(build.get("through_unit") == 30 and build.get("language") == "id-ID", "build receipt scope/language")
    require(build.get("title") == "Kurva Aljabar - Unit 1-30", "build receipt title")
    inputs = build.get("inputs", [])
    require(inputs and len({row.get("path") for row in inputs}) == len(inputs), "build input inventory uniqueness")
    for row in inputs:
        path = ROOT / row["path"]
        actual = fact(path)
        require((actual["bytes"], actual["sha256"]) == (row["bytes"], row["sha256"]),
                f"build input replay: {row['path']}")
    outputs = {row["path"]: row for row in build.get("outputs", [])}
    for path in (HTML, PDF):
        relative = path.relative_to(ROOT).as_posix()
        require(relative in outputs, f"build output absent: {relative}")
        actual = bound[relative]
        require((actual["bytes"], actual["sha256"]) ==
                (outputs[relative]["bytes"], outputs[relative]["sha256"]), f"build output replay: {relative}")
    html_log = ROOT / "build" / "reader-id" / "pandoc-html.log"
    pdf_log = PDF_LOG
    require(html_log.is_file() and html_log.stat().st_size == 0, "HTML build log is not empty")
    require(pdf_log.is_file() and pdf_log.stat().st_size == 0, "PDF build log is not empty")

    html_text = HTML.read_text(encoding="utf-8")
    soup = BeautifulSoup(html_text, "html.parser")
    require(soup.html is not None and soup.html.get("lang") == "id-ID", "HTML language")
    require(soup.title is not None and normalized(soup.title.get_text()) == "Kurva Aljabar - Unit 1-30", "HTML title")
    meta_viewport = soup.find("meta", attrs={"name": "viewport"})
    require(meta_viewport is not None and "width=device-width" in (meta_viewport.get("content") or ""), "responsive viewport metadata")
    ids = [node["id"] for node in soup.find_all(attrs={"id": True})]
    require(len(ids) == len(set(ids)), "duplicate HTML ids")
    id_set = set(ids)
    fragment_links = []
    broken_fragments = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("#") and len(href) > 1:
            target = unquote(href[1:])
            fragment_links.append(target)
            if target not in id_set:
                broken_fragments.append(target)
    require(not broken_fragments, f"broken internal anchors: {broken_fragments[:10]}")
    images = soup.find_all("img")
    empty_alt = [node.get("src", "") for node in images if not (node.get("alt") or "").strip()]
    require(not empty_alt, f"empty image alt text: {empty_alt[:10]}")
    embedded_images = [node.get("src", "") for node in images if node.get("src", "").lower().startswith("data:image/")]
    remote_images = [node.get("src", "") for node in images if re.match(r"^(?:https?|ftp):", node.get("src", ""), re.I)]
    require(not remote_images, f"remote image dependencies: {remote_images[:10]}")
    missing_images = []
    for node in images:
        src = unquote((node.get("src") or "").split("#", 1)[0].split("?", 1)[0])
        if src and not src.lower().startswith("data:image/") and not (HTML.parent / src).is_file():
            missing_images.append(src)
    require(not missing_images, f"missing local images: {missing_images[:10]}")
    math_nodes = soup.find_all("math")
    annotations = [node for node in soup.find_all("annotation") if node.get("encoding") == "application/x-tex"]
    require(len(math_nodes) == len(annotations), "MathML/TeX annotation topology")
    for required_id in (
        "br-ak-2012-l29", "br-ak-2012-w29", "br-ak-2012-w29-solutions", "agc-media-credits-unit-29",
        "br-ak-2012-l30", "br-ak-2012-w30", "br-ak-2012-w30-solutions", "agc-media-credits-unit-30",
    ):
        require(required_id in id_set, f"required terminal HTML id absent: {required_id}")
    require(not re.search(r"(?i)\b(TODO|FIXME|PLACEHOLDER|MISSING IMAGE|BROKEN IMAGE)\b", soup.get_text(" ")),
            "visible placeholder/error residue in HTML")

    reader = PdfReader(PDF, strict=True)
    require(not reader.is_encrypted and len(reader.pages) == 504, "PDF page count/encryption")
    metadata = reader.metadata or {}
    require(metadata.get("/Title") == "Kurva Aljabar - Unit 1-30", "PDF title metadata")
    require(metadata.get("/Author") == "Holger Brenner (karya sumber)", "PDF author metadata")
    for page_number, page in enumerate(reader.pages, start=1):
        box = page.mediabox
        width = float(box.width)
        height = float(box.height)
        require(math.isclose(width, 595.276, abs_tol=0.02) and math.isclose(height, 841.89, abs_tol=0.02),
                f"non-A4 page geometry: {page_number}: {width}x{height}")
        require(int(page.get("/Rotate", 0) or 0) % 360 == 0, f"rotated PDF page: {page_number}")
    page_texts = [page.extract_text() or "" for page in reader.pages]
    markers = [
        "Kuliah 29: Proyeksi dan Kurva Proyektif Terparametrisasi",
        "Soal 29.10",
        "Solusi Soal 29.3",
        "Kuliah 30: Teorema Bézout",
        "Soal 30.12",
        "Solusi Soal 30.4",
        "Kredit media Unit 29",
        "Kredit media Unit 30",
    ]
    terminal_marker_pages: dict[str, int] = {}
    for marker in markers:
        pages = marker_pages(page_texts, marker)
        require(pages, f"PDF marker absent: {marker}")
        terminal_marker_pages[marker] = max(pages)
    order = [terminal_marker_pages[marker] for marker in markers]
    require(order == sorted(order), f"terminal PDF marker order: {terminal_marker_pages}")
    terminal_start = terminal_marker_pages[markers[0]]
    require(
        terminal_start > baseline_machine["pdf"]["terminal_start_page"],
        "Unit 29 does not follow the accepted Unit 28 terminal-content start",
    )
    require(terminal_marker_pages["Kredit media Unit 30"] == 504, "Unit 30 credits are not on the terminal page")

    authority_rows: dict[str, Any] = {}
    for unit in (29, 30):
        payload = translations[unit]
        translation = payload["translation"]
        authority_rows[str(unit)] = {
            "exercises": translation["worksheet_exercises"],
            "public_solutions": translation["public_solutions"],
            "media_positions": translation["reader_media_positions"],
            "translation_qa": bound[TRANSLATION[unit].relative_to(ROOT).as_posix()],
            "authority_manifest": payload["bound_facts"][f"authority/wikiversity/unit-{unit}/UNIT_AUTHORITY_MANIFEST.json"],
        }

    receipt = {
        "schema": "ag-bridge-cumulative-reader-qa-v5",
        "status": "PASS",
        "verified_date": "2026-08-28",
        "through_unit": 30,
        "language": "id-ID",
        "coverage": {
            "lectures": cumulative["lectures"],
            "worksheets": cumulative["worksheets"],
            "exercises": cumulative["exercises"],
            "public_source_solutions": cumulative["public_solutions"],
            "reader_media_positions": cumulative["media_positions"],
            "stable_source_ids": cumulative["stable_source_ids"],
            "mathml_nodes": len(math_nodes),
        },
        "html": {
            **bound[HTML.relative_to(ROOT).as_posix()],
            "ids": len(ids),
            "images": len(images),
            "embedded_images": len(embedded_images),
            "mathml_nodes": len(math_nodes),
            "tex_annotations": len(annotations),
            "internal_links": len(fragment_links),
            "broken_internal_links": 0,
            "remote_images": 0,
            "missing_local_images": 0,
            "empty_alt": 0,
        },
        "pdf": {
            **bound[PDF.relative_to(ROOT).as_posix()],
            "pages": len(reader.pages),
            "paper": "A4",
            "encrypted": False,
            "terminal_start_page": terminal_start,
            "terminal_pages_checked": len(reader.pages) - terminal_start + 1,
            "terminal_marker_pages": terminal_marker_pages,
        },
        "build_receipt": {
            **bound[BUILD.relative_to(ROOT).as_posix()],
            "input_count": len(inputs),
            "source_markdown_input_count": sum(1 for row in inputs if row["path"].startswith("source/id-ID/") and row["path"].endswith(".md")),
            "output_count": len(outputs),
            "html_log_bytes": html_log.stat().st_size,
            "pdf_log_bytes": pdf_log.stat().st_size,
            "pdf_log_sha256": bound[PDF_LOG.relative_to(ROOT).as_posix()]["sha256"],
            "pdf_warning_count": 0,
            "pdf_warning_disposition": "The portrait Unit 29 figure is print-stage constrained; both Pandoc logs are empty.",
        },
        "authority_units_29_30": authority_rows,
        "baseline_and_checkpoint_facts": [
            bound[BASELINE_MACHINE.relative_to(ROOT).as_posix()],
            bound[BASELINE_PROTECTED.relative_to(ROOT).as_posix()],
            bound[TRANSLATION[29].relative_to(ROOT).as_posix()],
            bound[TRANSLATION[30].relative_to(ROOT).as_posix()],
        ],
        "checks": [
            "exact accepted Unit 28 machine/protected baselines are byte-pinned",
            "Unit 29 and Unit 30 translation-QA receipts are PASS and byte-pinned",
            "all build-receipt inputs and both output identities replay exactly",
            "complete 30-unit coverage counts are inherited from the verified Unit 30 source closure",
            "HTML IDs, MathML/TeX annotations, alternative text, internal anchors, and local image closure pass",
            "PDF metadata, 504 A4 page geometries, encryption state, and ordered Unit 29-30 terminal markers pass",
            "both Pandoc warning logs are empty after the portrait Unit 29 figure is constrained only in the PDF stage",
            "no visible placeholder/error residue remains",
        ],
        "provenance": MODEL,
    }
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "status": "PASS",
        "receipt": OUT.relative_to(ROOT).as_posix(),
        "bytes": OUT.stat().st_size,
        "sha256": digest(OUT),
        "html_ids": len(ids),
        "images": len(images),
        "mathml_nodes": len(math_nodes),
        "internal_links": len(fragment_links),
        "pdf_pages": len(reader.pages),
        "terminal_marker_pages": terminal_marker_pages,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
