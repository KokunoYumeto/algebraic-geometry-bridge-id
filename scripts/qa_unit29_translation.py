#!/usr/bin/env python3
"""Fail-closed translation, mathematics, rights, and accessibility QA for Unit 29."""

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
OUT = ROOT / "qa" / "UNIT_29_TRANSLATION_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra"
MANIFEST_SHA = "ec3b34ad387ae827ecaa365c4def3b0550f74b629d0db3873a7cc28dc0831bc5"

FACTS = {
    "authority/wikiversity/unit-29/UNIT_AUTHORITY_MANIFEST.json": (128548, MANIFEST_SHA),
    "authority/wikiversity/unit-29/ORDERED_EXERCISE_MAP.json": (13077, "75b07cabcb83cc12a6fd1259017f7e169c0ded461e7b7c94e65f033b71d12bc9"),
    "authority/wikiversity/unit-29/lecture-29.xml": (6360, "e5055632a6aa8119540cb5acccc0ba86a82b6d2bc88192b9ddd5a77aaea31d70"),
    "authority/wikiversity/unit-29/lecture-29-expanded.tex": (23292, "7c06a1dbb12904bd5f89427955ef8bdae5781e402522cd70f09a0c6e1ef1e784"),
    "authority/wikiversity/unit-29/worksheet-29.xml": (4871, "d82d020fef6e0d4f604bda9807f1befa2b8e1392afd9fb9459dbe17461d34574"),
    "authority/wikiversity/unit-29/worksheet-29-expanded.tex": (5439, "53a54b5b7e59be71c94d41dc791021c0b2d6165bf0b489670800b09387d560d2"),
    "authority/wikiversity/unit-29/solution-ex02.xml": (5545, "2b468a1f7d9bebff884c001c3a475a212601b022896953c97e6a55026cf38f66"),
    "authority/wikiversity/unit-29/solution-ex03.xml": (3994, "50771bcf86505ee8429426f3488ef46af450a258629d4403a2bc16aa74abcaff"),
    "authority/UNIT_29_AUTHORITY_FREEZE.md": (3828, "f95d74fa5f43f72e52204c482bcc9fdc2ad4b50e109beef4ac602b3e27e81826"),
    "authority/RIGHTS-unit-29.csv": (2939, "4962c9a0a32e775a788f1098cf994d4e6714f67226ae30e155189778e826323c"),
    "authority/ASSET_CLOSURE-unit-29.json": (10549, "d85f765a2ab195ed5c1ed12028c2558fcfadd227fa35ebf979267c4167e3f972"),
    "qa/UNIT_29_AUTHORITY_QA.json": (2439, "5632c075926fb6200d49c5f21d3425a5fed63dd67cf646128055fb96bf1afd00"),
    "qa/UNITS_01_28_MACHINE_QA.json": (3083, "c666cb1186f516cead5ebd1a16de616856c99013cd94983826c974aebbdf776f"),
    "source/id-ID/lecture-29.md": (19163, "3ed412b4c719d3ac03574013d5acc2bf8316ecc9a09ef33d286433400d5da951"),
    "source/id-ID/worksheet-29.md": (7831, "d061f5fb7132fa7e3c427f77ea3efce3dc07f4234c3cd4fa9389b03eff95d26b"),
    "source/id-ID/worksheet-29-solutions.md": (4232, "6ef42d1bdc9fab47fa0c2685b8754d3f9be14f0738c6c280f0f8ada89c6bd505"),
    "source/id-ID/media-credits-unit-29.md": (2734, "757ce4a42a2bdea04e8410609e68be7b5939d636cc72e26ae40007093d5fd7ae"),
    "source/id-ID/frontmatter-units-01-29.md": (5324, "fe21529faf5781ddbbacd58acc87e80bb9fcdabc1d32ec06f9050e2283de7c6c"),
    "00_control/TERMINOLOGY.csv": (43924, "2bf2e82d82b9cb6fa35818eb548cd768f5edfbf204bb64efa8ffecae25233f29"),
    "00_control/CORRECTIONS.csv": (85348, "b947d37222432ced8b55f37024ee805a71fcfca66c9e212392772736c1dd3c8f"),
}
TERM_IDS = [f"AGT-{number:04d}" for number in range(261, 266)]
CORRECTION_IDS = [f"AGC-CORR-{number:04d}" for number in range(126, 130)]


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
    raw = re.sub(r"\x60{3}.*?\x60{3}", "", raw, flags=re.S)
    raw = re.sub(r"\x60[^\x60\n]*\x60", "", raw)
    raw = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", raw)
    raw = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", raw)
    raw = re.sub(r"\$\$.*?\$\$", "", raw, flags=re.S)
    raw = re.sub(r"\$[^$\n]*\$", "", raw)
    return raw


