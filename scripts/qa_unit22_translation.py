#!/usr/bin/env python3
"""Fail-closed authority, translation, mathematics, accessibility, and rights QA for Unit 22."""

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
AUTH = ROOT / "authority" / "wikiversity" / "unit-22"
SOURCE = ROOT / "source" / "id-ID"
OUT = ROOT / "qa" / "UNIT_22_TRANSLATION_QA.json"

MANIFEST_FACT = (184308, "fefb7f6221a3e71b94649f03c75693f9eb34ec228cedf0af7d9e332aeda7d38a")
MAP_FACT = (14957, "d4b1d1f0a08de69d6fb7da513b8bce9ebaf697d5dad51632d0db063925d05f1e")
AUTHORITY_QA_FACT = (1977, "901c7333f38b9e8a47200e7a877002200b2d60a9afba3b5f39536ba7e02ed882")
FREEZE_FACT = (8874, "05b20bfdb03a7948680886f5d3029c6e75f2c5ac3ae7df6671da818226675c13")
SOURCE_FACTS = {
    "source/id-ID/lecture-22.md": (21213, "cfa8d5f920375021bb65bff969155f0289fac00a56fefea237edac473a22990a"),
    "source/id-ID/worksheet-22.md": (12475, "72accdf7704f2f91e9cc42fb14fef399960006e8da729a21524ec7ae86072203"),
    "source/id-ID/worksheet-22-solutions.md": (12568, "dc164ac9ee01271686afe637ebede3be1a2b92fb76d718f992787d1ebf6d9594"),
    "source/id-ID/media-credits-unit-22.md": (3127, "00d45167d500ad0013dcda970e71448fb9aaef5c6ba0c6bc85f6ac779d515db3"),
}
CONTROL_FACTS = {
    "00_control/TERMINOLOGY.csv": (27509, "d9765073c814b204d52dcbfe4ff255b2457206faa51ca3f94b559fc7479b16a4"),
    "00_control/CORRECTIONS.csv": (50348, "2bd456ce5157e2c91ff1e143e15d8dee0f5eb661d4ea9a76a9c115dc8dc5daae"),
    "authority/UNIT_22_AUTHORITY_FREEZE.md": FREEZE_FACT,
}
EXTERNAL_FACTS = {
    "authority/RIGHTS-unit-22.csv": (7705, "1c7d8493693002363e2482db54c0c421e7124faefc824eddb7a20daf81f071d4"),
    "authority/ASSET_CLOSURE-unit-22.json": (4313, "f0647334a7bd2b2bd1172dce5296812efd80dafadc4376268409a2a063607c45"),
    "authority/commons-imageinfo-unit-22.json": (49302, "7bac3e555b06ac1e1d4caac101b0fad9a8b6acbbcd72ac93c2e6b55b7e23676e"),
    "authority/artifacts/lecture-22-official.pdf": (317848, "ae0905f5a2fc3faf2d52902abd85d79cbc50faf15d0067ed2b368c997e843401"),
    "authority/artifacts/worksheet-22-official.pdf": (141837, "0806b21d473557628ddf3315700756a25bfe5736e33db1e54927e05cf2b2efeb"),
}
SOLUTION_NUMBERS = [5, 6, 9, 10, 12, 14, 15, 16, 18]
SOLUTION_REVIDS = [971273, 1067646, 1067974, 1067981, 1096085, 958122, 1089314, 1089323, 1094625]
SOLUTION_CLOSURE_COUNTS = [7, 10, 13, 10, 10, 7, 9, 11, 13]
TERM_IDS = [f"AGT-{number:04d}" for number in range(168, 182)]
CORRECTION_IDS = [f"AGC-CORR-{number:04d}" for number in range(71, 77)]
ASSET_PATHS = [
    "authority/assets/Tangent_to_a_curve.svg",
    "authority/assets/250px-3_equations_-5.JPG",
    "authority/assets/250px-Frans_Hals_-_Portret_van_René_Descartes.jpg",
    "authority/assets/Kartesisches-Blatt.svg",
    "authority/assets/250px-Intersect3.png",
    "authority/assets/Cercle_tangente_rayon.svg",
    "authority/assets/Cardioid.svg",
]
COMMONS_CREDIT_URLS = [
    "https://commons.wikimedia.org/wiki/File:Tangent_to_a_curve.svg",
    "https://commons.wikimedia.org/wiki/File:3_equations_-5.JPG",
    "https://commons.wikimedia.org/wiki/File:Frans_Hals_-_Portret_van_Ren%C3%A9_Descartes.jpg",
    "https://commons.wikimedia.org/wiki/File:Kartesisches-Blatt.svg",
    "https://commons.wikimedia.org/wiki/File:Intersect3.png",
    "https://commons.wikimedia.org/wiki/File:Cercle_tangente_rayon.svg",
    "https://commons.wikimedia.org/wiki/File:Cardioid.svg",
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
    manifest_fact = check_fact("authority/wikiversity/unit-22/UNIT_AUTHORITY_MANIFEST.json", MANIFEST_FACT)
    map_fact = check_fact("authority/wikiversity/unit-22/ORDERED_EXERCISE_MAP.json", MAP_FACT)
    authority_qa_fact = check_fact("qa/UNIT_22_AUTHORITY_QA.json", AUTHORITY_QA_FACT)
    freeze_fact = check_fact("authority/UNIT_22_AUTHORITY_FREEZE.md", FREEZE_FACT)
    manifest = json.loads((AUTH / "UNIT_AUTHORITY_MANIFEST.json").read_text(encoding="utf-8"))
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    authority_qa = json.loads((ROOT / "qa" / "UNIT_22_AUTHORITY_QA.json").read_text(encoding="utf-8"))

    require(authority_qa["result"] == "PASS" and authority_qa["unit"] == 22, "authority QA state")
    require(authority_qa["authority_manifest"]["sha256"] == MANIFEST_FACT[1], "authority QA manifest binding")
    require(manifest["schema"] == "brenner-unit-authority-freeze-v2" and manifest["unit_number"] == 22, "authority schema/unit")
    require(manifest["source_course_license"] == "CC BY-SA 4.0", "course licence")
    require(manifest["source_course_license_authority"]["declared_license"] == "CC BY-SA 4.0", "course licence authority")
    require(
        (manifest["lecture"]["pageid"], manifest["lecture"]["revid"], manifest["lecture"]["mediawiki_sha1"])
        == (165911, 1051397, "907644dc696a39dc2462e100fe3dd1f8a452fd8a"),
        "lecture identity",
    )
    require(
        (manifest["worksheet"]["pageid"], manifest["worksheet"]["revid"], manifest["worksheet"]["mediawiki_sha1"])
        == (165941, 1062660, "e82e91c94f0a39d73aa10913d6821f673925893e"),
        "worksheet identity",
    )
    require(
        [(row["bytes"], row["sha256"]) for row in manifest["derived_expanded_tex"]]
        == [
            (24142, "ba8f39ddc1cd90388fe9962dd6aabff5aa1b9e37432362e69676b383fe337130"),
            (11130, "f72523eee3cc5d807be6435787581d95da6902348172780cad88423ab19f9e34"),
        ],
        "expanded TeX identities",
    )
    require(manifest["entry_revision_recheck"]["result"] == "PASS", "entry revision recheck")
    require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 131, "lecture closure")
    require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 118, "worksheet closure")
    require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "lecture missing dependency")
    require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "worksheet missing dependency")

    require(len(manifest["files"]) == 84 and sum(row["bytes"] for row in manifest["files"]) == 1029606, "local authority inventory")
    for row in manifest["files"]:
        path = AUTH / row["file"]
        require(path.is_file() and path.stat().st_size == row["bytes"] and digest(path) == row["sha256"], f"authority file replay: {row['file']}")
    require(len(manifest["bounded_external_files"]) == 12 and sum(row["bytes"] for row in manifest["bounded_external_files"]) == 780858, "external authority inventory")
    for row in manifest["bounded_external_files"]:
        path = ROOT / row["file"]
        require(path.is_file() and path.stat().st_size == row["bytes"] and digest(path) == row["sha256"], f"external authority replay: {row['file']}")

    live = manifest["final_live_identity_replay"]
    require(live["result"] == "PASS" and live["wikiversity_identity_count"] == 242, "final Wikiversity replay")
    require(sum(row["title_count"] for row in live["wikiversity_batches"]) == 242, "final replay batch total")
    require(live["commons_pdf_identity_count"] == 2, "final Commons replay")

    require(mapping["unit"] == 22 and mapping["exercise_count"] == 23 and mapping["solution_count"] == 9, "map topology")
    require([row["exercise_number"] for row in mapping["entries"]] == list(range(1, 24)), "exercise order")
    solutions = [row for row in mapping["entries"] if row["has_public_solution"]]
    require([row["exercise_number"] for row in solutions] == SOLUTION_NUMBERS, "solution set")
    require([row["revid"] for row in solutions] == SOLUTION_REVIDS, "solution revisions")
    closures = manifest["solution_transclusion_closures"]
    require([row["exercise_number"] for row in closures] == SOLUTION_NUMBERS, "solution closure order")
    require([row["recursive_transclusion_closure"]["captured_page_count"] for row in closures] == SOLUTION_CLOSURE_COUNTS, "solution closure sizes")
    require(all(row["recursive_transclusion_closure"]["missing_page_count"] == 0 for row in closures), "solution closure completeness")
    wrappers = {row["exercise_number"]: row["direct_wrapper_dependency_titles"] for row in closures}
    require(wrappers[9] == ["Ebene algebraische Kurve/Glatter Punkt/Liegt nur auf einer Komponente/Fakt/Beweis"], "Exercise 9 wrapper")
    require(all(not titles for number, titles in wrappers.items() if number != 9), "unexpected solution wrapper")

    return {
        "manifest": manifest_fact,
        "exercise_map": map_fact,
        "authority_qa": authority_qa_fact,
        "authority_freeze": freeze_fact,
        "lecture_revid": 1051397,
        "worksheet_revid": 1062660,
        "lecture_transclusions": 131,
        "worksheet_transclusions": 118,
        "exercises": 23,
        "public_solutions": 9,
        "solution_numbers": SOLUTION_NUMBERS,
        "solution_recursive_closures": SOLUTION_CLOSURE_COUNTS,
        "wrapper_exercises": [9],
        "authority_files_verified": 84,
        "bounded_external_files_verified": 12,
        "live_wikiversity_identities": 242,
        "live_commons_pdf_identities": 2,
    }


