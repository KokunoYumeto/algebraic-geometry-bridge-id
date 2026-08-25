#!/usr/bin/env python3
"""Fail-closed authority, translation, mathematics, accessibility, and rights QA for Unit 24."""

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
AUTH = ROOT / "authority" / "wikiversity" / "unit-24"
SOURCE = ROOT / "source" / "id-ID"
OUT = ROOT / "qa" / "UNIT_24_TRANSLATION_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra."

MANIFEST_FACT = (119762, "3731896a5980c565d9d69a2e01eee497f13b6f449f2f9c701fce726271c026a5")
MAP_FACT = (10121, "250744d177bc2d5cf2a1cc506a99e05f1250c771de88b214a0e8d5cabfe7b9b8")
AUTHORITY_QA_FACT = (2673, "60b99b9e90a96d1a7a049050b1e0a3c41220f365e61ca758472a01b7668f6ca7")
FREEZE_FACT = (3945, "0313f42a7716e4c918f2531cf927e3bff4b136712284fab13740c4610237e20e")
SOURCE_FACTS = {
    "source/id-ID/lecture-24.md": (21016, "c57dbf838e6e83f2111654b2b35a11da8a63bd4d549676f1b4cc6b25a7692a62"),
    "source/id-ID/worksheet-24.md": (5482, "8d4e1e91890d24f5724dc8c5ae8c62c50e09815f8ded388c42091e9604e41b1a"),
    "source/id-ID/worksheet-24-solutions.md": (2342, "a824bb03e09d251cb006daa017d7034f6a1794f0496b07ad64c2b6110af868b7"),
    "source/id-ID/media-credits-unit-24.md": (1593, "e63177d420cbb485f255dd5e54059ab4150c388391001c35ea61cb3a3085ec5e"),
}
CONTROL_FACTS = {
    "00_control/TERMINOLOGY.csv": (31718, "6193cbff180864b2cff942f9f99a79c24aab473c71f70c160ade356d34ef079d"),
    "00_control/CORRECTIONS.csv": (59424, "4e06c3954eb1fb9845479a207626005ac4c1d21e909149b60b7a7ba4d3071579"),
    "authority/UNIT_24_AUTHORITY_FREEZE.md": FREEZE_FACT,
}
EXTERNAL_FACTS = {
    "authority/RIGHTS-unit-24.csv": (443, "6b8de6f5a63f32d9f22e7fb69c98ba2d787121a2437a392602571504c2a1c544"),
    "authority/ASSET_CLOSURE-unit-24.json": (5802, "6fe01774a095a6ed24549b8972fc1447d938a5d8868bd3bcc55691e88afea579"),
    "authority/artifacts/lecture-24-official.pdf": (90541, "916b8d41a946cdf8ac978112a46e4f6d1dfb6c70fc0efc65a689cb8ff7205df1"),
    "authority/artifacts/worksheet-24-official.pdf": (33474, "733135d556513d01148333551693db2713915ee82ac8faa8ce745e966c073102"),
}
TERM_IDS = [f"AGT-{number:04d}" for number in range(193, 209)]
CORRECTION_IDS = [f"AGC-CORR-{number:04d}" for number in range(83, 91)]
LECTURE_ENTITIES = [
    "Kurs:Algebraische Kurven (Osnabrück 2012)/Vorlesung 24#Tangenten bei Parametrisierungen",
    "Algebraische Kurven/Rationale Parametrisierung/Verhältnis Tangenten/Fakt",
    "Algebraische Kurven/Rationale Parametrisierung/Verhältnis Tangenten/Fakt/Beweis",
    "Endlicher Körper/(t^q-t,t^q-t)/Gerade/Ableitung ist keine Tangente/Beispiel",
    "Ebene algebraische Kurve/x^2-y^2+y^3/Tangente unter Parametrisierung/t ist 2/Beispiel",
    "Kurs:Algebraische Kurven (Osnabrück 2012)/Vorlesung 24#Tangenten bei Raumkurven",
    "Kurs:Algebraische Kurven (Osnabrück 2012)/Vorlesung 24#Tangenten bei Raumkurven/Jacobi-Absatz",
    "Algebraische Raumkurven/Schnitt von zwei gleichgroßen Zylindern/Singuläre Punkte/Beispiel",
    "Kurs:Algebraische Kurven (Osnabrück 2012)/Vorlesung 24#Potenzreihenringe",
    "Potenzreihenring/Allgemein und eine Variable/Einführung/Textabschnitt",
    "Potenzreihenring/Endlich viele Variablen/Formale Potenzreihe/Definition",
    "Potenzreihenring/Endlich viele Variablen/Definition",
    "Kurs:Algebraische Kurven (Osnabrück 2012)/Vorlesung 24#Potenzreihenringe/zusatz1",
    "Formaler Potenzreihenring/Eine Variable/Konstante nicht null, dann Einheit/Fakt",
    "Formaler Potenzreihenring/Eine Variable/Konstante nicht null, dann Einheit/Fakt/Beweis",
    "Formaler Potenzreihenring/Eine Variable/Diskreter Bewertungsring/Fakt",
    "Formaler Potenzreihenring/Eine Variable/Diskreter Bewertungsring/Fakt/Beweis",
    "Formaler Potenzreihenring/Eine Variable/Einsetzen von Potenzreihen mit Konstante null/Definition",
    "Formaler Potenzreihenring/Eine Variable/Einsetzen ergibt Ringhomomorphismus/Fakt",
    "Formaler Potenzreihenring/Eine Variable/Einsetzen ergibt Ringhomomorphismus/Fakt/Beweis",
    "Formaler Potenzreihenring/Eine Variable/T+../Transformierbar auf T/Fakt",
    "Formaler Potenzreihenring/Eine Variable/T+../Transformierbar auf T/Fakt/Beweis",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path, algorithm: str = "sha256") -> str:
    value = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def check_fact(relative: str, expected: tuple[int, str]) -> dict[str, Any]:
    path = ROOT / relative
    require(path.is_file() and not path.is_symlink(), f"missing/nonregular file: {relative}")
    actual = (path.stat().st_size, digest(path))
    require(actual == expected, f"identity drift for {relative}: {actual} != {expected}")
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
    manifest_fact = check_fact("authority/wikiversity/unit-24/UNIT_AUTHORITY_MANIFEST.json", MANIFEST_FACT)
    map_fact = check_fact("authority/wikiversity/unit-24/ORDERED_EXERCISE_MAP.json", MAP_FACT)
    authority_qa_fact = check_fact("qa/UNIT_24_AUTHORITY_QA.json", AUTHORITY_QA_FACT)
    freeze_fact = check_fact("authority/UNIT_24_AUTHORITY_FREEZE.md", FREEZE_FACT)
    manifest = json.loads((AUTH / "UNIT_AUTHORITY_MANIFEST.json").read_text(encoding="utf-8"))
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    authority_qa = json.loads((ROOT / "qa" / "UNIT_24_AUTHORITY_QA.json").read_text(encoding="utf-8"))

    require(authority_qa["result"] == "PASS" and authority_qa["unit"] == 24, "authority QA state")
    require(authority_qa["authority_manifest"]["sha256"] == MANIFEST_FACT[1], "authority QA manifest binding")
    require(authority_qa["authority_freeze_note"]["sha256"] == FREEZE_FACT[1], "authority QA freeze binding")
    require(authority_qa["exercise_count"] == 10, "authority QA exercise count")
    require(authority_qa["practice_numbers"] == list(range(1, 6)), "authority QA practice topology")
    require(authority_qa["submitted_points"] == [5, 3, 3, 3, 6], "authority QA point topology")
    require(authority_qa["public_solution_numbers"] == [4], "authority QA solution topology")
    require(authority_qa["reader_media_positions"] == 0, "authority QA media topology")

    require(manifest["schema"] == "brenner-unit-authority-freeze-v2" and manifest["unit_number"] == 24, "authority schema/unit")
    require(manifest["source_course"] == "Kurs:Algebraische Kurven (Osnabrück 2012)", "source-course identity")
    require(manifest["source_course_license"] == "CC BY-SA 4.0", "semantic course licence")
    route = manifest["source_component_license_route"]
    require(route["semantic_site_rights"]["notice"] == "CC BY-SA 4.0", "semantic-site rights notice")
    require(route["official_pdf_legacy_notice"] == "CC BY-SA 2.0 Germany", "legacy PDF notice")
    require(route["official_pdf_current_print_version_notice"] == "CC BY-SA 4.0", "current PDF notice")
    require(route["no_blanket_relicensing_claim"] is True, "no-blanket-relicensing boundary")
    require(
        (manifest["lecture"]["pageid"], manifest["lecture"]["revid"], manifest["lecture"]["mediawiki_sha1"], manifest["lecture"]["xml_sha256"])
        == (50730, 933672, "af86fa9893c96376f910495b9a5d0c8be417b09e", "0dd11d94f88e81036d00c2662c6377e13e25d749bed7721902ec75c737251bd3"),
        "lecture identity/XML",
    )
    require(
        (manifest["worksheet"]["pageid"], manifest["worksheet"]["revid"], manifest["worksheet"]["mediawiki_sha1"], manifest["worksheet"]["xml_sha256"])
        == (50759, 793492, "507a5966770c007e813734ca85da4e85f8a93b60", "c6b2e329dc1326aef1b0372702a03fba7fc7106c9e866498df92e1fc9508d4b2"),
        "worksheet identity/XML",
    )
    require(
        [(row["bytes"], row["sha256"]) for row in manifest["derived_expanded_tex"]]
        == [
            (21889, "b391d18cc0cea33afedfff5e6db46842d2ef6504843336b71f44eda448f12f5e"),
            (3771, "37b53c3b6049ba45ff4aa1f4b7b4c4f0666e8a97248ba3c6c34a38061b758a4f"),
        ],
        "expanded TeX identities",
    )
    require(manifest["entry_revision_recheck"]["result"] == "PASS", "entry revision recheck")
    require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 121, "lecture closure")
    require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 64, "worksheet closure")
    require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "lecture missing dependency")
    require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "worksheet missing dependency")
    require(manifest["transclusion_topology"]["lecture"]["with_root"] == 122, "lecture root-plus-closure topology")
    require(manifest["transclusion_topology"]["worksheet"]["with_root"] == 65, "worksheet root-plus-closure topology")
    require(manifest["transclusion_topology"]["lecture"]["canonical_identity_rows_sha256"] == "861c2d4566a137c9c3d791480bfa2f1f36a7885798f54f34c8e60557d34e75b2", "lecture identity rows")
    require(manifest["transclusion_topology"]["worksheet"]["canonical_identity_rows_sha256"] == "b02b815554f0c5dbb4e8f5aceb6b7cc7faa747d9c7c1aa136facd1f62d1831f1", "worksheet identity rows")

    require(len(manifest["files"]) == 52 and sum(row["bytes"] for row in manifest["files"]) == 651940, "local authority inventory")
    for row in manifest["files"]:
        path = AUTH / row["file"]
        require(path.is_file() and path.stat().st_size == row["bytes"] and digest(path) == row["sha256"], f"authority file replay: {row['file']}")
    require(len(manifest["bounded_external_files"]) == 4 and sum(row["bytes"] for row in manifest["bounded_external_files"]) == 130260, "external authority inventory")
    for row in manifest["bounded_external_files"]:
        path = ROOT / row["file"]
        require(path.is_file() and path.stat().st_size == row["bytes"] and digest(path) == row["sha256"], f"external authority replay: {row['file']}")

    live = manifest["final_live_identity_replay"]
    require(live["result"] == "PASS" and live["semantic_unique_identity_count"] == 159, "final semantic replay")
    require(sum(row["title_count"] for row in live["semantic_batches"]) == 159, "final replay batch total")
    require(live["local_wikiversity_pdf_identity_count"] == 2, "final local-PDF replay")

    require(mapping["schema"] == "brenner-worksheet-solution-map-v2" and mapping["unit"] == 24, "map schema/unit")
    require(mapping["exercise_count"] == 10 and mapping["solution_count"] == 1, "map topology")
    require([row["exercise_number"] for row in mapping["entries"]] == list(range(1, 11)), "exercise order")
    topology = mapping["ordered_role_point_and_star_topology"]
    require(topology["practice_numbers"] == list(range(1, 6)), "practice topology")
    require(topology["submitted_numbers"] == list(range(6, 11)), "submitted topology")
    require(topology["authored_points"] == {str(index): value for index, value in enumerate([2, 2, 2, 2, 3, 5, 3, 3, 3, 6], start=1)}, "authored point topology")
    require(topology["submitted_displayed_points"] == {"6": 5, "7": 3, "8": 3, "9": 3, "10": 6}, "submitted point topology")
    require(topology["submitted_displayed_point_total"] == 20 and topology["starred_numbers"] == [4], "point total/star topology")
    solutions = [row for row in mapping["entries"] if row["has_public_solution"]]
    require(len(solutions) == 1, "public solution set")
    solution = solutions[0]
    require(
        (solution["exercise_number"], solution["pageid"], solution["revid"], solution["mediawiki_sha1"], solution["xml_sha256"])
        == (4, 168447, 1068135, "c7d3afd4c8e56433e1d4b12c4ebb8e10b460bec0", "7904b98444817d81659d24fafd37e9009c39547c891bce705b0ae4b37f0ec527"),
        "public solution identity/XML",
    )
    closure = manifest["solution_transclusion_closure"]
    require(closure["exercise_number"] == 4 and closure["solution_revid"] == 1068135, "solution closure identity")
    require(closure["recursive_transclusion_closure"]["captured_page_count"] == 17, "solution dependency closure")
    require(closure["recursive_transclusion_closure"]["missing_page_count"] == 0, "solution missing dependency")
    require(closure["topology"]["with_root"] == 18, "solution root-plus-closure topology")
    require(closure["topology"]["canonical_identity_rows_sha256"] == "df98d341ed63b4cbd1b0051d725bfc8606937f489203941525b21bdfd54df7af", "solution identity rows")
    require(closure["direct_wrapper_dependency_titles"] == [], "unexpected solution wrapper")
    require([row["id"] for row in manifest["source_defect_bindings"]] == ["AGC-U24-SRC-001"], "source defect binding")
    require([row["id"] for row in manifest["historical_pdf_defect_bindings"]] == ["AGC-U24-PDF-001", "AGC-U24-PDF-002"], "PDF defect bindings")
    require(manifest["images"]["reader_media_positions"] == 0 and manifest["images"]["substantive_assets"] == [], "authority reader media topology")

    return {
        "manifest": manifest_fact,
        "exercise_map": map_fact,
        "authority_qa": authority_qa_fact,
        "authority_freeze": freeze_fact,
        "source_course": "Kurs:Algebraische Kurven (Osnabrück 2012)",
        "lecture_revid": 933672,
        "worksheet_revid": 793492,
        "lecture_transclusions_exact": 121,
        "worksheet_transclusions_exact": 64,
        "lecture_with_root": 122,
        "worksheet_with_root": 65,
        "exercises": 10,
        "public_solution_numbers": [4],
        "solution_revisions": [1068135],
        "solution_recursive_closure": 17,
        "solution_with_root": 18,
        "authority_files_verified": 52,
        "bounded_external_files_verified": 4,
        "live_semantic_wikiversity_identities": 159,
        "live_local_wikiversity_pdf_identities": 2,
        "source_defect_bindings": 1,
        "historical_pdf_defect_bindings": 2,
    }


