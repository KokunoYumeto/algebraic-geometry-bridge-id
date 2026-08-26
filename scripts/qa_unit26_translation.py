#!/usr/bin/env python3
"""Fail-closed authority, translation, mathematics, accessibility, and rights QA for Unit 26."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import struct
import subprocess
import unicodedata
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "authority" / "wikiversity" / "unit-26"
SOURCE = ROOT / "source" / "id-ID"
OUT = ROOT / "qa" / "UNIT_26_TRANSLATION_QA.json"
MODEL_BASE = "OpenAI Codex gpt-5.6-sol, Ultra"
MODEL = f"{MODEL_BASE}."

MANIFEST_FACT = (118791, "981fa3c86534514215c722b6d4f6d711c040a7829465f20ae18940373f94763c")
MAP_FACT = (13814, "efa1d77d8b594a24078097f3595c0ae8078d9735dfe7d2b3abb05392d7340423")
AUTHORITY_QA_FACT = (2621, "f29ef929df95410f21752e5fc1c08ed01995cb94fc77cc5598b96dc04c1e2c1a")
FREEZE_FACT = (2805, "9ebab81986fe8b1b2bc91174417ad27086816eabe8e635d183a53e6d689b80cb")
SOURCE_FACTS = {
    "source/id-ID/lecture-26.md": (21417, "1119ca7a9079dcc2bd1712c63067d08a32f74a031d6e140334208986461d51a6"),
    "source/id-ID/worksheet-26.md": (7267, "e18bae8b225872c2cb3f9dffc91af5a9d7824282a2d74af55bba0934d08acfd8"),
    "source/id-ID/worksheet-26-solutions.md": (3349, "4fe47d14fea117addf9256a9160d74afb0345c7ebe3adeb750ef531a609b610c"),
    "source/id-ID/media-credits-unit-26.md": (2446, "65abf73c3a1d2555f577d97599080b5e9baa96a80c5f7cf5674961ff0f508c16"),
    "source/id-ID/frontmatter-units-01-26.md": (4616, "b65af08094e4aa4031061ccf7a8359142dab032e28e9a2f051e9b652c92a3108"),
}
CONTROL_FACTS = {
    "00_control/TERMINOLOGY.csv": (35577, "d1305f559dcc00ac315f41905d1e672d557b30bc05aa3f6022b965a9b7f885a4"),
    "00_control/CORRECTIONS.csv": (69517, "9a73c0a59edd173732bf2c01d567c1912b427d402a2540b619ac948fc099d8a5"),
}
MEDIA_FACTS = {
    "authority/RIGHTS-unit-26.csv": (1277, "a03f4a998630ab426068253033abe3830cbb1d7a9caf03901b2254eb83d2e42b"),
    "authority/ASSET_CLOSURE-unit-26.json": (5850, "18b1600f93fbd49a6d68f5d54ab45060f1911f3266da4b933dcbcd96b22f798f"),
    "authority/assets/250px-Intersect3.png": (5922, "b29c15edf6619632fe033e0b6064c1826226abce0be6219262ca028a2a157818"),
    "authority/artifacts/lecture-26-official.pdf": (89958, "9ec109463f2fe8f00ca9d3f6edb6f3a604d8c5c6f79ed5dd6584d41456da10c7"),
    "authority/artifacts/worksheet-26-official.pdf": (34715, "4b1dc786752f41daa80031e8563ba0446e2d1a6c039798779fd0681f617f1c92"),
}
TERM_IDS = [f"AGT-{number:04d}" for number in range(221, 230)]
CORRECTION_IDS = [f"AGC-CORR-{number:04d}" for number in range(97, 108)]
LECTURE_ENTITIES = [
    "Ebene algebraische Kurven/Schnittmultiplizität/Lokale und semilokale Beschreibung/Einführung/Textabschnitt",
    "Ebene algebraische Kurven/Schnittmultiplizität/Restdimension ist endlich/Fakt",
    "Ebene algebraische Kurven/Schnittmultiplizität/Restdimension ist endlich/Fakt/Beweis",
    "Ebene algebraische Kurven/Schnittmultiplizität/Restdimension/Definition",
    "Ebene algebraische Kurven/Schnittmultiplizität/Restdimension/Schnitt mit Gerade/Beispiel",
    "Ebene algebraische Kurven/Schnittmultiplizität/Schnitt mit Gerade/Abschätzung zur Multiplizität/Fakt",
    "Ebene algebraische Kurven/Schnittmultiplizität/Schnitt mit Gerade/Abschätzung zur Multiplizität/Fakt/Beweis",
    "Ebene algebraische Kurven/Schnittmultiplizität/Erste Eigenschaften/Fakt",
    "Ebene algebraische Kurven/Schnittmultiplizität/Transversaler Schnitt/Definition",
    "Ebene algebraische Kurven/Schnittmultiplizität/Charakterisierung Transversaler Schnitt/Fakt",
    "Ebene algebraische Kurven/Schnittmultiplizität/Charakterisierung Transversaler Schnitt/Fakt/Beweis",
    "Ebene algebraische Kurven/Schnittmultiplizität/Summenformel für Schnittmultiplizität/Fakt",
    "Ebene algebraische Kurven/Schnittmultiplizität/Summenformel für Schnittmultiplizität/Fakt/Beweis",
    "Noetherscher Nulldimensionaler Ring/Produktdarstellung/Fakt",
    "Noetherscher Nulldimensionaler Ring/Produktdarstellung/Fakt/Beweis",
    "Ebene algebraische Kurve/Schnitt von Kurven ohne gemeinsame Komponente/Beschreibung als Produktring/Fakt",
    "Ebene algebraische Kurve/Schnitt von Kurven ohne gemeinsame Komponente/Beschreibung als Produktring/Fakt/Beweis",
    "Ebene algebraische Kurve/Schnittmultiplizität/Summe der Multiplizitäten ist Restklassendimension/Fakt",
    "Ebene algebraische Kurve/Schnittmultiplizität/Summe der Multiplizitäten ist Restklassendimension/Fakt/Beweis",
    "Ebene algebraische Kurven/Schnittmultiplizität/Abschätzung von Schnittmultiplizität und Multiplizität/Fakt",
    "Ebene algebraische Kurven/Schnittmultiplizität/Abschätzung von Schnittmultiplizität und Multiplizität/Fakt/Beweisverweis",
]
LECTURE_IDS = [
    "br-ak-2012-l26", "br-ak-2012-l26-s01",
    "br-ak-2012-l26-lem-01", "br-ak-2012-l26-lem-01-proof",
    "br-ak-2012-l26-def-01", "br-ak-2012-l26-ex-01",
    "br-ak-2012-l26-lem-02", "br-ak-2012-l26-lem-02-proof",
    "br-ak-2012-l26-lem-03", "br-ak-2012-l26-def-02",
    "br-ak-2012-l26-lem-04", "br-ak-2012-l26-lem-04-proof",
    "br-ak-2012-l26-thm-01", "br-ak-2012-l26-thm-01-proof",
    "br-ak-2012-l26-thm-02", "br-ak-2012-l26-thm-02-proof",
    "br-ak-2012-l26-cor-01", "br-ak-2012-l26-cor-01-proof",
    "br-ak-2012-l26-thm-03", "br-ak-2012-l26-thm-03-proof",
    "br-ak-2012-l26-thm-04", "br-ak-2012-l26-thm-04-proof-reference",
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
    manifest_fact = check_fact("authority/wikiversity/unit-26/UNIT_AUTHORITY_MANIFEST.json", MANIFEST_FACT)
    map_fact = check_fact("authority/wikiversity/unit-26/ORDERED_EXERCISE_MAP.json", MAP_FACT)
    authority_qa_fact = check_fact("qa/UNIT_26_AUTHORITY_QA.json", AUTHORITY_QA_FACT)
    freeze_fact = check_fact("authority/UNIT_26_AUTHORITY_FREEZE.md", FREEZE_FACT)
    manifest = json.loads((AUTH / "UNIT_AUTHORITY_MANIFEST.json").read_text(encoding="utf-8"))
    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    authority_qa = json.loads((ROOT / "qa" / "UNIT_26_AUTHORITY_QA.json").read_text(encoding="utf-8"))

    require(authority_qa["result"] == "PASS" and authority_qa["unit"] == 26, "authority QA state")
    require(authority_qa["authority_manifest"] == {
        "path": "authority/wikiversity/unit-26/UNIT_AUTHORITY_MANIFEST.json",
        "bytes": MANIFEST_FACT[0], "sha256": MANIFEST_FACT[1],
    }, "authority QA manifest binding")
    require(authority_qa["authority_freeze_note"] == {
        "path": "authority/UNIT_26_AUTHORITY_FREEZE.md",
        "bytes": FREEZE_FACT[0], "sha256": FREEZE_FACT[1],
    }, "authority QA freeze binding")
    require(authority_qa["local_inventory"] == {"files": 58, "bytes": 741361}, "authority local inventory")
    require(authority_qa["bounded_external_inventory"] == {"files": 5, "bytes": 137722}, "authority external inventory")
    require(authority_qa["entry_revisions"] == {"course": 658236, "lecture": 793526, "worksheet": 793494}, "authority entry revisions")
    require(authority_qa["recursive_pages_with_roots"] == {"lecture": 119, "worksheet": 58, "solution_04": 10}, "authority closure topology")
    require(authority_qa["canonical_identity_rows_sha256"] == {
        "lecture": "f1a064c0531f9079633a57009c565f20a0520a0ef10cb2336ad3b52aa2d331b8",
        "worksheet": "158fd9f6495ee9763d9e01cc1c0969a6be7c8b194dd88c4f8b12edbad900211f",
        "solution-04": "8fd91e101676ccbe314c5905bb2ac8ccbf457c5d629962206124b6878c212d30",
    }, "authority canonical topology")
    require(authority_qa["exercise_count"] == 11, "authority exercise count")
    require(authority_qa["roles"] == {"warm_up": [1, 2, 3, 4], "submitted": [5, 6, 7, 8, 9, 10, 11], "upload": []}, "authority roles")
    require(authority_qa["submitted_displayed_points"] == [4, 4, 4, 4, 4, 3, 8], "authority points")
    require(authority_qa["starred_numbers"] == [4], "authority stars")
    require(authority_qa["public_solution_numbers"] == [4], "authority public solution")
    require(authority_qa["negative_solution_numbers"] == [1, 2, 3, 5, 6, 7, 8, 9, 10, 11], "authority negative solutions")
    require(authority_qa["reader_media_positions"] == 1 and authority_qa["official_pdf_pages"] == [7, 2], "authority media/PDF topology")
    require(authority_qa["final_live_identity_replay"] == {
        "semantic_wikiversity": 157, "local_wikiversity_pdfs": 2, "commons_media": 1,
    }, "authority final replay")

    require(manifest["schema"] == "brenner-unit-authority-freeze-v2" and manifest["unit_number"] == 26, "manifest schema/unit")
    require(manifest["source_course"] == "Kurs:Algebraische Kurven (Osnabrück 2012)", "course identity")
    require(manifest["source_course_license"] == "CC BY-SA 4.0", "course licence")
    route = manifest["source_component_license_route"]
    require(route["semantic_site_rights"]["notice"] == "CC BY-SA 4.0", "semantic rights")
    require(route["official_pdf_legacy_notice"] == "CC BY-SA 2.0 Germany", "legacy PDF rights")
    require(route["official_pdf_current_print_version_notice"] == "CC BY-SA 4.0", "current PDF rights")
    require(route["no_blanket_relicensing_claim"] is True, "no blanket relicensing")
    require(
        (manifest["lecture"]["pageid"], manifest["lecture"]["revid"], manifest["lecture"]["mediawiki_sha1"], manifest["lecture"]["xml_sha256"])
        == (50732, 793526, "57845c7bb535d0cccde6d289409a8dbbe684f2d8", "cc6a483e01e22db4262c3e400325ec22c4cf8750e3a1a8c11043398368f40ff9"),
        "lecture identity/XML",
    )
    require(
        (manifest["worksheet"]["pageid"], manifest["worksheet"]["revid"], manifest["worksheet"]["mediawiki_sha1"], manifest["worksheet"]["xml_sha256"])
        == (50761, 793494, "10aad7862403732dbaa5a05ae637a084c2758751", "b5cc1634fba66dca202dec1947c17adf55182effecb80e3f298bf597e1535e78"),
        "worksheet identity/XML",
    )
    require([(row["bytes"], row["sha256"]) for row in manifest["derived_expanded_tex"]] == [
        (23994, "567968794b07d9e045813a62921dc8b527e99f500807bff843bd7cb498ea8ee7"),
        (5011, "2959064d81372593e3a7c619b0753d0be90dde49318262a5995e2b4abccfce71"),
    ], "expanded TeX identities")
    require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 118, "lecture closure")
    require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 57, "worksheet closure")
    require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "lecture missing dependency")
    require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "worksheet missing dependency")
    require(manifest["transclusion_topology"]["lecture"]["with_root"] == 119, "lecture root topology")
    require(manifest["transclusion_topology"]["worksheet"]["with_root"] == 58, "worksheet root topology")
    require(manifest["transclusion_topology"]["lecture"]["canonical_identity_rows_sha256"] == "f1a064c0531f9079633a57009c565f20a0520a0ef10cb2336ad3b52aa2d331b8", "lecture rows hash")
    require(manifest["transclusion_topology"]["worksheet"]["canonical_identity_rows_sha256"] == "158fd9f6495ee9763d9e01cc1c0969a6be7c8b194dd88c4f8b12edbad900211f", "worksheet rows hash")

    require(len(manifest["files"]) == 58 and sum(row["bytes"] for row in manifest["files"]) == 741361, "manifest local inventory")
    for row in manifest["files"]:
        path = AUTH / row["file"]
        require(path.is_file() and path.stat().st_size == row["bytes"] and digest(path) == row["sha256"], f"authority replay: {row['file']}")
    require(len(manifest["bounded_external_files"]) == 5 and sum(row["bytes"] for row in manifest["bounded_external_files"]) == 137722, "manifest external inventory")
    for row in manifest["bounded_external_files"]:
        path = ROOT / row["file"]
        require(path.is_file() and path.stat().st_size == row["bytes"] and digest(path) == row["sha256"], f"external replay: {row['file']}")

    require(mapping["schema"] == "brenner-worksheet-solution-map-v2" and mapping["unit"] == 26, "map schema/unit")
    require(mapping["exercise_count"] == 11 and mapping["solution_count"] == 1, "map counts")
    require([row["exercise_number"] for row in mapping["entries"]] == list(range(1, 12)), "map exercise order")
    topology = mapping["ordered_role_point_and_star_topology"]
    require(topology["warm_up_numbers"] == [1, 2, 3, 4], "warm-up topology")
    require(topology["submitted_numbers"] == [5, 6, 7, 8, 9, 10, 11] and topology["upload_numbers"] == [], "submitted/upload topology")
    authored = [2, 2, 3, 4, 4, 4, 4, 4, 4, 3, 8]
    require(topology["authored_points"] == {str(i): value for i, value in enumerate(authored, 1)}, "authored points")
    require(topology["displayed_points"] == {"3": 3, "5": 4, "6": 4, "7": 4, "8": 4, "9": 4, "10": 3, "11": 8}, "displayed points")
    require(topology["submitted_displayed_point_total"] == 31 and topology["starred_numbers"] == [4], "point total/star")
    require([row["role"] for row in mapping["entries"]] == ["warm-up"] * 4 + ["submitted"] * 7, "entry roles")
    require([row["authored_points"] for row in mapping["entries"]] == authored, "entry authored points")
    solutions = [row for row in mapping["entries"] if row["has_public_solution"]]
    require(len(solutions) == 1, "single public solution")
    solution = solutions[0]
    require((solution["exercise_number"], solution["pageid"], solution["revid"], solution["mediawiki_sha1"], solution["xml_sha256"]) ==
            (4, 21344, 1112503, "82d108d8f5b167d377b1f0a2ec03fa72073786d2", "d80e1ff03f562cdde8bfc9776ff56a7d1dfd364cf2c819d9d3187a5e91528ec0"), "solution identity")
    closure = manifest["public_solution_transclusion_closures"]
    require(len(closure) == 1 and closure[0]["exercise_number"] == 4, "solution closure order")
    require(closure[0]["recursive_transclusion_closure"]["captured_page_count"] == 9, "solution dependencies")
    require(closure[0]["recursive_transclusion_closure"]["missing_page_count"] == 0, "solution missing dependencies")
    require(closure[0]["topology"]["with_root"] == 10, "solution with-root topology")
    require(closure[0]["topology"]["canonical_identity_rows_sha256"] == "8fd91e101676ccbe314c5905bb2ac8ccbf457c5d629962206124b6878c212d30", "solution rows hash")
    negative = mapping["negative_public_solution_evidence"]
    require(negative["exact_candidate_title_count"] == 11 and negative["positive_numbers"] == [4], "candidate solutions")
    require(negative["negative_numbers"] == [1, 2, 3, 5, 6, 7, 8, 9, 10, 11] and negative["negative_count"] == 10, "negative solution evidence")
    require(all(row["api_missing"] is True for row in negative["entries"]), "negative solution API states")
    require(mapping["point_discrepancies"] == [], "unexpected point discrepancy")

    witnesses = manifest["official_pdf_witnesses"]
    require([row["kind"] for row in witnesses] == ["lecture", "worksheet"], "PDF witness order")
    require([(row["local_bytes"], row["local_sha256"], row["page_count"]) for row in witnesses] == [
        (89958, MEDIA_FACTS["authority/artifacts/lecture-26-official.pdf"][1], 7),
        (34715, MEDIA_FACTS["authority/artifacts/worksheet-26-official.pdf"][1], 2),
    ], "PDF identities/pages")
    live = manifest["final_live_identity_replay"]
    require(live["result"] == "PASS" and live["semantic_unique_identity_count"] == 157, "semantic live replay")
    require(sum(row["title_count"] for row in live["semantic_batches"]) == 157, "live batch total")
    require(live["local_wikiversity_pdf_identity_count"] == 2 and live["commons_media_identity_count"] == 1, "live binary replay")
    require(live["latest_solution_identity_replayed"] == {
        "exercise_number": 4, "revid": 1112503, "timestamp": "2026-08-21T15:27:54Z",
        "mediawiki_sha1": "82d108d8f5b167d377b1f0a2ec03fa72073786d2",
    }, "latest solution replay")

    freeze = (ROOT / "authority" / "UNIT_26_AUTHORITY_FREEZE.md").read_text(encoding="utf-8")
    require("Exactly 11 exercises are preserved in order" in freeze, "freeze exercise closure")
    require("Exercise 4 is starred and is the only public solution" in freeze, "freeze solution closure")
    require("one substantive static reader image" in freeze and "CC BY-SA 3.0" in freeze, "freeze image/rights boundary")
    require("157 unique semantic identities" in freeze and "no blanket relicensing claim" in freeze, "freeze replay/licence boundary")
    return {
        "manifest": manifest_fact,
        "exercise_map": map_fact,
        "authority_qa": authority_qa_fact,
        "authority_freeze": freeze_fact,
        "source_course": "Kurs:Algebraische Kurven (Osnabrück 2012)",
        "lecture_revid": 793526,
        "worksheet_revid": 793494,
        "lecture_transclusions_exact": 118,
        "worksheet_transclusions_exact": 57,
        "lecture_with_root": 119,
        "worksheet_with_root": 58,
        "exercises": 11,
        "public_solution_numbers": [4],
        "negative_solution_numbers": [1, 2, 3, 5, 6, 7, 8, 9, 10, 11],
        "solution_revision": 1112503,
        "solution_recursive_closure": 9,
        "solution_with_root": 10,
        "authority_files_verified": 58,
        "bounded_external_files_verified": 5,
        "live_semantic_wikiversity_identities": 157,
        "live_local_wikiversity_pdf_identities": 2,
        "live_commons_media_identities": 1,
    }


def verify_media_and_rights() -> dict[str, Any]:
    facts = [check_fact(relative, expected) for relative, expected in MEDIA_FACTS.items()]
    with (ROOT / "authority" / "RIGHTS-unit-26.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 1, "exactly one rights row")
    rights = rows[0]
    require(rights["asset_id"] == "br-ak-u26-media-001" and rights["resource_title"] == "File:Intersect3.png", "rights asset identity")
    require(rights["local_path"] == "authority/assets/250px-Intersect3.png", "rights local path")
    require((int(rights["local_bytes"]), rights["local_sha256"]) == MEDIA_FACTS["authority/assets/250px-Intersect3.png"], "rights local bytes")
    require((int(rights["local_width"]), int(rights["local_height"]), int(rights["frame_count"])) == (250, 249, 1), "rights dimensions")
    require((int(rights["original_bytes"]), rights["original_sha1"], int(rights["original_width"]), int(rights["original_height"])) ==
            (5018, "26fef135fcc9d950958068778e5805830ffa8b8e", 400, 399), "rights original identity")
    require(rights["license_short"] == "CC BY-SA 3.0" and rights["attribution_required"] == "true", "component licence")
    require(rights["uploader"] == "Maksim" and rights["source_course_creator"] == "Holger Brenner / Wikiversity course page", "component attribution")

    closure = json.loads((ROOT / "authority" / "ASSET_CLOSURE-unit-26.json").read_text(encoding="utf-8"))
    require(closure["schema"] == "brenner-unit-media-closure-v2" and closure["unit"] == 26, "closure identity")
    require(closure["authority_only_boundary"] is True, "closure authority boundary")
    require((closure["reader_media_positions"], closure["animated_html_positions"], closure["unique_local_assets"]) == (1, 0, 1), "closure topology")
    require((closure["rights_bytes"], closure["rights_sha256"]) == MEDIA_FACTS["authority/RIGHTS-unit-26.csv"], "closure rights binding")
    require(closure["reader_credits_required"] is True and closure["official_pdf_witnesses_are_not_media_positions"] is True, "credits/PDF separation")
    require(closure["accessibility"]["reader_media_alt_or_caption_required"] is True, "alt/caption requirement")
    require(closure["accessibility"]["planned_caption_id"] == "br-ak-u26-media-001-caption", "caption identity")
    require(closure["accessibility"]["planned_alt_id"] == "br-ak-u26-media-001-alt", "alt identity")
    require(len(closure["assets"]) == 1, "single closure asset")
    asset = closure["assets"][0]
    require(asset["asset_id"] == "br-ak-u26-media-001" and asset["resource_title"] == "File:Intersect3.png", "closure asset identity")
    require((asset["local_bytes"], asset["local_sha256"], asset["width"], asset["height"], asset["frame_count"]) ==
            (5922, MEDIA_FACTS["authority/assets/250px-Intersect3.png"][1], 250, 249, 1), "closure local asset")
    require(asset["license_short"] == "CC BY-SA 3.0" and asset["attribution_required"] is True, "closure asset rights")
    pdf_rights = closure["official_pdf_component_rights"]
    require([row["local_path"] for row in pdf_rights] == ["authority/artifacts/lecture-26-official.pdf", "authority/artifacts/worksheet-26-official.pdf"], "PDF rights order")
    require([(row["source_bytes"], row["source_sha1"]) for row in pdf_rights] == [
        (89958, "1b27e2c5d0bf430250d722751382ee3fdb129c6b"),
        (34715, "5b91dec48ec4ae9a1fae3a8e227c570ff3361e3f"),
    ], "PDF source identity")
    require(all(row["component_license_route"]["current_print_version_notice"] == "CC BY-SA 4.0" for row in pdf_rights), "PDF current rights")
    require(all(row["component_license_route"]["legacy_file_notice"] == "CC BY-SA 2.0 Germany" for row in pdf_rights), "PDF legacy rights")
    require(all(row["component_license_route"]["embedded_pdf_label"] is None for row in pdf_rights), "embedded PDF label")
    surfaces = closure["accessibility"]["official_pdf_surfaces"]
    require(all(row["encrypted"] is False for row in surfaces), "PDF encryption")
    require(all(row["tagged_pdf"] is False and row["structure_tree_present"] is False for row in surfaces), "PDF tags/structure")
    require(all(row["document_language"] is None and row["outline_or_bookmark_count"] == 0 for row in surfaces), "PDF language/outline")
    for relative in ("authority/artifacts/lecture-26-official.pdf", "authority/artifacts/worksheet-26-official.pdf"):
        require((ROOT / relative).read_bytes().startswith(b"%PDF-"), f"PDF signature: {relative}")
    png = (ROOT / "authority" / "assets" / "250px-Intersect3.png").read_bytes()
    require(png.startswith(b"\x89PNG\r\n\x1a\n") and png[12:16] == b"IHDR", "PNG signature/IHDR")
    require(struct.unpack(">II", png[16:24]) == (250, 249), "PNG dimensions")

    lecture = (SOURCE / "lecture-26.md").read_text(encoding="utf-8")
    images = re.findall(r"!\[([^\]]+)\]\(([^)]+)\)", lecture)
    require(images == [("Sebuah lingkaran dan sebuah kurva yang bersinggungan di sebelah kiri serta berpotongan melintang di sebelah kanan", "authority/assets/250px-Intersect3.png")], "reader image/alt/path")
    credits = (SOURCE / "media-credits-unit-26.md").read_text(encoding="utf-8")
    require("Michael Larsen" in credits and "Maksim" in credits, "creator/uploader credits")
    require("CC BY-SA 3.0" in credits and "CC BY-SA 2.0 Germany" in credits and "CC BY-SA 4.0" in credits, "component rights disclosure")
    require("tujuh halaman" in credits and "dua halaman" in credits, "PDF page disclosure")
    require("tidak bertag" in credits and "tidak mempunyai pohon struktur" in credits, "accessibility disclosure")
    require("tidak\nmemberikan lisensi payung" in credits, "no blanket relicensing disclosure")
    require(credits.count(MODEL_BASE) == 1, "credits provenance")
    return {
        "reader_media_positions": 1,
        "binary_assets": 1,
        "rights_rows": 1,
        "reader_alt_texts": 1,
        "official_pdf_witnesses": 2,
        "official_pdf_pages": [7, 2],
        "official_pdf_tagged": [False, False],
        "component_licences": ["CC BY-SA 3.0", "CC BY-SA 4.0", "CC BY-SA 2.0 Germany"],
        "facts": facts,
    }


def verify_translation() -> dict[str, Any]:
    facts = [check_fact(relative, expected) for relative, expected in SOURCE_FACTS.items()]
    facts.extend(check_fact(relative, expected) for relative, expected in CONTROL_FACTS.items())
    lecture = (SOURCE / "lecture-26.md").read_text(encoding="utf-8")
    worksheet = (SOURCE / "worksheet-26.md").read_text(encoding="utf-8")
    solutions = (SOURCE / "worksheet-26-solutions.md").read_text(encoding="utf-8")
    credits = (SOURCE / "media-credits-unit-26.md").read_text(encoding="utf-8")
    frontmatter = (SOURCE / "frontmatter-units-01-26.md").read_text(encoding="utf-8")
    unit_text = "\n".join((lecture, worksheet, solutions, credits))
    all_text = unit_text + "\n" + frontmatter

    for name, raw in (("lecture", lecture), ("worksheet", worksheet), ("solutions", solutions)):
        require("language: id-ID" in raw, f"{name} language")
        require("translation_status: complete" in raw, f"{name} completion")
        require(raw.count(MODEL_BASE) == 1, f"{name} provenance")
        require("CC BY-SA 4.0" in raw, f"{name} semantic licence")
        require(MANIFEST_FACT[1] in raw, f"{name} manifest binding")
        require("Osnabrück 2012" in raw and "Holger Brenner" in raw, f"{name} source attribution")
    require("frozen_revision_contributor: \"Arbota\"" in lecture and "frozen_revision_contributor: \"Arbota\"" in worksheet, "root contributors")
    require("frozen_revision_contributors: \"Soal 26.4: Bocardodarapti\"" in solutions, "solution contributor")
    require("source_semantic_entities: 21" in lecture and "source_corrections: 6" in lecture, "lecture topology metadata")
    require("correction_ids: \"AGC-CORR-0097; AGC-CORR-0098; AGC-CORR-0099; AGC-CORR-0100; AGC-CORR-0104; AGC-CORR-0106\"" in lecture, "lecture correction metadata")
    require("source_corrections: 4" in worksheet and "source_discrepancies: 0" in worksheet, "worksheet correction metadata")
    require("correction_ids: \"AGC-CORR-0101; AGC-CORR-0103; AGC-CORR-0105; AGC-CORR-0107\"" in worksheet, "worksheet correction IDs")
    require("source_corrections: 1" in solutions and "correction_ids: \"AGC-CORR-0102\"" in solutions, "solution correction metadata")
    require("public_solution_count: 1" in solutions and "reader_media_positions: 1" in lecture and "reader_media_positions: 0" in worksheet, "solution/media metadata")
    require("cc6a483e01e22db4262c3e400325ec22c4cf8750e3a1a8c11043398368f40ff9" in lecture, "lecture XML binding")
    require("567968794b07d9e045813a62921dc8b527e99f500807bff843bd7cb498ea8ee7" in lecture, "lecture TeX binding")
    require("f1a064c0531f9079633a57009c565f20a0520a0ef10cb2336ad3b52aa2d331b8" in lecture, "lecture closure binding")
    require("b5cc1634fba66dca202dec1947c17adf55182effecb80e3f298bf597e1535e78" in worksheet, "worksheet XML binding")
    require("2959064d81372593e3a7c619b0753d0be90dde49318262a5995e2b4abccfce71" in worksheet, "worksheet TeX binding")
    require(MAP_FACT[1] in worksheet and MAP_FACT[1] in solutions, "map binding")
    require("d80e1ff03f562cdde8bfc9776ff56a7d1dfd364cf2c819d9d3187a5e91528ec0" in solutions, "solution XML binding")
    require("br-ak-2025-2026" not in unit_text, "wrong Unit26 stable-ID namespace")

    lower = all_text.casefold()
    require(all(token not in lower for token in ("todo", "fixme", "tbd", "placeholder", "lorem ipsum", "terjemahkan di sini")), "placeholder residue")
    require(not re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|access[_-]?token|bearer\s+[A-Za-z0-9._-]{20,}|api[_-]?key\s*[:=]", all_text, flags=re.I), "secret-like content")
    controls = [(char, f"U+{ord(char):04X}") for char in all_text if unicodedata.category(char) in {"Cc", "Cf"} and char not in "\t\n\r"]
    require(not controls, f"invisible/control Unicode: {controls[:5]}")
    unicode_dashes = [(char, f"U+{ord(char):04X}") for char in all_text if char in "‐‑‒–—―−"]
    require(not unicode_dashes, f"Unicode dash residue: {unicode_dashes[:5]}")

    prose_by_file = {
        "lecture": strip_nonprose(lecture), "worksheet": strip_nonprose(worksheet),
        "solutions": strip_nonprose(solutions), "credits": strip_nonprose(credits),
    }
    prose = "\n".join(prose_by_file.values())
    residue = re.findall(
        r"\b(?:Es sei|Zeige|Bestimme|Aufgabe|Beweis|Lösung|Schnittmultiplizität|Restdimension|Transversaler Schnitt|Produktdarstellung|Chinesischer Restsatz|Nullpunkt)\b",
        prose, flags=re.I,
    )
    require(not residue, f"visible German residue: {residue}")
    markers = {
        "lecture": ("misalkan", "dengan", "maka", "bukti", "sehingga"),
        "worksheet": ("misalkan", "tunjukkan", "tentukan", "dengan", "suatu"),
        "solutions": ("jika", "karena", "garis", "gelanggang", "berdimensi"),
        "credits": ("sumber", "edisi", "kontributor", "hak", "lisensi"),
    }
    for name, needles in markers.items():
        file_prose = prose_by_file[name].casefold()
        require(all(re.search(rf"\b{re.escape(needle)}\b", file_prose) for needle in needles), f"Indonesian markers: {name}")

    lecture_comments = re.findall(r"<!-- upstream_entity: (.*?) -->", lecture)
    require(lecture_comments == LECTURE_ENTITIES and len(lecture_comments) == 21, "ordered lecture entities")
    lecture_ids = re.findall(r"\{#(br-ak-2012-l26[^}\s]*)\}", lecture)
    require(lecture_ids == LECTURE_IDS and len(set(lecture_ids)) == 22, "lecture stable IDs")
    require(lecture.count("> **Catatan edisi -") == 6, "lecture edition notes")

    mapping = json.loads((AUTH / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    worksheet_comments = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet)
    require(worksheet_comments == [row["exercise_title"] for row in mapping["entries"]] and len(worksheet_comments) == 11, "ordered worksheet entities")
    headers = re.findall(r"^### Soal 26\.(\d+)(?:[^\n]*)\{#br-ak-2012-w26-ex-(\d{2})\}$", worksheet, flags=re.M)
    require(headers == [(str(index), f"{index:02d}") for index in range(1, 12)], "exercise headers/IDs")
    require([int(value) for value in re.findall(r"^### Soal 26\.(\d+) ★", worksheet, flags=re.M)] == [4], "star topology")
    points = re.findall(r"^### Soal 26\.(\d+) \(([^)]*poin[^)]*)\)", worksheet, flags=re.M)
    require(points == [(str(i), f"{value} poin") for i, value in [(3, 3), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 3), (11, 8)]], "displayed points")
    require(worksheet.index("### Soal 26.4") < worksheet.index("## Soal untuk dikumpulkan") < worksheet.index("### Soal 26.5"), "role boundary")
    require("## Soal untuk diunggah" not in worksheet, "unexpected upload section")
    require(worksheet.count("> **Catatan edisi -") == 4, "worksheet edition notes")

    solution_headers = [int(value) for value in re.findall(r"^## Solusi Soal 26\.(\d+) ", solutions, flags=re.M)]
    require(solution_headers == [4], "single solution heading")
    solution_comments = re.findall(r"<!-- upstream_solution: (.*?); pageid=(\d+); revid=(\d+) -->", solutions)
    require(solution_comments == [("Kartesisches Blatt/Schnittmultiplizität im Nullpunkt/Mit jeder Geraden/Aufgabe/Lösung", "21344", "1112503")], "solution identity comment")
    require(solutions.count("<!-- upstream_solution_url:") == 1 and "oldid=1112503" in solutions, "solution immutable URL")
    require(re.findall(r"\[Kembali ke Soal 26\.(\d+)\]\(#br-ak-2012-w26-ex-\d{2}\)", solutions) == ["4"], "solution backlink")
    require("Sepuluh calon halaman solusi lainnya" in solutions and "Tidak ada solusi tambahan yang dibuat" in re.sub(r"\s+", " ", solutions), "no invented solutions disclosure")
    require(not re.search(r"^## Solusi Soal 26\.(?:1|2|3|5|6|7|8|9|10|11)\b", solutions, flags=re.M), "invented solution heading")
    require(solutions.count("> **Catatan edisi -") == 1, "solution edition note")

    stable_by_file = {
        "lecture": re.findall(r"\{#([^}\s]+)\}", lecture),
        "worksheet": re.findall(r"\{#([^}\s]+)\}", worksheet),
        "solutions": re.findall(r"\{#([^}\s]+)\}", solutions),
        "credits": re.findall(r"\{#([^}\s]+)\}", credits),
    }
    require({name: len(ids) for name, ids in stable_by_file.items()} == {"lecture": 22, "worksheet": 14, "solutions": 2, "credits": 1}, "per-file stable IDs")
    stable_ids = [stable_id for values in stable_by_file.values() for stable_id in values]
    require(len(stable_ids) == 39 and len(stable_ids) == len(set(stable_ids)), "39 unique Unit26 stable IDs")
    require(sum(stable_id.startswith("br-ak-2012-") for stable_id in stable_ids) == 38, "38 course IDs")
    require(stable_ids[-1] == "agc-media-credits-unit-26", "media-credit stable ID")

    with (ROOT / "00_control" / "TERMINOLOGY.csv").open(encoding="utf-8", newline="") as stream:
        term_rows = {row["term_id"]: row for row in csv.DictReader(stream)}
    expected_terms = {
        "AGT-0221": ("Schnittmultiplizität", "multiplisitas perpotongan"),
        "AGT-0222": ("transversaler Schnitt", "perpotongan transversal"),
        "AGT-0223": ("gemeinsame Komponente", "komponen bersama"),
        "AGT-0224": ("gemeinsamer Primteiler", "pembagi prima bersama"),
        "AGT-0225": ("Restdimension", "dimensi hasil bagi"),
        "AGT-0226": ("an einem Punkt lokalisieren", "melokalkan pada titik"),
        "AGT-0227": ("Chinesischer Restsatz", "Teorema Sisa Cina"),
        "AGT-0228": ("Produktdarstellung", "dekomposisi produk"),
        "AGT-0229": ("Summenformel für Schnittmultiplizität", "rumus aditivitas multiplisitas perpotongan"),
    }
    require(list(expected_terms) == TERM_IDS, "terminology interval")
    for term_id, (source_term, target_term) in expected_terms.items():
        require(term_rows[term_id]["source_term"] == source_term, f"term source: {term_id}")
        require(term_rows[term_id]["preferred_target"] == target_term and term_rows[term_id]["status"] == "admitted", f"term target/status: {term_id}")
    flat = re.sub(r"\s+", " ", unit_text).casefold()
    term_visibility = {
        "AGT-0221": "multiplisitas perpotongan", "AGT-0222": "perpotongan transversal",
        "AGT-0223": "komponen bersama", "AGT-0224": "pembagi prima bersama",
        "AGT-0225": "dimensi hasil bagi", "AGT-0226": "melokalkan",
        "AGT-0227": "teorema sisa cina", "AGT-0228": "dekomposisi produk",
        "AGT-0229": "rumus aditivitas",
    }
    require(not [term_id for term_id, needle in term_visibility.items() if needle not in flat], "preferred terminology visibility")
    require(not re.search(r"\b(?:multiplikitas irisan|irisan melintang|komponen sekutu|faktor prima bersama|dimensi residu|melokalisasi pada titik|teorema residu cina|representasi produk|rumus jumlah multiplisitas perpotongan)\b", prose, flags=re.I), "nonpreferred terminology")

    with (ROOT / "00_control" / "CORRECTIONS.csv").open(encoding="utf-8", newline="") as stream:
        corrections = {row["correction_id"]: row for row in csv.DictReader(stream)}
    expected_kinds = {
        "AGC-CORR-0097": "source_case_and_localization_omission",
        "AGC-CORR-0098": "source_without_loss_step_omission",
        "AGC-CORR-0099": "source_undefined_symbol",
        "AGC-CORR-0100": "source_missing_finiteness_hypothesis",
        "AGC-CORR-0101": "source_missing_variety_operator",
        "AGC-CORR-0102": "source_line_classification_duplication",
        "AGC-CORR-0103": "editorial_geometric_scope_note",
        "AGC-CORR-0104": "source_invalid_cross_reference",
        "AGC-CORR-0105": "source_common_component_scope_omission",
        "AGC-CORR-0106": "source_free_point_symbol",
        "AGC-CORR-0107": "source_degenerate_common_component_case",
    }
    require(list(expected_kinds) == CORRECTION_IDS, "correction interval")
    for correction_id, kind in expected_kinds.items():
        require(corrections[correction_id]["kind"] == kind, f"correction kind: {correction_id}")
        require(corrections[correction_id]["status"] == "applied_at_unit_26_translation", f"correction status: {correction_id}")
        require(unit_text.count(correction_id) == 1, f"correction metadata count: {correction_id}")

    normalized_lecture = normalized_math(lecture)
    normalized_worksheet = normalized_math(worksheet)
    normalized_solutions = normalized_math(solutions)
    disclosures = {
        "AGC-CORR-0097": "cabang eliminasi dan pelokalan" in lecture and all(normalized_math(token) in normalized_lecture for token in (r"d\ne0", r"K[X]_{(X-a)}/(\widetilde F)", r"d=0", r"c\ne0", r"(Y-b)")),
        "AGC-CORR-0098": "pilihan koordinat dalam bukti" in lecture and "Tanpa mengurangi keumuman, andaikan $b\\ne0$".replace("\\\\", "\\") in lecture and "menukar $X$ dengan $Y$" in lecture,
        "AGC-CORR-0099": "simbol gelanggang dalam bukti" in lecture and normalized_math(r"K[X,Y]/(F,G)") in normalized_lecture,
        "AGC-CORR-0100": "hipotesis keterhinggaan" in lecture and "dua polinom tanpa komponen bersama" in lecture,
        "AGC-CORR-0101": "simbol himpunan nol" in worksheet and normalized_math(r"D=V\left(X^r-Y^s\right)") in normalized_worksheet,
        "AGC-CORR-0102": "daftar garis melalui titik asal" in solutions and normalized_math(r"V(Y-aX),\qquad a\in K") in normalized_solutions and "garis vertikal $V(X)$" in solutions,
        "AGC-CORR-0103": "lingkup geometris" in worksheet and normalized_math(r"r>0") in normalized_worksheet and normalized_math(r"D=V\left(X^2+(Y-r)^2-r^2\right)") in normalized_worksheet,
        "AGC-CORR-0104": "perbaikan bukti arah balik" in lecture and normalized_math(r"(F,G)=\mathfrak m_P") in normalized_lecture and normalized_math(r"\mathfrak m_P/\mathfrak m_P^2") in normalized_lecture and "bebas linear" in lecture,
        "AGC-CORR-0105": "syarat keterhinggaan" in worksheet and "dua kurva aljabar bidang tanpa komponen bersama" in worksheet and "citra taknol $G$" in worksheet,
        "AGC-CORR-0106": "pengikatan titik" in lecture and normalized_math(r"P\in\mathbb A_K^2") in normalized_lecture and "Di luar titik perpotongan" in lecture,
        "AGC-CORR-0107": "kasus komponen bersama" in worksheet and "bukan komponen" in worksheet and normalized_math(r"d=e=1") in normalized_worksheet,
    }
    require(all(disclosures.values()), f"missing correction disclosure: {[key for key, value in disclosures.items() if not value]}")

    lecture_math = [
        r"C,D\subseteq\mathbb A_K^2", r"P\in C\cap D", r"C=V(F)", r"D=V(G)",
        r"R=K[X,Y]_{\mathfrak m_P}", r"\mathfrak m^s\subseteq(F,G)\subseteq\mathfrak m",
        r"\dim_K\left(K[X,Y]_{\mathfrak m_P}/(F,G)\right)", r"L=V(cX+dY)",
        r"Y=-\frac cdX", r"\widetilde F(X)=F\left(X,-\frac cdX\right)",
        r"K[X]_{(X-a)}/(\widetilde F)", r"\operatorname{mult}_P\bigl(L,V(F)\bigr)\geq m_P(F)=m",
        r"R/(F,H)\cong K[X]_{(X)}/\bigl(F_m(X,cX)+\cdots+F_d(X,cX)\bigr)",
        r"\operatorname{mult}_P(F,G)=\operatorname{mult}_P(G,F)",
        r"\operatorname{mult}_P(F,G)=\operatorname{mult}_P(F,G+HF)",
        r"\operatorname{mult}_P\bigl(V(F),V(G)\bigr)=1", r"B=R/(F)",
        r"G=X+H", r"H\in\mathfrak m_P^2", r"(F,G)=\mathfrak m_P",
        r"F=\prod_{i=1}^{m}F_i^{\nu_i}", r"G=\prod_{j=1}^{n}G_j^{\mu_j}",
        r"\operatorname{mult}_P(F,G)=\sum_{i,j}\nu_i\mu_j\operatorname{mult}_P(F_i,G_j)",
        r"R\cong R_{\mathfrak m_1}\times\cdots\times R_{\mathfrak m_n}",
        r"\mathfrak a=\bigcap_i\mathfrak m_i", r"\mathfrak a_1\cdots\mathfrak a_n=0",
        r"K[X,Y]/(F,G)\cong\prod_{i=1}^{n}\left(K[X,Y]_{\mathfrak m_i}/(F,G)\right)",
        r"\dim_K\bigl(K[X,Y]/(F,G)\bigr)=\sum_P\operatorname{mult}_P(F,G)",
        r"\operatorname{mult}_P(F,G)\geq m_P(F)\,m_P(G)",
    ]
    require(not [token for token in lecture_math if normalized_math(token) not in normalized_lecture], "protected lecture mathematics")
    worksheet_math = [
        r"y=2x^4+3x^2-x+1", r"P=(1,5)", r"C=V\left(X^d-Y^e\right)",
        r"C=V\left(X^3+Y^3-3XY\right)", r"C=V\left(X^5-Y^2\right)", r"D=V\left(X^7-Y^3\right)",
        r"R=K[X,Y]_{\mathfrak m_P}/(F)", r"\operatorname{mult}_P(F,G)=\operatorname{ord}(G)",
        r"C=V\left(Y-X^2\right)", r"D=V\left(X^2+(Y-r)^2-r^2\right)",
        r"\mathbb C[X,Y]/\left(XY-1,X^2+Y^2-a\right)",
        r"V\left(X^3+Y^3-3XY+1\right)", r"D=V\left(X^r-Y^s\right)",
    ]
    require(not [token for token in worksheet_math if normalized_math(token) not in normalized_worksheet], "protected worksheet mathematics")
    solution_math = [
        r"V(Y-aX)", r"V(X)", r"K[X,Y]_{(X,Y)}/(Y,X^3+Y^3-3XY)",
        r"K[X]_{(X)}/(X^3)", r"K[X,Y]_{(X,Y)}/(Y-aX,X^3+Y^3-3XY)",
        r"K[X]_{(X)}/\left(X^2\bigl(-3a+(1+a^3)X\bigr)\right)", r"K[X]_{(X)}/(X^2)",
    ]
    require(not [token for token in solution_math if normalized_math(token) not in normalized_solutions], "protected solution mathematics")

    expected_ast = {
        "lecture-26.md": (22, 257, 1), "worksheet-26.md": (14, 57, 0),
        "worksheet-26-solutions.md": (2, 32, 0), "media-credits-unit-26.md": (1, 0, 0),
        "frontmatter-units-01-26.md": (2, 0, 0),
    }
    ast_receipts: dict[str, Any] = {}
    unit_header_ids: list[str] = []
    for name, expected in expected_ast.items():
        ast = pandoc_ast(SOURCE / name)
        nodes = list(walk(ast.get("blocks", [])))
        headers_ast = [node for node in nodes if node.get("t") == "Header"]
        maths = [node for node in nodes if node.get("t") == "Math"]
        images = [node for node in nodes if node.get("t") == "Image"]
        ids = [node["c"][1][0] for node in headers_ast]
        require(all(ids) and len(ids) == len(set(ids)), f"AST header IDs: {name}")
        require((len(headers_ast), len(maths), len(images)) == expected, f"AST topology: {name}")
        if name != "frontmatter-units-01-26.md":
            unit_header_ids.extend(ids)
        ast_receipts[name] = {"headers": len(headers_ast), "math_nodes": len(maths), "images": len(images), "stable_header_ids": len(ids), "pandoc_warnings": 0}
    require(len(unit_header_ids) == 39 and len(unit_header_ids) == len(set(unit_header_ids)), "global AST Unit26 IDs")
    require(sum(row["math_nodes"] for name, row in ast_receipts.items() if name != "frontmatter-units-01-26.md") == 346, "global Unit26 math topology")

    front_flat = re.sub(r"\s+", " ", frontmatter)
    require(frontmatter.count(MODEL_BASE) == 1, "frontmatter provenance")
    require("Unit 1-26 memuat 646 soal" in front_flat and "semua 117 solusi publik" in front_flat, "frontmatter 26/646/117 coverage")
    require("Unit 1-23 mengikat revisi beku" in front_flat and "Unit 24-26 mengikat kuliah dan lembar kerja" in front_flat, "frontmatter edition split")
    require("kedua mata kuliah tidak diperlakukan sebagai satu edisi sumber" in front_flat, "frontmatter non-conflation")
    require("CC BY-SA 4.0" in front_flat and "Creative Commons Attribution-ShareAlike 2.0" in front_flat and "CC BY-SA 3.0" in front_flat, "frontmatter mixed rights")
    require("bukan klaim lisensi payung" in front_flat and "tidak menyiratkan dukungan" in front_flat, "frontmatter rights/nonendorsement")
    require("tidak ada solusi baru yang diada-adakan" in front_flat, "frontmatter no invented solutions")
    return {
        "source_and_control_facts": facts,
        "source_edition": "Osnabrück 2012",
        "lecture_semantic_entities": 21,
        "worksheet_exercise_entities": 11,
        "stable_ids": 39,
        "br_ak_2012_ids": 38,
        "media_credit_ids": 1,
        "math_nodes": 346,
        "exercises": 11,
        "warm_up_exercises": 4,
        "submitted_exercises": 7,
        "submitted_points": {"5": 4, "6": 4, "7": 4, "8": 4, "9": 4, "10": 3, "11": 8},
        "starred_exercises": [4],
        "public_solutions": [4],
        "invented_solutions": 0,
        "reader_images": 1,
        "ast": ast_receipts,
        "visible_german_residue": 0,
        "placeholder_count": 0,
        "secret_like_count": 0,
        "unicode_dash_count": 0,
        "invisible_unicode_controls": 0,
        "protected_lecture_math_checks": len(lecture_math),
        "protected_worksheet_math_checks": len(worksheet_math),
        "protected_solution_math_checks": len(solution_math),
        "terminology_bindings": TERM_IDS,
        "correction_bindings": CORRECTION_IDS,
        "visible_correction_disclosures": list(disclosures),
        "frontmatter_coverage": {"units": 26, "exercises": 646, "public_solutions": 117},
        "revision_contributors": {"lecture_root": "Arbota", "worksheet_root": "Arbota", "solution_26_4": "Bocardodarapti"},
    }


def main() -> int:
    receipt = {
        "schema": "ag-bridge-unit-translation-qa-v1",
        "status": "PASS",
        "unit": 26,
        "verified_date": "2026-08-26",
        "authority": verify_authority(),
        "media_and_rights": verify_media_and_rights(),
        "translation": verify_translation(),
        "provenance": MODEL,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "unit": 26, "receipt": OUT.relative_to(ROOT).as_posix(), "bytes": OUT.stat().st_size, "sha256": digest(OUT)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
