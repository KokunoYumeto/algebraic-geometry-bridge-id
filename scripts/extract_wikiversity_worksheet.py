#!/usr/bin/env python3
"""Create a clean review-only Markdown projection of a Wikiversity worksheet."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

from bs4 import BeautifulSoup


def pandoc_fragment(fragment: str) -> str:
    result = subprocess.run(
        ["pandoc", "--from=html", "--to=gfm", "--wrap=none"],
        input=fragment,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    value = result.stdout
    value = value.replace("$`", "$").replace("`$", "$")
    value = re.sub(r"\n{3,}", "\n\n", value).strip()
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    soup = BeautifulSoup(args.html.read_bytes(), "html.parser")
    rows = []
    for number, box in enumerate(soup.select("div.remark"), start=1):
        heading = box.find("h2")
        content = box.select_one("div.remark-content")
        if heading is None or content is None:
            raise RuntimeError(f"Malformed exercise box {number}")
        link = heading.find("a", title=True)
        source_title = link["title"] if link else ""
        heading_text = heading.get_text(" ", strip=True).replace("\u00a0", " ")
        star = "★" if "*" in heading_text else ""
        points_match = re.search(r"\((\d+)\s+Punkte\)", heading_text)
        points = f" — {points_match.group(1)} points" if points_match else ""
        rows.append(
            f"## Exercise {number} {star}{points}\n\n"
            f"Source entity: `{source_title}`\n\n"
            f"{pandoc_fragment(str(content))}\n"
        )
    args.output.write_text("\n".join(rows), encoding="utf-8")
    print(f"exercises={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
