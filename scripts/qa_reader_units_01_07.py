#!/usr/bin/env python3
"""Fail-closed structural, mathematical-surface, and artifact QA through Unit 7.

The audited Unit 6 checker remains the executable template.  This wrapper
specializes only the cumulative boundary and Unit 7 constants, so the verified
Units 1--6 checks are inherited rather than reimplemented.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "qa_reader_units_01_06.py"
source = TEMPLATE.read_text(encoding="utf-8")


def replace_exact(old: str, new: str, *, expected: int | None = None) -> None:
    global source
    count = source.count(old)
    if expected is not None and count != expected:
        raise SystemExit(f"Reader-QA template drift for {old!r}: expected {expected}, found {count}")
    if count == 0:
        raise SystemExit(f"Reader-QA template marker absent: {old!r}")
    source = source.replace(old, new)


replace_exact(
    '"""Fail-closed structural, mathematical-surface, and artifact QA through Unit 6."""',
    '"""Fail-closed structural, mathematical-surface, and artifact QA through Unit 7."""',
    expected=1,
)
replace_exact("import qa_reader_units_01_05 as previous", "import qa_reader_units_01_06 as previous", expected=1)
replace_exact("base = previous.prior", "base = previous.base", expected=1)
replace_exact("algebraic-geometry-bridge-id-units-01-06.pdf", "algebraic-geometry-bridge-id-units-01-07.pdf", expected=1)
replace_exact("UNITS_01_06_MACHINE_QA.json", "UNITS_01_07_MACHINE_QA.json", expected=1)
replace_exact("EXPECTED_PDF_PAGES = 117", "EXPECTED_PDF_PAGES = 142", expected=1)

replace_exact(
    '''    SOURCE / "worksheet-06-solutions.md",
    SOURCE / "media-credits.md",''',
    '''    SOURCE / "worksheet-06-solutions.md",
    SOURCE / "lecture-07.md",
    SOURCE / "worksheet-07.md",
    SOURCE / "worksheet-07-solutions.md",
    SOURCE / "media-credits.md",''',
    expected=1,
)
replace_exact(
    '''    SOURCE / "media-credits-unit-06.md",
)''',
    '''    SOURCE / "media-credits-unit-06.md",
    SOURCE / "media-credits-unit-07.md",
)''',
    expected=1,
)
replace_exact("frontmatter-units-01-06.md", "frontmatter-units-01-07.md", expected=1)

expected_block = '''EXPECTED = dict(previous.EXPECTED)
EXPECTED.update(
    {
        SOURCE / "lecture-07.md": {"math": 221, "images": 9, "headers": 13},
        SOURCE / "worksheet-07.md": {"math": 148, "images": 0, "exercises": 33, "headers": 36},
        SOURCE / "worksheet-07-solutions.md": {"math": 61, "images": 0, "solutions": 3, "headers": 4},
    }
)
'''
source, count = re.subn(
    r"EXPECTED = dict\(previous\.EXPECTED\)\nEXPECTED\.update\(\n    \{\n.*?\n    \}\n\)\n",
    expected_block,
    source,
    count=1,
    flags=re.DOTALL,
)
if count != 1:
    raise SystemExit("Reader-QA EXPECTED block drift")

authority_block = '''def verify_unit7_authority() -> dict:
    path = ROOT / "authority" / "wikiversity" / "unit-07" / "UNIT_AUTHORITY_MANIFEST.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    base.require(manifest["unit_number"] == 7, "Unit 7 manifest unit")
    base.require(manifest["lecture"]["revid"] == 1057689, "Unit 7 lecture revision")
    base.require(manifest["worksheet"]["revid"] == 1112363, "Unit 7 worksheet revision")
    base.require(manifest["lecture_transclusion_closure"]["requested_template_count"] == 78, "Unit 7 lecture template count")
    base.require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 78, "Unit 7 lecture captured transclusions")
    base.require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "Unit 7 lecture missing transclusion")
    base.require(manifest["worksheet_transclusion_closure"]["requested_template_count"] == 136, "Unit 7 worksheet template count")
    base.require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 136, "Unit 7 worksheet captured transclusions")
    base.require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "Unit 7 worksheet missing transclusion")
    for row in manifest["files"]:
        witness = path.parent / row["file"]
        base.require(
            witness.stat().st_size == row["bytes"] and base.digest(witness) == row["sha256"],
            f"Unit 7 authority replay {row['file']}",
        )
    pdf_pages = []
    for row in manifest["official_pdf_witnesses"]:
        witness = ROOT / row["local_path"]
        base.require(
            witness.stat().st_size == row["local_bytes"] and base.digest(witness) == row["local_sha256"],
            f"Unit 7 official PDF replay {witness.name}",
        )
        pdf_pages.append(len(PdfReader(witness).pages))
    base.require(sorted(pdf_pages) == [7, 13], "Unit 7 official PDF page closure")
    base.require(
        base.digest(path) == "6423629ff600ffcfc5067ea139eef01843ece1ce907dd4bda1bfdb12f49de96e",
        "Unit 7 authority manifest identity",
    )
    return {
        "manifest_sha256": base.digest(path),
        "file_count": len(manifest["files"]),
        "lecture_revid": 1057689,
        "worksheet_revid": 1112363,
        "official_pdf_pages": pdf_pages,
    }


'''
source, count = re.subn(
    r"def verify_unit6_authority\(\) -> dict:\n.*?\n\n(?=def main\(\) -> int:)",
    authority_block,
    source,
    count=1,
    flags=re.DOTALL,
)
if count != 1:
    raise SystemExit("Reader-QA authority block drift")

replace_exact('combined.count("**Catatan edisi:**") == 4', 'combined.count("**Catatan edisi:**") == 11', expected=1)
replace_exact(
    'visible = re.sub(r"^---\\n.*?\\n---$", "", visible, flags=re.S | re.M)',
    '''visible = re.sub(r"^---\\n.*?\\n---$", "", visible, flags=re.S | re.M)
    visible = re.sub(r"\\]\\([^)]*\\)", "]", visible)''',
    expected=1,
)
replace_exact(
    'base.require(re.search(r"github_pat_|ghp_[A-Za-z0-9]{20,}|ZENODO_ACCESS_TOKEN", combined) is None, "credential-shaped text")',
    '''base.require(re.search(r"github_pat_|ghp_[A-Za-z0-9]{20,}|ZENODO_ACCESS_TOKEN", combined) is None, "credential-shaped text")
    base.require(re.search(r"\\bmedan\\b", visible, flags=re.IGNORECASE) is None, "superseded field terminology remains")
    base.require("gelanggang hasil bagi" not in visible.casefold(), "superseded quotient-ring terminology remains")
    base.require("gelanggang faktor" in visible.casefold(), "migrated quotient-ring terminology absent")
    base.require("OpenAI Codex gpt-5.6-sol, Ultra." in combined, "exact model provenance absent")''',
    expected=1,
)
replace_exact(
    'base.require("Tidak ada\\nsolusi tambahan yang dibuat" in combined, "Unit 6 no-invented-solution notice")',
    '''base.require("Tidak ada\\nsolusi tambahan yang dibuat" in combined, "Unit 6 no-invented-solution notice")
    base.require("memerlukan $c\\\\ne0$ tanpa memisahkan kasus" in combined.replace("\\n", " "), "Unit 7 complex-classification condition note")
    base.require("Maka tugas pembuktian ini memerlukan hipotesis tambahan" in combined, "Unit 7 false-universal-claim note")
    base.require("dahulu disalahidentifikasi sebagai Johannes Kepler" in combined, "Unit 7 portrait correction")''',
    expected=1,
)
replace_exact(
    '''    for marker in ("AGC-CORR-0010", "AGC-ADAPT-0008", "AGC-ADAPT-0009", "AGC-ADAPT-0010", "AGC-ADAPT-0011"):
        base.require(marker in corrections, f"Unit 6 delta ledger marker {marker}")''',
    '''    for marker in ("AGC-CORR-0010", "AGC-ADAPT-0008", "AGC-ADAPT-0009", "AGC-ADAPT-0010", "AGC-ADAPT-0011"):
        base.require(marker in corrections, f"Unit 6 delta ledger marker {marker}")
    for marker in (
        "AGC-CORR-0011", "AGC-CORR-0012", "AGC-CORR-0013", "AGC-CORR-0014",
        "AGC-CORR-0015", "AGC-CORR-0016", "AGC-CORR-0017", "AGC-CORR-0018",
        "AGC-CORR-0019", "AGC-ADAPT-0012", "AGC-ADAPT-0013", "AGC-ADAPT-0014",
        "AGC-ADAPT-0015", "AGC-ADAPT-0016",
    ):
        base.require(marker in corrections, f"Unit 7 delta ledger marker {marker}")''',
    expected=1,
)
replace_exact("len(ids) == len(set(ids)) == 334", "len(ids) == len(set(ids)) == 388", expected=1)
replace_exact(
    '''        "unit_06": base.verify_solution_map(6, SOURCE / "worksheet-06-solutions.md", 30, 9),
    }''',
    '''        "unit_06": base.verify_solution_map(6, SOURCE / "worksheet-06-solutions.md", 30, 9),
        "unit_07": base.verify_solution_map(7, SOURCE / "worksheet-07-solutions.md", 33, 3),
    }''',
    expected=1,
)
replace_exact(
    '''        "unit_06": base.verify_rights("RIGHTS-unit-06.csv", "ASSET_CLOSURE-unit-06.json", 3, 4),
    }''',
    '''        "unit_06": base.verify_rights("RIGHTS-unit-06.csv", "ASSET_CLOSURE-unit-06.json", 3, 4),
        "unit_07": base.verify_rights("RIGHTS-unit-07.csv", "ASSET_CLOSURE-unit-07.json", 9, 13),
    }''',
    expected=1,
)
replace_exact(
    '''        "unit_05": previous.verify_unit5_authority(),
        "unit_06": verify_unit6_authority(),
    }''',
    '''        "unit_05": previous.previous.verify_unit5_authority(),
        "unit_06": previous.verify_unit6_authority(),
        "unit_07": verify_unit7_authority(),
    }''',
    expected=1,
)
replace_exact('"Kurva Aljabar - Unit 1-6", "HTML title"', '"Kurva Aljabar - Unit 1-7", "HTML title"', expected=1)
replace_exact("len(images) == 44", "len(images) == 53", expected=1)
replace_exact("== 2150", "== 2580", expected=1)
replace_exact(
    '''        "Kredit media Unit 6",
    ):
        base.require(marker in html_text, f"HTML marker absent: {marker}")''',
    '''        "Kredit media Unit 6",
        "Kuliah 7: Irisan Kerucut dan Kuadrik",
        "Soal 7.33 - 6 poin",
        "Solusi Soal 7.22",
        "Kredit media Unit 7",
    ):
        base.require(marker in html_text, f"HTML marker absent: {marker}")
    for alt in ("Orbit eliptik", "Orbit parabola", "Orbit hiperbola"):
        image = soup.find("img", attrs={"alt": alt})
        base.require(image is not None, f"HTML animated image absent: {alt}")
        base.require(image.get("src", "").startswith("data:image/gif;base64,"), f"HTML animation MIME lost: {alt}")''',
    expected=1,
)
replace_exact('receipt["through_unit"] == 6', 'receipt["through_unit"] == 7', expected=1)
replace_exact('reader.metadata.title == "Kurva Aljabar - Unit 1-6"', 'reader.metadata.title == "Kurva Aljabar - Unit 1-7"', expected=1)
replace_exact(
    '''        "Kredit media Unit 6",
    ):
        base.require(marker in pdf_text, f"PDF text marker absent: {marker}")''',
    '''        "Kredit media Unit 6",
        "Kuliah 7: Irisan Kerucut dan Kuadrik",
        "Soal 7.33 - 6 poin",
        "Solusi Soal 7.22",
        "Kredit media Unit 7",
    ):
        base.require(marker in pdf_text, f"PDF text marker absent: {marker}")''',
    expected=1,
)
replace_exact('"through_unit": 6', '"through_unit": 7', expected=1)
replace_exact("unit3_through_unit6_authority_and_official_pdf_hash_replay", "unit3_through_unit7_authority_and_official_pdf_hash_replay", expected=1)

required_markers = [
    'SOURCE / "lecture-07.md"',
    'SOURCE / "worksheet-07-solutions.md"',
    '"unit_07": base.verify_solution_map(7',
    '"unit_07": base.verify_rights("RIGHTS-unit-07.csv"',
    '"unit_07": verify_unit7_authority()',
    'EXPECTED_PDF_PAGES = 142',
    'len(images) == 53',
    '== 2580',
]
missing = [marker for marker in required_markers if marker not in source]
if missing:
    raise SystemExit(f"Transformed reader-QA markers absent: {missing}")

exec(compile(source, str(Path(__file__).resolve()), "exec"), globals())
