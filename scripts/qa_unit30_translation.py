#!/usr/bin/env python3
"""Fail-closed translation, mathematics, rights, and accessibility QA for Unit 30."""

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
SOURCE = ROOT / "source" / "id-ID"
OUT = ROOT / "qa" / "UNIT_30_TRANSLATION_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"

# These identities deliberately fail closed until the parallel authority and
# translation freeze has produced every final byte. They are replaced only
# with recomputed final identities; the gate never learns hashes at runtime.
FACTS: dict[str, tuple[int, str]] = {
    "authority/wikiversity/unit-30/UNIT_AUTHORITY_MANIFEST.json": (83295, "756ec1f9ea386b8ad0fac38086b6c97f0b94d6dc7a139dc4663911d48655bbe1"),
    "authority/wikiversity/unit-30/ORDERED_EXERCISE_MAP.json": (7720, "7b6ed646202784b0ae03782e76e751336516d2dda0ed17ecf70500ea2d7a491e"),
    "authority/wikiversity/unit-30/lecture-30.xml": (3794, "6b5118904f5cba97127372ccb52bb45a1c0e637202374c2d4842ff8246bd1cf0"),
    "authority/wikiversity/unit-30/lecture-30-expanded.tex": (17474, "0080d009a13829a4c0d75d4ce375090d76c5969b92a426635280c2c1d9af8d61"),
    "authority/wikiversity/unit-30/worksheet-30.xml": (4824, "0525c13b64a201759a6982c6f8885cc3fe456fb23abbd1be9ad1e1e6cc780382"),
    "authority/wikiversity/unit-30/worksheet-30-expanded.tex": (5814, "c32bea5c89b6606a5171f79958a1dccded6575c4cca1ff4ca154fe5961800966"),
    "authority/wikiversity/unit-30/solution-ex03.xml": (5520, "2657d734224c0681b15fd19b6dd1284f704e27b0eb3397e4cf7f91065f43ebcb"),
    "authority/wikiversity/unit-30/solution-ex04.xml": (6791, "1eb565f3f8ca6acd72b53a130427c18b1ca957b804b9ab7463d826396f8e9bd1"),
    "authority/UNIT_30_AUTHORITY_FREEZE.md": (1960, "e743b3d3cc0f28bfd479a676360c05779aee13939b8db5710c0ae6cbb45d6d49"),
    "authority/RIGHTS-unit-30.csv": (724, "8a549164ee7e165ab233fcb0cfe8bd50d4856d71f810437e7c10caa5f43d02d3"),
    "authority/ASSET_CLOSURE-unit-30.json": (3723, "b19821344583f9b07b6f189e49d826fe626878868f59c228c6a977303e510ea3"),
    "qa/UNIT_30_AUTHORITY_QA.json": (2026, "d16817a1327da71327225da925238c347f56a0b2747a9e4bec314e280d9a8504"),
    "qa/UNIT_29_TRANSLATION_QA.json": (6802, "7789a7a131bcf44946204f52c328e24fa96fee0c1e24383994d4485437bffb81"),
    "source/id-ID/lecture-30.md": (16737, "08d79de14854b3df6064e328049f4b729107c7aff350a4299e5ff3faaf266e9e"),
    "source/id-ID/worksheet-30.md": (7879, "6451395d896d6e8d4ff3e7216511309687838d163654e591989801f9e9ac12c6"),
    "source/id-ID/worksheet-30-solutions.md": (6991, "3e46d4bb540acd98d4f33bf91f0e3f08788dc1aa3637992e552eb9bdca6d9809"),
    "source/id-ID/media-credits-unit-30.md": (2147, "65294a2265f27a824b6800e0470f4076bd89e424a817ddb37a612c80f96e0d6e"),
    "source/id-ID/frontmatter-units-01-30.md": (5332, "231f5c64b61d792513e8b9748f1979a9d6a2c5d6e858abc88a937cd54588f3fa"),
    "00_control/TERMINOLOGY.csv": (43924, "2bf2e82d82b9cb6fa35818eb548cd768f5edfbf204bb64efa8ffecae25233f29"),
    "00_control/CORRECTIONS.csv": (85348, "b947d37222432ced8b55f37024ee805a71fcfca66c9e212392772736c1dd3c8f"),
}
TERM_IDS = [f"AGT-{number:04d}" for number in range(266, 277)]
CORRECTION_IDS = [f"AGC-CORR-{number:04d}" for number in range(130, 136)]
DISCREPANCY_ID = "AGC-U30-SRC-001"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def fact(relative: str) -> dict[str, Any]:
    path = ROOT / relative
    expected = FACTS[relative]
    require(path.is_file() and not path.is_symlink(), f"missing/nonregular: {relative}")
    require(expected[0] > 0 and re.fullmatch(r"[0-9a-f]{64}", expected[1]) is not None,
            f"unbound expected identity: {relative}")
    actual = (path.stat().st_size, digest(path))
    require(actual == expected, f"identity drift: {relative}: {actual} != {expected}")
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
    run = subprocess.run(
        [
            "pandoc",
            "--from=markdown+yaml_metadata_block+tex_math_dollars+fenced_divs+bracketed_spans+raw_attribute",
            "--to=json",
            str(path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    require(not run.stderr.strip(), f"Pandoc warning: {path.name}: {run.stderr}")
    return json.loads(run.stdout)


def strip_nonprose(raw: str) -> str:
    raw = re.sub(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", "", raw, flags=re.S)
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    raw = re.sub(r"\x60{3}.*?\x60{3}", "", raw, flags=re.S)
    raw = re.sub(r"\x60[^\x60\n]*\x60", "", raw)
    raw = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", raw)
    raw = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", raw)
    raw = re.sub(r"\$\$.*?\$\$", "", raw, flags=re.S)
    return re.sub(r"\$[^$\n]*\$", "", raw)


def verify() -> dict[str, Any]:
    bound = {name: fact(name) for name in FACTS}
    manifest_sha = FACTS["authority/wikiversity/unit-30/UNIT_AUTHORITY_MANIFEST.json"][1]
    manifest = json.loads((ROOT / "authority/wikiversity/unit-30/UNIT_AUTHORITY_MANIFEST.json").read_text(encoding="utf-8"))
    exercise_map = json.loads((ROOT / "authority/wikiversity/unit-30/ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    closure = json.loads((ROOT / "authority/ASSET_CLOSURE-unit-30.json").read_text(encoding="utf-8"))
    authority_qa = json.loads((ROOT / "qa/UNIT_30_AUTHORITY_QA.json").read_text(encoding="utf-8"))
    baseline = json.loads((ROOT / "qa/UNIT_29_TRANSLATION_QA.json").read_text(encoding="utf-8"))

    require(authority_qa["status"] == "PASS", "authority QA")
    expected_roots = {
        "lecture": {
            "title": "Kurs:Algebraische Kurven (Osnabrück 2012)/Vorlesung 30",
            "pageid": 51997,
            "revid": 1112650,
            "parentid": 793531,
            "timestamp": "2026-08-21T16:27:10Z",
            "mediawiki_sha1": "e457ac9823425ad360cc32d095178e513f79ec94",
            "wikitext_bytes": 662,
        },
        "worksheet": {
            "title": "Kurs:Algebraische Kurven (Osnabrück 2012)/Arbeitsblatt 30",
            "pageid": 50925,
            "revid": 1112597,
            "parentid": 793500,
            "timestamp": "2026-08-21T16:19:24Z",
            "mediawiki_sha1": "2111599a8a79cbd491a5f334baf54bb39e9af931",
            "wikitext_bytes": 1688,
        },
    }
    for kind, expected in expected_roots.items():
        require(all(manifest[kind].get(key) == value for key, value in expected.items()), f"{kind} root identity")
    require({row["kind"]: row["revision_contributor"] for row in manifest["root_revision_contributors"]["records"]} == {
        "lecture": "Bocardodarapti",
        "worksheet": "Bocardodarapti",
    }, "root revision contributors")
    require(manifest["final_live_identity_replay"]["result"] == "PASS", "live authority replay")
    require(manifest["final_live_identity_replay"]["semantic_unique_identity_count"] == 141, "semantic identity union")
    require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 93, "lecture closure")
    require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 63, "worksheet closure")
    require(authority_qa["authority"]["solution_closures_with_root"] == {"3": 13, "4": 14}, "solution closures")
    require(authority_qa["media"]["positions"] == 1 and authority_qa["media"]["assets"] == 1, "authority media topology")

    lecture = (SOURCE / "lecture-30.md").read_text(encoding="utf-8")
    worksheet = (SOURCE / "worksheet-30.md").read_text(encoding="utf-8")
    solutions = (SOURCE / "worksheet-30-solutions.md").read_text(encoding="utf-8")
    credits = (SOURCE / "media-credits-unit-30.md").read_text(encoding="utf-8")
    frontmatter = (SOURCE / "frontmatter-units-01-30.md").read_text(encoding="utf-8")
    named_texts = {
        "lecture": lecture,
        "worksheet": worksheet,
        "solutions": solutions,
        "credits": credits,
    }

    for name, raw in named_texts.items():
        require(MODEL in raw, f"provenance missing: {name}")
        require("translation_status: complete" in raw or name == "credits", f"translation status: {name}")
        require(not any(mark in raw for mark in ("\u2013", "\u2014", "\u2011")), f"Unicode dash: {name}")
        require(not re.search(r"(?i)\b(TODO|TBD|FIXME|LOREM|UNBOUND_PENDING|TO_BE_BOUND|PENDING_UNIT30)\b", raw), f"placeholder: {name}")
        require(not re.search(r"(?i)(ghp_[A-Za-z0-9]{20,}|api[_-]?key\s*[:=]|bearer\s+[A-Za-z0-9._-]{20,})", raw), f"secret-like text: {name}")
        require(not any(unicodedata.category(ch) == "Cf" for ch in raw), f"invisible control: {name}")

    expected_lecture_entities = [
        "Projektive ebene Kurven/Satz von Bézout/Beweisaufbau/Textabschnitt",
        "Schnitttheorie von Kurven/Satz von Bézout/Dimension von Stufe im homogenen Restklassenring/Fakt",
        "Schnitttheorie von Kurven/Satz von Bézout/Injektivität der Multiplikation mit Z im homogenen Restklassenring/Fakt",
        "Schnitttheorie von Kurven/Satz von Bézout/Fakt",
        "Schnitttheorie von Kurven/Satz von Bézout/Es gibt Schnittpunkt/Fakt",
        "Schnitttheorie von Kurven/Satz von Bézout/Maximal mn Schnittpunkte/Fakt",
        "Satz von Bézout/ZY^2-X^3 und (X-Z)^2+Y^2-1/Beispiel",
    ]
    lecture_entities = re.findall(r"<!-- upstream_entity: (.*?) -->", lecture)
    worksheet_entities = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    solution_entities = re.findall(r"<!-- upstream_solution: (.*?); pageid=\d+; revid=\d+ -->", solutions)
    require(lecture_entities == expected_lecture_entities, "lecture entity topology/order")
    require("source_semantic_entities: 7" in lecture, "lecture mapping count metadata")
    require(worksheet_entities == [row["exercise_title"] for row in exercise_map["entries"]], "worksheet authority order")
    require(solution_entities == [row["solution_title"] for row in exercise_map["entries"] if row["has_public_solution"]], "solution authority order")

    require(exercise_map["exercise_count"] == 12 and exercise_map["solution_count"] == 2, "exercise/solution topology")
    public_solution_roots = {
        row["exercise_number"]: {
            key: row[key]
            for key in ("pageid", "revid", "parentid", "timestamp", "mediawiki_sha1", "wikitext_bytes")
        }
        for row in exercise_map["entries"] if row["has_public_solution"]
    }
    require(public_solution_roots == {
        3: {
            "pageid": 21320,
            "revid": 1112942,
            "parentid": 1089325,
            "timestamp": "2026-08-22T09:35:40Z",
            "mediawiki_sha1": "215860c3489569cac5d17132ae794a6720380a8d",
            "wikitext_bytes": 2355,
        },
        4: {
            "pageid": 21596,
            "revid": 1106652,
            "parentid": 1094626,
            "timestamp": "2026-07-12T10:40:58Z",
            "mediawiki_sha1": "1ce667988ed88b94a1a3da789b92451c70a810bc",
            "wikitext_bytes": 3583,
        },
    }, "public solution root identities")
    roles = exercise_map["ordered_role_point_and_star_topology"]
    require(roles["warm_up_numbers"] == [1, 2, 3, 4], "warm-up topology")
    require(roles["submitted_numbers"] == list(range(5, 13)), "submitted topology")
    require(roles["starred_numbers"] == [3, 4] and roles["upload_numbers"] == [], "star/upload topology")
    require(roles["authored_points"] == {str(n): p for n, p in enumerate((3, 3, 4, 7, 6, 5, 5, 4, 4, 4, 4, 5), 1)}, "authored points")
    require(roles["displayed_points"] == {str(n): p for n, p in enumerate((6, 5, 5, 4, 4, 4, 4, 5), 5)}, "displayed points")
    require(roles["submitted_displayed_point_total"] == 37, "submitted point total")
    require([int(value) for value in re.findall(r"(?m)^### Soal 30\.(\d+)", worksheet)] == list(range(1, 13)), "reader exercise order")
    require(re.findall(r"(?m)^### Soal 30\.(\d+) \((\d+) poin\)", worksheet) == [(str(n), str(p)) for n, p in enumerate((6, 5, 5, 4, 4, 4, 4, 5), 5)], "reader displayed points")
    require(re.findall(r"(?m)^### Soal 30\.(\d+) \*", worksheet) == ["3", "4"], "reader stars")
    require("public_solution_count: 2" in solutions and "negative_public_solution_count: 10" in solutions, "solution closure metadata")
    require(re.findall(r"(?m)^## Solusi Soal 30\.(\d+)", solutions) == ["3", "4"], "public solution topology")
    require(re.search(r"Tidak ada solusi tambahan yang\s+dibuat", solutions), "no invented solutions")

    require(all(correction in lecture for correction in CORRECTION_IDS[:3]), "lecture correction disclosures")
    require(CORRECTION_IDS[3] in worksheet and DISCREPANCY_ID in worksheet, "worksheet disclosures")
    require(all(correction in solutions for correction in CORRECTION_IDS[4:]), "solution correction disclosures")
    require(all(correction in "\n".join(named_texts.values()) for correction in CORRECTION_IDS), "correction closure")
    require("B=-QF" in lecture or "B=-qF" in lecture, "restored Koszul sign")
    require(r"\lambda=0" in lecture and "identitas" in lecture, "degree-boundary correction")
    require("AGC-U30-SRC-001" in worksheet and "$X=Y^2$" in worksheet, "semantic-title discrepancy")
    require(r"\mathbb C[Y]_{(Y)}/(Y^2)" in solutions and CORRECTION_IDS[5] in solutions,
            "localization repair and disclosure")

    protected_lecture = [
        r"F,G\in K[X,Y,Z]=P",
        r"P/(F,G)",
        r"P_{\ell-m-n}",
        r"P_{\ell-m}\times P_{\ell-n}",
        r"V_+(Z)",
        r"\sum_P\operatorname{mult}_P(C,D)=mn",
        r"V_+(ZY^2-X^3)",
        r"V_+\bigl((X-Z)^2+Y^2-Z^2\bigr)",
    ]
    protected_worksheet = [
        r"V(Y-X^3)",
        r"V(Y^2-X^3)",
        r"C=V(X-Y^2)",
        r"D=V(Y^2-X^5)",
        r"C=V_+(X^3+Y^3+Z^3)",
        r"V_+(ZY^2-X^3)",
        r"V_+(ZY-X^2)",
        r"V(X^2-Y^3)",
        r"V(X^5-Y^4)",
        r"0\longrightarrow\operatorname{Hom}(P,R)",
    ]
    protected_solutions = [
        r"\{(0,0),(1,1),(\zeta,1),(\zeta^2,1)\}",
        r"\mathbb C[X]/(X^3)",
        r"V_+(YZ^2-X^3)",
        r"V_+(Y^2Z-X^3)",
        r"\mathbb C[Y]_{(Y)}/(Y^2)",
        r"2+8\cdot1=10",
    ]
    for surface in protected_lecture:
        require(surface in lecture, f"protected lecture surface: {surface}")
    for surface in protected_worksheet:
        require(surface in worksheet, f"protected worksheet surface: {surface}")
    for surface in protected_solutions:
        require(surface in solutions, f"protected solution surface: {surface}")

    with (ROOT / "00_control/TERMINOLOGY.csv").open(encoding="utf-8", newline="") as stream:
        terms = list(csv.DictReader(stream))
    with (ROOT / "00_control/CORRECTIONS.csv").open(encoding="utf-8", newline="") as stream:
        corrections = list(csv.DictReader(stream))
    require(len(terms) == 276 and len({row["term_id"] for row in terms}) == 276, "terminology IDs")
    require(len(corrections) == 156 and len({row["correction_id"] for row in corrections}) == 156, "correction IDs")
    term_rows = {row["term_id"]: row for row in terms}
    correction_rows = {row["correction_id"]: row for row in corrections}
    require(all(term_id in term_rows for term_id in TERM_IDS), "Unit 30 terms absent")
    require(all(correction_id in correction_rows for correction_id in CORRECTION_IDS), "Unit 30 corrections absent")
    expected_terms = {
        "AGT-0266": "Teorema Bézout",
        "AGT-0267": "komponen derajat dari gelanggang bergradasi",
        "AGT-0268": "barisan eksak",
        "AGT-0269": "homomorfisme modul",
        "AGT-0270": "funktor Hom",
        "AGT-0271": "titik perpotongan",
        "AGT-0272": "jumlah total multiplisitas perpotongan",
        "AGT-0273": "parabola Neil",
        "AGT-0274": "lingkaran satuan",
        "AGT-0275": "kubik Fermat",
        "AGT-0276": "gelanggang faktor bergradasi oleh ideal homogen",
    }
    require(all(term_rows[key]["preferred_target"] == value for key, value in expected_terms.items()), "Unit 30 terminology values")
    human = strip_nonprose("\n".join(named_texts.values()))
    require(not re.search(r"(?i)\bprojektif\b", human), "nonpreferred projektif residue")
    require(not re.search(r"(?i)\b(es sei|zeige|beweis|aufgabe|schnittpunkt|satz von|neilsche|projektive kurve|homogener restklassenring)\b", human), "visible German residue")

    expected_ast = {
        "lecture-30.md": (16, 193, 1),
        "worksheet-30.md": (15, 44, 0),
        "worksheet-30-solutions.md": (3, 68, 0),
        "media-credits-unit-30.md": (1, 0, 0),
        "frontmatter-units-01-30.md": (2, 0, 0),
    }
    ast_receipts: dict[str, Any] = {}
    unit_ids: list[str] = []
    for name, expected in expected_ast.items():
        require(expected[0] > 0, f"unbound AST expectation: {name}")
        ast = pandoc_ast(SOURCE / name)
        nodes = list(walk(ast.get("blocks", [])))
        headers = [node for node in nodes if node.get("t") == "Header"]
        maths = [node for node in nodes if node.get("t") == "Math"]
        images = [node for node in nodes if node.get("t") == "Image"]
        ids = [node["c"][1][0] for node in headers]
        require((len(headers), len(maths), len(images)) == expected, f"AST topology: {name}")
        require(all(ids) and len(ids) == len(set(ids)), f"AST IDs: {name}")
        if name != "frontmatter-units-01-30.md":
            unit_ids.extend(ids)
        ast_receipts[name] = {
            "headers": len(headers),
            "math_nodes": len(maths),
            "images": len(images),
            "stable_header_ids": len(ids),
            "pandoc_warnings": 0,
        }
    require(
        len(unit_ids) == len(set(unit_ids))
        and all(value.startswith("br-ak-2012-") or value == "agc-media-credits-unit-30" for value in unit_ids),
        "Unit 30 global IDs",
    )
    require(len(unit_ids) == 35, "Unit 30 stable ID count")
    require(sum(ast_receipts[name]["math_nodes"] for name in ("lecture-30.md", "worksheet-30.md", "worksheet-30-solutions.md")) == 305, "Unit 30 math total")

    image_rows = re.findall(r"!\[([^\]]+)\]\((authority/assets/[^)]+)\)", lecture + "\n" + worksheet)
    require([path for _, path in image_rows] == ["authority/assets/Two_cubic_curves.png"], "reader image order")
    require(all(alt.strip() for alt, _ in image_rows), "image alt text")
    closure_assets = {item["local_path"]: item for item in closure["assets"]}
    require(set(closure_assets) == {"authority/assets/Two_cubic_curves.png"}, "asset closure set")
    for _, relative in image_rows:
        item = closure_assets[relative]
        path = ROOT / relative
        require(path.is_file() and path.stat().st_size == item["local_bytes"] and digest(path) == item["local_sha256"], f"reader image drift: {relative}")
    asset = closure_assets["authority/assets/Two_cubic_curves.png"]
    require(asset["selected_form"] == "original" and asset["original_locally_archived"] is True, "media archive semantics")
    require(asset["local_bytes"] == 7957 and asset["local_sha256"] == "489afccf2128371df697f6121da75c376f4910a2404dfe572c7ae7adbdac663a", "media identity")
    require(asset["original_sha1"] == "60f5c1dec89a6806608626cd85cf1e7b94660863", "Commons SHA-1")
    normalized_credits = re.sub(r"\s+", " ", credits)
    require("Two cubic curves.png" in credits and "Hack" in credits and "domain publik" in credits, "media credit")
    require(asset["local_sha256"] in credits and "7.957 byte" in normalized_credits, "media identity disclosure")
    require("CC BY-SA 4.0" in credits and "komponen" in normalized_credits, "component rights disclosure")
    require("tidak membuat klaim pelisensian payung" in normalized_credits, "no blanket relicensing")

    rights_rows = list(csv.DictReader((ROOT / "authority/RIGHTS-unit-30.csv").open(encoding="utf-8", newline="")))
    require(len(rights_rows) == 1, "rights row count")
    rights = rights_rows[0]
    require(rights["asset_id"] == "br-ak-u30-media-001" and rights["local_path"] == "authority/assets/Two_cubic_curves.png", "rights asset binding")
    require(rights["license_short"] == "Public domain" and rights["attribution_required"].lower() == "false", "media license")
    require(rights["artist"] == "Hack" and rights["repository"] == "Wikimedia Commons", "media provenance")
    pdf_rights = closure["official_pdf_component_rights"]
    require(len(pdf_rights) == 2, "official PDF rights count")
    require({row["local_path"] for row in pdf_rights} == {
        "authority/artifacts/lecture-30-official.pdf",
        "authority/artifacts/worksheet-30-official.pdf",
    }, "official PDF paths")
    for row in pdf_rights:
        route = row["component_license_route"]
        require(route["current_print_version_notice"] == "CC BY-SA 4.0", "current PDF rights route")
        require(route["legacy_file_notice"] == "CC BY-SA 2.0 Germany", "legacy PDF rights route")

    cumulative_exercises = 0
    cumulative_solutions = 0
    for number in range(1, 31):
        suffix = f"{number:02d}"
        worksheet_text = (SOURCE / f"worksheet-{suffix}.md").read_text(encoding="utf-8")
        solution_text = (SOURCE / f"worksheet-{suffix}-solutions.md").read_text(encoding="utf-8")
        cumulative_exercises += len(re.findall(r"(?m)^### Soal \d+\.\d+", worksheet_text))
        cumulative_solutions += len(re.findall(r"(?m)^## Solusi Soal ", solution_text))
    require(baseline["status"] == "PASS" and baseline["unit"] == 29, "Unit 29 baseline status")
    require(baseline["cumulative_source"] == {
        "lectures": 29,
        "worksheets": 29,
        "exercises": 681,
        "public_solutions": 120,
        "media_positions": 100,
    }, "Unit 29 cumulative baseline")
    require((cumulative_exercises, cumulative_solutions, 100 + len(image_rows)) == (693, 122, 101), "cumulative source counts")
    flat_front = re.sub(r"\s+", " ", frontmatter)
    require("Unit 1-30" in flat_front and "693 soal" in flat_front and "122 solusi publik" in flat_front, "frontmatter coverage")
    require(manifest_sha in frontmatter and MODEL in frontmatter, "frontmatter manifest/provenance")
    require("tidak menyiratkan dukungan" in flat_front and "bukan klaim lisensi payung" in flat_front, "frontmatter rights/nonendorsement")

    return {
        "bound_facts": bound,
        "authority": {
            "lecture_root_plus_dependencies": 94,
            "worksheet_root_plus_dependencies": 64,
            "solution_root_plus_dependencies": {"3": 13, "4": 14},
            "semantic_live_union": 141,
        },
        "translation": {
            "lecture_semantic_entities": 7,
            "worksheet_exercises": 12,
            "public_solutions": 2,
            "negative_solution_candidates": 10,
            "stable_ids": len(unit_ids),
            "math_nodes": sum(ast_receipts[name]["math_nodes"] for name in ("lecture-30.md", "worksheet-30.md", "worksheet-30-solutions.md")),
            "reader_media_positions": 1,
            "visible_correction_disclosures": 6,
            "source_discrepancy_disclosures": 1,
            "terminology_bindings": TERM_IDS,
            "correction_bindings": CORRECTION_IDS,
            "visible_german_residue": 0,
            "placeholder_count": 0,
            "secret_like_count": 0,
            "unicode_dash_count": 0,
            "invisible_unicode_controls": 0,
        },
        "ast": ast_receipts,
        "cumulative_source": {
            "lectures": 30,
            "worksheets": 30,
            "exercises": 693,
            "public_solutions": 122,
            "media_positions": 101,
            "stable_source_ids": 1519 + len(unit_ids),
        },
        "rights": {
            "public_domain_media": 1,
            "original_media_locally_archived": True,
            "official_pdf_component_routes": 2,
            "blanket_relicense_claim": False,
        },
        "revision_contributors": {
            "lecture_root": "Bocardodarapti",
            "worksheet_root": "Bocardodarapti",
            "solution_3": "Bocardodarapti",
            "solution_4": "Arbota",
        },
    }


def main() -> int:
    receipt = {
        "schema": "ag-bridge-unit-translation-qa-v1",
        "status": "PASS",
        "unit": 30,
        "verified_date": "2026-08-28",
        **verify(),
        "provenance": MODEL + ".",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "status": "PASS",
        "unit": 30,
        "receipt": OUT.relative_to(ROOT).as_posix(),
        "bytes": OUT.stat().st_size,
        "sha256": digest(OUT),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
