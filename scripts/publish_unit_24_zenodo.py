#!/usr/bin/env python3
"""Publish the verified Unit 24 checkpoint in the existing Zenodo lineage.

This adapter specializes the byte-pinned, accepted Unit 21 publisher. It keeps
credentials runtime-only, loads final coverage and file identities from the
generated Unit 24 candidate/manifest, and performs the inherited anonymous
full-byte readback after publication.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "publish_unit_21_zenodo.py"
TEMPLATE_SHA256 = "2fe6b8eeea1d1fe99d9a090677ae53f1972f4987baa80a51cc64c5f746e22ef2"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Unit 24 Zenodo specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


def replace_section(text: str, start: str, end: str, replacement: str) -> str:
    if text.count(start) != 1 or text.count(end) != 1:
        raise SystemExit(f"Could not isolate Unit 21 section {start!r} .. {end!r}")
    left = text.index(start)
    right = text.index(end, left)
    return text[:left] + replacement.rstrip() + text[right:]


def materialize_unit21_implementation() -> str:
    """Materialize the accepted Unit 21 publisher without running it."""

    if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
        raise SystemExit("Accepted Unit 21 Zenodo publisher is absent or has drifted")
    source = TEMPLATE.read_text(encoding="utf-8")
    marker = '\nnamespace = {"__file__":'
    if source.count(marker) != 1:
        raise SystemExit("Could not isolate the accepted Unit 21 Zenodo builder")
    builder = source[: source.index(marker)]
    namespace = {"__file__": str(TEMPLATE), "__name__": "unit21_builder_capture"}
    exec(compile(builder, str(TEMPLATE), "exec"), namespace)
    generated = namespace.get("generated")
    if not isinstance(generated, str):
        raise SystemExit("Accepted Unit 21 Zenodo builder yielded no implementation")
    return generated


generated = materialize_unit21_implementation()
for old, new in (
    ("units-01-21", "units-01-24"),
    ("UNITS_01_21", "UNITS_01_24"),
    ("UNIT_21", "UNIT_24"),
    ("unit-21", "unit-24"),
    ("unit_21", "unit_24"),
    ("unit21", "unit24"),
    ("Unit 1–21", "Unit 1–24"),
    ("Units 1–21", "Units 1–24"),
    ("Unit 21", "Unit 24"),
):
    generated = generated.replace(old, new)
generated = generated.replace("22087566", "22088753")

generated = replace_once(
    generated,
    """EXPECTED_UNITS = 21
EXPECTED_PLANNED_UNITS = 30
EXPECTED_EXERCISES = 577
EXPECTED_PUBLIC_SOLUTIONS = 102
EXPECTED_MEDIA_POSITIONS = 76""",
    """EXPECTED_UNITS = 24
EXPECTED_PLANNED_UNITS = 30


def _runtime_candidate_coverage() -> dict[str, int]:
    path = ROOT / "qa" / "UNIT_24_RELEASE_CANDIDATE.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Unit 24 release candidate is unavailable or invalid: {exc}") from exc
    if not isinstance(value, dict) or not str(value.get("status", "")).startswith("PASS"):
        raise RuntimeError("Unit 24 release candidate is not a PASS object")
    if value.get("through_unit") != EXPECTED_UNITS:
        raise RuntimeError("Unit 24 release candidate has the wrong boundary")
    coverage = value.get("coverage")
    if not isinstance(coverage, dict):
        raise RuntimeError("Unit 24 release candidate coverage is missing")
    keys = ("exercises", "public_source_solutions", "reader_media_positions")
    result: dict[str, int] = {}
    for key in keys:
        item = coverage.get(key)
        if not isinstance(item, int) or isinstance(item, bool) or item < 0:
            raise RuntimeError(f"Unit 24 release candidate {key} is not a non-negative integer")
        result[key] = item
    if result["exercises"] == 0 or result["public_source_solutions"] == 0:
        raise RuntimeError("Unit 24 cumulative exercise/solution coverage cannot be zero")
    return result


