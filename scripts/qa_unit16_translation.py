#!/usr/bin/env python3
"""Fail-closed authority, translation, mathematics, media, and rights QA for Unit 16."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "authority" / "wikiversity" / "unit-16"
SOURCE = ROOT / "source" / "id-ID"
OUT = ROOT / "qa" / "UNIT_16_TRANSLATION_QA.json"

MANIFEST_FACT = (118777, "54c823b4aa99c6e37e1fd3f84754f290bb54500847800906569704c3b4d49da0")
MAP_FACT = (11533, "835029f5f5f46dea23486bd62edec6f4ab64667192c44504fee3af259e5b5266")
SOURCE_FACTS = {
    "source/id-ID/lecture-16.md": (16456, "c7cb0a1bc34e2003db18024d206c87d522a8df2082d186456d7a987cf0775d39"),
    "source/id-ID/worksheet-16.md": (11252, "871ea30f571ebc9e0e2a7b1e4d30cddfe719822f48b2bdbe97bd6d8a52a5268a"),
    "source/id-ID/worksheet-16-solutions.md": (9286, "5df1b9f46ba65622644feed0bf99191d5737d2edc2cc887c3b00efd2b50f8860"),
    "source/id-ID/media-credits-unit-16.md": (1316, "4a5bc83795b780ad26bffe425924bb010b966ed49dcbd0c3b073bc3be77f7a99"),
}
CONTROL_FACTS = {
    "00_control/TERMINOLOGY.csv": (16611, "5a7864ef341bf5fc5ea4d4f5342c44aa404aa959cd2831dd8ab0f9f6146b61ed"),
    "00_control/CORRECTIONS.csv": (29924, "7b2cf0d56f49a32d674b5c8ea66d1b5a2af8346729893891cfdee35ffc61e40c"),
}
MEDIA_FACTS = {
    "authority/RIGHTS-unit-16.csv": (5125, "f7472100f99256c04367f0c8f6f41fa7eef361fbb60044a13fcd0c8f76a019ea"),
    "authority/ASSET_CLOSURE-unit-16.json": (4952, "561184965af9c75ee6812a103a435af9cf74f1c1b60ac7007b851ce66b5df555"),
    "authority/commons-imageinfo-unit-16.json": (25535, "c965f9ac92a8e185959b69316b6d8d5ae2cbd57c5ff90805fc8a590c72e33c95"),
    "authority/assets/Kaffeefilter-500.jpg": (37416, "9f7a5b16d515fa46284ed1e9201060ba99b4882df5cf697ccecf66e58d94722c"),
    "authority/assets/Cone_intersects_line.png": (550044, "17096b23324c31443fde9e013d0746a9e96cf5a701f8e90cf119451411de0779"),
    "authority/assets/FiberBundle_2.png": (2936, "e51ef734bb86a889f81c6b56e8dc0c3f286ba55124d42a8f4a5e6640a9680909"),
    "authority/assets/Draft0-500.png": (16732, "0eeb76e7396cd19f049224fd45b27403c5ff2cea39c7c9993699b5174a50324b"),
    "scripts/freeze_unit16_media.py": (17548, "4ca5a97ed75c165c8af163a5715e5cb1b323c713c4e1e0f4b2b35ded462844ac"),
}
PDF_FACTS = {
    "authority/artifacts/lecture-16-official.pdf": (594980, "69c0610b63e083ef5c73b7d2e6f9524f07872b4f832872b242e583ff8941634f"),
    "authority/artifacts/worksheet-16-official.pdf": (150132, "aa65c948b67e3383b4341c30a67ae41d09d8798b751707365c38b385e6560e1c"),
}
SOLUTION_NUMBERS = [1, 10, 11, 12, 13, 15]
SOLUTION_REVIDS = [1068100, 1067953, 1094645, 1112750, 1089809, 1096228]
CORRECTION_IDS = [f"AGC-CORR-{number:04d}" for number in range(34, 40)]


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
    check_fact("authority/wikiversity/unit-16/UNIT_AUTHORITY_MANIFEST.json", MANIFEST_FACT)
    check_fact("authority/wikiversity/unit-16/ORDERED_EXERCISE_MAP.json", MAP_FACT)
    manifest = json.loads((AUTH / "UNIT_AUTHORITY_MANIFEST.json").read_text(encoding="utf-8"))
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    require(manifest["schema"] == "brenner-unit-authority-freeze-v2", "authority schema")
    require(manifest["unit_number"] == 16, "authority unit")
    require(manifest["lecture"]["revid"] == 1060232, "lecture revision")
    require(manifest["lecture"]["mediawiki_sha1"] == "59d50c0b858c5aa9b4a4be3b54c7336553e04482", "lecture SHA-1")
    require(manifest["worksheet"]["revid"] == 1067952, "worksheet revision")
    require(manifest["worksheet"]["mediawiki_sha1"] == "5aee338323cba27122a11b018b7ed938761b3d2f", "worksheet SHA-1")
    require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 127, "lecture closure count")
    require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 131, "worksheet closure count")
    require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "lecture missing transclusion")
    require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "worksheet missing transclusion")
    require(len(manifest["files"]) == 43, "authority file count")
    for row in manifest["files"]:
        path = AUTH / row["file"]
        require(path.is_file() and not path.is_symlink(), f"missing authority file: {row['file']}")
        require(path.stat().st_size == row["bytes"], f"authority bytes: {row['file']}")
        require(digest(path) == row["sha256"], f"authority hash: {row['file']}")
    require(mapping["unit"] == 16, "exercise map unit")
    require(mapping["exercise_count"] == 23, "exercise count")
    require(mapping["solution_count"] == 6, "solution count")
    require([row["exercise_number"] for row in mapping["entries"]] == list(range(1, 24)), "exercise order")
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
        "lecture_revid": 1060232,
        "worksheet_revid": 1067952,
        "lecture_transclusions": 127,
        "worksheet_transclusions": 131,
        "exercises": 23,
        "public_solutions": 6,
        "solution_numbers": SOLUTION_NUMBERS,
        "authority_files_verified": 43,
    }


def verify_media() -> dict[str, Any]:
    facts = [check_fact(relative, fact) for relative, fact in MEDIA_FACTS.items()]
    rights_path = ROOT / "authority" / "RIGHTS-unit-16.csv"
    with rights_path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 4, "rights row count")
    require([row["asset_id"] for row in rows] == [f"br-ak-u16-media-{i:03d}" for i in range(1, 5)], "asset IDs")
    require(
        [row["license_short"] for row in rows]
        == ["CC BY-SA 3.0", "Public domain", "CC BY-SA 3.0", "CC BY-SA 3.0"],
        "component licences",
    )
    for row in rows:
        asset = ROOT / row["local_path"]
        require(asset.is_file() and not asset.is_symlink(), f"missing media asset: {row['local_path']}")
        require(asset.stat().st_size == int(row["local_bytes"]), f"media bytes: {row['local_path']}")
        require(digest(asset) == row["local_sha256"], f"media hash: {row['local_path']}")
    require(rows[3]["thumbnail_dimension_discrepancy"] == "decoded=500x501;reported=500x500", "SVG thumbnail discrepancy record")
    closure = json.loads((ROOT / "authority" / "ASSET_CLOSURE-unit-16.json").read_text(encoding="utf-8"))
    require(closure["unit"] == 16, "media closure unit")
    require(closure["reader_media_positions"] == 4, "media positions")
    require(closure["unique_local_assets"] == 4, "binary media surfaces")
    require(closure["rights_sha256"] == MEDIA_FACTS["authority/RIGHTS-unit-16.csv"][1], "rights binding")
    require(closure["reader_credits_sha256"] == SOURCE_FACTS["source/id-ID/media-credits-unit-16.md"][1], "credits binding")
    require(len(closure["official_pdf_component_rights"]) == 2, "PDF component-rights closure")
    return {"media_positions": 4, "binary_surfaces": 4, "rights_rows": 4, "facts": facts}


def verify_translation() -> dict[str, Any]:
    facts = [check_fact(relative, fact) for relative, fact in SOURCE_FACTS.items()]
    facts.extend(check_fact(relative, fact) for relative, fact in CONTROL_FACTS.items())
    lecture = (SOURCE / "lecture-16.md").read_text(encoding="utf-8")
    worksheet = (SOURCE / "worksheet-16.md").read_text(encoding="utf-8")
    solutions = (SOURCE / "worksheet-16-solutions.md").read_text(encoding="utf-8")
    credits = (SOURCE / "media-credits-unit-16.md").read_text(encoding="utf-8")
    all_text = "\n".join((lecture, worksheet, solutions, credits))
    for name, raw in (("lecture", lecture), ("worksheet", worksheet), ("solutions", solutions)):
        require("translation_status: complete" in raw, f"{name} completion flag")
    require("OpenAI Codex\ngpt-5.6-sol, Ultra." in lecture, "exact model provenance")
    require(all(token not in all_text.casefold() for token in ("todo", "fixme", "tbd", "placeholder")), "placeholder residue")
    require(not re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|access[_-]?token|bearer\s+[A-Za-z0-9._-]{20,}", all_text, flags=re.I), "secret-like content")
    prose = strip_nonprose(all_text)
    residue = re.findall(
        r"\b(?:Es sei|Zeige|Dann|Aufgabe|Beweis|irreduzibler Filter|Morphismen|Faser|Erzwingende Algebra|Quotientenkörpern)\b",
        prose,
        flags=re.I,
    )
    require(not residue, f"visible German residue: {residue}")
    for rejected in ("morfisma", "fiber", "filter ireduksibel", "aljabar pemaksaan"):
        require(
            not re.search(rf"(?<![A-Za-z]){re.escape(rejected)}(?![A-Za-z])", prose, flags=re.I),
            f"nonpreferred term: {rejected}",
        )
    for term in (
        "filter tak tereduksi",
        "filter generik",
        "tangkai generik",
        "morfisme",
        "varietas kuasiafin",
        "serat",
        "aljabar pemaksa",
    ):
        require(term in prose.casefold(), f"required terminology absent: {term}")

    headers = re.findall(r"^### Soal 16\.(\d+)(?:[^\n]*)\{#br-ak-2025-2026-w16-ex-(\d{2})\}$", worksheet, flags=re.M)
    require(headers == [(str(i), f"{i:02d}") for i in range(1, 24)], "exercise headers/IDs")
    starred = [int(value) for value in re.findall(r"^### Soal 16\.(\d+) ★", worksheet, flags=re.M)]
    require(starred == SOLUTION_NUMBERS, "starred solution topology")
    point_rows = re.findall(r"^### Soal 16\.(\d+) \((\d+) poin\)", worksheet, flags=re.M)
    require(point_rows == [("19", "4"), ("20", "4"), ("21", "5"), ("22", "6"), ("23", "3")], "submitted problem points")
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    entity_comments = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    require(entity_comments == [row["exercise_title"] for row in mapping["entries"]], "exercise entity mapping")
    solution_headers = [int(value) for value in re.findall(r"^## Solusi Soal 16\.(\d+) ", solutions, flags=re.M)]
    require(solution_headers == SOLUTION_NUMBERS, "solution headers")
    solution_comments = re.findall(r"<!-- upstream_solution: .*?; pageid=\d+; revid=(\d+) -->", solutions)
    require([int(value) for value in solution_comments] == SOLUTION_REVIDS, "solution comments/revisions")
    back_links = [int(value) for value in re.findall(r"\[Kembali ke Soal 16\.(\d+)\]\(#br-ak-2025-2026-w16-ex-\d{2}\)", solutions)]
    require(back_links == SOLUTION_NUMBERS, "solution back links")
    stable_ids = re.findall(r"\{#(br-ak-2025-2026-[^}]+)\}", "\n".join((lecture, worksheet, solutions)))
    require(len(stable_ids) == len(set(stable_ids)), "duplicate Unit 16 stable IDs")
    require(len(stable_ids) == 53, f"unexpected stable-ID count: {len(stable_ids)}")
    require(lecture.count("<!-- upstream_entity:") == 12, "lecture semantic entity count")
    require(worksheet.count("<!-- upstream_entity:") == 23, "worksheet semantic entity count")
    require(solutions.count("<!-- upstream_solution:") == 6, "solution provenance count")
    require(lecture.count("![") == 3 and solutions.count("![") == 1, "reader image positions")
    for asset in ("Kaffeefilter-500.jpg", "Cone_intersects_line.png", "FiberBundle_2.png"):
        require(f"authority/assets/{asset}" in lecture, f"lecture media reference: {asset}")
    require("authority/assets/Draft0-500.png" in solutions, "solution media reference")

    normalized = normalized_math("\n".join((lecture, worksheet, solutions)))
    protected = [
        r"S=\{f\inR\midD(f)\inF\}",
        r"D(g)\cupD(h)=D(g,h)\supseteqD(g+h)",
        r"\widetilde\psi:\Gamma(U,\mathcalO)\longrightarrow\Gamma(\psi^{-1}(U),\mathcalO)",
        r"f\circ\varphi^*=\frac{\varphi(G)}{\varphi(H)}",
        r"\operatorname{Mor}(U,\mathbbA_K^1)&\longrightarrow\Gamma(U,\mathcalO)",
        r"S=K[T_1,\ldots,T_n]/\mathfraka",
        r"V=V(X^2+Y^2-Z^2)\subseteq\mathbbA_K^3",
        r"\frac{X}{Z-Y}=\frac{Z+Y}{X}",
        r"A=R[T_1,\ldots,T_n]/(f_1T_1+\cdots+f_nT_n+f)",
        r"f^{-1}(0)=V(h_1g_1,\ldots,h_ng_n)\capU",
        r"(ax-by)^2+(bx+ay)^2",
        r"V(XY,XZ,YZ)=V(X,Y)\cupV(X,Z)\cupV(Y,Z)",
        r"(B-Z)Z=-\frac{2AB^2(A-B)}{(A+B)^2}",
    ]
    missing = [token for token in protected if token not in normalized]
    require(not missing, f"protected mathematics absent: {missing}")
    require("Batas solusi sumber" in solutions, "Solution 16.13 source-scope disclosure")
    require("$q=g_i/h_i$" in worksheet, "Exercise 16.23 source-variable disclosure")

    ast_receipts: dict[str, Any] = {}
    for name in ("lecture-16.md", "worksheet-16.md", "worksheet-16-solutions.md", "media-credits-unit-16.md"):
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
    require(ast_receipts["lecture-16.md"]["headers"] == 20, "lecture AST header count")
    require(ast_receipts["worksheet-16.md"]["headers"] == 26, "worksheet AST header count")
    require(ast_receipts["worksheet-16-solutions.md"]["headers"] == 7, "solution AST header count")
    require(ast_receipts["media-credits-unit-16.md"]["headers"] == 1, "credits AST header count")

    with (ROOT / "00_control" / "TERMINOLOGY.csv").open(encoding="utf-8", newline="") as stream:
        terms = {row["source_term"]: row for row in csv.DictReader(stream)}
    expected_terms = {
        "irreduzibler Filter": "filter tak tereduksi",
        "generischer Filter": "filter generik",
        "generischer Halm": "tangkai generik",
        "Morphismus": "morfisme",
        "Faser": "serat",
        "erzwingende Algebra": "aljabar pemaksa",
    }
    for source_term, target_term in expected_terms.items():
        require(terms[source_term]["preferred_target"] == target_term, f"terminology target: {source_term}")
        require(terms[source_term]["status"] == "admitted", f"terminology status: {source_term}")
    with (ROOT / "00_control" / "CORRECTIONS.csv").open(encoding="utf-8", newline="") as stream:
        corrections = {row["correction_id"]: row for row in csv.DictReader(stream)}
    for correction_id in CORRECTION_IDS:
        require(correction_id in corrections, f"missing correction binding: {correction_id}")
        require(corrections[correction_id]["status"] == "applied_at_unit_16_translation", f"correction status: {correction_id}")
    require(all(correction_id not in all_text for correction_id in CORRECTION_IDS), "ledger IDs must not replace reader disclosures")
    return {
        "source_and_control_facts": facts,
        "stable_ids": len(stable_ids),
        "exercises": 23,
        "public_solutions": 6,
        "ast": ast_receipts,
        "visible_german_residue": 0,
        "placeholder_count": 0,
        "secret_like_count": 0,
        "protected_math_checks": len(protected),
        "correction_bindings": CORRECTION_IDS,
    }


def main() -> int:
    receipt = {
        "schema": "ag-bridge-unit-translation-qa-v1",
        "status": "PASS",
        "unit": 16,
        "verified_date": "2026-08-24",
        "authority": verify_authority(),
        "media_and_rights": verify_media(),
        "translation": verify_translation(),
        "provenance": "OpenAI Codex gpt-5.6-sol, Ultra.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "status": "PASS",
                "unit": 16,
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
