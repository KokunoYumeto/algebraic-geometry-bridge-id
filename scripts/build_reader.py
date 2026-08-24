#!/usr/bin/env python3
"""Build the bounded Indonesian Algebraic Geometry Bridge reader.

The authored source remains Markdown.  Pandoc emits a self-contained HTML
reader with MathML and an A4 PDF through LuaLaTeX.  The build is staged and
published only after both artifacts and their manifest are complete.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone


LANE = Path(__file__).resolve().parents[1]
SOURCE_DIR = LANE / "source" / "id-ID"
ASSET_DIR = LANE / "authority" / "assets"
BUILD_DIR = LANE / "build"
FINAL_DIR = BUILD_DIR / "reader-id"
CSS = SOURCE_DIR / "reader.css"
PDF_HEADER = SOURCE_DIR / "pdf-header.tex"
EXPECTED_PANDOC_PREFIX = "pandoc 3.9.0.2"
PDF_ASSET_REPLACEMENTS = {
    "authority/assets/RationalDegree2byXedi.gif":
        "authority/assets/RationalDegree2byXedi-frame-1.png",
    "authority/assets/Ellipse.svg":
        "authority/assets/Ellipse-250.png",
    "authority/assets/Newtonbig.gif":
        "authority/assets/Newtonbig-frame-1.png",
    "authority/assets/Conjuntos_algebraicos_2.svg":
        "authority/assets/Conjuntos_algebraicos_2-500.png",
    "authority/assets/Gerade.svg":
        "authority/assets/Gerade-500.png",
    "authority/assets/Straight_lines.svg":
        "authority/assets/Straight_lines-500.png",
    "authority/assets/Kuzel_obecny.svg":
        "authority/assets/Kuzel_obecny-500.png",
    "authority/assets/Cubic_with_double_point.svg":
        "authority/assets/Cubic_with_double_point-500.png",
    "authority/assets/Conic_sections.svg":
        "authority/assets/Conic_sections-500.png",
    "authority/assets/Elliptic_orbit.gif":
        "authority/assets/Elliptic_orbit-frame-1.png",
    "authority/assets/Parabolic_orbit.gif":
        "authority/assets/Parabolic_orbit-frame-1.png",
    "authority/assets/Hyperbolic_orbit.gif":
        "authority/assets/Hyperbolic_orbit-frame-1.png",
    "authority/assets/Lemniscate_Building.gif":
        "authority/assets/Lemniscate_Building-frame-1.png",
    "authority/assets/Steam_engine_in_action.gif":
        "authority/assets/Steam_engine_in_action-frame-1.png",
    "authority/assets/Hyperbola_one_over_x.svg":
        "authority/assets/Hyperbola_one_over_x-500.png",
    "authority/assets/Connected_and_disconnected_spaces2.svg":
        "authority/assets/Connected_and_disconnected_spaces2-500.png",
    "authority/assets/Concentric_Circles.svg":
        "authority/assets/Concentric_Circles-500.png",
}


def build_scope(through: int) -> tuple[tuple[Path, ...], str, str, str]:
    if through == 1:
        return (
            (
                SOURCE_DIR / "frontmatter.md",
                SOURCE_DIR / "lecture-01.md",
                SOURCE_DIR / "worksheet-01.md",
                SOURCE_DIR / "worksheet-01-solutions.md",
                SOURCE_DIR / "media-credits.md",
            ),
            "Kurva Aljabar — Unit 1",
            "Kuliah dan lembar kerja pertama, edisi Bahasa Indonesia",
            "algebraic-geometry-bridge-id-unit-01.pdf",
        )
    if through == 2:
        return (
            (
                SOURCE_DIR / "frontmatter-units-01-02.md",
                SOURCE_DIR / "lecture-01.md",
                SOURCE_DIR / "worksheet-01.md",
                SOURCE_DIR / "worksheet-01-solutions.md",
                SOURCE_DIR / "lecture-02.md",
                SOURCE_DIR / "worksheet-02.md",
                SOURCE_DIR / "worksheet-02-solutions.md",
                SOURCE_DIR / "media-credits.md",
                SOURCE_DIR / "media-credits-unit-02.md",
            ),
            "Kurva Aljabar — Unit 1–2",
            "Dua kuliah dan lembar kerja pertama, edisi Bahasa Indonesia",
            "algebraic-geometry-bridge-id-units-01-02.pdf",
        )
    if through == 3:
        return (
            (
                SOURCE_DIR / "frontmatter-units-01-03.md",
                SOURCE_DIR / "lecture-01.md",
                SOURCE_DIR / "worksheet-01.md",
                SOURCE_DIR / "worksheet-01-solutions.md",
                SOURCE_DIR / "lecture-02.md",
                SOURCE_DIR / "worksheet-02.md",
                SOURCE_DIR / "worksheet-02-solutions.md",
                SOURCE_DIR / "lecture-03.md",
                SOURCE_DIR / "worksheet-03.md",
                SOURCE_DIR / "worksheet-03-solutions.md",
                SOURCE_DIR / "media-credits.md",
                SOURCE_DIR / "media-credits-unit-02.md",
                SOURCE_DIR / "media-credits-unit-03.md",
            ),
            "Kurva Aljabar — Unit 1–3",
            "Tiga kuliah dan lembar kerja pertama, edisi Bahasa Indonesia",
            "algebraic-geometry-bridge-id-units-01-03.pdf",
        )
    if through == 4:
        return (
            (
                SOURCE_DIR / "frontmatter-units-01-04.md",
                SOURCE_DIR / "lecture-01.md",
                SOURCE_DIR / "worksheet-01.md",
                SOURCE_DIR / "worksheet-01-solutions.md",
                SOURCE_DIR / "lecture-02.md",
                SOURCE_DIR / "worksheet-02.md",
                SOURCE_DIR / "worksheet-02-solutions.md",
                SOURCE_DIR / "lecture-03.md",
                SOURCE_DIR / "worksheet-03.md",
                SOURCE_DIR / "worksheet-03-solutions.md",
                SOURCE_DIR / "lecture-04.md",
                SOURCE_DIR / "worksheet-04.md",
                SOURCE_DIR / "worksheet-04-solutions.md",
                SOURCE_DIR / "media-credits.md",
                SOURCE_DIR / "media-credits-unit-02.md",
                SOURCE_DIR / "media-credits-unit-03.md",
                SOURCE_DIR / "media-credits-unit-04.md",
            ),
            "Kurva Aljabar - Unit 1-4",
            "Empat kuliah dan lembar kerja pertama, edisi Bahasa Indonesia",
            "algebraic-geometry-bridge-id-units-01-04.pdf",
        )
    if through == 5:
        return (
            (
                SOURCE_DIR / "frontmatter-units-01-05.md",
                SOURCE_DIR / "lecture-01.md",
                SOURCE_DIR / "worksheet-01.md",
                SOURCE_DIR / "worksheet-01-solutions.md",
                SOURCE_DIR / "lecture-02.md",
                SOURCE_DIR / "worksheet-02.md",
                SOURCE_DIR / "worksheet-02-solutions.md",
                SOURCE_DIR / "lecture-03.md",
                SOURCE_DIR / "worksheet-03.md",
                SOURCE_DIR / "worksheet-03-solutions.md",
                SOURCE_DIR / "lecture-04.md",
                SOURCE_DIR / "worksheet-04.md",
                SOURCE_DIR / "worksheet-04-solutions.md",
                SOURCE_DIR / "lecture-05.md",
                SOURCE_DIR / "worksheet-05.md",
                SOURCE_DIR / "worksheet-05-solutions.md",
                SOURCE_DIR / "media-credits.md",
                SOURCE_DIR / "media-credits-unit-02.md",
                SOURCE_DIR / "media-credits-unit-03.md",
                SOURCE_DIR / "media-credits-unit-04.md",
                SOURCE_DIR / "media-credits-unit-05.md",
            ),
            "Kurva Aljabar - Unit 1-5",
            "Lima kuliah dan lembar kerja pertama, edisi Bahasa Indonesia",
            "algebraic-geometry-bridge-id-units-01-05.pdf",
        )
    if through == 6:
        return (
            (
                SOURCE_DIR / "frontmatter-units-01-06.md",
                SOURCE_DIR / "lecture-01.md",
                SOURCE_DIR / "worksheet-01.md",
                SOURCE_DIR / "worksheet-01-solutions.md",
                SOURCE_DIR / "lecture-02.md",
                SOURCE_DIR / "worksheet-02.md",
                SOURCE_DIR / "worksheet-02-solutions.md",
                SOURCE_DIR / "lecture-03.md",
                SOURCE_DIR / "worksheet-03.md",
                SOURCE_DIR / "worksheet-03-solutions.md",
                SOURCE_DIR / "lecture-04.md",
                SOURCE_DIR / "worksheet-04.md",
                SOURCE_DIR / "worksheet-04-solutions.md",
                SOURCE_DIR / "lecture-05.md",
                SOURCE_DIR / "worksheet-05.md",
                SOURCE_DIR / "worksheet-05-solutions.md",
                SOURCE_DIR / "lecture-06.md",
                SOURCE_DIR / "worksheet-06.md",
                SOURCE_DIR / "worksheet-06-solutions.md",
                SOURCE_DIR / "media-credits.md",
                SOURCE_DIR / "media-credits-unit-02.md",
                SOURCE_DIR / "media-credits-unit-03.md",
                SOURCE_DIR / "media-credits-unit-04.md",
                SOURCE_DIR / "media-credits-unit-05.md",
                SOURCE_DIR / "media-credits-unit-06.md",
            ),
            "Kurva Aljabar - Unit 1-6",
            "Enam kuliah dan lembar kerja pertama, edisi Bahasa Indonesia",
            "algebraic-geometry-bridge-id-units-01-06.pdf",
        )
    if through == 7:
        return (
            (
                SOURCE_DIR / "frontmatter-units-01-07.md",
                SOURCE_DIR / "lecture-01.md",
                SOURCE_DIR / "worksheet-01.md",
                SOURCE_DIR / "worksheet-01-solutions.md",
                SOURCE_DIR / "lecture-02.md",
                SOURCE_DIR / "worksheet-02.md",
                SOURCE_DIR / "worksheet-02-solutions.md",
                SOURCE_DIR / "lecture-03.md",
                SOURCE_DIR / "worksheet-03.md",
                SOURCE_DIR / "worksheet-03-solutions.md",
                SOURCE_DIR / "lecture-04.md",
                SOURCE_DIR / "worksheet-04.md",
                SOURCE_DIR / "worksheet-04-solutions.md",
                SOURCE_DIR / "lecture-05.md",
                SOURCE_DIR / "worksheet-05.md",
                SOURCE_DIR / "worksheet-05-solutions.md",
                SOURCE_DIR / "lecture-06.md",
                SOURCE_DIR / "worksheet-06.md",
                SOURCE_DIR / "worksheet-06-solutions.md",
                SOURCE_DIR / "lecture-07.md",
                SOURCE_DIR / "worksheet-07.md",
                SOURCE_DIR / "worksheet-07-solutions.md",
                SOURCE_DIR / "media-credits.md",
                SOURCE_DIR / "media-credits-unit-02.md",
                SOURCE_DIR / "media-credits-unit-03.md",
                SOURCE_DIR / "media-credits-unit-04.md",
                SOURCE_DIR / "media-credits-unit-05.md",
                SOURCE_DIR / "media-credits-unit-06.md",
                SOURCE_DIR / "media-credits-unit-07.md",
            ),
            "Kurva Aljabar - Unit 1-7",
            "Tujuh kuliah dan lembar kerja pertama, edisi Bahasa Indonesia",
            "algebraic-geometry-bridge-id-units-01-07.pdf",
        )
    if through == 8:
        return (
            (
                SOURCE_DIR / "frontmatter-units-01-08.md",
                SOURCE_DIR / "lecture-01.md",
                SOURCE_DIR / "worksheet-01.md",
                SOURCE_DIR / "worksheet-01-solutions.md",
                SOURCE_DIR / "lecture-02.md",
                SOURCE_DIR / "worksheet-02.md",
                SOURCE_DIR / "worksheet-02-solutions.md",
                SOURCE_DIR / "lecture-03.md",
                SOURCE_DIR / "worksheet-03.md",
                SOURCE_DIR / "worksheet-03-solutions.md",
                SOURCE_DIR / "lecture-04.md",
                SOURCE_DIR / "worksheet-04.md",
                SOURCE_DIR / "worksheet-04-solutions.md",
                SOURCE_DIR / "lecture-05.md",
                SOURCE_DIR / "worksheet-05.md",
                SOURCE_DIR / "worksheet-05-solutions.md",
                SOURCE_DIR / "lecture-06.md",
                SOURCE_DIR / "worksheet-06.md",
                SOURCE_DIR / "worksheet-06-solutions.md",
                SOURCE_DIR / "lecture-07.md",
                SOURCE_DIR / "worksheet-07.md",
                SOURCE_DIR / "worksheet-07-solutions.md",
                SOURCE_DIR / "lecture-08.md",
                SOURCE_DIR / "worksheet-08.md",
                SOURCE_DIR / "worksheet-08-solutions.md",
                SOURCE_DIR / "media-credits.md",
                SOURCE_DIR / "media-credits-unit-02.md",
                SOURCE_DIR / "media-credits-unit-03.md",
                SOURCE_DIR / "media-credits-unit-04.md",
                SOURCE_DIR / "media-credits-unit-05.md",
                SOURCE_DIR / "media-credits-unit-06.md",
                SOURCE_DIR / "media-credits-unit-07.md",
                SOURCE_DIR / "media-credits-unit-08.md",
            ),
            "Kurva Aljabar - Unit 1-8",
            "Delapan kuliah dan lembar kerja pertama, edisi Bahasa Indonesia",
            "algebraic-geometry-bridge-id-units-01-08.pdf",
        )
    if through == 9:
        return (
            (
                SOURCE_DIR / "frontmatter-units-01-09.md",
                SOURCE_DIR / "lecture-01.md",
                SOURCE_DIR / "worksheet-01.md",
                SOURCE_DIR / "worksheet-01-solutions.md",
                SOURCE_DIR / "lecture-02.md",
                SOURCE_DIR / "worksheet-02.md",
                SOURCE_DIR / "worksheet-02-solutions.md",
                SOURCE_DIR / "lecture-03.md",
                SOURCE_DIR / "worksheet-03.md",
                SOURCE_DIR / "worksheet-03-solutions.md",
                SOURCE_DIR / "lecture-04.md",
                SOURCE_DIR / "worksheet-04.md",
                SOURCE_DIR / "worksheet-04-solutions.md",
                SOURCE_DIR / "lecture-05.md",
                SOURCE_DIR / "worksheet-05.md",
                SOURCE_DIR / "worksheet-05-solutions.md",
                SOURCE_DIR / "lecture-06.md",
                SOURCE_DIR / "worksheet-06.md",
                SOURCE_DIR / "worksheet-06-solutions.md",
                SOURCE_DIR / "lecture-07.md",
                SOURCE_DIR / "worksheet-07.md",
                SOURCE_DIR / "worksheet-07-solutions.md",
                SOURCE_DIR / "lecture-08.md",
                SOURCE_DIR / "worksheet-08.md",
                SOURCE_DIR / "worksheet-08-solutions.md",
                SOURCE_DIR / "lecture-09.md",
                SOURCE_DIR / "worksheet-09.md",
                SOURCE_DIR / "worksheet-09-solutions.md",
                SOURCE_DIR / "media-credits.md",
                SOURCE_DIR / "media-credits-unit-02.md",
                SOURCE_DIR / "media-credits-unit-03.md",
                SOURCE_DIR / "media-credits-unit-04.md",
                SOURCE_DIR / "media-credits-unit-05.md",
                SOURCE_DIR / "media-credits-unit-06.md",
                SOURCE_DIR / "media-credits-unit-07.md",
                SOURCE_DIR / "media-credits-unit-08.md",
                SOURCE_DIR / "media-credits-unit-09.md",
            ),
            "Kurva Aljabar - Unit 1-9",
            "Sembilan kuliah dan lembar kerja pertama, edisi Bahasa Indonesia",
            "algebraic-geometry-bridge-id-units-01-09.pdf",
        )
    if through in (10, 11, 12, 13, 14, 15):
        number_words = {
            10: "Sepuluh",
            11: "Sebelas",
            12: "Dua belas",
            13: "Tiga belas",
            14: "Empat belas",
            15: "Lima belas",
        }
        unit_sources: list[Path] = [
            SOURCE_DIR / f"frontmatter-units-01-{through:02d}.md"
        ]
        for unit in range(1, through + 1):
            unit_sources.extend(
                (
                    SOURCE_DIR / f"lecture-{unit:02d}.md",
                    SOURCE_DIR / f"worksheet-{unit:02d}.md",
                    SOURCE_DIR / f"worksheet-{unit:02d}-solutions.md",
                )
            )
        unit_sources.append(SOURCE_DIR / "media-credits.md")
        unit_sources.extend(
            SOURCE_DIR / f"media-credits-unit-{unit:02d}.md"
            for unit in (*range(2, 10), 11, 12, 13, 14, 15)
            if unit <= through
        )
        return (
            tuple(unit_sources),
            f"Kurva Aljabar - Unit 1-{through}",
            f"{number_words[through]} kuliah dan lembar kerja pertama, edisi Bahasa Indonesia",
            f"algebraic-geometry-bridge-id-units-01-{through:02d}.pdf",
        )
    raise ValueError("only contiguous scopes --through 1 through --through 15 are supported")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tool_output(executable: str, *args: str) -> str:
    proc = subprocess.run(
        [executable, *args],
        cwd=LANE,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return proc.stdout.strip()


def run_logged(log: Path, executable: str, *args: str) -> None:
    proc = subprocess.run(
        [executable, *args],
        cwd=LANE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    log.write_text(proc.stdout, encoding="utf-8", newline="\n")
    if proc.returncode:
        raise RuntimeError(f"build command failed ({proc.returncode}); see {log}")


def regular_file(path: Path) -> None:
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"required regular file is missing or linked: {path}")


def canonical_rows(paths: list[Path]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in sorted(paths, key=lambda p: p.relative_to(LANE).as_posix().casefold()):
        rows.append(
            {
                "path": path.relative_to(LANE).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    return rows


def projected_output_rows(paths: tuple[Path, ...]) -> list[dict[str, object]]:
    return [
        {
            "path": f"build/reader-id/{path.name}",
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in sorted(paths, key=lambda item: item.name.casefold())
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--through", type=int, default=2)
    args = parser.parse_args()
    sources, title, subtitle, pdf_name = build_scope(args.through)

    for path in (*sources, CSS, PDF_HEADER):
        regular_file(path)

    pandoc = shutil.which("pandoc")
    lualatex = shutil.which("lualatex")
    if not pandoc or not lualatex:
        raise RuntimeError("pandoc and lualatex must both be available on PATH")
    pandoc_version = tool_output(pandoc, "--version").splitlines()[0]
    if pandoc_version != EXPECTED_PANDOC_PREFIX:
        raise RuntimeError(
            f"unexpected Pandoc version: {pandoc_version!r}; expected {EXPECTED_PANDOC_PREFIX!r}"
        )
    latex_version = tool_output(lualatex, "--version").splitlines()[0]

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".reader-id-stage-", dir=BUILD_DIR))
    try:
        html = stage / "index.html"
        pdf = stage / pdf_name
        resource_path = os.pathsep.join((str(SOURCE_DIR), str(ASSET_DIR), str(LANE)))
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
            f"--output={html}",
        )
        pdf_sources: list[Path] = []
        for source in sources:
            pdf_source = stage / f"pdf-{source.name}"
            text = source.read_text(encoding="utf-8")
            for before, after in PDF_ASSET_REPLACEMENTS.items():
                text = text.replace(before, after)
            text = text.replace("★", r"\sourceblackstar{}")
            text = text.replace("κ", r"$\kappa$")
            # The Commons uploader name is Hebrew and the selected PDF font
            # cannot encode it.  Keep the exact attribution in HTML/source;
            # use a readable Latin transliteration only in the PDF-stage copy.
            text = text.replace("דוד שי", "David Shai")
            # Pandoc serializes the source's definition-equality relation as
            # \vcentcolon=; MiKTeX does not provide that macro by default.
            # Keep the mathematical relation unchanged in the reader source,
            # and use the portable TeX spelling only in the PDF-stage copy.
            text = text.replace(r"\vcentcolon=", r":=")
            text = text.replace(
                "](authority/assets/Hydrant_Insel_Krk_Kroatien-500.jpg)",
                "](authority/assets/Hydrant_Insel_Krk_Kroatien-500.jpg){height=72%}",
            )
            text = text.replace(
                "](authority/assets/Dioklova_kisoida.png)",
                "](authority/assets/Dioklova_kisoida.png){height=72%}",
            )
            pdf_source.write_text(text, encoding="utf-8", newline="\n")
            pdf_sources.append(pdf_source)
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
            f"--output={pdf}",
        )
        regular_file(html)
        regular_file(pdf)
        if html.stat().st_size < 10_000 or pdf.stat().st_size < 10_000:
            raise RuntimeError("reader artifact is implausibly small")

        input_paths = [*sources, CSS, PDF_HEADER]
        if ASSET_DIR.is_dir():
            input_paths.extend(path for path in ASSET_DIR.rglob("*") if path.is_file())
        receipt = {
            "schema": "ag-bridge-build-receipt-v2",
            "built_utc": datetime.now(timezone.utc).isoformat(),
            "language": "id-ID",
            "through_unit": args.through,
            "title": title,
            "pandoc": pandoc_version,
            "latex": latex_version,
            "inputs": canonical_rows(input_paths),
            "outputs": projected_output_rows((html, pdf)),
        }
        (stage / "BUILD_RECEIPT.json").write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )

        previous = BUILD_DIR / ".reader-id-previous"
        if previous.exists():
            shutil.rmtree(previous)
        if FINAL_DIR.exists():
            FINAL_DIR.replace(previous)
        stage.replace(FINAL_DIR)
        if previous.exists():
            shutil.rmtree(previous)
    except Exception as exc:
        # Preserve the bounded failed stage so the exact command output remains
        # diagnosable.  A later successful build replaces only FINAL_DIR.
        raise RuntimeError(f"{exc}; failed stage retained at {stage}") from exc

    print(FINAL_DIR)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
