#!/usr/bin/env python3
"""Freeze the bounded official Unit 21 Wikiversity/Commons authority closure.

The script reuses the exercised Unit 12 capture primitives while binding every
write and every source identity to Unit 21.  Unit 21 has no substantive reader
image, so this wrapper captures the two official PDFs and emits an explicit
zero-media rights/accessibility closure instead of invoking the Unit 12
one-image path.
"""

from __future__ import annotations

import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import freeze_unit12_authority as base
from freeze_no_image_unit_rights import EMPTY_RIGHTS_FIELDS
from freeze_single_image_unit_media import commons_file_title, pdf_rights, title_key


ROOT = Path(__file__).resolve().parents[1]
UNIT = 21
UNIT_LABEL = f"{UNIT:02d}"

# Redirect every mutable/output and source-identity global before any request.
base.UNIT = UNIT
base.OUT = ROOT / "authority" / "wikiversity" / f"unit-{UNIT_LABEL}"
base.ARTIFACTS = ROOT / "authority" / "artifacts"
base.ASSETS = ROOT / "authority" / "assets"
base.RIGHTS = ROOT / "authority" / f"RIGHTS-unit-{UNIT_LABEL}.csv"
base.CLOSURE = ROOT / "authority" / f"ASSET_CLOSURE-unit-{UNIT_LABEL}.json"
base.COMMONS_META = ROOT / "authority" / f"commons-imageinfo-unit-{UNIT_LABEL}.json"
base.LECTURE_TITLE = f"{base.COURSE}/Vorlesung {UNIT}"
base.WORKSHEET_TITLE = f"{base.COURSE}/Arbeitsblatt {UNIT}"
base.USER_AGENT = "O016-unit21-authority-freeze/1.0 (bounded educational preservation)"

COURSE_LICENSE_TITLE = f"{base.COURSE}/Lizenzerklärung"
COURSE_LICENSE_DEPENDENCY = "Holger Brenner/Lizenzerklärung"
CURRENT_LICENSE = "CC BY-SA 4.0"
PDF_INTERNAL_LABEL = "CC-by-sa 3.0"
AUDIT_SEMANTIC_IDENTITIES = [
    {"label": "worksheet exercise 1", "pageid": 95378, "revid": 1107842},
    {"label": "worksheet exercise 6", "pageid": 95400, "revid": 1112454},
    {"label": "order lemma", "pageid": 15938, "revid": 1044491},
    {"label": "order-lemma proof task", "pageid": 16181, "revid": 1037187},
    {"label": "worksheet exercise 8", "pageid": 16574, "revid": 1097121},
    {"label": "worksheet exercise 12", "pageid": 25025, "revid": 1041710},
    {"label": "DVR characterization proof", "pageid": 15878, "revid": 1106770},
    {"label": "nilpotence proof", "pageid": 15870, "revid": 1086502},
    {"label": "worksheet exercise 20", "pageid": 95384, "revid": 1083418},
    {"label": "worksheet exercise 25", "pageid": 21161, "revid": 1107795},
    {"label": "worksheet exercise 26", "pageid": 21162, "revid": 1062610},
]


def key(value: str) -> str:
    """Canonical comparison key for already-canonical MediaWiki titles."""
    # MediaWiki normalizes underscores but permits distinct subpage titles that
    # differ by letter case; do not collapse those separate semantic pages.
    return value.replace("_", " ")


def bind_audit_semantic_identities(lecture_closure: dict, worksheet_closure: dict) -> list[dict]:
    """Prove eleven audited semantic pages are already inside the bounded closure."""
    found: dict[int, dict] = {}
    for surface, closure in (("lecture", lecture_closure), ("worksheet", worksheet_closure)):
        for page in closure["pages"]:
            pageid = int(page["pageid"])
            candidate = {"closure_surface": surface, **page}
            previous = found.get(pageid)
            if previous is not None and (
                int(previous["revid"]) != int(candidate["revid"])
                or previous["mediawiki_sha1"] != candidate["mediawiki_sha1"]
            ):
                raise RuntimeError(f"inconsistent repeated semantic identity: pageid {pageid}")
            found[pageid] = candidate
    bindings: list[dict] = []
    for expected in AUDIT_SEMANTIC_IDENTITIES:
        page = found.get(expected["pageid"])
        if page is None:
            raise RuntimeError(
                f"audited semantic page is absent from lecture/worksheet closure: {expected}"
            )
        if int(page["revid"]) != expected["revid"]:
            raise RuntimeError(
                "audited semantic revision drift: "
                f"pageid {expected['pageid']} expected {expected['revid']} got {page['revid']}"
            )
        bindings.append({"label": expected["label"], **page})
    return bindings


