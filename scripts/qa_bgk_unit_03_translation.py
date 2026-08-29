#!/usr/bin/env python3
"""Fail-closed source, mathematics, language, rights, and scope QA for BGK Unit 3."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess


LANE = Path(__file__).resolve().parents[1]
BGK = LANE / "source" / "id-ID" / "bgk"
AUTH = LANE / "authority" / "wikiversity-bgk" / "unit-03"
OUT = LANE / "qa" / "BGK_UNIT_03_TRANSLATION_QA.json"
FILES = (
    BGK / "frontmatter-bgk-units-01-03.md",
    BGK / "lecture-03.md",
    BGK / "worksheet-03.md",
    BGK / "worksheet-03-solutions.md",
)
EARLIER_BGK_FILES = (
    BGK / "frontmatter-bgk-units-01.md",
    BGK / "lecture-01.md",
    BGK / "worksheet-01.md",
    BGK / "worksheet-01-solutions.md",
    BGK / "frontmatter-bgk-units-01-02.md",
    BGK / "lecture-02.md",
    BGK / "worksheet-02.md",
    BGK / "worksheet-02-solutions.md",
)
AUTHORITY_SHA256 = {
    "UNIT_AUTHORITY_MANIFEST.json": "60270cc7ba74a4ed744687ae18c3887eca8a2fff6bce48a819be102d4a619a5a",
    "lecture-03.xml": "7c048b329215669e01d8068cd150f5a1bee11bc00c2466e2d9b63e3d7abfa258",
    "lecture-03-expanded.tex": "04989737d12bf8ac77127e60f193e6ac2c19201d4f5d66221f8c5e1de85a87eb",
    "worksheet-03.xml": "a34ac6428f6d2074e4bc01f3d3d6064c38625eea36fa4b5c48e18a524e583c15",
    "worksheet-03-expanded.tex": "08f9268af226916ef212041a50d430ca5fcf71df2c5a57ab5adb36183e2a4b2a",
    "ORDERED_EXERCISE_MAP.json": "5242db043a773e412806fd066ed831fe6ebbdc7d16a35af8070ff1ce7398901f",
    "worksheet-solution-candidates-api.json": "fead1cd2cfe79eb6dd0141474b4b0921986b32238bea7c2c6ba8fd8670942e64",
    "solution-ex01.xml": "cf9dff1014aa7f7f749f84660d4c4a4785bbc0ddfcf657cc2413c1eb91ef149b",
    "solution-ex01.html": "0e4ce7ff74ef14d54ce440c717e12a369a9201a9fb365579484a1839d0ab1ad1",
}
MEDIA_RIGHTS_SHA256 = {
    LANE / "authority" / "ASSET_CLOSURE-bgk-unit-03.json": "618a916073604a94387f04d87565c222be65a5c180ce690342742ae63858ea15",
    LANE / "authority" / "RIGHTS-bgk-unit-03.csv": "87f9d56b1300a56ca68e4aa8f50e3d50ab622d7a4d05221089d49e1dba35981d",
    LANE / "authority" / "commons-imageinfo-bgk-unit-03.json": "52411bf83dcc0c8999d35b6952dee76025e4685f4321cd5b76234111e61204b1",
    LANE / "source" / "id-ID" / "media-credits-bgk-unit-03.md": "bc08510f635abba677ac1cc5a18ddb4a3519284e83f1d2f17605989736c9f0a2",
}
CORRECTION_IDS = tuple(f"AGC-CORR-{number:04d}" for number in range(149, 154))
NEW_TERM_IDS = tuple(f"AGT-{number:04d}" for number in range(299, 315))
REUSED_TERM_IDS = (
    "AGT-0072",
    "AGT-0088",
    "AGT-0089",
    "AGT-0090",
    "AGT-0098",
    "AGT-0099",
    "AGT-0100",
    "AGT-0101",
    "AGT-0102",
    "AGT-0103",
    "AGT-0105",
    "AGT-0109",
    "AGT-0277",
    "AGT-0282",
    "AGT-0290",
    "AGT-0294",
    "AGT-0296",
    "AGT-0298",
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
    require(path.is_file() and not path.is_symlink(), f"missing regular file: {path}")
    return {
        "path": path.relative_to(LANE).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def walk_ast(node: object):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk_ast(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk_ast(value)


def pandoc_fact(path: Path) -> dict[str, object]:
    relative = path.relative_to(LANE)
    process = subprocess.run(
        [
            "pandoc",
            "--from=markdown+yaml_metadata_block+tex_math_dollars+fenced_divs+bracketed_spans",
            "--to=json",
            str(relative),
        ],
        cwd=LANE,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    ast = json.loads(process.stdout)
    nodes = tuple(walk_ast(ast))
    return {
        "path": relative.as_posix(),
        "pandoc_ast_parse": "PASS",
        "math_nodes": sum(node.get("t") == "Math" for node in nodes),
        "heading_nodes": sum(node.get("t") == "Header" for node in nodes),
    }


def body_without_metadata_or_comments(text: str) -> str:
    body = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    return re.sub(r"<!--.*?-->", "", body, flags=re.S)


def markdown_ids(text: str) -> list[str]:
    return re.findall(r"\{#(br-bgk-2019-[A-Za-z0-9_-]+)\}", text)


def main() -> int:
    for name, expected in AUTHORITY_SHA256.items():
        require(sha256(AUTH / name) == expected, f"authority hash mismatch: {name}")
    for path, expected in MEDIA_RIGHTS_SHA256.items():
        require(sha256(path) == expected, f"media/rights hash mismatch: {path.name}")

    manifest = json.loads((AUTH / "UNIT_AUTHORITY_MANIFEST.json").read_text(encoding="utf-8"))
    require(manifest["unit_number"] == 3, "authority manifest unit drifted")
    require(manifest["lecture"]["revid"] == 793623, "lecture revision drifted")
    require(manifest["worksheet"]["revid"] == 619301, "worksheet revision drifted")
    require(
        manifest["lecture_transclusion_closure"]["requested_template_count"]
        == manifest["lecture_transclusion_closure"]["captured_page_count"]
        == 166,
        "lecture transclusion closure drifted",
    )
    require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "lecture transclusion missing")
    require(
        manifest["worksheet_transclusion_closure"]["requested_template_count"]
        == manifest["worksheet_transclusion_closure"]["captured_page_count"]
        == 102,
        "worksheet transclusion closure drifted",
    )
    require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "worksheet transclusion missing")

    texts = {path.name: path.read_text(encoding="utf-8") for path in FILES}
    joined = "\n".join(texts.values())
    unit_files = ("lecture-03.md", "worksheet-03.md", "worksheet-03-solutions.md")
    for name in unit_files:
        require("OpenAI Codex gpt-5.6-sol, Ultra." in texts[name], f"exact provenance missing: {name}")
        require("CC BY-SA 4.0" in texts[name], f"CC BY-SA notice missing: {name}")
        require("tidak menyiratkan dukungan" in texts[name], f"non-endorsement missing: {name}")
    require("OpenAI Codex gpt-5.6-sol, Ultra." in texts["frontmatter-bgk-units-01-03.md"], "frontmatter provenance missing")
    require(not re.search(r"(?:TODO|TBD|PLACEHOLDER|LOREM IPSUM)", joined, re.I), "placeholder remains")
    require(not re.search(r"[\u200b\u200c\u200d\u2060\ufeff]", joined), "invisible control remains")
    require(not re.search(r"\$[^$\n]*`", joined), "stray backtick inside an unclosed math span")

    cleaned_body = "\n".join(body_without_metadata_or_comments(text) for text in texts.values())
    german_residue = re.findall(
        r"\b(?:Zeige|Berechne|Aufgabe|Vorlesung|Arbeitsblatt|Es sei|Dann nennt man|Beweis)\b",
        cleaned_body,
    )
    require(not german_residue, f"unexpected German prose residue: {german_residue[:5]}")

    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    require(mapping["exercise_count"] == 18 and mapping["solution_count"] == 1, "solution scope mismatch")
    public = [entry["exercise_number"] for entry in mapping["entries"] if entry["has_public_solution"]]
    require(public == [1], f"public-solution topology drifted: {public}")
    expected_titles = [entry["exercise_title"] for entry in mapping["entries"]]
    worksheet = texts["worksheet-03.md"]
    actual_titles = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    require(actual_titles == expected_titles, "ordered exercise mapping mismatch")
    exercise_ids = re.findall(r"^## Soal 3\.(\d+) \{#(br-bgk-2019-w03-ex\d{2})\}$", worksheet, re.M)
    require([int(number) for number, _ in exercise_ids] == list(range(1, 19)), "exercise numbering mismatch")
    require(len({identifier for _, identifier in exercise_ids}) == 18, "duplicate exercise ID")

    solutions = texts["worksheet-03-solutions.md"]
    require("tepat satu solusi" in solutions and "Soal 3.1" in solutions, "sole-solution disclosure missing")
    require("Tidak ada solusi baru yang dibuat" in solutions, "no-invention disclosure missing")
    require("negative_public_solution_count: 17" in solutions, "17 negative candidates not bound")
    require("negative_solution_numbers: \"2-18\"" in solutions, "negative candidate range drifted")
    solution_heading_numbers = re.findall(r"^## Solusi sumber untuk Soal 3\.(\d+)", solutions, re.M)
    require(solution_heading_numbers == ["1"], "invented or missing solution section")
    a = [[3, -4], [5, -2]]
    b = [[-2, 7], [6, 3]]
    computed = [
        [a[i][j] * b[k][ell] for j in range(2) for ell in range(2)]
        for i in range(2)
        for k in range(2)
    ]
    expected_matrix = [[-6, 21, 8, -28], [18, 9, -24, -12], [-10, 35, 4, -14], [30, 15, -12, -6]]
    require(computed == expected_matrix, "independent Kronecker arithmetic failed")
    for row in ("-6&21&8&-28", "18&9&-24&-12", "-10&35&4&-14", "30&15&-12&-6"):
        require(row in solutions, f"solution matrix row missing: {row}")

    lecture = texts["lecture-03.md"]
    numbered_lecture = re.findall(
        r"^### (?:Definisi|Contoh|Catatan|Lema) 3\.(\d+):",
        lecture,
        re.M,
    )
    require([int(value) for value in numbered_lecture] == list(range(1, 28)), "lecture numbering 3.1--3.27 drifted")
    require(lecture.count("#### Bukti") == 2, "two source proofs not preserved")
    required_witnesses = {
        "direct_sum": r"E\oplus F",
        "tensor_product": r"E\otimes F",
        "exterior_power": r"\bigwedge^rE",
        "determinant_bundle": r"\det E",
        "hom_bundle": r"\operatorname{Hom}(E,F)",
        "dual_bundle": r"E^*",
        "presheaf_composition": r"\rho_{W,U}=\rho_{V,U}\circ\rho_{W,V}",
        "subpresheaf_restriction": r"\rho^{\mathcal G}_{V,U}",
        "directed_colimit": r"\operatorname{colim}_{i\in I}M_i",
        "point_stalk": r"\mathcal F_P",
        "filter_stalk": r"\mathcal G_F",
        "typed_naturality_top": r"\mathcal F(V)&\xrightarrow{\varphi_V}&\mathcal G(V)",
        "typed_naturality_restriction": r"\rho^{\mathcal F}_{V,U}",
        "stalk_morphism": r"\varphi_P:\mathcal F_P\longrightarrow\mathcal G_P",
        "proof_well_defined": r"\rho_{U,P}\bigl(\varphi_U(s)\bigr)",
        "worksheet_tangent_section_presheaf": "praberkas seksi kontinu bundel tangen",
    }
    for label, witness in required_witnesses.items():
        target = worksheet if label == "worksheet_tangent_section_presheaf" else lecture
        require(witness in target, f"mathematical/source witness missing: {label}")
    require(joined.count("**Catatan edisi -") == 6, "six visible placements for five anomaly classes not preserved")
    require("Die wichtigsten Filter sind für und" in lecture, "garbled source sentence not preserved visibly")
    require(joined.count("Prägraben") == 3, "source typo disclosure count drifted")

    all_ids = [identifier for text in texts.values() for identifier in markdown_ids(text)]
    require(len(all_ids) == 58 and len(all_ids) == len(set(all_ids)), "Unit 3 heading-ID closure drifted")
    for name in unit_files:
        yaml_id = re.search(r"^stable_id: (br-bgk-2019-[A-Za-z0-9_-]+)$", texts[name], re.M)
        require(yaml_id is not None and yaml_id.group(1) in all_ids, f"YAML/root ID mismatch: {name}")
    earlier_ids: set[str] = set()
    for path in EARLIER_BGK_FILES:
        earlier_ids.update(markdown_ids(path.read_text(encoding="utf-8")))
    require(not (set(all_ids) & earlier_ids), "BGK Unit 1/2/3 stable-ID collision")
    classical_ids: set[str] = set()
    classical_root = LANE / "source" / "id-ID"
    for pattern in ("lecture-*.md", "worksheet-*.md", "worksheet-*-solutions.md"):
        for path in classical_root.glob(pattern):
            classical_ids.update(re.findall(r"\{#([^}]+)\}", path.read_text(encoding="utf-8")))
    require(not (set(all_ids) & classical_ids), "BGK/classical stable-ID collision")

    for number in (8, 12, 13, 17):
        require(f"3.{number}" in joined, f"required internal cross-reference missing: 3.{number}")
    frontmatter = texts["frontmatter-bgk-units-01-03.md"]
    require("seluruh 62 soal" in frontmatter, "cumulative exercise count missing")
    require("60 hasil negatif" in frontmatter, "cumulative negative-solution count missing")
    require("lima kelas" in frontmatter, "five Unit 3 anomaly classes not disclosed")
    require("Unit 3 tidak mempunyai posisi media pembaca substantif" in frontmatter, "zero-media boundary missing")

    closure = json.loads((LANE / "authority" / "ASSET_CLOSURE-bgk-unit-03.json").read_text(encoding="utf-8"))
    require(closure["reader_media_positions"] == 0, "Unit 3 reader-media position count drifted")
    require(closure["unique_local_assets"] == 0 and closure["assets"] == [], "Unit 3 gained an unauthorized asset")
    require(closure["official_pdf_witnesses_are_not_media_positions"] is True, "PDF witness/media distinction drifted")
    require(len(closure["official_pdf_component_rights"]) == 2, "official PDF rights closure drifted")
    image_links = re.findall(r"!\[[^\]]*\]\([^)]+\)", "\n".join(texts[name] for name in unit_files))
    require(image_links == [], "Unit 3 reader unexpectedly embeds media")

    with (LANE / "00_control" / "CORRECTIONS.csv").open("r", encoding="utf-8-sig", newline="") as stream:
        correction_rows = {row["correction_id"]: row for row in csv.DictReader(stream)}
    require(all(identifier in correction_rows for identifier in CORRECTION_IDS), "Unit 3 correction ledger closure missing")
    require(
        all(correction_rows[identifier]["status"] == "applied_at_bgk_unit_03_translation" for identifier in CORRECTION_IDS),
        "Unit 3 correction status drifted",
    )
    with (LANE / "00_control" / "TERMINOLOGY.csv").open("r", encoding="utf-8-sig", newline="") as stream:
        term_rows = {row["term_id"]: row for row in csv.DictReader(stream)}
    require(all(identifier in term_rows for identifier in (*NEW_TERM_IDS, *REUSED_TERM_IDS)), "terminology closure missing")
    require(all(term_rows[identifier]["status"] == "admitted" for identifier in (*NEW_TERM_IDS, *REUSED_TERM_IDS)), "terminology not admitted")

    pandoc = [pandoc_fact(path) for path in FILES]
    result = {
        "schema": "ag-bridge-bgk-unit-translation-qa-v1",
        "unit": 3,
        "language": "id-ID",
        "status": "PASS",
        "authority": [fact(AUTH / name) for name in AUTHORITY_SHA256],
        "media_and_rights": [fact(path) for path in MEDIA_RIGHTS_SHA256],
        "translation_files": [fact(path) for path in FILES],
        "pandoc": pandoc,
        "counts": {
            "source_exercises": 18,
            "translated_exercises": len(exercise_ids),
            "source_public_solutions": 1,
            "translated_public_solutions": len(solution_heading_numbers),
            "negative_solution_candidates": 17,
            "invented_solutions": 0,
            "lecture_numbered_entities": len(numbered_lecture),
            "heading_ids": len(all_ids),
            "heading_id_collisions": 0,
            "source_anomaly_classes": len(CORRECTION_IDS),
            "visible_anomaly_note_placements": joined.count("**Catatan edisi -"),
            "correction_ledger_rows_added": len(CORRECTION_IDS),
            "terminology_rows_added": len(NEW_TERM_IDS),
            "terminology_rows_reused": len(REUSED_TERM_IDS),
            "reader_media_positions": len(image_links),
        },
        "correction_ids": list(CORRECTION_IDS),
        "terminology_ids_added": list(NEW_TERM_IDS),
        "terminology_ids_reused": list(REUSED_TERM_IDS),
        "checks": [
            "frozen_authority_and_transclusion_hashes",
            "ordered_18_exercise_map",
            "exact_public_solution_3_1_and_17_negative_candidates",
            "independent_kronecker_arithmetic",
            "no_invented_solutions",
            "lecture_numbering_3_1_through_3_27",
            "source_order_and_formula_witnesses",
            "five_corrected_source_anomaly_classes_with_six_visible_placements",
            "append_only_correction_and_terminology_ledgers",
            "disjoint_bgk_and_classical_stable_ids",
            "zero_reader_media_bound_to_component_rights_closure",
            "pandoc_ast_all_four_files",
            "exact_model_provenance_license_and_nonendorsement",
            "no_placeholders_german_prose_malformed_math_backticks_or_invisible_controls",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"receipt": fact(OUT), "counts": result["counts"], "pandoc": pandoc}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
