#!/usr/bin/env python3
"""Fail-closed translation, mathematics, rights, and accessibility QA for Unit 27."""

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
OUT = ROOT / "qa" / "UNIT_27_TRANSLATION_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
MANIFEST_SHA = "98f9ebcc0d3b41bb0b955c5190d416b9ebfc07433015732faaf7f38366a1d9b2"

FACTS = {
    "authority/wikiversity/unit-27/UNIT_AUTHORITY_MANIFEST.json": (135052, MANIFEST_SHA),
    "authority/wikiversity/unit-27/ORDERED_EXERCISE_MAP.json": (12839, "4fb226bb355ef16c06ffbe81a8134585fa5c4f21ee4cf9101630c6f78930e55c"),
    "authority/wikiversity/unit-27/lecture-27.xml": (7112, "9e1a4f687ca1faf008e9864460dc036f7849e2a3203f7d30dd509c7876b69ea6"),
    "authority/wikiversity/unit-27/lecture-27-expanded.tex": (28235, "2b75b62d96c149f8344de2060fcbc96a4d2061140dd6c509b2b11ad2e95dc8b4"),
    "authority/wikiversity/unit-27/worksheet-27.xml": (4919, "fd72eb822d0be7c0779d79e43204cad46c7ff382fe8e04b8334a3b439916e540"),
    "authority/wikiversity/unit-27/worksheet-27-expanded.tex": (5050, "b329f0ac6cdf39744e79401a82e239ad1232c420a209e07dfcd01577f09ebfa1"),
    "authority/UNIT_27_AUTHORITY_FREEZE.md": (4838, "76da6c76238a6b542848b42d32a897613c24e43f9a2dee52b90a7300fa8ebb3d"),
    "authority/RIGHTS-unit-27.csv": (11564, "df2fb8403ddef014500e81e2165e2d4e400a0573dd262ba3dba5ece6bcd46821"),
    "authority/ASSET_CLOSURE-unit-27.json": (26057, "b08e53863d977899d9910d1b6f48e82237f590402e8450f2683b07a078c1ebc6"),
    "qa/UNIT_27_AUTHORITY_QA.json": (1430, "60b4b2cce7cbd18bcfdbe7698d136bcee9e721dba631e525726ea8e185a4c139"),
    "qa/UNIT_27_TERMINOLOGY_QA.md": (2156, "2af64f71732f7d2ee7bf8e163c2d097701471377e56472d4ab850ccbaba79035"),
    "source/id-ID/lecture-27.md": (24844, "81ed14c582b9b181cb9dfe1795c9f0bf95cf894f3af66935dd4912b397f446b9"),
    "source/id-ID/worksheet-27.md": (5728, "2ccf9879d8bad546a21e100fec700c49b49f5fdf98aa8a598c274827700487ee"),
    "source/id-ID/worksheet-27-solutions.md": (1723, "fe9b9dd6ced41c2ccbea06bd99e3dfba2708d68290c8763d1c9152cd25ab2733"),
    "source/id-ID/media-credits-unit-27.md": (5048, "4e46a14420118be7ad665a59ae39787d6dc29d6c8ca3df1c3bffb6f01dca1e55"),
    "source/id-ID/frontmatter-units-01-27.md": (4806, "66e9e4bfb31c24cb131e05c02c8b19509d9cfd44c9d222c3d75d312b5a95e280"),
    "00_control/TERMINOLOGY.csv": (39202, "8f0bfb467b935a34350e56a038d166a48ad89a2e656044563ac4a5c2aee0f11e"),
    "00_control/CORRECTIONS.csv": (73728, "e9f5aef207253e30badcfd095a3bc3cf5d465b18a6f700a82b1e32422183acc8"),
}
TERM_IDS = [f"AGT-{number:04d}" for number in range(230, 250)]
CORRECTION_IDS = [f"AGC-CORR-{number:04d}" for number in range(108, 115)]


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
    raw = re.sub(r"\x60\x60\x60.*?\x60\x60\x60", "", raw, flags=re.S)
    raw = re.sub(r"\x60[^\x60\n]*\x60", "", raw)
    raw = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", raw)
    raw = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", raw)
    raw = re.sub(r"\$\$.*?\$\$", "", raw, flags=re.S)
    raw = re.sub(r"\$[^$\n]*\$", "", raw)
    return raw


