#!/usr/bin/env python3
"""Build the independent Indonesian BGK reader in its own output namespace."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone


LANE = Path(__file__).resolve().parents[1]
SOURCE_ROOT = LANE / "source" / "id-ID"
SOURCE_DIR = SOURCE_ROOT / "bgk"
ASSET_DIR = LANE / "authority" / "assets"
BUILD_DIR = LANE / "build"
FINAL_DIR = BUILD_DIR / "reader-bgk-id"
CSS = SOURCE_ROOT / "reader.css"
PDF_HEADER = SOURCE_ROOT / "pdf-header.tex"
EXPECTED_PANDOC = "pandoc 3.9.0.2"
SOURCE_DATE_EPOCH = "1787875200"  # 2026-08-28T00:00:00Z
PDF_ID_PATTERN = re.compile(
    rb"/ID \[ <[0-9A-Fa-f]{32}> <[0-9A-Fa-f]{32}> \]"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fact(path: Path) -> dict[str, object]:
    return {
        "path": path.relative_to(LANE).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def regular(path: Path) -> None:
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"required regular file is missing or linked: {path}")


def add_html_landmarks(path: Path) -> None:
    """Wrap Pandoc's post-TOC reader content in one accessible main landmark."""

    text = path.read_text(encoding="utf-8")
    if "<main" in text or 'id="main-content"' in text:
        raise RuntimeError("HTML already contains a main landmark")
    body_match = re.search(r"<body(?:\s[^>]*)?>", text)
    if body_match is None:
        raise RuntimeError("Pandoc HTML lacks an opening body tag")
    if text.count("</nav>") != 1 or text.count("</body>") != 1:
        raise RuntimeError("Pandoc HTML has an unexpected nav/body structure")

    skip_link = (
        '\n<a class="skip-link" href="#main-content">Langsung ke isi utama</a>'
    )
    text = text[: body_match.end()] + skip_link + text[body_match.end() :]
    nav_end = text.index("</nav>") + len("</nav>")
    text = (
        text[:nav_end]
        + '\n<main id="main-content" tabindex="-1">'
        + text[nav_end:]
    )
    body_end = text.index("</body>")
    text = text[:body_end] + "</main>\n" + text[body_end:]
    path.write_text(text, encoding="utf-8", newline="\n")


def cumulative_inputs(
    through: int,
) -> tuple[tuple[Path, ...], dict[str, str]]:
    """Return every build-affecting frozen input through ``through``.

    Media closures are the authoritative unit-local index.  HTML keeps each
    selected asset (including animation); the PDF source substitutes only an
    explicitly frozen static fallback recorded by the closure.
    """

    inputs: list[Path] = [
        CSS,
        PDF_HEADER,
        LANE
        / "authority"
        / "wikiversity-bgk"
        / "course"
        / "COURSE_AUTHORITY_MANIFEST.json",
    ]
    pdf_replacements: dict[str, str] = {}
    fallback_keys = (
        "pdf_local_path",
        "pdf_fallback_local_path",
        "pdf_fallback_path",
        "pdf_static_fallback_path",
        "pdf_first_frame_path",
    )
    for unit in range(1, through + 1):
        closure_path = (
            LANE / "authority" / f"ASSET_CLOSURE-bgk-unit-{unit:02d}.json"
        )
        regular(closure_path)
        closure = json.loads(closure_path.read_text(encoding="utf-8"))
        if closure.get("unit") != unit:
            raise RuntimeError(
                f"media closure unit mismatch: expected {unit}, got {closure.get('unit')}"
            )
        manifest_rel = closure.get("authority_manifest", {}).get("path")
        rights_rel = closure.get("rights_file")
        if not isinstance(manifest_rel, str) or not isinstance(rights_rel, str):
            raise RuntimeError(f"incomplete authority/rights binding in {closure_path}")
        inputs.extend((LANE / manifest_rel, closure_path, LANE / rights_rel))
        for asset in closure.get("assets", []):
            local_rel = asset.get("local_path")
            if not isinstance(local_rel, str):
                raise RuntimeError(f"asset lacks local_path in {closure_path}")
            inputs.append(LANE / local_rel)
            fallback_rel = next(
                (
                    asset.get(key)
                    for key in fallback_keys
                    if isinstance(asset.get(key), str) and asset.get(key)
                ),
                None,
            )
            if fallback_rel is not None:
                inputs.append(LANE / fallback_rel)
                pdf_replacements[local_rel.replace("\\", "/")] = fallback_rel.replace(
                    "\\", "/"
                )

    # Preserve the first occurrence and make duplicate file references explicit
    # only once in the deterministic receipt.
    unique_inputs = tuple(dict.fromkeys(inputs))
    return unique_inputs, pdf_replacements


def normalize_pdf_id(path: Path) -> str:
    """Replace LuaTeX's random trailer ID with a content-derived stable ID.

    LuaTeX's generated PDF is otherwise byte-identical across replays.  The
    replacement is fixed-width, so it does not invalidate the cross-reference
    offsets.  Hashing the zeroed-ID representation avoids circularity.
    """

    payload = path.read_bytes()
    matches = tuple(PDF_ID_PATTERN.finditer(payload))
    if len(matches) != 1:
        raise RuntimeError(f"expected one PDF trailer ID, found {len(matches)}")
    zeroed = PDF_ID_PATTERN.sub(
        b"/ID [ <00000000000000000000000000000000> <00000000000000000000000000000000> ]",
        payload,
    )
    stable_id = hashlib.sha256(zeroed).hexdigest()[:32].encode("ascii")
    normalized = PDF_ID_PATTERN.sub(
        b"/ID [ <" + stable_id + b"> <" + stable_id + b"> ]",
        payload,
    )
    if len(normalized) != len(payload):
        raise RuntimeError("PDF trailer-ID normalization changed the byte length")
    path.write_bytes(normalized)
    return stable_id.decode("ascii")


def tool_line(executable: str, *args: str) -> str:
    process = subprocess.run(
        [executable, *args],
        cwd=LANE,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return process.stdout.splitlines()[0]


def run_logged(log: Path, executable: str, *args: str) -> None:
    environment = os.environ.copy()
    environment["SOURCE_DATE_EPOCH"] = SOURCE_DATE_EPOCH
    process = subprocess.run(
        [executable, *args],
        cwd=LANE,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    log.write_text(process.stdout, encoding="utf-8", newline="\n")
    if process.returncode:
        raise RuntimeError(f"build command failed ({process.returncode}); see {log}")


def scope(through: int) -> tuple[tuple[Path, ...], str, str, str]:
    if not 1 <= through <= 30:
        raise ValueError("--through must be between 1 and 30")
    frontmatter = (
        SOURCE_DIR / "frontmatter-bgk-units-01.md"
        if through == 1
        else SOURCE_DIR / f"frontmatter-bgk-units-01-{through:02d}.md"
    )
    paths: list[Path] = [frontmatter]
    for unit in range(1, through + 1):
        paths.extend(
            (
                SOURCE_DIR / f"lecture-{unit:02d}.md",
                SOURCE_DIR / f"worksheet-{unit:02d}.md",
                SOURCE_DIR / f"worksheet-{unit:02d}-solutions.md",
                SOURCE_ROOT / f"media-credits-bgk-unit-{unit:02d}.md",
            )
        )
    title = f"Bundel, Berkas, dan Kohomologi - Unit 1-{through}"
    if through == 1:
        title = "Bundel, Berkas, dan Kohomologi - Unit 1"
    subtitle = "Edisi Bahasa Indonesia independen"
    pdf_name = (
        "bundel-berkas-dan-kohomologi-id-unit-01.pdf"
        if through == 1
        else f"bundel-berkas-dan-kohomologi-id-units-01-{through:02d}.pdf"
    )
    return tuple(paths), title, subtitle, pdf_name


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--through", type=int, default=1)
    args = parser.parse_args()
    sources, title, subtitle, pdf_name = scope(args.through)
    fixed_inputs, pdf_asset_replacements = cumulative_inputs(args.through)
    for path in (*sources, *fixed_inputs):
        regular(path)

    pandoc = shutil.which("pandoc")
    lualatex = shutil.which("lualatex")
    if not pandoc or not lualatex:
        raise RuntimeError("pandoc and lualatex must both be available on PATH")
    pandoc_version = tool_line(pandoc, "--version")
    if pandoc_version != EXPECTED_PANDOC:
        raise RuntimeError(
            f"unexpected Pandoc version: {pandoc_version!r}; expected {EXPECTED_PANDOC!r}"
        )
    latex_version = tool_line(lualatex, "--version")

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".reader-bgk-id-stage-", dir=BUILD_DIR))
    try:
        html_path = stage / "index.html"
        pdf_path = stage / pdf_name
        resource_path = os.pathsep.join(
            (str(stage), str(SOURCE_DIR), str(SOURCE_ROOT), str(ASSET_DIR), str(LANE))
        )
        common = [
            "--from=markdown+yaml_metadata_block+tex_math_dollars+fenced_divs+bracketed_spans",
            "--standalone",
            "--toc",
            "--metadata=lang:id-ID",
            f"--metadata=title:{title}",
            f"--metadata=subtitle:{subtitle}",
            "--metadata=author:Holger Brenner (karya sumber)",
            f"--resource-path={resource_path}",
            *(str(path) for path in sources),
        ]
        run_logged(
            stage / "pandoc-html.log",
            pandoc,
            *common,
            "--to=html5",
            "--mathml",
            "--embed-resources",
            f"--css={CSS}",
            f"--output={html_path}",
        )
        add_html_landmarks(html_path)

        pdf_sources: list[Path] = []
        for source in sources:
            staged = stage / f"pdf-{source.name}"
            text = source.read_text(encoding="utf-8")
            text = text.replace("★", r"\sourceblackstar{}")
            text = text.replace("κ", r"$\kappa$")
            text = text.replace(r"\vcentcolon=", r":=")
            text = re.sub(
                # The opening delimiter must not itself be the closing backtick
                # of a preceding short code span (for example `PD`, followed
                # later by `{{PD-self}}`).
                r"(?<![\w}\]])`([^`\n]{40,})`",
                lambda match: r"\nolinkurl{" + match.group(1) + "}",
                text,
            )
            text = text.replace(
                "](authority/assets/bgk-tangent-bundle-500.png)",
                "](authority/assets/bgk-tangent-bundle-500.png){height=70%}",
            )
            for animated_path, fallback_path in pdf_asset_replacements.items():
                text = text.replace(animated_path, fallback_path)
            staged.write_text(text, encoding="utf-8", newline="\n")
            pdf_sources.append(staged)

        pdf_common = [
            "--from=markdown+yaml_metadata_block+tex_math_dollars+fenced_divs+bracketed_spans",
            "--standalone",
            "--toc",
            "--metadata=lang:id-ID",
            f"--metadata=title:{title}",
            f"--metadata=subtitle:{subtitle}",
            "--metadata=author:Holger Brenner (karya sumber)",
            f"--resource-path={resource_path}",
            f"--include-in-header={PDF_HEADER}",
            *(str(path) for path in pdf_sources),
        ]
        run_logged(
            stage / "pandoc-pdf.log",
            pandoc,
            *pdf_common,
            f"--pdf-engine={lualatex}",
            "--variable=papersize:a4",
            "--variable=geometry:margin=25mm",
            "--variable=colorlinks:true",
            f"--output={pdf_path}",
        )
        normalized_pdf_id = normalize_pdf_id(pdf_path)
        regular(html_path)
        regular(pdf_path)
        if html_path.stat().st_size < 10_000 or pdf_path.stat().st_size < 10_000:
            raise RuntimeError("BGK reader artifact is implausibly small")

        receipt = {
            "schema": "ag-bridge-bgk-build-receipt-v1",
            "built_utc": datetime.fromtimestamp(
                int(SOURCE_DATE_EPOCH), timezone.utc
            ).isoformat(),
            "source_date_epoch": SOURCE_DATE_EPOCH,
            "language": "id-ID",
            "volume": "Bündel, Garben und Kohomologie",
            "through_unit": args.through,
            "title": title,
            "pandoc": pandoc_version,
            "latex": latex_version,
            "normalized_pdf_trailer_id": normalized_pdf_id,
            "html_main_landmark": "main#main-content",
            "html_skip_link": "a.skip-link[href='#main-content']",
            "inputs": [fact(path) for path in (*sources, *fixed_inputs)],
            "outputs": [
                {
                    "path": "build/reader-bgk-id/index.html",
                    "bytes": html_path.stat().st_size,
                    "sha256": sha256(html_path),
                },
                {
                    "path": f"build/reader-bgk-id/{pdf_name}",
                    "bytes": pdf_path.stat().st_size,
                    "sha256": sha256(pdf_path),
                },
            ],
        }
        (stage / "BUILD_RECEIPT.json").write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )

        previous = BUILD_DIR / ".reader-bgk-id-previous"
        if previous.exists():
            shutil.rmtree(previous)
        if FINAL_DIR.exists():
            FINAL_DIR.replace(previous)
        stage.replace(FINAL_DIR)
        if previous.exists():
            shutil.rmtree(previous)
    except Exception as error:
        raise RuntimeError(f"{error}; failed stage retained at {stage}") from error

    print(FINAL_DIR)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
