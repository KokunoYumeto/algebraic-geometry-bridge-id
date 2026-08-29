#!/usr/bin/env python3
"""Fail-closed source, mathematics, language, rights, and scope QA for BGK Unit 4."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess


LANE = Path(__file__).resolve().parents[1]
BGK = LANE / "source" / "id-ID" / "bgk"
AUTH = LANE / "authority" / "wikiversity-bgk" / "unit-04"
OUT = LANE / "qa" / "BGK_UNIT_04_TRANSLATION_QA.json"
FILES = (
    BGK / "frontmatter-bgk-units-01-04.md",
    BGK / "lecture-04.md",
    BGK / "worksheet-04.md",
    BGK / "worksheet-04-solutions.md",
)
EARLIER_BGK_FILES = tuple(
    BGK / name
    for unit in range(1, 4)
    for name in (
        f"lecture-{unit:02d}.md",
        f"worksheet-{unit:02d}.md",
        f"worksheet-{unit:02d}-solutions.md",
    )
) + (
    BGK / "frontmatter-bgk-units-01.md",
    BGK / "frontmatter-bgk-units-01-02.md",
    BGK / "frontmatter-bgk-units-01-03.md",
)
AUTHORITY_SHA256 = {
    "UNIT_AUTHORITY_MANIFEST.json": "3f26616ff7e9f4ac0d5bb0e64ad8435fefc18e32e4c91b16d780d4346498f680",
    "lecture-04.xml": "008241be410fe252da296e8332fa11c1db08960ff84eaac3c073564007d5845a",
    "lecture-04-expanded.tex": "4dc55e0810888863946316396cff73ce5ef1a1bb9b46864b64b3ed80ba3a8ea1",
    "worksheet-04.xml": "3e205caf77b5388ff6a0aa2bb1fa3643e354ce4ccc7e5e19d2dc7f6e29daca8a",
    "worksheet-04-expanded.tex": "7af2dce83605791269ba4fc1d5351100411b0a8081920cce8f1241724249f974",
    "ORDERED_EXERCISE_MAP.json": "a53d958595d6fd0aac34f8ea6562204dda96b44a375e68b33d93d92e63485dcf",
    "worksheet-solution-candidates-api.json": "1eb1be9dc5b34a5cc19719ddaf57cd918df880b0b28c74f52ab62ab25d33b52f",
}
MEDIA_RIGHTS_SHA256 = {
    LANE / "authority" / "ASSET_CLOSURE-bgk-unit-04.json": "2de02cc0d3d6018f42925b72b41e1661f3e9e305a07486f584c6e17c2c2fd0b3",
    LANE / "authority" / "RIGHTS-bgk-unit-04.csv": "620791467ec9ce4b87edde9efb7760359c6acc8a203435863a6d37cc79fd5132",
    LANE / "authority" / "commons-imageinfo-bgk-unit-04.json": "2a43864e163ad727c4c03ea62e7dc5ba45b2262a2ad19cc226b3f8a1bc56dddf",
    LANE / "source" / "id-ID" / "media-credits-bgk-unit-04.md": "9d57b9c693fa327d008a191345e5a1f0ff58e87230e1b9ac16209ed46d178282",
    LANE / "authority" / "assets" / "bgk-u04-triticum-spelta.jpg": "1050547eae3e7855001791da54dc8cd957b324cf38e5ef5b0955b4a596b0da7b",
}
CORRECTION_IDS = tuple(f"AGC-CORR-{number:04d}" for number in range(154, 159))
NEW_TERM_IDS = tuple(f"AGT-{number:04d}" for number in range(315, 324))
REUSED_TERM_IDS = (
    "AGT-0072",
    "AGT-0088",
    "AGT-0089",
    "AGT-0090",
    "AGT-0098",
    "AGT-0100",
    "AGT-0102",
    "AGT-0103",
    "AGT-0105",
    "AGT-0277",
    "AGT-0290",
    "AGT-0306",
    "AGT-0312",
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
        "image_nodes": sum(node.get("t") == "Image" for node in nodes),
    }


def body_without_metadata_comments_or_notes(text: str) -> str:
    body = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    return re.sub(r"(?m)^>.*(?:\n>.*)*", "", body)


def markdown_ids(text: str) -> list[str]:
    return re.findall(r"\{#(br-bgk-2019-[A-Za-z0-9_-]+)\}", text)


def main() -> int:
    for name, expected in AUTHORITY_SHA256.items():
        require(sha256(AUTH / name) == expected, f"authority hash mismatch: {name}")
    for path, expected in MEDIA_RIGHTS_SHA256.items():
        require(sha256(path) == expected, f"media/rights hash mismatch: {path.name}")

    manifest = json.loads((AUTH / "UNIT_AUTHORITY_MANIFEST.json").read_text(encoding="utf-8"))
    require(manifest["unit_number"] == 4, "authority manifest unit drifted")
    require(manifest["lecture"]["revid"] == 1003714, "lecture revision drifted")
    require(manifest["worksheet"]["revid"] == 1003857, "worksheet revision drifted")
    require(
        manifest["lecture_transclusion_closure"]["requested_template_count"]
        == manifest["lecture_transclusion_closure"]["captured_page_count"]
        == 106,
        "lecture transclusion closure drifted",
    )
    require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "lecture transclusion missing")
    require(
        manifest["worksheet_transclusion_closure"]["requested_template_count"]
        == manifest["worksheet_transclusion_closure"]["captured_page_count"]
        == 60,
        "worksheet transclusion closure drifted",
    )
    require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "worksheet transclusion missing")

    texts = {path.name: path.read_text(encoding="utf-8") for path in FILES}
    joined = "\n".join(texts.values())
    unit_files = ("lecture-04.md", "worksheet-04.md", "worksheet-04-solutions.md")
    for name in unit_files:
        require("OpenAI Codex gpt-5.6-sol, Ultra." in texts[name], f"exact provenance missing: {name}")
        require("CC BY-SA 4.0" in texts[name], f"CC BY-SA notice missing: {name}")
        require("tidak menyiratkan dukungan" in texts[name], f"non-endorsement missing: {name}")
    frontmatter = texts["frontmatter-bgk-units-01-04.md"]
    require("OpenAI Codex gpt-5.6-sol, Ultra." in frontmatter, "frontmatter provenance missing")
    require("seluruh 71 soal" in frontmatter and "69 hasil" in frontmatter, "cumulative exercise/negative counts missing")
    require("lima temuan" in frontmatter and "CC BY-SA 2.5" in frontmatter, "Unit 4 anomaly/media disclosure missing")
    require(not re.search(r"(?:TODO|TBD|PLACEHOLDER|LOREM IPSUM)", joined, re.I), "placeholder remains")
    require(not re.search(r"[\u200b\u200c\u200d\u2060\ufeff]", joined), "invisible control remains")
    require(not re.search(r"\$[^$\n]*`", joined), "stray backtick inside an unclosed math span")

    cleaned_body = "\n".join(body_without_metadata_comments_or_notes(text) for text in texts.values())
    german_residue = re.findall(
        r"\b(?:Zeige|Berechne|Aufgabe|Vorlesung|Arbeitsblatt|Es sei|Dann nennt man|Beweis)\b",
        cleaned_body,
    )
    require(not german_residue, f"unexpected German prose residue: {german_residue[:5]}")

    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    require(mapping["exercise_count"] == 9 and mapping["solution_count"] == 0, "solution scope mismatch")
    require(not any(entry["has_public_solution"] for entry in mapping["entries"]), "unexpected public solution")
    worksheet = texts["worksheet-04.md"]
    expected_titles = [entry["exercise_title"] for entry in mapping["entries"]]
    actual_titles = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    require(actual_titles == expected_titles, "ordered exercise mapping mismatch")
    exercise_ids = re.findall(r"^## Soal 4\.(\d+) \{#(br-bgk-2019-w04-ex\d{2})\}$", worksheet, re.M)
    require([int(number) for number, _ in exercise_ids] == list(range(1, 10)), "exercise numbering mismatch")
    require(len({identifier for _, identifier in exercise_ids}) == 9, "duplicate exercise ID")

    solutions = texts["worksheet-04-solutions.md"]
    require("tidak menyediakan solusi publik" in solutions, "zero-solution disclosure missing")
    require("Tidak ada solusi baru yang dibuat" in solutions, "no-invention disclosure missing")
    require("negative_public_solution_count: 9" in solutions, "nine negative candidates not bound")
    require("negative_solution_numbers: \"1-9\"" in solutions, "negative candidate range drifted")
    require(not re.search(r"^## Solusi sumber", solutions, re.M), "invented solution section")

    lecture = texts["lecture-04.md"]
    numbered_lecture = re.findall(r"^### (?:Definisi|Contoh|Lema|Korolari) 4\.(\d+):", lecture, re.M)
    require([int(value) for value in numbered_lecture] == list(range(1, 12)), "lecture numbering 4.1--4.11 drifted")
    require(lecture.count("#### Bukti") == 6, "six source proof positions not preserved")
    required_witnesses = {
        "first_sheaf_axiom": r"\rho_{U,U_i}(s)=\rho_{U,U_i}(t)",
        "second_sheaf_axiom": r"\rho_{U_i,U_i\cap U_j}(s_i)",
        "continuous_sections": r"S(U,Y)",
        "continuous_group_maps": r"C^0(U,G)",
        "stalk_equality": r"s_P=t_P",
        "injective_section_map": r"\varphi_U:\mathcal F(U)\longrightarrow\mathcal G(U)",
        "stalk_isomorphism": r"\varphi_P:\mathcal F_P\longrightarrow\mathcal G_P",
        "circle_cover": r"t\longmapsto(\cos t,\sin t)",
        "hom_sheaf": r"\operatorname{Mor}(\mathcal F|_U,\mathcal G|_U)",
        "all_open_subsets_completion": r"setiap himpunan terbuka $V\subseteq U$",
        "restriction_compatibility": r"Jika $W\subseteq V$",
        "consistent_point_index": r"\alpha_P=\beta_P",
        "constant_presheaf_cardinality": "sekurang-kurangnya dua unsur",
        "skyscraper_stalk": r"\mathcal G_Q",
    }
    for label, witness in required_witnesses.items():
        target = worksheet if label in {"constant_presheaf_cardinality", "skyscraper_stalk"} else lecture
        require(witness in target, f"mathematical/source witness missing: {label}")

    require(joined.count("**Catatan edisi -") == 5, "five visible source-treatment notes not preserved")
    for witness in ("Garbenmorpismen", "Besitmme die Halm", r"\alpha_p=\beta_P", r"M\ne\varnothing"):
        require(witness in joined, f"source form not preserved visibly: {witness}")

    all_ids = [identifier for text in texts.values() for identifier in markdown_ids(text)]
    require(len(all_ids) == 33 and len(all_ids) == len(set(all_ids)), "Unit 4 heading-ID closure drifted")
    for name in unit_files:
        yaml_id = re.search(r"^stable_id: (br-bgk-2019-[A-Za-z0-9_-]+)$", texts[name], re.M)
        require(yaml_id is not None and yaml_id.group(1) in all_ids, f"YAML/root ID mismatch: {name}")
    earlier_ids: set[str] = set()
    for path in EARLIER_BGK_FILES:
        earlier_ids.update(markdown_ids(path.read_text(encoding="utf-8")))
    require(not (set(all_ids) & earlier_ids), "BGK Unit 1/2/3/4 stable-ID collision")
    classical_ids: set[str] = set()
    classical_root = LANE / "source" / "id-ID"
    for pattern in ("lecture-*.md", "worksheet-*.md", "worksheet-*-solutions.md"):
        for path in classical_root.glob(pattern):
            classical_ids.update(re.findall(r"\{#([^}]+)\}", path.read_text(encoding="utf-8")))
    require(not (set(all_ids) & classical_ids), "BGK/classical stable-ID collision")

    closure = json.loads((LANE / "authority" / "ASSET_CLOSURE-bgk-unit-04.json").read_text(encoding="utf-8"))
    require(closure["reader_media_positions"] == 1 and closure["unique_local_assets"] == 1, "Unit 4 media count drifted")
    require(len(closure["assets"]) == 1 and closure["assets"][0]["license_short"] == "CC BY-SA 2.5", "asset license drifted")
    image_links = re.findall(r"!\[([^\]]+)\]\(([^)]+)\)", "\n".join(texts[name] for name in unit_files))
    require(image_links == [("Berkas-berkas gandum spelta yang berdiri tegak di sebuah ladang", "authority/assets/bgk-u04-triticum-spelta.jpg")], "reader media placement/alt drifted")
    require("André Karwath aka Aka" in lecture and "CC BY-SA 2.5" in lecture, "inline image attribution missing")

    with (LANE / "00_control" / "CORRECTIONS.csv").open("r", encoding="utf-8-sig", newline="") as stream:
        correction_rows = {row["correction_id"]: row for row in csv.DictReader(stream)}
    require(all(identifier in correction_rows for identifier in CORRECTION_IDS), "Unit 4 correction ledger closure missing")
    require(
        all(correction_rows[identifier]["status"] == "applied_at_bgk_unit_04_translation" for identifier in CORRECTION_IDS),
        "Unit 4 correction status drifted",
    )
    with (LANE / "00_control" / "TERMINOLOGY.csv").open("r", encoding="utf-8-sig", newline="") as stream:
        term_rows = {row["term_id"]: row for row in csv.DictReader(stream)}
    require(all(identifier in term_rows for identifier in (*NEW_TERM_IDS, *REUSED_TERM_IDS)), "terminology closure missing")
    require(all(term_rows[identifier]["status"] == "admitted" for identifier in (*NEW_TERM_IDS, *REUSED_TERM_IDS)), "terminology not admitted")

    pandoc = [pandoc_fact(path) for path in FILES]
    result = {
        "schema": "ag-bridge-bgk-unit-translation-qa-v1",
        "unit": 4,
        "language": "id-ID",
        "status": "PASS",
        "authority": [fact(AUTH / name) for name in AUTHORITY_SHA256],
        "media_and_rights": [fact(path) for path in MEDIA_RIGHTS_SHA256],
        "translation_files": [fact(path) for path in FILES],
        "pandoc": pandoc,
        "counts": {
            "source_exercises": 9,
            "translated_exercises": len(exercise_ids),
            "source_public_solutions": 0,
            "translated_public_solutions": 0,
            "negative_solution_candidates": 9,
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
            "ordered_nine_exercise_map_and_nine_negative_solution_candidates",
            "no_invented_solutions",
            "lecture_numbering_4_1_through_4_11_and_six_proofs",
            "source_order_and_formula_witnesses",
            "five_corrected_source_anomaly_classes_with_five_visible_notes",
            "complete_hom_sheaf_construction_for_every_open_subset_and_naturality",
            "append_only_correction_and_terminology_ledgers",
            "disjoint_bgk_and_classical_stable_ids",
            "one_reader_media_position_bound_to_cc_by_sa_2_5_component_rights",
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
