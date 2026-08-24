#!/usr/bin/env python3
"""Fail-closed authority, translation, mathematics, media, and rights QA for Unit 15."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "authority" / "wikiversity" / "unit-15"
SOURCE = ROOT / "source" / "id-ID"
OUT = ROOT / "qa" / "UNIT_15_TRANSLATION_QA.json"

MANIFEST_FACT = (116332, "86e394725e766838f01eb035ca53044c4d3b85ff20eb99f8fecda9c2a0156425")
MAP_FACT = (11789, "3c8c41458f5418ff858a58748ba4b23bc0a8cb34d9c386c155806b4482760470")
SOURCE_FACTS = {
    "source/id-ID/lecture-15.md": (16666, "e1affd57e9f9d33f7e85a2b8c8fe993ecd821d1fff1075588f51dca2014763b4"),
    "source/id-ID/worksheet-15.md": (13700, "feb6d9c38b669718c548608865f416eb1b3a03ac2d1ce6fac92cb5a288f48784"),
    "source/id-ID/worksheet-15-solutions.md": (6476, "49fecc0631064c646bd8fe2707f2ab84f8e33f32e9c4f99028b4dc9f508ec948"),
    "source/id-ID/media-credits-unit-15.md": (424, "ccb29926735e5cdf47f628e2a66cf8c8e9017d64f3357a116e7e5abec3c41734"),
}
CONTROL_FACTS = {
    "00_control/TERMINOLOGY.csv": (15577, "50b90c41f918d8fc75ea170cecf8063148b1c78540a3d00cc96bff614ebe6cfe"),
    "00_control/CORRECTIONS.csv": (26995, "b0895d2b5e21cb02cb4aabb65c598ee7f190ba2ae6a93c62823cf26718676fd4"),
}
MEDIA_FACTS = {
    "authority/RIGHTS-unit-15.csv": (1980, "28ed5e373e07f80cef981315733e53069bdcf8f14c4447d1d21c3fabb2b5f4d7"),
    "authority/ASSET_CLOSURE-unit-15.json": (4103, "cdf6371ba9e44f9828f166f8da5ecfe4b6141e0b9ba0c7c02a5dfba156fea0a4"),
    "authority/commons-imageinfo-unit-15.json": (13862, "860588698c312dcf2909d9d8fdf41cd6f7b56a8223fb11f2de156c611f20fdb3"),
    "authority/assets/Concentric_Circles.svg": (1322, "6f0e0f26b61f100e45ac7bc5b8848277f5dbdc65800590a6995bf3a40238fe0b"),
    "authority/assets/Concentric_Circles-500.png": (28917, "72640399ebd372c13b73037f056081de05bdf09ced7210ae16b668a298943b98"),
    "scripts/freeze_unit15_media.py": (14581, "8d7e47c3b796a41188fb4bb7c58b46d74edeafea789b1905610b90f407167bdd"),
}
PDF_FACTS = {
    "authority/artifacts/lecture-15-official.pdf": (206189, "f8682cc415719772732e897d005be59f1f261c24a7cb8b1b71886d972b1c92ed"),
    "authority/artifacts/worksheet-15-official.pdf": (160974, "242b92bb6c752d3ed4d49d1396f3643376c2e7140fd2e99db22b2b99eb99c59a"),
}
SOLUTION_NUMBERS = [6, 9, 19, 22]
SOLUTION_REVIDS = [663110, 1095144, 1112864, 1089392]


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
    check_fact("authority/wikiversity/unit-15/UNIT_AUTHORITY_MANIFEST.json", MANIFEST_FACT)
    check_fact("authority/wikiversity/unit-15/ORDERED_EXERCISE_MAP.json", MAP_FACT)
    manifest = json.loads((AUTH / "UNIT_AUTHORITY_MANIFEST.json").read_text(encoding="utf-8"))
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    require(manifest["schema"] == "brenner-unit-authority-freeze-v2", "authority schema")
    require(manifest["unit_number"] == 15, "authority unit")
    require(manifest["lecture"]["revid"] == 1051357, "lecture revision")
    require(manifest["lecture"]["mediawiki_sha1"] == "72949885b4a089a2f30ea68019ce98ea55d1939d", "lecture SHA-1")
    require(manifest["worksheet"]["revid"] == 1062620, "worksheet revision")
    require(manifest["worksheet"]["mediawiki_sha1"] == "346fec4a9ab11ba39f42f25198e5adfc26d6c71c", "worksheet SHA-1")
    require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 116, "lecture closure count")
    require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 142, "worksheet closure count")
    require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "lecture missing transclusion")
    require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "worksheet missing transclusion")
    require(len(manifest["files"]) == 38, "authority file count")
    for row in manifest["files"]:
        path = AUTH / row["file"]
        require(path.is_file() and not path.is_symlink(), f"missing authority file: {row['file']}")
        require(path.stat().st_size == row["bytes"], f"authority bytes: {row['file']}")
        require(digest(path) == row["sha256"], f"authority hash: {row['file']}")
    require(mapping["unit"] == 15, "exercise map unit")
    require(mapping["exercise_count"] == 29, "exercise count")
    require(mapping["solution_count"] == 4, "solution count")
    require([row["exercise_number"] for row in mapping["entries"]] == list(range(1, 30)), "exercise order")
    solutions = [row for row in mapping["entries"] if row["has_public_solution"]]
    require([row["exercise_number"] for row in solutions] == SOLUTION_NUMBERS, "solution-number topology")
    require([row["revid"] for row in solutions] == SOLUTION_REVIDS, "solution revision topology")
    for row in solutions:
        for key in ("xml_file", "html_file"):
            path = AUTH / row[key]
            require(path.is_file() and not path.is_symlink(), f"missing solution witness: {row[key]}")
            require(path.stat().st_size == row[key.replace("file", "bytes")], f"solution bytes: {row[key]}")
            require(digest(path) == row[key.replace("file", "sha256")], f"solution hash: {row[key]}")
    for relative, fact in PDF_FACTS.items():
        check_fact(relative, fact)
        require((ROOT / relative).read_bytes().startswith(b"%PDF-"), f"PDF signature: {relative}")
    return {
        "manifest_bytes": MANIFEST_FACT[0],
        "manifest_sha256": MANIFEST_FACT[1],
        "lecture_revid": 1051357,
        "worksheet_revid": 1062620,
        "lecture_transclusions": 116,
        "worksheet_transclusions": 142,
        "exercises": 29,
        "public_solutions": 4,
        "solution_numbers": SOLUTION_NUMBERS,
        "authority_files_verified": 38,
    }


def verify_media() -> dict[str, Any]:
    facts = [check_fact(relative, fact) for relative, fact in MEDIA_FACTS.items()]
    rights_path = ROOT / "authority" / "RIGHTS-unit-15.csv"
    with rights_path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 1, "rights row count")
    row = rows[0]
    require(row["asset_id"] == "br-ak-u15-media-001", "asset ID")
    require(row["license_short"] == "CC BY-SA 4.0", "component licence")
    for path_key, bytes_key, hash_key in (
        ("local_path", "local_bytes", "local_sha256"),
        ("pdf_local_path", "pdf_local_bytes", "pdf_local_sha256"),
    ):
        asset = ROOT / row[path_key]
        require(asset.is_file() and not asset.is_symlink(), f"missing media asset: {path_key}")
        require(asset.stat().st_size == int(row[bytes_key]), f"media bytes: {path_key}")
        require(digest(asset) == row[hash_key], f"media hash: {path_key}")
    closure = json.loads((ROOT / "authority" / "ASSET_CLOSURE-unit-15.json").read_text(encoding="utf-8"))
    require(closure["unit"] == 15, "media closure unit")
    require(closure["reader_media_positions"] == 1, "media positions")
    require(closure["unique_local_assets"] == 2, "binary media surfaces")
    require(closure["decoded_thumbnail_dimensions"] == [500, 501], "decoded thumbnail dimensions")
    require(closure["rights_sha256"] == MEDIA_FACTS["authority/RIGHTS-unit-15.csv"][1], "rights binding")
    require(closure["reader_credits_sha256"] == SOURCE_FACTS["source/id-ID/media-credits-unit-15.md"][1], "credits binding")
    require(len(closure["official_pdf_component_rights"]) == 2, "PDF component-rights closure")
    return {"media_positions": 1, "binary_surfaces": 2, "rights_rows": 1, "facts": facts}


def verify_translation() -> dict[str, Any]:
    facts = [check_fact(relative, fact) for relative, fact in SOURCE_FACTS.items()]
    facts.extend(check_fact(relative, fact) for relative, fact in CONTROL_FACTS.items())
    lecture = (SOURCE / "lecture-15.md").read_text(encoding="utf-8")
    worksheet = (SOURCE / "worksheet-15.md").read_text(encoding="utf-8")
    solutions = (SOURCE / "worksheet-15-solutions.md").read_text(encoding="utf-8")
    credits = (SOURCE / "media-credits-unit-15.md").read_text(encoding="utf-8")
    all_text = "\n".join((lecture, worksheet, solutions, credits))
    for name, raw in (("lecture", lecture), ("worksheet", worksheet), ("solutions", solutions)):
        require("translation_status: complete" in raw, f"{name} completion flag")
    require("OpenAI Codex\ngpt-5.6-sol, Ultra." in lecture, "exact model provenance")
    require(all(token not in all_text.casefold() for token in ("todo", "fixme", "tbd", "placeholder")), "placeholder residue")
    require(not re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|access[_-]?token|bearer\s+[A-Za-z0-9._-]{20,}", all_text, flags=re.I), "secret-like content")
    prose = strip_nonprose(all_text)
    residue = re.findall(r"\b(?:Es sei|Zeige|Dann|Aufgabe|Beweis|Lokaler Ring|Umgebungsfilter|gerichtetes System|Kolimes|Halm|Funktionenkörper)\b", prose, flags=re.I)
    require(not residue, f"visible German residue: {residue}")
    for rejected in ("lokalisasi", "medan fungsi", "filter ketetanggaan", "sistem berarah"):
        require(rejected not in prose.casefold(), f"nonpreferred term: {rejected}")
    for term in (
        "varietas afin",
        "varietas kuasiafin",
        "gelanggang lokal",
        "lapangan residu",
        "pelokalan pada ideal prima",
        "filter topologis",
        "filter lingkungan",
        "himpunan terarah",
        "sistem terarah",
        "kolimit",
        "tangkai",
        "lapangan fungsi",
    ):
        require(term in prose.casefold(), f"required terminology absent: {term}")

    headers = re.findall(r"^### Soal 15\.(\d+)(?:[^\n]*)\{#br-ak-2025-2026-w15-ex-(\d{2})\}$", worksheet, flags=re.M)
    require(headers == [(str(i), f"{i:02d}") for i in range(1, 30)], "exercise headers/IDs")
    starred = [int(value) for value in re.findall(r"^### Soal 15\.(\d+) ★", worksheet, flags=re.M)]
    require(starred == SOLUTION_NUMBERS, "starred solution topology")
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    entity_comments = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    require(entity_comments == [row["exercise_title"] for row in mapping["entries"]], "exercise entity mapping")
    solution_headers = [int(value) for value in re.findall(r"^## Solusi Soal 15\.(\d+) ", solutions, flags=re.M)]
    require(solution_headers == SOLUTION_NUMBERS, "solution headers")
    solution_comments = re.findall(r"<!-- upstream_solution: .*?; pageid=\d+; revid=(\d+) -->", solutions)
    require([int(value) for value in solution_comments] == SOLUTION_REVIDS, "solution comments/revisions")
    back_links = [int(value) for value in re.findall(r"\[Kembali ke Soal 15\.(\d+)\]\(#br-ak-2025-2026-w15-ex-\d{2}\)", solutions)]
    require(back_links == SOLUTION_NUMBERS, "solution back links")
    stable_ids = re.findall(r"\{#(br-ak-2025-2026-[^}]+)\}", "\n".join((lecture, worksheet, solutions)))
    require(len(stable_ids) == len(set(stable_ids)), "duplicate Unit 15 stable IDs")
    require(len(stable_ids) == 60, f"unexpected stable-ID count: {len(stable_ids)}")
    require(lecture.count("<!-- upstream_entity:") == 14, "lecture semantic entity count")
    require(worksheet.count("<!-- upstream_entity:") == 29, "worksheet semantic entity count")
    require(solutions.count("<!-- upstream_solution:") == 4, "solution provenance count")
    require(lecture.count("![") == 1, "lecture image positions")
    require("authority/assets/Concentric_Circles.svg" in lecture, "media reference")
    require(r"s_i\inM_i" in normalized_math(lecture), "corrected colimit representative type")
    require("AGC-CORR-0032" not in lecture and "AGC-CORR-0033" not in solutions, "ledger IDs must not replace reader disclosures")

    normalized = normalized_math("\n".join((lecture, worksheet, solutions)))
    protected = [
        r"V=K\!-\!\operatorname{Spek}(R)",
        r"\mathfrakpR_{\mathfrakp}",
        r"\Gamma(U,\mathcalO)\longrightarrowQ(R)",
        r"GH'=G'H",
        r"\operatorname{colim}_{i\inI}M_i",
        r"\mathcalO_F=\operatorname{colim}_{U\inF}\Gamma(U,\mathcalO)",
        r"R_{\mathfrakm}\longrightarrow\mathcalO_P",
        r"H(H')^2G=0",
        r"\Gamma(U,\mathcalO)=\bigcap_{P\inU}\mathcalO_P",
        r"Q(S)\congR_{\mathfrakp}/\mathfrakpR_{\mathfrakp}",
        r"h_i\bigl(\varphi(r_i)-\varphi(g_i)x_i\bigr)=0",
        r"\operatorname{colim}_{f\inS}R_f=R_S",
    ]
    missing = [token for token in protected if token not in normalized]
    require(not missing, f"protected mathematics absent: {missing}")

    ast_receipts: dict[str, Any] = {}
    for name in ("lecture-15.md", "worksheet-15.md", "worksheet-15-solutions.md", "media-credits-unit-15.md"):
        ast = pandoc_ast(SOURCE / name)
        nodes = list(walk(ast.get("blocks", [])))
        ast_headers = [node for node in nodes if node.get("t") == "Header"]
        maths = [node for node in nodes if node.get("t") == "Math"]
        images = [node for node in nodes if node.get("t") == "Image"]
        header_ids = [node["c"][1][0] for node in ast_headers]
        require(all(header_ids), f"header without ID: {name}")
        require(len(header_ids) == len(set(header_ids)), f"duplicate AST header ID: {name}")
        ast_receipts[name] = {
            "headers": len(ast_headers),
            "math_nodes": len(maths),
            "images": len(images),
            "stable_header_ids": len(header_ids),
            "pandoc_warnings": 0,
        }
    require(ast_receipts["lecture-15.md"]["headers"] == 23, "lecture AST header count")
    require(ast_receipts["worksheet-15.md"]["headers"] == 32, "worksheet AST header count")
    require(ast_receipts["worksheet-15-solutions.md"]["headers"] == 5, "solution AST header count")

    with (ROOT / "00_control" / "TERMINOLOGY.csv").open(encoding="utf-8", newline="") as stream:
        terms = {row["source_term"]: row for row in csv.DictReader(stream)}
    expected_terms = {
        "affine Varietät": "varietas afin",
        "quasiaffine Varietät": "varietas kuasiafin",
        "lokaler Ring": "gelanggang lokal",
        "topologischer Filter": "filter topologis",
        "Umgebungsfilter": "filter lingkungan",
        "gerichtete Menge": "himpunan terarah",
        "gerichtetes System": "sistem terarah",
        "Kolimes": "kolimit",
        "Halm": "tangkai",
        "Funktionenkörper": "lapangan fungsi",
    }
    for source_term, target_term in expected_terms.items():
        require(terms[source_term]["preferred_target"] == target_term, f"terminology target: {source_term}")
        require(terms[source_term]["status"] == "admitted", f"terminology status: {source_term}")
    with (ROOT / "00_control" / "CORRECTIONS.csv").open(encoding="utf-8", newline="") as stream:
        corrections = {row["correction_id"]: row for row in csv.DictReader(stream)}
    for correction_id in ("AGC-CORR-0032", "AGC-CORR-0033"):
        require(correction_id in corrections, f"missing correction binding: {correction_id}")
        require(corrections[correction_id]["status"] == "applied_at_unit_15_translation", f"correction status: {correction_id}")
    return {
        "source_and_control_facts": facts,
        "stable_ids": len(stable_ids),
        "exercises": 29,
        "public_solutions": 4,
        "ast": ast_receipts,
        "visible_german_residue": 0,
        "placeholder_count": 0,
        "secret_like_count": 0,
        "protected_math_checks": len(protected),
        "correction_bindings": ["AGC-CORR-0032", "AGC-CORR-0033"],
    }


def main() -> int:
    receipt = {
        "schema": "ag-bridge-unit-translation-qa-v1",
        "status": "PASS",
        "unit": 15,
        "verified_date": "2026-08-24",
        "authority": verify_authority(),
        "media_and_rights": verify_media(),
        "translation": verify_translation(),
        "provenance": "OpenAI Codex gpt-5.6-sol, Ultra.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "unit": 15, "receipt": OUT.relative_to(ROOT).as_posix(), "bytes": OUT.stat().st_size, "sha256": digest(OUT)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
