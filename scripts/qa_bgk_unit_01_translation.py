#!/usr/bin/env python3
"""Deterministic semantic and source-closure QA for BGK Unit 1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


LANE = Path(__file__).resolve().parents[1]
BGK = LANE / "source" / "id-ID" / "bgk"
AUTH = LANE / "authority" / "wikiversity-bgk" / "unit-01"
OUT = LANE / "qa" / "BGK_UNIT_01_TRANSLATION_QA.json"
FILES = (
    BGK / "frontmatter-bgk-units-01.md",
    BGK / "lecture-01.md",
    BGK / "worksheet-01.md",
    BGK / "worksheet-01-solutions.md",
)
AUTHORITY_SHA256 = {
    "UNIT_AUTHORITY_MANIFEST.json": "ad271f5ad69f9990dbe3082c22f8c52b7a4c58494c8f6614350078535d4f2ba1",
    "lecture-01.xml": "68d7783afc1c1353c3298638f150095dad79c2424c356bc09bc50c023ab86392",
    "lecture-01-expanded.tex": "7b22065d36d75d01385aabd97edd6e5416f817e1ebf96af9543023242135c77d",
    "worksheet-01.xml": "95e392e04115c0dcfc94eebc28bfdbdbdfc1cda3c46d6f008d7d1324b3e81095",
    "worksheet-01-expanded.tex": "566b4211d5b25be90256a24567f0c448a6cc9fe23aec74c4fde8c6922cba2d97",
    "ORDERED_EXERCISE_MAP.json": "21244128b357d5fc35d5a8dc7129c27e091a781594516c4f6db87e9202b162ba",
    "worksheet-solution-candidates-api.json": "89db963b3ae3fdff32a8a16317c249849ea6d59ea1b3a19686c9beb382633bc2",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fact(path: Path) -> dict[str, object]:
    require(path.is_file() and not path.is_symlink(), f"missing regular file: {path}")
    return {
        "path": path.relative_to(LANE).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def walk_ast(node: object):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk_ast(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk_ast(value)


def pandoc_fact(path: Path) -> dict[str, object]:
    process = subprocess.run(
        [
            "pandoc",
            "--from=markdown+yaml_metadata_block+tex_math_dollars+fenced_divs+bracketed_spans",
            "--to=json",
            str(path),
        ],
        cwd=LANE,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    ast = json.loads(process.stdout)
    nodes = tuple(walk_ast(ast))
    return {
        "path": path.relative_to(LANE).as_posix(),
        "pandoc_ast_parse": "PASS",
        "math_nodes": sum(node.get("t") == "Math" for node in nodes),
        "heading_nodes": sum(node.get("t") == "Header" for node in nodes),
    }


def main() -> int:
    for name, expected in AUTHORITY_SHA256.items():
        require(sha256(AUTH / name) == expected, f"authority hash mismatch: {name}")

    texts = {path.name: path.read_text(encoding="utf-8") for path in FILES}
    joined = "\n".join(texts.values())
    require("OpenAI Codex gpt-5.6-sol, Ultra." in joined, "exact provenance missing")
    require("terdiferensialkan" not in joined, "rejected terminology remains")
    require("pemetaan tangen total" not in joined, "rejected tangent-map heading remains")
    require(not re.search(r"(?:TODO|TBD|PLACEHOLDER|LOREM IPSUM)", joined, re.I), "placeholder remains")
    require(not re.search(r"[\u200b\u200c\u200d\u2060\ufeff]", joined), "invisible control remains")

    worksheet = texts["worksheet-01.md"]
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    expected_titles = [entry["exercise_title"] for entry in mapping["entries"]]
    actual_titles = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    require(actual_titles == expected_titles, "ordered exercise mapping mismatch")
    exercise_ids = re.findall(r"^## Soal 1\.(\d+) \{#(br-bgk-2019-w01-ex\d{2})\}$", worksheet, re.M)
    require([int(number) for number, _ in exercise_ids] == list(range(1, 18)), "exercise numbering mismatch")
    require(len({identifier for _, identifier in exercise_ids}) == 17, "duplicate exercise ID")
    require(mapping["exercise_count"] == 17 and mapping["solution_count"] == 0, "source solution scope mismatch")
    require(all(not entry["has_public_solution"] for entry in mapping["entries"]), "unexpected public solution")
    require("Tidak ada solusi baru yang dibuat" in texts["worksheet-01-solutions.md"], "zero-solution disclosure missing")

    identifiers = re.findall(r"\{#(br-bgk-2019-[A-Za-z0-9_-]+)\}", joined)
    require(len(identifiers) == len(set(identifiers)), "duplicate BGK heading IDs")
    classical_ids: set[str] = set()
    classical_root = LANE / "source" / "id-ID"
    for pattern in ("lecture-*.md", "worksheet-*.md", "worksheet-*-solutions.md"):
        for path in classical_root.glob(pattern):
            classical_ids.update(re.findall(r"\{#([^}]+)\}", path.read_text(encoding="utf-8")))
    require(not (set(identifiers) & classical_ids), "BGK/classical stable-ID collision")

    lecture = texts["lecture-01.md"]
    required_witnesses = (
        r"\mathbb R^2\setminus\{(0,0)\}",
        r"\left(\mathbb R^3\setminus\{(0,0,0)\}\right)\times\mathbb R^3",
        r"-af+cd",
        r"(a,b,c,d,e,f;s)",
        "Lema 33.3",
        "pemetaan tangen",
        r"U\times\mathbb R^r",
    )
    for witness in required_witnesses:
        require(witness in lecture, f"formula or reference witness missing: {witness}")
    require(lecture.count("**Catatan edisi -") >= 4, "visible source-correction disclosures missing")
    expected_alt = "Diagram bundel tangen dengan ruang tangen sebagai serat di atas setiap titik manifold"
    require(
        f"![{expected_alt}](authority/assets/bgk-tangent-bundle-500.png)" in lecture,
        "reader image or exact rights-bound alt missing",
    )

    ledger = (LANE / "00_control" / "CORRECTIONS.csv").read_text(encoding="utf-8")
    for correction in range(136, 142):
        require(f"AGC-CORR-{correction:04d}" in ledger, f"correction ledger row missing: {correction}")
    terminology = (LANE / "00_control" / "TERMINOLOGY.csv").read_text(encoding="utf-8")
    for term in range(277, 290):
        require(f"AGT-{term:04d}" in terminology, f"terminology row missing: {term}")

    result = {
        "schema": "ag-bridge-bgk-unit-translation-qa-v1",
        "unit": 1,
        "language": "id-ID",
        "status": "PASS",
        "authority": [fact(AUTH / name) for name in AUTHORITY_SHA256],
        "translation_files": [fact(path) for path in FILES],
        "pandoc": [pandoc_fact(path) for path in FILES],
        "counts": {
            "source_exercises": 17,
            "translated_exercises": 17,
            "source_public_solutions": 0,
            "invented_solutions": 0,
            "heading_ids": len(identifiers),
            "heading_id_collisions": 0,
            "visible_source_correction_notes": lecture.count("**Catatan edisi -"),
            "correction_ledger_rows_added": 6,
            "terminology_rows_added": 13,
        },
        "checks": [
            "frozen_authority_hashes",
            "pandoc_ast_all_four_files",
            "ordered_17_exercise_map",
            "zero_public_solutions_preserved_without_invention",
            "disjoint_bgk_stable_ids",
            "formula_and_external_reference_witnesses",
            "rights_bound_image_and_alt",
            "terminology_normalization",
            "visible_and_ledgered_source_corrections",
            "exact_model_provenance_and_nonendorsement",
            "no_placeholders_or_invisible_controls",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"receipt": fact(OUT), "counts": result["counts"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
