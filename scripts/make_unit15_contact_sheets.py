#!/usr/bin/env python3
"""Create bounded contact sheets for visual review of all Units 1-15 pages."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
RENDER_DIR = ROOT / "tmp" / "pdfs" / "unit-15-release-render"
OUTPUT_DIR = ROOT / "tmp" / "pdfs" / "unit-15-release-contact"
PAGES_PER_SHEET = 20
COLUMNS = 5
THUMB_WIDTH = 240
LABEL_HEIGHT = 30
GAP = 10


def main() -> int:
    pages = sorted(RENDER_DIR.glob("page-*.png"))
    if len(pages) != 267:
        raise RuntimeError(f"expected 267 pages, found {len(pages)}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default(size=18)
    with Image.open(pages[0]) as sample:
        thumb_height = round(sample.height * THUMB_WIDTH / sample.width)
    rows = (PAGES_PER_SHEET + COLUMNS - 1) // COLUMNS
    sheet_width = GAP + COLUMNS * (THUMB_WIDTH + GAP)
    sheet_height = GAP + rows * (LABEL_HEIGHT + thumb_height + GAP)

    outputs = []
    for start in range(0, len(pages), PAGES_PER_SHEET):
        batch = pages[start : start + PAGES_PER_SHEET]
        sheet = Image.new("RGB", (sheet_width, sheet_height), "#d8d8d8")
        draw = ImageDraw.Draw(sheet)
        for offset, path in enumerate(batch):
            page_number = start + offset + 1
            row, column = divmod(offset, COLUMNS)
            left = GAP + column * (THUMB_WIDTH + GAP)
            top = GAP + row * (LABEL_HEIGHT + thumb_height + GAP)
            draw.rectangle((left, top, left + THUMB_WIDTH, top + LABEL_HEIGHT), fill="white")
            draw.text((left + 6, top + 5), f"Halaman {page_number}", fill="black", font=font)
            with Image.open(path) as page:
                thumb = page.convert("RGB").resize((THUMB_WIDTH, thumb_height), Image.Resampling.LANCZOS)
            sheet.paste(thumb, (left, top + LABEL_HEIGHT))
        end = start + len(batch)
        output = OUTPUT_DIR / f"pages-{start + 1:03d}-{end:03d}.png"
        sheet.save(output, format="PNG", optimize=True)
        outputs.append(output)
    print("\n".join(path.as_posix() for path in outputs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
