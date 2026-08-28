#!/usr/bin/env python3
"""Freeze the already captured official Unit 30 authority without network access.

The probe files are immutable API/XML/HTML/expanded-TeX witnesses captured
from de.wikiversity.org and commons.wikimedia.org.  This script verifies their
known roots, recomputes every local hash, closes the recursive transclusion and
solution sets, and emits the deterministic authority/rights receipts.  The two
2012 PDF binaries are metadata-bound because their canonical download endpoint
was rate-limited; no local binary or SHA-256 is invented.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "authority" / "wikiversity" / "unit-30"
ASSET = ROOT / "authority" / "assets" / "Two_cubic_curves.png"
MANIFEST = UNIT / "UNIT_AUTHORITY_MANIFEST.json"
FREEZE = ROOT / "authority" / "UNIT_30_AUTHORITY_FREEZE.md"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-30.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-30.json"
QA = ROOT / "qa" / "UNIT_30_AUTHORITY_QA.json"

EXPECTED = {
    "PROBE_SUMMARY.json": (13942, "db8d7f0b4242c638d2dac185f443444ae1bd32ca28e5d56b22386f5b090d97f3"),
    "lecture-30.xml": (3794, "6b5118904f5cba97127372ccb52bb45a1c0e637202374c2d4842ff8246bd1cf0"),
    "lecture-30-expanded.tex": (17474, "0080d009a13829a4c0d75d4ce375090d76c5969b92a426635280c2c1d9af8d61"),
    "worksheet-30.xml": (4824, "0525c13b64a201759a6982c6f8885cc3fe456fb23abbd1be9ad1e1e6cc780382"),
    "worksheet-30-expanded.tex": (5814, "c32bea5c89b6606a5171f79958a1dccded6575c4cca1ff4ca154fe5961800966"),
    "solution-ex03.xml": (5520, "2657d734224c0681b15fd19b6dd1284f704e27b0eb3397e4cf7f91065f43ebcb"),
    "solution-ex04.xml": (6791, "1eb565f3f8ca6acd72b53a130427c18b1ca957b804b9ab7463d826396f8e9bd1"),
    "worksheet-solution-candidates-api.json": (8186, "5f663d1f87bbb5e362d6bc4c34ffa8826f27a59bdd7d8835df5be38d66e593ad"),
    "official-pdfs-api.json": (1784, "da40a0cf5427eb7311cdb5abef9210654f67a82823e4a25ce17b63783fc346cf"),
    "local-pdf-file-metadata-api.json": (4189, "b808eb8fac29a52f362b3496a7f101127d1074dd9eaf1a461377dbdc07551ca4"),
}

ROOTS = {
    "lecture": {
        "title": "Kurs:Algebraische Kurven (Osnabrück 2012)/Vorlesung 30",
        "pageid": 51997,
        "revid": 1112650,
        "parentid": 793531,
        "timestamp": "2026-08-21T16:27:10Z",
        "mediawiki_sha1": "e457ac9823425ad360cc32d095178e513f79ec94",
        "wikitext_bytes": 662,
        "revision_contributor": "Bocardodarapti",
    },
    "worksheet": {
        "title": "Kurs:Algebraische Kurven (Osnabrück 2012)/Arbeitsblatt 30",
        "pageid": 50925,
        "revid": 1112597,
        "parentid": 793500,
        "timestamp": "2026-08-21T16:19:24Z",
        "mediawiki_sha1": "2111599a8a79cbd491a5f334baf54bb39e9af931",
        "wikitext_bytes": 1688,
        "revision_contributor": "Bocardodarapti",
    },
}

AUTHORED_POINTS = {str(number): points for number, points in enumerate(
    (3, 3, 4, 7, 6, 5, 5, 4, 4, 4, 4, 5), 1
)}
DISPLAYED_POINTS = {str(number): points for number, points in enumerate(
    (6, 5, 5, 4, 4, 4, 4, 5), 5
)}


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def identity(path: Path, base: Path = ROOT) -> dict[str, Any]:
    return {
        "path": path.relative_to(base).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def verify_inputs() -> None:
    for name, expected in EXPECTED.items():
        path = UNIT / name
        require(path.is_file() and not path.is_symlink(), f"missing input: {name}")
        require((path.stat().st_size, sha256(path)) == expected, f"input drift: {name}")
    require(ASSET.is_file() and not ASSET.is_symlink(), "missing Unit 30 image")
    require(
        (ASSET.stat().st_size, sha256(ASSET))
        == (7957, "489afccf2128371df697f6121da75c376f4910a2404dfe572c7ae7adbdac663a"),
        "Unit 30 image drift",
    )


def api_root(name: str) -> dict[str, Any]:
    data = read_json(UNIT / f"{name}-30-api.json")
    page = data["query"]["pages"][0]
    revision = page["revisions"][0]
    slot = revision["slots"]["main"]
    contributor = ROOTS[name]["revision_contributor"]
    xml_text = (UNIT / f"{name}-30.xml").read_text(encoding="utf-8")
    require(f"<username>{contributor}</username>" in xml_text, f"{name} XML contributor")
    result = {
        "title": page["title"],
        "pageid": page["pageid"],
        "revid": revision["revid"],
        "parentid": revision["parentid"],
        "timestamp": revision["timestamp"],
        "mediawiki_sha1": revision["sha1"],
        "wikitext_bytes": len(slot["content"].encode("utf-8")),
        "revision_contributor": contributor,
        "revision_contributor_userid": 2041,
        "oldid_url": f"https://de.wikiversity.org/w/index.php?oldid={revision['revid']}",
    }
    require(all(result[key] == value for key, value in ROOTS[name].items()), f"{name} root drift")
    return result


def pages_from(pattern: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(UNIT.glob(pattern), key=lambda item: item.name):
        data = read_json(path)
        for page in data["query"]["pages"]:
            if page.get("missing"):
                continue
            revision = page["revisions"][0]
            content = revision["slots"]["main"].get("content", "")
            rows.append({
                "title": page["title"],
                "pageid": page["pageid"],
                "revid": revision["revid"],
                "parentid": revision.get("parentid", 0),
                "timestamp": revision["timestamp"],
                "mediawiki_sha1": revision["sha1"],
                "wikitext_bytes": len(content.encode("utf-8")),
                "capture_file": path.name,
            })
    unique: dict[tuple[str, int], dict[str, Any]] = {}
    for row in rows:
        key = (row["title"], row["pageid"])
        if key in unique:
            require(
                all(unique[key][field] == row[field] for field in (
                    "revid", "parentid", "timestamp", "mediawiki_sha1", "wikitext_bytes"
                )),
                f"conflicting transclusion identity: {key}",
            )
        else:
            unique[key] = row
    return [unique[key] for key in sorted(unique)]


def add_root(rows: list[dict[str, Any]], root: dict[str, Any]) -> list[dict[str, Any]]:
    result = list(rows)
    keyset = {(row["title"], row["pageid"]) for row in result}
    if (root["title"], root["pageid"]) not in keyset:
        result.append({key: root[key] for key in (
            "title", "pageid", "revid", "parentid", "timestamp", "mediawiki_sha1", "wikitext_bytes"
        )})
    return sorted(result, key=lambda row: (row["title"], row["pageid"]))


def file_inventory() -> list[dict[str, Any]]:
    excluded = {MANIFEST.name}
    return [
        identity(path, UNIT)
        for path in sorted(UNIT.iterdir(), key=lambda item: item.name.casefold())
        if path.is_file() and not path.is_symlink() and path.name not in excluded
    ]


def main() -> int:
    verify_inputs()
    probe = read_json(UNIT / "PROBE_SUMMARY.json")
    lecture = api_root("lecture")
    worksheet = api_root("worksheet")

    lecture_rows = pages_from("lecture-30-transclusions-*.json")
    worksheet_rows = pages_from("worksheet-30-transclusions-*.json")
    solution_rows = {
        3: pages_from("solution-ex03-transclusions-*.json"),
        4: pages_from("solution-ex04-transclusions-*.json"),
    }
    require(len(lecture_rows) == 93, "lecture transclusion closure count")
    require(len(worksheet_rows) == 63, "worksheet transclusion closure count")
    require({number: len(rows) for number, rows in solution_rows.items()} == {3: 12, 4: 13},
            "solution transclusion closure count")

    exercise_map = read_json(UNIT / "ORDERED_EXERCISE_MAP.json")
    require(exercise_map["exercise_count"] == 12, "exercise count")
    require([row["exercise_number"] for row in exercise_map["entries"]] == list(range(1, 13)),
            "exercise order")
    require([row["exercise_number"] for row in exercise_map["entries"] if row["has_public_solution"]] == [3, 4],
            "solution topology")
    exercise_map.pop("map_file", None)
    exercise_map.pop("map_bytes", None)
    exercise_map.pop("map_sha256", None)
    exercise_map["ordered_role_point_and_star_topology"] = {
        "warm_up_numbers": [1, 2, 3, 4],
        "submitted_numbers": list(range(5, 13)),
        "starred_numbers": [3, 4],
        "upload_numbers": [],
        "authored_points": AUTHORED_POINTS,
        "displayed_points": DISPLAYED_POINTS,
        "submitted_displayed_point_total": 37,
        "evidence": "frozen root order plus exact Inputaufgabe/Inputaufgabegibtloesung arguments",
    }
    exercise_map["solution_closures"] = {
        str(number): {
            "dependency_count": len(rows),
            "with_root": len(rows) + 1,
            "capture_files": [item.name for item in sorted(UNIT.glob(f"solution-ex{number:02d}-transclusions-*.json"))],
        }
        for number, rows in solution_rows.items()
    }
    write_json(UNIT / "ORDERED_EXERCISE_MAP.json", exercise_map)
    exercise_identity = identity(UNIT / "ORDERED_EXERCISE_MAP.json")

    commons = read_json(UNIT / "local-pdf-file-metadata-api.json")["query"]["pages"][-1]
    imageinfo = commons["imageinfo"][0]
    file_revision = commons["revisions"][0]
    require(imageinfo["sha1"] == "60f5c1dec89a6806608626cd85cf1e7b94660863", "Commons image SHA-1")
    require(imageinfo["extmetadata"]["LicenseShortName"]["value"] == "Public domain", "image rights")

    pdf_pages = read_json(UNIT / "official-pdfs-api.json")["query"]["pages"]
    pdf_by_kind = {
        "lecture": next(page for page in pdf_pages if "Vorlesung30" in page["title"]),
        "worksheet": next(page for page in pdf_pages if "Arbeitsblatt30" in page["title"]),
    }
    pdf_expected = {
        "lecture": (53381, 90813, 7, "693ce1c8eba815282b96746054049bf12a46119f"),
        "worksheet": (54442, 38514, 2, "ffc2e642d73d802b9c1f520607a8e00f440dffee"),
    }
    pdf_rows: list[dict[str, Any]] = []
    for kind, page in pdf_by_kind.items():
        info = page["imageinfo"][0]
        expected = pdf_expected[kind]
        require((page["pageid"], info["size"], info["pagecount"], info["sha1"]) == expected,
                f"{kind} PDF metadata")
        pdf_rows.append({
            "kind": kind,
            "title": page["title"],
            "pageid": page["pageid"],
            "timestamp": info["timestamp"],
            "source_bytes": info["size"],
            "source_sha1": info["sha1"],
            "page_count": info["pagecount"],
            "source_url": info["url"],
            "description_url": info["descriptionurl"],
            "local_path": f"authority/artifacts/{kind}-30-official.pdf",
            "local_binary_archived": False,
            "binary_sha256": "PENDING",
            "binary_status": "canonical endpoint returned HTTP 429 during bounded capture; metadata frozen, no hash invented",
            "component_license_route": {
                "current_print_version_notice": "CC BY-SA 4.0",
                "legacy_file_notice": "CC BY-SA 2.0 Germany",
                "resolution": "preserve both component notices; no blanket relicensing claim",
            },
        })

    asset_closure = {
        "schema": "ag-bridge-asset-closure-v1",
        "unit": 30,
        "status": "PASS",
        "assets": [{
            "asset_id": "br-ak-u30-media-001",
            "source_title": commons["title"],
            "source_pageid": commons["pageid"],
            "description_revid": file_revision["revid"],
            "description_parentid": file_revision["parentid"],
            "description_timestamp": file_revision["timestamp"],
            "description_mediawiki_sha1": file_revision["sha1"],
            "description_url": imageinfo["descriptionurl"],
            "source_url": imageinfo["url"],
            "original_bytes": imageinfo["size"],
            "original_sha1": imageinfo["sha1"],
            "width": imageinfo["width"],
            "height": imageinfo["height"],
            "artist": "Hack",
            "uploader": imageinfo["user"],
            "source_credit": "own work, with Mathematica 6.0",
            "license_short": "Public domain",
            "license_evidence": "PD-self; Public Domain",
            "attribution_required": False,
            "selected_form": "original",
            "original_locally_archived": True,
            "local_path": "authority/assets/Two_cubic_curves.png",
            "local_bytes": ASSET.stat().st_size,
            "local_sha256": sha256(ASSET),
            "reader_positions": 1,
        }],
        "official_pdf_component_rights": pdf_rows,
        "blanket_relicense_claim": False,
    }
    write_json(CLOSURE, asset_closure)

    RIGHTS.parent.mkdir(parents=True, exist_ok=True)
    with RIGHTS.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=[
            "asset_id", "local_path", "source_title", "source_pageid", "source_url",
            "description_url", "artist", "uploader", "repository", "license_short",
            "license_evidence", "attribution_required", "source_bytes", "source_sha1",
            "local_bytes", "local_sha256", "reader_positions",
        ], lineterminator="\n")
        writer.writeheader()
        writer.writerow({
            "asset_id": "br-ak-u30-media-001",
            "local_path": "authority/assets/Two_cubic_curves.png",
            "source_title": commons["title"],
            "source_pageid": commons["pageid"],
            "source_url": imageinfo["url"],
            "description_url": imageinfo["descriptionurl"],
            "artist": "Hack",
            "uploader": imageinfo["user"],
            "repository": "Wikimedia Commons",
            "license_short": "Public domain",
            "license_evidence": "PD-self; Public Domain",
            "attribution_required": "false",
            "source_bytes": imageinfo["size"],
            "source_sha1": imageinfo["sha1"],
            "local_bytes": ASSET.stat().st_size,
            "local_sha256": sha256(ASSET),
            "reader_positions": 1,
        })

    solution_roots = {}
    for number in (3, 4):
        entry = exercise_map["entries"][number - 1]
        solution_roots[number] = {key: entry[key] for key in (
            "resolved_title", "pageid", "revid", "parentid", "timestamp",
            "mediawiki_sha1", "wikitext_bytes", "oldid_url", "xml_file",
            "xml_bytes", "xml_sha256", "html_file", "html_bytes", "html_sha256"
        )}

    semantic_union: dict[tuple[str, int], dict[str, Any]] = {}
    for rows in (add_root(lecture_rows, lecture), add_root(worksheet_rows, worksheet)):
        for row in rows:
            semantic_union[(row["title"], row["pageid"])] = row
    for number, rows in solution_rows.items():
        root = {
            "title": solution_roots[number]["resolved_title"],
            **{key: solution_roots[number][key] for key in (
                "pageid", "revid", "parentid", "timestamp", "mediawiki_sha1", "wikitext_bytes"
            )},
        }
        for row in add_root(rows, root):
            key = (row["title"], row["pageid"])
            if key in semantic_union:
                require(semantic_union[key]["revid"] == row["revid"], f"semantic union conflict: {key}")
            semantic_union[key] = row
    require(len(semantic_union) == 141, "semantic live union count")

    manifest = {
        "schema": "ag-bridge-unit-authority-manifest-v1",
        "unit": 30,
        "source_course": probe["course"],
        "lecture": lecture,
        "worksheet": worksheet,
        "root_revision_contributors": {
            "records": [
                {"kind": "lecture", "revision_contributor": lecture["revision_contributor"],
                 "userid": lecture["revision_contributor_userid"]},
                {"kind": "worksheet", "revision_contributor": worksheet["revision_contributor"],
                 "userid": worksheet["revision_contributor_userid"]},
            ],
            "source_author": "Holger Brenner (Wikiversity user Bocardodarapti)",
        },
        "lecture_transclusion_closure": {
            "captured_page_count": len(lecture_rows),
            "with_root": len(add_root(lecture_rows, lecture)),
            "canonical_identity_rows_sha256": probe["transclusion_topology"]["lecture"]["canonical_identity_rows_sha256"],
            "capture_files": [item.name for item in sorted(UNIT.glob("lecture-30-transclusions-*.json"))],
            "rows": lecture_rows,
        },
        "worksheet_transclusion_closure": {
            "captured_page_count": len(worksheet_rows),
            "with_root": len(add_root(worksheet_rows, worksheet)),
            "canonical_identity_rows_sha256": probe["transclusion_topology"]["worksheet"]["canonical_identity_rows_sha256"],
            "capture_files": [item.name for item in sorted(UNIT.glob("worksheet-30-transclusions-*.json"))],
            "rows": worksheet_rows,
        },
        "solutions": {
            "exercise_count": 12,
            "public_solution_numbers": [3, 4],
            "negative_solution_numbers": [1, 2, 5, 6, 7, 8, 9, 10, 11, 12],
            "roots": {str(key): value for key, value in solution_roots.items()},
            "closures": {
                str(number): {
                    "captured_page_count": len(rows),
                    "with_root": len(rows) + 1,
                    "rows": rows,
                }
                for number, rows in solution_rows.items()
            },
        },
        "ordered_exercise_map": exercise_identity,
        "media": {
            "reader_positions": 1,
            "asset_closure": identity(CLOSURE),
            "rights_ledger": identity(RIGHTS),
        },
        "official_pdfs": pdf_rows,
        "source_discrepancies_and_repairs": [
            "Example 30.6 omits its field; the Indonesian edition states C explicitly.",
            "Exercises 30.9-30.10 omit the field and degenerate in characteristic 2; the edition states C.",
            "Exercise 30.4 semantic title says Y=X^2 while displayed formula and solution use X=Y^2.",
            "Lemma 30.1 prose omits the negative sign B=-QF required by its displayed Koszul map.",
            "Theorem 30.3 proof needs the identity case when lambda=0.",
            "Solution 30.3 reverses gradient component order; the edition normalizes to (X,Y).",
            "Solution 30.4 prints K[Y]_Y instead of the local ring K[Y]_(Y).",
            "Forward navigation targets Unit 31, which is absent: Unit 30 is the source-course endpoint.",
            "The 2012 PDFs predate the current 2026 semantic revisions and are visual/build witnesses only.",
        ],
        "final_live_identity_replay": {
            "result": "PASS",
            "basis": "captured official API roots and recursive transclusion responses; no compaction claims",
            "semantic_unique_identity_count": len(semantic_union),
            "root_revisions": {"lecture": lecture["revid"], "worksheet": worksheet["revid"]},
        },
        "captured_file_inventory": file_inventory(),
        "license": {
            "semantic_text_and_translation": "CC BY-SA 4.0",
            "media_components": "per-file rights",
            "official_pdfs": "component routes preserved; binaries not silently equated to 2026 text",
            "blanket_relicense_claim": False,
            "non_endorsement": True,
        },
    }
    write_json(MANIFEST, manifest)

    freeze_text = f"""# Unit 30 authority freeze - Teorema Bézout

