#!/usr/bin/env python3
"""Freeze one BGK lecture/worksheet unit from official Wikiversity APIs.

This is a storage-isolated adapter over :mod:`freeze_brenner_unit`.  It keeps
the established capture semantics (revision metadata, XML, rendered HTML,
semantic parse surfaces, transclusion closure, ordered exercises, every public
solution, /latex pages, derived TeX witnesses, and official PDFs) while using
BGK-only authority and artifact names.  It never writes to the classical
``authority/wikiversity`` unit tree.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import freeze_brenner_unit as core


ROOT = Path(__file__).resolve().parents[1]
COURSE = "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)"
COURSE_NAMESPACE_LABEL = "Kurs"
AUTHORITY_NAMESPACE = Path("authority") / "wikiversity-bgk"
ARTIFACT_PREFIX = "bgk"
UNIT_MIN = 1
UNIT_MAX = 30


def unit_plan(unit: int) -> dict[str, Any]:
    """Return the exact no-I/O capture plan for a BGK unit."""
    target = ROOT / AUTHORITY_NAMESPACE / f"unit-{unit:02d}"
    lecture_title = f"{COURSE}/Vorlesung {unit}"
    worksheet_title = f"{COURSE}/Arbeitsblatt {unit}"
    return {
        "course_title": COURSE,
        "source_namespace_label": COURSE_NAMESPACE_LABEL,
        "unit": unit,
        "lecture_title": lecture_title,
        "worksheet_title": worksheet_title,
        "lecture_latex_title": lecture_title + "/latex",
        "worksheet_latex_title": worksheet_title + "/latex",
        "authority_target": target.relative_to(ROOT).as_posix(),
        "authority_namespace": AUTHORITY_NAMESPACE.as_posix(),
        "official_pdf_name_pattern": f"authority/artifacts/{ARTIFACT_PREFIX}-<kind>-{unit:02d}-official.pdf",
    }


def validate_unit(unit: int) -> None:
    if not UNIT_MIN <= unit <= UNIT_MAX:
        raise SystemExit(f"--unit must be between {UNIT_MIN} and {UNIT_MAX}")


def kind_for_pdf(title: str) -> str:
    if "Vorlesung" in title:
        return "lecture"
    if "Arbeitsblatt" in title:
        return "worksheet"
    return "other"


def freeze_official_pdfs(
    *,
    unit: int,
    image_names: list[str],
    target: Path,
    resume: bool,
) -> list[dict[str, Any]]:
    """Capture all official PDF surfaces under noncolliding BGK names."""
    pdf_names = sorted({name for name in image_names if name.lower().endswith(".pdf")})
    if not pdf_names:
        raise RuntimeError("No official PDF file surfaces found in parse images")

    metadata_path = target / "official-pdfs-api.json"
    _raw, parsed = core.api_or_reuse(
        metadata_path,
        {
            "action": "query",
            "prop": "imageinfo",
            "iiprop": "url|size|mime|sha1|timestamp",
            "titles": "|".join("File:" + name for name in pdf_names),
        },
        resume=resume,
    )

    rows: list[tuple[dict[str, Any], dict[str, Any], str, str]] = []
    for page in parsed.get("query", {}).get("pages", []):
        info_rows = page.get("imageinfo", [])
        if len(info_rows) != 1:
            raise RuntimeError(f"No unique official PDF imageinfo for {page.get('title')}")
        info = info_rows[0]
        title = page["title"].removeprefix("File:")
        rows.append((page, info, title, kind_for_pdf(title)))
    rows.sort(key=lambda row: row[2].casefold())

    kind_counts = Counter(row[3] for row in rows)
    kind_ordinals: defaultdict[str, int] = defaultdict(int)
    artifact_root = ROOT / "authority" / "artifacts"
    artifact_root.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    for page, info, title, kind in rows:
        kind_ordinals[kind] += 1
        if kind_counts[kind] == 1:
            filename = f"{ARTIFACT_PREFIX}-{kind}-{unit:02d}-official.pdf"
        else:
            filename = (
                f"{ARTIFACT_PREFIX}-{kind}-{unit:02d}-"
                f"{kind_ordinals[kind]:02d}-official.pdf"
            )
        output = artifact_root / filename
        if output.exists() and not resume:
            raise RuntimeError(f"Refusing to overwrite existing BGK PDF witness: {output}")
        # MediaWiki appends analytics parameters to the byte-identical upload
        # URL.  Fetch the canonical query-free URL so an unrelated UTM throttle
        # cannot strand a resumable authority capture.
        download_url = info["url"].split("?", 1)[0]
        pdf_raw = core.fetch_or_reuse(
            output,
            download_url,
            resume=resume,
            accept="application/pdf",
        )
        if not pdf_raw.startswith(b"%PDF-"):
            raise RuntimeError(f"Official PDF does not have a PDF signature: {title}")
        records.append(
            {
                "kind": kind,
                "source_file_title": title,
                "pageid": page.get("pageid"),
                "image_timestamp": info.get("timestamp"),
                "mediawiki_sha1": info.get("sha1"),
                "source_bytes": info.get("size"),
                "mime": info.get("mime"),
                "source_url": info["url"],
                "canonical_download_url": download_url,
                "description_url": info.get("descriptionurl"),
                "local_path": output.relative_to(ROOT).as_posix(),
                "local_bytes": len(pdf_raw),
                "local_sha256": core.sha256(output),
            }
        )

    captured_kinds = {record["kind"] for record in records}
    if not {"lecture", "worksheet"}.issubset(captured_kinds):
        raise RuntimeError(
            f"Official PDF closure lacks lecture or worksheet witness: {records}"
        )
    return sorted(records, key=lambda record: record["local_path"])


def captured_namespace(api_file: Path, expected_title: str) -> int:
    """Verify an entry API file and return its captured namespace number."""
    parsed = json.loads(api_file.read_text(encoding="utf-8"))
    page, _revision, _content = core.revision_page(parsed, expected_title)
    if page.get("title") != expected_title:
        raise RuntimeError(
            f"Captured title mismatch: expected {expected_title!r}, got {page.get('title')!r}"
        )
    namespace = page.get("ns")
    if not isinstance(namespace, int):
        raise RuntimeError(f"Missing numeric source namespace for {expected_title!r}")
    return namespace


def capture_identity(plan: dict[str, Any]) -> dict[str, Any]:
    """Return the immutable identity marker written before the first fetch."""
    return {
        "schema": "brenner-bgk-capture-identity-v1",
        "course_title": COURSE,
        "source_namespace_label": COURSE_NAMESPACE_LABEL,
        "authority_namespace": AUTHORITY_NAMESPACE.as_posix(),
        "artifact_prefix": ARTIFACT_PREFIX,
        "unit": plan["unit"],
        "lecture_title": plan["lecture_title"],
        "worksheet_title": plan["worksheet_title"],
        "lecture_latex_title": plan["lecture_latex_title"],
        "worksheet_latex_title": plan["worksheet_latex_title"],
    }


def validate_resume_identity(target: Path, plan: dict[str, Any]) -> None:
    """Reject reuse of any files not carrying the exact BGK identity marker."""
    marker_path = target / "CAPTURE_IDENTITY.json"
    if any(target.iterdir()):
        if not marker_path.is_file():
            raise RuntimeError(
                f"Refusing --resume without BGK identity marker: {marker_path}"
            )
        observed_marker = json.loads(marker_path.read_text(encoding="utf-8"))
        expected_marker = capture_identity(plan)
        if observed_marker != expected_marker:
            raise RuntimeError(
                "Refusing --resume across capture identity: "
                f"expected {expected_marker}, got {observed_marker}"
            )

    manifest_path = target / "UNIT_AUTHORITY_MANIFEST.json"
    if not manifest_path.is_file():
        return
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    identity = manifest.get("source_identity", {})
    storage = manifest.get("storage_identity", {})
    expected = {
        "course_title": COURSE,
        "source_namespace_label": COURSE_NAMESPACE_LABEL,
    }
    observed = {
        "course_title": identity.get("course_title"),
        "source_namespace_label": identity.get("source_namespace_label"),
    }
    if observed != expected:
        raise RuntimeError(
            f"Refusing --resume across course identity: expected {expected}, got {observed}"
        )
    if storage.get("authority_namespace") != AUTHORITY_NAMESPACE.as_posix():
        raise RuntimeError(
            "Refusing --resume across authority namespace: "
            f"expected {AUTHORITY_NAMESPACE.as_posix()!r}, "
            f"got {storage.get('authority_namespace')!r}"
        )
    if manifest.get("unit_number") != plan["unit"]:
        raise RuntimeError("Refusing --resume across unit identity")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Freeze one BGK unit into its isolated Wikiversity authority namespace."
    )
    parser.add_argument("--unit", type=int, required=True)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--plan-only",
        action="store_true",
        help="print exact titles and output namespaces without network or filesystem writes",
    )
    args = parser.parse_args()
    unit = args.unit
    validate_unit(unit)
    plan = unit_plan(unit)
    if args.plan_only:
        print(json.dumps({"status": "PLAN_ONLY", **plan}, ensure_ascii=False))
        return

    target = ROOT / AUTHORITY_NAMESPACE / f"unit-{unit:02d}"
    if target.exists() and any(target.iterdir()) and not args.resume:
        raise SystemExit(f"Refusing to overwrite non-empty authority directory: {target}")
    if args.resume and target.exists():
        validate_resume_identity(target, plan)
    target.mkdir(parents=True, exist_ok=True)
    identity_path = target / "CAPTURE_IDENTITY.json"
    if not identity_path.exists():
        core.write_json(identity_path, capture_identity(plan))

    lecture_title = plan["lecture_title"]
    worksheet_title = plan["worksheet_title"]
    lecture, lecture_wikitext, lecture_parse = core.freeze_entry(
        title=lecture_title,
        stem=f"lecture-{unit:02d}",
        target=target,
        resume=args.resume,
        parse_surface=True,
    )
    worksheet, worksheet_wikitext, worksheet_parse = core.freeze_entry(
        title=worksheet_title,
        stem=f"worksheet-{unit:02d}",
        target=target,
        resume=args.resume,
        parse_surface=True,
    )
    assert lecture_parse is not None and worksheet_parse is not None

    lecture_latex, _, _ = core.freeze_entry(
        title=lecture_title + "/latex",
        stem=f"lecture-{unit:02d}-latex-page",
        target=target,
        resume=args.resume,
        parse_surface=False,
    )
    worksheet_latex, _, _ = core.freeze_entry(
        title=worksheet_title + "/latex",
        stem=f"worksheet-{unit:02d}-latex-page",
        target=target,
        resume=args.resume,
        parse_surface=False,
    )
    lecture_tex = target / f"lecture-{unit:02d}-expanded.tex"
    worksheet_tex = target / f"worksheet-{unit:02d}-expanded.tex"
    core.derive_tex(target / lecture_latex["html_file"], lecture_tex)
    core.derive_tex(target / worksheet_latex["html_file"], worksheet_tex)

    lecture_templates = [
        row["title"] for row in lecture_parse["parse"].get("templates", [])
    ]
    worksheet_templates = [
        row["title"] for row in worksheet_parse["parse"].get("templates", [])
    ]
    lecture_closure = core.transclusion_closure(
        prefix=f"lecture-{unit:02d}",
        template_titles=lecture_templates,
        target=target,
        resume=args.resume,
    )
    worksheet_closure = core.transclusion_closure(
        prefix=f"worksheet-{unit:02d}",
        template_titles=worksheet_templates,
        target=target,
        resume=args.resume,
    )
    _ordered_map, solutions = core.freeze_solutions(
        unit=unit,
        worksheet_record=worksheet,
        worksheet_wikitext=worksheet_wikitext,
        target=target,
        resume=args.resume,
    )

    lecture_images = lecture_parse["parse"].get("images", [])
    worksheet_images = worksheet_parse["parse"].get("images", [])
    official_pdfs = freeze_official_pdfs(
        unit=unit,
        image_names=lecture_images + worksheet_images,
        target=target,
        resume=args.resume,
    )

    source_namespaces = {
        "lecture": captured_namespace(
            target / f"lecture-{unit:02d}-api.json", lecture_title
        ),
        "worksheet": captured_namespace(
            target / f"worksheet-{unit:02d}-api.json", worksheet_title
        ),
        "lecture_latex": captured_namespace(
            target / f"lecture-{unit:02d}-latex-page-api.json",
            lecture_title + "/latex",
        ),
        "worksheet_latex": captured_namespace(
            target / f"worksheet-{unit:02d}-latex-page-api.json",
            worksheet_title + "/latex",
        ),
    }

    manifest_path = target / "UNIT_AUTHORITY_MANIFEST.json"
    frozen_utc = datetime.now(timezone.utc).isoformat()
    if args.resume and manifest_path.is_file():
        existing_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        existing_frozen_utc = existing_manifest.get("frozen_utc")
        if not isinstance(existing_frozen_utc, str) or not existing_frozen_utc:
            raise RuntimeError("Existing BGK unit manifest lacks a valid frozen_utc")
        frozen_utc = existing_frozen_utc
    files = [
        core.file_fact(path, target)
        for path in sorted(target.iterdir())
        if path.is_file() and path != manifest_path
    ]
    manifest = {
        "schema": "brenner-bgk-unit-authority-freeze-v1",
        "frozen_utc": frozen_utc,
        "unit_number": unit,
        "source_identity": {
            "project": "German Wikiversity",
            "course_title": COURSE,
            "source_namespace_label": COURSE_NAMESPACE_LABEL,
            "captured_namespace_ids": source_namespaces,
            "source_api": core.API,
            "lecture_title": lecture_title,
            "worksheet_title": worksheet_title,
        },
        "storage_identity": {
            "authority_namespace": AUTHORITY_NAMESPACE.as_posix(),
            "unit_directory": target.relative_to(ROOT).as_posix(),
            "artifact_prefix": ARTIFACT_PREFIX,
        },
        "source_api": core.API,
        "lecture": lecture,
        "worksheet": worksheet,
        "lecture_latex_page": lecture_latex,
        "worksheet_latex_page": worksheet_latex,
        "derived_expanded_tex": [
            core.file_fact(lecture_tex, target),
            core.file_fact(worksheet_tex, target),
        ],
        "lecture_transclusion_closure": lecture_closure,
        "worksheet_transclusion_closure": worksheet_closure,
        "solutions": solutions,
        "images": {"lecture": lecture_images, "worksheet": worksheet_images},
        "official_pdf_witnesses": official_pdfs,
        "files": files,
    }
    core.write_json(manifest_path, manifest)

    print(
        json.dumps(
            {
                "status": "PASS",
                "course_title": COURSE,
                "authority_namespace": AUTHORITY_NAMESPACE.as_posix(),
                "unit": unit,
                "lecture_revid": lecture["revid"],
                "worksheet_revid": worksheet["revid"],
                "lecture_transclusions": lecture_closure["captured_page_count"],
                "worksheet_transclusions": worksheet_closure["captured_page_count"],
                "exercises": solutions["exercise_count"],
                "public_solutions": solutions["solution_count"],
                "images": len(set(lecture_images + worksheet_images)),
                "manifest_files": len(files),
                "manifest": manifest_path.relative_to(ROOT).as_posix(),
                "manifest_bytes": manifest_path.stat().st_size,
                "manifest_sha256": core.sha256(manifest_path),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise
