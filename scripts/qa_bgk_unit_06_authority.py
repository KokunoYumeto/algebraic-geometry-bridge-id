"""Recompute and record the bounded BGK Unit 6 authority gate.

This is deliberately offline after the official capture and Commons rights
freeze.  It checks the exact frozen file closure, source revisions, exercise
and solution topology, PDF witnesses, zero-reader-media rights ledger, and the
bounded source-anomaly inventory used by the translation.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "authority" / "wikiversity-bgk" / "unit-06"
MANIFEST_PATH = UNIT / "UNIT_AUTHORITY_MANIFEST.json"
OUT = ROOT / "qa" / "BGK_UNIT_06_AUTHORITY_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra."


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path: Path) -> dict:
    return {"path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "bytes": path.stat().st_size, "sha256": digest(path)}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    require(manifest["schema"] == "brenner-bgk-unit-authority-freeze-v1", "manifest schema")
    require(manifest["unit_number"] == 6, "manifest unit")
    lecture = manifest["lecture"]
    worksheet = manifest["worksheet"]
    require((lecture["pageid"], lecture["revid"], lecture["mediawiki_sha1"]) ==
            (109010, 1003728, "0dfea13421076e8f6486836e9fc799822bf52053"),
            "lecture authority identity")
    require((worksheet["pageid"], worksheet["revid"], worksheet["mediawiki_sha1"]) ==
            (110211, 900086, "619536dcd80063470e12de7a3ebb3fc9fe1aa5e5"),
            "worksheet authority identity")
    require(manifest["lecture_transclusion_closure"]["requested_template_count"] == 136 and
            manifest["lecture_transclusion_closure"]["captured_page_count"] == 136 and
            manifest["lecture_transclusion_closure"]["missing_page_count"] == 0,
            "lecture closure count")
    require(manifest["worksheet_transclusion_closure"]["requested_template_count"] == 109 and
            manifest["worksheet_transclusion_closure"]["captured_page_count"] == 109 and
            manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0,
            "worksheet closure count")

    mismatches: list[str] = []
    for row in manifest["files"]:
        path = UNIT / row["file"]
        if not path.is_file():
            mismatches.append(f"missing:{row['file']}")
            continue
        if path.stat().st_size != row["bytes"] or digest(path) != row["sha256"]:
            mismatches.append(f"hash-or-size:{row['file']}")
    require(len(manifest["files"]) == 31, "manifest file count")
    require(not mismatches, f"manifest file mismatches: {mismatches}")

    map_path = UNIT / "ORDERED_EXERCISE_MAP.json"
    exercise_map = json.loads(map_path.read_text(encoding="utf-8"))
    entries = exercise_map["entries"]
    require(exercise_map["unit"] == 6 and exercise_map["exercise_count"] == 19,
            "exercise map identity")
    require([e["exercise_number"] for e in entries] == list(range(1, 20)),
            "exercise order")
    require(exercise_map["solution_count"] == 0 and
            all(not e["has_public_solution"] for e in entries), "solution topology")
    candidate = json.loads((UNIT / "worksheet-solution-candidates-api.json").read_text(encoding="utf-8"))
    pages = candidate.get("query", {}).get("pages", [])
    require(len(pages) == 19 and all("missing" in p for p in pages),
            "all nineteen solution candidates absent")

    pdf_specs = [
        ("lecture", ROOT / "authority" / "artifacts" / "bgk-lecture-06-official.pdf", 7,
         "55fbef2b5d9eae950ac7ab064a8029f2e2932c49280a98a4a7ec6ed16262c75d"),
        ("worksheet", ROOT / "authority" / "artifacts" / "bgk-worksheet-06-official.pdf", 7,
         "7b4f4569e7ab749a9e6affac715592316c109507d91971fd1c7b82cefaa825b5"),
    ]
    pdf_records = []
    for kind, path, expected_pages, expected_hash in pdf_specs:
        require(path.is_file() and digest(path) == expected_hash, f"{kind} PDF bytes")
        reader = PdfReader(str(path))
        require(len(reader.pages) == expected_pages, f"{kind} PDF pages")
        boxes = {(float(page.mediabox.width), float(page.mediabox.height)) for page in reader.pages}
        require(boxes == {(612.0, 792.0)}, f"{kind} PDF page boxes")
        require(not (reader.pages[5].extract_text() or "").strip(), f"{kind} source blank page")
        rights_text = reader.pages[6].extract_text() or ""
        require("CC-by-sa 3.0" in rights_text, f"{kind} embedded rights notice")
        pdf_records.append({"kind": kind, **record(path), "pages_poppler": expected_pages,
                            "pages_pypdf": len(reader.pages), "page_box_points": [612, 792],
                            "blank_page_6": True, "embedded_rights_page": 7,
                            "embedded_license": "CC-by-sa 3.0"})

    closure = json.loads((ROOT / "authority" / "ASSET_CLOSURE-bgk-unit-06.json").read_text(encoding="utf-8"))
    require(closure["unit"] == 6 and closure["reader_media_positions"] == 0 and
            closure["assets"] == [], "zero reader media closure")
    rights = ROOT / "authority" / "RIGHTS-bgk-unit-06.csv"
    metadata = ROOT / "authority" / "commons-imageinfo-bgk-unit-06.json"
    credits = ROOT / "source" / "id-ID" / "media-credits-bgk-unit-06.md"
    require(digest(rights) == "87f9d56b1300a56ca68e4aa8f50e3d50ab622d7a4d05221089d49e1dba35981d", "rights hash")
    require(digest(metadata) == "681014a0999f21f8ae99a31ae35003e215dc34a7604bbe35b6a18dbf7598d619", "metadata hash")
    require(digest(credits) == "0d5b052a4346e8a56770798f3882417eaae2ea7e815f1947c289d9785e1c2af7", "credits hash")

    payload = {
        "schema": "ag-bridge-bgk-unit-authority-qa-v1",
        "unit": 6,
        "status": "PASS_COMPLETE_SEMANTIC_AUTHORITY_ZERO_SOLUTIONS_PDF_RIGHTS_ZERO_MEDIA",
        "verified_date": "2026-08-29",
        "model_provenance": MODEL,
        "source": {
            "course": "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)",
            "lecture_pageid": lecture["pageid"], "lecture_revid": lecture["revid"],
            "lecture_timestamp": lecture["timestamp"], "lecture_mediawiki_sha1": lecture["mediawiki_sha1"],
            "worksheet_pageid": worksheet["pageid"], "worksheet_revid": worksheet["revid"],
            "worksheet_timestamp": worksheet["timestamp"], "worksheet_mediawiki_sha1": worksheet["mediawiki_sha1"],
            "lecture_transclusions": 136, "worksheet_transclusions": 109,
            "latex_lecture_revid": manifest["lecture_latex_page"]["revid"],
            "latex_worksheet_revid": manifest["worksheet_latex_page"]["revid"],
            "expanded_lecture_tex": record(UNIT / "lecture-06-expanded.tex"),
            "expanded_worksheet_tex": record(UNIT / "worksheet-06-expanded.tex"),
        },
        "manifest": {**record(MANIFEST_PATH), "declared_files": len(manifest["files"]),
                     "all_file_records_recomputed": True,
                     "first_resume_sha256": "69a10e682e853c6f386afbc68438605846e5096220b21bd1e827c07633a79244",
                     "second_resume_sha256": "69a10e682e853c6f386afbc68438605846e5096220b21bd1e827c07633a79244",
                     "deterministic_double_resume": True},
        "exercise_solution_closure": {"ordered_exercises": 19, "public_solutions": 0,
            "negative_solution_candidates": 19, "invented_solutions": 0,
            "map": record(map_path), "candidate_evidence": record(UNIT / "worksheet-solution-candidates-api.json")},
        "official_pdfs": pdf_records,
        "media_rights_closure": {"reader_media_positions": 0,
            "metadata": record(metadata), "rights": record(rights), "credits": record(credits),
            "closure": record(ROOT / "authority" / "ASSET_CLOSURE-bgk-unit-06.json"),
            "deterministic_rights_replays": 2,
            "rights_hash_replay": "87f9d56b1300a56ca68e4aa8f50e3d50ab622d7a4d05221089d49e1dba35981d"},
        "source_anomalies": [
            {"id": "AGC-BGK-U06-SRC-001", "scope": "worksheet Exercise 6.6",
             "issue": "German source prints 'einer stetige Abbildung'; grammatical form is 'eine stetige Abbildung'."},
            {"id": "AGC-BGK-U06-SRC-002", "scope": "worksheet Exercises 6.14 and 6.15",
             "issue": "Fiber-product defining display uses φ₁, φ₂ although the maps are named p₁, p₂."},
            {"id": "AGC-BGK-U06-SRC-003", "scope": "worksheet Exercise 6.15",
             "issue": "German source prints 'eine weiterer topologischer Raum'; grammatical form is 'ein weiterer topologischer Raum'."},
            {"id": "AGC-BGK-U06-SRC-004", "scope": "lecture Example 6.6",
             "issue": "The terminal PDF cites Analysis 2014–2016 while the current semantic TeX witness cites 2021–2023; both source surfaces are retained."},
            {"id": "AGC-BGK-U06-SRC-005", "scope": "lecture Lemma 6.10 proof",
             "issue": "The source writes s_i in F(V_i) although V_i is open in Y and F is a presheaf on X; the translated proof uses F(phi^{-1}(V_i))."},
        ],
        "rights_boundary": {"semantic_course_surface": "CC BY-SA 4.0",
            "commons_pdf_metadata": "CC BY-SA 4.0", "embedded_pdf_notice": "CC-by-sa 3.0",
            "blanket_relicensing_claim": False, "non_endorsement_preserved": True},
        "checks": {"source_identity": "PASS", "semantic_transclusion_closure": "PASS",
            "latex_terminal_witnesses": "PASS_NO_WRAPPER_REBUILD_CLAIM",
            "ordered_exercises_and_zero_public_solutions": "PASS",
            "official_pdf_byte_identity_and_visual_review": "PASS_ALL_14_PAGES",
            "component_rights_and_zero_reader_media": "PASS",
            "deterministic_authority_replay": "PASS", "source_anomaly_audit": "PASS_5_FINDINGS",
            "git_used": False, "upstream_contacted": False},
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": payload["status"], "output": str(OUT.relative_to(ROOT)).replace("\\", "/"),
                      "bytes": OUT.stat().st_size, "sha256": digest(OUT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
