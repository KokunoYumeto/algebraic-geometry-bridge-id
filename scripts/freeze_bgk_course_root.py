#!/usr/bin/env python3
"""Freeze the official BGK course root and prove its 30+30 unit surface.

This script writes only to the dedicated BGK authority namespace.  It captures
the current course-root revision/XML/HTML/parse surfaces, current identities for
all 30 lectures and 30 worksheets, and the official complete-course PDF.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pypdf import PdfReader

from freeze_brenner_unit import (
    API,
    REVISION_PROPS,
    ROOT,
    api_or_reuse,
    fetch_or_reuse,
    file_fact,
    freeze_entry,
    page_metadata,
    sha256,
    write_json,
)


COURSE = "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)"
TARGET = ROOT / "authority" / "wikiversity-bgk" / "course"
PDF_TARGET = ROOT / "authority" / "artifacts" / "bgk-course-official.pdf"
EXPECTED_PDF_PAGES = 265
EXPECTED_PDF_BYTES = 2_104_862
EXPECTED_PDF_SHA256 = "87655cf7e96dc0eaa185ca49a374dc9e25f4b739670495f423279aa332fce66c"


def capture_unit_index(*, target: Path, resume: bool) -> dict[str, Any]:
    expected: list[tuple[str, int, str]] = []
    for unit in range(1, 31):
        expected.append(("lecture", unit, f"{COURSE}/Vorlesung {unit}"))
        expected.append(("worksheet", unit, f"{COURSE}/Arbeitsblatt {unit}"))

    by_title: dict[str, dict[str, Any]] = {}
    batches: list[dict[str, Any]] = []
    titles = [title for _, _, title in expected]
    for start in range(0, len(titles), 25):
        batch_titles = titles[start : start + 25]
        path = target / f"unit-index-{start // 25 + 1:02d}.json"
        raw, parsed = api_or_reuse(
            path,
            {
                "action": "query",
                "prop": "revisions",
                "rvprop": REVISION_PROPS,
                "rvslots": "main",
                "titles": "|".join(batch_titles),
            },
            resume=resume,
        )
        pages = parsed.get("query", {}).get("pages", [])
        missing = [page.get("title") for page in pages if page.get("missing")]
        if missing:
            raise RuntimeError(f"Missing BGK unit pages: {missing}")
        for page in pages:
            revisions = page.get("revisions", [])
            if len(revisions) != 1:
                raise RuntimeError(f"No unique current revision for {page.get('title')!r}")
            revision = revisions[0]
            content = revision.get("slots", {}).get("main", {}).get("content")
            if not isinstance(content, str):
                raise RuntimeError(f"No main-slot content for {page.get('title')!r}")
            by_title[page["title"]] = page_metadata(page, revision, content)
        batches.append(
            {
                "file": path.name,
                "bytes": len(raw),
                "sha256": sha256(path),
                "requested_titles": batch_titles,
            }
        )

    missing_expected = [title for title in titles if title not in by_title]
    if missing_expected or len(by_title) != 60:
        raise RuntimeError(
            f"BGK 30+30 closure failed: captured={len(by_title)}, missing={missing_expected}"
        )

    rows = [
        {"kind": kind, "unit": unit, **by_title[title]}
        for kind, unit, title in expected
    ]
    return {
        "expected_lectures": 30,
        "expected_worksheets": 30,
        "captured_lectures": sum(row["kind"] == "lecture" for row in rows),
        "captured_worksheets": sum(row["kind"] == "worksheet" for row in rows),
        "batches": batches,
        "rows": rows,
    }


def freeze_course_pdf(
    *, root_parse: dict[str, Any], target: Path, resume: bool
) -> dict[str, Any]:
    image_names = root_parse.get("parse", {}).get("images", [])
    pdf_names = sorted({name for name in image_names if name.lower().endswith(".pdf")})
    candidates = [name for name in pdf_names if "Bündel" in name or "Garben" in name]
    if len(candidates) != 1:
        raise RuntimeError(f"Expected one official BGK course PDF, found {pdf_names}")
    pdf_name = candidates[0]
    metadata_path = target / "course-pdf-rights-api.json"
    raw, parsed = api_or_reuse(
        metadata_path,
        {
            "action": "query",
            "prop": "imageinfo",
            "iiprop": "url|size|mime|sha1|timestamp|extmetadata",
            "titles": "File:" + pdf_name,
        },
        resume=resume,
    )
    pages = parsed.get("query", {}).get("pages", [])
    # A Commons-hosted file can carry MediaWiki's local-wiki ``missing`` flag
    # while still returning authoritative shared-repository imageinfo.
    if len(pages) != 1:
        raise RuntimeError(f"Official BGK PDF metadata is missing: {pdf_name}")
    info_rows = pages[0].get("imageinfo", [])
    if len(info_rows) != 1:
        raise RuntimeError(f"Official BGK PDF has ambiguous imageinfo: {pdf_name}")
    info = info_rows[0]

    PDF_TARGET.parent.mkdir(parents=True, exist_ok=True)
    pdf_raw = fetch_or_reuse(PDF_TARGET, info["url"], resume=resume, accept="application/pdf")
    if not pdf_raw.startswith(b"%PDF-"):
        raise RuntimeError("Official BGK course witness lacks a PDF signature")
    pages_count = len(PdfReader(PDF_TARGET).pages)
    observed_sha256 = sha256(PDF_TARGET)
    if (
        len(pdf_raw) != EXPECTED_PDF_BYTES
        or pages_count != EXPECTED_PDF_PAGES
        or observed_sha256 != EXPECTED_PDF_SHA256
    ):
        raise RuntimeError(
            "Official BGK PDF identity differs from the admitted witness: "
            f"pages={pages_count}, bytes={len(pdf_raw)}, sha256={observed_sha256}"
        )
    extmetadata = info.get("extmetadata", {})
    rights = {
        key: extmetadata[key].get("value")
        for key in ("LicenseShortName", "LicenseUrl", "UsageTerms", "Artist", "Credit")
        if isinstance(extmetadata.get(key), dict)
    }
    if rights.get("LicenseShortName") != "CC BY-SA 4.0":
        raise RuntimeError(f"Unexpected official BGK PDF component licence: {rights}")
    return {
        "source_file_title": pdf_name,
        "pageid": pages[0].get("pageid"),
        "image_timestamp": info.get("timestamp"),
        "mediawiki_sha1": info.get("sha1"),
        "source_bytes": info.get("size"),
        "mime": info.get("mime"),
        "source_url": info["url"],
        "description_url": info.get("descriptionurl"),
        "metadata_file": metadata_path.name,
        "metadata_bytes": len(raw),
        "metadata_sha256": sha256(metadata_path),
        "local_path": PDF_TARGET.relative_to(ROOT).as_posix(),
        "local_bytes": len(pdf_raw),
        "local_pages": pages_count,
        "local_sha256": observed_sha256,
        "admitted_identity_match": True,
        "component_rights": rights,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    if TARGET.exists() and any(TARGET.iterdir()) and not args.resume:
        raise SystemExit(f"Refusing to overwrite non-empty BGK authority directory: {TARGET}")
    TARGET.mkdir(parents=True, exist_ok=True)

    root, _, root_parse = freeze_entry(
        title=COURSE,
        stem="course-root",
        target=TARGET,
        resume=args.resume,
        parse_surface=True,
    )
    if root_parse is None:
        raise RuntimeError("BGK course-root parse surface was not captured")
    unit_index = capture_unit_index(target=TARGET, resume=args.resume)
    official_pdf = freeze_course_pdf(root_parse=root_parse, target=TARGET, resume=args.resume)

    manifest_path = TARGET / "COURSE_AUTHORITY_MANIFEST.json"
    frozen_utc = datetime.now(timezone.utc).isoformat()
    if args.resume and manifest_path.is_file():
        existing_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        existing_frozen_utc = existing_manifest.get("frozen_utc")
        if not isinstance(existing_frozen_utc, str) or not existing_frozen_utc:
            raise RuntimeError("Existing BGK course manifest lacks a valid frozen_utc")
        frozen_utc = existing_frozen_utc
    files = [
        file_fact(path, TARGET)
        for path in sorted(TARGET.iterdir())
        if path.is_file() and path != manifest_path
    ]
    manifest = {
        "schema": "brenner-bgk-course-authority-freeze-v1",
        "frozen_utc": frozen_utc,
        "course": COURSE,
        "source_api": API,
        "authority_namespace": "authority/wikiversity-bgk",
        "course_root": root,
        "unit_index": unit_index,
        "official_course_pdf": official_pdf,
        "rights_boundary": {
            "course_text": "CC BY-SA 4.0",
            "official_course_pdf_component": official_pdf["component_rights"],
            "official_course_pdf_visible_notice": "CC BY-SA 3.0 on PDF page 265",
            "official_course_pdf_resolution": "preserve both the current Commons CC BY-SA 4.0 metadata and the embedded PDF CC BY-SA 3.0 notice; make no blanket relicensing claim",
            "media": "per-component rights must be frozen per unit",
            "blanket_relicense_claim": False,
        },
        "files": files,
    }
    write_json(manifest_path, manifest)
    print(
        json.dumps(
            {
                "status": "PASS",
                "course_root_revid": root["revid"],
                "lectures": unit_index["captured_lectures"],
                "worksheets": unit_index["captured_worksheets"],
                "pdf_pages": official_pdf["local_pages"],
                "pdf_bytes": official_pdf["local_bytes"],
                "pdf_sha256": official_pdf["local_sha256"],
                "manifest": manifest_path.relative_to(ROOT).as_posix(),
                "manifest_bytes": manifest_path.stat().st_size,
                "manifest_sha256": sha256(manifest_path),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
