#!/usr/bin/env python3
"""Compare ordered Parsoid and translated-Markdown math surfaces."""

from __future__ import annotations

import difflib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

from bs4 import BeautifulSoup


LANE = Path(__file__).resolve().parents[1]


def normalize(tex: str) -> str:
    tex = tex.replace("{{}}", "")
    tex = tex.replace("\\mathbb {", "\\mathbb{")
    tex = tex.replace("\\mathbb ", "\\mathbb")
    return re.sub(r"\s+", "", tex).rstrip(".,;:")


def authority_math(path: Path) -> list[str]:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    result: list[str] = []
    for node in soup.find_all("math"):
        data = json.loads(node.get("data-mw", "{}"))
        result.append(data.get("body", {}).get("extsrc", node.get_text(" ")))
    return result


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def target_math(path: Path) -> list[str]:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise RuntimeError("pandoc is not on PATH")
    raw = subprocess.check_output(
        [
            pandoc,
            "--from=markdown+yaml_metadata_block+tex_math_dollars+fenced_divs+bracketed_spans",
            "--to=json",
            str(path),
        ],
        cwd=LANE,
    )
    ast = json.loads(raw)
    return [node["c"][1] for node in walk(ast["blocks"]) if node.get("t") == "Math"]


def compare(stem: str) -> bool:
    source = authority_math(LANE / "authority" / "wikiversity" / f"{stem}.html")
    target = target_math(LANE / "source" / "id-ID" / f"{stem}.md")
    left = [normalize(item) for item in source]
    right = [normalize(item) for item in target]
    matcher = difflib.SequenceMatcher(a=left, b=right, autojunk=False)
    problems = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != "equal":
            problems.append(
                {
                    "kind": tag,
                    "source_range": [i1 + 1, i2],
                    "target_range": [j1 + 1, j2],
                    "source": source[i1:i2],
                    "target": target[j1:j2],
                }
            )
    print(
        json.dumps(
            {
                "file": stem,
                "source_count": len(source),
                "target_count": len(target),
                "mismatches": problems,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return not problems


def main() -> int:
    stems = sys.argv[1:] or ["lecture-01", "worksheet-01"]
    return 0 if all(compare(stem) for stem in stems) else 1


if __name__ == "__main__":
    raise SystemExit(main())
