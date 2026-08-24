#!/usr/bin/env python3
"""Fail-closed cumulative reader QA through the frozen Unit 18 milestone."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source" / "id-ID"
BUILD = ROOT / "build" / "reader-id"
QA = ROOT / "qa"
HTML = BUILD / "index.html"
PDF = BUILD / "algebraic-geometry-bridge-id-units-01-18.pdf"
RECEIPT = BUILD / "BUILD_RECEIPT.json"
OUT = QA / "UNITS_01_18_MACHINE_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra."

BASELINE_FACTS = {
    "qa/UNIT_15_RELEASE_CANDIDATE.json": (6263, "da14d1c5773e2235bbfb59d3c462396dc24e3f753599a87dee395ad834b243f3"),
    "qa/UNITS_01_15_MACHINE_QA.json": (18674, "ee2d2f8ea2b181eeee32177e0320a0e8450f64744189708e53f394ec02edc38e"),
    "qa/UNITS_01_15_VISUAL_QA.json": (3807, "ec29a754845159ab8f236821dcf32c71202344c745c0521f23edd28e26aa0461"),
    "qa/UNITS_01_15_RESPONSIVE_QA.json": (2915, "edaafd54d7bafcddf175b4e456cf3a801be88b196333fe7333bdaeeadb455de5"),
    "qa/UNIT_15_PROTECTED_SURFACES.json": (9656, "633df9e390d6aceb55baf40f7ddc79173963a076593c0ba68d83f8fa7e245a3b"),
}
NEW_QA_FACTS = {
    "qa/UNIT_16_TRANSLATION_QA.json": (4373, "02ff081cd808172438262846944763e25871f6805a6a6f59bee933e3bf1fda19"),
    "qa/UNIT_17_TRANSLATION_QA.json": (3630, "738a9d27d620c55770e17a0bcb089ae756cfa632262074a94f02393498a1d8be"),
    "qa/UNIT_18_TRANSLATION_QA.json": (3610, "9a0d480dc799bb53669e324a324f43f89d9672a7d3bf5a5cdae9cd45e3dd669c"),
}
SOURCE_FACTS = {
    "source/id-ID/frontmatter-units-01-18.md": (2896, "2b24a7d9c28a311768f206a270191598b6a233a0338f237628c2bac80437c4be"),
    "source/id-ID/lecture-16.md": (16456, "c7cb0a1bc34e2003db18024d206c87d522a8df2082d186456d7a987cf0775d39"),
    "source/id-ID/worksheet-16.md": (11252, "871ea30f571ebc9e0e2a7b1e4d30cddfe719822f48b2bdbe97bd6d8a52a5268a"),
    "source/id-ID/worksheet-16-solutions.md": (9286, "5df1b9f46ba65622644feed0bf99191d5737d2edc2cc887c3b00efd2b50f8860"),
    "source/id-ID/media-credits-unit-16.md": (1316, "4a5bc83795b780ad26bffe425924bb010b966ed49dcbd0c3b073bc3be77f7a99"),
    "source/id-ID/lecture-17.md": (15109, "53bdc1f91f02a4b28dcc0c78247ef2ab9f5102377d8d0b6eedc88ed6879f37e8"),
    "source/id-ID/worksheet-17.md": (15940, "2ec3c00332fad5683d56d9a608bf6544371732207312c4dc77c479621624efa0"),
    "source/id-ID/worksheet-17-solutions.md": (5104, "5a56a15a9cb38ef4859a53ccd690309965c22a1fef54b018f162ec12fac6adef"),
    "source/id-ID/media-credits-unit-17.md": (451, "2647366a9bad10aff220f263a3a9c14d3620c43b42c0b4d2195e0c38d263f537"),
    "source/id-ID/lecture-18.md": (14716, "319cca4f08a3a4ee0bf0fa2a9d525e0adcd2f6f639705dd1c2eb06580b7bfcd3"),
    "source/id-ID/worksheet-18.md": (14530, "ec760a90d6f7462dbe71f755149886006e144bedc8ce11d09f72452472ee641e"),
    "source/id-ID/worksheet-18-solutions.md": (9027, "10fcda87b4613fdf6bd037b8428ee46b82ffbfa73c182dbb3732602d0f683db4"),
    "source/id-ID/media-credits-unit-18.md": (789, "9e1f8c342873acbe70a43ab88718bba67cbe4ed10672afb77f2ed5c41a78f0c5"),
}
BUILD_FACTS = {
    "build/reader-id/BUILD_RECEIPT.json": (29068, "4b11ab1cdad6f8685133e3c5c0facc2bcce7de8ede7e060b558c8f6d9ecfbeb9"),
    "build/reader-id/index.html": (11555390, "fab05aac5a84b45ee36260d895dcf89e2ad2d13fd6b7545eba2ae4c2e3db2f0a"),
    "build/reader-id/algebraic-geometry-bridge-id-units-01-18.pdf": (6905745, "ba62b61759a50925dcefa1a3a0153c8b597ee1386dd2033b610dae622e33ed99"),
    "build/reader-id/pandoc-html.log": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "build/reader-id/pandoc-pdf.log": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
}
UNIT_SPEC = {
    16: {
        "manifest": (118777, "54c823b4aa99c6e37e1fd3f84754f290bb54500847800906569704c3b4d49da0"),
        "map": (11533, "835029f5f5f46dea23486bd62edec6f4ab64667192c44504fee3af259e5b5266"),
        "rights": (5125, "f7472100f99256c04367f0c8f6f41fa7eef361fbb60044a13fcd0c8f76a019ea"),
        "closure": (4952, "561184965af9c75ee6812a103a435af9cf74f1c1b60ac7007b851ce66b5df555"),
        "exercises": 23,
        "solutions": [1, 10, 11, 12, 13, 15],
        "media": 4,
    },
    17: {
        "manifest": (116257, "c6747335c58fb3b4303cf3095705df7f991143f79d2d3598582a1cc8c99bef1a"),
        "map": (13819, "f329f9d1a6fc2e862009acd4761ed8289da2cf4c8b42e057db275642c05a700e"),
        "rights": (443, "6b8de6f5a63f32d9f22e7fb69c98ba2d787121a2437a392602571504c2a1c544"),
        "closure": (3013, "87c3d88789d822210b388e0c21e0e25a7418e77930e245ab2bc32916a0508d4f"),
        "exercises": 39,
        "solutions": [3, 12, 31, 32],
        "media": 0,
    },
    18: {
        "manifest": (106298, "26a56a0ccad60414bf09320dc008d438ccf84b3dd11c12c31e80fa6088437033"),
        "map": (11943, "8b55ef14cccbcab93ba99882d16e0f9888780353f7290eff8e1d2d6cd6bc4cd9"),
        "rights": (1998, "8cbf29b0063c2463fe89f9dec67bda671f9ee366db2c91176e37d4ef3532fbb0"),
        "closure": (4025, "69bfe604847dbb57fa21e07f8308901f02b87fba92c668b2b0fec27e3c2e8ad3"),
        "exercises": 28,
        "solutions": [3, 4, 10, 11, 15],
        "media": 1,
    },
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


def check_fact(relative: str, fact: tuple[int, str]) -> dict[str, Any]:
    path = ROOT / relative
    require(path.is_file() and not path.is_symlink(), f"missing/nonregular file: {relative}")
    actual = (path.stat().st_size, digest(path))
    require(actual == fact, f"identity drift for {relative}: {actual} != {fact}")
    return {"path": relative, "bytes": actual[0], "sha256": actual[1]}


def main() -> int:
    facts = []
    for group in (BASELINE_FACTS, NEW_QA_FACTS, SOURCE_FACTS, BUILD_FACTS):
        facts.extend(check_fact(relative, fact) for relative, fact in group.items())
    for relative in BASELINE_FACTS:
        payload = json.loads((ROOT / relative).read_text(encoding="utf-8"))
        require(str(payload.get("status", "")).startswith("PASS"), f"baseline status: {relative}")
    for relative in NEW_QA_FACTS:
        payload = json.loads((ROOT / relative).read_text(encoding="utf-8"))
        require(payload.get("status") == "PASS", f"per-unit QA status: {relative}")

    authority_summary: dict[str, Any] = {}
    for unit, spec in UNIT_SPEC.items():
        paths = {
            "manifest": f"authority/wikiversity/unit-{unit:02d}/UNIT_AUTHORITY_MANIFEST.json",
            "map": f"authority/wikiversity/unit-{unit:02d}/ORDERED_EXERCISE_MAP.json",
            "rights": f"authority/RIGHTS-unit-{unit:02d}.csv",
            "closure": f"authority/ASSET_CLOSURE-unit-{unit:02d}.json",
        }
        for key, relative in paths.items():
            facts.append(check_fact(relative, spec[key]))
        manifest = json.loads((ROOT / paths["manifest"]).read_text(encoding="utf-8"))
        mapping = json.loads((ROOT / paths["map"]).read_text(encoding="utf-8"))
        closure = json.loads((ROOT / paths["closure"]).read_text(encoding="utf-8"))
        require(manifest["unit_number"] == unit, f"manifest unit {unit}")
        require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, f"lecture closure unit {unit}")
        require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, f"worksheet closure unit {unit}")
        require(mapping["exercise_count"] == spec["exercises"], f"exercise count unit {unit}")
        solutions = [row["exercise_number"] for row in mapping["entries"] if row["has_public_solution"]]
        require(solutions == spec["solutions"], f"solution topology unit {unit}")
        require(closure["reader_media_positions"] == spec["media"], f"media positions unit {unit}")
        authority_summary[str(unit)] = {"exercises": spec["exercises"], "solutions": solutions, "media_positions": spec["media"], "manifest_sha256": spec["manifest"][1]}

    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    require(receipt["schema"] == "ag-bridge-build-receipt-v2", "build receipt schema")
    require(receipt["through_unit"] == 18 and receipt["language"] == "id-ID", "build scope/language")
    require(receipt["title"] == "Kurva Aljabar - Unit 1-18", "build title")
    input_rows = {row["path"]: row for row in receipt["inputs"]}
    output_rows = {row["path"]: row for row in receipt["outputs"]}
    require(set(output_rows) == {"build/reader-id/index.html", "build/reader-id/algebraic-geometry-bridge-id-units-01-18.pdf"}, "build output set")
    for relative, fact in SOURCE_FACTS.items():
        require(input_rows.get(relative, {}).get("bytes") == fact[0], f"receipt input bytes: {relative}")
        require(input_rows.get(relative, {}).get("sha256") == fact[1], f"receipt input hash: {relative}")
    for relative in ("build/reader-id/index.html", "build/reader-id/algebraic-geometry-bridge-id-units-01-18.pdf"):
        fact = BUILD_FACTS[relative]
        require(output_rows[relative]["bytes"] == fact[0] and output_rows[relative]["sha256"] == fact[1], f"receipt output identity: {relative}")
    for row in receipt["inputs"]:
        path = ROOT / row["path"]
        require(path.is_file() and not path.is_symlink(), f"receipt input missing: {row['path']}")
        require(path.stat().st_size == row["bytes"] and digest(path) == row["sha256"], f"receipt input drift: {row['path']}")

    source_paths = [ROOT / row["path"] for row in receipt["inputs"] if row["path"].startswith("source/id-ID/") and row["path"].endswith(".md")]
    source_raw = "\n".join(path.read_text(encoding="utf-8") for path in source_paths)
    stable_ids = re.findall(r"\{#([A-Za-z][A-Za-z0-9_.:-]*)\}", source_raw)
    require(len(stable_ids) == 1046 and len(stable_ids) == len(set(stable_ids)), f"stable source ID closure: {len(stable_ids)}")
    exercise_count = len(re.findall(r"^### Soal \d+\.\d+", source_raw, flags=re.M))
    solution_count = len(re.findall(r"^## Solusi Soal \d+\.\d+", source_raw, flags=re.M))
    require(exercise_count == 513, f"exercise total: {exercise_count}")
    require(solution_count == 90, f"solution total: {solution_count}")
    require(MODEL in source_raw, "exact model provenance")
    require(all(token not in source_raw.casefold() for token in ("todo", "fixme", "tbd", "placeholder")), "source placeholder residue")
    require(not re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|access[_-]?token|bearer\s+[A-Za-z0-9._-]{20,}", source_raw, flags=re.I), "secret-like source content")

    html_raw = HTML.read_text(encoding="utf-8")
    soup = BeautifulSoup(html_raw, "html.parser")
    require(soup.html is not None and soup.html.get("lang") == "id-ID", "HTML language")
    require(soup.title is not None and soup.title.get_text(strip=True) == "Kurva Aljabar - Unit 1-18", "HTML title")
    html_ids = [tag["id"] for tag in soup.find_all(id=True)]
    require(len(html_ids) == 2011 and len(html_ids) == len(set(html_ids)), "HTML ID uniqueness/count")
    missing_ids = [identifier for identifier in stable_ids if soup.find(id=identifier) is None]
    require(not missing_ids, f"source IDs absent from HTML: {missing_ids[:5]}")
    images = soup.find_all("img")
    require(len(images) == 74, f"HTML media count: {len(images)}")
    require(all(image.get("alt", "").strip() for image in images), "empty HTML image alt")
    require(all(not str(image.get("src", "")).startswith(("http://", "https://")) for image in images), "remote HTML image")
    internal = [anchor.get("href", "")[1:] for anchor in soup.find_all("a", href=True) if anchor.get("href", "").startswith("#")]
    html_id_set = set(html_ids)
    broken = [target for target in internal if target not in html_id_set]
    require(not broken, f"broken internal anchors: {broken[:5]}")
    require(len(soup.find_all("math")) == 7186, "MathML node count")
    require("１３２人目" in html_raw, "exact Japanese creator account absent from HTML")
    html_text = soup.get_text(" ", strip=True)
    for marker in ("Kuliah 16: Filter Tak Tereduksi", "Soal 16.23", "Solusi Soal 16.15", "Kuliah 17: Gelanggang Monoid", "Soal 17.39", "Solusi Soal 17.32", "Kuliah 18: Kurva Monomial", "Soal 18.28", "Solusi Soal 18.15", "Kredit media Unit 18"):
        require(marker in html_text, f"HTML marker absent: {marker}")
    require("pending_component_audit" not in html_raw and "<!-- QA:" not in html_raw, "HTML unresolved marker")

    reader = PdfReader(PDF, strict=True)
    require(not reader.is_encrypted, "PDF encrypted")
    require(reader.metadata is not None and reader.metadata.title == "Kurva Aljabar - Unit 1-18", "PDF title metadata")
    require(len(reader.pages) == 320, f"PDF page count: {len(reader.pages)}")
    pdf_text_parts = []
    for index, page in enumerate(reader.pages, start=1):
        box = page.mediabox
        require(abs(float(box.width) - 595.276) < 1 and abs(float(box.height) - 841.89) < 1, f"non-A4 page {index}")
        pdf_text_parts.append(page.extract_text() or "")
    pdf_text = "\n".join(pdf_text_parts)
    for marker in ("Kuliah 16", "Soal 16.23", "Solusi Soal 16.15", "Kuliah 17", "Soal 17.39", "Solusi Soal 17.32", "Kuliah 18", "Soal 18.28", "Solusi Soal 18.15", "Kredit media Unit 18", "132ninme"):
        require(marker in pdf_text, f"PDF marker absent: {marker}")
    require("pending_component_audit" not in pdf_text, "PDF unresolved marker")

    result = {
        "schema": "ag-bridge-cumulative-reader-qa-v3",
        "status": "PASS",
        "verified_date": "2026-08-24",
        "through_unit": 18,
        "language": "id-ID",
        "coverage": {"lectures": 18, "worksheets": 18, "exercises": 513, "public_source_solutions": 90, "reader_media_positions": 74, "stable_source_ids": 1046, "mathml_nodes": 7186},
        "html": {"path": "build/reader-id/index.html", "bytes": HTML.stat().st_size, "sha256": digest(HTML), "ids": len(html_ids), "images": len(images), "mathml_nodes": len(soup.find_all("math")), "internal_links": len(internal), "broken_internal_links": 0, "remote_images": 0, "empty_alt": 0},
        "pdf": {"path": "build/reader-id/algebraic-geometry-bridge-id-units-01-18.pdf", "bytes": PDF.stat().st_size, "sha256": digest(PDF), "pages": len(reader.pages), "paper": "A4", "encrypted": False},
        "build_receipt": {"path": "build/reader-id/BUILD_RECEIPT.json", "bytes": RECEIPT.stat().st_size, "sha256": digest(RECEIPT), "input_count": len(receipt["inputs"]), "output_count": len(receipt["outputs"]), "html_log_bytes": 0, "pdf_log_bytes": 0},
        "authority_units_16_18": authority_summary,
        "baseline_and_new_facts": facts,
        "checks": ["unit_15_verified_baseline_bound", "units_16_18_authority_solution_media_rights_closure", "all_build_receipt_inputs_replayed", "source_id_exercise_solution_and_provenance_closure", "html_mathml_media_alt_anchor_and_local_resource_closure", "pdf_a4_metadata_page_and_terminal_marker_closure", "warning_logs_empty", "no_placeholder_or_secret_like_source_content"],
        "provenance": MODEL,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "receipt": OUT.relative_to(ROOT).as_posix(), "bytes": OUT.stat().st_size, "sha256": digest(OUT), "pages": len(reader.pages), "mathml": len(soup.find_all('math'))}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