def verify_media_and_rights() -> dict[str, Any]:
    facts = [check_fact(relative, fact) for relative, fact in EXTERNAL_FACTS.items()]
    with (ROOT / "authority" / "RIGHTS-unit-22.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    closure = json.loads((ROOT / "authority" / "ASSET_CLOSURE-unit-22.json").read_text(encoding="utf-8"))
    require(closure["schema"] == "brenner-unit-media-closure-v2" and closure["unit"] == 22, "media closure identity")
    require(closure["reader_media_positions"] == 7 and closure["unique_local_assets"] == 7, "media topology")
    require(closure["animated_html_positions"] == 0 and len(closure["assets"]) == 7, "asset topology")
    require(closure["rights_sha256"] == EXTERNAL_FACTS["authority/RIGHTS-unit-22.csv"][1], "rights binding")
    require(closure["metadata_sha256"] == EXTERNAL_FACTS["authority/commons-imageinfo-unit-22.json"][1], "Commons metadata binding")
    require(closure["reader_credits_required"] is True, "reader credits requirement")
    require(len(rows) == 7, "rights row count")
    expected_ids = [f"br-ak-u22-media-{index:03d}" for index in range(1, 8)]
    require([row["asset_id"] for row in rows] == expected_ids, "rights asset IDs")
    require([row["asset_id"] for row in closure["assets"]] == expected_ids, "closure asset IDs")
    require([row["local_path"] for row in rows] == ASSET_PATHS, "reader asset order")
    require([row["license_short"] for row in rows] == ["Public domain"] * 3 + ["CC BY-SA 3.0"] * 4, "component licence routes")
    require(sum(row["attribution_required"].casefold() == "true" for row in rows) == 4, "attribution topology")
    for row in rows:
        path = ROOT / row["local_path"]
        require(path.is_file() and path.stat().st_size == int(row["local_bytes"]), f"asset bytes: {row['local_path']}")
        require(digest(path) == row["local_sha256"], f"asset hash: {row['local_path']}")
    for relative in ("authority/artifacts/lecture-22-official.pdf", "authority/artifacts/worksheet-22-official.pdf"):
        require((ROOT / relative).read_bytes().startswith(b"%PDF-"), f"PDF signature: {relative}")
    credits = (SOURCE / "media-credits-unit-22.md").read_text(encoding="utf-8")
    require(all(url in credits for url in COMMONS_CREDIT_URLS), "complete component credits")
    require("AxelBoldt" in credits and "Jacj" in credits and "Oleg Alexandrov" in credits, "tangent attribution reconciliation")
    require("GFDL" in credits and "CC BY-SA 2.1 JP" in credits, "raw alternate-rights disclosure")
    require("CC BY-SA 3.0" in credits and "CC BY-SA 4.0" in credits, "component/course licence disclosure")
    require("OpenAI Codex gpt-5.6-sol, Ultra." in credits, "media-credit model provenance")
    return {"reader_media_positions": 7, "binary_assets": 7, "rights_rows": 7, "official_pdf_witnesses": 2, "facts": facts}


def verify_translation() -> dict[str, Any]:
    facts = [check_fact(relative, fact) for relative, fact in SOURCE_FACTS.items()]
    facts.extend(check_fact(relative, fact) for relative, fact in CONTROL_FACTS.items())
    lecture = (SOURCE / "lecture-22.md").read_text(encoding="utf-8")
    worksheet = (SOURCE / "worksheet-22.md").read_text(encoding="utf-8")
    solutions = (SOURCE / "worksheet-22-solutions.md").read_text(encoding="utf-8")
    credits = (SOURCE / "media-credits-unit-22.md").read_text(encoding="utf-8")
    all_text = "\n".join((lecture, worksheet, solutions, credits))

    for name, raw in (("lecture", lecture), ("worksheet", worksheet), ("solutions", solutions)):
        require("translation_status: complete" in raw, f"{name} completion flag")
        require("OpenAI Codex gpt-5.6-sol, Ultra" in raw, f"{name} exact model provenance")
        require('license: "CC BY-SA 4.0' in raw, f"{name} licence metadata")
        require(MANIFEST_FACT[1] in raw or name == "solutions", f"{name} manifest binding")
    require("source_semantic_entities: 20" in lecture, "lecture entity metadata")
    require("edition_bridges: 1" in lecture and "source_corrections: 1" in lecture, "lecture editorial metadata")
    require("source_corrections: 2" in worksheet and "source_corrections: 2" in solutions, "worksheet/solution correction metadata")
    require("public_solution_count: 9" in solutions, "solution count metadata")

    lower = all_text.casefold()
    require(all(token not in lower for token in ("todo", "fixme", "tbd", "placeholder", "lorem ipsum")), "placeholder residue")
    require(not re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|access[_-]?token|bearer\s+[A-Za-z0-9._-]{20,}|api[_-]?key\s*[:=]", all_text, flags=re.I), "secret-like content")
    controls = [(character, f"U+{ord(character):04X}") for character in all_text if unicodedata.category(character) in {"Cc", "Cf"} and character not in "\t\n\r"]
    require(not controls, f"invisible/control Unicode residue: {controls[:5]}")
    prose = strip_nonprose(all_text)
    residue = re.findall(
        r"\b(?:Es sei|Zeige|Aufgabe|Beweis|Einbettungsdimension|Kotangentialraum|glatter Punkt|singulärer Punkt|Tangentialabbildung|partielle Ableitung|Jacobi-Matrix|Kettenregel|Lösung)\b",
        prose,
        flags=re.I,
    )
    require(not residue, f"visible German residue: {residue}")

    headers = re.findall(r"^### Soal 22\.(\d+)(?:[^\n]*)\{#br-ak-2025-2026-w22-ex-(\d{2})\}$", worksheet, flags=re.M)
    require(headers == [(str(index), f"{index:02d}") for index in range(1, 24)], "exercise headers/IDs")
    starred = [int(value) for value in re.findall(r"^### Soal 22\.(\d+) ★", worksheet, flags=re.M)]
    require(starred == SOLUTION_NUMBERS, "solution-star topology")
    points = re.findall(r"^### Soal 22\.(\d+) \(([^)]*poin[^)]*)\)", worksheet, flags=re.M)
    require(points == [("19", "3 poin"), ("20", "4 poin"), ("21", "3 poin"), ("22", "6 poin"), ("23", "4 poin")], "submitted points")
    require(worksheet.index("### Soal 22.18") < worksheet.index("## Soal untuk dikumpulkan") < worksheet.index("### Soal 22.19"), "practice/submitted boundary")
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    entity_comments = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    require(entity_comments == [row["exercise_title"] for row in mapping["entries"]], "exercise entity mapping")
    require(lecture.count("<!-- upstream_entity:") == 20, "lecture semantic entity count")
    lecture_titles = {row["title"] for row in json.loads((AUTH / "UNIT_AUTHORITY_MANIFEST.json").read_text(encoding="utf-8"))["lecture_transclusion_closure"]["pages"]}
    require(set(re.findall(r"<!-- upstream_entity: (.*?) -->", lecture)) <= lecture_titles, "lecture entity authority closure")

    solution_headers = [int(value) for value in re.findall(r"^## Solusi Soal 22\.(\d+) ", solutions, flags=re.M)]
    require(solution_headers == SOLUTION_NUMBERS, "solution headers")
    solution_comments = re.findall(r"<!-- upstream_solution: .*?; pageid=\d+; revid=(\d+) -->", solutions)
    require([int(value) for value in solution_comments] == SOLUTION_REVIDS, "solution comments/revisions")
    require(solutions.count("<!-- upstream_solution_url:") == 9, "solution immutable URLs")
    require("frozen_transclusion:" in solutions and "pageid=84110; revid=1101009" in solutions, "Exercise 9 proof binding")
    back_links = [int(value) for value in re.findall(r"\[Kembali ke Soal 22\.(\d+)\]\(#br-ak-2025-2026-w22-ex-\d{2}\)", solutions)]
    require(back_links == SOLUTION_NUMBERS, "solution backlinks")

    stable_ids = re.findall(r"\{#(br-ak-2025-2026-[^}]+|agc-media-credits-unit-22)\}", all_text)
    require(len(stable_ids) == 58 and len(stable_ids) == len(set(stable_ids)), f"stable-ID topology: {len(stable_ids)}")
    raw_image_paths = re.findall(r"!\[[^\]]+\]\((authority/assets/[^)]+)\)", lecture + "\n" + worksheet)
    require(raw_image_paths == ASSET_PATHS, f"reader asset order/path: {raw_image_paths}")
    require(lecture.count("![") == 5 and worksheet.count("![") == 2 and solutions.count("![") == 0, "reader image topology")

    with (ROOT / "00_control" / "TERMINOLOGY.csv").open(encoding="utf-8", newline="") as stream:
        term_rows = {row["term_id"]: row for row in csv.DictReader(stream)}
    expected_terms = {
        "AGT-0168": ("minimale Erzeugendenzahl", "banyak pembangkit minimal"),
        "AGT-0169": ("Kotangentialraum", "ruang kotangen"),
        "AGT-0170": ("regulärer Ring", "gelanggang reguler"),
        "AGT-0171": ("glatter Punkt", "titik mulus"),
        "AGT-0172": ("singulärer Punkt", "titik singular"),
        "AGT-0173": ("Tangente", "garis singgung"),
        "AGT-0174": ("Tangentialabbildung", "pemetaan tangen"),
        "AGT-0175": ("totales Differential", "diferensial total"),
        "AGT-0176": ("partielle Ableitung", "turunan parsial"),
        "AGT-0177": ("Jacobi-Matrix", "matriks Jacobi"),
        "AGT-0178": ("Kettenregel", "aturan rantai"),
        "AGT-0179": ("geometrisch reduziert", "tereduksi secara geometris"),
        "AGT-0180": ("Kartesisches Blatt", "folium Descartes"),
        "AGT-0181": ("lokale Diffeomorphie", "difeomorfisme lokal"),
    }
    require(list(expected_terms) == TERM_IDS, "terminology ID interval")
    for term_id, (source_term, target_term) in expected_terms.items():
        require(term_id in term_rows and term_rows[term_id]["source_term"] == source_term, f"terminology source: {term_id}")
        require(term_rows[term_id]["preferred_target"] == target_term and term_rows[term_id]["status"] == "admitted", f"terminology target/status: {term_id}")
    preferred_visible = [
        "banyak pembangkit minimal",
        "ruang kotangen",
        "gelanggang reguler",
        "titik mulus",
        "titik singular",
        "garis singgung",
        "pemetaan tangen",
        "diferensial total",
        "turunan parsial",
        "matriks Jacobi",
        "aturan rantai",
        "tereduksi secara geometris",
        "folium Descartes",
    ]
    require(all(term.casefold() in prose.casefold() for term in preferred_visible), "preferred reader terminology absent")
    require(not re.search(r"\b(?:dimensi benaman|pemetaan tangensial|irreduksibel|ireduksibel|derivatif parsial|matriks Jacobian|daun Descartes)\b", prose, flags=re.I), "nonpreferred terminology residue")

    with (ROOT / "00_control" / "CORRECTIONS.csv").open(encoding="utf-8", newline="") as stream:
        corrections = {row["correction_id"]: row for row in csv.DictReader(stream)}
    for correction_id in CORRECTION_IDS:
        require(correction_id in corrections, f"missing correction binding: {correction_id}")
        require(corrections[correction_id]["status"] == "applied_at_unit_22_translation", f"correction status: {correction_id}")
    require(all(correction_id not in all_text for correction_id in CORRECTION_IDS), "ledger IDs must not replace reader disclosures")
    disclosure_checks = {
        "geometric_reducedness": "tereduksi secara geometris" in worksheet and "$K$ tak sempurna" in worksheet,
        "tangent_equation_zero": "memulihkan\nsyarat sama dengan nol" in solutions and r"2a(X-a)+2b(Y-b)=0" in solutions,
        "field_scope": r"\operatorname{char}(K)\notin\{2,3\}" in worksheet and r"\sqrt3\in K" in worksheet and solutions and "satu garis singgung ganda" in worksheet,
        "media_credit": "Baris kredit sumber menamai AxelBoldt" in lecture and "Metadata Commons" in lecture,
        "affine_translation": "perubahan koordinat afin" in lecture and "bukan transformasi\nlinear" in lecture,
        "smoothness_scope": "Jembatan edisi 22.A" in lecture and "kemulusan skema" in lecture,
    }
    require(all(disclosure_checks.values()), f"missing correction/scope disclosure: {[key for key, value in disclosure_checks.items() if not value]}")

    normalized = normalized_math("\n".join((lecture, worksheet, solutions)))
    protected = [
        r"\operatorname{embdim}(R)",
        r"V=U+\mathfrakmV",
        r"\mu(\mathfrakm)=\dim_K\left(\mathfrakm/\mathfrakm^2\right)",
        r"\mathfrakn/\mathfrakn^2\longrightarrow\mathfrakm/\mathfrakm^2",
        r"f=\frac{a_1}{s_1}g_1h_1+\cdots+\frac{a_n}{s_n}g_nh_n",
        r"\mathfrakn/\mathfrakn^2=\bigoplus_{m\inM_+\setminus2M_+}K\,T^m",
        r"F=F_d+F_{d-1}+\cdots+F_1+F_0",
        r"\frac{\partialF}{\partialX}(P)=a",
        r"F_m=G_1\cdotsG_m",
        r"F=X^3+Y^3-3XY=0",
        r"\frac{\partialF}{\partialX}(P)(X-a)+\frac{\partialF}{\partialY}(P)(Y-b)=0",
        r"F=F_1\cdotsF_n",
        r"J(G\circF)_P=J(G)_{F(P)}\circJ(F)_P",
        r"eH=X_1\frac{\partialH}{\partialX_1}+\cdots+X_n\frac{\partialH}{\partialX_n}",
        r"P=(1,5)",
        r"V\left(-2X^3+3X^2Y-Y+\frac{2}{3}\sqrt{\frac{1}{3}}\right)\subseteq\mathbbA_{\mathbbC}^2",
        r"V^3+U^2V-2UV+2U^2-4U-2V",
        r"V\left(X^3+Y^3-3XY+1\right)",
        r"C=V\left(x^3+5x^2y-6xy^2-x^2-xy+4y^2\right)",
        r"X_1^{\nu_1}X_2^{\nu_2}X_3^{\nu_3}\cdotsX_n^{\nu_n}",
        r"\frac{\partial F}{\partial X}(P)&=\frac{\partial(F_1\cdots F_n)}{\partial X}(P)\\&=\sum_{k=1}^nF_1(P)\cdots F_{k-1}(P)\cdot\frac{\partial F_k}{\partial X}(P)\cdot F_{k+1}(P)\cdots F_n(P)",
        r"2a(X-a)+2b(Y-b)=0",
        r"\left(\sqrt{\frac13},\sqrt{\frac13}\right)",
        r"X(X+\mathrm iY)(X-\mathrm iY)",
        r"X^2-3Y^2=(X-\sqrt3Y)(X+\sqrt3Y)",
    ]
    missing = [token for token in protected if normalized_math(token) not in normalized]
    require(not missing, f"protected mathematics absent: {missing}")

    ast_receipts: dict[str, Any] = {}
    expected_ast = {
        "lecture-22.md": (21, 205, 5),
        "worksheet-22.md": (26, 99, 2),
        "worksheet-22-solutions.md": (10, 85, 0),
        "media-credits-unit-22.md": (1, 0, 0),
    }
    ast_image_paths: list[str] = []
    for name, (header_count, math_count, image_count) in expected_ast.items():
        ast = pandoc_ast(SOURCE / name)
        nodes = list(walk(ast.get("blocks", [])))
        headers_ast = [node for node in nodes if node.get("t") == "Header"]
        maths = [node for node in nodes if node.get("t") == "Math"]
        images = [node for node in nodes if node.get("t") == "Image"]
        header_ids = [node["c"][1][0] for node in headers_ast]
        require(all(header_ids) and len(header_ids) == len(set(header_ids)), f"AST header IDs: {name}")
        require((len(headers_ast), len(maths), len(images)) == (header_count, math_count, image_count), f"AST topology: {name}")
        for image in images:
            require(image["c"][1], f"empty image alt: {name}")
            ast_image_paths.append(image["c"][2][0])
        ast_receipts[name] = {
            "headers": len(headers_ast),
            "math_nodes": len(maths),
            "images": len(images),
            "stable_header_ids": len(header_ids),
            "pandoc_warnings": 0,
        }
    require(ast_image_paths == ASSET_PATHS, "AST image path/order")

    return {
        "source_and_control_facts": facts,
        "stable_ids": len(stable_ids),
        "lecture_semantic_entities": 20,
        "worksheet_semantic_entities": 23,
        "exercises": 23,
        "practice_exercises": 18,
        "submitted_exercises": 5,
        "public_solutions": 9,
        "reader_images": 7,
        "image_alts_nonempty": 7,
        "ast": ast_receipts,
        "visible_german_residue": 0,
        "placeholder_count": 0,
        "secret_like_count": 0,
        "invisible_unicode_controls": 0,
        "protected_math_checks": len(protected),
        "terminology_bindings": TERM_IDS,
        "correction_and_scope_bindings": CORRECTION_IDS,
        "visible_editorial_bridges": 1,
    }


def main() -> int:
    receipt = {
        "schema": "ag-bridge-unit-translation-qa-v1",
        "status": "PASS",
        "unit": 22,
        "verified_date": "2026-08-25",
        "authority": verify_authority(),
        "media_and_rights": verify_media_and_rights(),
        "translation": verify_translation(),
        "provenance": "OpenAI Codex gpt-5.6-sol, Ultra.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "unit": 22, "receipt": OUT.relative_to(ROOT).as_posix(), "bytes": OUT.stat().st_size, "sha256": digest(OUT)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
