#!/usr/bin/env python3
"""Fail-closed authority, translation, mathematics, and rights QA for Unit 18."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "authority" / "wikiversity" / "unit-18"
SOURCE = ROOT / "source" / "id-ID"
OUT = ROOT / "qa" / "UNIT_18_TRANSLATION_QA.json"

MANIFEST_FACT = (106298, "26a56a0ccad60414bf09320dc008d438ccf84b3dd11c12c31e80fa6088437033")
MAP_FACT = (11943, "8b55ef14cccbcab93ba99882d16e0f9888780353f7290eff8e1d2d6cd6bc4cd9")
SOURCE_FACTS = {
    "source/id-ID/lecture-18.md": (14716, "319cca4f08a3a4ee0bf0fa2a9d525e0adcd2f6f639705dd1c2eb06580b7bfcd3"),
    "source/id-ID/worksheet-18.md": (14530, "ec760a90d6f7462dbe71f755149886006e144bedc8ce11d09f72452472ee641e"),
    "source/id-ID/worksheet-18-solutions.md": (9027, "10fcda87b4613fdf6bd037b8428ee46b82ffbfa73c182dbb3732602d0f683db4"),
    "source/id-ID/media-credits-unit-18.md": (789, "9e1f8c342873acbe70a43ab88718bba67cbe4ed10672afb77f2ed5c41a78f0c5"),
}
CONTROL_FACTS = {
    "00_control/TERMINOLOGY.csv": (19481, "60b5f85b616205aa2ed3f8e0a1c2bc532ba45f825acb0b88d3bd77c85703f8c3"),
    "00_control/CORRECTIONS.csv": (35273, "976eac154c13183c6909be9061b7093780598ef0b44795fd1569e21b7e1f131a"),
}
MEDIA_FACTS = {
    "authority/RIGHTS-unit-18.csv": (1998, "8cbf29b0063c2463fe89f9dec67bda671f9ee366db2c91176e37d4ef3532fbb0"),
    "authority/ASSET_CLOSURE-unit-18.json": (4025, "69bfe604847dbb57fa21e07f8308901f02b87fba92c668b2b0fec27e3c2e8ad3"),
    "authority/commons-imageinfo-unit-18.json": (15755, "a2eaa60a79d0b07f0f820545896113987f1d53c66e9a4edff770da1fcaea67c0"),
    "authority/assets/Cusp-500.png": (31209, "fe619908aa78afea1928dcc3dc7932b34d86134516d57a190bf0095ca3403b65"),
}
PDF_FACTS = {
    "authority/artifacts/lecture-18-official.pdf": (195384, "898bbdac03b255ffa3defcd3a1215c0491e63ef8dad217ed99b7a9b36d18329e"),
    "authority/artifacts/worksheet-18-official.pdf": (135343, "e38c639f5f3df0b422f2fa1695a62bc8678ae556f6f595ee0a2c75d9f26f05f2"),
}
SOLUTION_NUMBERS = [3, 4, 10, 11, 15]
SOLUTION_REVIDS = [959312, 959372, 1112399, 1111901, 1090073]
CORRECTION_IDS = [f"AGC-CORR-{number:04d}" for number in range(46, 51)]


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
    check_fact("authority/wikiversity/unit-18/UNIT_AUTHORITY_MANIFEST.json", MANIFEST_FACT)
    check_fact("authority/wikiversity/unit-18/ORDERED_EXERCISE_MAP.json", MAP_FACT)
    manifest = json.loads((AUTH / "UNIT_AUTHORITY_MANIFEST.json").read_text(encoding="utf-8"))
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    require(manifest["schema"] == "brenner-unit-authority-freeze-v2", "authority schema")
    require(manifest["unit_number"] == 18, "authority unit")
    require(manifest["lecture"]["revid"] == 1051383, "lecture revision")
    require(manifest["lecture"]["mediawiki_sha1"] == "a30ad183e1e879bf7fec6ce414cbfad149b89bb1", "lecture SHA-1")
    require(manifest["worksheet"]["revid"] == 1062146, "worksheet revision")
    require(manifest["worksheet"]["mediawiki_sha1"] == "283fabbf95717c759b92d7845d97cbf77c0dcbd9", "worksheet SHA-1")
    require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 97, "lecture closure count")
    require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 130, "worksheet closure count")
    require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "lecture missing transclusion")
    require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "worksheet missing transclusion")
    require(len(manifest["files"]) == 39, "authority file count")
    for row in manifest["files"]:
        path = AUTH / row["file"]
        require(path.is_file() and not path.is_symlink(), f"missing authority file: {row['file']}")
        require(path.stat().st_size == row["bytes"], f"authority bytes: {row['file']}")
        require(digest(path) == row["sha256"], f"authority hash: {row['file']}")
    require(mapping["unit"] == 18, "exercise map unit")
    require(mapping["exercise_count"] == 28, "exercise count")
    require(mapping["solution_count"] == 5, "solution count")
    require([row["exercise_number"] for row in mapping["entries"]] == list(range(1, 29)), "exercise order")
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
        "lecture_revid": 1051383,
        "worksheet_revid": 1062146,
        "lecture_transclusions": 97,
        "worksheet_transclusions": 130,
        "exercises": 28,
        "public_solutions": 5,
        "solution_numbers": SOLUTION_NUMBERS,
        "authority_files_verified": 39,
    }


def verify_media() -> dict[str, Any]:
    facts = [check_fact(relative, fact) for relative, fact in MEDIA_FACTS.items()]
    with (ROOT / "authority" / "RIGHTS-unit-18.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 1, "Unit 18 rights row count")
    row = rows[0]
    require(row["asset_id"] == "br-ak-u18-media-001", "asset ID")
    require(row["local_path"] == "authority/assets/Cusp-500.png", "asset path")
    require(row["local_bytes"] == "31209" and row["local_sha256"] == MEDIA_FACTS["authority/assets/Cusp-500.png"][1], "asset identity binding")
    require(row["license_short"] == "CC BY-SA 3.0", "asset licence")
    require(row["source_course_inline_license_label"] == "PD", "source inline rights label")
    require("discrepancy" not in row["license_discrepancy_note"].casefold(), "rights note must state facts rather than placeholder")
    closure = json.loads((ROOT / "authority" / "ASSET_CLOSURE-unit-18.json").read_text(encoding="utf-8"))
    require(closure["unit"] == 18, "media closure unit")
    require(closure["reader_media_positions"] == 1, "media positions")
    require(closure["unique_local_assets"] == 1, "binary media surfaces")
    require(closure["rights_sha256"] == MEDIA_FACTS["authority/RIGHTS-unit-18.csv"][1], "rights binding")
    require(closure["source_inline_license_discrepancy"]["reuse_option_bound"] == "CC BY-SA 3.0", "conservative media licence binding")
    require(len(closure["official_pdf_component_rights"]) == 2, "PDF component-rights closure")
    require([item["license_short"] for item in closure["official_pdf_component_rights"]] == ["CC BY-SA 4.0", "CC BY-SA 4.0"], "official PDF component licences")
    require(closure["assets"][0]["local_sha256"] == MEDIA_FACTS["authority/assets/Cusp-500.png"][1], "closure asset hash")
    return {"media_positions": 1, "binary_surfaces": 1, "rights_rows": 1, "facts": facts}


def verify_translation() -> dict[str, Any]:
    facts = [check_fact(relative, fact) for relative, fact in SOURCE_FACTS.items()]
    facts.extend(check_fact(relative, fact) for relative, fact in CONTROL_FACTS.items())
    lecture = (SOURCE / "lecture-18.md").read_text(encoding="utf-8")
    worksheet = (SOURCE / "worksheet-18.md").read_text(encoding="utf-8")
    solutions = (SOURCE / "worksheet-18-solutions.md").read_text(encoding="utf-8")
    credits = (SOURCE / "media-credits-unit-18.md").read_text(encoding="utf-8")
    all_text = "\n".join((lecture, worksheet, solutions, credits))
    for name, raw in (("lecture", lecture), ("worksheet", worksheet), ("solutions", solutions)):
        require("translation_status: complete" in raw, f"{name} completion flag")
    require("OpenAI Codex\ngpt-5.6-sol, Ultra." in lecture, "exact model provenance")
    require(all(token not in all_text.casefold() for token in ("todo", "fixme", "tbd", "placeholder")), "placeholder residue")
    require(not re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|access[_-]?token|bearer\s+[A-Za-z0-9._-]{20,}", all_text, flags=re.I), "secret-like content")
    require("\u200b" not in all_text and "\ufeff" not in all_text, "invisible Unicode residue")
    prose = strip_nonprose(all_text)
    residue = re.findall(r"\b(?:Es sei|Zeige|Aufgabe|Beweis|Führungszahl|Einbettungsdimension|Multiplizität|Singularitätsgrad|Neilsche|Geldfälscher|teilerfremd)\b", prose, flags=re.I)
    require(not residue, f"visible German residue: {residue}")
    for rejected in ("monoid numeris", "bilangan penghantar", "dimensi embedding", "multiplikitas", "tingkat singularitas"):
        require(not re.search(rf"(?<![A-Za-z]){re.escape(rejected)}(?![A-Za-z])", prose, flags=re.I), f"nonpreferred term: {rejected}")
    for term in ("kurva monomial", "monoid numerik", "bilangan konduktor", "dimensi penyematan", "multiplisitas", "derajat singularitas", "saling prima", "grup selisih"):
        require(term in prose, f"required terminology absent: {term}")

    headers = re.findall(r"^### Soal 18\.(\d+)(?:[^\n]*)\{#br-ak-2025-2026-w18-ex-(\d{2})\}$", worksheet, flags=re.M)
    require(headers == [(str(i), f"{i:02d}") for i in range(1, 29)], "exercise headers/IDs")
    starred = [int(value) for value in re.findall(r"^### Soal 18\.(\d+) ★", worksheet, flags=re.M)]
    require(starred == SOLUTION_NUMBERS, "starred solution topology")
    point_rows = re.findall(r"^### Soal 18\.(\d+) \(([^)]*poin[^)]*)\)", worksheet, flags=re.M)
    require(point_rows == [("21", "6 poin"), ("22", "3 poin"), ("23", "4 poin"), ("24", "8 poin: 1+3+1+2+1"), ("25", "3 poin"), ("26", "4 poin"), ("27", "3 poin"), ("28", "3 poin")], "submitted problem points")
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    entity_comments = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    require(entity_comments == [row["exercise_title"] for row in mapping["entries"]], "exercise entity mapping")
    solution_headers = [int(value) for value in re.findall(r"^## Solusi Soal 18\.(\d+) ", solutions, flags=re.M)]
    require(solution_headers == SOLUTION_NUMBERS, "solution headers")
    solution_comments = re.findall(r"<!-- upstream_solution: .*?; pageid=\d+; revid=(\d+) -->", solutions)
    require([int(value) for value in solution_comments] == SOLUTION_REVIDS, "solution comments/revisions")
    back_links = [int(value) for value in re.findall(r"\[Kembali ke Soal 18\.(\d+)\]\(#br-ak-2025-2026-w18-ex-\d{2}\)", solutions)]
    require(back_links == SOLUTION_NUMBERS, "solution back links")
    stable_ids = re.findall(r"\{#(br-ak-2025-2026-[^}]+)\}", "\n".join((lecture, worksheet, solutions)))
    require(len(stable_ids) == len(set(stable_ids)), "duplicate Unit 18 stable IDs")
    require(len(stable_ids) == 58, f"unexpected stable-ID count: {len(stable_ids)}")
    require(lecture.count("<!-- upstream_entity:") == 13, "lecture semantic entity count")
    require(worksheet.count("<!-- upstream_entity:") == 28, "worksheet semantic entity count")
    require(solutions.count("<!-- upstream_solution:") == 5, "solution provenance count")
    require(lecture.count("![") == 1 and worksheet.count("![") == 0 and solutions.count("![") == 0, "reader image topology")
    require("![Kurva berbentuk cusp dengan dua cabang halus yang bertemu runcing di titik asal](authority/assets/Cusp-500.png)" in lecture, "reader image path/alt")
    require("CC BY-SA 3.0" in lecture and "Georg-Johann" in lecture, "reader media attribution")

    normalized = normalized_math("\n".join((lecture, worksheet, solutions)))
    protected = [
        r"t\longmapsto(t^{e_1},\ldots,t^{e_n})",
        r"s\longmapsto(s^{f_1},\ldots,s^{f_n})",
        r"\mathbbN^n\longrightarrowM\longrightarrow\mathbbN",
        r"K[\mathbbN^n]=K[X_1,\ldots,X_n]",
        r"C=V(Y^2-X^3)",
        r"\mathbbN_{\geqf}\subseteqM",
        r"M_+\setminus(M_++M_+)",
        r"x=x_1+x_2",
        r"\varphi:M\longrightarrowK",
        r"m_1e_1+\cdots+m_ne_n=1",
        r"a=a_1^{m_1}\cdotsa_n^{m_n}",
        r"R=\mathbbC[X,Y]/(Y^2-X^3)",
        r"\psi:\operatorname{Mor}_{\mathrm{mon}}(\mathbbN,R)",
        r"K[M\timesM]\congK[M]\otimesK[M]",
        r"F(x,y)=(x^ay^b,x^cy^d)",
        r"nM_+=\left\{m\inM\mathrel{\Big|}",
        r"\varphi(f)=c(T-1)^n",
        r"\pi(1)=\rho(3)\rho(2)^{-1}",
        r"6+8+1=15",
        r"\mathbbN\subset\mathbbZ",
    ]
    missing = [token for token in protected if token not in normalized]
    require(not missing, f"protected mathematics absent: {missing}")
    require("sumber mencetak koordinat citranya" in lecture, "scalar-factorization correction disclosure")
    require("sumber mencetak koordinat sebagai" in lecture, "monomial-coordinate correction disclosure")
    require("sumber menyebut sifat universal gelanggang" in lecture, "difference-group correction disclosure")
    require("sumber mencetak $x_1,x_2\\in M_++M_+$" in lecture, "sumset-membership correction disclosure")
    require("sumber menulis langsung" in solutions and "$\\varphi(f)=(T-1)^n$" in solutions, "solution scalar-factor correction disclosure")

    ast_receipts: dict[str, Any] = {}
    expected = {
        "lecture-18.md": (21, 1),
        "worksheet-18.md": (31, 0),
        "worksheet-18-solutions.md": (6, 0),
        "media-credits-unit-18.md": (1, 0),
    }
    for name, (header_count, image_count) in expected.items():
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
        ast_receipts[name] = {"headers": len(headers_ast), "math_nodes": len(maths), "images": len(images), "stable_header_ids": len(header_ids), "pandoc_warnings": 0}

    with (ROOT / "00_control" / "TERMINOLOGY.csv").open(encoding="utf-8", newline="") as stream:
        terms = {row["source_term"]: row for row in csv.DictReader(stream)}
    expected_terms = {
        "monomiale Kurve": "kurva monomial",
        "numerisches Monoid": "monoid numerik",
        "Führungszahl": "bilangan konduktor",
        "Einbettungsdimension": "dimensi penyematan",
        "Multiplizität": "multiplisitas",
        "Singularitätsgrad": "derajat singularitas",
        "teilerfremd": "saling prima",
    }
    for source_term, target_term in expected_terms.items():
        require(terms[source_term]["preferred_target"] == target_term, f"terminology target: {source_term}")
        require(terms[source_term]["status"] == "admitted", f"terminology status: {source_term}")
    with (ROOT / "00_control" / "CORRECTIONS.csv").open(encoding="utf-8", newline="") as stream:
        corrections = {row["correction_id"]: row for row in csv.DictReader(stream)}
    for correction_id in CORRECTION_IDS:
        require(correction_id in corrections, f"missing correction binding: {correction_id}")
        require(corrections[correction_id]["status"] == "applied_at_unit_18_translation", f"correction status: {correction_id}")
    require(all(correction_id not in all_text for correction_id in CORRECTION_IDS), "ledger IDs must not replace reader disclosures")
    return {
        "source_and_control_facts": facts,
        "stable_ids": len(stable_ids),
        "exercises": 28,
        "public_solutions": 5,
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
        "unit": 18,
        "verified_date": "2026-08-24",
        "authority": verify_authority(),
        "media_and_rights": verify_media(),
        "translation": verify_translation(),
        "provenance": "OpenAI Codex gpt-5.6-sol, Ultra.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "unit": 18, "receipt": OUT.relative_to(ROOT).as_posix(), "bytes": OUT.stat().st_size, "sha256": digest(OUT)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
