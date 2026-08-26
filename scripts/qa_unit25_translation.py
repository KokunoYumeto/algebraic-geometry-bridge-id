#!/usr/bin/env python3
"""Fail-closed authority, translation, mathematics, accessibility, and rights QA for Unit 25."""

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
AUTH = ROOT / "authority" / "wikiversity" / "unit-25"
SOURCE = ROOT / "source" / "id-ID"
OUT = ROOT / "qa" / "UNIT_25_TRANSLATION_QA.json"
MODEL_BASE = "OpenAI Codex gpt-5.6-sol, Ultra"
MODEL = f"{MODEL_BASE}."

MANIFEST_FACT = (108049, "7cafbca7b5fd080529c2019967647ef8ffa823539b2113caaf0ad65e56d6afc1")
MAP_FACT = (16373, "1a887b81de9ccf9707e1e4835e477f9c9fb4a4358ab697242b17fd29873e8370")
AUTHORITY_QA_FACT = (2857, "252b8beea4aa11575727b639da03ddba2a47f95b86945cbd13519a3db3e91252")
FREEZE_FACT = (2883, "753109fa305eb1e9815a4bd4cd6dcf747b824e21b25ab8fd55898cf90622d7bb")
SOURCE_FACTS = {
    "source/id-ID/lecture-25.md": (16861, "7cc97947851f8e81d94f4c95ff8698be3d68883f4437a2c9ea3668984fb71916"),
    "source/id-ID/worksheet-25.md": (9017, "b14e559e69eef11553922ff521f5619edd2d2aae7bb160e989c23a52d72aef64"),
    "source/id-ID/worksheet-25-solutions.md": (3865, "7480af475102a439bcb381911ddb32351a16505c4e5485e90ddfcd4252845fc8"),
    "source/id-ID/media-credits-unit-25.md": (1856, "c6ccf54878cb00c9331d32dc4dbe36df88aea3e4962251509ace3d2b7529e9d7"),
}
CONTROL_FACTS = {
    "00_control/TERMINOLOGY.csv": (33838, "8eda4f9055604bc6aaa529249869fb70e01c0fa464838a051020f6f0c247a1f0"),
    "00_control/CORRECTIONS.csv": (62788, "b2cc62424c71e8540e435779236401c77fbd61ff6466eb5a0c2cc68483579c33"),
    "authority/UNIT_25_AUTHORITY_FREEZE.md": FREEZE_FACT,
}
EXTERNAL_FACTS = {
    "authority/RIGHTS-unit-25.csv": (443, "6b8de6f5a63f32d9f22e7fb69c98ba2d787121a2437a392602571504c2a1c544"),
    "authority/ASSET_CLOSURE-unit-25.json": (3927, "d177f9ca04beb707935ffa8695bbd9913b0fd081cbdbf2d8e77866c0c609b96f"),
    "authority/artifacts/lecture-25-official.pdf": (83406, "2543659400dcdeae70e7b088ebd2acc3298444af944812a10e1ae87cc939c449"),
    "authority/artifacts/worksheet-25-official.pdf": (47791, "e111513289034c75da657a778b7ca699e1a5fda55749477e5696aa5afa00a8d5"),
}
TERM_IDS = [f"AGT-{number:04d}" for number in range(209, 221)]
CORRECTION_IDS = [f"AGC-CORR-{number:04d}" for number in range(91, 97)]
LECTURE_ENTITIES = [
    "Ebene algebraische Kurve/Potenzreihenansatz/Einführung und Beispiele/Textabschnitt",
    "Ebene algebraische Kurven/Potenzreihenlösung für Punkt/Linearer Term liegt auf Tangente/Fakt",
    "Ebene algebraische Kurven/Potenzreihenlösung für Punkt/Linearer Term liegt auf Tangente/Fakt/Beweis",
    "Ebene algebraische Kurven/Tangenten mit Kontaktordnung eins/Formal-analytische Realisierung als Graph/Fakt",
    "Ebene algebraische Kurven/Tangenten mit Kontaktordnung eins/Formal-analytische Realisierung als Graph/Fakt/Beweis",
    "Potenzreihe für ebene Kurven/Graph einer rationalen Funktion/X^3+XY+Y ist 0/Beispiel",
    "Potenzreihe für ebene Kurven/Kartesisches Blatt/Graph/Beispiel",
    "Potenzreihe für ebene Kurven/Neilsche Parabel/Keine tangentiale Potenzreihe/Beispiel",
    "Satz über implizite Funktionen/Ebene Kurven/Bemerkung",
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


def check_fact(relative: str, expected: tuple[int, str]) -> dict[str, Any]:
    path = ROOT / relative
    require(path.is_file() and not path.is_symlink(), f"missing/nonregular file: {relative}")
    actual = (path.stat().st_size, digest(path))
    require(actual == expected, f"identity drift for {relative}: {actual} != {expected}")
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
    raw = re.sub(r"`[^`\n]*`", "", raw)
    return raw


def normalized_math(raw: str) -> str:
    return re.sub(r"\s+", "", raw)


def verify_authority() -> dict[str, Any]:
    manifest_fact = check_fact("authority/wikiversity/unit-25/UNIT_AUTHORITY_MANIFEST.json", MANIFEST_FACT)
    map_fact = check_fact("authority/wikiversity/unit-25/ORDERED_EXERCISE_MAP.json", MAP_FACT)
    authority_qa_fact = check_fact("qa/UNIT_25_AUTHORITY_QA.json", AUTHORITY_QA_FACT)
    freeze_fact = check_fact("authority/UNIT_25_AUTHORITY_FREEZE.md", FREEZE_FACT)
    manifest = json.loads((AUTH / "UNIT_AUTHORITY_MANIFEST.json").read_text(encoding="utf-8"))
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    authority_qa = json.loads((ROOT / "qa" / "UNIT_25_AUTHORITY_QA.json").read_text(encoding="utf-8"))

    require(authority_qa["result"] == "PASS" and authority_qa["unit"] == 25, "authority QA state")
    require(authority_qa["authority_manifest"] == {
        "path": "authority/wikiversity/unit-25/UNIT_AUTHORITY_MANIFEST.json",
        "bytes": MANIFEST_FACT[0],
        "sha256": MANIFEST_FACT[1],
    }, "authority QA manifest binding")
    require(authority_qa["authority_freeze_note"] == {
        "path": "authority/UNIT_25_AUTHORITY_FREEZE.md",
        "bytes": FREEZE_FACT[0],
        "sha256": FREEZE_FACT[1],
    }, "authority QA freeze binding")
    require(authority_qa["local_inventory"] == {"files": 56, "bytes": 691376}, "authority QA local inventory")
    require(authority_qa["bounded_external_inventory"] == {"files": 4, "bytes": 135567}, "authority QA external inventory")
    require(authority_qa["entry_revisions"] == {"course": 658236, "lecture": 793525, "worksheet": 793493}, "authority QA entry revisions")
    require(authority_qa["recursive_pages_with_roots"] == {"lecture": 70, "worksheet": 62, "solution_01": 12, "solution_02": 9}, "authority QA closure topology")
    require(authority_qa["exercise_count"] == 13, "authority QA exercise count")
    require(authority_qa["roles"] == {"warm_up": list(range(1, 6)), "submitted": list(range(6, 13)), "upload": [13]}, "authority QA exercise roles")
    require(authority_qa["submitted_displayed_points"] == [4, 4, 4, 3, 4, 4, 5], "authority QA submitted points")
    require((authority_qa["upload_displayed_points"], authority_qa["upload_authored_points"]) == (4, 3), "authority QA upload-point discrepancy")
    require(authority_qa["starred_numbers"] == [1, 2], "authority QA stars")
    require(authority_qa["public_solution_numbers"] == [1, 2] and authority_qa["negative_solution_numbers"] == list(range(3, 14)), "authority QA solution topology")
    require(authority_qa["reader_media_positions"] == 0 and authority_qa["official_pdf_pages"] == [7, 3], "authority QA media/PDF topology")
    require(authority_qa["final_live_identity_replay"] == {"semantic_wikiversity": 120, "local_wikiversity_pdfs": 2}, "authority QA live replay")

    require(manifest["schema"] == "brenner-unit-authority-freeze-v2" and manifest["unit_number"] == 25, "authority schema/unit")
    require(manifest["source_course"] == "Kurs:Algebraische Kurven (Osnabrück 2012)", "source-course identity")
    require(manifest["source_course_license"] == "CC BY-SA 4.0", "semantic course licence")
    route = manifest["source_component_license_route"]
    require(route["semantic_site_rights"]["notice"] == "CC BY-SA 4.0", "semantic-site rights notice")
    require(route["official_pdf_legacy_notice"] == "CC BY-SA 2.0 Germany", "legacy PDF notice")
    require(route["official_pdf_current_print_version_notice"] == "CC BY-SA 4.0", "current PDF notice")
    require(route["no_blanket_relicensing_claim"] is True, "no-blanket-relicensing boundary")
    require(
        (manifest["lecture"]["pageid"], manifest["lecture"]["revid"], manifest["lecture"]["mediawiki_sha1"], manifest["lecture"]["xml_sha256"])
        == (50731, 793525, "c589c3b9586e551eb81d7d941d79a9bc1461fe06", "4063269fa3a4e919790799935760600f5df9fecb1c8a677554188f059b316aa1"),
        "lecture identity/XML",
    )
    require(
        (manifest["worksheet"]["pageid"], manifest["worksheet"]["revid"], manifest["worksheet"]["mediawiki_sha1"], manifest["worksheet"]["xml_sha256"])
        == (50760, 793493, "1418cec6171ff8fd056dda7e6461f5ca4d91d910", "f682934e1b3b2cc74a078af4611c56de2aa73b41cfa5d61edf406ff7b13601f7"),
        "worksheet identity/XML",
    )
    require(
        [(row["bytes"], row["sha256"]) for row in manifest["derived_expanded_tex"]]
        == [
            (22932, "47cd10c4b01ead8e51b1fa6e1e020900032bae6517030efd4cc116ef0ba1fe5e"),
            (7379, "40661bb4202b74ed245da30306df0456c3b60d17ee62e054871386a70300514e"),
        ],
        "expanded TeX identities",
    )
    require(manifest["entry_revision_recheck"]["result"] == "PASS", "entry revision recheck")
    require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 69, "lecture closure")
    require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 61, "worksheet closure")
    require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "lecture missing dependency")
    require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "worksheet missing dependency")
    require(manifest["transclusion_topology"]["lecture"]["with_root"] == 70, "lecture root-plus-closure topology")
    require(manifest["transclusion_topology"]["worksheet"]["with_root"] == 62, "worksheet root-plus-closure topology")
    require(manifest["transclusion_topology"]["lecture"]["canonical_identity_rows_sha256"] == "aa14c07698e5e2911790457bee99f6e58a47b68fd5e75520c175ecc2756df8b1", "lecture identity rows")
    require(manifest["transclusion_topology"]["worksheet"]["canonical_identity_rows_sha256"] == "92727348e69deb229c952710318393751f99b09fea0b41b4c855daeadcb62828", "worksheet identity rows")

    require(len(manifest["files"]) == 56 and sum(row["bytes"] for row in manifest["files"]) == 691376, "local authority inventory")
    for row in manifest["files"]:
        path = AUTH / row["file"]
        require(path.is_file() and path.stat().st_size == row["bytes"] and digest(path) == row["sha256"], f"authority file replay: {row['file']}")
    require(len(manifest["bounded_external_files"]) == 4 and sum(row["bytes"] for row in manifest["bounded_external_files"]) == 135567, "external authority inventory")
    for row in manifest["bounded_external_files"]:
        path = ROOT / row["file"]
        require(path.is_file() and path.stat().st_size == row["bytes"] and digest(path) == row["sha256"], f"external authority replay: {row['file']}")

    live = manifest["final_live_identity_replay"]
    require(live["result"] == "PASS" and live["semantic_unique_identity_count"] == 120, "final semantic replay")
    require(sum(row["title_count"] for row in live["semantic_batches"]) == 120, "final replay batch total")
    require(live["local_wikiversity_pdf_identity_count"] == 2, "final local-PDF replay")
    require(live["latest_solution_identity_replayed"] == {
        "exercise_number": 1,
        "revid": 1112930,
        "timestamp": "2026-08-22T08:48:42Z",
        "mediawiki_sha1": "a388a7f91dd1a2c6759186a6c63de83eb93ba8e9",
    }, "latest solution live replay")

    require(mapping["schema"] == "brenner-worksheet-solution-map-v2" and mapping["unit"] == 25, "map schema/unit")
    require(mapping["exercise_count"] == 13 and mapping["solution_count"] == 2, "map topology")
    require([row["exercise_number"] for row in mapping["entries"]] == list(range(1, 14)), "exercise order")
    topology = mapping["ordered_role_point_and_star_topology"]
    require(topology["warm_up_numbers"] == list(range(1, 6)), "warm-up topology")
    require(topology["submitted_numbers"] == list(range(6, 13)), "submitted topology")
    require(topology["upload_numbers"] == [13], "upload topology")
    authored_points = [4, 4, 3, 3, 3, 4, 4, 4, 3, 4, 4, 5, 3]
    require(topology["authored_points"] == {str(index): value for index, value in enumerate(authored_points, start=1)}, "authored point topology")
    require(topology["displayed_points"] == {"6": 4, "7": 4, "8": 4, "9": 3, "10": 4, "11": 4, "12": 5, "13": 4}, "displayed point topology")
    require(topology["submitted_displayed_point_total"] == 28 and topology["starred_numbers"] == [1, 2], "point total/star topology")
    expected_roles = ["warm-up"] * 5 + ["submitted"] * 7 + ["upload"]
    require([row["role"] for row in mapping["entries"]] == expected_roles, "entry role order")
    require([row["authored_points"] for row in mapping["entries"]] == authored_points, "entry authored points")

    solutions = [row for row in mapping["entries"] if row["has_public_solution"]]
    require(len(solutions) == 2 and [row["exercise_number"] for row in solutions] == [1, 2], "public solution set")
    require(
        [(row["exercise_number"], row["pageid"], row["revid"], row["mediawiki_sha1"], row["xml_sha256"]) for row in solutions]
        == [
            (1, 21296, 1112930, "a388a7f91dd1a2c6759186a6c63de83eb93ba8e9", "39ac23016a2014f255207ba743a8537d2e0744a7aa3d624e16cd2de1f5bf4ad5"),
            (2, 21581, 1022975, "4e9bc137ff33d63de0728b6b9c40093ba7e95e46", "74a2d210868885487a9091acf5735ff97fb8a1809f697440bb87083584df6570"),
        ],
        "public solution identity/XML",
    )
    closures = manifest["public_solution_transclusion_closures"]
    require([row["exercise_number"] for row in closures] == [1, 2], "solution closure order")
    require([row["solution_revid"] for row in closures] == [1112930, 1022975], "solution closure revisions")
    require([row["recursive_transclusion_closure"]["captured_page_count"] for row in closures] == [11, 8], "solution dependency closures")
    require([row["recursive_transclusion_closure"]["missing_page_count"] for row in closures] == [0, 0], "solution missing dependencies")
    require([row["topology"]["with_root"] for row in closures] == [12, 9], "solution root-plus-closure topology")
    require([row["topology"]["canonical_identity_rows_sha256"] for row in closures] == [
        "cf8713fe21f8f85b327439235147d91ea4be82422f56750a3e70d51fd17e22fe",
        "9c6d058cb3adb20f94624e47caaf62847655243262aeda7d497cceae5a079e51",
    ], "solution identity rows")
    require(all(row["direct_wrapper_dependency_titles"] == [] for row in closures), "unexpected solution wrapper")
    negative = mapping["negative_public_solution_evidence"]
    require(negative["exact_candidate_title_count"] == 13 and negative["positive_numbers"] == [1, 2], "candidate solution set")
    require(negative["negative_numbers"] == list(range(3, 14)) and negative["negative_count"] == 11, "negative solution evidence")
    require(all(row["api_missing"] is True for row in negative["entries"]), "negative solution API evidence")
    require(manifest["source_defect_bindings"] == [], "unexpected source-defect binding")
    require([row["id"] for row in manifest["source_discrepancy_bindings"]] == ["AGC-U25-POINT-001"], "source discrepancy binding")
    require(mapping["point_discrepancies"] == manifest["source_discrepancy_bindings"], "point-discrepancy cross-binding")
    require(manifest["images"]["reader_media_positions"] == 0 and manifest["images"]["substantive_assets"] == [], "authority reader media topology")

    witnesses = manifest["official_pdf_witnesses"]
    require([row["kind"] for row in witnesses] == ["lecture", "worksheet"], "official PDF witness order")
    require([(row["local_bytes"], row["local_sha256"], row["page_count"]) for row in witnesses] == [
        (83406, EXTERNAL_FACTS["authority/artifacts/lecture-25-official.pdf"][1], 7),
        (47791, EXTERNAL_FACTS["authority/artifacts/worksheet-25-official.pdf"][1], 3),
    ], "official PDF witness identity/pages")

    freeze = (ROOT / "authority" / "UNIT_25_AUTHORITY_FREEZE.md").read_text(encoding="utf-8")
    require("Exactly 13 exercises are preserved in order" in freeze, "freeze exercise closure")
    require("Exercises 1 and 2 are starred and are the only public solutions" in freeze, "freeze solution closure")
    require("zero reader media positions" in freeze and "no blanket relicensing claim" in freeze, "freeze media/rights boundary")

    return {
        "manifest": manifest_fact,
        "exercise_map": map_fact,
        "authority_qa": authority_qa_fact,
        "authority_freeze": freeze_fact,
        "source_course": "Kurs:Algebraische Kurven (Osnabrück 2012)",
        "lecture_revid": 793525,
        "worksheet_revid": 793493,
        "lecture_transclusions_exact": 69,
        "worksheet_transclusions_exact": 61,
        "lecture_with_root": 70,
        "worksheet_with_root": 62,
        "exercises": 13,
        "public_solution_numbers": [1, 2],
        "negative_solution_numbers": list(range(3, 14)),
        "solution_revisions": [1112930, 1022975],
        "solution_recursive_closures": [11, 8],
        "solution_with_roots": [12, 9],
        "authority_files_verified": 56,
        "bounded_external_files_verified": 4,
        "live_semantic_wikiversity_identities": 120,
        "live_local_wikiversity_pdf_identities": 2,
        "source_discrepancy_bindings": ["AGC-U25-POINT-001"],
    }