def course_license_surface() -> dict:
    """Freeze and validate the course-specific license wrapper and dependency."""
    entry, parsed = base.entry_surface(COURSE_LICENSE_TITLE, "course-license")
    closure = base.transclusion_closure(parsed, "course-license")
    dependencies = {key(item["title"]) for item in closure["pages"]}
    if key(COURSE_LICENSE_DEPENDENCY) not in dependencies:
        raise RuntimeError("course license dependency is absent from recursive closure")

    declaration = ""
    for batch in closure["batches"]:
        payload = json.loads((base.OUT / batch["file"]).read_text(encoding="utf-8"))
        for page in payload.get("query", {}).get("pages", []):
            if key(page.get("title", "")) == key(COURSE_LICENSE_DEPENDENCY):
                declaration = base.revision(page)["slots"]["main"]["content"]
    if "CC-by-sa 4.0" not in declaration:
        raise RuntimeError("frozen course license dependency does not declare CC-by-sa 4.0")
    return {
        "declared_license": CURRENT_LICENSE,
        "wrapper": entry,
        "recursive_transclusion_closure": closure,
        "validated_dependency_title": COURSE_LICENSE_DEPENDENCY,
    }


def solution_transclusion_closures(solutions: dict) -> list[dict]:
    """Freeze parser-recursive closure for every extant public solution."""
    candidate_payload = json.loads(
        (base.OUT / solutions["candidate_api_file"]).read_text(encoding="utf-8")
    )
    pages = {
        key(page["title"]): page
        for page in candidate_payload.get("query", {}).get("pages", [])
        if not page.get("missing")
    }
    records: list[dict] = []
    for item in solutions["entries"]:
        if not item["has_public_solution"]:
            continue
        number = int(item["exercise_number"])
        title = str(item["resolved_title"])
        page = pages.get(key(title))
        if page is None:
            raise RuntimeError(f"solution content is absent from frozen candidates: {title}")
        rev = base.revision(page)
        if int(rev["revid"]) != int(item["revid"]):
            raise RuntimeError(f"solution revision drift before closure capture: {title}")
        wikitext = rev["slots"]["main"]["content"]
        direct_wrappers = [
            value.strip()
            for value in re.findall(r"\{\{\s*:\s*([^|}\n]+)", wikitext)
            if value.strip()
        ]

        raw, payload = base.api_raw(
            base.WIKI_API,
            {
                "action": "parse",
                "oldid": int(item["revid"]),
                "prop": "links|templates|images|externallinks|tocdata",
            },
        )
        parse_path = base.OUT / f"solution-ex{number:02d}-parse-api.json"
        base.write_bytes(parse_path, raw)
        parsed = payload["parse"]
        if int(parsed["pageid"]) != int(item["pageid"]) or int(parsed["revid"]) != int(item["revid"]):
            raise RuntimeError(f"solution parse identity drift: {title}")
        parsed_titles = {key(template["title"]) for template in parsed.get("templates", [])}
        if any(key(wrapper) not in parsed_titles for wrapper in direct_wrappers):
            raise RuntimeError(f"direct solution wrapper missing from parser closure: {title}")
        closure = base.transclusion_closure(parsed, f"solution-ex{number:02d}")
        records.append(
            {
                "exercise_number": number,
                "solution_title": title,
                "solution_revid": int(item["revid"]),
                "parse_api_file": parse_path.name,
                "parse_api_bytes": parse_path.stat().st_size,
                "parse_api_sha256": base.digest(parse_path),
                "direct_wrapper_dependency_titles": direct_wrappers,
                "recursive_transclusion_closure": closure,
            }
        )
    if len(records) != int(solutions["solution_count"]):
        raise RuntimeError("public-solution closure count mismatch")
    return records


def official_pdfs_no_assets(
    lecture_parsed: dict, worksheet_parsed: dict
) -> tuple[list[dict], list[dict]]:
    """Freeze both official PDFs and prove that Unit 21 has no reader asset."""
    image_names = list(
        dict.fromkeys(lecture_parsed.get("images", []) + worksheet_parsed.get("images", []))
    )
    pdf_names = [name for name in image_names if name.casefold().endswith(".pdf")]
    substantive = [name for name in image_names if not name.casefold().endswith(".pdf")]
    if substantive:
        raise RuntimeError(f"Unit 21 media topology changed materially: {substantive}")
    lecture_pdf = [name for name in pdf_names if f"Vorlesung{UNIT}.pdf" in name.replace("_", "")]
    worksheet_pdf = [name for name in pdf_names if f"Arbeitsblatt{UNIT}.pdf" in name.replace("_", "")]
    if len(lecture_pdf) != 1 or len(worksheet_pdf) != 1 or len(pdf_names) != 2:
        raise RuntimeError(f"official Unit 21 PDF identity is not exactly closed: {pdf_names}")

    wiki_raw, wiki_payload = base.api_raw(
        base.WIKI_API,
        {
            "action": "query",
            "prop": "imageinfo",
            "iiprop": "timestamp|url|size|sha1|mime|mediatype",
            "titles": "|".join("File:" + name for name in [lecture_pdf[0], worksheet_pdf[0]]),
        },
    )
    official_api_path = base.OUT / "official-pdfs-api.json"
    base.write_bytes(official_api_path, wiki_raw)

    commons_raw, commons_payload = base.api_raw(
        base.COMMONS_API,
        {
            "action": "query",
            "prop": "imageinfo|revisions",
            "iiprop": "timestamp|user|url|size|sha1|mime|mediatype|extmetadata",
            "rvprop": "ids|timestamp|sha1|content",
            "rvslots": "main",
            "titles": "|".join("File:" + name for name in [lecture_pdf[0], worksheet_pdf[0]]),
        },
    )
    base.write_bytes(base.COMMONS_META, commons_raw)
    commons_pages = {
        base.file_key(page["title"]): page
        for page in commons_payload.get("query", {}).get("pages", [])
    }
    wiki_pages = {
        base.file_key(page["title"]): page
        for page in wiki_payload.get("query", {}).get("pages", [])
    }

    records: list[dict] = []
    ordered = (("lecture", lecture_pdf[0]), ("worksheet", worksheet_pdf[0]))
    for kind, name in ordered:
        page = wiki_pages.get(base.file_key(name))
        commons_page = commons_pages.get(base.file_key(name))
        if (
            page is None
            or not page.get("imageinfo")
            or commons_page is None
            or commons_page.get("missing")
            or not commons_page.get("imageinfo")
        ):
            raise RuntimeError(f"official PDF did not resolve on both wikis: {name}")
        info = page["imageinfo"][0]
        commons_info = commons_page["imageinfo"][0]
        data = base.fetch(info["url"])
        if len(data) != int(info["size"]) or base.digest_bytes(data, "sha1") != info["sha1"]:
            raise RuntimeError(f"official PDF byte identity mismatch: {name}")
        local = base.ARTIFACTS / f"{kind}-{UNIT_LABEL}-official.pdf"
        base.write_bytes(local, data)
        reader = base.PdfReader(str(local))
        if reader.is_encrypted:
            raise RuntimeError(f"encrypted official PDF: {name}")
        extracted = "\n".join((page.extract_text() or "") for page in reader.pages)
        normalized_text = " ".join(extracted.split()).casefold()
        if PDF_INTERNAL_LABEL.casefold() not in normalized_text:
            raise RuntimeError(f"expected legacy PDF license boilerplate is absent: {name}")
        root_object = reader.trailer["/Root"]
        mark_info = root_object.get("/MarkInfo")
        if hasattr(mark_info, "get_object"):
            mark_info = mark_info.get_object()
        tagged_pdf = bool(mark_info and mark_info.get("/Marked", False))
        metadata = commons_info.get("extmetadata", {})
        license_short = base.ext(metadata, "LicenseShortName") or base.ext(metadata, "UsageTerms")
        if license_short != CURRENT_LICENSE:
            raise RuntimeError(f"unexpected current Commons PDF license for {name}: {license_short}")
        records.append(
            {
                "source_file_title": page["title"],
                "commons_pageid": commons_page.get("pageid"),
                "image_timestamp": info["timestamp"],
                "mediawiki_sha1": info["sha1"],
                "source_bytes": int(info["size"]),
                "mime": info["mime"],
                "source_url": info["url"],
                "description_url": info["descriptionurl"],
                "local_path": local.relative_to(ROOT).as_posix(),
                "local_bytes": local.stat().st_size,
                "local_sha256": base.digest(local),
                "page_count": len(reader.pages),
                "license_short": license_short,
                "license_url": base.ext(metadata, "LicenseUrl"),
                "artist": base.ext(metadata, "Artist"),
                "credit": base.ext(metadata, "Credit"),
                "accessibility": {
                    "encrypted": False,
                    "extractable_text_characters": len(extracted),
                    "tagged_pdf": tagged_pdf,
                },
                "internal_pdf_boilerplate_label": PDF_INTERNAL_LABEL,
                "governing_current_course_and_commons_license": CURRENT_LICENSE,
                "license_discrepancy_note": (
                    "The generated PDF retains a CC-by-sa 3.0 boilerplate, while the "
                    "frozen current course declaration and Commons description bind this "
                    "official component as CC BY-SA 4.0."
                ),
            }
        )
    return records, list(commons_pages.values())


