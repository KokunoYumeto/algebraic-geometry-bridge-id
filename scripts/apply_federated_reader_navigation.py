#!/usr/bin/env python3
"""Apply and verify D100's universal hosted-reader navigation.

The source of truth is ``source/federated-navigation/d100-reader-navigation-v1.json``.
The operation is byte-preserving outside two marked blocks and is idempotent.
It also fails closed if a new HTML file appears in the GitHub Pages tree without
being registered, so future reader additions cannot silently lose the route back
to the program or the authoritative originals.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = (
    ROOT / "source" / "federated-navigation" / "d100-reader-navigation-v1.json"
)
STYLE_START = "<!-- federated-program-navigation-style:v1:start -->"
STYLE_END = "<!-- federated-program-navigation-style:v1:end -->"
NAV_START = "<!-- federated-program-navigation:D100:v1:start -->"
NAV_END = "<!-- federated-program-navigation:D100:v1:end -->"
EN_PUBLIC_ROOT = ROOT / "docs" / "en"
EN_PUBLIC_MANIFEST = EN_PUBLIC_ROOT / "public-manifest.json"
EN_INVENTORY = EN_PUBLIC_ROOT / "sha256-inventory.json"
EN_PDFS = {
    "algebraic-curves-en-units-01-30.pdf",
    "bundles-sheaves-cohomology-en-units-01-30.pdf",
    "varieties-to-schemes-editorial-companion-en.pdf",
}


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_config() -> dict[str, object]:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    if config.get("schema") != "interlanguage-federated-reader-navigation-v1":
        raise RuntimeError("unexpected federated-navigation schema")
    if config.get("role_id") != "D100":
        raise RuntimeError("navigation configuration is not bound to D100")
    return config


def style_block() -> str:
    return """<!-- federated-program-navigation-style:v1:start -->