Status: **PASS**. This freeze is generated offline from the bounded official
API/XML/HTML/expanded-TeX witnesses already stored in
`authority/wikiversity/unit-30`; it performs no network call.

- Lecture root: page 51997, revision 1112650, MediaWiki SHA-1
  `e457ac9823425ad360cc32d095178e513f79ec94`, 2026-08-21T16:27:10Z.
- Worksheet root: page 50925, revision 1112597, MediaWiki SHA-1
  `2111599a8a79cbd491a5f334baf54bb39e9af931`, 2026-08-21T16:19:24Z.
- Recursive closures: 93 lecture dependencies (94 with root), 63 worksheet
  dependencies (64 with root), and solution closures 12/13 dependencies for
  Exercises 3/4 (13/14 with their roots).
- Live semantic union: 141 unique `(title,pageid)` identities.
- Worksheet topology: 12 ordered exercises; warm-ups 1-4; submitted 5-12;
  stars and public solutions exactly 3 and 4; 37 displayed submitted points.
- Reader media: one original 7,957-byte public-domain PNG by Hack, SHA-256
  `{sha256(ASSET)}`.
- Official 2012 PDFs: lecture 7 pages / 90,813 bytes / source SHA-1
  `693ce1c8eba815282b96746054049bf12a46119f`; worksheet 2 pages / 38,514
  bytes / source SHA-1 `ffc2e642d73d802b9c1f520607a8e00f440dffee`.
  Their binary endpoints returned HTTP 429 during the bounded capture, so no
  local SHA-256 is invented. They predate the binding 2026 semantic pages and
  are visual/build witnesses, not revision-identical textual authority.