def write_zero_media_rights(
    pdf_records: list[dict], commons_pages: list[dict], lecture_entry: dict
) -> dict:
    """Emit an explicit empty reader-media ledger plus exact PDF component rights."""
    by_key = {title_key(page["title"]): page for page in commons_pages}
    rights_records: list[dict] = []
    for witness in pdf_records:
        title = commons_file_title(witness["source_file_title"])
        page = by_key.get(title_key(title))
        if page is None:
            raise RuntimeError(f"Commons rights page missing for {title}")
        local = ROOT / witness["local_path"]
        record = pdf_rights(page, local)
        if record["license_short"] != CURRENT_LICENSE:
            raise RuntimeError(f"unexpected PDF component license: {title}")
        record["accessibility"] = witness["accessibility"]
        record["internal_pdf_boilerplate_label"] = witness["internal_pdf_boilerplate_label"]
        record["governing_current_course_and_commons_license"] = witness[
            "governing_current_course_and_commons_license"
        ]
        record["license_discrepancy_note"] = witness["license_discrepancy_note"]
        rights_records.append(record)

    base.RIGHTS.parent.mkdir(parents=True, exist_ok=True)
    with base.RIGHTS.open("w", encoding="utf-8", newline="") as stream:
        csv.DictWriter(stream, fieldnames=EMPTY_RIGHTS_FIELDS, lineterminator="\n").writeheader()

    lecture_pdf = next(item for item in pdf_records if "lecture-21" in item["local_path"])
    if lecture_pdf["image_timestamp"] >= lecture_entry["timestamp"]:
        raise RuntimeError("expected Unit 21 lecture/PDF temporal discrepancy changed")
    closure = {
        "schema": "brenner-unit-media-closure-v2",
        "unit": UNIT,
        "authority_only_boundary": True,
        "reader_media_positions": 0,
        "animated_html_positions": 0,
        "unique_local_assets": 0,
        "metadata_file": base.COMMONS_META.relative_to(ROOT).as_posix(),
        "metadata_bytes": base.COMMONS_META.stat().st_size,
        "metadata_sha256": base.digest(base.COMMONS_META),
        "rights_file": base.RIGHTS.relative_to(ROOT).as_posix(),
        "rights_bytes": base.RIGHTS.stat().st_size,
        "rights_sha256": base.digest(base.RIGHTS),
        "reader_credits_file": None,
        "reader_credits_required": False,
        "accessibility": {
            "reader_media_alt_or_caption_required": False,
            "reason": "The parsed Unit 21 entry surfaces contain no substantive reader media.",
            "official_pdf_surfaces": [
                {"local_path": item["local_path"], **item["accessibility"]}
                for item in pdf_records
            ],
        },
        "official_pdf_witnesses_are_not_media_positions": True,
        "official_pdf_component_rights": sorted(
            rights_records, key=lambda item: item["local_path"]
        ),
        "component_discrepancies": {
            "official_pdf_license_boilerplate": [
                {
                    "local_path": item["local_path"],
                    "embedded_label": item["internal_pdf_boilerplate_label"],
                    "current_commons_and_course_license": item[
                        "governing_current_course_and_commons_license"
                    ],
                    "note": item["license_discrepancy_note"],
                }
                for item in pdf_records
            ],
            "lecture_pdf_temporal_scope": {
                "entry_revid": lecture_entry["revid"],
                "entry_timestamp": lecture_entry["timestamp"],
                "official_pdf_timestamp": lecture_pdf["image_timestamp"],
                "note": (
                    "The current lecture revision postdates the official PDF binary. The PDF "
                    "is retained as an official witness, not asserted to be a current-content clone."
                ),
            },
        },
        "assets": [],
    }
    base.write_json(base.CLOSURE, closure)
    return closure