def verify_media_and_rights() -> dict[str, Any]:
    facts = [check_fact(relative, expected) for relative, expected in EXTERNAL_FACTS.items()]
    with (ROOT / "authority" / "RIGHTS-unit-25.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    closure = json.loads((ROOT / "authority" / "ASSET_CLOSURE-unit-25.json").read_text(encoding="utf-8"))
    require(closure["schema"] == "brenner-unit-media-closure-v2" and closure["unit"] == 25, "media closure identity")
    require(closure["authority_only_boundary"] is True, "authority-only media boundary")
    require(closure["reader_media_positions"] == 0 and closure["unique_local_assets"] == 0, "zero-media topology")
    require(closure["animated_html_positions"] == 0 and closure["assets"] == [], "asset topology")
    require((closure["rights_bytes"], closure["rights_sha256"]) == EXTERNAL_FACTS["authority/RIGHTS-unit-25.csv"], "rights binding")
    require(closure["reader_credits_file"] is None and closure["reader_credits_required"] is False, "reader credits requirement")
    require(rows == [], "rights file must be header-only at zero-media boundary")
    require(closure["official_pdf_witnesses_are_not_media_positions"] is True, "PDF/media separation")
    pdf_rights = closure["official_pdf_component_rights"]
    require([row["local_path"] for row in pdf_rights] == ["authority/artifacts/lecture-25-official.pdf", "authority/artifacts/worksheet-25-official.pdf"], "PDF rights order")
    require([(row["source_bytes"], row["source_sha1"]) for row in pdf_rights] == [
        (83406, "f456dc49f8f4c1f1d67c921124496871f54f5c0b"),
        (47791, "3d854595c241715a34b1f003440b2171d2e4b7e8"),
    ], "official PDF source identity")
    require(all(row["component_license_route"]["current_print_version_notice"] == "CC BY-SA 4.0" for row in pdf_rights), "PDF current licence route")
    require(all(row["component_license_route"]["legacy_file_notice"] == "CC BY-SA 2.0 Germany" for row in pdf_rights), "PDF legacy licence route")
    require(all(row["component_license_route"]["embedded_pdf_label"] is None for row in pdf_rights), "embedded-PDF licence claim")
    surfaces = closure["accessibility"]["official_pdf_surfaces"]
    require(all(row["encrypted"] is False for row in surfaces), "PDF encryption topology")
    require(all(row["tagged_pdf"] is False and row["structure_tree_present"] is False for row in surfaces), "PDF tag/structure topology")
    require(all(row["document_language"] is None and row["outline_or_bookmark_count"] == 0 for row in surfaces), "PDF language/outline topology")
    mismatch = closure["component_discrepancies"]["exercise_13_point_mismatch"]
    require(mismatch == {"exercise_page_authored_points": 3, "worksheet_displayed_points": 4}, "media-closure point discrepancy")
    for relative in ("authority/artifacts/lecture-25-official.pdf", "authority/artifacts/worksheet-25-official.pdf"):
        require((ROOT / relative).read_bytes().startswith(b"%PDF-"), f"PDF signature: {relative}")

    credits = (SOURCE / "media-credits-unit-25.md").read_text(encoding="utf-8")
    require("tidak\nmemuat posisi media pembaca substantif" in credits, "zero-media reader disclosure")
    require("tidak menyediakan\nberkas gambar" in credits, "exercise-13 zero-asset disclosure")
    require("CC BY-SA 2.0 Germany" in credits and "CC BY-SA 4.0" in credits, "dual PDF/course licence disclosure")
    require("tujuh\nhalaman" in credits and "tiga halaman" in credits, "PDF page topology disclosure")
    require("tidak bertag" in credits and "tidak mempunyai pohon struktur" in credits, "PDF accessibility disclosure")
    require("Holger Brenner" in credits and "Arbota" in credits and "Bocardodarapti" in credits, "author/revision-contributor credits")
    require("hubungan yang berbeda" in credits, "author/contributor distinction")
    require(credits.count(MODEL_BASE) == 1, "media-credit model provenance")
    require("tidak menyiratkan\ndukungan atau afiliasi resmi" in credits, "independent-edition non-endorsement")
    return {
        "reader_media_positions": 0,
        "binary_assets": 0,
        "rights_rows": 0,
        "official_pdf_witnesses": 2,
        "official_pdf_pages": [7, 3],
        "official_pdf_tagged": [False, False],
        "dual_component_licence_routes_preserved": True,
        "facts": facts,
    }


def verify_translation() -> dict[str, Any]:
    facts = [check_fact(relative, expected) for relative, expected in SOURCE_FACTS.items()]
    facts.extend(check_fact(relative, expected) for relative, expected in CONTROL_FACTS.items())
    lecture = (SOURCE / "lecture-25.md").read_text(encoding="utf-8")
    worksheet = (SOURCE / "worksheet-25.md").read_text(encoding="utf-8")
    solutions = (SOURCE / "worksheet-25-solutions.md").read_text(encoding="utf-8")
    credits = (SOURCE / "media-credits-unit-25.md").read_text(encoding="utf-8")
    all_text = "\n".join((lecture, worksheet, solutions, credits))

    for name, raw in (("lecture", lecture), ("worksheet", worksheet), ("solutions", solutions)):
        require("language: id-ID" in raw, f"{name} Indonesian language tag")
        require("translation_status: complete" in raw, f"{name} completion flag")
        require(raw.count(MODEL_BASE) == 1, f"{name} exact model provenance")
        require("CC BY-SA 4.0" in raw, f"{name} semantic-source licence metadata")
        require(MANIFEST_FACT[1] in raw, f"{name} manifest binding")
        require("Osnabrück 2012" in raw, f"{name} exact 2012 source-edition identity")
        require("Holger Brenner" in raw, f"{name} source-author attribution")
    require("frozen_revision_contributor: \"Arbota\"" in lecture and "frozen_revision_contributor: \"Arbota\"" in worksheet, "root revision-contributor attribution")
    require("frozen_revision_contributors: \"Soal 25.1: Bocardodarapti; Soal 25.2: Arbota\"" in solutions, "solution revision-contributor attribution")
    require("source_semantic_entities: 9" in lecture and "source_corrections: 3" in lecture, "lecture source topology metadata")
    require("correction_ids: \"AGC-CORR-0091; AGC-CORR-0092; AGC-CORR-0093\"" in lecture, "lecture correction-ID metadata")
    require("source_corrections: 2" in worksheet and "source_discrepancies: 1" in worksheet, "worksheet correction/discrepancy metadata")
    require("correction_ids: \"AGC-CORR-0094; AGC-CORR-0095\"" in worksheet, "worksheet correction-ID metadata")
    require("source_discrepancy_ids: \"AGC-CORR-0096; AGC-U25-POINT-001\"" in worksheet, "worksheet discrepancy-ID metadata")
    require("source_corrections: 0" in solutions and "public_solution_count: 2" in solutions, "solution topology metadata")
    require("reader_media_positions: 0" in lecture and "reader_media_positions: 0" in worksheet, "zero-media metadata")
    require("4063269fa3a4e919790799935760600f5df9fecb1c8a677554188f059b316aa1" in lecture, "lecture XML binding")
    require("47cd10c4b01ead8e51b1fa6e1e020900032bae6517030efd4cc116ef0ba1fe5e" in lecture, "lecture TeX binding")
    require("aa14c07698e5e2911790457bee99f6e58a47b68fd5e75520c175ecc2756df8b1" in lecture, "lecture dependency binding")
    require("f682934e1b3b2cc74a078af4611c56de2aa73b41cfa5d61edf406ff7b13601f7" in worksheet, "worksheet XML binding")
    require("40661bb4202b74ed245da30306df0456c3b60d17ee62e054871386a70300514e" in worksheet, "worksheet TeX binding")
    require(MAP_FACT[1] in worksheet and MAP_FACT[1] in solutions, "exercise-map source binding")
    require("39ac23016a2014f255207ba743a8537d2e0744a7aa3d624e16cd2de1f5bf4ad5" in solutions, "solution-01 XML binding")
    require("74a2d210868885487a9091acf5735ff97fb8a1809f697440bb87083584df6570" in solutions, "solution-02 XML binding")
    require("br-ak-2025-2026" not in all_text, "wrong source-edition stable-ID namespace")

    lower = all_text.casefold()
    require(all(token not in lower for token in ("todo", "fixme", "tbd", "placeholder", "lorem ipsum", "terjemahkan di sini")), "placeholder residue")
    require(not re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|access[_-]?token|bearer\s+[A-Za-z0-9._-]{20,}|api[_-]?key\s*[:=]", all_text, flags=re.I), "secret-like content")
    controls = [(character, f"U+{ord(character):04X}") for character in all_text if unicodedata.category(character) in {"Cc", "Cf"} and character not in "\t\n\r"]
    require(not controls, f"invisible/control Unicode residue: {controls[:5]}")

    prose_by_file = {
        "lecture": strip_nonprose(lecture),
        "worksheet": strip_nonprose(worksheet),
        "solutions": strip_nonprose(solutions),
        "credits": strip_nonprose(credits),
    }
    prose = "\n".join(prose_by_file.values())
    residue = re.findall(
        r"\b(?:Es sei|Zeige|Aufgabe|Beweis|Lösung|Potenzreihenlösung|Potenzreihenansatz|Komplettierung|Umgebungsbasis|Kontaktordnung|Graphenlösung|Tangentenparameter)\b",
        prose,
        flags=re.I,
    )
    require(not residue, f"visible German residue: {residue}")
    language_needles = {
        "lecture": ("misalkan", "dengan", "maka", "bukti", "sehingga"),
        "worksheet": ("misalkan", "tunjukkan", "tentukan", "dengan", "suatu"),
        "solutions": ("kita", "diperoleh", "karena", "koefisien", "harus"),
        "credits": ("tidak", "sumber", "edisi", "kontributor", "hak"),
    }
    for name, needles in language_needles.items():
        file_prose = prose_by_file[name].casefold()
        require(all(re.search(rf"\b{re.escape(needle)}\b", file_prose) for needle in needles), f"Indonesian prose markers: {name}")

    lecture_comments = re.findall(r"<!-- upstream_entity: (.*?) -->", lecture)
    require(lecture_comments == LECTURE_ENTITIES and len(lecture_comments) == 9, "ordered lecture semantic entity mappings")
    lecture_ids = re.findall(r"\{#(br-ak-2012-l25[^}\s]*)\}", lecture)
    expected_lecture_ids = [
        "br-ak-2012-l25",
        "br-ak-2012-l25-s01",
        "br-ak-2012-l25-lem-01",
        "br-ak-2012-l25-lem-01-proof",
        "br-ak-2012-l25-thm-01",
        "br-ak-2012-l25-thm-01-proof",
        "br-ak-2012-l25-ex-01",
        "br-ak-2012-l25-ex-02",
        "br-ak-2012-l25-ex-03",
        "br-ak-2012-l25-rem-01",
    ]
    require(lecture_ids == expected_lecture_ids and len(set(lecture_ids)) == 10, "lecture stable-ID topology")
    require(lecture.count("> **Catatan edisi -") == 3, "lecture visible correction-note count")
    require(all(lecture.count(correction_id) == 1 for correction_id in CORRECTION_IDS[:3]), "lecture correction-ID count")

    headers = re.findall(r"^### Soal 25\.(\d+)(?:[^\n]*)\{#br-ak-2012-w25-ex-(\d{2})\}$", worksheet, flags=re.M)
    require(headers == [(str(index), f"{index:02d}") for index in range(1, 14)], "exercise headers/IDs")
    starred = [int(value) for value in re.findall(r"^### Soal 25\.(\d+) ★", worksheet, flags=re.M)]
    require(starred == [1, 2], "solution-star topology")
    points = re.findall(r"^### Soal 25\.(\d+) \(([^)]*poin[^)]*)\)", worksheet, flags=re.M)
    require(points == [(str(index), f"{value} poin") for index, value in zip(range(6, 14), [4, 4, 4, 3, 4, 4, 5, 4])], "displayed point topology")
    require(worksheet.index("### Soal 25.5") < worksheet.index("## Soal untuk dikumpulkan") < worksheet.index("### Soal 25.6"), "warm-up/submitted boundary")
    require(worksheet.index("### Soal 25.12") < worksheet.index("## Soal untuk diunggah") < worksheet.index("### Soal 25.13"), "submitted/upload boundary")
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    worksheet_comments = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    require(worksheet_comments == [row["exercise_title"] for row in mapping["entries"]] and len(worksheet_comments) == 13, "ordered worksheet entity mappings")
    require(worksheet.count("> **Catatan edisi -") == 3, "worksheet visible correction/discrepancy-note count")
    require(all(worksheet.count(correction_id) == 1 for correction_id in CORRECTION_IDS[3:]), "worksheet correction-ID count")
    require(worksheet.count("AGC-U25-POINT-001") == 1, "worksheet point-discrepancy ID count")

    solution_headers = [int(value) for value in re.findall(r"^## Solusi Soal 25\.(\d+) ", solutions, flags=re.M)]
    require(solution_headers == [1, 2], "exact public solution headers")
    solution_comments = re.findall(r"<!-- upstream_solution: (.*?); pageid=(\d+); revid=(\d+) -->", solutions)
    require(solution_comments == [
        ("Ebene algebraische Kurve/Potenzreihenansatz/x^3+y^2-xy+x/Nullpunkt/Aufgabe/Lösung", "21296", "1112930"),
        ("Ebene algebraische Kurve/Potenzreihenansatz/x^2y+x^2+y^2-5xy+y/Nullpunkt/Aufgabe/Lösung", "21581", "1022975"),
    ], "solution comments/identities")
    require(solutions.count("<!-- upstream_solution_url:") == 2, "solution immutable URL count")
    require("https://de.wikiversity.org/w/index.php?oldid=1112930" in solutions and "https://de.wikiversity.org/w/index.php?oldid=1022975" in solutions, "solution oldid URLs")
    require(re.findall(r"\[Kembali ke Soal 25\.(\d+)\]\(#br-ak-2012-w25-ex-\d{2}\)", solutions) == ["1", "2"], "solution backlinks")
    require("Sebelas calon halaman solusi lainnya\ndinyatakan tidak ada" in solutions and "Tidak ada solusi\ntambahan yang dibuat" in solutions, "no-invented-solutions disclosure")
    require(not re.search(r"^## Solusi Soal 25\.(?:[3-9]|1[0-3])\b", solutions, flags=re.M), "invented solution heading")

    stable_ids_by_file = {
        "lecture": re.findall(r"\{#([^}\s]+)\}", lecture),
        "worksheet": re.findall(r"\{#([^}\s]+)\}", worksheet),
        "solutions": re.findall(r"\{#([^}\s]+)\}", solutions),
        "credits": re.findall(r"\{#([^}\s]+)\}", credits),
    }
    require({name: len(ids) for name, ids in stable_ids_by_file.items()} == {"lecture": 10, "worksheet": 17, "solutions": 3, "credits": 1}, "per-file stable-ID counts")
    stable_ids = [stable_id for ids in stable_ids_by_file.values() for stable_id in ids]
    require(len(stable_ids) == 31 and len(stable_ids) == len(set(stable_ids)), "global stable-ID topology")
    require({"br-ak-2012-l25", "br-ak-2012-w25", "br-ak-2012-w25-solutions", "agc-media-credits-unit-25"} <= set(stable_ids), "2012 stable-ID roots")
    require(not re.search(r"!\[[^\]]*\]\(", all_text), "reader image topology")

    with (ROOT / "00_control" / "TERMINOLOGY.csv").open(encoding="utf-8", newline="") as stream:
        term_rows = {row["term_id"]: row for row in csv.DictReader(stream)}
    expected_terms = {
        "AGT-0209": ("Potenzreihenlösung", "solusi deret pangkat"),
        "AGT-0210": ("Potenzreihenansatz", "pendekatan deret pangkat"),
        "AGT-0211": ("Anfangsbedingung", "syarat awal"),
        "AGT-0212": ("einfacher Linearfaktor", "faktor linear sederhana"),
        "AGT-0213": ("Kontaktordnung", "orde kontak"),
        "AGT-0214": ("Graphenlösung", "solusi berbentuk grafik"),
        "AGT-0215": ("Komplettierung", "kompletasi"),
        "AGT-0216": ("verträgliche Folge", "barisan kompatibel"),
        "AGT-0217": ("Ideal-adische Topologie", "topologi I-adik"),
        "AGT-0218": ("Umgebungsbasis", "basis lingkungan"),
        "AGT-0219": ("formale Laurentreihe mit endlichem Hauptteil", "deret Laurent formal dengan bagian utama berhingga"),
        "AGT-0220": ("Tangentenparameter", "parameter garis singgung"),
    }
    require(list(expected_terms) == TERM_IDS, "terminology ID interval")
    for term_id, (source_term, target_term) in expected_terms.items():
        require(term_id in term_rows and term_rows[term_id]["source_term"] == source_term, f"terminology source: {term_id}")
        require(term_rows[term_id]["preferred_target"] == target_term and term_rows[term_id]["status"] == "admitted", f"terminology target/status: {term_id}")
    flat_text = re.sub(r"\s+", " ", all_text).casefold()
    visibility_needles = {
        "AGT-0209": "solusi deret pangkat",
        "AGT-0210": "pendekatan deret pangkat",
        "AGT-0211": "syarat awal",
        "AGT-0212": "faktor linear sederhana",
        "AGT-0213": "orde kontak",
        "AGT-0214": "solusi berbentuk grafik",
        "AGT-0215": "kompletasi",
        "AGT-0216": "barisan kompatibel",
        "AGT-0217": "topologi $i$-adik",
        "AGT-0218": "basis lingkungan",
        "AGT-0219": "deret laurent formal dengan bagian utama berhingga",
        "AGT-0220": "parameter garis singgung",
    }
    missing_terms = [term_id for term_id, needle in visibility_needles.items() if needle not in flat_text]
    require(not missing_terms, f"preferred reader terminology absent: {missing_terms}")
    require(not re.search(r"\b(?:solusi deret kuasa|ansatz deret pangkat|kondisi awal|faktor linear bermultipisitas satu|tingkat kontak|solusi grafik|pelengkapan|keluarga kompatibel|topologi adik ideal|basis persekitaran|parameter tangen)\b", prose, flags=re.I), "nonpreferred terminology residue")

    with (ROOT / "00_control" / "CORRECTIONS.csv").open(encoding="utf-8", newline="") as stream:
        corrections = {row["correction_id"]: row for row in csv.DictReader(stream)}
    expected_correction_kinds = {
        "AGC-CORR-0091": "source_composition_orientation_error",
        "AGC-CORR-0092": "source_initial_condition_notation_ambiguity",
        "AGC-CORR-0093": "source_malformed_field_alternative",
        "AGC-CORR-0094": "editorial_field_scope_note",
        "AGC-CORR-0095": "source_characteristic_scope_omission",
        "AGC-CORR-0096": "source_point_value_discrepancy",
    }
    require(list(expected_correction_kinds) == CORRECTION_IDS, "correction ID interval")
    for correction_id, kind in expected_correction_kinds.items():
        require(correction_id in corrections and corrections[correction_id]["kind"] == kind, f"correction kind: {correction_id}")
        require(corrections[correction_id]["status"] == "applied_at_unit_25_translation", f"correction status: {correction_id}")
    disclosures = {
        "AGC-CORR-0091": "koreksi orientasi komposisi sumber" in lecture and normalized_math(r"G(U(T))=T") in normalized_math(lecture) and normalized_math(r"H(U(T))=\widetilde H(T)") in normalized_math(lecture),
        "AGC-CORR-0092": "penegasan syarat awal" in lecture and normalized_math(r"a_0=b_0=0") in normalized_math(lecture),
        "AGC-CORR-0093": "perbaikan redaksional sumber" in lecture and normalized_math(r"K=\mathbb R\qquad\text{atau}\qquad K=\mathbb C") in normalized_math(lecture),
        "AGC-CORR-0094": "lingkup lapangan" in worksheet and "edisi memakai lapangan dasar $\\mathbb R$" in worksheet,
        "AGC-CORR-0095": "karakteristik" in worksheet and normalized_math(r"\operatorname{char}(K)\ne2") in normalized_math(worksheet) and "koefisien $T^2$" in worksheet,
        "AGC-CORR-0096": "ketidaksesuaian poin sumber" in worksheet and "menampilkan 4 poin" in worksheet and "mencatat 3 poin" in worksheet,
    }
    require(all(disclosures.values()), f"missing visible correction disclosure: {[key for key, value in disclosures.items() if not value]}")

    normalized_lecture = normalized_math(lecture)
    lecture_protected = [
        r"K[X,Y]/(F)\longrightarrow K[[T]]",
        r"F(G,H)=0",
        r"G=\sum_{k=0}^{\infty}a_kT^k",
        r"H=\sum_{\ell=0}^{\infty}b_\ell T^\ell",
        r"a_0=b_0=0",
        r"F=F_m+\cdots+F_d",
        r"F_m=\prod_{\lambda=1}^{m}(u_\lambda X+v_\lambda Y)",
        r"u_\lambda a_1+v_\lambda b_1=0",
        r"F_m(a_1,b_1)=0",
        r"G(U(T))=T",
        r"H(U(T))=\widetilde H(T)",
        r"a_1u+b_1v=0",
        r"c_{m,0}=0",
        r"c_{m-1,1}\ne0",
        r"i+\sum_{\rho=1}^{j}\ell_\rho=k",
        r"k=m+\ell-1",
        r"c_{m-1,1}b_\ell",
        r"F=X^3+XY+Y=0",
        r"H=-T^3+T^4-T^5+T^6-T^7+\cdots",
        r"Y=\frac{-X^3}{1+X}",
        r"X^3+Y^3-3XY=0",
        r"b_2=\frac13",
        r"b_5=\frac1{81}",
        r"b_8=\frac1{729}",
        r"H=\frac13T^2+\frac1{81}T^5+\frac1{729}T^8+\cdots",
        r"X^3-Y^2=0",
        r"G=T^2",
        r"H=T^3",
        r"K=\mathbb R",
        r"K=\mathbb C",
    ]
    missing_lecture_math = [token for token in lecture_protected if normalized_math(token) not in normalized_lecture]
    require(not missing_lecture_math, f"protected lecture mathematics absent: {missing_lecture_math}")

    normalized_worksheet = normalized_math(worksheet)
    worksheet_protected = [
        r"V\left(X^3+Y^2-XY+X\right)",
        r"X=F(Y)",
        r"V\left(X^2Y+X^2+Y^2-5XY+Y\right)",
        r"Y=F(X)",
        r"\varphi_n:R/\mathfrak m^{n+1}\longrightarrow R/\mathfrak m^n",
        r"\varphi_n(a_{n+1})=a_n",
        r"\left\{x+I^n\mid n\in\mathbb N\right\}",
        r"\bigcap_n I^n=\{0\}",
        r"V\left(\left(X^2+Y^2\right)^2-2X\left(X^2+Y^2\right)-Y^2\right)",
        r"\operatorname{char}(K)\ne2",
        r"a_0=1,\qquad a_1=0,\qquad b_0=0,\qquad b_1=1",
        r"G(T)^2+H(T)^2=1",
        r"C=V\left(Y^3-X^2\right)",
        r"F=\sum_{n=k}^{\infty}a_nT^n",
        r"R=K[[T]]",
        r"\mathfrak m=(T)",
        r"K=\mathbb Z/(7)",
        r"R=K[X,Y]/(F)",
        r"S=R^{\operatorname{norm}}",
        r"R\longrightarrow K[[T]]",
    ]
    missing_worksheet_math = [token for token in worksheet_protected if normalized_math(token) not in normalized_worksheet]
    require(not missing_worksheet_math, f"protected worksheet mathematics absent: {missing_worksheet_math}")
    worksheet_semantic_needles = [
        "sampai dengan suku keenam",
        "sampai dengan orde kelima",
        "barisan kompatibel",
        "bersifat injektif",
        "topologi $I$-adik",
        "parameter garis singgung",
        "sampai dengan suku kelima",
        "deret Laurent formal dengan bagian utama berhingga",
        "lapangan pecahan",
        "tidak ada akar kuadrat dari $T$",
        "terdapat tepat satu homomorfisme gelanggang",
        "berbagai aproksimasi polinomial",
    ]
    worksheet_flat = re.sub(r"\s+", " ", worksheet)
    require(all(needle in worksheet_flat for needle in worksheet_semantic_needles), "exercise-statement semantic closure")

    normalized_solutions = normalized_math(solutions)
    solution_protected = [
        r"X=F(Y)=\sum_{i=0}^{\infty}a_iY^i",
        r"a_0=0",
        r"a_1=0",
        r"a_2=-1",
        r"a_3=a_2=-1",
        r"a_4=a_3=-1",
        r"a_5=a_4=-1",
        r"a_2^3-a_5+a_6=0",
        r"a_6=a_5-a_2^3=-1-(-1)^3=0",
        r"Y=F(X)=\sum_{n=0}^{\infty}a_nX^n",
        r"X^1:\qquad a_1=0",
        r"X^2:\qquad1+a_2=0",
        r"a_3=-5",
        r"a_4=5a_3=-25",
        r"a_5&=-a_3-2a_2a_3+5a_4",
        r"F=-X^2-5X^3-25X^4-130X^5+\ldots",
    ]
    missing_solution_math = [token for token in solution_protected if normalized_math(token) not in normalized_solutions]
    require(not missing_solution_math, f"protected public-solution mathematics absent: {missing_solution_math}")

    ast_receipts: dict[str, Any] = {}
    expected_ast = {
        "lecture-25.md": (10, 201, 0),
        "worksheet-25.md": (17, 67, 0),
        "worksheet-25-solutions.md": (3, 27, 0),
        "media-credits-unit-25.md": (1, 0, 0),
    }
    global_header_ids: list[str] = []
    for name, (header_count, math_count, image_count) in expected_ast.items():
        ast = pandoc_ast(SOURCE / name)
        nodes = list(walk(ast.get("blocks", [])))
        headers_ast = [node for node in nodes if node.get("t") == "Header"]
        maths = [node for node in nodes if node.get("t") == "Math"]
        images = [node for node in nodes if node.get("t") == "Image"]
        header_ids = [node["c"][1][0] for node in headers_ast]
        require(all(header_ids) and len(header_ids) == len(set(header_ids)), f"AST header IDs: {name}")
        require((len(headers_ast), len(maths), len(images)) == (header_count, math_count, image_count), f"AST topology: {name}")
        global_header_ids.extend(header_ids)
        ast_receipts[name] = {
            "headers": len(headers_ast),
            "math_nodes": len(maths),
            "images": len(images),
            "stable_header_ids": len(header_ids),
            "pandoc_warnings": 0,
        }
    require(len(global_header_ids) == 31 and len(global_header_ids) == len(set(global_header_ids)), "global AST stable-ID topology")

    return {
        "source_and_control_facts": facts,
        "source_edition": "Osnabrück 2012",
        "stable_ids": len(stable_ids),
        "lecture_stable_ids": len(lecture_ids),
        "lecture_semantic_entities": len(lecture_comments),
        "lecture_visible_correction_notes": 3,
        "worksheet_exercise_entities": len(worksheet_comments),
        "exercises": 13,
        "warm_up_exercises": 5,
        "submitted_exercises": 7,
        "upload_exercises": 1,
        "submitted_points": {str(index): value for index, value in zip(range(6, 13), [4, 4, 4, 3, 4, 4, 5])},
        "upload_points": {"displayed": 4, "authored": 3},
        "starred_exercises": [1, 2],
        "public_solutions": [1, 2],
        "invented_solutions": 0,
        "reader_images": 0,
        "ast": ast_receipts,
        "visible_german_residue": 0,
        "placeholder_count": 0,
        "secret_like_count": 0,
        "invisible_unicode_controls": 0,
        "protected_lecture_math_checks": len(lecture_protected),
        "protected_worksheet_math_checks": len(worksheet_protected),
        "protected_solution_math_checks": len(solution_protected),
        "terminology_bindings": TERM_IDS,
        "correction_bindings": CORRECTION_IDS,
        "visible_correction_disclosures": list(disclosures),
        "revision_contributors": {
            "lecture_root": "Arbota",
            "worksheet_root": "Arbota",
            "solution_25_1": "Bocardodarapti",
            "solution_25_2": "Arbota",
        },
    }


def main() -> int:
    receipt = {
        "schema": "ag-bridge-unit-translation-qa-v1",
        "status": "PASS",
        "unit": 25,
        "verified_date": "2026-08-26",
        "authority": verify_authority(),
        "media_and_rights": verify_media_and_rights(),
        "translation": verify_translation(),
        "provenance": MODEL,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "unit": 25, "receipt": OUT.relative_to(ROOT).as_posix(), "bytes": OUT.stat().st_size, "sha256": digest(OUT)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
