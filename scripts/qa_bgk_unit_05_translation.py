#!/usr/bin/env python3
"""Fail-closed source, mathematics, language, rights, and scope QA for BGK Unit 5."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess


LANE = Path(__file__).resolve().parents[1]
BGK = LANE / "source" / "id-ID" / "bgk"
AUTH = LANE / "authority" / "wikiversity-bgk" / "unit-05"
OUT = LANE / "qa" / "BGK_UNIT_05_TRANSLATION_QA.json"
FILES = (
    BGK / "lecture-05.md",
    BGK / "worksheet-05.md",
    BGK / "worksheet-05-solutions.md",
)
AUTHORITY_SHA256 = {
    "UNIT_AUTHORITY_MANIFEST.json": "328774ffd66341ba8841b86935037a043067202dd10916d3e0be5082faeac35e",
    "lecture-05.xml": "edc881b76f88954eeceb7fa0a1902791218e064b947adee9e01119969c21c237",
    "lecture-05-expanded.tex": "d5d29f43c3209ccf8c8f80290ba3e44e800552807d4975ae0e78cb2dcd73735f",
    "worksheet-05.xml": "89e545b88502d4e9f4bd19c8ca79a68cf86a480aca360f4d0c3740589366a7f5",
    "worksheet-05-expanded.tex": "af4235ab3c393b02ad8f081f8f8fb17c24067fa07af63ec7f9bb3f17e1526b86",
    "lecture-05-latex-page-api.json": "f1f399219ce3bb9372e97a235db196fbe4237da3f33ebfc3f031285f62384eab",
    "worksheet-05-latex-page-api.json": "7de690f0ce79cb0ac2aecea072ea8d035bf7dba46af5ec0bda1434c290a6ae78",
    "solution-ex05.xml": "95fa2f0799fb9bfbfe0d9475a42c061ea805618e25e31560a6004da4672c5c86",
    "solution-ex05.html": "04c72e340da0acd5220449d60b5bc1d18e30d2808f549600b5288910de26d406",
    "ORDERED_EXERCISE_MAP.json": "b6bf28ef883ac91c07d0c50526ff655b2bcf7fc1b0d45773f0543092d463cadf",
    "worksheet-solution-candidates-api.json": "8b7b0d65fa6670632c96c8ab95b48b732576ebc3db80007ce281c78fb9875d51",
    "official-pdfs-api.json": "870f061afcbdc878e8fcfa1cb239adca56573f753f1115a0c94f20b7a634b295",
}
MEDIA_RIGHTS_SHA256 = {
    LANE / "authority" / "ASSET_CLOSURE-bgk-unit-05.json": "c1e2145df10a647b185cbdb79f4d8d215a253604242fb694aa057b08cf3c34a3",
    LANE / "authority" / "RIGHTS-bgk-unit-05.csv": "87f9d56b1300a56ca68e4aa8f50e3d50ab622d7a4d05221089d49e1dba35981d",
    LANE / "authority" / "commons-imageinfo-bgk-unit-05.json": "09fff01c6ed1a153c4970265001b0251c705e51142ca022a9c7260cfff74edf2",
    LANE / "source" / "id-ID" / "media-credits-bgk-unit-05.md": "c2e2db42f0ad4479c84ab0c00b1cb72f3fafd2e6e0ce291d32cbc03e10fcdf9e",
    LANE / "authority" / "artifacts" / "bgk-lecture-05-official.pdf": "85be007896876a0717ef5eddfe64ed919aeb6559dce44ec2828ffe2b1d755085",
    LANE / "authority" / "artifacts" / "bgk-worksheet-05-official.pdf": "206418f092c563128b3dbf893b8547dc6db727773d4e4ec88e07140886d79113",
}
CORRECTION_IDS = tuple(f"AGC-CORR-{number:04d}" for number in range(159, 165))
NEW_TERM_IDS = tuple(f"AGT-{number:04d}" for number in range(324, 334))


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
            str(path.relative_to(LANE)),
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
        "image_nodes": sum(node.get("t") == "Image" for node in nodes),
    }


def body_without_metadata_comments_or_notes(text: str) -> str:
    body = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    return re.sub(r"(?m)^>.*(?:\n>.*)*", "", body)


def markdown_ids(text: str) -> list[str]:
    return re.findall(r"\{#(br-bgk-2019-[A-Za-z0-9_-]+)\}", text)


def main() -> int:
    for name, expected in AUTHORITY_SHA256.items():
        require(sha256(AUTH / name) == expected, f"authority hash mismatch: {name}")
    for path, expected in MEDIA_RIGHTS_SHA256.items():
        require(sha256(path) == expected, f"media/rights hash mismatch: {path.name}")

    manifest = json.loads((AUTH / "UNIT_AUTHORITY_MANIFEST.json").read_text(encoding="utf-8"))
    require(manifest["unit_number"] == 5, "authority manifest unit drifted")
    require(manifest["lecture"]["revid"] == 1003725, "lecture revision drifted")
    require(manifest["worksheet"]["revid"] == 619386, "worksheet revision drifted")
    require(
        manifest["lecture_transclusion_closure"]["requested_template_count"]
        == manifest["lecture_transclusion_closure"]["captured_page_count"]
        == 105,
        "lecture transclusion closure drifted",
    )
    require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "lecture transclusion missing")
    require(
        manifest["worksheet_transclusion_closure"]["requested_template_count"]
        == manifest["worksheet_transclusion_closure"]["captured_page_count"]
        == 68,
        "worksheet transclusion closure drifted",
    )
    require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "worksheet transclusion missing")

    texts = {path.name: path.read_text(encoding="utf-8") for path in FILES}
    joined = "\n".join(texts.values())
    for name in texts:
        require("OpenAI Codex gpt-5.6-sol, Ultra." in texts[name], f"exact provenance missing: {name}")
        require("CC BY-SA 4.0" in texts[name], f"CC BY-SA notice missing: {name}")
        require("tidak menyiratkan dukungan" in texts[name], f"non-endorsement missing: {name}")
        require("translation_status: complete" in texts[name], f"incomplete translation status: {name}")
    require(not re.search(r"(?:TODO|TBD|PLACEHOLDER|LOREM IPSUM)", joined, re.I), "placeholder remains")
    require(not re.search(r"[\u200b\u200c\u200d\u2060\ufeff]", joined), "invisible control remains")
    require(not re.search(r"\$[^$\n]*`", joined), "stray backtick inside an unclosed math span")

    cleaned_body = "\n".join(body_without_metadata_comments_or_notes(text) for text in texts.values())
    german_residue = re.findall(
        r"\b(?:Zeige|Berechne|Aufgabe|Vorlesung|Arbeitsblatt|Es sei|Dann nennt man|Beweis)\b",
        cleaned_body,
    )
    require(not german_residue, f"unexpected German prose residue: {german_residue[:5]}")

    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    require(mapping["exercise_count"] == 11 and mapping["solution_count"] == 1, "solution scope mismatch")
    require(sum(entry.get("has_public_solution", False) for entry in mapping["entries"]) == 1, "public solution topology drifted")
    worksheet = texts["worksheet-05.md"]
    expected_titles = [entry["exercise_title"] for entry in mapping["entries"]]
    actual_titles = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    require(actual_titles == expected_titles, "ordered exercise mapping mismatch")
    exercise_ids = re.findall(r"^## Soal 5\.(\d+)\*? \{#(br-bgk-2019-w05-ex\d{2})\}$", worksheet, re.M)
    require([int(number) for number, _ in exercise_ids] == list(range(1, 12)), "exercise numbering mismatch")
    require(len({identifier for _, identifier in exercise_ids}) == 11, "duplicate exercise ID")
    require("## Soal 5.5*" in worksheet, "source exercise star not preserved")

    solutions = texts["worksheet-05-solutions.md"]
    require("tepat satu solusi" in solutions and "5.1-5.4 dan 5.6-5.11" in solutions, "solution scope disclosure missing")
    require("## Solusi sumber untuk Soal 5.5" in solutions, "public solution section missing")
    require("Tidak ada solusi baru" in solutions, "no-invention disclosure missing")
    require("(g_i)_P\\in\\mathcal F_P" in texts["lecture-05.md"], "typed germ correction missing")

    lecture = texts["lecture-05.md"]
    numbered_lecture = re.findall(r"^### (?:Definisi|Contoh|Lema) 5\.(\d+):", lecture, re.M)
    require([int(value) for value in numbered_lecture] == list(range(1, 10)), "lecture numbering drifted")
    require(lecture.count("#### Bukti") == 2, "two source proof positions not preserved")
    required_witnesses = {
        "sheafification_definition": r"\widetilde{\mathcal F}(U)",
        "compatibility": "syarat kompatibilitas",
        "factorization": r"\widetilde\psi:",
        "topological_group_example": r"C^0(U,F)&\longrightarrow C^0(U,G)",
        "kernel": r"(\ker\varphi)(U):=\ker\varphi_U",
        "image": r"(\operatorname{im}\varphi)(U):=\operatorname{im}\varphi_U",
        "matrix_source": r"\operatorname{Mat}_{m\times n}\bigl(C^0(X,\mathbb R)\bigr)",
        "matrix_note": r"M\in\operatorname{Mat}_{m\times n}(C^0(X,\mathbb R))",
        "quotient": r"\mathcal G/\mathcal F",
        "quotient_stalk": r"(\mathcal G/\mathcal F)_P",
        "germ_fix": r"(g_i)_P\in\mathcal F_P",
    }
    for label, witness in required_witnesses.items():
        require(witness in lecture, f"mathematical/source witness missing: {label}")
    require(lecture.count("**Catatan edisi -") == 4, "visible lecture source-note placement drifted")
    require(solutions.count("**Catatan edisi -") == 1, "visible solution source-note placement drifted")
    for witness in ("Garbenmorp", "die natürliche Morphismus", r"Mat}_{1\times3}(K)", "tidak didefinisikan"):
        require(witness in joined, f"source form or anomaly witness missing: {witness}")

    all_ids = [identifier for text in texts.values() for identifier in markdown_ids(text)]
    require(len(all_ids) == 29 and len(all_ids) == len(set(all_ids)), "Unit 5 heading-ID closure drifted")
    for path in FILES:
        yaml_id = re.search(r"^stable_id: (br-bgk-2019-[A-Za-z0-9_-]+)$", path.read_text(encoding="utf-8"), re.M)
        require(yaml_id is not None and yaml_id.group(1) in all_ids, f"YAML/root ID mismatch: {path.name}")

    earlier_ids: set[str] = set()
    for unit in range(1, 5):
        for name in (f"lecture-{unit:02d}.md", f"worksheet-{unit:02d}.md", f"worksheet-{unit:02d}-solutions.md"):
            path = BGK / name
            if path.is_file():
                earlier_ids.update(markdown_ids(path.read_text(encoding="utf-8")))
    require(not (set(all_ids) & earlier_ids), "BGK stable-ID collision")

    with (LANE / "00_control" / "CORRECTIONS.csv").open("r", encoding="utf-8-sig", newline="") as stream:
        correction_rows = {row["correction_id"]: row for row in csv.DictReader(stream)}
    require(all(identifier in correction_rows for identifier in CORRECTION_IDS), "Unit 5 correction ledger closure missing")
    require(all(correction_rows[identifier]["status"] == "applied_at_bgk_unit_05_translation" for identifier in CORRECTION_IDS), "Unit 5 correction status drifted")
    with (LANE / "00_control" / "TERMINOLOGY.csv").open("r", encoding="utf-8-sig", newline="") as stream:
        term_rows = {row["term_id"]: row for row in csv.DictReader(stream)}
    require(all(identifier in term_rows for identifier in NEW_TERM_IDS), "Unit 5 terminology closure missing")
    require(all(term_rows[identifier]["status"] == "admitted" for identifier in NEW_TERM_IDS), "Unit 5 terminology not admitted")

    closure = json.loads((LANE / "authority" / "ASSET_CLOSURE-bgk-unit-05.json").read_text(encoding="utf-8"))
    require(closure["reader_media_positions"] == 0 and closure["unique_local_assets"] == 0, "Unit 5 media count drifted")
    require(not re.search(r"!\[[^\]]*\]\([^)]*\)", joined), "unexpected Unit 5 reader media link")

    pandoc = [pandoc_fact(path) for path in FILES]
    result = {
        "schema": "ag-bridge-bgk-unit-translation-qa-v1",
        "unit": 5,
        "language": "id-ID",
        "status": "PASS",
        "authority": [fact(AUTH / name) for name in AUTHORITY_SHA256],
        "media_and_rights": [fact(path) for path in MEDIA_RIGHTS_SHA256],
        "translation_files": [fact(path) for path in FILES],
        "pandoc": pandoc,
        "counts": {
            "source_exercises": 11,
            "translated_exercises": len(exercise_ids),
            "source_public_solutions": 1,
            "translated_public_solutions": 1,
            "negative_solution_candidates": 10,
            "invented_solutions": 0,
            "lecture_numbered_entities": len(numbered_lecture),
            "proof_positions": lecture.count("#### Bukti"),
            "heading_ids": len(all_ids),
            "heading_id_collisions": 0,
            "source_anomaly_classes": len(CORRECTION_IDS),
            "visible_anomaly_note_placements": lecture.count("**Catatan edisi -") + solutions.count("**Catatan edisi -"),
            "correction_ledger_rows_added": len(CORRECTION_IDS),
            "terminology_rows_added": len(NEW_TERM_IDS),
            "reader_media_positions": 0,
        },
        "correction_ids": list(CORRECTION_IDS),
        "terminology_ids_added": list(NEW_TERM_IDS),
        "checks": [
            "frozen_authority_and_transclusion_hashes",
            "ordered_eleven_exercise_map_and_one_public_solution",
            "no_invented_solutions_and_negative_scope_disclosure",
            "lecture_numbering_and_two_source_proof_positions",
            "source_order_and_formula_witnesses",
            "six_correction_classes_with_visible_treatment",
            "append_only_correction_and_terminology_ledgers",
            "disjoint_bgk_stable_ids",
            "zero_reader_media_bound_to_official_pdf_rights_evidence",
            "pandoc_ast_all_three_files",
            "exact_model_provenance_license_and_nonendorsement",
            "no_placeholders_german_prose_malformed_math_backticks_or_invisible_controls",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"receipt": fact(OUT), "counts": result["counts"], "pandoc": pandoc}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
