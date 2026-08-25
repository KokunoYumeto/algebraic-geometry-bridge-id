#!/usr/bin/env python3
"""Fail-closed authority, translation, mathematics, and rights QA for Unit 21."""

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
AUTH = ROOT / "authority" / "wikiversity" / "unit-21"
SOURCE = ROOT / "source" / "id-ID"
OUT = ROOT / "qa" / "UNIT_21_TRANSLATION_QA.json"

MANIFEST_FACT = (142834, "d85444ddfc66c8e77d52db3f3abc0a186e5dd598789edaaf890b3c09cf00f923")
MAP_FACT = (9992, "9329621bbdd62df63f01d7298dc2a4a65a296211db131f8d8730b7d308fd5f47")
FREEZE_FACT = (5585, "d60f85cc2f8394ca5c1735e9ecf0424c883036c4e2a8ab6ae5271daacf8bffc7")
SOURCE_FACTS = {
    "source/id-ID/lecture-21.md": (17276, "4bfbb794483fdc0466acda10c7e63fa09891ad8da435888b2b59a0e051c7b8a6"),
    "source/id-ID/worksheet-21.md": (14505, "9fe5a9e27c5de0b17ec1e0512c1d4368d21ad886c7bc5f4d4a27b6a27bf089f9"),
    "source/id-ID/worksheet-21-solutions.md": (5662, "e872b5002fa8bf278e907b8247a74a23f9efb09eeba1f4610df655dd5d25c4bc"),
    "source/id-ID/media-credits-unit-21.md": (935, "e4076d9aa394dd6901e49dd9c73216eb80d8f0938ea7571f4d6cc30d87e44f67"),
}
CONTROL_FACTS = {
    "00_control/TERMINOLOGY.csv": (25187, "db3184ec04fe01f6712e46b3b7b36131f1a5838574e3dd07d6bdc36d02493590"),
    "00_control/CORRECTIONS.csv": (46027, "ae31d9a7ef70c031e84e524dc129454705b1fa87d8a21a91bc3dc631949a39bc"),
    "authority/UNIT_21_AUTHORITY_FREEZE.md": FREEZE_FACT,
}
EXTERNAL_FACTS = {
    "authority/ASSET_CLOSURE-unit-21.json": (5705, "8708a399d7c950101609281c14fe4e48eb02aa70335a7ad6cf7ef4194e9bc483"),
    "authority/RIGHTS-unit-21.csv": (443, "6b8de6f5a63f32d9f22e7fb69c98ba2d787121a2437a392602571504c2a1c544"),
    "authority/commons-imageinfo-unit-21.json": (7983, "62a31cd0b5759ac7ab18ae47203a1285d6bb3d4825fbe407140da2a4a3192be1"),
    "authority/artifacts/lecture-21-official.pdf": (189481, "12c5dd813cd7d574aaeca33c02dbab1f8cbc4de131030c31dd9eba4007e14ebd"),
    "authority/artifacts/worksheet-21-official.pdf": (155433, "5457b23d9e4dfb6054fa0cdd1d7c823440307ed4d4710a9af244573b8bf89440"),
}
SOLUTION_NUMBERS = [3, 8]
SOLUTION_REVIDS = [1068126, 1113184]
SOLUTION_CLOSURE_COUNTS = [9, 17]
TERM_IDS = [f"AGT-{number:04d}" for number in range(150, 168)]
CORRECTION_IDS = [f"AGC-CORR-{number:04d}" for number in range(62, 71)]
SOURCE_CORRECTION_IDS = CORRECTION_IDS[:6]
BRIDGE_IDS = CORRECTION_IDS[6:]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path, algorithm: str = "sha256") -> str:
    value = hashlib.new(algorithm)
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
    return raw


def normalized_math(raw: str) -> str:
    return re.sub(r"\s+", "", raw)


