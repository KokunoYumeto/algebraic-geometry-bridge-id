#!/usr/bin/env python3
"""Fail-closed machine QA for the cumulative Indonesian BGK Units 1--6 reader.

This verifier is deliberately non-visual.  It binds the frozen Unit 5 and Unit
6 translation gates, replays every input and output in the deterministic build
receipt, validates the self-contained semantic HTML surface, and checks the
82-page A4 PDF with both pypdf and Poppler.  The owner records the independent
all-page raster review separately.
"""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

from bs4 import BeautifulSoup
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build" / "reader-bgk-id"
HTML = BUILD / "index.html"
PDF = BUILD / "bundel-berkas-dan-kohomologi-id-units-01-06.pdf"
RECEIPT = BUILD / "BUILD_RECEIPT.json"
UNIT_05_QA = ROOT / "qa" / "BGK_UNIT_05_TRANSLATION_QA.json"
UNIT_06_QA = ROOT / "qa" / "BGK_UNIT_06_TRANSLATION_QA.json"
BUILDER = ROOT / "scripts" / "build_bgk_reader.py"
OUT = ROOT / "qa" / "BGK_UNITS_01_06_READER_QA.json"

EXPECTED = {
    HTML: {
        "bytes": 3_272_151,
        "sha256": "feb45d21d6168feaedf35719fdcb0b7f5532687846041d9fd75573c6d66fc5e9",
    },
    PDF: {
        "bytes": 896_202,
        "sha256": "f89a622f15acab90f683fb2a0b72a150363fc71d0f41f971c48b8c8ee43c2c9b",
    },
    RECEIPT: {
        "bytes": 10_118,
        "sha256": "e69b24950f0d7ede5cf8c33b6bec32298c08555758936193e1bb4a002844937b",
    },
    UNIT_05_QA: {
        "bytes": 6_137,
        "sha256": "95735e6853026cd7c6a4eea0ccd9d53dfdd22d25cea017ae3297cc9c35668f68",
    },
    UNIT_06_QA: {
        "bytes": 10_661,
        "sha256": "9b2c3c3a89f5ff48432d68ac26363b78d408e86ce9abfc42ad45b88d99b4fe9e",
    },
    BUILDER: {
        "bytes": 14_399,
        "sha256": "10a96cc77ddb925a0e16fe7c368a60e83b38f46bf333a5588f5777c78d5a20c6",
    },
}

