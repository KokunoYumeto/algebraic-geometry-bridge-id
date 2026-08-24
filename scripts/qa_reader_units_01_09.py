#!/usr/bin/env python3
"""Fail-closed cumulative reader QA through Unit 9."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "qa_reader_units_01_08.py"
wrapper = TEMPLATE.read_text(encoding="utf-8")
marker = 'exec(compile(outer, str(Path(__file__).resolve()), "exec"), globals())'
if wrapper.count(marker) != 1:
    raise SystemExit("Unit 8 reader-QA wrapper final exec marker drift")

post = r'''

def _u9_replace(old: str, new: str, expected: int = 1) -> None:
    global outer
    count = outer.count(old)
    if count != expected:
        raise SystemExit(f"Unit 9 reader-QA template drift for {old!r}: expected {expected}, found {count}")
    outer = outer.replace(old, new)


_u9_replace("through Unit 8.", "through Unit 9.")
_u9_replace("algebraic-geometry-bridge-id-units-01-08.pdf", "algebraic-geometry-bridge-id-units-01-09.pdf")
_u9_replace("UNITS_01_08_MACHINE_QA.json", "UNITS_01_09_MACHINE_QA.json")
_u9_replace("EXPECTED_PDF_PAGES = 161", "EXPECTED_PDF_PAGES = 174", expected=2)
_u9_replace("frontmatter-units-01-08.md", "frontmatter-units-01-09.md")
_u9_replace(
    '    SOURCE / \\"media-credits-unit-08.md\\",\\n)',
    '    SOURCE / \\"media-credits-unit-08.md\\",\\n'
    '    SOURCE / \\"lecture-09.md\\",\\n'
    '    SOURCE / \\"worksheet-09.md\\",\\n'
    '    SOURCE / \\"worksheet-09-solutions.md\\",\\n'
    '    SOURCE / \\"media-credits-unit-09.md\\",\\n)',
)
_u9_replace(
    '        SOURCE / \\"worksheet-08-solutions.md\\": {\\"math\\": 43, \\"images\\": 0, \\"solutions\\": 2, \\"headers\\": 3},\\n',
    '        SOURCE / \\"worksheet-08-solutions.md\\": {\\"math\\": 43, \\"images\\": 0, \\"solutions\\": 2, \\"headers\\": 3},\\n'
    '        SOURCE / \\"lecture-09.md\\": {\\"math\\": 202, \\"images\\": 1, \\"headers\\": 30},\\n'
    '        SOURCE / \\"worksheet-09.md\\": {\\"math\\": 101, \\"images\\": 0, \\"exercises\\": 24, \\"headers\\": 27},\\n'
    '        SOURCE / \\"worksheet-09-solutions.md\\": {\\"math\\": 37, \\"images\\": 0, \\"solutions\\": 3, \\"headers\\": 4},\\n',
)

unit9_authority = "\n".join(
    [
        "def verify_unit9_authority() -> dict:",
        '    path = ROOT / "authority" / "wikiversity" / "unit-09" / "UNIT_AUTHORITY_MANIFEST.json"',
        '    manifest = json.loads(path.read_text(encoding="utf-8"))',
        '    base.require(manifest["unit_number"] == 9, "Unit 9 manifest unit")',
        '    base.require(manifest["lecture"]["revid"] == 1112241, "Unit 9 lecture revision")',
        '    base.require(manifest["worksheet"]["revid"] == 1059491, "Unit 9 worksheet revision")',
        '    base.require(manifest["lecture_transclusion_closure"]["requested_template_count"] == 113, "Unit 9 lecture template count")',
        '    base.require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 113, "Unit 9 lecture captured transclusions")',
        '    base.require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "Unit 9 lecture missing transclusion")',
        '    base.require(manifest["worksheet_transclusion_closure"]["requested_template_count"] == 109, "Unit 9 worksheet template count")',
        '    base.require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 109, "Unit 9 worksheet captured transclusions")',
        '    base.require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "Unit 9 worksheet missing transclusion")',
        '    for row in manifest["files"]:',
        '        witness = path.parent / row["file"]',
        '        base.require(witness.stat().st_size == row["bytes"] and base.digest(witness) == row["sha256"], f"Unit 9 authority replay {row[\'file\']}")',
        '    pdf_pages = []',
        '    for row in manifest["official_pdf_witnesses"]:',
        '        witness = ROOT / row["local_path"]',
        '        base.require(witness.stat().st_size == row["local_bytes"] and base.digest(witness) == row["local_sha256"], f"Unit 9 official PDF replay {witness.name}")',
        '        pdf_pages.append(len(PdfReader(witness).pages))',
        '    base.require(sorted(pdf_pages) == [5, 9], "Unit 9 official PDF page closure")',
        '    base.require(base.digest(path) == "7cf7a956dffe854da9d021e3c74615573b91b5701d7e3b78a8f5f1aa45bfbc29", "Unit 9 authority manifest identity")',
        '    return {"manifest_sha256": base.digest(path), "file_count": len(manifest["files"]), "lecture_revid": 1112241, "worksheet_revid": 1059491, "official_pdf_pages": pdf_pages}',
        "",
        "",
    ]
)
unit9_authority_literal = repr(unit9_authority)
_u9_replace(
    'authority + "def main() -> int:\\n"',
    unit9_authority_literal + ' + authority + "def main() -> int:\\n"',
    expected=1,
)
_u9_replace("len(ids) == len(set(ids)) == 431", "len(ids) == len(set(ids)) == 493")
_u9_replace(
    '        "unit_08": base.verify_solution_map(8, SOURCE / "worksheet-08-solutions.md", 24, 2),\\n',
    '        "unit_08": base.verify_solution_map(8, SOURCE / "worksheet-08-solutions.md", 24, 2),\\n'
    '        "unit_09": base.verify_solution_map(9, SOURCE / "worksheet-09-solutions.md", 24, 3),\\n',
)
_u9_replace(
    '        "unit_08": base.verify_rights("RIGHTS-unit-08.csv", "ASSET_CLOSURE-unit-08.json", 6, 8),\\n',
    '        "unit_08": base.verify_rights("RIGHTS-unit-08.csv", "ASSET_CLOSURE-unit-08.json", 6, 8),\\n'
    '        "unit_09": base.verify_rights("RIGHTS-unit-09.csv", "ASSET_CLOSURE-unit-09.json", 1, 1),\\n',
)
_u9_replace(
    '        "unit_08": verify_unit8_authority(),\\n',
    '        "unit_08": verify_unit8_authority(),\\n'
    '        "unit_09": verify_unit9_authority(),\\n',
)
_u9_replace('"Kurva Aljabar - Unit 1-8"', '"Kurva Aljabar - Unit 1-9"', expected=1)
_u9_replace("len(images) == 59", "len(images) == 60", expected=2)
_u9_replace("== 2922", "== 3262", expected=2)
_u9_replace(
    '        "Kredit media Unit 8",\\n',
    '        "Kredit media Unit 8",\\n'
    '        "Kuliah 9:",\\n'
    '        "Soal 9.24 (4 poin)",\\n'
    '        "Solusi Soal 9.18",\\n'
    '        "Kredit media Unit 9",\\n',
    expected=1,
)
_u9_replace('receipt["through_unit"] == 8', 'receipt["through_unit"] == 9')
_u9_replace('"through_unit": 8', '"through_unit": 9')
_u9_replace(
    '"unit3_through_unit8_authority_and_official_pdf_hash_replay"',
    '"unit3_through_unit9_authority_and_official_pdf_hash_replay"',
)

required_unit9_markers = [
    'lecture-09.md',
    'worksheet-09-solutions.md',
    '"unit_09": base.verify_solution_map(9',
    '"unit_09": base.verify_rights("RIGHTS-unit-09.csv"',
    '"unit_09": verify_unit9_authority()',
    'EXPECTED_PDF_PAGES = 174',
    'len(images) == 60',
    '== 3262',
]
missing = [item for item in required_unit9_markers if item not in outer]
if missing:
    raise SystemExit(f"Transformed Unit 9 reader-QA markers absent: {missing}")
'''

wrapper = wrapper.replace(marker, post + "\n" + marker, 1)
exec(compile(wrapper, str(Path(__file__).resolve()), "exec"), globals())