def add_expected(expected: dict[str, dict], record: dict) -> None:
    title = str(record["title"])
    candidate = {"title": title, "revid": int(record["revid"]), "sha1": record["mediawiki_sha1"]}
    previous = expected.get(key(title))
    if previous is not None and previous != candidate:
        raise RuntimeError(f"inconsistent frozen identity for repeated title: {title}")
    expected[key(title)] = candidate


def final_live_identity_replay(
    primary_records: list[dict],
    closures: list[dict],
    solutions: dict,
    pdf_records: list[dict],
    pdf_rights_records: list[dict],
) -> dict:
    """Requery every frozen wiki identity and both Commons PDF components."""
    expected: dict[str, dict] = {}
    for record in primary_records:
        add_expected(expected, record)
    for closure in closures:
        for page in closure["pages"]:
            add_expected(expected, page)
    for item in solutions["entries"]:
        if item["has_public_solution"]:
            add_expected(
                expected,
                {
                    "title": item["resolved_title"],
                    "revid": item["revid"],
                    "mediawiki_sha1": item["mediawiki_sha1"],
                },
            )

    requested = [item["title"] for item in sorted(expected.values(), key=lambda row: row["title"])]
    batches: list[dict] = []
    for offset in range(0, len(requested), 25):
        titles = requested[offset : offset + 25]
        raw, payload = base.api_raw(
            base.WIKI_API,
            {
                "action": "query",
                "prop": "revisions",
                "rvprop": "ids|timestamp|sha1",
                "titles": "|".join(titles),
            },
        )
        path = base.OUT / f"final-identity-replay-{offset // 25 + 1:02d}.json"
        base.write_bytes(path, raw)
        pages = payload.get("query", {}).get("pages", [])
        if len(pages) != len(titles) or any(page.get("missing") for page in pages):
            raise RuntimeError(f"final identity replay page closure failed: {path.name}")
        for page in pages:
            current = base.revision(page)
            frozen = expected.get(key(page["title"]))
            if frozen is None:
                raise RuntimeError(f"unexpected final replay title: {page['title']}")
            if int(current["revid"]) != frozen["revid"] or current["sha1"] != frozen["sha1"]:
                raise RuntimeError(f"live revision drift during Unit 21 freeze: {page['title']}")
        batches.append(
            {
                "file": path.name,
                "bytes": path.stat().st_size,
                "sha256": base.digest(path),
                "title_count": len(titles),
            }
        )

    commons_raw, commons_payload = base.api_raw(
        base.COMMONS_API,
        {
            "action": "query",
            "prop": "imageinfo|revisions",
            "iiprop": "timestamp|url|size|sha1|mime|mediatype",
            "rvprop": "ids|timestamp|sha1",
            "titles": "|".join(
                commons_file_title(item["source_file_title"]) for item in pdf_records
            ),
        },
    )
    commons_path = base.OUT / "final-commons-pdf-identity-replay.json"
    base.write_bytes(commons_path, commons_raw)
    commons_pages = {
        title_key(page["title"]): page
        for page in commons_payload.get("query", {}).get("pages", [])
    }
    rights_by_title = {title_key(item["title"]): item for item in pdf_rights_records}
    for witness in pdf_records:
        title = commons_file_title(witness["source_file_title"])
        page = commons_pages.get(title_key(title))
        rights = rights_by_title.get(title_key(title))
        if page is None or rights is None or page.get("missing"):
            raise RuntimeError(f"final Commons PDF replay missing: {title}")
        info = page["imageinfo"][0]
        rev = base.revision(page)
        if int(info["size"]) != int(witness["source_bytes"]) or info["sha1"] != witness["mediawiki_sha1"]:
            raise RuntimeError(f"final Commons PDF byte drift: {title}")
        if int(rev["revid"]) != int(rights["revid"]) or rev["sha1"] != rights["mediawiki_sha1"]:
            raise RuntimeError(f"final Commons description drift: {title}")
    return {
        "result": "PASS",
        "wikiversity_identity_count": len(expected),
        "wikiversity_batches": batches,
        "commons_pdf_identity_count": len(pdf_records),
        "commons_replay_file": commons_path.name,
        "commons_replay_bytes": commons_path.stat().st_size,
        "commons_replay_sha256": base.digest(commons_path),
    }