<style id="federated-program-navigation-style-v1">
.federated-program-nav{box-sizing:border-box;margin:0;padding:.8rem 1rem;background:#0f172a;color:#f8fafc;border-bottom:3px solid #38bdf8;font:600 1rem/1.45 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.federated-program-nav__inner{box-sizing:border-box;max-width:90rem;margin:0 auto;display:flex;flex-wrap:wrap;align-items:center;gap:.35rem .75rem}.federated-program-nav a{color:#e0f2fe;text-decoration:underline;text-decoration-thickness:.1em;text-underline-offset:.18em}.federated-program-nav a:visited{color:#e9d5ff}.federated-program-nav a:hover{color:#fff}.federated-program-nav a:focus-visible{outline:3px solid #fde047;outline-offset:3px}.federated-program-nav__label{color:#fff}.federated-program-nav__separator{color:#94a3b8}.federated-program-nav__sources{display:flex;flex-wrap:wrap;gap:.35rem .75rem}
</style>
<!-- federated-program-navigation-style:v1:end -->
"""


def nav_block(config: dict[str, object]) -> str:
    central = config["central_program"]
    originals = config["original_sources"]
    assert isinstance(central, dict)
    assert isinstance(originals, list)

    central_links: list[str] = []
    for key in ("id", "en"):
        row = central[key]
        assert isinstance(row, dict)
        central_links.append(
            '<a href="{url}" hreflang="{hreflang}">{label}</a>'.format(
                url=html.escape(str(row["url"]), quote=True),
                hreflang=html.escape(str(row["hreflang"]), quote=True),
                label=html.escape(str(row["label"])),
            )
        )

    source_links: list[str] = []
    for row in originals:
        assert isinstance(row, dict)
        source_links.append(
            '<a href="{url}" hreflang="{hreflang}" rel="external">{label}</a>'.format(
                url=html.escape(str(row["url"]), quote=True),
                hreflang=html.escape(str(row["hreflang"]), quote=True),
                label=html.escape(str(row["label"])),
            )
        )

    return (
        NAV_START
        + '\n<nav class="federated-program-nav" '
        + 'aria-label="Program matematika dan sumber asli / Mathematics program and original sources" '
        + 'data-program-role="D100">\n'
        + '  <div class="federated-program-nav__inner">\n'
        + '    <span class="federated-program-nav__label">Kembali ke program / Back to program:</span>\n'
        + "    "
        + ' <span class="federated-program-nav__separator" aria-hidden="true">·</span> '.join(central_links)
        + '\n    <span class="federated-program-nav__separator" aria-hidden="true">|</span>\n'
        + '    <span class="federated-program-nav__label">Sumber asli / Original sources:</span>\n'
        + '    <span class="federated-program-nav__sources">'
        + ' <span class="federated-program-nav__separator" aria-hidden="true">·</span> '.join(source_links)
        + "</span>\n"
        + "  </div>\n"
        + "</nav>\n"
        + NAV_END
        + "\n"
    )


def replace_or_insert(
    text: str, start: str, end: str, replacement: str, insertion: tuple[int, int]
) -> str:
    if start in text or end in text:
        if text.count(start) != 1 or text.count(end) != 1:
            raise RuntimeError(f"malformed marker pair: {start} / {end}")
        left = text.index(start)
        right = text.index(end, left) + len(end)
        if replacement.endswith("\n"):
            while right < len(text) and text[right] in "\r\n":
                right += 1
        return text[:left] + replacement + text[right:]
    begin, finish = insertion
    if replacement.endswith("\n"):
        while finish < len(text) and text[finish] in "\r\n":
            finish += 1
    return text[:begin] + replacement + text[finish:]


def apply_to_text(text: str, config: dict[str, object]) -> str:
    head_end = re.search(r"</head\s*>", text, flags=re.IGNORECASE)
    body_open = re.search(r"<body(?:\s[^>]*)?>", text, flags=re.IGNORECASE)
    if head_end is None or body_open is None:
        raise RuntimeError("HTML must contain one head close and one body open")

    styled = replace_or_insert(
        text,
        STYLE_START,
        STYLE_END,
        style_block(),
        (head_end.start(), head_end.start()),
    )
    body_open = re.search(r"<body(?:\s[^>]*)?>", styled, flags=re.IGNORECASE)
    if body_open is None:
        raise RuntimeError("HTML body disappeared while adding navigation style")

    insertion_at = body_open.end()
    after_body = styled[insertion_at:]
    skip = re.match(
        r"(?is)(\s*<a\b[^>]*class=[\"'][^\"']*\bskip-link\b[^\"']*[\"'][^>]*>.*?</a>)",
        after_body,
    )
    if skip is not None:
        insertion_at += skip.end()

    return replace_or_insert(
        styled,
        NAV_START,
        NAV_END,
        nav_block(config),
        (insertion_at, insertion_at),
    )


def inventory(config: dict[str, object]) -> tuple[list[Path], list[Path]]:
    declared_raw = config["published_html_files"]
    root_raw = config["published_html_root"]
    assert isinstance(declared_raw, list)
    declared = [ROOT / str(value) for value in declared_raw]
    actual = sorted((ROOT / str(root_raw)).rglob("*.html"))
    return declared, actual


def file_rows(root: Path, excluded: set[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    candidates = [
        (path.relative_to(root).as_posix(), path)
        for path in root.rglob("*")
        if path.is_file()
    ]
    for relative, path in sorted(candidates, key=lambda pair: pair[0]):
        if relative in excluded:
            continue
        rows.append(
            {
                "bytes": path.stat().st_size,
                "path": relative,
                "sha256": sha256(path),
            }
        )
    return rows


def closure_digest(rows: list[dict[str, object]]) -> str:
    rendered = json.dumps(rows, ensure_ascii=False, indent=2) + "\n"
    return sha256_bytes(rendered.encode("utf-8"))


def refresh_english_public_closure(config: dict[str, object]) -> None:
    """Refresh current Pages inventory while preserving the historical build receipt."""

    manifest = json.loads(EN_PUBLIC_MANIFEST.read_text(encoding="utf-8"))
    tree_rows = file_rows(
        EN_PUBLIC_ROOT,
        {"public-manifest.json", "sha256-inventory.json", *EN_PDFS},
    )
    manifest["html_tree"] = {
        **manifest["html_tree"],
        "bytes": sum(int(row["bytes"]) for row in tree_rows),
        "closure_sha256": closure_digest(tree_rows),
        "file_count": len(tree_rows),
        "preserved_byte_for_byte": False,
        "postprocessed_navigation": True,
    }
    manifest["federated_navigation"] = {
        "status": "PASS",
        "role_id": "D100",
        "config": CONFIG_PATH.relative_to(ROOT).as_posix(),
        "published_html_count": len(config["published_html_files"]),
        "english_html_count": 4,
        "central_links_per_document": 2,
        "original_source_links_per_document": 3,
        "historical_build_receipt_preserved": "build-receipt.json",
    }
    EN_PUBLIC_MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    inventory_payload = json.loads(EN_INVENTORY.read_text(encoding="utf-8"))
    inventory_payload["files"] = file_rows(EN_PUBLIC_ROOT, {"sha256-inventory.json"})
    EN_INVENTORY.write_text(
        json.dumps(inventory_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def validate_english_public_closure() -> dict[str, object]:
    inventory_payload = json.loads(EN_INVENTORY.read_text(encoding="utf-8"))
    recorded = inventory_payload.get("files")
    if not isinstance(recorded, list):
        raise RuntimeError("English public inventory has no file rows")
    actual = file_rows(EN_PUBLIC_ROOT, {"sha256-inventory.json"})
    if recorded != actual:
        raise RuntimeError("English public inventory does not match current bytes")

    manifest = json.loads(EN_PUBLIC_MANIFEST.read_text(encoding="utf-8"))
    tree_rows = file_rows(
        EN_PUBLIC_ROOT,
        {"public-manifest.json", "sha256-inventory.json", *EN_PDFS},
    )
    expected_tree = {
        "bytes": sum(int(row["bytes"]) for row in tree_rows),
        "closure_sha256": closure_digest(tree_rows),
        "file_count": len(tree_rows),
    }
    for key, value in expected_tree.items():
        if manifest["html_tree"].get(key) != value:
            raise RuntimeError(f"English HTML closure mismatch: {key}")
    if manifest.get("federated_navigation", {}).get("status") != "PASS":
        raise RuntimeError("English public manifest lacks federated navigation admission")
    return {
        "status": "pass",
        "file_count_excluding_inventory": len(actual),
        "html_tree": expected_tree,
        "public_manifest": {
            "path": EN_PUBLIC_MANIFEST.relative_to(ROOT).as_posix(),
            "bytes": EN_PUBLIC_MANIFEST.stat().st_size,
            "sha256": sha256(EN_PUBLIC_MANIFEST),
        },
        "sha256_inventory": {
            "path": EN_INVENTORY.relative_to(ROOT).as_posix(),
            "bytes": EN_INVENTORY.stat().st_size,
            "sha256": sha256(EN_INVENTORY),
        },
    }


def validate(config: dict[str, object]) -> dict[str, object]:
    declared, actual = inventory(config)
    if set(declared) != set(actual):
        missing = sorted(path.relative_to(ROOT).as_posix() for path in set(declared) - set(actual))
        undeclared = sorted(path.relative_to(ROOT).as_posix() for path in set(actual) - set(declared))
        raise RuntimeError(
            f"published HTML inventory mismatch; missing={missing}; undeclared={undeclared}"
        )

    expected_urls = [
        str(row["url"])
        for row in (
            list(config["central_program"].values())
            + list(config["original_sources"])
        )
    ]
    rows: list[dict[str, object]] = []
    for path in declared:
        payload = path.read_bytes()
        text = payload.decode("utf-8")
        if text.count(STYLE_START) != 1 or text.count(STYLE_END) != 1:
            raise RuntimeError(f"style marker failure: {path.relative_to(ROOT)}")
        if text.count(NAV_START) != 1 or text.count(NAV_END) != 1:
            raise RuntimeError(f"navigation marker failure: {path.relative_to(ROOT)}")
        if text.count('data-program-role="D100"') != 1:
            raise RuntimeError(f"D100 role marker failure: {path.relative_to(ROOT)}")
        nav = text[
            text.index(NAV_START) : text.index(NAV_END, text.index(NAV_START))
            + len(NAV_END)
        ]
        for url in expected_urls:
            if nav.count(html.escape(url, quote=True)) != 1:
                raise RuntimeError(
                    f"required navigation URL missing or duplicated in {path.relative_to(ROOT)}: {url}"
                )
        if apply_to_text(text, config) != text:
            raise RuntimeError(f"navigation is not idempotent: {path.relative_to(ROOT)}")
        rows.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": len(payload),
                "sha256": sha256_bytes(payload),
                "central_links": 2,
                "original_links": 3,
                "marker_count": 1
            }
        )

    return {
        "schema": "interlanguage-federated-reader-navigation-qa-v1",
        "role_id": "D100",
        "status": "pass",
        "pages_source": {"branch": "main", "path": "/docs"},
        "config": {
            "path": CONFIG_PATH.relative_to(ROOT).as_posix(),
            "bytes": CONFIG_PATH.stat().st_size,
            "sha256": sha256(CONFIG_PATH)
        },
        "script": {
            "path": Path(__file__).resolve().relative_to(ROOT).as_posix(),
            "bytes": Path(__file__).resolve().stat().st_size,
            "sha256": sha256(Path(__file__).resolve())
        },
        "published_html_count": len(rows),
        "expected_links_per_document": 5,
        "documents": rows,
        "english_public_closure": validate_english_public_closure()
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="apply or refresh marked blocks")
    parser.add_argument("--check", action="store_true", help="validate without changing HTML")
    parser.add_argument("--report", type=Path, help="write deterministic JSON validation report")
    args = parser.parse_args()
    if args.apply == args.check:
        parser.error("choose exactly one of --apply or --check")

    config = load_config()
    if args.apply:
        declared, actual = inventory(config)
        if set(declared) != set(actual):
            raise RuntimeError("refusing to apply: published HTML inventory is not exact")
        for path in declared:
            payload = path.read_bytes()
            text = payload.decode("utf-8")
            updated = apply_to_text(text, config)
            path.write_bytes(updated.encode("utf-8"))
        refresh_english_public_closure(config)

    report = validate(config)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        report_path = args.report if args.report.is_absolute() else ROOT / args.report
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(rendered, encoding="utf-8", newline="\n")
    sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