def verify_authority() -> dict[str, Any]:
    manifest_fact = check_fact("authority/wikiversity/unit-21/UNIT_AUTHORITY_MANIFEST.json", MANIFEST_FACT)
    map_fact = check_fact("authority/wikiversity/unit-21/ORDERED_EXERCISE_MAP.json", MAP_FACT)
    freeze_fact = check_fact("authority/UNIT_21_AUTHORITY_FREEZE.md", FREEZE_FACT)
    manifest = json.loads((AUTH / "UNIT_AUTHORITY_MANIFEST.json").read_text(encoding="utf-8"))
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))

    require(manifest["schema"] == "brenner-unit-authority-freeze-v2", "authority schema")
    require(manifest["unit_number"] == 21, "authority unit")
    require(manifest["source_course_license"] == "CC BY-SA 4.0", "course licence")
    require(manifest["source_course_license_authority"]["declared_license"] == "CC BY-SA 4.0", "licence authority")
    require(manifest["source_course_license_authority"]["recursive_transclusion_closure"]["captured_page_count"] == 1, "licence closure")
    require(manifest["lecture"]["pageid"] == 165910 and manifest["lecture"]["revid"] == 1112312, "lecture identity")
    require(manifest["lecture"]["mediawiki_sha1"] == "05c51f6e29f6ec12aef400195396ca517924b094", "lecture SHA-1")
    require(manifest["worksheet"]["pageid"] == 165940 and manifest["worksheet"]["revid"] == 1062605, "worksheet identity")
    require(manifest["worksheet"]["mediawiki_sha1"] == "38a7856a5df3695eb80874194bc043dda3377f90", "worksheet SHA-1")
    require(manifest["lecture_latex_page"]["pageid"] == 165974 and manifest["lecture_latex_page"]["revid"] == 1033020, "lecture /latex identity")
    require(manifest["worksheet_latex_page"]["pageid"] == 166034 and manifest["worksheet_latex_page"]["revid"] == 1033082, "worksheet /latex identity")
    require(
        [(row["bytes"], row["sha256"]) for row in manifest["derived_expanded_tex"]]
        == [
            (20239, "0a6fc74c8d01069d327fe25c5203bf4587b4564c8409ad57f625c3ac16ceb62f"),
            (17259, "d49d171f1e6dea766ba1ff7bca9fce1a44ef38fff87fc3064b4071cdfb1ce9a4"),
        ],
        "expanded TeX identities",
    )
    require(manifest["entry_revision_recheck"]["result"] == "PASS", "entry revision recheck")
    require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 122, "lecture closure count")
    require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 144, "worksheet closure count")
    require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "lecture missing transclusion")
    require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "worksheet missing transclusion")

    files = manifest["files"]
    require(len(files) == 54 and len({row["file"] for row in files}) == 54, "authority file inventory")
    require(sum(row["bytes"] for row in files) == 848227, "authority byte inventory")
    for row in files:
        path = AUTH / row["file"]
        require(path.is_file() and not path.is_symlink(), f"missing authority file: {row['file']}")
        require(path.stat().st_size == row["bytes"], f"authority bytes: {row['file']}")
        require(digest(path) == row["sha256"], f"authority hash: {row['file']}")

    external_rows = manifest["bounded_external_files"]
    require(len(external_rows) == 5 and sum(row["bytes"] for row in external_rows) == 359045, "bounded external inventory")
    require({row["file"] for row in external_rows} == set(EXTERNAL_FACTS), "bounded external names")
    for row in external_rows:
        require((row["bytes"], row["sha256"]) == EXTERNAL_FACTS[row["file"]], f"manifest external binding: {row['file']}")
        check_fact(row["file"], EXTERNAL_FACTS[row["file"]])

    live = manifest["final_live_identity_replay"]
    require(live["result"] == "PASS", "final live identity replay")
    require(live["wikiversity_identity_count"] == 223, "live Wikiversity identity count")
    require(len(live["wikiversity_batches"]) == 9, "live replay batch count")
    require(sum(row["title_count"] for row in live["wikiversity_batches"]) == 223, "live replay batch total")
    require(live["commons_pdf_identity_count"] == 2, "Commons PDF identity count")
    for row in live["wikiversity_batches"]:
        require(any(item["file"] == row["file"] and item["sha256"] == row["sha256"] for item in files), f"live replay file binding: {row['file']}")
    require(any(item["file"] == live["commons_replay_file"] and item["sha256"] == live["commons_replay_sha256"] for item in files), "Commons replay binding")

    require(mapping["unit"] == 21 and mapping["exercise_count"] == 26, "exercise map identity/count")
    require(mapping["solution_count"] == 2, "solution count")
    require([row["exercise_number"] for row in mapping["entries"]] == list(range(1, 27)), "exercise order")
    solutions = [row for row in mapping["entries"] if row["has_public_solution"]]
    require([row["exercise_number"] for row in solutions] == SOLUTION_NUMBERS, "solution-number topology")
    require([row["revid"] for row in solutions] == SOLUTION_REVIDS, "solution revision topology")
    require(manifest["solutions"]["exercise_count"] == 26 and manifest["solutions"]["solution_count"] == 2, "manifest solution summary")
    require(manifest["solutions"]["map_sha256"] == MAP_FACT[1], "manifest map binding")
    manifest_solutions = [row for row in manifest["solutions"]["entries"] if row["has_public_solution"]]
    require([row["exercise_number"] for row in manifest_solutions] == SOLUTION_NUMBERS, "manifest solution exercises")
    require([row["revid"] for row in manifest_solutions] == SOLUTION_REVIDS, "manifest solution revisions")
    for row in manifest_solutions:
        for key in ("xml_file", "html_file"):
            path = AUTH / row[key]
            require(path.is_file() and not path.is_symlink(), f"missing solution witness: {row[key]}")
            require(path.stat().st_size == row[key.replace("file", "bytes")], f"solution bytes: {row[key]}")
            require(digest(path) == row[key.replace("file", "sha256")], f"solution hash: {row[key]}")

    closures = manifest["solution_transclusion_closures"]
    require([row["exercise_number"] for row in closures] == SOLUTION_NUMBERS, "solution closure exercises")
    require([row["solution_revid"] for row in closures] == SOLUTION_REVIDS, "solution closure revisions")
    require([row["recursive_transclusion_closure"]["captured_page_count"] for row in closures] == SOLUTION_CLOSURE_COUNTS, "solution closure counts")
    require(all(row["recursive_transclusion_closure"]["missing_page_count"] == 0 for row in closures), "solution missing transclusions")
    require(all(row["direct_wrapper_dependency_titles"] == [] for row in closures), "unexpected solution wrapper")

    identities = {
        (row.get("pageid"), row.get("revid"), row.get("mediawiki_sha1"))
        for row in walk(manifest)
        if "pageid" in row and "revid" in row and "mediawiki_sha1" in row
    }
    correction_authorities = {
        (95378, 1107842, "36f8475dda012b6cbb95729ef298b358f543b9ff"),
        (15938, 1044491, "745e997665c0a461c985ac4faed2ff7639c332ea"),
        (16181, 1037187, "ee2d899f4743d124310af381022327f5a996e95d"),
        (16574, 1097121, "7931676bb5873b4f544e70da924522d4afd841db"),
        (16847, 1113184, "605715141b55061b2efc433f9bd039e84ec8fde0"),
        (95400, 1112454, "c979295f167250e06f397918535c91248177b360"),
        (25025, 1041710, "88029b1c179718d08dd51272269f368b1dfd3a38"),
        (95384, 1083418, "ba8681723f6fe3492514088367fed8ba2eb6e65d"),
        (15870, 1086502, "c876e45a56444d50cf7f8395f7e65c510f54495f"),
        (15878, 1106770, "a90460d4fd6c0928f6871f3b2a590813e05c6c2d"),
        (20586, 975809, "8901bb72f153ce3db82d903fa384c6b425f8a098"),
        (20589, 1086679, "c433baa01be4633f4bf88b38fe2c3593c33f38fc"),
    }
    require(correction_authorities <= identities, "correction/bridge authority closure")

    require(manifest["images"]["substantive_assets"] == [], "substantive media must be empty")
    require(manifest["images"]["reader_media_positions"] == 0, "reader media positions")
    for relative in ("authority/artifacts/lecture-21-official.pdf", "authority/artifacts/worksheet-21-official.pdf"):
        require((ROOT / relative).read_bytes().startswith(b"%PDF-"), f"PDF signature: {relative}")
    require(
        [(row["local_bytes"], row["local_sha256"], row["page_count"], row["license_short"]) for row in manifest["official_pdf_witnesses"]]
        == [
            (189481, EXTERNAL_FACTS["authority/artifacts/lecture-21-official.pdf"][1], 7, "CC BY-SA 4.0"),
            (155433, EXTERNAL_FACTS["authority/artifacts/worksheet-21-official.pdf"][1], 7, "CC BY-SA 4.0"),
        ],
        "official PDF facts",
    )
    return {
        "manifest": manifest_fact,
        "exercise_map": map_fact,
        "authority_freeze": freeze_fact,
        "lecture_revid": 1112312,
        "worksheet_revid": 1062605,
        "lecture_transclusions": 122,
        "worksheet_transclusions": 144,
        "exercises": 26,
        "public_solutions": 2,
        "solution_numbers": SOLUTION_NUMBERS,
        "solution_recursive_closures": SOLUTION_CLOSURE_COUNTS,
        "wrapper_dependencies": 0,
        "authority_files_verified": 54,
        "bounded_external_files_verified": 5,
        "live_wikiversity_identities": 223,
        "live_commons_pdf_identities": 2,
    }


