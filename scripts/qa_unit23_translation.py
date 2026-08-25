#!/usr/bin/env python3
"""Fail-closed authority, translation, mathematics, accessibility, and rights QA for Unit 23."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import unicodedata
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "authority" / "wikiversity" / "unit-23"
SOURCE = ROOT / "source" / "id-ID"
OUT = ROOT / "qa" / "UNIT_23_TRANSLATION_QA.json"

MANIFEST_FACT = (161310, "f7ee49a4bfa589b831c1fdb69e6f091ac1762d9da019a133670e4e0d723d34ae")
MAP_FACT = (11439, "fdfec83fe1ef4f0d87eca194f2991805cd69ff2af070b73ef83c0ba1c9d1e4c4")
AUTHORITY_QA_FACT = (2366, "6a55326eec4079a0000dcc7d449e92e9213254b2b16a8400ed7b784b200805ac")
FREEZE_FACT = (4776, "353d0b922f69caf330571a271c2ca6bf5c031c27062f82366ab01b87dd475c36")
SOURCE_FACTS = {
    "source/id-ID/lecture-23.md": (16697, "8f143de32c72078c7d9e09d5a9837584589068740d7702f857ec4183047c82ed"),
    "source/id-ID/worksheet-23.md": (8157, "011f5bb26e81002d262ffe0425ad290bdb2a287cb88864f080ea46554d2c8b19"),
    "source/id-ID/worksheet-23-solutions.md": (4580, "d817803e00f5df55473330608847a4664845c67c1319bbd73c12f1d5dd1bb939"),
    "source/id-ID/media-credits-unit-23.md": (1131, "bef7b4083c04fb72e7b17ad27657a730f8d48b72317714478489d6ebd3c74553"),
}
CONTROL_FACTS = {
    "00_control/TERMINOLOGY.csv": (29219, "f4c115caaad530456c541d61bb9b7567226869437cd5ceab2ebf29951731e12e"),
    "00_control/CORRECTIONS.csv": (54444, "d1b1fae8c947773eb9ed6e3a027d139b4c1b4f03af80e543bb5f88ee15b19737"),
    "authority/UNIT_23_AUTHORITY_FREEZE.md": FREEZE_FACT,
}
EXTERNAL_FACTS = {
    "authority/RIGHTS-unit-23.csv": (443, "6b8de6f5a63f32d9f22e7fb69c98ba2d787121a2437a392602571504c2a1c544"),
    "authority/ASSET_CLOSURE-unit-23.json": (33083, "d6bd0435e6c24d3085e8b4282d89bc263c4957b699d92d5c8409f7c16a43da64"),
    "authority/artifacts/lecture-23-official.pdf": (191471, "96fc99009c2f4640ba99db6203c06bd59e03bdc2927c1bf81302625431302724"),
    "authority/artifacts/worksheet-23-official.pdf": (159393, "6494630aba1d79f238c762b30cb382918444b19a82de3d96d66c4d6e3108d15b"),
}
SOLUTION_NUMBERS = [4, 5]
SOLUTION_PAGEIDS = [95515, 95541]
SOLUTION_REVIDS = [1090216, 1096444]
SOLUTION_XML_HASHES = [
    "56b03cddd25d14146c8934076599108a3cbf927f6696e7aaed9612b3fed40bea",
    "549cbd738a19c67071ca964c1bfa55e472c8ae592b01e8ce88b2a62114924300",
]
SOLUTION_CLOSURE_COUNTS = [19, 13]
TERM_IDS = [f"AGT-{number:04d}" for number in range(182, 193)]
CORRECTION_IDS = [f"AGC-CORR-{number:04d}" for number in range(77, 83)]
LECTURE_ENTITIES = [
    "Algebraische Derivation/Definition",
    "K-Algebra/Algebraischer Kotangentialraum an K-Punkt/Direkte Derivation/Fakt",
    "K-Algebra/Algebraischer Kotangentialraum an K-Punkt/Direkte Derivation/Fakt/Beweis",
    "Ebene algebraische Kurve/Glatter Punkt/Lokaler Ring ist diskreter Bewertungsring/Fakt",
    "Ebene algebraische Kurve/Glatter Punkt/Lokaler Ring ist diskreter Bewertungsring/Fakt/Beweis",
    "Noetherscher lokaler Ring/Potenzen vom maximalen Ideal/Restklassenring und Jets sind endlich-dimensional/Fakt",
    "Noetherscher lokaler Ring/Potenzen vom maximalen Ideal/Restklassenring und Jets sind endlich-dimensional/Fakt/Beweis",
    "Ebene algebraische Kurve/Multiplizität über Hilbert-Samuel Polynom/Fakt",
    "Ebene algebraische Kurve/Multiplizität über Hilbert-Samuel Polynom/Fakt/Beweis",
    "Ebene algebraische Kurve/Multiplizität über Hilbert-Samuel Polynom/Bemerkung",
    "Ebene algebraische Kurve/Punkt/Glatt,diskreter Bewertungsring, Multiplizität/Fakt",
    "Ebene algebraische Kurve/Punkt/Glatt,diskreter Bewertungsring, Multiplizität/Fakt/Beweis",
    "Monomiale Kurve/Multiplizität/Numerisch und Hilbert-Samuel/Textabschnitt",
    "Monomiale Kurven/Multiplizität/Abschätzungen für Anzahl in Differenzmengen/Fakt",
    "Monomiale Kurven/Multiplizität/Abschätzungen für Anzahl in Differenzmengen/Fakt/Beweis",
    "Monomiale Kurve/Hilbert-Samuel Multiplizität ist numerische Multiplizität/Fakt",
    "Monomiale Kurve/Hilbert-Samuel Multiplizität ist numerische Multiplizität/Fakt/Beweis",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path, algorithm: str = "sha256") -> str:
    hasher = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def check_fact(relative: str, fact: tuple[int, str]) -> dict[str, Any]:
    path = ROOT / relative
    require(path.is_file() and not path.is_symlink(), f"missing/nonregular file: {relative}")
    actual = (path.stat().st_size, digest(path))
    require(actual == fact, f"identity drift for {relative}: {actual} != {fact}")
    return {"path": relative, "bytes": actual[0], "sha256": actual[1]}


def walk(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def pandoc_ast(path: Path) -> dict[str, Any]:
    process = subprocess.run(
        [
            "pandoc",
            "--from=markdown+yaml_metadata_block+tex_math_dollars+fenced_divs+bracketed_spans+raw_attribute",
            "--to=json",
            str(path),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    require(not process.stderr.strip(), f"Pandoc warning for {path.name}: {process.stderr}")
    return json.loads(process.stdout)


def strip_nonprose(raw: str) -> str:
    raw = re.sub(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", "", raw, flags=re.S)
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    raw = re.sub(r"\$\$.*?\$\$", "", raw, flags=re.S)
    raw = re.sub(r"\$[^$\n]*\$", "", raw)
    raw = re.sub(r"```.*?```", "", raw, flags=re.S)
    raw = re.sub(r"`[^`\n]*`", "", raw)
    return raw


def normalized_math(raw: str) -> str:
    return re.sub(r"\s+", "", raw)


def verify_authority() -> dict[str, Any]:
    manifest_fact = check_fact("authority/wikiversity/unit-23/UNIT_AUTHORITY_MANIFEST.json", MANIFEST_FACT)
    map_fact = check_fact("authority/wikiversity/unit-23/ORDERED_EXERCISE_MAP.json", MAP_FACT)
    authority_qa_fact = check_fact("qa/UNIT_23_AUTHORITY_QA.json", AUTHORITY_QA_FACT)
    freeze_fact = check_fact("authority/UNIT_23_AUTHORITY_FREEZE.md", FREEZE_FACT)
    manifest = json.loads((AUTH / "UNIT_AUTHORITY_MANIFEST.json").read_text(encoding="utf-8"))
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    authority_qa = json.loads((ROOT / "qa" / "UNIT_23_AUTHORITY_QA.json").read_text(encoding="utf-8"))

    require(authority_qa["result"] == "PASS" and authority_qa["unit"] == 23, "authority QA state")
    require(authority_qa["authority_manifest"]["sha256"] == MANIFEST_FACT[1], "authority QA manifest binding")
    require(authority_qa["authority_freeze_note"]["sha256"] == FREEZE_FACT[1], "authority QA freeze binding")
    require(authority_qa["exercise_count"] == 12 and authority_qa["public_solution_numbers"] == SOLUTION_NUMBERS, "authority QA exercise topology")
    require(authority_qa["reader_media_positions"] == 0, "authority QA media topology")
    require(authority_qa["source_defect_ids"] == [f"AGC-U23-SRC-{index:03d}" for index in range(1, 7)], "authority QA defect topology")

    require(manifest["schema"] == "brenner-unit-authority-freeze-v2" and manifest["unit_number"] == 23, "authority schema/unit")
    require(manifest["source_course_license"] == "CC BY-SA 4.0", "course licence")
    require(manifest["source_course_license_authority"]["declared_license"] == "CC BY-SA 4.0", "course licence authority")
    require(
        (manifest["lecture"]["pageid"], manifest["lecture"]["revid"], manifest["lecture"]["mediawiki_sha1"], manifest["lecture"]["xml_sha256"])
        == (165912, 1112318, "a38160a106cf39298b3f2cb23f7880e05a5a86f7", "e03f37dab14063c982dec993e0da4dd94e9e4cbdf9b73b38ad4c77a63dd83116"),
        "lecture identity/XML",
    )
    require(
        (manifest["worksheet"]["pageid"], manifest["worksheet"]["revid"], manifest["worksheet"]["mediawiki_sha1"], manifest["worksheet"]["xml_sha256"])
        == (165942, 1062659, "19554b41098b4f02ac6e558145036ca293e4bbc9", "98b40a9acd3a8da5e5b743b8245b2690007abdbbc6d7fa7b2106e2871560dabc"),
        "worksheet identity/XML",
    )
    require(
        [(row["bytes"], row["sha256"]) for row in manifest["derived_expanded_tex"]]
        == [
            (21754, "17aa88b5aa9a8d130f0995c036cb9ca332ef1b0feaef3b2d5ac5396e47b343a0"),
            (8243, "865905ee0d321006682c162fb2d9e272f1fc251e61b8dde9844981f6baba9c0f"),
        ],
        "expanded TeX identities",
    )
    require(manifest["entry_revision_recheck"]["result"] == "PASS", "entry revision recheck")
    require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 142, "lecture closure")
    require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 102, "worksheet closure")
    require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "lecture missing dependency")
    require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "worksheet missing dependency")
    require(manifest["transclusion_topology"]["lecture"]["unique_casefold_comparison_keys"] == 141, "lecture casefold topology")
    require(manifest["transclusion_topology"]["worksheet"]["unique_casefold_comparison_keys"] == 101, "worksheet casefold topology")

    require(len(manifest["files"]) == 57 and sum(row["bytes"] for row in manifest["files"]) == 808727, "local authority inventory")
    for row in manifest["files"]:
        path = AUTH / row["file"]
        require(path.is_file() and path.stat().st_size == row["bytes"] and digest(path) == row["sha256"], f"authority file replay: {row['file']}")
    require(len(manifest["bounded_external_files"]) == 4 and sum(row["bytes"] for row in manifest["bounded_external_files"]) == 384390, "external authority inventory")
    for row in manifest["bounded_external_files"]:
        path = ROOT / row["file"]
        require(path.is_file() and path.stat().st_size == row["bytes"] and digest(path) == row["sha256"], f"external authority replay: {row['file']}")

    live = manifest["final_live_identity_replay"]
    require(live["result"] == "PASS" and live["wikiversity_identity_count"] == 208, "final Wikiversity replay")
    require(sum(row["title_count"] for row in live["wikiversity_batches"]) == 208, "final replay batch total")
    require(live["commons_pdf_identity_count"] == 2, "final Commons replay")

    require(mapping["schema"] == "brenner-worksheet-solution-map-v2" and mapping["unit"] == 23, "map schema/unit")
    require(mapping["exercise_count"] == 12 and mapping["solution_count"] == 2, "map topology")
    require([row["exercise_number"] for row in mapping["entries"]] == list(range(1, 13)), "exercise order")
    topology = mapping["ordered_role_and_point_topology"]
    require(topology["practice_numbers"] == list(range(1, 8)), "practice topology")
    require(topology["submitted_numbers"] == list(range(8, 13)), "submitted topology")
    require(topology["practice_authored_hidden_points"] == {"3": 2, "4": 4, "5": 4, "6": 3, "7": 2}, "hidden authored points")
    require(topology["practice_authored_hidden_subpoints"] == {"5": [2, 1, 1]}, "hidden authored subpoints")
    require(topology["submitted_displayed_points"] == {"8": 4, "9": 3, "10": 5, "11": 5, "12": 3}, "submitted point topology")
    require(topology["submitted_displayed_point_total"] == 20, "submitted point total")
    solutions = [row for row in mapping["entries"] if row["has_public_solution"]]
    require([row["exercise_number"] for row in solutions] == SOLUTION_NUMBERS, "solution set")
    require([row["pageid"] for row in solutions] == SOLUTION_PAGEIDS, "solution page IDs")
    require([row["revid"] for row in solutions] == SOLUTION_REVIDS, "solution revisions")
    require([row["xml_sha256"] for row in solutions] == SOLUTION_XML_HASHES, "solution XML identities")
    closures = manifest["solution_transclusion_closures"]
    require([row["exercise_number"] for row in closures] == SOLUTION_NUMBERS, "solution closure order")
    require([row["solution_revid"] for row in closures] == SOLUTION_REVIDS, "solution closure revisions")
    require([row["recursive_transclusion_closure"]["captured_page_count"] for row in closures] == SOLUTION_CLOSURE_COUNTS, "solution closure sizes")
    require(all(row["recursive_transclusion_closure"]["missing_page_count"] == 0 for row in closures), "solution closure completeness")
    require(all(not row["direct_wrapper_dependency_titles"] for row in closures), "unexpected solution wrapper")
    require([row["id"] for row in manifest["source_defect_bindings"]] == [f"AGC-U23-SRC-{index:03d}" for index in range(1, 7)], "source defect bindings")
    require(manifest["images"]["reader_media_positions"] == 0 and manifest["images"]["substantive_assets"] == [], "authority reader media topology")

    return {
        "manifest": manifest_fact,
        "exercise_map": map_fact,
        "authority_qa": authority_qa_fact,
        "authority_freeze": freeze_fact,
        "lecture_revid": 1112318,
        "worksheet_revid": 1062659,
        "lecture_transclusions_exact": 142,
        "worksheet_transclusions_exact": 102,
        "lecture_casefold_diagnostic_keys": 141,
        "worksheet_casefold_diagnostic_keys": 101,
        "exercises": 12,
        "public_solution_numbers": SOLUTION_NUMBERS,
        "solution_revisions": SOLUTION_REVIDS,
        "solution_recursive_closures": SOLUTION_CLOSURE_COUNTS,
        "authority_files_verified": 57,
        "bounded_external_files_verified": 4,
        "live_wikiversity_identities": 208,
        "live_commons_pdf_identities": 2,
        "source_defect_bindings": 6,
    }


def verify_media_and_rights() -> dict[str, Any]:
    facts = [check_fact(relative, fact) for relative, fact in EXTERNAL_FACTS.items()]
    with (ROOT / "authority" / "RIGHTS-unit-23.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    closure = json.loads((ROOT / "authority" / "ASSET_CLOSURE-unit-23.json").read_text(encoding="utf-8"))
    require(closure["schema"] == "brenner-unit-media-closure-v2" and closure["unit"] == 23, "media closure identity")
    require(closure["authority_only_boundary"] is True, "authority-only media boundary")
    require(closure["reader_media_positions"] == 0 and closure["unique_local_assets"] == 0, "zero-media topology")
    require(closure["animated_html_positions"] == 0 and closure["assets"] == [], "asset topology")
    require(closure["rights_sha256"] == EXTERNAL_FACTS["authority/RIGHTS-unit-23.csv"][1], "rights binding")
    require(closure["reader_credits_required"] is False, "reader credits requirement")
    require(rows == [], "rights file must be header-only at zero-media boundary")
    require(closure["official_pdf_witnesses_are_not_media_positions"] is True, "PDF/media separation")
    pdf_rights = closure["official_pdf_component_rights"]
    require([row["local_path"] for row in pdf_rights] == ["authority/artifacts/lecture-23-official.pdf", "authority/artifacts/worksheet-23-official.pdf"], "PDF rights order")
    require([row["license_short"] for row in pdf_rights] == ["CC BY-SA 4.0", "CC BY-SA 4.0"], "PDF current licences")
    require([row["internal_pdf_boilerplate_label"] for row in pdf_rights] == ["CC-by-sa 3.0", "CC-by-sa 3.0"], "PDF embedded labels")
    surfaces = closure["accessibility"]["official_pdf_surfaces"]
    require([row["blank_page_numbers"] for row in surfaces] == [[], [4]], "PDF blank-page topology")
    require(all(row["tagged_pdf"] is False and row["structure_tree_present"] is False for row in surfaces), "PDF accessibility topology")
    for relative in ("authority/artifacts/lecture-23-official.pdf", "authority/artifacts/worksheet-23-official.pdf"):
        require((ROOT / relative).read_bytes().startswith(b"%PDF-"), f"PDF signature: {relative}")
    credits = (SOURCE / "media-credits-unit-23.md").read_text(encoding="utf-8")
    require("tidak\nmemuat posisi media pembaca substantif" in credits, "zero-media reader disclosure")
    require("CC BY-SA 3.0" in credits and "CC BY-SA 4.0" in credits, "PDF/course licence discrepancy disclosure")
    require("tujuh halaman" in credits and "lima halaman" in credits and "halaman keempatnya kosong" in credits, "PDF page topology disclosure")
    require("tidak bertag" in credits and "tidak memiliki\nstruktur dokumen PDF" in credits, "PDF accessibility disclosure")
    require("OpenAI Codex gpt-5.6-sol, Ultra." in credits, "media-credit model provenance")
    return {
        "reader_media_positions": 0,
        "binary_assets": 0,
        "rights_rows": 0,
        "official_pdf_witnesses": 2,
        "official_pdf_pages": [7, 5],
        "worksheet_blank_page_numbers": [4],
        "facts": facts,
    }


def verify_translation() -> dict[str, Any]:
    facts = [check_fact(relative, fact) for relative, fact in SOURCE_FACTS.items()]
    facts.extend(check_fact(relative, fact) for relative, fact in CONTROL_FACTS.items())
    lecture = (SOURCE / "lecture-23.md").read_text(encoding="utf-8")
    worksheet = (SOURCE / "worksheet-23.md").read_text(encoding="utf-8")
    solutions = (SOURCE / "worksheet-23-solutions.md").read_text(encoding="utf-8")
    credits = (SOURCE / "media-credits-unit-23.md").read_text(encoding="utf-8")
    all_text = "\n".join((lecture, worksheet, solutions, credits))

    for name, raw in (("lecture", lecture), ("worksheet", worksheet), ("solutions", solutions)):
        require("translation_status: complete" in raw, f"{name} completion flag")
        require("OpenAI Codex gpt-5.6-sol, Ultra" in raw, f"{name} exact model provenance")
        require('license: "CC BY-SA 4.0"' in raw, f"{name} licence metadata")
        require(MANIFEST_FACT[1] in raw, f"{name} manifest binding")
    require("source_semantic_entities: 17" in lecture, "lecture entity metadata")
    require("source_corrections: 3" in lecture, "lecture correction metadata")
    require("source_corrections: 1" in worksheet and "source_corrections: 2" in solutions, "worksheet/solution correction metadata")
    require("public_solution_count: 2" in solutions, "solution count metadata")
    require("reader_media_positions: 0" in lecture and "reader_media_positions: 0" in worksheet, "zero-media metadata")
    require("e03f37dab14063c982dec993e0da4dd94e9e4cbdf9b73b38ad4c77a63dd83116" in lecture, "lecture XML binding")
    require("17aa88b5aa9a8d130f0995c036cb9ca332ef1b0feaef3b2d5ac5396e47b343a0" in lecture, "lecture TeX binding")
    require("98b40a9acd3a8da5e5b743b8245b2690007abdbbc6d7fa7b2106e2871560dabc" in worksheet, "worksheet XML binding")
    require("865905ee0d321006682c162fb2d9e272f1fc251e61b8dde9844981f6baba9c0f" in worksheet, "worksheet TeX binding")
    require(MAP_FACT[1] in worksheet and MAP_FACT[1] in solutions, "exercise-map source binding")
    require(all(value in solutions for value in SOLUTION_XML_HASHES), "solution XML frontmatter binding")

    lower = all_text.casefold()
    require(all(token not in lower for token in ("todo", "fixme", "tbd", "placeholder", "lorem ipsum")), "placeholder residue")
    require(not re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|access[_-]?token|bearer\s+[A-Za-z0-9._-]{20,}|api[_-]?key\s*[:=]", all_text, flags=re.I), "secret-like content")
    controls = [(character, f"U+{ord(character):04X}") for character in all_text if unicodedata.category(character) in {"Cc", "Cf"} and character not in "\t\n\r"]
    require(not controls, f"invisible/control Unicode residue: {controls[:5]}")
    non_ascii_dashes = [(character, f"U+{ord(character):04X}") for character in all_text if 0x2010 <= ord(character) <= 0x2014]
    require(not non_ascii_dashes, f"non-ASCII dash residue: {non_ascii_dashes[:5]}")
    prose = strip_nonprose(all_text)
    residue = re.findall(
        r"\b(?:Es sei|Zeige|Aufgabe|Beweis|Lösung|Noetherscher lokaler Ring|Krulldimension|Multiplizität|Numerisches Monoid|Abschätzungen|Glatter Punkt)\b",
        prose,
        flags=re.I,
    )
    require(not residue, f"visible German residue: {residue}")

    headers = re.findall(r"^### Soal 23\.(\d+)(?:[^\n]*)\{#br-ak-2025-2026-w23-ex-(\d{2})\}$", worksheet, flags=re.M)
    require(headers == [(str(index), f"{index:02d}") for index in range(1, 13)], "exercise headers/IDs")
    starred = [int(value) for value in re.findall(r"^### Soal 23\.(\d+) ★", worksheet, flags=re.M)]
    require(starred == SOLUTION_NUMBERS, "solution-star topology")
    points = re.findall(r"^### Soal 23\.(\d+) \(([^)]*poin[^)]*)\)", worksheet, flags=re.M)
    require(points == [("8", "4 poin"), ("9", "3 poin"), ("10", "5 poin"), ("11", "5 poin"), ("12", "3 poin")], "submitted points")
    require(worksheet.index("### Soal 23.7") < worksheet.index("## Soal untuk dikumpulkan") < worksheet.index("### Soal 23.8"), "practice/submitted boundary")
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    worksheet_comments = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    exercise_comments = [value for value in worksheet_comments if value.endswith("/Aufgabe")]
    require(exercise_comments == [row["exercise_title"] for row in mapping["entries"]], "12 exercise entity mappings")
    require(len(worksheet_comments) == 13 and worksheet_comments[6] == "Kommutative Ringtheorie/Primidealkette/Krulldimension/Definition", "worksheet definition entity mapping")
    lecture_comments = re.findall(r"<!-- upstream_entity: (.*?) -->", lecture)
    require(lecture_comments == LECTURE_ENTITIES and len(lecture_comments) == 17, "lecture semantic entity mapping")
    lecture_titles = {row["title"] for row in json.loads((AUTH / "UNIT_AUTHORITY_MANIFEST.json").read_text(encoding="utf-8"))["lecture_transclusion_closure"]["pages"]}
    require(set(lecture_comments) <= lecture_titles, "lecture entity authority closure")

    solution_headers = [int(value) for value in re.findall(r"^## Solusi Soal 23\.(\d+) ", solutions, flags=re.M)]
    require(solution_headers == SOLUTION_NUMBERS, "solution headers")
    solution_comments = re.findall(r"<!-- upstream_solution: (.*?); pageid=(\d+); revid=(\d+) -->", solutions)
    require(
        solution_comments
        == [
            ("Polynomring/2/Multiplizität/Multiplikation/Aufgabe/Lösung", "95515", "1090216"),
            ("Numerisches Monoid/N ab e/Hilbert-Funktion/Aufgabe/Lösung", "95541", "1096444"),
        ],
        "solution comments/identities",
    )
    require(solutions.count("<!-- upstream_solution_url:") == 2, "solution immutable URLs")
    require("https://de.wikiversity.org/w/index.php?oldid=1090216" in solutions and "https://de.wikiversity.org/w/index.php?oldid=1096444" in solutions, "solution oldid URLs")
    back_links = [int(value) for value in re.findall(r"\[Kembali ke Soal 23\.(\d+)\]\(#br-ak-2025-2026-w23-ex-\d{2}\)", solutions)]
    require(back_links == SOLUTION_NUMBERS, "solution backlinks")

    stable_ids = re.findall(r"\{#(br-ak-2025-2026-[^}]+|agc-media-credits-unit-23)\}", all_text)
    require(len(stable_ids) == 42 and len(stable_ids) == len(set(stable_ids)), f"stable-ID topology: {len(stable_ids)}")
    require("![" not in lecture + worksheet + solutions + credits, "reader image topology")

    with (ROOT / "00_control" / "TERMINOLOGY.csv").open(encoding="utf-8", newline="") as stream:
        term_rows = {row["term_id"]: row for row in csv.DictReader(stream)}
    expected_terms = {
        "AGT-0182": ("Derivation", "derivasi"),
        "AGT-0183": ("Leibniz-Regel", "aturan Leibniz"),
        "AGT-0184": ("K-Algebra von endlichem Typ", "aljabar K bertipe hingga"),
        "AGT-0185": ("Hilbert-Samuel-Multiplizität", "multiplisitas Hilbert-Samuel"),
        "AGT-0186": ("Krulldimension", "dimensi Krull"),
        "AGT-0187": ("Primidealkette", "rantai ideal prima"),
        "AGT-0188": ("Reduktion", "reduksi"),
        "AGT-0189": ("Monoid-Ideal", "ideal monoid"),
        "AGT-0190": ("numerische Multiplizität", "multiplisitas numerik"),
        "AGT-0191": ("Hilbert-Funktion", "fungsi Hilbert"),
        "AGT-0192": ("homogene Zerlegung", "dekomposisi homogen"),
    }
    require(list(expected_terms) == TERM_IDS, "terminology ID interval")
    for term_id, (source_term, target_term) in expected_terms.items():
        require(term_id in term_rows and term_rows[term_id]["source_term"] == source_term, f"terminology source: {term_id}")
        require(term_rows[term_id]["preferred_target"] == target_term and term_rows[term_id]["status"] == "admitted", f"terminology target/status: {term_id}")
    preferred_visible = [target for _, target in expected_terms.values()]
    visibility_needles = {
        target: ([target] if term_id != "AGT-0184" else ["aljabar bertipe hingga atas"])
        for term_id, (_, target) in expected_terms.items()
    }
    missing_terms = [
        term
        for term, needles in visibility_needles.items()
        if not all(needle.casefold() in prose.casefold() for needle in needles)
    ]
    require(not missing_terms, f"preferred reader terminology absent: {missing_terms}")
    require(not re.search(r"\b(?:turunan aljabar|aljabar K terhingga dihasilkan|multipelitas Hilbert-Samuel|rantai prima|ideal pada monoid|multiplisitas bilangan|penguraian homogen)\b", prose, flags=re.I), "nonpreferred terminology residue")

    with (ROOT / "00_control" / "CORRECTIONS.csv").open(encoding="utf-8", newline="") as stream:
        corrections = {row["correction_id"]: row for row in csv.DictReader(stream)}
    for correction_id in CORRECTION_IDS:
        require(correction_id in corrections, f"missing correction binding: {correction_id}")
        require(corrections[correction_id]["status"] == "applied_at_unit_23_translation", f"correction status: {correction_id}")
    require(all(correction_id not in all_text for correction_id in CORRECTION_IDS), "ledger IDs must not replace reader disclosures")
    disclosure_checks = {
        "quotient_class_mod_m2": "semua kesamaan berikut dipahami di dalam\n$\\mathfrak m/\\mathfrak m^2$" in lecture and "unsur $\\mathfrak m^2$, yang kelasnya\nnol" in lecture,
        "positive_conductor_and_M_plus": r"\ell\ge1" in lecture and r"\ell'\in M_+" in lecture and "semua $n$ suku benar-benar berada di\n$M_+$" in lecture,
        "monomial_ideal_K_nM_plus": r"K[nM_+]" in lecture and "ideal monom" in lecture,
        "uniform_local_nilpotence": r"(\mathfrak mR_{\mathfrak m})^n=0" in worksheet and r"R=K\times K" in worksheet and "hasil kali\n*hingga*" in worksheet,
        "lowest_component_degree": r"F_mG_q" in solutions and r"m+q<n" in solutions and "kemungkinan pembatalan" in solutions,
        "correct_index_and_span": r"m_j\ge e" in solutions and r"\operatorname{span}_K" in solutions and "ruang linear dengan basis monom" in solutions,
    }
    require(all(disclosure_checks.values()), f"missing correction disclosure: {[key for key, value in disclosure_checks.items() if not value]}")

    normalized = normalized_math("\n".join((lecture, worksheet, solutions)))
    protected = [
        r"d(fg)=f\,dg+g\,df",
        r"\delta(ab)=a\delta(b)+b\delta(a)",
        r"d f:=\overline{f-f(P)}",
        r"(f-f(P))(P)=0",
        r"Y(1+G)=XH(X)",
        r"R=K[X,Y]_{(X,Y)}/(F)",
        r"\mathfrak m^n/\mathfrak m^{n+1}",
        r"\dim_K(R/\mathfrak m^n)=m_Pn+c",
        r"K[X,Y]/(\mathfrak a^n+(F))=R/\mathfrak m^n",
        r"S/\mathfrak a^{n-m}\xrightarrow{\,\cdot F\,}S/\mathfrak a^n",
        r"\dim_K(S/\mathfrak a^n)=\frac{n(n+1)}2",
        r"mn-\frac{m(m-1)}2",
        r"\mathfrak m^n=(\pi^n)",
        r"nM_+=\left\{m\in M\ \middle|\m=m_1+\cdots+m_n\text{ untuk suatu }m_i\in M_+\right\}",
        r"K[nM_+]=\bigoplus_{m\in nM_+}KT^m",
        r"\mathfrak m^n=K[nM_+]",
        r"ne_1-\ell\le\#(M\setminus nM_+)\le(n-1)e_1+\ell",
        r"\frac{\dim_K\left(K[M]/\mathfrak m^n\right)}{n}=e_1",
        r"X_1^{\nu_1}\cdots X_n^{\nu_n}",
        r"\sum_{i=1}^n\nu_i<d",
        r"R/\mathfrak a\cong R_{\mathfrak m}/\mathfrak aR_{\mathfrak m}",
        r"(\mathfrak mR_{\mathfrak m})^n=0",
        r"R_{\mathrm{red}}=R/\sqrt{(0)}",
        r"F_mG_q\ne0",
        r"\deg(F_mG_q)=m+q<n",
        r"nM_+=\mathbb N_{\ge ne}",
        r"k=m_1+\cdots+m_n",
        r"m_j\ge e",
        r"\operatorname{span}_K\{T^m\mid m\in M\setminus nM_+\}",
        r"\dim_K(R/\mathfrak m^n)=(n-1)e+1",
    ]
    missing = [token for token in protected if normalized_math(token) not in normalized]
    require(not missing, f"protected mathematics absent: {missing}")

    ast_receipts: dict[str, Any] = {}
    expected_ast = {
        "lecture-23.md": (21, 198, 0),
        "worksheet-23.md": (17, 74, 0),
        "worksheet-23-solutions.md": (3, 55, 0),
        "media-credits-unit-23.md": (1, 0, 0),
    }
    global_header_ids: list[str] = []
    for name, (header_count, math_count, image_count) in expected_ast.items():
        ast = pandoc_ast(SOURCE / name)
        nodes = list(walk(ast.get("blocks", [])))
        headers_ast = [node for node in nodes if node.get("t") == "Header"]
        maths = [node for node in nodes if node.get("t") == "Math"]
        images = [node for node in nodes if node.get("t") == "Image"]
        header_ids = [node["c"][1][0] for node in headers_ast]
        require(all(header_ids) and len(header_ids) == len(set(header_ids)), f"AST header IDs: {name}")
        require((len(headers_ast), len(maths), len(images)) == (header_count, math_count, image_count), f"AST topology: {name}")
        global_header_ids.extend(header_ids)
        ast_receipts[name] = {
            "headers": len(headers_ast),
            "math_nodes": len(maths),
            "images": len(images),
            "stable_header_ids": len(header_ids),
            "pandoc_warnings": 0,
        }
    require(len(global_header_ids) == 42 and len(global_header_ids) == len(set(global_header_ids)), "global AST stable-ID topology")

    return {
        "source_and_control_facts": facts,
        "stable_ids": len(stable_ids),
        "lecture_semantic_entities": 17,
        "worksheet_exercise_entities": 12,
        "worksheet_definition_entities": 1,
        "exercises": 12,
        "practice_exercises": 7,
        "submitted_exercises": 5,
        "submitted_points": {"8": 4, "9": 3, "10": 5, "11": 5, "12": 3},
        "public_solutions": 2,
        "reader_images": 0,
        "ast": ast_receipts,
        "visible_german_residue": 0,
        "placeholder_count": 0,
        "secret_like_count": 0,
        "invisible_unicode_controls": 0,
        "non_ascii_dashes_u2010_to_u2014": 0,
        "protected_math_checks": len(protected),
        "terminology_bindings": TERM_IDS,
        "correction_bindings": CORRECTION_IDS,
        "visible_correction_disclosures": list(disclosure_checks),
    }


def main() -> int:
    receipt = {
        "schema": "ag-bridge-unit-translation-qa-v1",
        "status": "PASS",
        "unit": 23,
        "verified_date": "2026-08-25",
        "authority": verify_authority(),
        "media_and_rights": verify_media_and_rights(),
        "translation": verify_translation(),
        "provenance": "OpenAI Codex gpt-5.6-sol, Ultra.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "unit": 23, "receipt": OUT.relative_to(ROOT).as_posix(), "bytes": OUT.stat().st_size, "sha256": digest(OUT)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
