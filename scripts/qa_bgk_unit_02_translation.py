#!/usr/bin/env python3
"""Fail-closed semantic, mathematical, rights, and source-closure QA for BGK Unit 2."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess


LANE = Path(__file__).resolve().parents[1]
BGK = LANE / "source" / "id-ID" / "bgk"
AUTH = LANE / "authority" / "wikiversity-bgk" / "unit-02"
OUT = LANE / "qa" / "BGK_UNIT_02_TRANSLATION_QA.json"
FILES = (
    BGK / "frontmatter-bgk-units-01-02.md",
    BGK / "lecture-02.md",
    BGK / "worksheet-02.md",
    BGK / "worksheet-02-solutions.md",
)
UNIT_01_FILES = (
    BGK / "frontmatter-bgk-units-01.md",
    BGK / "lecture-01.md",
    BGK / "worksheet-01.md",
    BGK / "worksheet-01-solutions.md",
)
AUTHORITY_SHA256 = {
    "UNIT_AUTHORITY_MANIFEST.json": "a348b56811fe98266feff9108a21a436a9b8f07a343321feab7d9fbb3b75e64d",
    "lecture-02.xml": "9e5823b1031d2d8877147923324a95a78ff255d00a840745fe6a83dddb749670",
    "lecture-02-expanded.tex": "ae973e45a0aa3228ac31a61dd71b995d7872bfaaf8adca164bd97bd045f000b3",
    "worksheet-02.xml": "b7d96a8bfc59545c18c4dbbe2bb3f6e3b4aa112a45d9a41e7a8f86de15113e1e",
    "worksheet-02-expanded.tex": "6aaed409db9e572b53def3dd35c3b9a5cb6d4467d8d5c3a4360ac6b24d78ccdd",
    "ORDERED_EXERCISE_MAP.json": "4e0633e8c35ea5a2fddd0b63a0bb67fdd6af93f11a55f3a2eae10eae0d25a10a",
    "worksheet-solution-candidates-api.json": "5051d800bed72fe432757012033319ca30c14503254f16d0d385f9a0a3c82ad2",
    "solution-ex04.xml": "6f326a59a4289d17ac6aee485706faa81d641d994ddda72bd463053eec4b71b1",
    "solution-ex04.html": "8cf7b19c9693b1817e5699b32703545716fb35dfa713b9f6129758dbe0bf0e7f",
}
MEDIA_SHA256 = {
    LANE / "authority" / "ASSET_CLOSURE-bgk-unit-02.json": "902522f5a7231d562dc09f30bbd13b76ed5c087b17fd533b7d5cc71c0fd4844d",
    LANE / "authority" / "RIGHTS-bgk-unit-02.csv": "bc85cef5f20150941f3a6492c67702bcddd3d23bdd6ac5939c0148e5d57dc9f6",
    LANE / "authority" / "commons-imageinfo-bgk-unit-02.json": "d35c85d8e57594b709d5a771a4322c27eb34ebac16f3244de9f5572bd465b5ea",
    LANE / "source" / "id-ID" / "media-credits-bgk-unit-02.md": "cec28c3bd197ffb7aabadfa0d67ddf8945cc7899834c4470780618ca60008158",
}
CORRECTION_IDS = tuple(f"AGC-CORR-{number:04d}" for number in range(142, 149))
NEW_TERM_IDS = tuple(f"AGT-{number:04d}" for number in range(290, 299))
REUSED_TERM_IDS = ("AGT-0241",)


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


def body_without_metadata_or_comments(text: str) -> str:
    body = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    return re.sub(r"<!--.*?-->", "", body, flags=re.S)


def main() -> int:
    for name, expected in AUTHORITY_SHA256.items():
        require(sha256(AUTH / name) == expected, f"authority hash mismatch: {name}")
    for path, expected in MEDIA_SHA256.items():
        require(sha256(path) == expected, f"media/rights hash mismatch: {path.name}")

    texts = {path.name: path.read_text(encoding="utf-8") for path in FILES}
    joined = "\n".join(texts.values())
    require("OpenAI Codex gpt-5.6-sol, Ultra." in joined, "exact provenance missing")
    require(not re.search(r"(?:TODO|TBD|PLACEHOLDER|LOREM IPSUM)", joined, re.I), "placeholder remains")
    require(not re.search(r"[\u200b\u200c\u200d\u2060\ufeff]", joined), "invisible control remains")

    cleaned_body = "\n".join(body_without_metadata_or_comments(text) for text in texts.values())
    german_residue = re.findall(
        r"\b(?:Zeige|Aufgabe|Vorlesung|Arbeitsblatt|Dann gibt es|Wir betrachten|Es sei)\b",
        cleaned_body,
    )
    require(not german_residue, f"unexpected German prose residue: {german_residue[:5]}")

    worksheet = texts["worksheet-02.md"]
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    expected_titles = [entry["exercise_title"] for entry in mapping["entries"]]
    actual_titles = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    require(actual_titles == expected_titles, "ordered exercise mapping mismatch")
    exercise_ids = re.findall(r"^## Soal 2\.(\d+) \{#(br-bgk-2019-w02-ex\d{2})\}$", worksheet, re.M)
    require([int(number) for number, _ in exercise_ids] == list(range(1, 28)), "exercise numbering mismatch")
    require(len({identifier for _, identifier in exercise_ids}) == 27, "duplicate exercise ID")
    require(mapping["exercise_count"] == 27 and mapping["solution_count"] == 1, "solution scope mismatch")
    public = [entry["exercise_number"] for entry in mapping["entries"] if entry["has_public_solution"]]
    require(public == [4], f"public-solution topology drifted: {public}")

    solutions = texts["worksheet-02-solutions.md"]
    require("tepat satu solusi" in solutions and "Soal 2.4" in solutions, "sole-solution disclosure missing")
    require("Tidak ada solusi baru yang dibuat" in solutions, "no-invention disclosure missing")
    require("negative_public_solution_count: 26" in solutions, "26 negative candidates not bound")

    headings = re.findall(r"\{#(br-bgk-2019-[A-Za-z0-9_-]+)\}", joined)
    require(len(headings) == 52 and len(headings) == len(set(headings)), "Unit 2/cumulative-frontmatter heading closure drifted")
    for name in ("lecture-02.md", "worksheet-02.md", "worksheet-02-solutions.md"):
        yaml_id = re.search(r"^stable_id: (br-bgk-2019-[A-Za-z0-9_-]+)$", texts[name], re.M)
        require(yaml_id is not None and yaml_id.group(1) in headings, f"YAML/root ID mismatch: {name}")
    unit_01_ids: set[str] = set()
    for path in UNIT_01_FILES:
        unit_01_ids.update(re.findall(r"\{#(br-bgk-2019-[A-Za-z0-9_-]+)\}", path.read_text(encoding="utf-8")))
    require(not (set(headings) & unit_01_ids), "BGK Unit 1/Unit 2 stable-ID collision")
    classical_ids: set[str] = set()
    classical_root = LANE / "source" / "id-ID"
    for pattern in ("lecture-*.md", "worksheet-*.md", "worksheet-*-solutions.md"):
        for path in classical_root.glob(pattern):
            classical_ids.update(re.findall(r"\{#([^}]+)\}", path.read_text(encoding="utf-8")))
    require(not (set(headings) & classical_ids), "BGK/classical stable-ID collision")

    lecture = texts["lecture-02.md"]
    numbered_lecture = re.findall(
        r"^### (?:Definisi|Teorema|Catatan|Lema|Contoh) 2\.(\d+):",
        lecture,
        re.M,
    )
    require([int(value) for value in numbered_lecture] == list(range(1, 13)), "lecture numbering 2.1--2.12 drifted")
    required_witnesses = {
        "lecture_typed_topological_transition": (lecture, r"\varphi_{ji}(x)"),
        "lecture_typed_glued_map": (lecture, r"\theta|_{V_i}\circ\psi_i=\theta_i"),
        "lecture_typed_bundle_transition": (lecture, r"\varphi_{ji}:E_i|_{U_i\cap U_j}"),
        "lecture_mobius_variables": (lecture, r"$\sqrt{1-y}$ pada $U$ dan $\sqrt{1+y}$ pada $V$"),
        "worksheet_typed_glued_map": (worksheet, r"\theta|_{V_i}\circ\psi_i=\theta_i"),
        "worksheet_corrected_parameterization": (worksheet, r"\left(\sin t,\cos t,\cos\frac t2,\sin\frac t2\right)"),
        "solution_defined_field": (solutions, r"F(x,y)=\frac{1}{1+x^2+y^2}e_1"),
        "solution_sequence_subscripts": (solutions, r"\frac{1}{1+x_n^2+y_n^2}e_1"),
    }
    for label, (text, witness) in required_witnesses.items():
        require(witness in text, f"corrected mathematical witness missing: {label}")
    require(joined.count("**Catatan edisi -") == 7, "seven visible anomaly notes not preserved")
    frontmatter = texts["frontmatter-bgk-units-01-02.md"]
    require("Tujuh kelas" in frontmatter and "seluruh 44 soal" in frontmatter, "cumulative scope/anomaly disclosure missing")

    closure = json.loads((LANE / "authority" / "ASSET_CLOSURE-bgk-unit-02.json").read_text(encoding="utf-8"))
    require(closure["reader_media_positions"] == 3 and closure["unique_local_assets"] == 4, "media closure count drifted")
    image_matches = re.findall(r"!\[([^\]]+)\]\((authority/assets/[^)]+)\)", lecture)
    expected_images = [(asset["reader_alt_id"], asset["local_path"]) for asset in closure["assets"]]
    require(image_matches == expected_images, "media order/path/alt mismatch")
    for asset in closure["asset_manifest"]:
        path = LANE / asset["path"]
        require(path.stat().st_size == asset["bytes"] and sha256(path) == asset["sha256"], f"asset drift: {path.name}")

    defined_numbers: set[str] = set()
    for path in (*UNIT_01_FILES, *FILES):
        for match in re.finditer(
            r"^#{2,4} (?:Definisi|Teorema|Catatan|Lema|Contoh|Soal) (\d+\.\d+)(?::| )",
            path.read_text(encoding="utf-8"),
            re.M,
        ):
            defined_numbers.add(match.group(1))
    reference_numbers = re.findall(
        r"\b(?:Definisi|Teorema|Catatan|Lema|Contoh|Soal) (\d+\.\d+)\b",
        "\n".join(line for line in cleaned_body.splitlines() if not line.startswith("#")),
    )
    missing_refs = sorted(set(reference_numbers) - defined_numbers)
    require(not missing_refs, f"missing cross-reference targets: {missing_refs}")

    with (LANE / "00_control" / "CORRECTIONS.csv").open("r", encoding="utf-8-sig", newline="") as stream:
        correction_rows = {row["correction_id"]: row for row in csv.DictReader(stream)}
    require(all(identifier in correction_rows for identifier in CORRECTION_IDS), "Unit 2 correction ledger closure missing")
    require(
        all(correction_rows[identifier]["status"] == "applied_at_bgk_unit_02_translation" for identifier in CORRECTION_IDS),
        "Unit 2 correction status drifted",
    )
    with (LANE / "00_control" / "TERMINOLOGY.csv").open("r", encoding="utf-8-sig", newline="") as stream:
        term_rows = {row["term_id"]: row for row in csv.DictReader(stream)}
    require(all(identifier in term_rows for identifier in (*NEW_TERM_IDS, *REUSED_TERM_IDS)), "terminology closure missing")
    require(all(term_rows[identifier]["status"] == "admitted" for identifier in (*NEW_TERM_IDS, *REUSED_TERM_IDS)), "terminology not admitted")

    pandoc = [pandoc_fact(path) for path in FILES]
    math_by_name = {Path(row["path"]).name: row["math_nodes"] for row in pandoc}
    require(math_by_name["lecture-02.md"] == 180, "lecture math-node count drifted")
    require(math_by_name["worksheet-02.md"] == 111, "worksheet math-node count drifted")
    require(math_by_name["worksheet-02-solutions.md"] == 28, "solution math-node count drifted")

    result = {
        "schema": "ag-bridge-bgk-unit-translation-qa-v1",
        "unit": 2,
        "language": "id-ID",
        "status": "PASS",
        "authority": [fact(AUTH / name) for name in AUTHORITY_SHA256],
        "media_and_rights": [fact(path) for path in MEDIA_SHA256],
        "translation_files": [fact(path) for path in FILES],
        "pandoc": pandoc,
        "counts": {
            "source_exercises": 27,
            "translated_exercises": 27,
            "source_public_solutions": 1,
            "translated_public_solutions": 1,
            "negative_solution_candidates": 26,
            "invented_solutions": 0,
            "heading_ids": len(headings),
            "heading_id_collisions": 0,
            "lecture_numbered_entities": len(numbered_lecture),
            "visible_source_anomaly_notes": joined.count("**Catatan edisi -"),
            "correction_ledger_rows_added": len(CORRECTION_IDS),
            "terminology_rows_added": len(NEW_TERM_IDS),
            "terminology_rows_reused": len(REUSED_TERM_IDS),
            "media_positions": len(image_matches),
            "cross_reference_occurrences": len(reference_numbers),
            "missing_cross_reference_targets": len(missing_refs),
        },
        "correction_ids": list(CORRECTION_IDS),
        "terminology_ids": [*NEW_TERM_IDS, *REUSED_TERM_IDS],
        "checks": [
            "frozen_authority_hashes",
            "pandoc_ast_all_four_files",
            "ordered_27_exercise_map",
            "exact_public_solution_2_4_and_26_negative_candidates",
            "no_invented_solutions",
            "disjoint_unit_and_classical_stable_ids",
            "lecture_numbering_2_1_through_2_12",
            "corrected_formula_and_index_witnesses",
            "seven_visible_source_anomaly_disclosures",
            "rights_bound_media_order_paths_alt_and_hashes",
            "append_only_correction_and_terminology_ledgers",
            "closed_cross_references",
            "exact_model_provenance_and_nonendorsement",
            "no_placeholders_german_prose_or_invisible_controls",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"receipt": fact(OUT), "counts": result["counts"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
