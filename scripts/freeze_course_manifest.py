#!/usr/bin/env python3
"""Turn the captured Wikiversity course-prefix response into a frozen manifest."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re


LANE = Path(__file__).resolve().parents[1]
SOURCE = LANE / "authority" / "wikiversity" / "course-prefix-api.json"
MANIFEST = LANE / "authority" / "wikiversity" / "COURSE_PREFIX_MANIFEST.csv"
RECEIPT = LANE / "authority" / "wikiversity" / "COURSE_PREFIX_RECEIPT.json"
ROOT = "Kurs:Algebraische Kurven (Osnabrück 2025-2026)"


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def kind(title: str) -> str:
    if title == ROOT:
        return "course_root"
    suffix = title[len(ROOT) :]
    patterns = (
        (r"/Vorlesung \d+$", "lecture"),
        (r"/Arbeitsblatt \d+$", "worksheet"),
        (r"/Vorlesung \d+/kontrolle$", "lecture_control"),
        (r"/Arbeitsblatt \d+/kontrolle$", "worksheet_control"),
        (r"/Vorlesung \d+/latex$", "lecture_latex"),
        (r"/Arbeitsblatt \d+/latex$", "worksheet_latex"),
    )
    for pattern, label in patterns:
        if re.fullmatch(pattern, suffix, flags=re.IGNORECASE):
            return label
    return "course_local_other"


def main() -> int:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    if "continue" in data:
        raise RuntimeError("course-prefix capture is paginated/truncated")
    pages = data.get("query", {}).get("pages", [])
    if len(pages) != 433:
        raise RuntimeError(f"expected 433 course-prefix pages, found {len(pages)}")
    if len({page["pageid"] for page in pages}) != len(pages):
        raise RuntimeError("duplicate course-prefix page ID")
    if len({page["title"] for page in pages}) != len(pages):
        raise RuntimeError("duplicate course-prefix title")

    rows = []
    for ordinal, page in enumerate(sorted(pages, key=lambda item: item["title"].casefold()), 1):
        revision = page["revisions"][0]
        rows.append(
            {
                "ordinal": ordinal,
                "pageid": page["pageid"],
                "namespace": page["ns"],
                "kind": kind(page["title"]),
                "title": page["title"],
                "revid": revision["revid"],
                "parentid": revision["parentid"],
                "timestamp": revision["timestamp"],
                "mediawiki_sha1": revision["sha1"],
                "wikitext_bytes": revision["size"],
            }
        )
    root = next(row for row in rows if row["kind"] == "course_root")
    if root["pageid"] != 165855 or root["revid"] != 1074230:
        raise RuntimeError("course-root identity drift")

    with MANIFEST.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    counts: dict[str, int] = {}
    for row in rows:
        counts[row["kind"]] = counts.get(row["kind"], 0) + 1
    expected = {
        "course_root": 1,
        "lecture": 30,
        "worksheet": 30,
        "lecture_control": 30,
        "worksheet_control": 30,
        "lecture_latex": 30,
        "worksheet_latex": 30,
        "course_local_other": 252,
    }
    if counts != expected:
        raise RuntimeError(f"unexpected course-prefix classes: {counts!r}")

    receipt = {
        "schema": "brenner-course-prefix-receipt-v1",
        "source_api": "https://de.wikiversity.org/w/api.php",
        "namespace": 106,
        "prefix": "Algebraische Kurven (Osnabrück 2025-2026)",
        "capture_file": "authority/wikiversity/course-prefix-api.json",
        "capture_bytes": SOURCE.stat().st_size,
        "capture_sha256": sha256(SOURCE),
        "manifest_file": "authority/wikiversity/COURSE_PREFIX_MANIFEST.csv",
        "manifest_bytes": MANIFEST.stat().st_size,
        "manifest_sha256": sha256(MANIFEST),
        "page_count": len(rows),
        "classes": counts,
        "course_root": {
            key: root[key]
            for key in ("pageid", "revid", "parentid", "timestamp", "mediawiki_sha1", "wikitext_bytes")
        },
    }
    RECEIPT.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"pages": len(rows), "manifest_sha256": sha256(MANIFEST)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