def main() -> int:
    base.OUT.mkdir(parents=True, exist_ok=True)
    base.ARTIFACTS.mkdir(parents=True, exist_ok=True)
    base.ASSETS.mkdir(parents=True, exist_ok=True)

    lecture, lecture_parsed = base.entry_surface(base.LECTURE_TITLE, "lecture-21")
    worksheet, worksheet_parsed = base.entry_surface(base.WORKSHEET_TITLE, "worksheet-21")
    lecture_latex, lecture_tex = base.latex_surface(base.LECTURE_TITLE + "/latex", "lecture-21")
    worksheet_latex, worksheet_tex = base.latex_surface(
        base.WORKSHEET_TITLE + "/latex", "worksheet-21"
    )
    lecture_closure = base.transclusion_closure(lecture_parsed, "lecture-21")
    worksheet_closure = base.transclusion_closure(worksheet_parsed, "worksheet-21")
    semantic_audit_bindings = bind_audit_semantic_identities(
        lecture_closure, worksheet_closure
    )
    solutions = base.solution_map(worksheet, worksheet_parsed)
    if int(solutions["exercise_count"]) != 26 or int(solutions["solution_count"]) != 2:
        raise RuntimeError(
            "Unit 21 exercise/solution topology differs from the bounded preflight "
            f"(got {solutions['exercise_count']}/{solutions['solution_count']})"
        )
    solution_closures = solution_transclusion_closures(solutions)
    if any(item["direct_wrapper_dependency_titles"] for item in solution_closures):
        raise RuntimeError("Unit 21 public-solution wrapper shape changed from preflight")
    license_surface = course_license_surface()
    pdf_records, commons_pages = official_pdfs_no_assets(lecture_parsed, worksheet_parsed)
    media_closure = write_zero_media_rights(pdf_records, commons_pages, lecture)
    entry_recheck = base.final_identity_recheck(lecture["revid"], worksheet["revid"])

    solution_recursive_closures = [
        item["recursive_transclusion_closure"] for item in solution_closures
    ]
    all_recursive_closures = [
        lecture_closure,
        worksheet_closure,
        license_surface["recursive_transclusion_closure"],
        *solution_recursive_closures,
    ]
    primary_records = [
        lecture,
        worksheet,
        lecture_latex,
        worksheet_latex,
        license_surface["wrapper"],
    ]
    identity_replay = final_live_identity_replay(
        primary_records,
        all_recursive_closures,
        solutions,
        pdf_records,
        media_closure["official_pdf_component_rights"],
    )

    manifest = {
        "schema": "brenner-unit-authority-freeze-v2",
        "frozen_utc": datetime.now(timezone.utc).isoformat(),
        "unit_number": UNIT,
        "source_api": base.WIKI_API,
        "source_course_license": CURRENT_LICENSE,
        "source_course_license_authority": license_surface,
        "lecture": lecture,
        "worksheet": worksheet,
        "lecture_latex_page": lecture_latex,
        "worksheet_latex_page": worksheet_latex,
        "latex_capture_semantics": (
            "Each /latex page is a frozen launcher revision; expanded TeX is a byte-bound "
            "capture of its dynamic Parsoid rendering at freeze time."
        ),
        "derived_expanded_tex": [lecture_tex, worksheet_tex],
        "lecture_transclusion_closure": lecture_closure,
        "worksheet_transclusion_closure": worksheet_closure,
        "semantic_audit_identity_bindings": semantic_audit_bindings,
        "solutions": solutions,
        "solution_transclusion_closures": solution_closures,
        "images": {
            "lecture": lecture_parsed.get("images", []),
            "worksheet": worksheet_parsed.get("images", []),
            "substantive_assets": [],
            "reader_media_positions": 0,
        },
        "official_pdf_witnesses": pdf_records,
        "media_rights_accessibility_and_discrepancies": {
            "closure_file": base.CLOSURE.relative_to(ROOT).as_posix(),
            "closure_bytes": base.CLOSURE.stat().st_size,
            "closure_sha256": base.digest(base.CLOSURE),
            "rights_file": base.RIGHTS.relative_to(ROOT).as_posix(),
            "rights_bytes": base.RIGHTS.stat().st_size,
            "rights_sha256": base.digest(base.RIGHTS),
        },
        "entry_revision_recheck": entry_recheck,
        "final_live_identity_replay": identity_replay,
    }
    manifest["files"] = [
        {"file": path.name, "bytes": path.stat().st_size, "sha256": base.digest(path)}
        for path in sorted(base.OUT.iterdir(), key=lambda item: item.name)
        if path.is_file() and path.name != "UNIT_AUTHORITY_MANIFEST.json"
    ]
    external_paths = [
        *(ROOT / item["local_path"] for item in pdf_records),
        base.RIGHTS,
        base.CLOSURE,
        base.COMMONS_META,
    ]
    manifest["bounded_external_files"] = [
        {
            "file": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": base.digest(path),
        }
        for path in sorted(external_paths, key=lambda item: item.as_posix())
    ]
    manifest_path = base.OUT / "UNIT_AUTHORITY_MANIFEST.json"
    base.write_json(manifest_path, manifest)

    replay = json.loads(manifest_path.read_text(encoding="utf-8"))
    actual_names = {
        path.name
        for path in base.OUT.iterdir()
        if path.is_file() and path.name != manifest_path.name
    }
    bound_names = {item["file"] for item in replay["files"]}
    if actual_names != bound_names:
        raise RuntimeError("manifest-local file inventory replay failed")
    for record in replay["files"]:
        path = base.OUT / record["file"]
        if path.stat().st_size != record["bytes"] or base.digest(path) != record["sha256"]:
            raise RuntimeError(f"manifest replay failed: {path}")
    for record in replay["bounded_external_files"]:
        path = ROOT / record["file"]
        if path.stat().st_size != record["bytes"] or base.digest(path) != record["sha256"]:
            raise RuntimeError(f"external-file replay failed: {path}")
    parsed_exercises = [
        item
        for item in worksheet_parsed["templates"]
        if item.get("ns") != 10 and item["title"].endswith("/Aufgabe")
    ]
    if len(parsed_exercises) != 26 or replay["solutions"]["exercise_count"] != 26:
        raise RuntimeError("exercise topology replay failed")
    if replay["solutions"]["solution_count"] != 2 or len(solution_closures) != 2:
        raise RuntimeError("solution topology replay failed")
    if media_closure["reader_media_positions"] != 0 or media_closure["assets"]:
        raise RuntimeError("zero-media topology replay failed")
    if replay["final_live_identity_replay"]["result"] != "PASS":
        raise RuntimeError("final live identity replay did not pass")

    result = {
        "result": "PASS",
        "unit": UNIT,
        "lecture_pageid": lecture["pageid"],
        "lecture_revid": lecture["revid"],
        "worksheet_pageid": worksheet["pageid"],
        "worksheet_revid": worksheet["revid"],
        "lecture_transclusions": lecture_closure["captured_page_count"],
        "worksheet_transclusions": worksheet_closure["captured_page_count"],
        "solution_transclusions": [
            item["recursive_transclusion_closure"]["captured_page_count"]
            for item in solution_closures
        ],
        "exercises": solutions["exercise_count"],
        "public_solutions": solutions["solution_count"],
        "media_positions": 0,
        "official_pdf_pages": [item["page_count"] for item in pdf_records],
        "live_replay_identities": identity_replay["wikiversity_identity_count"],
        "manifest_bytes": manifest_path.stat().st_size,
        "manifest_sha256": base.digest(manifest_path),
        "rights_bytes": base.RIGHTS.stat().st_size,
        "rights_sha256": base.digest(base.RIGHTS),
        "closure_bytes": base.CLOSURE.stat().st_size,
        "closure_sha256": base.digest(base.CLOSURE),
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
