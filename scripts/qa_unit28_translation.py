#!/usr/bin/env python3
"""Fail-closed translation, mathematics, rights, and accessibility QA for Unit 28."""

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
OUT = ROOT / "qa" / "UNIT_28_TRANSLATION_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
MANIFEST_SHA = "f2e34fc420c4beec300ea9e0accc52598e12c27f46c9022611996b1b43e29a99"

FACTS = {
    "authority/wikiversity/unit-28/UNIT_AUTHORITY_MANIFEST.json": (134460, MANIFEST_SHA),
    "authority/wikiversity/unit-28/ORDERED_EXERCISE_MAP.json": (16100, "c5aed5500f44a39bbe0a7a079792e0da11781a24a69c274d7170b0e2cdc1df40"),
    "authority/wikiversity/unit-28/lecture-28.xml": (7443, "3dc1abff96585199774b74910d1fc93102d0baf31e09ffa432a6e3966ddb5423"),
    "authority/wikiversity/unit-28/lecture-28-expanded.tex": (25871, "ed9054224eb4f1d8d5849d9e44c88f82107866c8f0944ee7cb047e27ad337709"),
    "authority/wikiversity/unit-28/worksheet-28.xml": (4988, "dc1af11088dac5f3ae3597a94af6bdba91afe35de35d8c2aecf4d26edd00f4fa"),
    "authority/wikiversity/unit-28/worksheet-28-expanded.tex": (6809, "9505f42a5a87139ca3e3dae694dc90b1692b38e0a9e312efa3b9159bbf2bab94"),
    "authority/wikiversity/unit-28/solution-ex10.xml": (4429, "b0ed23c137883f7304b18304e06b5fa5e02cce5ae81b966a5e23c428d84497be"),
    "authority/UNIT_28_AUTHORITY_FREEZE.md": (5425, "acb9e2053e6f883953f05ff4f274f96aa70f7c6f8239667f47cc838627f313d2"),
    "authority/RIGHTS-unit-28.csv": (4967, "84e7132495c1f78bd71afb0c436e23322f90d05f81a74e2f088cb1b586321651"),
    "authority/ASSET_CLOSURE-unit-28.json": (12939, "d7059564e2214dcafef6a8e0cd9cc43d7f2a86e70ca9e647719995cb0ef231b3"),
    "qa/UNIT_28_AUTHORITY_QA.json": (1670, "e6c5826d63697b57da35f2b3117652160ed2fd5652c7ec395554c1d9887c45b1"),
    "qa/UNIT_28_TERMINOLOGY_QA.md": (2156, "e1bccf3c34d32b74d70c81d06b2ecd9ede0e37cd75d0c78a1b753cba076d62f1"),
    "qa/UNITS_01_27_MACHINE_QA.json": (4254, "33fdf951354c620bbfeedc483338aa611ef577f0adcb8e509bca7361dc9bb074"),
    "source/id-ID/lecture-28.md": (21279, "2a33c0e3049b0d2b140ee46b37f9fba452dca8f19c553317ddbee5c23f3768b7"),
    "source/id-ID/worksheet-28.md": (7393, "fa6b7003de697739d3a03e00cb35b42119f1fff78836de536ba32584e33a361e"),
    "source/id-ID/worksheet-28-solutions.md": (3107, "4428b2e180096f7ab719aa649f64e2caa3be03c71d1198a7c7747616b90dfbf5"),
    "source/id-ID/media-credits-unit-28.md": (3774, "6155b47c596d97ea0af6f50f0c451453eca43231f8f04b4ad7617f36abfa1b52"),
    "source/id-ID/frontmatter-units-01-28.md": (4985, "f2408d86b7eef190ca586c8041e3ac733784b91cf1bbf7445baed1b604b87d9c"),
    "00_control/TERMINOLOGY.csv": (41134, "2a0ac96829d12afa2e07ae503ed067aa6416ca17e0acc66d2d2f7cac6ba52213"),
    "00_control/CORRECTIONS.csv": (79899, "d39f2599526d9be24b4f6b7246b6ad92b87fd9d1a6042733903288f636bc056b"),
}
TERM_IDS = [f"AGT-{number:04d}" for number in range(250, 261)]
CORRECTION_IDS = [f"AGC-CORR-{number:04d}" for number in range(115, 126)]


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
        ["pandoc", "--from=markdown+yaml_metadata_block+tex_math_dollars+fenced_divs+bracketed_spans+raw_attribute", "--to=json", str(path)],
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
    raw = re.sub(r"```.*?```", "", raw, flags=re.S)
    raw = re.sub(r"`[^`\n]*`", "", raw)
    raw = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", raw)
    raw = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", raw)
    raw = re.sub(r"\$\$.*?\$\$", "", raw, flags=re.S)
    raw = re.sub(r"\$[^$\n]*\$", "", raw)
    return raw