def verify_media_and_rights() -> dict[str, Any]:
    facts = [check_fact(relative, expected) for relative, expected in EXTERNAL_FACTS.items()]
    with (ROOT / "authority" / "RIGHTS-unit-24.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    closure = json.loads((ROOT / "authority" / "ASSET_CLOSURE-unit-24.json").read_text(encoding="utf-8"))
    require(closure["schema"] == "brenner-unit-media-closure-v2" and closure["unit"] == 24, "media closure identity")
    require(closure["authority_only_boundary"] is True, "authority-only media boundary")
    require(closure["reader_media_positions"] == 0 and closure["unique_local_assets"] == 0, "zero-media topology")
    require(closure["animated_html_positions"] == 0 and closure["assets"] == [], "asset topology")
    require(closure["rights_sha256"] == EXTERNAL_FACTS["authority/RIGHTS-unit-24.csv"][1], "rights binding")
    require(closure["reader_credits_required"] is False, "reader credits requirement")
    require(rows == [], "rights file must be header-only at zero-media boundary")
    require(closure["official_pdf_witnesses_are_not_media_positions"] is True, "PDF/media separation")
    pdf_rights = closure["official_pdf_component_rights"]
    require([row["local_path"] for row in pdf_rights] == ["authority/artifacts/lecture-24-official.pdf", "authority/artifacts/worksheet-24-official.pdf"], "PDF rights order")
    require(all(row["component_license_route"]["current_print_version_notice"] == "CC BY-SA 4.0" for row in pdf_rights), "PDF current licence route")
    require(all(row["component_license_route"]["legacy_file_notice"] == "CC BY-SA 2.0 Germany" for row in pdf_rights), "PDF legacy licence route")
    require(all(row["component_license_route"]["embedded_pdf_label"] is None for row in pdf_rights), "embedded-PDF licence claim")
    surfaces = closure["accessibility"]["official_pdf_surfaces"]
    require(all(row["encrypted"] is False for row in surfaces), "PDF encryption topology")
    require(all(row["tagged_pdf"] is False and row["structure_tree_present"] is False for row in surfaces), "PDF tag/structure topology")
    require(all(row["document_language"] is None and row["outline_or_bookmark_count"] == 0 for row in surfaces), "PDF language/outline topology")
    require([row["id"] for row in closure["component_discrepancies"]["historical_pdf_math"]] == ["AGC-U24-PDF-001", "AGC-U24-PDF-002"], "media-closure PDF defects")
    for relative in ("authority/artifacts/lecture-24-official.pdf", "authority/artifacts/worksheet-24-official.pdf"):
        require((ROOT / relative).read_bytes().startswith(b"%PDF-"), f"PDF signature: {relative}")
    credits = (SOURCE / "media-credits-unit-24.md").read_text(encoding="utf-8")
    require("tidak memuat posisi media pembaca substantif" in credits, "zero-media reader disclosure")
    require("CC BY-SA 2.0 Germany" in credits and "CC BY-SA 4.0" in credits, "dual PDF/course licence disclosure")
    require("enam\nhalaman" in credits and "dua halaman" in credits, "PDF page topology disclosure")
    require("tidak bertag" in credits and "tidak mempunyai pohon struktur" in credits, "PDF accessibility disclosure")
    require("$G=x^2+z^2-1$" in credits and "$G=y^2+z^2-1$" in credits, "historical/live cylinder disclosure")
    require("$a_{\\ell+1}$" in credits and "$b_{\\ell+1}$" in credits, "coefficient repair disclosure")
    require(MODEL in credits, "media-credit model provenance")
    return {
        "reader_media_positions": 0,
        "binary_assets": 0,
        "rights_rows": 0,
        "official_pdf_witnesses": 2,
        "official_pdf_pages": [6, 2],
        "official_pdf_tagged": [False, False],
        "dual_component_licence_routes_preserved": True,
        "facts": facts,
    }


def verify_translation() -> dict[str, Any]:
    facts = [check_fact(relative, expected) for relative, expected in SOURCE_FACTS.items()]
    facts.extend(check_fact(relative, expected) for relative, expected in CONTROL_FACTS.items())
    lecture = (SOURCE / "lecture-24.md").read_text(encoding="utf-8")
    worksheet = (SOURCE / "worksheet-24.md").read_text(encoding="utf-8")
    solutions = (SOURCE / "worksheet-24-solutions.md").read_text(encoding="utf-8")
    credits = (SOURCE / "media-credits-unit-24.md").read_text(encoding="utf-8")
    all_text = "\n".join((lecture, worksheet, solutions, credits))

    for name, raw in (("lecture", lecture), ("worksheet", worksheet), ("solutions", solutions)):
        require("translation_status: complete" in raw, f"{name} completion flag")
        require("OpenAI Codex gpt-5.6-sol, Ultra" in raw, f"{name} exact model provenance")
        require("CC BY-SA 4.0" in raw, f"{name} semantic-source licence metadata")
        require(MANIFEST_FACT[1] in raw, f"{name} manifest binding")
        require("Osnabrück 2012" in raw, f"{name} exact 2012 source-edition identity")
    require("source_semantic_entities: 22" in lecture and "source_corrections: 6" in lecture, "lecture source topology metadata")
    require("source_corrections: 1" in worksheet and "source_corrections: 1" in solutions, "worksheet/solution correction metadata")
    require("public_solution_count: 1" in solutions, "solution count metadata")
    require("reader_media_positions: 0" in lecture and "reader_media_positions: 0" in worksheet, "zero-media metadata")
    require("0dd11d94f88e81036d00c2662c6377e13e25d749bed7721902ec75c737251bd3" in lecture, "lecture XML binding")
    require("b391d18cc0cea33afedfff5e6db46842d2ef6504843336b71f44eda448f12f5e" in lecture, "lecture TeX binding")
    require("861c2d4566a137c9c3d791480bfa2f1f36a7885798f54f34c8e60557d34e75b2" in lecture, "lecture dependency binding")
    require("c6b2e329dc1326aef1b0372702a03fba7fc7106c9e866498df92e1fc9508d4b2" in worksheet, "worksheet XML binding")
    require("37b53c3b6049ba45ff4aa1f4b7b4c4f0666e8a97248ba3c6c34a38061b758a4f" in worksheet, "worksheet TeX binding")
    require(MAP_FACT[1] in worksheet and MAP_FACT[1] in solutions, "exercise-map source binding")
    require("7904b98444817d81659d24fafd37e9009c39547c891bce705b0ae4b37f0ec527" in solutions, "solution XML frontmatter binding")
    require("br-ak-2025-2026" not in all_text, "wrong source-edition stable-ID namespace")

    lower = all_text.casefold()
    require(all(token not in lower for token in ("todo", "fixme", "tbd", "placeholder", "lorem ipsum")), "placeholder residue")
    require(not re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|access[_-]?token|bearer\s+[A-Za-z0-9._-]{20,}|api[_-]?key\s*[:=]", all_text, flags=re.I), "secret-like content")
    controls = [(character, f"U+{ord(character):04X}") for character in all_text if unicodedata.category(character) in {"Cc", "Cf"} and character not in "\t\n\r"]
    require(not controls, f"invisible/control Unicode residue: {controls[:5]}")
    non_ascii_dashes = [(character, f"U+{ord(character):04X}") for character in all_text if 0x2010 <= ord(character) <= 0x2014]
    require(not non_ascii_dashes, f"non-ASCII dash residue: {non_ascii_dashes[:5]}")
    prose = strip_nonprose(all_text)
    residue = re.findall(
        r"\b(?:Es sei|Zeige|Aufgabe|Beweis|Lösung|Potenzreihenring|Formale Potenzreihe|Tangenten bei|Raumkurven|Konstante nicht null|Diskreter Bewertungsring|Einsetzen ergibt|Glatter Punkt)\b",
        prose,
        flags=re.I,
    )
    require(not residue, f"visible German residue: {residue}")

    headers = re.findall(r"^### Soal 24\.(\d+)(?:[^\n]*)\{#br-ak-2012-w24-ex-(\d{2})\}$", worksheet, flags=re.M)
    require(headers == [(str(index), f"{index:02d}") for index in range(1, 11)], "exercise headers/IDs")
    starred = [int(value) for value in re.findall(r"^### Soal 24\.(\d+) ★", worksheet, flags=re.M)]
    require(starred == [4], "solution-star topology")
    points = re.findall(r"^### Soal 24\.(\d+) \(([^)]*poin[^)]*)\)", worksheet, flags=re.M)
    require(points == [("6", "5 poin"), ("7", "3 poin"), ("8", "3 poin"), ("9", "3 poin"), ("10", "6 poin")], "submitted points")
    require(worksheet.index("### Soal 24.5") < worksheet.index("## Soal untuk dikumpulkan") < worksheet.index("### Soal 24.6"), "practice/submitted boundary")
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    worksheet_comments = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    require(worksheet_comments == [row["exercise_title"] for row in mapping["entries"]] and len(worksheet_comments) == 10, "ordered worksheet entity mappings")
    lecture_comments = re.findall(r"<!-- upstream_entity: (.*?) -->", lecture)
    require(lecture_comments == LECTURE_ENTITIES and len(lecture_comments) == 22, "ordered lecture semantic entity mappings")

    solution_headers = [int(value) for value in re.findall(r"^## Solusi Soal 24\.(\d+) ", solutions, flags=re.M)]
    require(solution_headers == [4], "solution headers")
    solution_comments = re.findall(r"<!-- upstream_solution: (.*?); pageid=(\d+); revid=(\d+) -->", solutions)
    require(
        solution_comments
        == [("Potenzreihenring eine Variable/Abbildung der Lokalisierung an maximalen Ideal/Aufgabe/Lösung", "168447", "1068135")],
        "solution comment/identity",
    )
    require(solutions.count("<!-- upstream_solution_url:") == 1, "solution immutable URL count")
    require("https://de.wikiversity.org/w/index.php?oldid=1068135" in solutions, "solution oldid URL")
    require(re.findall(r"\[Kembali ke Soal 24\.(\d+)\]\(#br-ak-2012-w24-ex-\d{2}\)", solutions) == ["4"], "solution backlink")

    stable_ids = re.findall(r"\{#(br-ak-2012-[^}]+|agc-media-credits-unit-24)\}", all_text)
    require(len(stable_ids) == 36 and len(stable_ids) == len(set(stable_ids)), f"stable-ID topology: {len(stable_ids)}")
    require({"br-ak-2012-l24", "br-ak-2012-w24", "br-ak-2012-w24-solutions", "agc-media-credits-unit-24"} <= set(stable_ids), "2012 stable-ID roots")
    require(not re.search(r"!\[[^\]]*\]\(", lecture + worksheet + solutions + credits), "reader image topology")

    with (ROOT / "00_control" / "TERMINOLOGY.csv").open(encoding="utf-8", newline="") as stream:
        term_rows = {row["term_id"]: row for row in csv.DictReader(stream)}
    expected_terms = {
        "AGT-0193": ("formale Potenzreihe", "deret pangkat formal"),
        "AGT-0194": ("eingesetzte Potenzreihe", "deret pangkat hasil substitusi"),
        "AGT-0195": ("Einsetzen", "substitusi"),
        "AGT-0196": ("konstanter Term", "suku konstan"),
        "AGT-0197": ("Anfangsterm", "suku awal"),
        "AGT-0198": ("komponentenweise", "komponen demi komponen"),
        "AGT-0199": ("Algebraautomorphismus", "automorfisme aljabar"),
        "AGT-0200": ("Ableitungsvektor", "vektor turunan"),
        "AGT-0201": ("Raumkurve", "kurva ruang"),
        "AGT-0202": ("formale Parametrisierung", "parametrisasi formal"),
        "AGT-0203": ("geordnetes s-Tupel", "s-tupel terurut"),
        "AGT-0204": ("Nullteilerfreiheit", "tanpa pembagi nol"),
        "AGT-0205": ("Algebrahomomorphismus", "homomorfisme aljabar"),
        "AGT-0206": ("Hilbertscher Basissatz", "Teorema Basis Hilbert"),
        "AGT-0207": ("glatte Kurve", "kurva mulus"),
        "AGT-0208": ("konvergieren", "konvergen"),
    }
    require(list(expected_terms) == TERM_IDS, "terminology ID interval")
    for term_id, (source_term, target_term) in expected_terms.items():
        require(term_id in term_rows and term_rows[term_id]["source_term"] == source_term, f"terminology source: {term_id}")
        require(term_rows[term_id]["preferred_target"] == target_term and term_rows[term_id]["status"] == "admitted", f"terminology target/status: {term_id}")
    visibility_needles = {
        "AGT-0193": "deret pangkat formal",
        "AGT-0194": "deret pangkat hasil substitusi",
        "AGT-0195": "substitusi",
        "AGT-0196": "suku konstan",
        "AGT-0197": "suku awal",
        "AGT-0198": "komponen demi komponen",
        "AGT-0199": "automorfisme",
        "AGT-0200": "vektor turunan",
        "AGT-0201": "kurva ruang",
        "AGT-0202": "parametrisasi formal",
        "AGT-0203": "tupel terurut",
        "AGT-0204": "ketiadaan pembagi nol",
        "AGT-0205": "homomorfisme aljabar",
        "AGT-0206": "Teorema Basis Hilbert",
        "AGT-0207": "kurva mulus",
        "AGT-0208": "konvergen",
    }
    missing_terms = [term_id for term_id, needle in visibility_needles.items() if needle.casefold() not in prose.casefold()]
    require(not missing_terms, f"preferred reader terminology absent: {missing_terms}")
    require(not re.search(r"\b(?:deret kuasa formal|deret pangkat tersubstitusi|penyulihan|istilah konstan|suku terdepan|secara komponen|automorfisma aljabar|vektor derivatif|kurva spasial|tuple-s terurut|bebas pembagi nol|kurva licin|memusat)\b", prose, flags=re.I), "nonpreferred terminology residue")

    with (ROOT / "00_control" / "CORRECTIONS.csv").open(encoding="utf-8", newline="") as stream:
        corrections = {row["correction_id"]: row for row in csv.DictReader(stream)}
    for correction_id in CORRECTION_IDS:
        require(correction_id in corrections, f"missing correction binding: {correction_id}")
        require(corrections[correction_id]["status"] == "applied_at_unit_24_translation", f"correction status: {correction_id}")
    require(all(correction_id not in all_text for correction_id in CORRECTION_IDS), "ledger IDs must not replace reader disclosures")
    disclosure_checks = {
        "formal_chain_rule": "Aturan rantai formal" in lecture and r"0=(T(F\circ\varphi))_Q=(TF)_P\circ(T\varphi)_Q" in normalized_math(lecture),
        "finite_field_K_rational_scope": "fungsi pada titik-titik $K$-rasional" in lecture and "bukan morfisme\n> konstan" in lecture,
        "characteristic_zero_numerical_example": "kita bekerja di atas lapangan $K$ berkarakteristik nol" in lecture and "kemulusan dan arah garis singgung harus diperiksa kembali" in lecture,
        "live_cylinder_and_exact_scope": r"G=y^2+z^2-1" in normalized_math(lecture) and r"\operatorname{char}(K)\ne2" in normalized_math(lecture) and normalized_math(r"r_1,r_2\in K^\times") in normalized_math(lecture) and "kuadrat jari-jari tak nol" in lecture,
        "formal_evaluation_at_zero": r"\operatorname{ev}_0" in lecture and "rujukan gantung" in lecture and r"F(0)=a_0" in normalized_math(lecture),
        "coefficient_family_repair": r"b_{\ell+1}T^{\ell+1}" in normalized_math(lecture) and "Indeks keluarga\n> koefisien yang benar" in lecture,
        "full_substitution_recurrence": r"c_k=\sum_{s=0}^ka_s" in normalized_math(lecture) and r"(j_1,\ldots,j_s)\in\mathbbN_+^s" in normalized_math(lecture),
        "substitution_automorphism": r"F(G)=T" in normalized_math(lecture) and r"a_kb_1^k" in normalized_math(lecture) and r"G^j\ne0" in normalized_math(lecture),
        "worksheet_curve_repair": r"C=V\left(Y^2-X^2-X^3\right)" in normalized_math(worksheet) and r"(x,y)=\left(t^2-1,t(t^2-1)\right)" in normalized_math(worksheet) and "Substitusi langsung memberi" in worksheet,
        "worksheet_ring_parentheses_and_inclusion": "(K[X])[[Y]]" in worksheet and "(K[[Y]])[X]" in worksheet and "tentukan arah inklusinya" in worksheet,
        "solution_operand_and_localization": r"P(0)\ne0" in normalized_math(solutions) and "sifat universal pelokalan" in solutions and normalized_math(r"K[T]_{(T)}\longrightarrow K[[T]]") in normalized_math(solutions),
    }
    require(all(disclosure_checks.values()), f"missing protected/correction disclosure: {[key for key, value in disclosure_checks.items() if not value]}")

    normalized = normalized_math("\n".join((lecture, worksheet, solutions)))
    protected = [
        r"0=(T(F\circ\varphi))_Q=(TF)_P\circ(T\varphi)_Q",
        r"t&\longmapsto(t^q-t,t^q-t)",
        r"V(y^2-x^2-x^3)",
        r"(2t,3t^2-1)",
        r"P=(3,6)",
        r"V(-11x+4y+9)",
        r"F=x^2+y^2-1",
        r"G=y^2+z^2-1",
        r"\operatorname{char}(K)\ne2",
        r"xy=xz=yz=0",
        r"r_1,r_2\in K^\times",
        r"F=\sum_\nu a_\nu T^\nu",
        r"c_k=\sum_{i=0}^ka_ib_{k-i}",
        r"R[\![X_1,\ldots,X_n]\!]",
        r"a_0\ne0",
        r"\operatorname{ev}_0\colon K[\![T]\!]&\longrightarrow K",
        r"0=c_n=a_0b_n+a_1b_{n-1}+\cdots+a_{n-1}b_1+a_nb_0",
        r"G=b_\ell T^\ell+b_{\ell+1}T^{\ell+1}+\cdots",
        r"c_{k+\ell}=a_kb_\ell\ne0",
        r"I=(T^j)",
        r"c_k=\sum_{s=0}^ka_s\left(\sum_{j_1+\cdots+j_s=k}b_{j_1}\cdots b_{j_s}\right)",
        r"(j_1,\ldots,j_s)\in\mathbbN_+^s",
        r"K[\![T]\!]&\longrightarrow K[\![S]\!]",
        r"F(G)=T",
        r"a_1=b_1^{-1}",
        r"a_kb_1^k",
        r"G^j\ne0",
        r"C=V\left(Y^2-X^2-X^3\right)",
        r"(x,y)=\left(t^2-1,t(t^2-1)\right)",
        r"y^2-x^2-x^3=(t^2-1)^2\left(t^2-1-(t^2-1)\right)=0",
        r"(K[X])[[Y]]",
        r"(K[[Y]])[X]",
        r"R[[T_1,\ldots,T_n]]",
        r"P(0)\ne0",
        r"K[T]_{(T)}\longrightarrow K[[T]]",
        r"\frac{f}{P}\longmapsto fP^{-1}",
    ]
    missing = [token for token in protected if normalized_math(token) not in normalized]
    require(not missing, f"protected mathematics absent: {missing}")

    ast_receipts: dict[str, Any] = {}
    expected_ast = {
        "lecture-24.md": (20, 227, 0),
        "worksheet-24.md": (13, 32, 0),
        "worksheet-24-solutions.md": (2, 13, 0),
        "media-credits-unit-24.md": (1, 4, 0),
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
    require(len(global_header_ids) == 36 and len(global_header_ids) == len(set(global_header_ids)), "global AST stable-ID topology")

    return {
        "source_and_control_facts": facts,
        "source_edition": "Osnabrück 2012",
        "stable_ids": len(stable_ids),
        "lecture_semantic_entities": 22,
        "worksheet_exercise_entities": 10,
        "exercises": 10,
        "practice_exercises": 5,
        "submitted_exercises": 5,
        "submitted_points": {"6": 5, "7": 3, "8": 3, "9": 3, "10": 6},
        "public_solutions": 1,
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
        "visible_correction_and_protected_disclosures": list(disclosure_checks),
    }


def main() -> int:
    receipt = {
        "schema": "ag-bridge-unit-translation-qa-v1",
        "status": "PASS",
        "unit": 24,
        "verified_date": "2026-08-25",
        "authority": verify_authority(),
        "media_and_rights": verify_media_and_rights(),
        "translation": verify_translation(),
        "provenance": MODEL,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "unit": 24, "receipt": OUT.relative_to(ROOT).as_posix(), "bytes": OUT.stat().st_size, "sha256": digest(OUT)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
