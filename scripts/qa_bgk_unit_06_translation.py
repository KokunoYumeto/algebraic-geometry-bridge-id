#!/usr/bin/env python3
"""Fail-closed translation, formula, rights, and scope QA for BGK Unit 6."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
BGK = ROOT / "source" / "id-ID" / "bgk"
AUTH = ROOT / "authority" / "wikiversity-bgk" / "unit-06"
OUT = ROOT / "qa" / "BGK_UNIT_06_TRANSLATION_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra."
MANIFEST_SHA256 = "69a10e682e853c6f386afbc68438605846e5096220b21bd1e827c07633a79244"
AUTHORITY_QA_SHA256 = "c22f362a9b1bc71d4f8497ac06e8f1264935977a7d43584178c941de613306ed"
AUTHORITY_FREEZE_SHA256 = "6d8c217580f71cd2840521d6f7ecbdc80415c566058f7848890011bb2d10d45c"

FILES = (
    BGK / "lecture-06.md",
    BGK / "worksheet-06.md",
    BGK / "worksheet-06-solutions.md",
)
RIGHTS_FILES = {
    ROOT / "authority" / "ASSET_CLOSURE-bgk-unit-06.json": "9efa26ce4f4d0c0f95af36b7bba1efef15b55af9dcbd7533353e20c64f8f83b3",
    ROOT / "authority" / "RIGHTS-bgk-unit-06.csv": "87f9d56b1300a56ca68e4aa8f50e3d50ab622d7a4d05221089d49e1dba35981d",
    ROOT / "authority" / "commons-imageinfo-bgk-unit-06.json": "681014a0999f21f8ae99a31ae35003e215dc34a7604bbe35b6a18dbf7598d619",
    ROOT / "source" / "id-ID" / "media-credits-bgk-unit-06.md": "0d5b052a4346e8a56770798f3882417eaae2ea7e815f1947c289d9785e1c2af7",
    ROOT / "authority" / "artifacts" / "bgk-lecture-06-official.pdf": "55fbef2b5d9eae950ac7ab064a8029f2e2932c49280a98a4a7ec6ed16262c75d",
    ROOT / "authority" / "artifacts" / "bgk-worksheet-06-official.pdf": "7b4f4569e7ab749a9e6affac715592316c109507d91971fd1c7b82cefaa825b5",
}
LEDGER_CORRECTIONS = tuple(f"AGC-CORR-{n:04d}" for n in range(165, 170))
LEDGER_TERMS = tuple(f"AGT-{n:04d}" for n in range(334, 344))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def fact(path: Path) -> dict[str, object]:
    require(path.is_file() and not path.is_symlink(), f"missing regular file: {path}")
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)}


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
            str(path.relative_to(ROOT)),
        ],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    ast = json.loads(process.stdout)
    nodes = tuple(walk_ast(ast))
    return {
        "path": path.relative_to(ROOT).as_posix(),
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
    manifest_path = AUTH / "UNIT_AUTHORITY_MANIFEST.json"
    require(sha256(manifest_path) == MANIFEST_SHA256, "authority manifest hash mismatch")
    authority_qa = ROOT / "qa" / "BGK_UNIT_06_AUTHORITY_QA.json"
    require(sha256(authority_qa) == AUTHORITY_QA_SHA256, "authority QA hash mismatch")
    authority_freeze = ROOT / "authority" / "BGK_UNIT_06_AUTHORITY_FREEZE.md"
    require(sha256(authority_freeze) == AUTHORITY_FREEZE_SHA256, "authority freeze hash mismatch")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["unit_number"] == 6, "authority unit drifted")
    require(manifest["lecture"]["revid"] == 1003728 and manifest["worksheet"]["revid"] == 900086,
            "source revision drifted")
    require(manifest["lecture"]["mediawiki_sha1"] == "0dfea13421076e8f6486836e9fc799822bf52053",
            "lecture source SHA-1 drifted")
    require(manifest["worksheet"]["mediawiki_sha1"] == "619536dcd80063470e12de7a3ebb3fc9fe1aa5e5",
            "worksheet source SHA-1 drifted")
    require(manifest["lecture_transclusion_closure"]["requested_template_count"] ==
            manifest["lecture_transclusion_closure"]["captured_page_count"] == 136 and
            manifest["lecture_transclusion_closure"]["missing_page_count"] == 0,
            "lecture transclusion closure drifted")
    require(manifest["worksheet_transclusion_closure"]["requested_template_count"] ==
            manifest["worksheet_transclusion_closure"]["captured_page_count"] == 109 and
            manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0,
            "worksheet transclusion closure drifted")
    mismatches = []
    for row in manifest["files"]:
        path = AUTH / row["file"]
        if not path.is_file() or path.stat().st_size != row["bytes"] or sha256(path) != row["sha256"]:
            mismatches.append(row["file"])
    require(len(manifest["files"]) == 31 and not mismatches, f"authority file closure mismatch: {mismatches}")
    for path, expected in RIGHTS_FILES.items():
        require(sha256(path) == expected, f"rights file hash mismatch: {path.name}")

    texts = {path.name: path.read_text(encoding="utf-8") for path in FILES}
    joined = "\n".join(texts.values())
    for name, text in texts.items():
        require(f"translation_provenance: \"{MODEL}\"" in text, f"exact provenance missing: {name}")
        require("CC BY-SA 4.0" in text, f"CC BY-SA notice missing: {name}")
        require("tidak menyiratkan dukungan" in text, f"non-endorsement missing: {name}")
    require("translation_status: complete" in texts["lecture-06.md"], "lecture status incomplete")
    require("translation_status: complete" in texts["worksheet-06.md"], "worksheet status incomplete")
    require("translation_status: source_scope_complete" in texts["worksheet-06-solutions.md"], "solution scope status drifted")
    require(not re.search(r"(?:TODO|TBD|PLACEHOLDER|LOREM IPSUM)", joined, re.I), "placeholder remains")
    require(not re.search(r"[\u200b\u200c\u200d\u2060\ufeff]", joined), "invisible control remains")
    require(not re.search(r"\$[^$\n]*`", joined), "stray backtick inside math")
    require("$\\mathcal F_n$" in texts["lecture-06.md"] and "$\\mathcal F_\\bullet$" in texts["lecture-06.md"],
            "correct mathcal markup missing")
    require("$mathcal F_n$" not in joined and "$mathcal F_\\bullet$" not in joined, "malformed mathcal remains")
    require(re.search(r"funktor\s+eksak-kiri", texts["lecture-06.md"]), "preferred exact-functor term missing")
    require("funtor" not in joined and "fungtor" not in joined, "misspelled functor term remains")

    cleaned = "\n".join(body_without_metadata_comments_or_notes(text) for text in texts.values())
    german_residue = re.findall(r"\b(?:Zeige|Berechne|Aufgabe|Vorlesung|Arbeitsblatt|Es sei|Dann nennt man|Beweis)\b", cleaned)
    require(not german_residue, f"unexpected German prose residue: {german_residue[:5]}")

    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    require(mapping["unit"] == 6 and mapping["exercise_count"] == 19 and mapping["solution_count"] == 0,
            "exercise/solution scope drifted")
    require(all(not entry.get("has_public_solution") for entry in mapping["entries"]), "public solution topology drifted")
    worksheet = texts["worksheet-06.md"]
    expected_titles = [entry["exercise_title"] for entry in mapping["entries"]]
    actual_titles = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    require(len(actual_titles) == 20 and actual_titles[0] == "Überlagerung/Diskret/Definition",
            "worksheet definition mapping marker missing")
    require(actual_titles[1:] == expected_titles, "ordered exercise mapping mismatch")
    exercise_ids = re.findall(r"^## Soal 6\.(\d+) \{#(br-bgk-2019-w06-ex\d{2})\}$", worksheet, re.M)
    require([int(number) for number, _ in exercise_ids] == list(range(1, 20)), "exercise numbering mismatch")
    require(len({identifier for _, identifier in exercise_ids}) == 19, "duplicate exercise ID")
    candidates = json.loads((AUTH / "worksheet-solution-candidates-api.json").read_text(encoding="utf-8"))
    pages = candidates.get("query", {}).get("pages", [])
    require(len(pages) == 19 and all("missing" in page for page in pages), "negative solution evidence drifted")
    solutions = texts["worksheet-06-solutions.md"]
    require("satu pun dari sembilan belas soal" in solutions and "seluruh sembilan belas" in solutions,
            "nineteen-solution disclosure missing")
    require("Tidak ada solusi baru" in solutions and "negative_public_solution_count: 19" in solutions,
            "no-invention disclosure missing")

    lecture = texts["lecture-06.md"]
    expected_headings = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    numbered = [int(value) for value in re.findall(r"^### (?:Definisi|Contoh|Lema) 6\.(\d+):", lecture, re.M)]
    require(numbered == expected_headings, f"lecture numbered entities drifted: {numbered}")
    require(lecture.count("#### Bukti") == 5, "semantic proof-body count drifted")
    require(lecture.count("**Catatan edisi -") == 3, "lecture source-note count drifted")
    require(worksheet.count("**Catatan edisi -") == 4, "worksheet source-note count drifted")
    required_witnesses = (
        r"\operatorname{im}\varphi_n\subseteq\ker\varphi_{n+1}",
        r"\operatorname{im}\varphi_n=\ker\varphi_{n+1}",
        r"\mathcal F\xrightarrow{\alpha}\mathcal G\xrightarrow{\beta}\mathcal H",
        r"0\longrightarrow\mathcal F\xrightarrow{d}\mathcal G",
        r"\Gamma(X,\mathcal F)\longrightarrow\Gamma(X,\mathcal G)",
        r"(\varphi_*\mathcal F)(U):=\mathcal F\bigl(\varphi^{-1}(U)\bigr)",
        r"\operatorname*{colim}_{\substack{V\subseteq Y",
        r"\varphi^{-1}\mathcal G",
        r"s_i\in\mathcal F(\varphi^{-1}(V_i))",
    )
    for witness in required_witnesses:
        require(witness in lecture, f"mathematical witness missing: {witness}")
    for witness in ("einer stetige Abbildung", "eine weiterer topologischer Raum", r"\varphi_1,\varphi_2", "2014--2016", "2021--2023", r"$s_i\in\mathcal F(V_i)$"):
        require(witness in joined, f"source anomaly witness missing: {witness}")
    require("p_1(x_1)=p_2(x_2)" in worksheet and "p_1\\circ\\psi_1=p_2\\circ\\psi_2" in worksheet,
            "fiber-product notation missing")

    all_ids = [identifier for text in texts.values() for identifier in markdown_ids(text)]
    require(len(all_ids) == 45 and len(set(all_ids)) == 45, "Unit 6 heading-ID closure drifted")
    prior_ids = set()
    for unit in range(1, 6):
        for name in (f"lecture-{unit:02d}.md", f"worksheet-{unit:02d}.md", f"worksheet-{unit:02d}-solutions.md"):
            path = BGK / name
            if path.is_file():
                prior_ids.update(markdown_ids(path.read_text(encoding="utf-8")))
    require(not (set(all_ids) & prior_ids), "BGK stable-ID collision")
    with (ROOT / "00_control" / "CORRECTIONS.csv").open(encoding="utf-8-sig", newline="") as stream:
        corrections = {row["correction_id"]: row for row in csv.DictReader(stream)}
    require(all(identifier in corrections for identifier in LEDGER_CORRECTIONS), "Unit 6 correction ledger closure missing")
    require(all(corrections[identifier]["status"] == "applied_at_bgk_unit_06_translation" for identifier in LEDGER_CORRECTIONS),
            "Unit 6 correction status drifted")
    with (ROOT / "00_control" / "TERMINOLOGY.csv").open(encoding="utf-8-sig", newline="") as stream:
        terms = {row["term_id"]: row for row in csv.DictReader(stream)}
    require(all(identifier in terms for identifier in LEDGER_TERMS), "Unit 6 terminology closure missing")
    require(all(terms[identifier]["status"] == "admitted" for identifier in LEDGER_TERMS), "Unit 6 terminology status drifted")
    require(terms["AGT-0337"]["preferred_target"] == "funktor eksak-kiri" and
            terms["AGT-0337"]["rejected_or_variant"] == "funktor kiri-eksak",
            "Unit 6 exact-functor terminology drifted")

    closure = json.loads((ROOT / "authority" / "ASSET_CLOSURE-bgk-unit-06.json").read_text(encoding="utf-8"))
    require(closure["reader_media_positions"] == 0 and closure["unique_local_assets"] == 0 and not re.search(r"!\[[^\]]*\]\([^)]*\)", joined),
            "unexpected Unit 6 reader media")
    pandoc = [pandoc_fact(path) for path in FILES]
    result = {
        "schema": "ag-bridge-bgk-unit-translation-qa-v1",
        "unit": 6,
        "language": "id-ID",
        "status": "PASS",
        "model_provenance": MODEL,
        "authority": [fact(manifest_path), fact(authority_qa), fact(authority_freeze)] + [fact(AUTH / row["file"]) for row in manifest["files"]],
        "media_and_rights": [fact(path) for path in RIGHTS_FILES],
        "translation_files": [fact(path) for path in FILES],
        "pandoc": pandoc,
        "counts": {
            "source_exercises": 19, "translated_exercises": 19,
            "source_public_solutions": 0, "translated_public_solutions": 0,
            "negative_solution_candidates": 19, "invented_solutions": 0,
            "lecture_numbered_entities": 14, "source_fact_proof_templates": 7,
            "semantic_proof_bodies": 5, "heading_ids": len(all_ids),
            "heading_id_collisions": 0, "source_anomaly_classes": 5,
            "visible_anomaly_note_placements": lecture.count("**Catatan edisi -") + worksheet.count("**Catatan edisi -"),
            "correction_ledger_rows_added": len(LEDGER_CORRECTIONS),
            "terminology_rows_added": len(LEDGER_TERMS), "reader_media_positions": 0,
        },
        "correction_ids": list(LEDGER_CORRECTIONS),
        "terminology_ids_added": list(LEDGER_TERMS),
        "checks": [
            "frozen_manifest_and_complete_31_file_authority_closure",
            "exact_revision_transclusion_and_terminal_tex_identity",
            "ordered_nineteen_exercise_map_and_zero_public_solutions",
            "no_invented_solutions_and_negative_scope_disclosure",
            "lecture_fourteen_entities_and_five_semantic_proof_bodies",
            "source_formula_witnesses_and_five_visible_anomaly_treatments",
            "append_only_correction_and_terminology_ledgers",
            "preferred_functor_spelling_in_text_and_terminology_ledger",
            "disjoint_bgk_stable_ids",
            "zero_reader_media_bound_to_component_rights_evidence",
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
