#!/usr/bin/env python3
"""Create a clean review-only Markdown projection of frozen solution pages."""

from __future__ import annotations

import argparse
import json
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
    value = result.stdout.replace("$`", "$").replace("`$", "$")
    return re.sub(r"\n{3,}", "\n\n", value).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authority-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    mapping = json.loads((args.authority_dir / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
    rows = []
    for entry in mapping["entries"]:
        if not entry["has_public_solution"]:
            continue
        html_path = args.authority_dir / entry["html_file"]
        soup = BeautifulSoup(html_path.read_bytes(), "html.parser")
        box = soup.find("div", style=re.compile(r"border\s*:\s*5px\s+solid\s+grey", re.I))
        if box is None:
            raise RuntimeError(f"Solution content box not found: {html_path.name}")
        rows.append(
            f"## Solution to Exercise {entry['exercise_number']}\n\n"
            f"Source revision: `{entry['revid']}`\n\n"
            f"{pandoc_fragment(str(box))}\n"
        )
    args.output.write_text("\n".join(rows), encoding="utf-8")
    print(f"solutions={len(rows)} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