Manifest: `{MANIFEST.relative_to(ROOT).as_posix()}` - {MANIFEST.stat().st_size}
bytes - SHA-256 `{sha256(MANIFEST)}`.

Rights: semantic text and the Indonesian derivative follow CC BY-SA 4.0;
media retain component-specific rights. The old/current PDF notice routes are
recorded without making a blanket relicensing claim. This independent edition
does not imply endorsement by the author, source institutions, or platforms.
"""
    FREEZE.write_text(freeze_text, encoding="utf-8", newline="\n")

    receipt = {
        "schema": "ag-bridge-unit-authority-qa-v1",
        "status": "PASS",
        "unit": 30,
        "verified_date": "2026-08-28",
        "authority": {
            "lecture_root_plus_dependencies": 94,
            "worksheet_root_plus_dependencies": 64,
            "solution_closures_with_root": {"3": 13, "4": 14},
            "semantic_unique_identity_count": 141,
            "exercise_count": 12,
            "public_solution_numbers": [3, 4],
            "negative_solution_count": 10,
            "submitted_displayed_points": 37,
        },
        "media": {
            "positions": 1,
            "assets": 1,
            "public_domain_assets": 1,
            "original_assets_locally_archived": 1,
            "official_pdf_metadata_rows": 2,
            "official_pdf_binaries_local": 0,
            "invented_pdf_hashes": 0,
        },
        "bound_artifacts": {
            "manifest": identity(MANIFEST),
            "freeze": identity(FREEZE),
            "rights": identity(RIGHTS),
            "asset_closure": identity(CLOSURE),
            "exercise_map": identity(UNIT / "ORDERED_EXERCISE_MAP.json"),
        },
        "checks": {
            "root_identity": "PASS",
            "recursive_transclusion_closure": "PASS",
            "exercise_solution_topology": "PASS",
            "media_rights_and_binary_identity": "PASS",
            "official_pdf_metadata_and_nonidentity_disclosure": "PASS",
            "source_defect_disclosure": "PASS",
            "no_network_calls": True,
        },
    }
    write_json(QA, receipt)

    print(json.dumps({
        "status": "PASS",
        "manifest": identity(MANIFEST),
        "authority_qa": identity(QA),
        "exercise_map": identity(UNIT / "ORDERED_EXERCISE_MAP.json"),
        "freeze": identity(FREEZE),
        "rights": identity(RIGHTS),
        "asset_closure": identity(CLOSURE),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