EXPECTED_TITLE = "Bundel, Berkas, dan Kohomologi - Unit 1-6"
EXPECTED_PDF_PAGES = 82
EXPECTED_PDF_BOX = (0.0, 0.0, 595.276, 841.89)
EXPECTED_PDF_TRAILER_ID = "85f46ebc2256d17c65a4e0e71b4bab23"
EXPECTED_PDFTOTEXT = {
    "bytes": 214_187,
    "sha256": "567027cbae2ba3980c4f36740aae08a3f996ddb0dab7cb116d09251107e9c3ff",
}
PDF_ID_PATTERN = re.compile(
    rb"/ID \[ <([0-9A-Fa-f]{32})> <([0-9A-Fa-f]{32})> \]"
)
SOURCE_ID_PATTERN = re.compile(r"\{#([A-Za-z][A-Za-z0-9_.:-]*)[^}]*\}")
SOURCE_SOLUTION_PATTERN = re.compile(
    r"^## Solusi sumber untuk Soal (\d+\.\d+)\s+\{#[^}]+\}\s*$", re.MULTILINE
)
REMOTE_STYLE_PATTERN = re.compile(
    r"(?:url\s*\(\s*|@import\s+)[\"']?https?://", re.IGNORECASE
)
FONT_ROW_PATTERN = re.compile(
    r"^(?P<name>\S+)\s+(?P<type>.+?)\s+(?P<encoding>\S+)\s+"
    r"(?P<embedded>yes|no)\s+(?P<subset>yes|no)\s+(?P<unicode>yes|no)\s+"
    r"(?P<object>\d+)\s+(?P<generation>\d+)\s*$"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fact(path: Path) -> dict[str, object]:
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def require_regular(path: Path) -> None:
    require(path.is_file() and not path.is_symlink(), f"missing/nonregular file: {path}")


def require_expected_fact(path: Path) -> dict[str, object]:
    require_regular(path)
    observed = fact(path)
    expected = EXPECTED[path]
    require(observed["bytes"] == expected["bytes"], f"byte mismatch: {path}")
    require(observed["sha256"] == expected["sha256"], f"SHA-256 mismatch: {path}")
    return observed


def receipt_path(relative: str) -> Path:
    require(isinstance(relative, str) and relative, "empty receipt path")
    path = (ROOT / relative).resolve()
    require(path.is_relative_to(ROOT.resolve()), f"receipt path escapes lane: {relative}")
    return path


def replay_receipt_row(row: dict[str, object]) -> dict[str, object]:
    path = receipt_path(str(row.get("path", "")))
    require_regular(path)
    observed = fact(path)
    require(observed["bytes"] == row.get("bytes"), f"receipt byte replay failed: {path}")
    require(observed["sha256"] == row.get("sha256"), f"receipt hash replay failed: {path}")
    return observed


def independent_byte_observations(path: Path) -> tuple[dict[str, object], dict[str, object]]:
    observations: list[dict[str, object]] = []
    for _ in range(2):
        payload = path.read_bytes()
        observations.append(
            {
                "bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
        )
    require(observations[0] == observations[1], f"two byte observations differ: {path}")
    return observations[0], observations[1]


def run_tool(executable: str, *arguments: str, text: bool = True) -> subprocess.CompletedProcess:
    tool = shutil.which(executable)
    require(bool(tool), f"required executable unavailable: {executable}")
    return subprocess.run(
        [str(tool), *arguments],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
        encoding="utf-8" if text else None,
        errors="replace" if text else None,
    )


def parse_pdfinfo(output: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in output.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


def parse_pdffonts(output: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in output.splitlines()[2:]:
        if not line.strip():
            continue
        match = FONT_ROW_PATTERN.match(line)
        require(match is not None, f"unparseable pdffonts row: {line!r}")
        rows.append(match.groupdict())
    return rows


def normalized_pdf_identity(payload: bytes) -> tuple[str, str, int]:
    matches = tuple(PDF_ID_PATTERN.finditer(payload))
    require(len(matches) == 1, f"expected one PDF trailer ID, found {len(matches)}")
    first, second = (item.decode("ascii").lower() for item in matches[0].groups())
    require(first == second, "PDF trailer IDs differ")
    zeroed = PDF_ID_PATTERN.sub(
        b"/ID [ <00000000000000000000000000000000> <00000000000000000000000000000000> ]",
        payload,
    )
    recomputed = hashlib.sha256(zeroed).hexdigest()[:32]
    require(first == recomputed, "normalized PDF trailer ID is not content-derived")
    return first, recomputed, len(matches)


def main() -> int:
    bound_facts = {path: require_expected_fact(path) for path in EXPECTED}

    unit_qa: dict[int, dict[str, object]] = {}
    for unit, path in ((5, UNIT_05_QA), (6, UNIT_06_QA)):
        data = json.loads(path.read_text(encoding="utf-8"))
        require(data.get("schema") == "ag-bridge-bgk-unit-translation-qa-v1", f"Unit {unit} QA schema")
        require(data.get("unit") == unit, f"Unit {unit} QA unit")
        require(data.get("language") == "id-ID", f"Unit {unit} QA language")
        require(data.get("status") == "PASS", f"Unit {unit} translation gate is not PASS")
        unit_qa[unit] = data

    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    require(receipt.get("schema") == "ag-bridge-bgk-build-receipt-v1", "build receipt schema")
    require(receipt.get("through_unit") == 6, "build receipt scope")
    require(receipt.get("language") == "id-ID", "build receipt language")
    require(receipt.get("title") == EXPECTED_TITLE, "build receipt title")
    require(receipt.get("source_date_epoch") == "1787875200", "build receipt source epoch")
    require(receipt.get("built_utc") == "2026-08-28T00:00:00+00:00", "build receipt pinned timestamp")
    require(receipt.get("pandoc") == "pandoc 3.9.0.2", "build receipt Pandoc identity")
    require(
        receipt.get("latex") == "This is LuaHBTeX, Version 1.25.7 (MiKTeX 26.5)",
        "build receipt LuaHBTeX identity",
    )
    require(receipt.get("normalized_pdf_trailer_id") == EXPECTED_PDF_TRAILER_ID, "receipt trailer ID")
    require(receipt.get("html_main_landmark") == "main#main-content", "receipt main binding")
    require(
        receipt.get("html_skip_link") == "a.skip-link[href='#main-content']",
        "receipt skip-link binding",
    )
    require(len(receipt.get("inputs", [])) == 52, "build input closure count")
    require(len(receipt.get("outputs", [])) == 2, "build output closure count")
    receipt_inputs = [replay_receipt_row(row) for row in receipt["inputs"]]
    receipt_outputs = [replay_receipt_row(row) for row in receipt["outputs"]]
    output_paths = {row["path"] for row in receipt["outputs"]}
    require(
        output_paths
        == {
            "build/reader-bgk-id/index.html",
            "build/reader-bgk-id/bundel-berkas-dan-kohomologi-id-units-01-06.pdf",
        },
        "build output path closure",
    )

    receipt_input_by_path = {row["path"]: row for row in receipt["inputs"]}
    for unit, data in unit_qa.items():
        for row in data.get("translation_files", []):
            built = receipt_input_by_path.get(row.get("path"))
            require(built is not None, f"Unit {unit} QA translation absent from build receipt")
            require(
                built.get("bytes") == row.get("bytes") and built.get("sha256") == row.get("sha256"),
                f"Unit {unit} translation/build cross-binding failed: {row.get('path')}",
            )

    frontmatter_path = receipt_path("source/id-ID/bgk/frontmatter-bgk-units-01-06.md")
    frontmatter_text = re.sub(
        r"\s+", " ", frontmatter_path.read_text(encoding="utf-8")
    )
    require(
        "seluruh 101 soal, dan tiga solusi publik" in frontmatter_text,
        "frontmatter does not disclose the exact 101-exercise/3-solution closure",
    )
    require(
        "mendokumentasikan 98 hasil negatif" in frontmatter_text,
        "frontmatter does not disclose the exact 98 negative solution checks",
    )

    expected_exercises_by_unit = {1: 17, 2: 27, 3: 18, 4: 9, 5: 11, 6: 19}
    exercises_by_unit: dict[int, int] = {}
    public_solutions: list[str] = []
    for unit, expected_count in expected_exercises_by_unit.items():
        worksheet_path = receipt_path(f"source/id-ID/bgk/worksheet-{unit:02d}.md")
        worksheet_text = worksheet_path.read_text(encoding="utf-8")
        exercise_ids = re.findall(
            rf"^## Soal {unit}\.(\d+)(?:\*)?\s+\{{#br-bgk-2019-w{unit:02d}-ex\d+\}}\s*$",
            worksheet_text,
            flags=re.MULTILINE,
        )
        require(
            len(exercise_ids) == expected_count,
            f"Unit {unit} exercise closure: {len(exercise_ids)} != {expected_count}",
        )
        require(
            [int(number) for number in exercise_ids] == list(range(1, expected_count + 1)),
            f"Unit {unit} exercise order/number closure",
        )
        exercises_by_unit[unit] = len(exercise_ids)

        solutions_path = receipt_path(
            f"source/id-ID/bgk/worksheet-{unit:02d}-solutions.md"
        )
        public_solutions.extend(
            SOURCE_SOLUTION_PATTERN.findall(
                solutions_path.read_text(encoding="utf-8")
            )
        )

    total_exercises = sum(exercises_by_unit.values())
    require(total_exercises == 101, f"cumulative exercise closure: {total_exercises}")
    require(public_solutions == ["2.4", "3.1", "5.5"], "public-solution identity/order closure")
    negative_solution_checks = total_exercises - len(public_solutions)
    require(negative_solution_checks == 98, "negative solution-check closure")

    html_payload = HTML.read_bytes()
    soup = BeautifulSoup(html_payload, "html.parser")
    require(soup.html is not None and soup.html.get("lang") == "id-ID", "HTML language")
    require(soup.title is not None and soup.title.get_text(strip=True) == EXPECTED_TITLE, "HTML title")
    viewport = soup.select("meta[name='viewport']")
    require(len(viewport) == 1, "HTML viewport count")
    require(
        viewport[0].get("content") == "width=device-width, initial-scale=1.0, user-scalable=yes",
        "HTML scalable viewport",
    )

    html_ids = [str(node.get("id")) for node in soup.find_all(id=True)]
    id_counts = collections.Counter(html_ids)
    duplicate_ids = sorted(identifier for identifier, count in id_counts.items() if count > 1)
    require(len(html_ids) == 492, f"HTML ID count: {len(html_ids)}")
    require(not duplicate_ids, f"duplicate HTML IDs: {duplicate_ids[:5]}")

    source_ids: list[str] = []
    for row in receipt["inputs"]:
        relative = str(row["path"])
        if relative.endswith(".md"):
            source_ids.extend(SOURCE_ID_PATTERN.findall(receipt_path(relative).read_text(encoding="utf-8")))
    require(len(source_ids) == len(set(source_ids)) == 254, "explicit source-ID closure")
    missing_source_ids = sorted(identifier for identifier in source_ids if id_counts[identifier] != 1)
    require(not missing_source_ids, f"source IDs missing/nonunique in HTML: {missing_source_ids[:5]}")

    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    require(len(headings) == 255, f"HTML heading count: {len(headings)}")
    require(sum(bool(node.get("id")) for node in headings) == 254, "HTML heading-ID count")

    hrefs = [str(node.get("href")) for node in soup.find_all(href=True)]
    internal_hrefs = [href for href in hrefs if href.startswith("#")]
    broken_internal = sorted(href for href in internal_hrefs if href[1:] not in id_counts)
    require(len(hrefs) == 247, f"HTML href count: {len(hrefs)}")
    require(len(internal_hrefs) == 237, f"HTML internal-href count: {len(internal_hrefs)}")
    require(not broken_internal, f"broken internal anchors: {broken_internal[:5]}")

    require(len(soup.find_all("header")) == 1, "HTML header landmark")
    require(len(soup.find_all("nav")) == 1, "HTML navigation landmark")
    require(len(soup.select("main#main-content")) == 1, "HTML main landmark")
    skip_links = soup.select("a.skip-link[href='#main-content']")
    require(len(skip_links) == 1, "HTML skip link")
    require(skip_links[0].get_text(" ", strip=True) == "Langsung ke isi utama", "skip-link label")

    images = soup.find_all("img")
    require(len(images) == 5, f"HTML image count: {len(images)}")
    require(all(image.get("alt", "").strip() for image in images), "empty/missing image alt")
    require(all(image.get("src", "").startswith("data:image/") for image in images), "non-embedded image")
    fetch_sources = soup.find_all(["img", "script", "iframe", "source", "video", "audio", "embed"], src=True)
    require(
        all(not str(node.get("src", "")).startswith(("http://", "https://")) for node in fetch_sources),
        "remote fetch source in self-contained HTML",
    )
    require(not soup.select("link[rel~=stylesheet][href]"), "external stylesheet link")
    require(not soup.find_all("object", attrs={"data": True}), "external/object data surface")
    require(not soup.find_all("script", src=True), "external script source")
    require(len(soup.find_all("style")) == 2, "embedded style-tag count")
    require(
        all(REMOTE_STYLE_PATTERN.search(style.get_text()) is None for style in soup.find_all("style")),
        "remote URL in embedded style",
    )

    mathml = soup.find_all("math")
    block_math = [node for node in mathml if node.get("display") == "block"]
    require(len(mathml) == 1_829, f"MathML node count: {len(mathml)}")
    require(len(block_math) == 497, f"block MathML count: {len(block_math)}")
    require(len(soup.find_all("script")) == 0, "script surface in static reader")
    require(len(soup.find_all("iframe")) == 0, "iframe surface in static reader")

    unit_05_ids = [
        identifier
        for identifier in html_ids
        if identifier.startswith(("br-bgk-2019-l05", "br-bgk-2019-w05"))
    ]
    unit_06_ids = [
        identifier
        for identifier in html_ids
        if identifier.startswith(("br-bgk-2019-l06", "br-bgk-2019-w06"))
    ]
    require(len(unit_05_ids) == 29, "Unit 5 HTML ID closure")
    require(len(unit_06_ids) == 45, "Unit 6 HTML ID closure")
    require(id_counts["agc-bgk-media-credits-unit-05"] == 1, "Unit 5 credits ID")
    require(id_counts["agc-bgk-media-credits-unit-06"] == 1, "Unit 6 credits ID")

    html_text = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
    text_markers = (
        "Kuliah 5: Berkasisasi, Homomorfisme, dan Berkas Hasil Bagi",
        "Soal 5.11",
        "Solusi Publik dan Cakupan Lembar Kerja 5",
        "Kredit media BGK Unit 5",
        "Kuliah 6: Eksak, Evaluasi Global, serta Tarik dan Dorong Berkas",
        "Soal 6.19",
        "Cakupan Solusi Publik Lembar Kerja 6",
        "Kredit media BGK Unit 6",
        "OpenAI Codex gpt-5.6-sol, Ultra.",
    )
    for marker in text_markers:
        require(marker in html_text, f"HTML text marker absent: {marker}")
    require(html_text.count("OpenAI Codex gpt-5.6-sol, Ultra.") == 1, "HTML provenance count")
    require("seluruh 101 soal, dan tiga solusi publik" in html_text, "HTML 101/3 closure disclosure")
    require("mendokumentasikan 98 hasil negatif" in html_text, "HTML 98-negative disclosure")

    # LuaTeX's positioned glyph stream is semantically complete, but pypdf
    # inserts a space inside the word "Tarik" in the Unit 6 heading.  Use the
    # unambiguous stable prefix for both independent PDF text extractors while
    # the HTML gate above checks the complete heading.
    pdf_text_markers = (
        "Kuliah 5: Berkasisasi, Homomorfisme, dan Berkas Hasil Bagi",
        "Soal 5.11",
        "Solusi Publik dan Cakupan Lembar Kerja 5",
        "Kredit media BGK Unit 5",
        "Kuliah 6: Eksak, Evaluasi Global",
        "Soal 6.19",
        "Cakupan Solusi Publik Lembar Kerja 6",
        "Kredit media BGK Unit 6",
        "OpenAI Codex gpt-5.6-sol, Ultra.",
    )

    reader = PdfReader(PDF, strict=True)
    require(not reader.is_encrypted, "PDF is encrypted")
    require(len(reader.pages) == EXPECTED_PDF_PAGES, f"pypdf page count: {len(reader.pages)}")
    require(reader.metadata is not None, "PDF metadata missing")
    require(reader.metadata.title == EXPECTED_TITLE, "PDF title metadata")
    require(reader.metadata.author == "Holger Brenner (karya sumber)", "PDF author metadata")

    link_annotations = 0
    out_of_bounds_links: list[dict[str, object]] = []
    page_boxes: list[tuple[float, float, float, float]] = []
    page_texts: list[str] = []
    for page_number, page in enumerate(reader.pages, 1):
        box = tuple(float(value) for value in (page.mediabox.left, page.mediabox.bottom, page.mediabox.right, page.mediabox.top))
        page_boxes.append(box)
        require(
            all(abs(observed - expected) <= 0.001 for observed, expected in zip(box, EXPECTED_PDF_BOX)),
            f"non-A4 media box on page {page_number}: {box}",
        )
        require(int(page.get("/Rotate", 0)) % 360 == 0, f"rotated PDF page: {page_number}")
        page_texts.append(page.extract_text() or "")
        for reference in page.get("/Annots") or []:
            annotation = reference.get_object()
            if annotation.get("/Subtype") != "/Link":
                continue
            link_annotations += 1
            rect = annotation.get("/Rect")
            require(rect is not None and len(rect) == 4, f"malformed link rectangle on page {page_number}")
            values = [float(value) for value in rect]
            x0, x1 = sorted((values[0], values[2]))
            y0, y1 = sorted((values[1], values[3]))
            if (
                x0 < box[0] - 0.01
                or x1 > box[2] + 0.01
                or y0 < box[1] - 0.01
                or y1 > box[3] + 0.01
                or x1 <= x0
                or y1 <= y0
            ):
                out_of_bounds_links.append({"page": page_number, "rect": values})
    require(len(set(page_boxes)) == 1, "PDF page-box inconsistency")
    require(link_annotations == 247, f"PDF link annotation count: {link_annotations}")
    require(not out_of_bounds_links, f"out-of-bounds PDF links: {out_of_bounds_links[:3]}")

    require(all(text.strip() for text in page_texts), "PDF page without extractable text")
    require(min(len(text) for text in page_texts) == 76, "minimum per-page text surface changed")
    require(sum(len(text) for text in page_texts) == 140_233, "pypdf extracted-text surface changed")
    pdf_text = re.sub(r"\s+", " ", " ".join(page_texts))
    for marker in pdf_text_markers:
        require(marker in pdf_text, f"pypdf text marker absent: {marker}")
    require("seluruh 101 soal, dan tiga solusi publik" in pdf_text, "pypdf 101/3 closure disclosure")
    require("mendokumentasikan 98 hasil negatif" in pdf_text, "pypdf 98-negative disclosure")
    require("pending_component_audit" not in pdf_text, "pending marker in PDF text")

    catalog = reader.trailer["/Root"]
    require(catalog.get("/AcroForm") is None, "PDF AcroForm present")
    names = catalog.get("/Names")
    if names is not None:
        names = names.get_object()
        require(names.get("/JavaScript") is None, "PDF JavaScript name tree present")
    mark_info = catalog.get("/MarkInfo")
    tagged = bool(mark_info and mark_info.get_object().get("/Marked"))
    require(not tagged, "unexpected tagged-PDF state")

    pdfinfo_process = run_tool("pdfinfo", str(PDF))
    require(not pdfinfo_process.stderr.strip(), f"pdfinfo stderr: {pdfinfo_process.stderr.strip()}")
    pdfinfo = parse_pdfinfo(pdfinfo_process.stdout)
    require(pdfinfo.get("Pages") == "82", "Poppler page count")
    require(pdfinfo.get("Page size") == "595.276 x 841.89 pts (A4)", "Poppler A4 page size")
    require(pdfinfo.get("Encrypted") == "no", "Poppler encryption state")
    require(pdfinfo.get("Tagged") == "no", "Poppler tagged state")
    require(pdfinfo.get("Form") == "none", "Poppler form state")
    require(pdfinfo.get("JavaScript") == "no", "Poppler JavaScript state")

    pdffonts_process = run_tool("pdffonts", str(PDF))
    require(not pdffonts_process.stderr.strip(), f"pdffonts stderr: {pdffonts_process.stderr.strip()}")
    fonts = parse_pdffonts(pdffonts_process.stdout)
    require(len(fonts) == 14, f"PDF font count: {len(fonts)}")
    require(all(row["embedded"] == "yes" for row in fonts), "unembedded PDF font")
    require(all(row["subset"] == "yes" for row in fonts), "nonsubset PDF font")
    require(all("Type 3" not in row["type"] for row in fonts), "Type 3 PDF font")
    require(sum(row["unicode"] == "yes" for row in fonts) == 13, "PDF Unicode font-map count")
    require(
        [row["name"] for row in fonts if row["unicode"] == "no"] == ["TMHVPV+MSAM10"],
        "unexpected font without Unicode map",
    )

    pdftotext_process = run_tool(
        "pdftotext", "-layout", "-enc", "UTF-8", str(PDF), "-", text=False
    )
    require(not pdftotext_process.stderr, f"pdftotext stderr bytes: {len(pdftotext_process.stderr)}")
    poppler_text = pdftotext_process.stdout
    require(len(poppler_text) == EXPECTED_PDFTOTEXT["bytes"], "Poppler text byte count")
    require(
        hashlib.sha256(poppler_text).hexdigest() == EXPECTED_PDFTOTEXT["sha256"],
        "Poppler text SHA-256",
    )
    poppler_text_decoded = poppler_text.decode("utf-8")
    for marker in pdf_text_markers:
        require(marker in poppler_text_decoded, f"Poppler text marker absent: {marker}")
    normalized_poppler_text = re.sub(r"\s+", " ", poppler_text_decoded)
    require(
        "seluruh 101 soal, dan tiga solusi publik" in normalized_poppler_text,
        "Poppler 101/3 closure disclosure",
    )
    require(
        "mendokumentasikan 98 hasil negatif" in normalized_poppler_text,
        "Poppler 98-negative disclosure",
    )

    pdf_payload = PDF.read_bytes()
    actual_id, recomputed_id, id_count = normalized_pdf_identity(pdf_payload)
    require(actual_id == EXPECTED_PDF_TRAILER_ID, "PDF trailer identity")
    require(receipt["normalized_pdf_trailer_id"] == recomputed_id, "receipt/content trailer-ID cross-binding")

    byte_replays: dict[str, dict[str, object]] = {}
    for label, path in (("html", HTML), ("pdf", PDF), ("build_receipt", RECEIPT)):
        first, second = independent_byte_observations(path)
        require(first == EXPECTED[path], f"{label} byte observation differs from frozen identity")
        byte_replays[label] = {"first": first, "second": second, "identical": True}

    result = {
        "schema": "ag-bridge-bgk-cumulative-reader-machine-qa-v1",
        "through_unit": 6,
        "language": "id-ID",
        "verified_date": "2026-08-29",
        "status": "PASS_MACHINE_READER_82_A4_PAGES",
        "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra.",
        "translation_gates": {
            "unit_05": {**bound_facts[UNIT_05_QA], "status": unit_qa[5]["status"]},
            "unit_06": {**bound_facts[UNIT_06_QA], "status": unit_qa[6]["status"]},
            "translation_files_cross_bound_to_build_receipt": 6,
        },
        "exercise_solution_closure": {
            "exercises_by_unit": {
                f"unit_{unit:02d}": count for unit, count in exercises_by_unit.items()
            },
            "total_exercises": total_exercises,
            "public_solution_ids": public_solutions,
            "public_solutions": len(public_solutions),
            "negative_solution_checks": negative_solution_checks,
            "invented_solutions": 0,
            "frontmatter_html_pypdf_and_poppler_disclosures_match": True,
        },
        "builder": {
            **bound_facts[BUILDER],
            "command": "python scripts/build_bgk_reader.py --through 6",
            "source_date_epoch": receipt["source_date_epoch"],
            "pandoc": receipt["pandoc"],
            "latex": receipt["latex"],
        },
        "build_receipt": {
            **bound_facts[RECEIPT],
            "input_records_replayed": len(receipt_inputs),
            "output_records_replayed": len(receipt_outputs),
            "all_input_and_output_bytes_match": True,
        },
        "deterministic_frozen_byte_replay": {
            "status": "PASS_TWO_INDEPENDENT_READS_MATCH_RECEIPT_BOUND_IDENTITIES",
            "scope": "non-mutating byte replay of the frozen artifacts; no build or visual claim",
            "observations_per_artifact": 2,
            "artifacts": byte_replays,
            "normalized_pdf_trailer_id": actual_id,
            "normalized_pdf_trailer_id_recomputed_from_zeroed_content": recomputed_id,
            "normalized_pdf_trailer_id_occurrences": id_count,
        },
        "html": {
            **bound_facts[HTML],
            "self_contained": True,
            "html_lang": "id-ID",
            "scalable_viewport": True,
            "embedded_style_tags": 2,
            "remote_fetch_sources": 0,
            "mathml_nodes": len(mathml),
            "block_math_nodes": len(block_math),
            "all_ids": len(html_ids),
            "explicit_source_ids": len(source_ids),
            "heading_nodes": len(headings),
            "heading_nodes_with_ids": sum(bool(node.get("id")) for node in headings),
            "duplicate_ids": 0,
            "hrefs": len(hrefs),
            "internal_anchors": len(internal_hrefs),
            "broken_internal_anchors": 0,
            "images": len(images),
            "embedded_data_images": len(images),
            "images_missing_alt": 0,
            "header_landmarks": 1,
            "navigation_landmarks": 1,
            "main_landmarks": 1,
            "skip_links": 1,
            "unit_05_ids": len(unit_05_ids),
            "unit_06_ids": len(unit_06_ids),
            "exact_model_provenance_occurrences": 1,
        },
        "pdf": {
            **bound_facts[PDF],
            "pages_pypdf": len(reader.pages),
            "pages_poppler": int(pdfinfo["Pages"]),
            "page_size": "A4",
            "page_box_points": list(EXPECTED_PDF_BOX),
            "page_box_variants": len(set(page_boxes)),
            "encrypted": False,
            "tagged": False,
            "forms": False,
            "javascript": False,
            "extractable_text_pages": sum(bool(text.strip()) for text in page_texts),
            "pypdf_extracted_text_characters": sum(len(text) for text in page_texts),
            "minimum_page_text_characters": min(len(text) for text in page_texts),
            "pdftotext_bytes": len(poppler_text),
            "pdftotext_sha256": hashlib.sha256(poppler_text).hexdigest(),
            "font_rows": len(fonts),
            "fonts_embedded": sum(row["embedded"] == "yes" for row in fonts),
            "fonts_subset": sum(row["subset"] == "yes" for row in fonts),
            "fonts_with_unicode_map": sum(row["unicode"] == "yes" for row in fonts),
            "type_3_fonts": 0,
            "link_annotations": link_annotations,
            "out_of_bounds_link_annotations": 0,
            "semantic_accessibility_surface": "Self-contained id-ID HTML with landmarks, MathML, alt text, and scalable viewport is primary; this deterministic PDF is untagged.",
        },
        "visual_review": {
            "included": False,
            "reason": "This receipt contains machine-verifiable facts only; the canonical owner binds the separate all-82-page raster review.",
        },
        "qa_script": fact(Path(__file__)),
        "check_families": [
            "unit_05_and_unit_06_translation_gate_hash_binding",
            "101_exercises_3_exact_public_solutions_and_98_negative_checks",
            "all_52_build_inputs_and_2_outputs_exact_receipt_replay",
            "two_independent_frozen_byte_observations_and_content_derived_pdf_id",
            "self_contained_id_ID_mathml_html_with_closed_ids_anchors_and_alt_text",
            "header_navigation_main_and_skip_link_landmarks",
            "82_A4_pages_in_pypdf_and_poppler",
            "complete_pypdf_and_poppler_text_extraction_with_boundary_markers",
            "all_fonts_embedded_subset_and_no_type_3_fonts",
            "all_247_pdf_link_annotations_within_page_bounds",
            "no_forms_javascript_encryption_or_blank_text_pages",
        ],
    }
    OUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