def verify_media_and_rights() -> dict[str, Any]:
    facts = [check_fact(relative, fact) for relative, fact in EXTERNAL_FACTS.items()]
    with (ROOT / "authority" / "RIGHTS-unit-21.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(rows == [], "Unit 21 rights table must have no substantive asset rows")
    closure = json.loads((ROOT / "authority" / "ASSET_CLOSURE-unit-21.json").read_text(encoding="utf-8"))
    require(closure["schema"] == "brenner-unit-media-closure-v2" and closure["unit"] == 21, "media closure identity")
    require(closure["authority_only_boundary"] is True, "authority-only media boundary")
    require(closure["reader_media_positions"] == 0 and closure["unique_local_assets"] == 0, "media topology")
    require(closure["animated_html_positions"] == 0 and closure["assets"] == [], "asset closure")
    require(closure["rights_sha256"] == EXTERNAL_FACTS["authority/RIGHTS-unit-21.csv"][1], "rights binding")
    require(closure["metadata_sha256"] == EXTERNAL_FACTS["authority/commons-imageinfo-unit-21.json"][1], "Commons metadata binding")
    require(closure["reader_credits_required"] is False, "reader credits requirement")
    require(len(closure["official_pdf_component_rights"]) == 2, "PDF component-rights closure")
    require([row["license_short"] for row in closure["official_pdf_component_rights"]] == ["CC BY-SA 4.0", "CC BY-SA 4.0"], "PDF licences")
    require([row["internal_pdf_boilerplate_label"] for row in closure["official_pdf_component_rights"]] == ["CC-by-sa 3.0", "CC-by-sa 3.0"], "PDF internal labels")
    require([row["governing_current_course_and_commons_license"] for row in closure["official_pdf_component_rights"]] == ["CC BY-SA 4.0", "CC BY-SA 4.0"], "PDF governing licences")
    require([row["local_sha256"] for row in closure["official_pdf_component_rights"]] == [EXTERNAL_FACTS["authority/artifacts/lecture-21-official.pdf"][1], EXTERNAL_FACTS["authority/artifacts/worksheet-21-official.pdf"][1]], "PDF rights/hash binding")
    credits = (SOURCE / "media-credits-unit-21.md").read_text(encoding="utf-8")
    require("tidak\nmemuat posisi media pembaca substantif" in credits, "zero-media reader disclosure")
    require("CC BY-SA 3.0" in credits and "CC BY-SA 4.0" in credits, "PDF licence discrepancy disclosure")
    require("OpenAI Codex gpt-5.6-sol, Ultra." in credits, "media-credit model provenance")
    return {"reader_media_positions": 0, "binary_assets": 0, "rights_rows": 0, "official_pdf_witnesses": 2, "facts": facts}


def verify_translation() -> dict[str, Any]:
    facts = [check_fact(relative, fact) for relative, fact in SOURCE_FACTS.items()]
    facts.extend(check_fact(relative, fact) for relative, fact in CONTROL_FACTS.items())
    lecture = (SOURCE / "lecture-21.md").read_text(encoding="utf-8")
    worksheet = (SOURCE / "worksheet-21.md").read_text(encoding="utf-8")
    solutions = (SOURCE / "worksheet-21-solutions.md").read_text(encoding="utf-8")
    credits = (SOURCE / "media-credits-unit-21.md").read_text(encoding="utf-8")
    all_text = "\n".join((lecture, worksheet, solutions, credits))

    for name, raw in (("lecture", lecture), ("worksheet", worksheet), ("solutions", solutions)):
        require("translation_status: complete" in raw, f"{name} completion flag")
        require("OpenAI Codex\ngpt-5.6-sol, Ultra." in raw, f"{name} exact model provenance")
        require('license: "CC BY-SA 4.0' in raw, f"{name} licence metadata")
    require("source_semantic_entities: 13" in lecture, "lecture entity metadata")
    require("edition_bridges: 3" in lecture and "source_corrections: 2" in lecture, "lecture editorial metadata")
    require("public_solution_count: 2" in solutions, "solution-count metadata")
    require("upstream_solution_revisions: \"Soal 21.3=1068126; Soal 21.8=1113184\"" in solutions, "solution-revision metadata")

    lower = all_text.casefold()
    require(all(token not in lower for token in ("todo", "fixme", "tbd", "placeholder", "lorem ipsum")), "placeholder residue")
    require(not re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|access[_-]?token|bearer\s+[A-Za-z0-9._-]{20,}|api[_-]?key\s*[:=]", all_text, flags=re.I), "secret-like content")
    controls = [(character, f"U+{ord(character):04X}") for character in all_text if unicodedata.category(character) == "Cf"]
    require(not controls, f"invisible Unicode control residue: {controls[:5]}")
    prose = strip_nonprose(all_text)
    residue = re.findall(
        r"\b(?:Es sei|Zeige|Aufgabe|Beweis|Bewertungsring|Bewertung|Ordnung|Verschwindungsordnung|Formale Ableitung|Formales Ableiten|Mehrfache Nullstelle|Potenzreihe|Potenzreihenring|Idealprodukt|Teilbarkeitsbeziehung|Primelement|Assoziiertheit|noethersch|Untermodul|Restklassenmodul|Restklassenkörper|Lösung)\b",
        prose,
        flags=re.I,
    )
    require(not residue, f"visible German residue: {residue}")

    headers = re.findall(r"^### Soal 21\.(\d+)(?:[^\n]*)\{#br-ak-2025-2026-w21-ex-(\d{2})\}$", worksheet, flags=re.M)
    require(headers == [(str(i), f"{i:02d}") for i in range(1, 27)], "exercise headers/IDs")
    starred = [int(value) for value in re.findall(r"^### Soal 21\.(\d+) ★", worksheet, flags=re.M)]
    require(starred == SOLUTION_NUMBERS, "starred solution topology")
    point_rows = re.findall(r"^### Soal 21\.(\d+) \(([^)]*poin[^)]*)\)", worksheet, flags=re.M)
    require(point_rows == [("22", "4 poin"), ("23", "4 poin"), ("24", "4 poin"), ("25", "3 poin"), ("26", "3 poin")], "submitted problem points")
    require(worksheet.index("## Soal latihan") < worksheet.index("### Soal 21.1") < worksheet.index("### Soal 21.21"), "practice range")
    require(worksheet.index("### Soal 21.21") < worksheet.index("## Soal untuk dikumpulkan") < worksheet.index("### Soal 21.22"), "submitted boundary")
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    entity_comments = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    require(entity_comments == [row["exercise_title"] for row in mapping["entries"]], "exercise entity mapping")
    require(lecture.count("<!-- upstream_entity:") == 13, "lecture semantic entity count")
    require(worksheet.count("<!-- upstream_entity:") == 26, "worksheet semantic entity count")

    solution_headers = [int(value) for value in re.findall(r"^## Solusi Soal 21\.(\d+) ", solutions, flags=re.M)]
    require(solution_headers == SOLUTION_NUMBERS, "solution headers")
    solution_comments = re.findall(r"<!-- upstream_solution: .*?; pageid=\d+; revid=(\d+) -->", solutions)
    require([int(value) for value in solution_comments] == SOLUTION_REVIDS, "solution comments/revisions")
    require(solutions.count("<!-- upstream_solution_url:") == 2, "solution immutable URLs")
    require("<!-- upstream_transcluded_proof:" not in solutions, "unexpected solution wrapper/proof")
    back_links = [int(value) for value in re.findall(r"\[Kembali ke Soal 21\.(\d+)\]\(#br-ak-2025-2026-w21-ex-\d{2}\)", solutions)]
    require(back_links == SOLUTION_NUMBERS, "solution back links")

    stable_ids = re.findall(r"\{#(br-ak-2025-2026-[^}]+)\}", "\n".join((lecture, worksheet, solutions)))
    require(len(stable_ids) == len(set(stable_ids)), "duplicate Unit 21 stable IDs")
    require(len(stable_ids) == 48, f"unexpected stable-ID count: {len(stable_ids)}")
    require(all(raw.count("![") == 0 for raw in (lecture, worksheet, solutions, credits)), "reader image topology")

    with (ROOT / "00_control" / "TERMINOLOGY.csv").open(encoding="utf-8", newline="") as stream:
        term_rows = {row["term_id"]: row for row in csv.DictReader(stream)}
    expected_terms = {
        "AGT-0150": ("diskreter Bewertungsring", "gelanggang valuasi diskret"),
        "AGT-0151": ("diskrete Bewertung", "valuasi diskret"),
        "AGT-0152": ("Ordnung (Bewertungstheorie)", "orde"),
        "AGT-0153": ("Verschwindungsordnung", "orde pelenyapan"),
        "AGT-0154": ("Ortsuniformisierende", "uniformisator (pembangkit ideal maksimal)"),
        "AGT-0155": ("formale Ableitung", "turunan formal"),
        "AGT-0156": ("formales Ableiten", "pendiferensialan formal"),
        "AGT-0157": ("mehrfache Nullstelle", "akar multipel"),
        "AGT-0158": ("Potenzreihe", "deret pangkat"),
        "AGT-0159": ("Potenzreihenring", "gelanggang deret pangkat"),
        "AGT-0160": ("Idealprodukt", "hasil kali ideal"),
        "AGT-0161": ("totale Teilbarkeitsbeziehung", "relasi keterbagian total"),
        "AGT-0162": ("Primelement", "unsur prima"),
        "AGT-0163": ("Assoziiertheit", "asosiasi"),
        "AGT-0164": ("noethersch", "Noether"),
        "AGT-0165": ("Untermodul", "submodul"),
        "AGT-0166": ("Restklassenmodul", "modul faktor"),
        "AGT-0167": ("Restklassenkörper", "lapangan residu"),
    }
    require(list(expected_terms) == TERM_IDS, "terminology ID interval")
    for term_id, (source_term, target_term) in expected_terms.items():
        require(term_id in term_rows, f"missing terminology binding: {term_id}")
        require(term_rows[term_id]["source_term"] == source_term, f"terminology source: {term_id}")
        require(term_rows[term_id]["preferred_target"] == target_term, f"terminology target: {term_id}")
        require(term_rows[term_id]["status"] == "admitted", f"terminology status: {term_id}")
        rejected = term_rows[term_id]["rejected_or_variant"]
        require(not re.search(rf"(?<![A-Za-z]){re.escape(rejected)}(?![A-Za-z])", prose, flags=re.I), f"nonpreferred term: {term_id} {rejected}")
    visible_terms = (
        "gelanggang valuasi diskret",
        "valuasi diskret",
        "orde",
        "orde pelenyapan",
        "uniformisator",
        "pembangkit ideal maksimal",
        "turunan formal",
        "pendiferensialan formal",
        "akar multipel",
        "deret pangkat",
        "hasil kali ideal",
        "unsur prima",
        "asosiasi",
        "Noether",
        "submodul",
        "modul faktor",
        "lapangan residu",
    )
    for term in visible_terms:
        require(term.casefold() in prose.casefold(), f"required reader terminology absent: {term}")
    require("salah satu dari $f$ membagi $g$ atau $g$ membagi $f$" in worksheet, "total-divisibility concept rendering")

    with (ROOT / "00_control" / "CORRECTIONS.csv").open(encoding="utf-8", newline="") as stream:
        corrections = {row["correction_id"]: row for row in csv.DictReader(stream)}
    for correction_id in CORRECTION_IDS:
        require(correction_id in corrections, f"missing correction/bridge binding: {correction_id}")
        require(corrections[correction_id]["status"] == "applied_at_unit_21_translation", f"correction status: {correction_id}")
    require(all(corrections[item]["kind"] != "editorial_bridge" for item in SOURCE_CORRECTION_IDS), "source correction kind topology")
    require(all(corrections[item]["kind"] == "editorial_bridge" for item in BRIDGE_IDS), "bridge kind topology")
    require(all(correction_id not in all_text for correction_id in CORRECTION_IDS), "ledger IDs must not replace reader disclosures")

    disclosure_checks = {
        "positive_monomial_index": "memasukkan\n$T^0=1$" in worksheet and r"m\in M_+" in worksheet,
        "order_domain": "menambahkan\nsyarat " in lecture and r"$f+g\ne0$" in lecture and r"tidak memperluas $\nu$ ke $0$" in solutions,
        "unit_circle_hypotheses": "karakteristik $2$" in worksheet and "tertutup secara aljabar juga dihapus" in worksheet,
        "multiple_root_premise": "Hipotesis $F(a)=0$ ditambahkan" in worksheet,
        "dvr_transition_scope": "koreksi lingkup sumber" in lecture and "tepat dua ideal prima" in lecture,
        "bound_exponent": r"Kuantifikasi $n\in\mathbb N$ ditambahkan" in worksheet,
    }
    require(all(disclosure_checks.values()), f"missing source-correction disclosure: {[key for key, value in disclosure_checks.items() if not value]}")
    require(lecture.count("Jembatan edisi") == 3, "visible edition-bridge count")
    require(all(label in lecture for label in ("Jembatan edisi 21.A", "Jembatan edisi 21.B", "Jembatan edisi 21.C")), "edition-bridge labels")
    require("maksimal di antara ideal-ideal yang tidak beririsan" in lecture and "Jadi $\\mathfrak p$ prima" in lecture, "prime-avoidance bridge")
    require("$S=R/(f)$" in lecture and "$\\widetilde{\\mathfrak m}=\\mathfrak m/(f)$" in lecture, "quotient bridge")
    require("membangkitkan $V$ jika dan hanya jika kelas-kelasnya" in lecture and "jumlah minimal pembangkit" in lecture, "Nakayama generator bridge")

    normalized = normalized_math("\n".join((lecture, worksheet, solutions)))
    protected = [
        r"K[X,Y]_{(X-a,Y-b)}/(F)\cong(K[X,Y]/(F))_{\mathfrakm}",
        r"R\setminus\{0\}\longrightarrow\mathbbN",
        r"\operatorname{ord}(f+g)\geq\min\{\operatorname{ord}(f),\operatorname{ord}(g)\}",
        r"\mathfrakm^n=0",
        r"T=\{1,f,f^2,\ldots\}",
        r"S=R/(f)",
        r"\widetilde{\mathfrakm}=\mathfrakm/(f)",
        r"\mathfrakm^n\subseteq(f)",
        r"h:=\fracfg",
        r"h^{-1}=\fracgf",
        r"h^{-1}\mathfrakm=\fracgf\mathfrakm\subseteq\frac{\mathfrakm^n}{f}\subseteqR",
        r"1=ab\pi",
        r"V/N=\mathfrakm(V/N)",
        r"\mu_R(\mathfrakm)=\dim_k(\mathfrakm/\mathfrakm^2)",
        r"M_+=M\setminus\{0\}",
        r"\mathfrakm=K[M_+]=\left\langleT^m\mathrel{\Big|}m\inM_+\right\rangle",
        r"K[X,Y]/(X^2+Y^2-1)",
        r"\nu:(K^\times,\cdot,1)\longrightarrow(\mathbbZ,+,0)",
        r"R=\{f\inK^\times\mid\nu(f)\geq0\}\cup\{0\}",
        r"F'=na_nX^{n-1}+(n-1)a_{n-1}X^{n-2}+\cdots+3a_3X^2+2a_2X+a_1",
        r"\frac{1}{i!}\left(X^n\right)^{(i)}=\binomniX^{n-i}",
        r"\mathfrakm^{n+1}=\mathfrakm^n",
        r"R\capK[T]=K",
        r"K[X,Y]_{(X,Y)}/(X^2-Y^3)",
        r"Q(R)=R_\pi",
        r"\pi^{-1}=\pi^{-n-1}\pi^n\inT",
        r"\mathfrakm:=\{f\inK^\times\mid\nu(f)\geq1\}\cup\{0\}",
        r"\nu(x/p^n)=0",
    ]
    missing = [token for token in protected if token not in normalized]
    require(not missing, f"protected mathematics absent: {missing}")

    ast_receipts: dict[str, Any] = {}
    expected = {
        "lecture-21.md": (16, 0, True),
        "worksheet-21.md": (29, 0, True),
        "worksheet-21-solutions.md": (3, 0, True),
        "media-credits-unit-21.md": (1, 0, False),
    }
    for name, (header_count, image_count, requires_math) in expected.items():
        ast = pandoc_ast(SOURCE / name)
        nodes = list(walk(ast.get("blocks", [])))
        headers_ast = [node for node in nodes if node.get("t") == "Header"]
        maths = [node for node in nodes if node.get("t") == "Math"]
        images = [node for node in nodes if node.get("t") == "Image"]
        header_ids = [node["c"][1][0] for node in headers_ast]
        require(all(header_ids), f"header without ID: {name}")
        require(len(header_ids) == len(set(header_ids)), f"duplicate AST header ID: {name}")
        require(len(headers_ast) == header_count, f"AST header count: {name}")
        require(len(images) == image_count, f"AST image count: {name}")
        require(bool(maths) is requires_math, f"AST mathematics topology: {name}")
        ast_receipts[name] = {
            "headers": len(headers_ast),
            "math_nodes": len(maths),
            "images": len(images),
            "stable_header_ids": len(header_ids),
            "pandoc_warnings": 0,
        }

    return {
        "source_and_control_facts": facts,
        "stable_ids": len(stable_ids),
        "lecture_semantic_entities": 13,
        "worksheet_semantic_entities": 26,
        "exercises": 26,
        "practice_exercises": 21,
        "submitted_exercises": 5,
        "public_solutions": 2,
        "reader_images": 0,
        "ast": ast_receipts,
        "visible_german_residue": 0,
        "placeholder_count": 0,
        "secret_like_count": 0,
        "invisible_unicode_controls": 0,
        "protected_math_checks": len(protected),
        "terminology_bindings": TERM_IDS,
        "source_correction_bindings": SOURCE_CORRECTION_IDS,
        "editorial_bridge_bindings": BRIDGE_IDS,
        "visible_editorial_bridges": 3,
    }


def main() -> int:
    receipt = {
        "schema": "ag-bridge-unit-translation-qa-v1",
        "status": "PASS",
        "unit": 21,
        "verified_date": "2026-08-25",
        "authority": verify_authority(),
        "media_and_rights": verify_media_and_rights(),
        "translation": verify_translation(),
        "provenance": "OpenAI Codex gpt-5.6-sol, Ultra.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "status": "PASS",
                "unit": 21,
                "receipt": OUT.relative_to(ROOT).as_posix(),
                "bytes": OUT.stat().st_size,
                "sha256": digest(OUT),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
