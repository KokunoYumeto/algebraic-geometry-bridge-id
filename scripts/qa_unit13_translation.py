#!/usr/bin/env python3
"""Fail-closed authority, translation, mathematics, media, and rights QA for Unit 13."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "authority" / "wikiversity" / "unit-13"
SOURCE = ROOT / "source" / "id-ID"
QA = ROOT / "qa"
OUT = QA / "UNIT_13_TRANSLATION_QA.json"

MANIFEST_FACT = (149341, "dc86b4d124c7e775fb635a1f9672a8b8faadc4ff2259b0779f7bac6302d18848")
MAP_FACT = (20313, "f954f09c996c8aa22f94ec826a1503b135a7b4fb9f9e0d5d6ff21f36a519e52a")
SOURCE_FACTS = {
    "source/id-ID/lecture-13.md": (14295, "6b2c8a6aac3c80a3bf45cdb83db085e59f72f09bb7829528f2719c6b7af178fa"),
    "source/id-ID/worksheet-13.md": (16401, "b9dbf3ee514c8e7d59bdf60ba4617cb0b8a38b5e299cc65af53cdd8e7f56adcd"),
    "source/id-ID/worksheet-13-solutions.md": (15292, "787b24f616ac7823c88b7f45ea827df5bbdea34be111bb36822d542121e89774"),
    "source/id-ID/media-credits-unit-13.md": (742, "f5aa7d11bb7fd29860bdaec51fdb03790fdd6361e6f0ef2b4fbac72040de1341"),
}
CONTROL_FACTS = {
    "00_control/TERMINOLOGY.csv": (11768, "7d3711bc1890ec3451aa2e8cb51752cfc7a04526841966458fee85af6546177f"),
    "00_control/CORRECTIONS.csv": (25527, "9fcff85e47c97bf98fd49b6be6a14946250a2a2aa671c20e7184662931052d6f"),
}
MEDIA_FACTS = {
    "authority/RIGHTS-unit-13.csv": (3677, "cdf370a6e3d7b80e137e6eb98a1180519b0cb97865ee39197de07c37e1a3c825"),
    "authority/ASSET_CLOSURE-unit-13.json": (4489, "771a8f09fd262838873e1390c43cae7da1f3989b74d8d2a7f67a856da9ea5e23"),
    "authority/commons-imageinfo-unit-13.json": (19061, "5f3c11df072f416668556047c0580ef3614c933810cb0444568a36e0d76e9aa5"),
    "authority/assets/Hyperbola_one_over_x.svg": (24384, "7007de14361a2f26446deee17751207ad13ec86d1572f1892a652df35107c85a"),
    "authority/assets/Hyperbola_one_over_x-500.png": (14689, "37faab77218828c177fe61e1efe9aa5417c6c986667b53c25b2880a56e31ddf2"),
    "authority/assets/Connected_and_disconnected_spaces2.svg": (652, "7bd06a32030d958226587efc35242c624a67c19a5cc31680569321d2f68887f5"),
    "authority/assets/Connected_and_disconnected_spaces2-500.png": (17967, "1d23e9a59e6fbbdccd3e58ab1e48e3088a102bc4661199554cb931339a197b08"),
    "scripts/freeze_unit13_media.py": (16130, "ab30c73f8cf4f5271caa6f8f656130fab05626bf1058988830a9e7265bf77617"),
}
PDF_FACTS = {
    "authority/artifacts/lecture-13-official.pdf": (242286, "185e4bfd91ff1814bed56af0c6eb619acaef772161b99232312d688c0690bd95"),
    "authority/artifacts/worksheet-13-official.pdf": (175801, "789444e8297ce0f896eb449a944c74e7555c959a01acfe66d329e05501c341bc"),
}

SOLUTION_NUMBERS = [3, 6, 8, 9, 11, 14, 15, 17, 20, 21, 24, 27, 28, 31]
SOLUTION_REVIDS = [
    1023890,
    663088,
    1112836,
    1060069,
    1023327,
    1089391,
    1029221,
    1113410,
    1095814,
    1096486,
    1060010,
    1094892,
    1089663,
    1065090,
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


def pandoc_ast(path: Path) -> tuple[dict[str, Any], str]:
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
    return json.loads(process.stdout), process.stderr


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
    manifest_path = AUTH / "UNIT_AUTHORITY_MANIFEST.json"
    map_path = AUTH / "ORDERED_EXERCISE_MAP.json"
    check_fact("authority/wikiversity/unit-13/UNIT_AUTHORITY_MANIFEST.json", MANIFEST_FACT)
    check_fact("authority/wikiversity/unit-13/ORDERED_EXERCISE_MAP.json", MAP_FACT)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    mapping = json.loads(map_path.read_text(encoding="utf-8"))
    require(manifest["schema"] == "brenner-unit-authority-freeze-v2", "authority schema")
    require(manifest["unit_number"] == 13, "authority unit")
    require(manifest["lecture"]["revid"] == 1112285, "lecture revision")
    require(manifest["lecture"]["mediawiki_sha1"] == "21738279d828654cee2399253d3c1763db6476a6", "lecture SHA-1")
    require(manifest["worksheet"]["revid"] == 1065092, "worksheet revision")
    require(manifest["worksheet"]["mediawiki_sha1"] == "20d30f0f2a09974c436262bbe20c0fab3fa34faa", "worksheet SHA-1")
    require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 142, "lecture closure count")
    require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 171, "worksheet closure count")
    require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "lecture missing transclusion")
    require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "worksheet missing transclusion")
    require(len(manifest["files"]) == 60, "authority file count")
    for row in manifest["files"]:
        path = AUTH / row["file"]
        require(path.is_file() and not path.is_symlink(), f"missing authority file: {row['file']}")
        require(path.stat().st_size == row["bytes"], f"authority bytes: {row['file']}")
        require(digest(path) == row["sha256"], f"authority hash: {row['file']}")
    require(mapping["unit"] == 13, "exercise map unit")
    require(mapping["exercise_count"] == 37, "exercise map count")
    require(mapping["solution_count"] == 14, "solution map count")
    require([row["exercise_number"] for row in mapping["entries"]] == list(range(1, 38)), "exercise order")
    solutions = [row for row in mapping["entries"] if row["has_public_solution"]]
    require([row["exercise_number"] for row in solutions] == SOLUTION_NUMBERS, "solution-number topology")
    require([row["revid"] for row in solutions] == SOLUTION_REVIDS, "solution revision topology")
    for row in solutions:
        for key in ("xml_file", "html_file"):
            witness = AUTH / row[key]
            require(witness.is_file() and not witness.is_symlink(), f"missing solution witness {row[key]}")
            require(witness.stat().st_size == row[key.replace("file", "bytes")], f"solution bytes {row[key]}")
            require(digest(witness) == row[key.replace("file", "sha256")], f"solution hash {row[key]}")
    for relative, fact in PDF_FACTS.items():
        check_fact(relative, fact)
        require((ROOT / relative).read_bytes().startswith(b"%PDF-"), f"PDF signature {relative}")
    return {
        "manifest_bytes": MANIFEST_FACT[0],
        "manifest_sha256": MANIFEST_FACT[1],
        "lecture_revid": 1112285,
        "worksheet_revid": 1065092,
        "lecture_transclusions": 142,
        "worksheet_transclusions": 171,
        "exercises": 37,
        "public_solutions": 14,
        "solution_numbers": SOLUTION_NUMBERS,
        "authority_files_verified": 60,
    }


def verify_media() -> dict[str, Any]:
    facts = [check_fact(relative, fact) for relative, fact in MEDIA_FACTS.items()]
    rights_path = ROOT / "authority" / "RIGHTS-unit-13.csv"
    with rights_path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 2, "rights row count")
    require([row["asset_id"] for row in rows] == ["br-ak-u13-media-001", "br-ak-u13-media-002"], "asset IDs")
    require(all(row["license_short"] or row["usage_terms"] for row in rows), "missing component licence")
    for row in rows:
        for prefix in ("local", "pdf_local"):
            path = ROOT / row[f"{prefix}_path"]
            require(path.is_file() and not path.is_symlink(), f"missing {prefix} asset")
            require(path.stat().st_size == int(row[f"{prefix}_bytes"]), f"{prefix} bytes")
            require(digest(path) == row[f"{prefix}_sha256"], f"{prefix} hash")
    closure = json.loads((ROOT / "authority" / "ASSET_CLOSURE-unit-13.json").read_text(encoding="utf-8"))
    require(closure["unit"] == 13, "media closure unit")
    require(closure["reader_media_positions"] == 2, "media positions")
    require(closure["unique_local_assets"] == 4, "binary media surfaces")
    require(closure["rights_sha256"] == MEDIA_FACTS["authority/RIGHTS-unit-13.csv"][1], "rights binding")
    require(closure["reader_credits_sha256"] == SOURCE_FACTS["source/id-ID/media-credits-unit-13.md"][1], "credits binding")
    require(len(closure["official_pdf_component_rights"]) == 2, "PDF component-rights closure")
    return {
        "media_positions": 2,
        "binary_surfaces": 4,
        "rights_rows": 2,
        "facts": facts,
    }


def verify_translation() -> dict[str, Any]:
    facts = [check_fact(relative, fact) for relative, fact in SOURCE_FACTS.items()]
    facts.extend(check_fact(relative, fact) for relative, fact in CONTROL_FACTS.items())
    lecture = (SOURCE / "lecture-13.md").read_text(encoding="utf-8")
    worksheet = (SOURCE / "worksheet-13.md").read_text(encoding="utf-8")
    solutions = (SOURCE / "worksheet-13-solutions.md").read_text(encoding="utf-8")
    credits = (SOURCE / "media-credits-unit-13.md").read_text(encoding="utf-8")
    all_text = "\n".join((lecture, worksheet, solutions, credits))
    require("translation_status: complete" in lecture, "lecture completion flag")
    require("translation_status: complete" in worksheet, "worksheet completion flag")
    require("translation_status: complete" in solutions, "solution completion flag")
    require(all(token not in all_text.casefold() for token in ("todo", "fixme", "tbd", "placeholder")), "placeholder residue")
    require(not re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|access[_-]?token|bearer\s+[A-Za-z0-9._-]{20,}", all_text, flags=re.I), "secret-like content")
    prose = strip_nonprose(all_text)
    residue = re.findall(r"\b(?:Es sei|Zeige|Dann|Aufgabe|Beweis|Nenneraufnahme|zusammenhängend|idempotentes)\b", prose, flags=re.I)
    require(not residue, f"visible German residue: {residue}")
    require("lokalisasi" not in prose.casefold(), "nonpreferred localization term")
    for term in ("pelokalan", "sistem multiplikatif", "unsur idempoten", "gelanggang produk", "sistem multiplikatif jenuh"):
        require(term in prose.casefold(), f"required terminology absent: {term}")

    exercise_headers = re.findall(r"^### Soal 13\.(\d+)(?:[^\n]*)\{#br-ak-2025-2026-w13-ex-(\d{2})\}$", worksheet, flags=re.M)
    require(exercise_headers == [(str(i), f"{i:02d}") for i in range(1, 38)], "exercise headers/IDs")
    starred = [int(value) for value in re.findall(r"^### Soal 13\.(\d+) ★", worksheet, flags=re.M)]
    require(starred == SOLUTION_NUMBERS, "starred solution topology")
    entity_comments = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    require(entity_comments == [row["exercise_title"] for row in mapping["entries"]], "exercise entity mapping")
    solution_headers = [int(value) for value in re.findall(r"^## Solusi Soal 13\.(\d+) ", solutions, flags=re.M)]
    require(solution_headers == SOLUTION_NUMBERS, "solution headers")
    solution_comments = re.findall(r"<!-- upstream_solution: .*?; pageid=\d+; revid=(\d+) -->", solutions)
    require([int(value) for value in solution_comments] == SOLUTION_REVIDS, "solution comments/revisions")
    back_links = [int(value) for value in re.findall(r"\[Kembali ke Soal 13\.(\d+)\]\(#br-ak-2025-2026-w13-ex-\d{2}\)", solutions)]
    require(back_links == SOLUTION_NUMBERS, "solution back links")
    stable_ids = re.findall(r"\{#(br-ak-2025-2026-[^}]+)\}", "\n".join((lecture, worksheet, solutions)))
    require(len(stable_ids) == len(set(stable_ids)), "duplicate Unit 13 stable IDs")
    require(len(stable_ids) == 74, f"unexpected stable-ID count: {len(stable_ids)}")
    require(lecture.count("<!-- upstream_entity:") == 13, "lecture semantic entity count")
    require(worksheet.count("<!-- upstream_entity:") == 37, "worksheet semantic entity count")
    require(solutions.count("<!-- upstream_solution:") == 14, "solution provenance count")
    require(lecture.count("![") == 2, "lecture image positions")
    require("authority/assets/Hyperbola_one_over_x.svg" in lecture, "hyperbola media reference")
    require("authority/assets/Connected_and_disconnected_spaces2.svg" in lecture, "connectedness media reference")

    normalized = normalized_math("\n".join((lecture, worksheet, solutions)))
    protected = [
        r"D(f)\subseteqK\!-\!\operatorname{Spek}(R)",
        r"R_f\congR[T]/(Tf-1)",
        r"K[X]_X=K[X,X^{-1}]",
        r"K[X,Y]/(XY-1)",
        r"e^2=e",
        r"D(e)\capD(1-e)=D(e(1-e))=D(e-e^2)=D(0)=\varnothing",
        r"(R/(F))_S\cong(R_S)/(F)",
        r"(R/\mathfraka)_S\congR_S/\mathfrakaR_S",
        r"\mathbbQ[X]/(X^4-1)",
        r"R/(\mathfraka_1\cdots\mathfraka_n)",
        r"V(g)=\varnothing=V(1)",
        r"R=(\mathbbZ/n\mathbbZ)[X]/(X^n)",
    ]
    missing = [token for token in protected if token not in normalized]
    require(not missing, f"protected mathematics absent: {missing}")

    ast_receipts: dict[str, Any] = {}
    for name in ("lecture-13.md", "worksheet-13.md", "worksheet-13-solutions.md", "media-credits-unit-13.md"):
        ast, _ = pandoc_ast(SOURCE / name)
        nodes = list(walk(ast.get("blocks", [])))
        headers = [node for node in nodes if node.get("t") == "Header"]
        maths = [node for node in nodes if node.get("t") == "Math"]
        images = [node for node in nodes if node.get("t") == "Image"]
        header_ids = [node["c"][1][0] for node in headers]
        require(all(header_ids), f"header without ID: {name}")
        require(len(header_ids) == len(set(header_ids)), f"duplicate AST header ID: {name}")
        ast_receipts[name] = {
            "headers": len(headers),
            "math_nodes": len(maths),
            "images": len(images),
            "stable_header_ids": len(header_ids),
            "pandoc_warnings": 0,
        }
    require(ast_receipts["worksheet-13.md"]["headers"] == 40, "worksheet AST header count")
    require(ast_receipts["worksheet-13-solutions.md"]["headers"] == 15, "solution AST header count")

    with (ROOT / "00_control" / "TERMINOLOGY.csv").open(encoding="utf-8", newline="") as stream:
        terms = {row["source_term"]: row for row in csv.DictReader(stream)}
    expected_terms = {
        "Nenneraufnahme": "pelokalan",
        "multiplikatives System": "sistem multiplikatif",
        "idempotentes Element": "unsur idempoten",
        "Produktring": "gelanggang produk",
        "saturiertes multiplikatives System": "sistem multiplikatif jenuh",
    }
    for source_term, target_term in expected_terms.items():
        require(terms[source_term]["preferred_target"] == target_term, f"terminology target {source_term}")
        require(terms[source_term]["status"] == "admitted", f"terminology status {source_term}")
    with (ROOT / "00_control" / "CORRECTIONS.csv").open(encoding="utf-8", newline="") as stream:
        correction_ids = {row["correction_id"] for row in csv.DictReader(stream)}
    require({"AGC-CORR-0028", "AGC-CORR-0029", "AGC-CORR-0030"} <= correction_ids, "Unit 13 correction ledger bindings")
    return {
        "source_and_control_facts": facts,
        "stable_ids": len(stable_ids),
        "exercises": 37,
        "public_solutions": 14,
        "ast": ast_receipts,
        "visible_german_residue": 0,
        "placeholder_count": 0,
        "secret_like_count": 0,
        "protected_math_checks": len(protected),
        "correction_bindings": ["AGC-CORR-0028", "AGC-CORR-0029", "AGC-CORR-0030"],
    }


def main() -> int:
    receipt = {
        "schema": "ag-bridge-unit-translation-qa-v1",
        "status": "PASS",
        "unit": 13,
        "verified_date": "2026-08-24",
        "authority": verify_authority(),
        "media_and_rights": verify_media(),
        "translation": verify_translation(),
        "provenance": "OpenAI Codex gpt-5.6-sol, Ultra.",
    }
    QA.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "unit": 13, "receipt": OUT.relative_to(ROOT).as_posix(), "bytes": OUT.stat().st_size, "sha256": digest(OUT)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