def verify() -> dict[str, Any]:
    bound = {name: fact(name) for name in FACTS}
    manifest = json.loads((ROOT / "authority/wikiversity/unit-28/UNIT_AUTHORITY_MANIFEST.json").read_text(encoding="utf-8"))
    exercise_map = json.loads((ROOT / "authority/wikiversity/unit-28/ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    closure = json.loads((ROOT / "authority/ASSET_CLOSURE-unit-28.json").read_text(encoding="utf-8"))
    authority_qa = json.loads((ROOT / "qa/UNIT_28_AUTHORITY_QA.json").read_text(encoding="utf-8"))
    require(authority_qa["status"] == "PASS", "authority QA")
    require(manifest["final_live_identity_replay"]["result"] == "PASS", "live authority replay")
    require(manifest["final_live_identity_replay"]["semantic_unique_identity_count"] == 164, "semantic identity union")

    lecture = (SOURCE / "lecture-28.md").read_text(encoding="utf-8")
    worksheet = (SOURCE / "worksheet-28.md").read_text(encoding="utf-8")
    solutions = (SOURCE / "worksheet-28-solutions.md").read_text(encoding="utf-8")
    credits = (SOURCE / "media-credits-unit-28.md").read_text(encoding="utf-8")
    frontmatter = (SOURCE / "frontmatter-units-01-28.md").read_text(encoding="utf-8")
    unit_texts = [lecture, worksheet, solutions, credits]

    for name, raw in zip(("lecture", "worksheet", "solutions", "credits"), unit_texts, strict=True):
        require(MODEL in raw, f"provenance missing: {name}")
        require(not any(mark in raw for mark in ("\u2013", "\u2014", "\u2011")), f"Unicode dash: {name}")
        require(not re.search(r"(?i)\b(TODO|TBD|FIXME|LOREM|UNBOUND_PENDING|TO_BE_BOUND)\b", raw), f"placeholder: {name}")
        require(not re.search(r"(?i)(ghp_[A-Za-z0-9]{20,}|api[_-]?key\s*[:=]|bearer\s+[A-Za-z0-9._-]{20,})", raw), f"secret-like text: {name}")
        require(not any(unicodedata.category(ch) == "Cf" for ch in raw), f"invisible control: {name}")

    require("nach Aufgabe *****" in lecture and "siehe Aufgabe *****" in lecture, "source placeholders not disclosed exactly")
    require("tanpa menebak nomornya" in lecture, "unresolved reference handling")
    require("V_+(X^d+Y^d+Z^d)" in lecture and "operator titik nol proyektif" in lecture, "Fermat correction")
    require("Jika $d=1$" in lecture and "kedua turunan merupakan konstanta" in lecture, "Fermat degree-one repair")
    require(r"\operatorname{char}(K)\ne2" in lecture and "karakteristik dua" in lecture, "conic characteristic-two repair")
    require(lecture.count("**Jembatan edisi.**") == 1 and solutions.count("**Jembatan edisi.**") == 1, "editorial bridge disclosures")
    require("konvensi kurva eliptik" in lecture and "titik dasar" in lecture, "elliptic convention note")
    require("semua eksponen bulat" in worksheet and "n=0" in worksheet and "n<0" in worksheet, "integer exponent cases")
    require("tepat satu titik di tak hingga" in solutions.lower() and "kesesuaian tunggal-jamak" in solutions, "solution normalization")

    lecture_entities = re.findall(r"<!-- upstream_entity: (.*?) -->", lecture)
    worksheet_entities = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    require(len(lecture_entities) == 19 and len(set(lecture_entities)) == 19, "lecture entity topology")
    require(len(worksheet_entities) == 14 and len(set(worksheet_entities)) == 14, "worksheet entity topology")
    require(worksheet_entities == [row["exercise_title"] for row in exercise_map["entries"]], "worksheet authority order")
    require(exercise_map["exercise_count"] == 14 and exercise_map["solution_count"] == 1, "exercise/solution topology")
    roles = exercise_map["ordered_role_point_and_star_topology"]
    require(roles["warm_up_numbers"] == list(range(1, 11)) and roles["submitted_numbers"] == list(range(11, 15)), "role topology")
    require(roles["starred_numbers"] == [10] and roles["upload_numbers"] == [], "star/upload topology")
    require(roles["displayed_points"] == {"11": 3, "12": 4, "13": 3, "14": 3}, "displayed point topology")
    require([int(value) for value in re.findall(r"(?m)^### Soal 28\.(\d+)", worksheet)] == list(range(1, 15)), "reader exercise order")
    require(re.findall(r"(?m)^### Soal 28\.(\d+) \((\d+) poin\)", worksheet) == [("11", "3"), ("12", "4"), ("13", "3"), ("14", "3")], "reader displayed points")
    require(re.findall(r"(?m)^### Soal 28\.(\d+) \*", worksheet) == ["10"], "reader star topology")
    require("public_solution_count: 1" in solutions and "negative_public_solution_count: 13" in solutions, "solution closure metadata")
    require(re.findall(r"(?m)^## Solusi Soal 28\.(\d+)", solutions) == ["10"], "reader public solution topology")
    require("Tidak ada solusi tambahan yang dibuat" in solutions, "no invented solutions")

    protected_lecture = [
        r"V_+(\mathfrak a)\subseteq\mathbb P_K^n",
        r"D_+^Y(X_i):=Y\cap D_+^{\mathbb P_K^n}(X_i)",
        r"\Gamma(U,\mathcal O)",
        r"\psi^{-1}(U)\longrightarrow U\stackrel{f}{\longrightarrow}\mathbb A_K^1",
        r"V(XY-1)\subset\mathbb A_K^2\subset\mathbb P_K^2",
        r"\widetilde F=F(1,X_1,\ldots,X_n)",
        r"F=G_d+G_{d-1}Z+\cdots+G_mZ^{d-m}",
        r"V_+(X^d+Y^d+Z^d)\subseteq\mathbb P_K^2",
        r"g=\frac{(d-1)(d-2)}{2}",
    ]
    for surface in protected_lecture:
        require(surface in lecture, f"protected lecture surface: {surface}")
    protected_worksheet = [
        r"x\longmapsto x^n",
        r"V\!\left((X^2+Y^2)^2-2X(X^2+Y^2)-Y^2\right)",
        r"\mathbb A_K^{n+1}\setminus\{0\}\longrightarrow\mathbb P_K^n",
        r"C=V(Y-X^3+X+2)",
        r"V(\mathfrak a)\cap(\mathbb A_K^{n+1}\setminus\{0\})",
        r"\Gamma(U,\mathcal O)",
        r"\Gamma\!\left(\mathbb P_K^n,\mathcal O_{\mathbb P_K^n}\right)=K",
    ]
    for surface in protected_worksheet:
        require(surface in worksheet, f"protected worksheet surface: {surface}")
    protected_solution = [
        r"x\longmapsto(x,x^3-x-2)=(x,y)",
        r"V_+(YZ^2-X^3+XZ^2+2Z^3)",
        r"V(Z^2-X^3+XZ^2+2Z^3)",
    ]
    for surface in protected_solution:
        require(surface in solutions, f"protected solution surface: {surface}")
    require(lecture.count("**Catatan edisi -") == 7, "lecture visible edition-note count")
    require(worksheet.count("**Catatan edisi -") == 1, "worksheet visible edition-note count")
    require(solutions.count("**Catatan edisi -") == 1, "solution visible edition-note count")
    require(all(correction in lecture + worksheet + solutions for correction in CORRECTION_IDS), "correction metadata")

    with (ROOT / "00_control/TERMINOLOGY.csv").open(encoding="utf-8", newline="") as stream:
        terms = list(csv.DictReader(stream))
    with (ROOT / "00_control/CORRECTIONS.csv").open(encoding="utf-8", newline="") as stream:
        corrections = list(csv.DictReader(stream))
    require(len(terms) == 260 and len({row["term_id"] for row in terms}) == 260, "terminology IDs")
    require(len(corrections) == 146 and len({row["correction_id"] for row in corrections}) == 146, "correction IDs")
    term_rows = {row["term_id"]: row for row in terms}
    correction_rows = {row["correction_id"]: row for row in corrections}
    require(all(term_id in term_rows for term_id in TERM_IDS), "Unit 28 terms absent")
    require(all(correction_id in correction_rows for correction_id in CORRECTION_IDS), "Unit 28 corrections absent")
    require(term_rows["AGT-0251"]["preferred_target"] == "varietas kuasiprojektif", "quasiprojective terminology")
    require(term_rows["AGT-0255"]["preferred_target"] == "genus", "genus terminology")
    human = strip_nonprose(lecture + "\n" + worksheet + "\n" + solutions + "\n" + credits)
    require(not re.search(r"(?i)\bprojektif\b", human), "nonpreferred projektif residue")
    require(not re.search(r"(?i)\b(es sei|zeige|projektive varietät|quasiprojektive varietät|beweis|aufgabe)\b", human), "visible German residue")

    expected_ast = {
        "lecture-28.md": (24, 221, 4),
        "worksheet-28.md": (17, 58, 0),
        "worksheet-28-solutions.md": (2, 12, 0),
        "media-credits-unit-28.md": (1, 0, 0),
        "frontmatter-units-01-28.md": (2, 0, 0),
    }
    ast_receipts: dict[str, Any] = {}
    unit_ids: list[str] = []
    for name, expected in expected_ast.items():
        ast = pandoc_ast(SOURCE / name)
        nodes = list(walk(ast.get("blocks", [])))
        headers = [node for node in nodes if node.get("t") == "Header"]
        maths = [node for node in nodes if node.get("t") == "Math"]
        images = [node for node in nodes if node.get("t") == "Image"]
        ids = [node["c"][1][0] for node in headers]
        require((len(headers), len(maths), len(images)) == expected, f"AST topology: {name}")
        require(all(ids) and len(ids) == len(set(ids)), f"AST IDs: {name}")
        if name != "frontmatter-units-01-28.md":
            unit_ids.extend(ids)
        ast_receipts[name] = {"headers": len(headers), "math_nodes": len(maths), "images": len(images), "stable_header_ids": len(ids), "pandoc_warnings": 0}
    require(len(unit_ids) == 44 and len(unit_ids) == len(set(unit_ids)), "Unit 28 global IDs")
    require(sum(ast_receipts[name]["math_nodes"] for name in ("lecture-28.md", "worksheet-28.md", "worksheet-28-solutions.md")) == 291, "Unit 28 math node total")

    image_rows = re.findall(r"!\[([^\]]+)\]\((authority/assets/[^)]+)\)", lecture)
    require(len(image_rows) == 4 and all(alt.strip() for alt, _ in image_rows), "image alt topology")
    closure_assets = {item["local_path"]: item for item in closure["assets"]}
    for alt, relative in image_rows:
        require(relative in closure_assets, f"unbound reader image: {relative}")
        path = ROOT / relative
        item = closure_assets[relative]
        require(path.is_file() and path.stat().st_size == item["local_bytes"] and digest(path) == item["local_sha256"], f"reader image drift: {relative}")
    normalized_credits = re.sub(r"\s+", " ", credits)
    require(credits.count("SHA-256") >= 6 and "tidak membuat klaim pelisensian payung" in normalized_credits, "credit closure")
    require("CC0" in credits and "domain publik" in credits and "CC BY-SA 2.0" in credits and "CC BY-SA 4.0" in credits, "mixed rights disclosure")
    require("Ranveig" in credits and "bukan" in credits and "pencipta" in credits and "Oleg Alexandrov" in credits, "creator/uploader discrepancy")

    cumulative_exercises = 0
    cumulative_solutions = 0
    for number in range(1, 29):
        suffix = f"{number:02d}"
        worksheet_text = (SOURCE / f"worksheet-{suffix}.md").read_text(encoding="utf-8")
        solution_text = (SOURCE / f"worksheet-{suffix}-solutions.md").read_text(encoding="utf-8")
        cumulative_exercises += len(re.findall(r"(?m)^### Soal \d+\.\d+", worksheet_text))
        cumulative_solutions += len(re.findall(r"(?m)^## Solusi Soal ", solution_text))
    baseline = json.loads((ROOT / "qa/UNITS_01_27_MACHINE_QA.json").read_text(encoding="utf-8"))["coverage"]
    require(baseline["reader_media_positions"] == 94, "Unit 27 media baseline")
    cumulative_media = baseline["reader_media_positions"] + len(image_rows)
    require((cumulative_exercises, cumulative_solutions, cumulative_media) == (671, 118, 98), "cumulative source counts")
    flat_front = re.sub(r"\s+", " ", frontmatter)
    require("Unit 1-28 memuat 671 soal" in flat_front and "semua 118 solusi publik" in flat_front, "frontmatter coverage")
    require("Unit 1-23 mengikat revisi beku" in flat_front and "Unit 24-28 mengikat kuliah dan lembar kerja" in flat_front, "edition split")
    require(MANIFEST_SHA in frontmatter and MODEL in frontmatter, "frontmatter manifest/provenance")
    require("tidak menyiratkan dukungan" in flat_front and "bukan klaim lisensi payung" in flat_front, "frontmatter rights/nonendorsement")

    return {
        "bound_facts": bound,
        "authority": {"lecture_root_plus_dependencies": 120, "worksheet_root_plus_dependencies": 75, "solution_root_plus_dependencies": 8, "semantic_live_union": 164},
        "translation": {
            "lecture_semantic_entities": 19,
            "worksheet_exercises": 14,
            "public_solutions": 1,
            "negative_solution_candidates": 13,
            "stable_ids": 44,
            "math_nodes": 291,
            "reader_media_positions": 4,
            "visible_correction_disclosures": 9,
            "visible_editorial_bridges": 2,
            "terminology_bindings": TERM_IDS,
            "correction_bindings": CORRECTION_IDS,
            "visible_german_residue": 0,
            "placeholder_count_excluding_two_disclosed_source_stars": 0,
            "secret_like_count": 0,
            "unicode_dash_count": 0,
            "invisible_unicode_controls": 0,
        },
        "ast": ast_receipts,
        "cumulative_source": {"lectures": 28, "worksheets": 28, "exercises": 671, "public_solutions": 118, "media_positions": 98},
        "rights": {"cc0_media": 1, "public_domain_media": 3, "blanket_relicense_claim": False},
        "revision_contributors": {"lecture_root": "Arbota", "worksheet_root": "Arbota", "solution_10": "Bocardodarapti"},
    }


def main() -> int:
    receipt = {
        "schema": "ag-bridge-unit-translation-qa-v1",
        "status": "PASS",
        "unit": 28,
        "verified_date": "2026-08-26",
        **verify(),
        "provenance": MODEL + ".",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "unit": 28, "receipt": OUT.relative_to(ROOT).as_posix(), "bytes": OUT.stat().st_size, "sha256": digest(OUT)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
