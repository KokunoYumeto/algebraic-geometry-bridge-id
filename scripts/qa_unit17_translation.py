#!/usr/bin/env python3
"""Fail-closed authority, translation, mathematics, and rights QA for Unit 17."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "authority" / "wikiversity" / "unit-17"
SOURCE = ROOT / "source" / "id-ID"
OUT = ROOT / "qa" / "UNIT_17_TRANSLATION_QA.json"

MANIFEST_FACT = (116257, "c6747335c58fb3b4303cf3095705df7f991143f79d2d3598582a1cc8c99bef1a")
MAP_FACT = (13819, "f329f9d1a6fc2e862009acd4761ed8289da2cf4c8b42e057db275642c05a700e")
SOURCE_FACTS = {
    "source/id-ID/lecture-17.md": (15109, "53bdc1f91f02a4b28dcc0c78247ef2ab9f5102377d8d0b6eedc88ed6879f37e8"),
    "source/id-ID/worksheet-17.md": (15940, "2ec3c00332fad5683d56d9a608bf6544371732207312c4dc77c479621624efa0"),
    "source/id-ID/worksheet-17-solutions.md": (5104, "5a56a15a9cb38ef4859a53ccd690309965c22a1fef54b018f162ec12fac6adef"),
    "source/id-ID/media-credits-unit-17.md": (451, "2647366a9bad10aff220f263a3a9c14d3620c43b42c0b4d2195e0c38d263f537"),
}
CONTROL_FACTS = {
    "00_control/TERMINOLOGY.csv": (18332, "483df95662eb38ac8173d0718e7a56d3c8c28c44d8caf6a5ea730eb106091519"),
    "00_control/CORRECTIONS.csv": (32909, "f66dae4b899358de190cd495841ff156f20505897e949b063d61eeac708bd53b"),
}
MEDIA_FACTS = {
    "authority/RIGHTS-unit-17.csv": (443, "6b8de6f5a63f32d9f22e7fb69c98ba2d787121a2437a392602571504c2a1c544"),
    "authority/ASSET_CLOSURE-unit-17.json": (3013, "87c3d88789d822210b388e0c21e0e25a7418e77930e245ab2bc32916a0508d4f"),
    "authority/commons-imageinfo-unit-17.json": (7634, "e8531c2bebfb0dc0e761bfe2bd88d18a01ec73584024182a5fa3a59a2cf8b0fc"),
    "scripts/freeze_no_image_unit_rights.py": (5075, "389b22f640c52ee2bbbc1903efe2a5cf94ead08ead74721c855262a292e83a75"),
}
PDF_FACTS = {
    "authority/artifacts/lecture-17-official.pdf": (189434, "eaf34132d06a20fd4df1d445b067d43b6eba3286007ec0043b04a889c5450e70"),
    "authority/artifacts/worksheet-17-official.pdf": (171377, "3b103a04e2bacc5aa09c0a6982de22bd4bb420524babba3a55011bf1f4cad212"),
}
SOLUTION_NUMBERS = [3, 12, 31, 32]
SOLUTION_REVIDS = [1068109, 1090071, 1090074, 1090075]
CORRECTION_IDS = [f"AGC-CORR-{number:04d}" for number in range(40, 46)]


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
    check_fact("authority/wikiversity/unit-17/UNIT_AUTHORITY_MANIFEST.json", MANIFEST_FACT)
    check_fact("authority/wikiversity/unit-17/ORDERED_EXERCISE_MAP.json", MAP_FACT)
    manifest = json.loads((AUTH / "UNIT_AUTHORITY_MANIFEST.json").read_text(encoding="utf-8"))
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    require(manifest["schema"] == "brenner-unit-authority-freeze-v2", "authority schema")
    require(manifest["unit_number"] == 17, "authority unit")
    require(manifest["lecture"]["revid"] == 1112301, "lecture revision")
    require(manifest["lecture"]["mediawiki_sha1"] == "da4e92351c0197e66d117d85306d1578900dc81b", "lecture SHA-1")
    require(manifest["worksheet"]["revid"] == 1068111, "worksheet revision")
    require(manifest["worksheet"]["mediawiki_sha1"] == "1d9cda72f556181cf9d9e50c3784c41ddaa96888", "worksheet SHA-1")
    require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 116, "lecture closure count")
    require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 133, "worksheet closure count")
    require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "lecture missing transclusion")
    require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "worksheet missing transclusion")
    require(len(manifest["files"]) == 38, "authority file count")
    for row in manifest["files"]:
        path = AUTH / row["file"]
        require(path.is_file() and not path.is_symlink(), f"missing authority file: {row['file']}")
        require(path.stat().st_size == row["bytes"], f"authority bytes: {row['file']}")
        require(digest(path) == row["sha256"], f"authority hash: {row['file']}")
    require(mapping["unit"] == 17, "exercise map unit")
    require(mapping["exercise_count"] == 39, "exercise count")
    require(mapping["solution_count"] == 4, "solution count")
    require([row["exercise_number"] for row in mapping["entries"]] == list(range(1, 40)), "exercise order")
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
        "lecture_revid": 1112301,
        "worksheet_revid": 1068111,
        "lecture_transclusions": 116,
        "worksheet_transclusions": 133,
        "exercises": 39,
        "public_solutions": 4,
        "solution_numbers": SOLUTION_NUMBERS,
        "authority_files_verified": 38,
    }


def verify_media() -> dict[str, Any]:
    facts = [check_fact(relative, fact) for relative, fact in MEDIA_FACTS.items()]
    rights_path = ROOT / "authority" / "RIGHTS-unit-17.csv"
    with rights_path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(rows == [], "Unit 17 rights ledger must contain no reader-media row")
    closure = json.loads((ROOT / "authority" / "ASSET_CLOSURE-unit-17.json").read_text(encoding="utf-8"))
    require(closure["unit"] == 17, "media closure unit")
    require(closure["reader_media_positions"] == 0, "media positions")
    require(closure["unique_local_assets"] == 0, "binary media surfaces")
    require(closure["assets"] == [], "asset closure")
    require(closure["rights_sha256"] == MEDIA_FACTS["authority/RIGHTS-unit-17.csv"][1], "rights binding")
    require(len(closure["official_pdf_component_rights"]) == 2, "PDF component-rights closure")
    require(
        [row["license_short"] for row in closure["official_pdf_component_rights"]]
        == ["CC BY-SA 4.0", "CC BY-SA 4.0"],
        "official PDF component licences",
    )
    return {"media_positions": 0, "binary_surfaces": 0, "rights_rows": 0, "facts": facts}


def verify_translation() -> dict[str, Any]:
    facts = [check_fact(relative, fact) for relative, fact in SOURCE_FACTS.items()]
    facts.extend(check_fact(relative, fact) for relative, fact in CONTROL_FACTS.items())
    lecture = (SOURCE / "lecture-17.md").read_text(encoding="utf-8")
    worksheet = (SOURCE / "worksheet-17.md").read_text(encoding="utf-8")
    solutions = (SOURCE / "worksheet-17-solutions.md").read_text(encoding="utf-8")
    credits = (SOURCE / "media-credits-unit-17.md").read_text(encoding="utf-8")
    all_text = "\n".join((lecture, worksheet, solutions, credits))
    for name, raw in (("lecture", lecture), ("worksheet", worksheet), ("solutions", solutions)):
        require("translation_status: complete" in raw, f"{name} completion flag")
    require("OpenAI Codex\ngpt-5.6-sol, Ultra." in lecture, "exact model provenance")
    require(all(token not in all_text.casefold() for token in ("todo", "fixme", "tbd", "placeholder")), "placeholder residue")
    require(not re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|access[_-]?token|bearer\s+[A-Za-z0-9._-]{20,}", all_text, flags=re.I), "secret-like content")
    require("\u200b" not in all_text and "\ufeff" not in all_text, "invisible Unicode residue")
    prose = strip_nonprose(all_text)
    residue = re.findall(
        r"\b(?:Es sei|Zeige|Nachdem|Aufgabe|Beweis|Monoidring|Differenzengruppe|Kürzungsregel|wobei|Dann gibt es)\b",
        prose,
        flags=re.I,
    )
    require(not residue, f"visible German residue: {residue}")
    for rejected in ("cincin monoid", "group ring", "difference group", "hukum pencoretan"):
        require(
            not re.search(rf"(?<![A-Za-z]){re.escape(rejected)}(?![A-Za-z])", prose, flags=re.I),
            f"nonpreferred term: {rejected}",
        )
    for term in (
        "gelanggang monoid",
        "homomorfisme monoid",
        "gelanggang Laurent",
        "titik bernilai",
        "grup selisih",
        "hukum pembatalan",
        "grup satuan",
        "stabil terhadap pembagi",
        "representasi",
    ):
        require(term in prose, f"required terminology absent: {term}")

    headers = re.findall(r"^### Soal 17\.(\d+)(?:[^\n]*)\{#br-ak-2025-2026-w17-ex-(\d{2})\}$", worksheet, flags=re.M)
    require(headers == [(str(i), f"{i:02d}") for i in range(1, 40)], "exercise headers/IDs")
    starred = [int(value) for value in re.findall(r"^### Soal 17\.(\d+) ★", worksheet, flags=re.M)]
    require(starred == SOLUTION_NUMBERS, "starred solution topology")
    point_rows = re.findall(r"^### Soal 17\.(\d+) \((\d+) poin\)", worksheet, flags=re.M)
    require(point_rows == [("33", "6"), ("34", "4"), ("35", "4"), ("36", "4"), ("37", "4"), ("38", "3"), ("39", "4")], "submitted problem points")
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    entity_comments = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    require(entity_comments == [row["exercise_title"] for row in mapping["entries"]], "exercise entity mapping")
    solution_headers = [int(value) for value in re.findall(r"^## Solusi Soal 17\.(\d+) ", solutions, flags=re.M)]
    require(solution_headers == SOLUTION_NUMBERS, "solution headers")
    solution_comments = re.findall(r"<!-- upstream_solution: .*?; pageid=\d+; revid=(\d+) -->", solutions)
    require([int(value) for value in solution_comments] == SOLUTION_REVIDS, "solution comments/revisions")
    back_links = [int(value) for value in re.findall(r"\[Kembali ke Soal 17\.(\d+)\]\(#br-ak-2025-2026-w17-ex-\d{2}\)", solutions)]
    require(back_links == SOLUTION_NUMBERS, "solution back links")
    stable_ids = re.findall(r"\{#(br-ak-2025-2026-[^}]+)\}", "\n".join((lecture, worksheet, solutions)))
    require(len(stable_ids) == len(set(stable_ids)), "duplicate Unit 17 stable IDs")
    require(len(stable_ids) == 71, f"unexpected stable-ID count: {len(stable_ids)}")
    require(lecture.count("<!-- upstream_entity:") == 15, "lecture semantic entity count")
    require(worksheet.count("<!-- upstream_entity:") == 39, "worksheet semantic entity count")
    require(solutions.count("<!-- upstream_solution:") == 4, "solution provenance count")
    require(all(raw.count("![") == 0 for raw in (lecture, worksheet, solutions, credits)), "unexpected reader image")

    normalized = normalized_math("\n".join((lecture, worksheet, solutions)))
    protected = [
        r"R[M]=\bigoplus_{m\inM}Re_m",
        r"e_m\cdote_k:=e_{m+k}",
        r"X^mX^k=X^{m+k}",
        r"R[\mathbbN]=R[X]",
        r"R[X_1,\ldots,X_n]_{X_1\cdotsX_n}",
        r"\widetilde\varphi(X^m)=\varphi(m)",
        r"\widetilde\varphi:R[M]&\longrightarrowR[N]",
        r"\operatorname{Mor}_{\mathrm{mon}}(M,K)",
        r"a_1^{n_1}\cdotsa_r^{n_r}=a_1^{m_1}\cdotsa_r^{m_r}",
        r"\Gamma(M)=\{m-n\midm,n\inM\}",
        r"u+m_1+n_2=u+m_2+n_1",
        r"m+n=m+k",
        r"K[M]\congK[X,Y,U,V]/(UX-VY)",
        r"R[I]=\bigoplus_{m\inI}RT^m\subseteqR[M]",
        r"R[M_f]\congR[M]_{T^f}",
        r"e+f=5g",
        r"F=P(X^{1/b})",
        r"\varphi\circ\rho(g)=\rho(g)\circ\varphi",
        r"q_1+r_1=q_n+r_m=1",
        r"q_1+r_1=q_n+r_m=0",
    ]
    missing = [token for token in protected if token not in normalized]
    require(not missing, f"protected mathematics absent: {missing}")
    require("setidaknya satu $n$ dengan $m+n=0$" in solutions, "Solution 17.12 corrected proof disclosure")
    require("$a_{q_n}b_{r_n}$" in solutions, "Solution 17.31 source-index disclosure")
    require("$\\rho\\circ\\varphi$" in worksheet, "Exercise 17.39 source-form disclosure")

    ast_receipts: dict[str, Any] = {}
    expected_headers = {
        "lecture-17.md": 24,
        "worksheet-17.md": 42,
        "worksheet-17-solutions.md": 5,
        "media-credits-unit-17.md": 1,
    }
    for name in expected_headers:
        ast = pandoc_ast(SOURCE / name)
        nodes = list(walk(ast.get("blocks", [])))
        ast_headers = [node for node in nodes if node.get("t") == "Header"]
        maths = [node for node in nodes if node.get("t") == "Math"]
        images = [node for node in nodes if node.get("t") == "Image"]
        header_ids = [node["c"][1][0] for node in ast_headers]
        require(all(header_ids), f"header without ID: {name}")
        require(len(header_ids) == len(set(header_ids)), f"duplicate AST header ID: {name}")
        require(len(ast_headers) == expected_headers[name], f"AST header count: {name}")
        require(not images, f"unexpected AST image: {name}")
        ast_receipts[name] = {
            "headers": len(ast_headers),
            "math_nodes": len(maths),
            "images": len(images),
            "stable_header_ids": len(header_ids),
            "pandoc_warnings": 0,
        }

    with (ROOT / "00_control" / "TERMINOLOGY.csv").open(encoding="utf-8", newline="") as stream:
        terms = {row["source_term"]: row for row in csv.DictReader(stream)}
    expected_terms = {
        "Monoid": "monoid",
        "Monoidring": "gelanggang monoid",
        "Monoidhomomorphismus": "homomorfisme monoid",
        "Grundring": "gelanggang dasar",
        "Laurent-Ring": "gelanggang Laurent",
        "R-wertiger Punkt": "titik bernilai R",
        "Differenzengruppe": "grup selisih",
        "Kürzungsregel": "hukum pembatalan",
        "Einheitengruppe": "grup satuan",
        "teilerstabil": "stabil terhadap pembagi",
        "Darstellung einer Gruppe": "representasi grup",
    }
    for source_term, target_term in expected_terms.items():
        require(terms[source_term]["preferred_target"] == target_term, f"terminology target: {source_term}")
        require(terms[source_term]["status"] == "admitted", f"terminology status: {source_term}")
    with (ROOT / "00_control" / "CORRECTIONS.csv").open(encoding="utf-8", newline="") as stream:
        corrections = {row["correction_id"]: row for row in csv.DictReader(stream)}
    for correction_id in CORRECTION_IDS:
        require(correction_id in corrections, f"missing correction binding: {correction_id}")
        require(corrections[correction_id]["status"] == "applied_at_unit_17_translation", f"correction status: {correction_id}")
    require(all(correction_id not in all_text for correction_id in CORRECTION_IDS), "ledger IDs must not replace reader disclosures")
    return {
        "source_and_control_facts": facts,
        "stable_ids": len(stable_ids),
        "exercises": 39,
        "public_solutions": 4,
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
        "unit": 17,
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
                "unit": 17,
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
