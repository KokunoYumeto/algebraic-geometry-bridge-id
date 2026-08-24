#!/usr/bin/env python3
"""Fail-closed authority, translation, mathematics, media, and rights QA for Unit 14."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "authority" / "wikiversity" / "unit-14"
SOURCE = ROOT / "source" / "id-ID"
OUT = ROOT / "qa" / "UNIT_14_TRANSLATION_QA.json"

MANIFEST_FACT = (123197, "a63c3481d0a9cfa9b960f12c9bf0eec9a5d39cecfb61eddb8f9d96190e52e83e")
MAP_FACT = (10735, "0d223f7f3c56c4714736dfc6eb3dbd40dc8cd3cb30a05f66281a6f2b1b875dbe")
SOURCE_FACTS = {
    "source/id-ID/lecture-14.md": (13617, "64b2519967638116cb3f98a2a200ad23efb5212e5c5c24b7f53e93ad2211f2d4"),
    "source/id-ID/worksheet-14.md": (15430, "45dc11df386efc92ff537be1c53d7e2d9f16938be2fe5cd8eeb14eac347059cc"),
    "source/id-ID/worksheet-14-solutions.md": (4048, "d64c25e2062d8a437465e7bb64d192e6d3ae347cdd6780c02e5146331cbe44dd"),
    "source/id-ID/media-credits-unit-14.md": (403, "b7960d839016c9f6705c1fdba68685a889c1af3261d2339190931e5f9f8b3dc3"),
}
CONTROL_FACTS = {
    "00_control/TERMINOLOGY.csv": (13543, "c9abe9920bfa08031502b528a9008c77cec5d2aebf2c59ca38f40c78b99156c0"),
    "00_control/CORRECTIONS.csv": (25971, "354ca7a26819774967b9f2b26bb0041ecc63022acf946483feaedbc1cf560d8b"),
}
MEDIA_FACTS = {
    "authority/RIGHTS-unit-14.csv": (1858, "9c377f7c679ff0730bcd075201a4d587a322f004b118b0e31fc9c51b267e8973"),
    "authority/ASSET_CLOSURE-unit-14.json": (3658, "8fd50fae2515e6150e3d81c98573dd7bb204211e787d68405f7c3b03aab452d0"),
    "authority/commons-imageinfo-unit-14.json": (20306, "b2632266b022c81f2853549e49b4307a7f80f6d0ecd648377f0597bddd3a4cca"),
    "authority/assets/Monkey_Saddle_Surface_Shaded-500.png": (158107, "0b47780791f72a9e3359bdaafebbea1a26e3fd33d39dda22b093848ecab9c2e7"),
    "scripts/freeze_unit14_media.py": (13516, "14b7e0c8ddf6f20e5412bf49fd169330854ea713d4f412604c2901d2eaaae47e"),
}
PDF_FACTS = {
    "authority/artifacts/lecture-14-official.pdf": (935025, "2e8707f9041d6b9560c5e52a45981a3ee894ee47e747d9b4fd606a6998aa2241"),
    "authority/artifacts/worksheet-14-official.pdf": (169746, "352cccfd0d3ac8688ea25f179dfa6898b3fd2596f8c4b4ef2c198a65c50cde99"),
}
SOLUTION_NUMBERS = [2, 7]
SOLUTION_REVIDS = [1068085, 1095255]


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
    check_fact("authority/wikiversity/unit-14/UNIT_AUTHORITY_MANIFEST.json", MANIFEST_FACT)
    check_fact("authority/wikiversity/unit-14/ORDERED_EXERCISE_MAP.json", MAP_FACT)
    manifest = json.loads((AUTH / "UNIT_AUTHORITY_MANIFEST.json").read_text(encoding="utf-8"))
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    require(manifest["schema"] == "brenner-unit-authority-freeze-v2", "authority schema")
    require(manifest["unit_number"] == 14, "authority unit")
    require(manifest["lecture"]["revid"] == 1051343, "lecture revision")
    require(manifest["lecture"]["mediawiki_sha1"] == "5bc2e2c3db815edeb4f10640564c8cd793de74a8", "lecture SHA-1")
    require(manifest["worksheet"]["revid"] == 1061213, "worksheet revision")
    require(manifest["worksheet"]["mediawiki_sha1"] == "3313c0d85b8477557eca2efe9b74d71d3b712a4b", "worksheet SHA-1")
    require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 106, "lecture closure count")
    require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 164, "worksheet closure count")
    require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "lecture missing transclusion")
    require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "worksheet missing transclusion")
    require(len(manifest["files"]) == 35, "authority file count")
    for row in manifest["files"]:
        path = AUTH / row["file"]
        require(path.is_file() and not path.is_symlink(), f"missing authority file: {row['file']}")
        require(path.stat().st_size == row["bytes"], f"authority bytes: {row['file']}")
        require(digest(path) == row["sha256"], f"authority hash: {row['file']}")
    require(mapping["unit"] == 14, "exercise map unit")
    require(mapping["exercise_count"] == 27, "exercise count")
    require(mapping["solution_count"] == 2, "solution count")
    require([row["exercise_number"] for row in mapping["entries"]] == list(range(1, 28)), "exercise order")
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
        "lecture_revid": 1051343,
        "worksheet_revid": 1061213,
        "lecture_transclusions": 106,
        "worksheet_transclusions": 164,
        "exercises": 27,
        "public_solutions": 2,
        "solution_numbers": SOLUTION_NUMBERS,
        "authority_files_verified": 35,
    }


def verify_media() -> dict[str, Any]:
    facts = [check_fact(relative, fact) for relative, fact in MEDIA_FACTS.items()]
    rights_path = ROOT / "authority" / "RIGHTS-unit-14.csv"
    with rights_path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 1, "rights row count")
    row = rows[0]
    require(row["asset_id"] == "br-ak-u14-media-001", "asset ID")
    require(bool(row["license_short"] or row["usage_terms"]), "missing component licence")
    asset = ROOT / row["local_path"]
    require(asset.is_file() and not asset.is_symlink(), "missing media asset")
    require(asset.stat().st_size == int(row["local_bytes"]), "media asset bytes")
    require(digest(asset) == row["local_sha256"], "media asset hash")
    closure = json.loads((ROOT / "authority" / "ASSET_CLOSURE-unit-14.json").read_text(encoding="utf-8"))
    require(closure["unit"] == 14, "media closure unit")
    require(closure["reader_media_positions"] == 1, "media positions")
    require(closure["unique_local_assets"] == 1, "binary media surfaces")
    require(closure["rights_sha256"] == MEDIA_FACTS["authority/RIGHTS-unit-14.csv"][1], "rights binding")
    require(closure["reader_credits_sha256"] == SOURCE_FACTS["source/id-ID/media-credits-unit-14.md"][1], "credits binding")
    require(len(closure["official_pdf_component_rights"]) == 2, "PDF component-rights closure")
    return {"media_positions": 1, "binary_surfaces": 1, "rights_rows": 1, "facts": facts}


def verify_translation() -> dict[str, Any]:
    facts = [check_fact(relative, fact) for relative, fact in SOURCE_FACTS.items()]
    facts.extend(check_fact(relative, fact) for relative, fact in CONTROL_FACTS.items())
    lecture = (SOURCE / "lecture-14.md").read_text(encoding="utf-8")
    worksheet = (SOURCE / "worksheet-14.md").read_text(encoding="utf-8")
    solutions = (SOURCE / "worksheet-14-solutions.md").read_text(encoding="utf-8")
    credits = (SOURCE / "media-credits-unit-14.md").read_text(encoding="utf-8")
    all_text = "\n".join((lecture, worksheet, solutions, credits))
    for name, raw in (("lecture", lecture), ("worksheet", worksheet), ("solutions", solutions)):
        require("translation_status: complete" in raw, f"{name} completion flag")
    require("OpenAI Codex\ngpt-5.6-sol, Ultra." in lecture, "exact model provenance")
    require(all(token not in all_text.casefold() for token in ("todo", "fixme", "tbd", "placeholder")), "placeholder residue")
    require(not re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|access[_-]?token|bearer\s+[A-Za-z0-9._-]{20,}", all_text, flags=re.I), "secret-like content")
    prose = strip_nonprose(all_text)
    residue = re.findall(r"\b(?:Es sei|Zeige|Dann|Aufgabe|Beweis|Schnittring|Strukturgarbe|Prägarbe|minimales Primideal)\b", prose, flags=re.I)
    require(not residue, f"visible German residue: {residue}")
    for rejected in ("fungsi algebraik", "gelanggang irisan", "presheaf"):
        require(rejected not in prose.casefold(), f"nonpreferred term: {rejected}")
    for term in ("fungsi aljabar", "gelanggang seksi", "berkas struktur", "praberkas", "ideal prima minimal", "pemetaan restriksi"):
        require(term in prose.casefold(), f"required terminology absent: {term}")

    headers = re.findall(r"^### Soal 14\.(\d+)(?:[^\n]*)\{#br-ak-2025-2026-w14-ex-(\d{2})\}$", worksheet, flags=re.M)
    require(headers == [(str(i), f"{i:02d}") for i in range(1, 28)], "exercise headers/IDs")
    starred = [int(value) for value in re.findall(r"^### Soal 14\.(\d+) ★", worksheet, flags=re.M)]
    require(starred == SOLUTION_NUMBERS, "starred solution topology")
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    entity_comments = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    require(entity_comments == [row["exercise_title"] for row in mapping["entries"]], "exercise entity mapping")
    solution_headers = [int(value) for value in re.findall(r"^## Solusi Soal 14\.(\d+) ", solutions, flags=re.M)]
    require(solution_headers == SOLUTION_NUMBERS, "solution headers")
    solution_comments = re.findall(r"<!-- upstream_solution: .*?; pageid=\d+; revid=(\d+) -->", solutions)
    require([int(value) for value in solution_comments] == SOLUTION_REVIDS, "solution comments/revisions")
    back_links = [int(value) for value in re.findall(r"\[Kembali ke Soal 14\.(\d+)\]\(#br-ak-2025-2026-w14-ex-\d{2}\)", solutions)]
    require(back_links == SOLUTION_NUMBERS, "solution back links")
    stable_ids = re.findall(r"\{#(br-ak-2025-2026-[^}]+)\}", "\n".join((lecture, worksheet, solutions)))
    require(len(stable_ids) == len(set(stable_ids)), "duplicate Unit 14 stable IDs")
    require(len(stable_ids) == 54, f"unexpected stable-ID count: {len(stable_ids)}")
    require(lecture.count("<!-- upstream_entity:") == 11, "lecture semantic entity count")
    require(worksheet.count("<!-- upstream_entity:") == 27, "worksheet semantic entity count")
    require(solutions.count("<!-- upstream_solution:") == 2, "solution provenance count")
    require(lecture.count("![") == 1, "lecture image positions")
    require("authority/assets/Monkey_Saddle_Surface_Shaded-500.png" in lecture, "media reference")
    require("=\\frac{-t^2}{t-1}" not in normalized_math(solutions), "uncorrected source sign in proof display")
    require("AGC-CORR-0031" not in solutions, "ledger ID must not replace reader disclosure")

    normalized = normalized_math("\n".join((lecture, worksheet, solutions)))
    protected = [
        r"f(Q)=\frac{G(Q)}{H(Q)}",
        r"D(H)\capD(H')=D(HH')",
        r"f=\fracZX=\fracWY",
        r"\Gamma(U,\mathcalO)=\{f:U\longrightarrowK\midf\text{aljabar}\}",
        r"\Gamma(V,\mathcalO)=R",
        r"\Gamma(D(F),\mathcalO)=R_F",
        r"H_1^rH_2^r(G_1H_2-G_2H_1)^r=0",
        r"\Gamma(U,\mathcalO)=\bigcap_{i=1}^nR_{f_i}",
        r"C=V(Y^2-X^2-X^3)",
        r"\rho_{W,U}=\rho_{V,U}\circ\rho_{W,V}",
        r"fg^n=0",
        r"C=V(X^2-Y^3)",
        r"\frac{t^2(1+t)}{(t+1)(t-1)}=\frac{t^2}{t-1}",
    ]
    missing = [token for token in protected if token not in normalized]
    require(not missing, f"protected mathematics absent: {missing}")

    ast_receipts: dict[str, Any] = {}
    for name in ("lecture-14.md", "worksheet-14.md", "worksheet-14-solutions.md", "media-credits-unit-14.md"):
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
    require(ast_receipts["worksheet-14.md"]["headers"] == 32, "worksheet AST header count")
    require(ast_receipts["worksheet-14-solutions.md"]["headers"] == 3, "solution AST header count")

    with (ROOT / "00_control" / "TERMINOLOGY.csv").open(encoding="utf-8", newline="") as stream:
        terms = {row["source_term"]: row for row in csv.DictReader(stream)}
    expected_terms = {
        "algebraische Funktion": "fungsi aljabar",
        "Schnittring": "gelanggang seksi",
        "Strukturgarbe": "berkas struktur",
        "Prägarbe": "praberkas",
        "Garbe": "berkas",
        "Restriktionsabbildung": "pemetaan restriksi",
        "minimales Primideal": "ideal prima minimal",
    }
    for source_term, target_term in expected_terms.items():
        require(terms[source_term]["preferred_target"] == target_term, f"terminology target: {source_term}")
        require(terms[source_term]["status"] == "admitted", f"terminology status: {source_term}")
    with (ROOT / "00_control" / "CORRECTIONS.csv").open(encoding="utf-8", newline="") as stream:
        corrections = {row["correction_id"]: row for row in csv.DictReader(stream)}
    require("AGC-CORR-0031" in corrections, "Unit 14 correction ledger binding")
    require(corrections["AGC-CORR-0031"]["status"] == "applied_at_unit_14_translation", "correction status")
    return {
        "source_and_control_facts": facts,
        "stable_ids": len(stable_ids),
        "exercises": 27,
        "public_solutions": 2,
        "ast": ast_receipts,
        "visible_german_residue": 0,
        "placeholder_count": 0,
        "secret_like_count": 0,
        "protected_math_checks": len(protected),
        "correction_bindings": ["AGC-CORR-0031"],
    }


def main() -> int:
    receipt = {
        "schema": "ag-bridge-unit-translation-qa-v1",
        "status": "PASS",
        "unit": 14,
        "verified_date": "2026-08-24",
        "authority": verify_authority(),
        "media_and_rights": verify_media(),
        "translation": verify_translation(),
        "provenance": "OpenAI Codex gpt-5.6-sol, Ultra.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "unit": 14, "receipt": OUT.relative_to(ROOT).as_posix(), "bytes": OUT.stat().st_size, "sha256": digest(OUT)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