def verify() -> dict[str, Any]:
    bound = {name: fact(name) for name in FACTS}
    manifest = json.loads((ROOT / "authority/wikiversity/unit-27/UNIT_AUTHORITY_MANIFEST.json").read_text(encoding="utf-8"))
    exercise_map = json.loads((ROOT / "authority/wikiversity/unit-27/ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    closure = json.loads((ROOT / "authority/ASSET_CLOSURE-unit-27.json").read_text(encoding="utf-8"))
    authority_qa = json.loads((ROOT / "qa/UNIT_27_AUTHORITY_QA.json").read_text(encoding="utf-8"))
    require(authority_qa["status"] == "PASS", "authority QA")
    require(manifest["final_live_identity_replay"]["result"] == "PASS", "live authority replay")
    require(manifest["final_live_identity_replay"]["semantic_unique_identity_count"] == 157, "semantic identity union")
    require(manifest["transclusion_topology"]["lecture"]["with_root"] == 121, "lecture authority closure")
    require(manifest["transclusion_topology"]["worksheet"]["with_root"] == 61, "worksheet authority closure")

    lecture = (SOURCE / "lecture-27.md").read_text(encoding="utf-8")
    worksheet = (SOURCE / "worksheet-27.md").read_text(encoding="utf-8")
    solutions = (SOURCE / "worksheet-27-solutions.md").read_text(encoding="utf-8")
    credits = (SOURCE / "media-credits-unit-27.md").read_text(encoding="utf-8")
    frontmatter = (SOURCE / "frontmatter-units-01-27.md").read_text(encoding="utf-8")
    unit_texts = [lecture, worksheet, solutions, credits]

    for name, raw in zip(("lecture", "worksheet", "solutions", "credits"), unit_texts, strict=True):
        require(MODEL in raw, f"provenance missing: {name}")
        require(not any(mark in raw for mark in ("\u2013", "\u2014", "\u2011")), f"Unicode dash: {name}")
        require(not re.search(r"(?i)\b(TODO|TBD|FIXME|LOREM|UNBOUND_PENDING)\b", raw), f"placeholder: {name}")
        require(not re.search(r"(?i)(ghp_[A-Za-z0-9]{20,}|api[_-]?key\s*[:=]|bearer\s+[A-Za-z0-9._-]{20,})", raw), f"secret-like text: {name}")
        require(not any(unicodedata.category(ch) == "Cf" for ch in raw), f"invisible control: {name}")
    require(lecture.count("Fakt *****") == 1 and "Catatan edisi - rujukan yang terputus" in lecture, "dangling reference disclosure")

    lecture_entities = re.findall(r"<!-- upstream_entity: (.*?) -->", lecture)
    worksheet_entities = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    require(len(lecture_entities) == 21 and len(set(lecture_entities)) == 21, "lecture entity topology")
    require(len(worksheet_entities) == 11 and len(set(worksheet_entities)) == 11, "worksheet entity topology")
    require(exercise_map["exercise_count"] == 11 and exercise_map["solution_count"] == 0, "exercise/solution topology")
    require(exercise_map["negative_public_solution_evidence"]["negative_numbers"] == list(range(1, 12)), "negative solution closure")
    require(exercise_map["ordered_role_point_and_star_topology"]["warm_up_numbers"] == list(range(1, 8)), "warm-up topology")
    require(exercise_map["ordered_role_point_and_star_topology"]["submitted_numbers"] == list(range(8, 12)), "submitted topology")
    require(exercise_map["ordered_role_point_and_star_topology"]["displayed_points"] == {"8": 3, "9": 3, "10": 3, "11": 3}, "displayed points")
    require(not exercise_map["ordered_role_point_and_star_topology"]["starred_numbers"], "unexpected stars")
    require([int(value) for value in re.findall(r"(?m)^### Soal 27\.(\d+)", worksheet)] == list(range(1, 12)), "reader exercise order")
    require(re.findall(r"(?m)^### Soal 27\.(\d+) \(3 poin\)", worksheet) == ["8", "9", "10", "11"], "reader point topology")
    require("public_solution_count: 0" in solutions and "negative_public_solution_count: 11" in solutions, "solution closure metadata")
    require("Tidak ada solusi tambahan yang dibuat" in solutions, "no invented solutions")

    protected = [
        r"\varphi_i:\mathbb A_K^n&\longrightarrow\mathbb P_K^n",
        r"D_+(X_i)",
        r"F(1,X_1,\ldots,X_n)=0",
        r"F(0,X_1,\ldots,X_n)=0",
        r"F=a_0X_0+a_1X_1+\cdots+a_nX_n",
        r"\mathfrak a_P+(X_0^2)",
        r"\mathbb K^\times\times V(X_i-1)",
        r"P,Q\in D_+(L)\cong\mathbb K^n",
    ]
    for surface in protected:
        require(surface in lecture, f"protected lecture surface: {surface}")
    worksheet_surfaces = [
        r"\mathbb A_K^{n+1}\setminus\{0\}",
        r"r+s\geq n",
        r"X\cap Y\ne\varnothing",
        r"D_+(L)",
        r"r(R_+)^k\subseteq I",
    ]
    for surface in worksheet_surfaces:
        require(surface in worksheet, f"protected worksheet surface: {surface}")
    require(lecture.count("**Catatan edisi -") == 7, "visible correction note count")
    require(all(correction in lecture for correction in CORRECTION_IDS), "correction metadata")

    with (ROOT / "00_control/TERMINOLOGY.csv").open(encoding="utf-8", newline="") as stream:
        terms = list(csv.DictReader(stream))
    with (ROOT / "00_control/CORRECTIONS.csv").open(encoding="utf-8", newline="") as stream:
        corrections = list(csv.DictReader(stream))
    require(len(terms) == 249 and len({row["term_id"] for row in terms}) == 249, "terminology IDs")
    require(len(corrections) == 135 and len({row["correction_id"] for row in corrections}) == 135, "correction IDs")
    term_rows = {row["term_id"]: row for row in terms}
    correction_rows = {row["correction_id"]: row for row in corrections}
    require(all(term_id in term_rows for term_id in TERM_IDS), "Unit 27 terms absent")
    require(all(correction_id in correction_rows for correction_id in CORRECTION_IDS), "Unit 27 corrections absent")
    require(term_rows["AGT-0230"]["preferred_target"] == "ruang proyektif", "proyektif terminology")
    human = strip_nonprose(lecture + "\n" + worksheet + "\n" + solutions + "\n" + credits)
    require(not re.search(r"(?i)\bprojektif\b", human), "nonpreferred projektif residue")
    require(not re.search(r"(?i)\b(es sei|zeige|der projektive|die projektive|ist genau dann|beweis)\b", human), "visible German residue")

    expected_ast = {
        "lecture-27.md": (23, 230, 10),
        "worksheet-27.md": (14, 39, 0),
        "worksheet-27-solutions.md": (1, 0, 0),
        "media-credits-unit-27.md": (1, 0, 0),
        "frontmatter-units-01-27.md": (2, 0, 0),
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
        if name != "frontmatter-units-01-27.md":
            unit_ids.extend(ids)
        ast_receipts[name] = {"headers": len(headers), "math_nodes": len(maths), "images": len(images), "stable_header_ids": len(ids), "pandoc_warnings": 0}
    require(len(unit_ids) == 39 and len(unit_ids) == len(set(unit_ids)), "Unit 27 global IDs")
    require(ast_receipts["lecture-27.md"]["math_nodes"] + ast_receipts["worksheet-27.md"]["math_nodes"] == 269, "Unit 27 math node total")

    image_rows = re.findall(r"!\[([^\]]+)\]\((authority/assets/[^)]+)\)", lecture)
    require(len(image_rows) == 10 and all(alt.strip() for alt, _ in image_rows), "image alt topology")
    closure_assets = {item["local_path"]: item for item in closure["assets"]}
    for alt, relative in image_rows:
        require(relative in closure_assets, f"unbound reader image: {relative}")
        path = ROOT / relative
        item = closure_assets[relative]
        require(path.is_file() and path.stat().st_size == item["local_bytes"] and digest(path) == item["local_sha256"], f"reader image drift: {relative}")
    normalized_credits = re.sub(r"\s+", " ", credits)
    require(credits.count("SHA-256") >= 12 and "tidak ada klaim pelisensian payung" in normalized_credits, "credit closure")
    require("CC BY-SA 3.0" in credits and "domain publik" in credits and "CC BY-SA 2.0" in credits and "CC BY-SA 4.0" in credits, "mixed rights disclosure")

    cumulative_exercises = 0
    cumulative_solutions = 0
    for number in range(1, 28):
        suffix = f"{number:02d}"
        worksheet_text = (SOURCE / f"worksheet-{suffix}.md").read_text(encoding="utf-8")
        solution_text = (SOURCE / f"worksheet-{suffix}-solutions.md").read_text(encoding="utf-8")
        cumulative_exercises += len(re.findall(r"(?m)^### Soal \d+\.\d+", worksheet_text))
        cumulative_solutions += len(re.findall(r"(?m)^## Solusi Soal ", solution_text))
    require(cumulative_exercises == 657, "cumulative exercise count")
    require(cumulative_solutions == 117, "cumulative public solution count")
    flat_front = re.sub(r"\s+", " ", frontmatter)
    require("Unit 1-27 memuat 657 soal" in flat_front and "semua 117 solusi publik" in flat_front, "frontmatter coverage")
    require("Unit 1-23 mengikat revisi beku" in flat_front and "Unit 24-27 mengikat kuliah dan lembar kerja" in flat_front, "edition split")
    require(MANIFEST_SHA in frontmatter and MODEL in frontmatter, "frontmatter manifest/provenance")
    require("tidak menyiratkan dukungan" in flat_front and "bukan klaim lisensi payung" in flat_front, "frontmatter rights/nonendorsement")

    return {
        "bound_facts": bound,
        "authority": {"lecture_root_plus_dependencies": 121, "worksheet_root_plus_dependencies": 61, "semantic_live_union": 157},
        "translation": {
            "lecture_semantic_entities": 21,
            "worksheet_exercises": 11,
            "public_solutions": 0,
            "negative_solution_candidates": 11,
            "stable_ids": 39,
            "math_nodes": 269,
            "reader_media_positions": 10,
            "visible_correction_disclosures": 7,
            "terminology_bindings": TERM_IDS,
            "correction_bindings": CORRECTION_IDS,
            "visible_german_residue": 0,
            "placeholder_count": 0,
            "secret_like_count": 0,
            "unicode_dash_count": 0,
            "invisible_unicode_controls": 0,
        },
        "ast": ast_receipts,
        "cumulative_source": {"lectures": 27, "worksheets": 27, "exercises": 657, "public_solutions": 117, "media_positions": 94},
        "rights": {"component_licensed_media": 9, "public_domain_media": 1, "blanket_relicense_claim": False},
        "revision_contributors": {"lecture_root": "Arbota", "worksheet_root": "Arbota"},
    }


def main() -> int:
    receipt = {
        "schema": "ag-bridge-unit-translation-qa-v1",
        "status": "PASS",
        "unit": 27,
        "verified_date": "2026-08-26",
        **verify(),
        "provenance": MODEL + ".",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "unit": 27, "receipt": OUT.relative_to(ROOT).as_posix(), "bytes": OUT.stat().st_size, "sha256": digest(OUT)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
