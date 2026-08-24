#!/usr/bin/env python3
"""Fail-closed cumulative reader QA through Unit 8."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "qa_reader_units_01_07.py"
outer = TEMPLATE.read_text(encoding="utf-8")
marker = 'exec(compile(source, str(Path(__file__).resolve()), "exec"), globals())'
if outer.count(marker) != 1:
    raise SystemExit("Unit 7 reader-QA template final exec marker drift")

post = r'''

# Extend the already audited Unit 7 generated checker at the next contiguous
# boundary.  Every replacement is fail-closed so template drift cannot
# silently change the audited scope.
def _replace(old: str, new: str, expected: int = 1) -> None:
    global source
    count = source.count(old)
    if count != expected:
        raise SystemExit(f"Unit 8 reader-QA template drift for {old!r}: expected {expected}, found {count}")
    source = source.replace(old, new)


_replace("through Unit 7.", "through Unit 8.")
_replace("algebraic-geometry-bridge-id-units-01-07.pdf", "algebraic-geometry-bridge-id-units-01-08.pdf")
_replace("UNITS_01_07_MACHINE_QA.json", "UNITS_01_08_MACHINE_QA.json")
_replace("EXPECTED_PDF_PAGES = 142", "EXPECTED_PDF_PAGES = 161")
_replace("frontmatter-units-01-07.md", "frontmatter-units-01-08.md")
_replace(
    "    SOURCE / \"media-credits-unit-07.md\",\n)",
    "    SOURCE / \"media-credits-unit-07.md\",\n"
    "    SOURCE / \"lecture-08.md\",\n"
    "    SOURCE / \"worksheet-08.md\",\n"
    "    SOURCE / \"worksheet-08-solutions.md\",\n"
    "    SOURCE / \"media-credits-unit-08.md\",\n)",
)
_replace(
    "        SOURCE / \"worksheet-07-solutions.md\": {\"math\": 61, \"images\": 0, \"solutions\": 3, \"headers\": 4},\n",
    "        SOURCE / \"worksheet-07-solutions.md\": {\"math\": 61, \"images\": 0, \"solutions\": 3, \"headers\": 4},\n"
    "        SOURCE / \"lecture-08.md\": {\"math\": 199, \"images\": 6, \"headers\": 11},\n"
    "        SOURCE / \"worksheet-08.md\": {\"math\": 100, \"images\": 0, \"exercises\": 24, \"headers\": 28},\n"
    "        SOURCE / \"worksheet-08-solutions.md\": {\"math\": 43, \"images\": 0, \"solutions\": 2, \"headers\": 3},\n",
)

authority = "\n".join(
    [
        "def verify_unit8_authority() -> dict:",
        '    path = ROOT / "authority" / "wikiversity" / "unit-08" / "UNIT_AUTHORITY_MANIFEST.json"',
        '    manifest = json.loads(path.read_text(encoding="utf-8"))',
        '    base.require(manifest["unit_number"] == 8, "Unit 8 manifest unit")',
        '    base.require(manifest["lecture"]["revid"] == 1051293, "Unit 8 lecture revision")',
        '    base.require(manifest["worksheet"]["revid"] == 1057977, "Unit 8 worksheet revision")',
        '    base.require(manifest["lecture_transclusion_closure"]["requested_template_count"] == 73, "Unit 8 lecture template count")',
        '    base.require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 73, "Unit 8 lecture captured transclusions")',
        '    base.require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "Unit 8 lecture missing transclusion")',
        '    base.require(manifest["worksheet_transclusion_closure"]["requested_template_count"] == 103, "Unit 8 worksheet template count")',
        '    base.require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 103, "Unit 8 worksheet captured transclusions")',
        '    base.require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "Unit 8 worksheet missing transclusion")',
        '    for row in manifest["files"]:',
        '        witness = path.parent / row["file"]',
        '        base.require(',
        '            witness.stat().st_size == row["bytes"] and base.digest(witness) == row["sha256"],',
        '            f"Unit 8 authority replay {row[\'file\']}",',
        '        )',
        '    pdf_pages = []',
        '    for row in manifest["official_pdf_witnesses"]:',
        '        witness = ROOT / row["local_path"]',
        '        base.require(',
        '            witness.stat().st_size == row["local_bytes"] and base.digest(witness) == row["local_sha256"],',
        '            f"Unit 8 official PDF replay {witness.name}",',
        '        )',
        '        pdf_pages.append(len(PdfReader(witness).pages))',
        '    base.require(sorted(pdf_pages) == [7, 11], "Unit 8 official PDF page closure")',
        '    base.require(',
        '        base.digest(path) == "f9089c78e81511bdbc24dc62d7c506a77c266426ea73b3e390f20ec30dabb40f",',
        '        "Unit 8 authority manifest identity",',
        '    )',
        '    return {',
        '        "manifest_sha256": base.digest(path),',
        '        "file_count": len(manifest["files"]),',
        '        "lecture_revid": 1051293,',
        '        "worksheet_revid": 1057977,',
        '        "official_pdf_pages": pdf_pages,',
        '    }',
        "",
        "",
    ]
)
_replace("def main() -> int:\n", authority + "def main() -> int:\n")
_replace('combined.count("**Catatan edisi:**") == 11', 'combined.count("**Catatan edisi:**") == 12')
_replace(
    '    base.require("dahulu disalahidentifikasi sebagai Johannes Kepler" in combined, "Unit 7 portrait correction")',
    '    base.require("dahulu disalahidentifikasi sebagai Johannes Kepler" in combined, "Unit 7 portrait correction")\n'
    '    base.require("argumen ini tidak sepenuhnya benar" in combined, "Unit 8 source proof-gap disclosure")\n'
    '    base.require("|x_1|\\\\le d\\\\sqrt{1+e^2}" in combined, "Unit 8 exact reachable-bound note")',
)
_replace(
    '    css_text = CSS.read_text(encoding="utf-8")',
    '    for marker in ("AGC-CORR-0020", "AGC-CORR-0021", "AGC-ADAPT-0017", "AGC-ADAPT-0018", "AGC-ADAPT-0019", "AGC-ADAPT-0020"):\n'
    '        base.require(marker in corrections, f"Unit 8 delta ledger marker {marker}")\n\n'
    '    css_text = CSS.read_text(encoding="utf-8")',
)
_replace("len(ids) == len(set(ids)) == 388", "len(ids) == len(set(ids)) == 431")
_replace(
    '        "unit_07": base.verify_solution_map(7, SOURCE / "worksheet-07-solutions.md", 33, 3),\n',
    '        "unit_07": base.verify_solution_map(7, SOURCE / "worksheet-07-solutions.md", 33, 3),\n'
    '        "unit_08": base.verify_solution_map(8, SOURCE / "worksheet-08-solutions.md", 24, 2),\n',
)
_replace(
    '        "unit_07": base.verify_rights("RIGHTS-unit-07.csv", "ASSET_CLOSURE-unit-07.json", 9, 13),\n',
    '        "unit_07": base.verify_rights("RIGHTS-unit-07.csv", "ASSET_CLOSURE-unit-07.json", 9, 13),\n'
    '        "unit_08": base.verify_rights("RIGHTS-unit-08.csv", "ASSET_CLOSURE-unit-08.json", 6, 8),\n',
)
_replace(
    '        "unit_07": verify_unit7_authority(),\n',
    '        "unit_07": verify_unit7_authority(),\n'
    '        "unit_08": verify_unit8_authority(),\n',
)
_replace('"Kurva Aljabar - Unit 1-7"', '"Kurva Aljabar - Unit 1-8"', expected=2)
_replace("len(images) == 53", "len(images) == 59")
_replace("== 2580", "== 2922")
_replace(
    '        "Kredit media Unit 7",\n',
    '        "Kredit media Unit 7",\n'
    '        "Kuliah 8: Kurva Aljabar yang Didefinisikan Secara Mekanis",\n'
    '        "Soal 8.24 - 3 poin",\n'
    '        "Solusi Soal 8.17",\n'
    '        "Kredit media Unit 8",\n',
    expected=2,
)
_replace(
    'for alt in ("Orbit eliptik", "Orbit parabola", "Orbit hiperbola"):',
    'for alt in ("Orbit eliptik", "Orbit parabola", "Orbit hiperbola", "Gedung berbentuk lemniskata", "Mesin uap sedang bekerja"):',
)
_replace('receipt["through_unit"] == 7', 'receipt["through_unit"] == 8')
_replace('"through_unit": 7', '"through_unit": 8')
_replace(
    '"unit3_through_unit7_authority_and_official_pdf_hash_replay"',
    '"unit3_through_unit8_authority_and_official_pdf_hash_replay"',
)

required_unit8_markers = [
    'SOURCE / "lecture-08.md"',
    'SOURCE / "worksheet-08-solutions.md"',
    '"unit_08": base.verify_solution_map(8',
    '"unit_08": base.verify_rights("RIGHTS-unit-08.csv"',
    '"unit_08": verify_unit8_authority()',
    'EXPECTED_PDF_PAGES = 161',
    'len(images) == 59',
    '== 2922',
]
missing = [marker for marker in required_unit8_markers if marker not in source]
if missing:
    raise SystemExit(f"Transformed Unit 8 reader-QA markers absent: {missing}")
'''
outer = outer.replace(marker, post + "\n" + marker, 1)
exec(compile(outer, str(Path(__file__).resolve()), "exec"), globals())