_RUNTIME_COVERAGE = _runtime_candidate_coverage()
EXPECTED_EXERCISES = _RUNTIME_COVERAGE["exercises"]
EXPECTED_PUBLIC_SOLUTIONS = _RUNTIME_COVERAGE["public_source_solutions"]
EXPECTED_MEDIA_POSITIONS = _RUNTIME_COVERAGE["reader_media_positions"]""",
)

generated = replace_once(
    generated,
    """    require_equal(
        rights.get("independent_non_endorsed_derivative"),
        True,
        "non-endorsement flag",
    )""",
    """    require_equal(
        rights.get("independent_non_endorsed_derivative"),
        True,
        "non-endorsement flag",
    )
    require_equal(
        rights.get("source_course_boundary"),
        {
            "units_01_23": "Algebraische Kurven (Osnabrück 2025–2026)",
            "unit_24": "Algebraische Kurven (Osnabrück 2012)",
        },
        "source-course boundary",
    )
    require_equal(
        rights.get("unit_24_pdf_component_notices"),
        ["CC BY-SA 4.0 course route", "CC BY-SA 2.0 Germany file notice"],
        "Unit 24 PDF component notices",
    )""",
)

# Strengthen the inherited archive smoke test at the new boundary: the source
# archive must expose the actual Unit 24 lecture, worksheet, and public-solution
# files, not merely the older Unit 15 sentinel trio.
for old, new in (
    ('f"{prefix}source/id-ID/lecture-15.md"', 'f"{prefix}source/id-ID/lecture-24.md"'),
    ('f"{prefix}source/id-ID/worksheet-15.md"', 'f"{prefix}source/id-ID/worksheet-24.md"'),
    (
        'f"{prefix}source/id-ID/worksheet-15-solutions.md"',
        'f"{prefix}source/id-ID/worksheet-24-solutions.md"',
    ),
):
    generated = replace_once(generated, old, new)

metadata_function = r'''
def metadata(contract: dict | None = None) -> dict:
    if contract is None:
        manifest_path = RELEASE / MANIFEST_NAME
        contract = validate_release_contract() if manifest_path.is_file() else current_boundary_contract()
    coverage = contract["coverage"]
    pages = coverage["pdf_pages"]
    backend_records = coverage["backend_records"]
    pages_id = format_id_number(pages)
    records_id = format_id_number(backend_records)
    exercises = coverage["exercises"]
    solutions = coverage["public_source_solutions"]
    media_positions = coverage["reader_media_positions"]
    payload = {
        "title": TITLE,
        "upload_type": "publication",
        "publication_type": "book",
        "description": (
            "<p><strong>Rilis kumulatif kerja Bahasa Indonesia (id-ID), Unit 1–24</strong>, "
            "dari <em>Algebraische Kurven</em> karya Holger Brenner. Unit 1–23 mengikuti "
            "kursus resmi <em>Osnabrück 2025–2026</em>; Unit 24 mengikuti kuliah dan "
            "lembar kerja resmi <em>Osnabrück 2012</em>, karena kursus 2025–2026 "
            "berakhir pada Unit 23. "
            f"Checkpoint parsial ini memuat 24 kuliah, 24 lembar kerja, {exercises} soal, "
            f"seluruh {solutions} solusi publik yang tersedia pada revisi sumber yang "
            f"dibekukan, dan {media_positions} posisi media pembaca yang dilengkapi kredit. "
            "Ini belum merupakan edisi 30-unit yang lengkap; penerjemahan berlanjut dalam "
            "urutan sumber.</p>"
            f"<p>Paket preservasi memuat pembaca PDF A4 {pages_id} halaman, pembaca HTML "
            "mandiri dengan MathML dan reflow seluler, snapshot sumber/backend asli "
            f"{records_id} rekaman yang dapat dilanjutkan, adapter backend modular "
            "tervalidasi, manifest, build receipt, saksi otoritas, hak komponen, dan bukti "
            "QA. Terjemahan dan penataan ulang teks kursus berada di bawah CC BY-SA 4.0. "
            "Saksi PDF resmi Unit 24 mempertahankan pemberitahuan komponen jalur kursus "
            "CC BY-SA 4.0 dan berkas CC BY-SA 2.0 Germany; setiap media pihak ketiga "
            "mempertahankan pencipta, sumber, dan lisensi komponennya sendiri. Edisi "
            "independen ini disiapkan atas arahan pengguna "
            f"dengan {PROVENANCE} Ini bukan terbitan resmi Holger Brenner, Universitas "
            "Osnabrück, Wikiversity, atau Wikimedia Foundation, dan tidak menyiratkan "
            "dukungan mereka.</p>"
            "<p><strong>English identification:</strong> Cumulative working Indonesian "
            "(id-ID) edition, Units 1–24, of Holger Brenner's <em>Algebraische Kurven</em>. "
            "Units 1–23 follow the official Osnabrück 2025–2026 course; Unit 24 follows "
            "the official Osnabrück 2012 lecture and worksheet because the 2025–2026 "
            f"course ends at Unit 23. It contains {exercises} exercises, all {solutions} "
            f"frozen public-source solutions, {media_positions} credited reader-media "
            f"positions, self-contained HTML, a {pages}-page A4 PDF, and an editable "
            f"{backend_records:,}-record native-backend snapshot with a validated modular "
            "adapter, component-rights records, authority witnesses, and QA evidence. The "
            "Unit 24 official PDF witnesses retain both the CC BY-SA 4.0 course-route and "
            "CC BY-SA 2.0 Germany file notices; no blanket licence is asserted for the "
            "mixed-rights payload. This is an independent, non-endorsed derivative and "
            "not yet the complete 30-unit edition.</p>"
        ),
        "creators": [{"name": "Brenner, Holger"}],
        "contributors": [
            {"name": "TTP", "type": "Other", "affiliation": ORGANIZATION_HUB},
            {"name": MODEL_ID, "type": "Other"},
        ],
        "access_right": "open",
        "license": "other-open",
        "keywords": [
            "geometri aljabar",
            "algebraic geometry",
            "Bahasa Indonesia",
            "id-ID",
            "kurva aljabar",
            "open textbook",
        ],
        "language": "ind",
        "version": VERSION,
        "related_identifiers": [
            {
                "identifier": (
                    "https://de.wikiversity.org/wiki/"
                    "Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)"
                ),
                "relation": "isDerivedFrom",
                "resource_type": "publication-book",
            },
            {
                "identifier": (
                    "https://de.wikiversity.org/wiki/"
                    "Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2012)"
                ),
                "relation": "isDerivedFrom",
                "resource_type": "publication-book",
            },
            {
                "identifier": ORGANIZATION_HUB,
                "relation": "isReferencedBy",
                "resource_type": "software",
            },
        ],
    }
    validate_metadata(payload, contract)
    return payload
'''
generated = replace_section(
    generated,
    "def metadata(contract: dict | None = None) -> dict:",
    "\n\ndef validate_metadata(payload: dict, contract: dict) -> None:",
    metadata_function,
)

validate_metadata_function = r'''
def validate_metadata(payload: dict, contract: dict) -> None:
    coverage = contract["coverage"]
    description = payload.get("description", "")
    title = payload.get("title", "")
    contributors = payload.get("contributors", [])
    creators = payload.get("creators", [])
    ttp_entries = [item for item in contributors if item.get("name") == "TTP"]
    model_entries = [item for item in contributors if item.get("name") == MODEL_ID]
    normalized_model_entries = [
        {key: value for key, value in item.items() if value is not None}
        for item in model_entries
    ]
    normalized_creators = [
        {key: value for key, value in item.items() if value is not None}
        for item in creators
    ]

    require_equal(title, TITLE, "Zenodo title")
    if "TTP" in title or "TTP" in description:
        raise RuntimeError("TTP leaked into the title or description")
    require_equal(
        json.dumps(payload, ensure_ascii=False).count("TTP"),
        1,
        "Zenodo metadata TTP occurrence count",
    )
    require_equal(
        ttp_entries,
        [{"name": "TTP", "type": "Other", "affiliation": ORGANIZATION_HUB}],
        "Zenodo organization contributor",
    )
    require_equal(
        normalized_model_entries,
        [{"name": MODEL_ID, "type": "Other"}],
        "Zenodo model contributor",
    )
    require_equal(normalized_creators, [{"name": "Brenner, Holger"}], "Zenodo creators")
    require_equal(payload.get("access_right"), "open", "Zenodo access right")
    require_equal(license_id(payload.get("license")), "other-open", "Zenodo mixed-rights licence")
    require_equal(payload.get("language"), "ind", "Zenodo language")
    require_equal(payload.get("version"), VERSION, "Zenodo version")
    if PROVENANCE not in description:
        raise RuntimeError("Exact model provenance is absent from the Zenodo description")

    markers = (
        "Unit 1–24",
        "Unit 1–23",
        "Unit 24",
        "Osnabrück 2025–2026",
        "Osnabrück 2012",
        f"{coverage['exercises']} soal",
        f"{coverage['public_source_solutions']} solusi publik",
        f"{coverage['reader_media_positions']} posisi media pembaca",
        f"{format_id_number(coverage['pdf_pages'])} halaman",
        f"{format_id_number(coverage['backend_records'])} rekaman",
        "CC BY-SA 4.0",
        "CC BY-SA 2.0 Germany",
        "lisensi komponennya sendiri",
        "belum merupakan edisi 30-unit yang lengkap",
        "tidak menyiratkan dukungan mereka",
        "Units 1–24",
        "independent, non-endorsed derivative",
        "no blanket licence",
    )
    missing = [marker for marker in markers if marker not in description]
    if missing:
        raise RuntimeError(f"Required Unit 24 description markers are missing: {missing}")

    expected_sources = [
        "https://de.wikiversity.org/wiki/"
        "Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)",
        "https://de.wikiversity.org/wiki/"
        "Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2012)",
    ]
    actual_sources = [
        item.get("identifier")
        for item in payload.get("related_identifiers", [])
        if item.get("relation") == "isDerivedFrom"
    ]
    require_equal(actual_sources, expected_sources, "Zenodo source-course identifiers")
'''
generated = replace_section(
    generated,
    "def validate_metadata(payload: dict, contract: dict) -> None:",
    "\n\ndef expected_files() -> dict[str, dict[str, object]]:",
    validate_metadata_function,
)

generated = replace_once(
    generated,
    '            "translated_course_text_license": "CC BY-SA 4.0",',
    '            "translated_course_text_license": "CC BY-SA 4.0",\n'
    '            "source_course_boundary": {\n'
    '                "units_01_23": "Algebraische Kurven (Osnabrück 2025–2026)",\n'
    '                "unit_24": "Algebraische Kurven (Osnabrück 2012)",\n'
    '            },\n'
    '            "unit_24_pdf_component_notices": [\n'
    '                "CC BY-SA 4.0 course route",\n'
    '                "CC BY-SA 2.0 Germany file notice",\n'
    '            ],',
)

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE), "exec"), namespace)