def verify() -> dict[str, Any]:
    bound = {name: fact(name) for name in FACTS}
    manifest = json.loads((ROOT / "authority/wikiversity/unit-29/UNIT_AUTHORITY_MANIFEST.json").read_text(encoding="utf-8"))
    exercise_map = json.loads((ROOT / "authority/wikiversity/unit-29/ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    closure = json.loads((ROOT / "authority/ASSET_CLOSURE-unit-29.json").read_text(encoding="utf-8"))
    authority_qa = json.loads((ROOT / "qa/UNIT_29_AUTHORITY_QA.json").read_text(encoding="utf-8"))
    baseline = json.loads((ROOT / "qa/UNITS_01_28_MACHINE_QA.json").read_text(encoding="utf-8"))

    require(authority_qa["status"] == "PASS", "authority QA")
    require(manifest["final_live_identity_replay"]["result"] == "PASS", "live authority replay")
    require(manifest["final_live_identity_replay"]["semantic_unique_identity_count"] == 150, "semantic identity union")
    require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 106, "lecture closure")
    require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 61, "worksheet closure")
    require(authority_qa["authority"]["solution_closures_with_root"] == {"2": 17, "3": 8}, "solution closures")
    require(authority_qa["media"]["positions"] == 2 and authority_qa["media"]["assets"] == 2, "authority media topology")

    lecture = (SOURCE / "lecture-29.md").read_text(encoding="utf-8")
    worksheet = (SOURCE / "worksheet-29.md").read_text(encoding="utf-8")
    solutions = (SOURCE / "worksheet-29-solutions.md").read_text(encoding="utf-8")
    credits = (SOURCE / "media-credits-unit-29.md").read_text(encoding="utf-8")
    frontmatter = (SOURCE / "frontmatter-units-01-29.md").read_text(encoding="utf-8")
    unit_texts = [lecture, worksheet, solutions, credits]

    for name, raw in zip(("lecture", "worksheet", "solutions", "credits"), unit_texts, strict=True):
        require(MODEL in raw, f"provenance missing: {name}")
        require(not any(mark in raw for mark in ("\u2013", "\u2014", "\u2011")), f"Unicode dash: {name}")
        require(not re.search(r"(?i)\b(TODO|TBD|FIXME|LOREM|UNBOUND_PENDING|TO_BE_BOUND)\b", raw), f"placeholder: {name}")
        require(not re.search(r"(?i)(ghp_[A-Za-z0-9]{20,}|api[_-]?key\s*[:=]|bearer\s+[A-Za-z0-9._-]{20,})", raw), f"secret-like text: {name}")
        require(not any(unicodedata.category(ch) == "Cf" for ch in raw), f"invisible control: {name}")

    require("translation_status: complete" in lecture + worksheet + solutions, "translation status")
    require(r"K\!-\!\operatorname{Spek}(R)" in lecture and r"K\!-!\operatorname" not in lecture, "affine spectrum TeX")
    require(r"\varphi:D\longrightarrow\mathbb P_K^1" in lecture and r"\mathbb P^1" not in lecture, "projective-line field normalization")
    require("pembenaman dengan koordinat tertukar" in lecture, "natural swapped-coordinate wording")
    require(re.search(r"tempat\s+\$g/h\$ tidak bernilai nol dan tidak mempunyai kutub", lecture), "rational-function zero/pole repair")
    require("pangkat $t$ yang sesuai" in lecture and "tidak mempunyai pembagi" in lecture, "homogenization/gcd precision")
    require(r"V_+\bigl(YZ^{d-1}-\widehat F(X,Z)\bigr)" in lecture, "projective graph locus")
    require(r"V_+\bigl(X^dZ^{e-d}-Y^e\bigr)" in lecture, "projective monomial locus")
    require("AGC-U29-SRC-001 / AGC-CORR-0126" in lecture, "undefined degree disclosure")
    require(all(correction in lecture for correction in CORRECTION_IDS), "correction disclosures")
    require("AGC-U29-SRC-002" in worksheet and "tidak menebak matriks" in worksheet, "blank projection-matrix disclosure")

    expected_lecture_entities = [
        "Projektiver Raum/Projektion weg von einem Punkt/Definition",
        "Ebene projektive Kurve/Abbildung nach P^1 über Projektion von einem Punkt/Fakt",
        "Glatte projektive Kurven/Rationale Funktion als Morphismus nach P^1/Fakt",
        "Projektive Gerade/Rationale Funktion/z nach 1/z/Beispiel",
        "Rationale Kurvenparametrisierung/Fortsetzung auf projektive Gerade/Fakt",
        "Ebene projektive Kurve/Graph eines Polynoms in einer Variable/Singularität im Unendlichen/Fakt",
        "Ebene projektive Kurve/Graph einer rationalen Funktion in einer Variable/Singularität im Unendlichen/Fakt",
        "Ebene projektive monomiale Kurve/Singularität/Gesamtmultiplizität/Fakt",
    ]
    lecture_entities = re.findall(r"<!-- upstream_entity: (.*?) -->", lecture)
    worksheet_entities = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    require(lecture_entities == expected_lecture_entities, "lecture entity topology/order")
    require(worksheet_entities == [row["exercise_title"] for row in exercise_map["entries"]], "worksheet authority order")

    require(exercise_map["exercise_count"] == 10 and exercise_map["solution_count"] == 2, "exercise/solution topology")
    roles = exercise_map["ordered_role_point_and_star_topology"]
    require(roles["warm_up_numbers"] == [1, 2, 3, 4, 5], "warm-up topology")
    require(roles["submitted_numbers"] == [6, 7, 8, 9, 10], "submitted topology")
    require(roles["starred_numbers"] == [2, 3] and roles["upload_numbers"] == [], "star/upload topology")
    require(roles["authored_points"] == {"1": 2, "2": 4, "3": 3, "4": 3, "5": 4, "6": 3, "7": 3, "8": 3, "9": 3, "10": 5}, "authored points")
    require(roles["displayed_points"] == {"6": 3, "7": 3, "8": 3, "9": 3, "10": 5}, "displayed points")
    require(roles["submitted_displayed_point_total"] == 17, "submitted point total")
    require([int(value) for value in re.findall(r"(?m)^### Soal 29\.(\d+)", worksheet)] == list(range(1, 11)), "reader exercise order")
    require(re.findall(r"(?m)^### Soal 29\.(\d+) \((\d+) poin\)", worksheet) == [("6", "3"), ("7", "3"), ("8", "3"), ("9", "3"), ("10", "5")], "reader displayed points")
    require(re.findall(r"(?m)^### Soal 29\.(\d+) \*", worksheet) == ["2", "3"], "reader stars")
    require("public_solution_count: 2" in solutions and "negative_public_solution_count: 8" in solutions, "solution closure metadata")
    require(re.findall(r"(?m)^## Solusi Soal 29\.(\d+)", solutions) == ["2", "3"], "public solution topology")
    require(re.search(r"Tidak ada solusi tambahan yang\s+dibuat", solutions), "no invented solutions")

    protected_lecture = [
        r"\mathbb P_K^n\setminus\{(1,0,\ldots,0)\}",
        r"D=C\cap D_+(Z)\cong K\!-\!\operatorname{Spek}(R)",
        r"q=\frac gh\in Q(R)",
        r"\varphi:D\longrightarrow\mathbb P_K^1",
        r"H:\mathbb P_K^1&\longrightarrow\mathbb P_K^2",
        r"V_+\bigl(YZ^{d-1}-\widehat F(X,Z)\bigr)",
        r"V_+\bigl(X^dZ^{e-d}-Y^e\bigr)",
    ]
    protected_worksheet = [
        r"C=V(X^2+Y^2-1)",
        r"D=V(X^3-2Y^2+3)",
        r"ZX^2=Y^3",
        r"V(X^3+3X^2-Y^2)",
        r"\begin{pmatrix}",
        r"\end{pmatrix}",
        r"V_+\!\left((X^2+Y^2)^2-Z^2X^2+Z^2Y^2\right)",
    ]
    protected_solutions = [
        r"X^2+Y^2-Z^2=0",
        r"X^2+Y^2=0",
        r"P\in\mathbb A_K^1=D_+(L)\subset\mathbb P_K^1",
        r"K[X]_{(X)}",
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
    require(all(term_id in term_rows for term_id in TERM_IDS), "Unit 29 terms absent")
    require(all(correction_id in correction_rows for correction_id in CORRECTION_IDS), "Unit 29 corrections absent")
    require(term_rows["AGT-0261"]["preferred_target"] == "proyeksi dari sebuah titik", "projection terminology")
    require(term_rows["AGT-0262"]["preferred_target"] == "bundel garis", "line-family terminology")
    require(term_rows["AGT-0264"]["preferred_target"] == "kurva proyektif monomial", "monomial terminology")
    human = strip_nonprose(lecture + "\n" + worksheet + "\n" + solutions + "\n" + credits)
    require(not re.search(r"(?i)\bprojektif\b", human), "nonpreferred projektif residue")
    require(not re.search(r"(?i)\b(es sei|zeige|beweis|aufgabe|projektive gerade|glatte projektive)\b", human), "visible German residue")

    expected_ast = {
        "lecture-29.md": (19, 229, 0),
        "worksheet-29.md": (13, 38, 2),
        "worksheet-29-solutions.md": (3, 27, 0),
        "media-credits-unit-29.md": (1, 0, 0),
        "frontmatter-units-01-29.md": (2, 0, 0),
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
        if name != "frontmatter-units-01-29.md":
            unit_ids.extend(ids)
        ast_receipts[name] = {
            "headers": len(headers),
            "math_nodes": len(maths),
            "images": len(images),
            "stable_header_ids": len(ids),
            "pandoc_warnings": 0,
        }
    require(len(unit_ids) == 36 and len(unit_ids) == len(set(unit_ids)), "Unit 29 global IDs")
    require(sum(ast_receipts[name]["math_nodes"] for name in ("lecture-29.md", "worksheet-29.md", "worksheet-29-solutions.md")) == 294, "Unit 29 math total")

    image_rows = re.findall(r"!\[([^\]]+)\]\((authority/assets/[^)]+)\)", worksheet)
    require([path for _, path in image_rows] == ["authority/assets/Lemniscate_of_Bernoulli.svg", "authority/assets/Tschirnhausen_cubic-500.png"], "reader image order")
    require(all(alt.strip() for alt, _ in image_rows), "image alt text")
    closure_assets = {item["local_path"]: item for item in closure["assets"]}
    for _, relative in image_rows:
        require(relative in closure_assets, f"unbound reader image: {relative}")
        path = ROOT / relative
        item = closure_assets[relative]
        require(path.is_file() and path.stat().st_size == item["local_bytes"] and digest(path) == item["local_sha256"], f"reader image drift: {relative}")
    tsch = closure_assets["authority/assets/Tschirnhausen_cubic-500.png"]
    require(tsch["selected_form"] == "thumbnail_500px" and tsch["original_locally_archived"] is False, "Tschirnhausen fallback semantics")
    require(tsch["original_bytes"] == 64767 and tsch["original_sha1"] == "44a9bbaa597b2fce69ca491335199890546cfb3d", "Tschirnhausen original metadata")
    normalized_credits = re.sub(r"\s+", " ", credits)
    require("HTTP 429" in credits and "thumbnail resmi Commons" in normalized_credits, "thumbnail fallback disclosure")
    require("83.502 byte" in normalized_credits and tsch["local_sha256"] in credits, "selected asset identity")
    require("64.767 byte" in normalized_credits and tsch["original_sha1"] in credits, "unarchived original identity")
    require("tidak diarsipkan secara lokal" in normalized_credits, "no false original archive claim")
    require("domain publik" in credits and "CC BY-SA 2.0 Germany" in credits and "CC BY-SA 4.0" in credits, "mixed rights disclosure")
    require("tidak membuat klaim pelisensian payung" in normalized_credits, "no blanket relicensing")
    require("bukan kurva itu" in normalized_credits, "Tschirnhausen identification warning")

    cumulative_exercises = 0
    cumulative_solutions = 0
    for number in range(1, 30):
        suffix = f"{number:02d}"
        worksheet_text = (SOURCE / f"worksheet-{suffix}.md").read_text(encoding="utf-8")
        solution_text = (SOURCE / f"worksheet-{suffix}-solutions.md").read_text(encoding="utf-8")
        cumulative_exercises += len(re.findall(r"(?m)^### Soal \d+\.\d+", worksheet_text))
        cumulative_solutions += len(re.findall(r"(?m)^## Solusi Soal ", solution_text))
    require(baseline["status"] == "PASS", "Unit 28 baseline status")
    require(baseline["coverage"] == {
        "lectures": 28,
        "worksheets": 28,
        "exercises": 671,
        "public_source_solutions": 118,
        "reader_media_positions": 98,
        "stable_source_ids": 1483,
        "mathml_nodes": 10717,
    }, "Unit 28 coverage baseline")
    require((cumulative_exercises, cumulative_solutions, 98 + len(image_rows)) == (681, 120, 100), "cumulative source counts")
    flat_front = re.sub(r"\s+", " ", frontmatter)
    require("Unit 1-29 memuat 681 soal" in flat_front and "semua 120 solusi publik" in flat_front, "frontmatter coverage")
    require("Unit 1-23 mengikat revisi beku" in flat_front and "Unit 24-29 mengikat kuliah dan lembar kerja" in flat_front, "edition split")
    require(MANIFEST_SHA in frontmatter and MODEL in frontmatter, "frontmatter manifest/provenance")
    require("tidak menyiratkan dukungan" in flat_front and "bukan klaim lisensi payung" in flat_front, "frontmatter rights/nonendorsement")

    return {
        "bound_facts": bound,
        "authority": {
            "lecture_root_plus_dependencies": 107,
            "worksheet_root_plus_dependencies": 62,
            "solution_root_plus_dependencies": {"2": 17, "3": 8},
            "semantic_live_union": 150,
        },
        "translation": {
            "lecture_semantic_entities": 8,
            "worksheet_exercises": 10,
            "public_solutions": 2,
            "negative_solution_candidates": 8,
            "stable_ids": 36,
            "math_nodes": 294,
            "reader_media_positions": 2,
            "visible_correction_disclosures": 4,
            "source_defect_disclosures": 2,
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
            "lectures": 29,
            "worksheets": 29,
            "exercises": 681,
            "public_solutions": 120,
            "media_positions": 100,
        },
        "rights": {
            "public_domain_media": 2,
            "tschirnhausen_original_locally_archived": False,
            "tschirnhausen_selected_form": "official_500px_thumbnail",
            "blanket_relicense_claim": False,
        },
        "revision_contributors": {
            "lecture_root": "Bocardodarapti",
            "worksheet_root": "Arbota",
            "solution_2": "Arbota",
            "solution_3": "Arbota",
        },
    }


def main() -> int:
    receipt = {
        "schema": "ag-bridge-unit-translation-qa-v1",
        "status": "PASS",
        "unit": 29,
        "verified_date": "2026-08-28",
        **verify(),
        "provenance": MODEL + ".",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "status": "PASS",
        "unit": 29,
        "receipt": OUT.relative_to(ROOT).as_posix(),
        "bytes": OUT.stat().st_size,
        "sha256": digest(OUT),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
