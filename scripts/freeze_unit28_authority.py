#!/usr/bin/env python3
"""Freeze the complete bounded official Unit 28 Wikiversity authority closure.

This specialization reuses the proven Unit 27 authority implementation while
binding only independently discovered Unit 28 identities and topology.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "freeze_unit27_authority.py"
TEMPLATE_SHA256 = "9f8b9cbb6b42c7bca26b0ff77f42bbfa9784babf7b9a4497f19a5d9b66b8f864"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Unit 28 specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


def replace_section(text: str, start: str, end: str, replacement: str) -> str:
    first = text.find(start)
    if first < 0:
        raise SystemExit(f"Unit 28 specialization start marker absent: {start!r}")
    second = text.find(end, first)
    if second < 0:
        raise SystemExit(f"Unit 28 specialization end marker absent: {end!r}")
    return text[:first] + replacement.rstrip() + "\n\n\n" + text[second:]


if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
    raise SystemExit("Frozen Unit 27 authority template is absent or has drifted")

generated = TEMPLATE.read_text(encoding="utf-8")
generated = replace_once(
    generated,
    "from pathlib import Path\n",
    "from pathlib import Path\nimport xml.etree.ElementTree as ET\n",
)
for old, new in (
    ("Unit 27", "Unit 28"),
    ("unit-27", "unit-28"),
    ("UNIT_27", "UNIT_28"),
    ("unit27", "unit28"),
    ("AGC-U27", "AGC-U28"),
    ("br-ak-u27", "br-ak-u28"),
    ("lecture-27", "lecture-28"),
    ("worksheet-27", "worksheet-28"),
    ("Vorlesung27", "Vorlesung28"),
    ("Arbeitsblatt27", "Arbeitsblatt28"),
    ("{kind}-27", "{kind}-28"),
):
    generated = generated.replace(old, new)

generated = replace_once(generated, "UNIT = 27", "UNIT = 28")
generated = replace_once(generated, 'LECTURE_TITLE = f"{COURSE}/Vorlesung 27"', 'LECTURE_TITLE = f"{COURSE}/Vorlesung 28"')
generated = replace_once(generated, 'WORKSHEET_TITLE = f"{COURSE}/Arbeitsblatt 27"', 'WORKSHEET_TITLE = f"{COURSE}/Arbeitsblatt 28"')
generated = generated.replace('"unit": 27,', '"unit": 28,')
generated = replace_once(generated, '"unit_number": 27,', '"unit_number": 28,')

generated = replace_section(
    generated,
    'TOPIC_HEADING = "Der projektive Raum"',
    "EXPECTED_COURSE = {",
    '''TOPIC_HEADING = "Projektive Varietäten"
ADDITIONAL_TOPIC_HEADINGS = [
    "Algebraische Funktionen und Morphismen",
    "Homogenisierung und projektiver Abschluss",
    "Projektive ebene Kurven",
]''',
)

generated = replace_section(
    generated,
    "EXPECTED_ENTRIES = {",
    "EXPECTED_LATEX = {",
    '''EXPECTED_ENTRIES = {
    "lecture": {
        "pageid": 50734,
        "revid": 1052516,
        "parentid": 1019437,
        "timestamp": "2025-08-27T13:52:03Z",
        "sha1": "d037d0173bca4c443e06c7991d830568fa8dc0ea",
        "wikitext_bytes": 4266,
    },
    "worksheet": {
        "pageid": 50763,
        "revid": 793497,
        "parentid": 541288,
        "timestamp": "2022-08-25T06:04:27Z",
        "sha1": "7ee8f07ea803541b23e8e1fa686c7b2c17e6f67a",
        "wikitext_bytes": 1811,
    },
}''',
)

generated = replace_section(
    generated,
    "EXPECTED_LATEX = {",
    "EXPECTED_CLOSURES = {",
    '''EXPECTED_LATEX = {
    "lecture": {
        "pageid": 51876,
        "revid": 806126,
        "parentid": 796346,
        "timestamp": "2022-09-18T07:15:12Z",
        "sha1": "1d092e4f15139d9908d36c4d64a1f4fde570e1ba",
        "wikitext_bytes": 9,
    },
    "worksheet": {
        "pageid": 53021,
        "revid": 806094,
        "parentid": 796313,
        "timestamp": "2022-09-18T07:10:02Z",
        "sha1": "1d092e4f15139d9908d36c4d64a1f4fde570e1ba",
        "wikitext_bytes": 9,
    },
}''',
)

generated = replace_section(
    generated,
    "EXPECTED_CLOSURES = {",
    "def require(condition: bool, message: str) -> None:",
    '''EXPECTED_CLOSURES = {
    "lecture": {
        "parser_occurrences": 119,
        "unique_exact_titles": 119,
        "dependencies": 119,
        "with_root": 120,
        "canonical_sha256": "e5f7a370f948b4e1ab9cc663820569cfad9811bf7c9da88546995084059120cc",
    },
    "worksheet": {
        "parser_occurrences": 74,
        "unique_exact_titles": 74,
        "dependencies": 74,
        "with_root": 75,
        "canonical_sha256": "394da195ee18a8413830d80e0552ed4d71d69f04a83e952c594de3ab799249f5",
    },
    "solution-10": {
        "parser_occurrences": 7,
        "unique_exact_titles": 7,
        "dependencies": 7,
        "with_root": 8,
        "canonical_sha256": "54c8c9c86a9e42371574b63eb8b25cfc84e0848f25a46e9fd81f48839ce0a619",
    },
}
EXPECTED_SOLUTIONS = {
    10: {
        "pageid": 21591,
        "revid": 1112869,
        "parentid": 958136,
        "timestamp": "2026-08-21T18:15:43Z",
        "sha1": "85608d2ad2ee8515d39df596af6407dc0270b7f0",
        "wikitext_bytes": 1269,
    },
}
EXPECTED_PUBLIC_SOLUTION_NUMBERS: list[int] | None = [10]
EXPECTED_AUTHORED_POINTS: list[int] | None = [2, 2, 2, 2, 2, 3, 2, 4, 3, 4, 3, 4, 3, 3]
EXPECTED_DISPLAYED_POINTS = {11: 3, 12: 4, 13: 3, 14: 3}
EXPECTED_MEDIA_NAMES = [
    "Soccerball.svg",
    "Torus_illustration.png",
    "Double_torus_illustration.png",
    "Sphere_with_three_handles.png",
]
EXPECTED_COURSE_CREDITS = {
    "Soccerball.svg": {"author": "", "user": "Ranveig", "repository": "Commons", "license_label": "PD"},
    "Torus_illustration.png": {"author": "Oleg Alexandrov", "user": "", "repository": "Commons", "license_label": "PD"},
    "Double_torus_illustration.png": {"author": "Oleg Alexandrov", "user": "", "repository": "Commons", "license_label": "PD"},
    "Sphere_with_three_handles.png": {"author": "Oleg Alexandrov", "user": "", "repository": "Commons", "license_label": "PD"},
}
EXPECTED_MEDIA: dict[str, dict] = {
    "Soccerball.svg": {
        "pageid": 342296, "revid": 1235719533, "parentid": 1219683471,
        "timestamp": "2026-06-21T18:54:02Z", "sha1": "304fcc46c72e046d920a590b6f27c93865f9f4f3",
        "wikitext_bytes": 874, "source_timestamp": "2019-02-02T16:20:56Z", "source_bytes": 1311,
        "source_sha1": "bff39e7bffd1d5e84fd063bc11205226a62a3db7", "width": 500, "height": 500,
    },
    "Torus_illustration.png": {
        "pageid": 4369490, "revid": 1134413459, "parentid": 1124090063,
        "timestamp": "2025-12-21T08:02:32Z", "sha1": "9790f679d35ecf3a4ebb4ee9d89c6bc2759c536e",
        "wikitext_bytes": 1821, "source_timestamp": "2008-07-13T01:12:06Z", "source_bytes": 150645,
        "source_sha1": "40b8981eb5d3c98f12109b57b0f281e7a0f6dbc0", "width": 900, "height": 594,
    },
    "Double_torus_illustration.png": {
        "pageid": 2690147, "revid": 1211711172, "parentid": 1134412824,
        "timestamp": "2026-05-10T11:06:13Z", "sha1": "640673e0e4c111dae4dd6b5a29394d419ac70b26",
        "wikitext_bytes": 2404, "source_timestamp": "2008-07-12T04:32:19Z", "source_bytes": 266030,
        "source_sha1": "87ef1565f0a904b7ff52022b44a3ca2265339c58", "width": 985, "height": 1077,
    },
    "Sphere_with_three_handles.png": {
        "pageid": 4262090, "revid": 1134413394, "parentid": 1127050379,
        "timestamp": "2025-12-21T08:02:25Z", "sha1": "b2fabe6bb8a0c3e88ecfc38f253e16d0c98371f0",
        "wikitext_bytes": 2819, "source_timestamp": "2008-06-23T04:28:09Z", "source_bytes": 398740,
        "source_sha1": "6890fd8dbe8f2a238b2629531380e3dcbaa792eb", "width": 1308, "height": 1004,
    },
}
EXPECTED_PDFS = {
    "lecture": {
        "file_title": "Datei:Algebraische Kurven (Osnabrück 2012)Vorlesung28.pdf",
        "file_pageid": 53377,
        "file_revid": 325147,
        "file_parentid": 322185,
        "file_timestamp": "2012-08-02T10:18:19Z",
        "file_sha1": "0dddd953193e6bd38b187c0dc8835839191007b6",
        "source_timestamp": "2012-08-02T10:18:19Z",
        "source_bytes": 106537,
        "source_sha1": "bbdfbb98c0784205fd5e2ab006b6fd6992d54e2d",
        "local_sha256": "0d040f9a5663e6d0d7451f4de864a0712e35e08e961afc66d6742dfbee065609",
        "page_count": 9,
    },
    "worksheet": {
        "file_title": "Datei:Algebraische Kurven (Osnabrück 2012)Arbeitsblatt28.pdf",
        "file_pageid": 54275,
        "file_revid": 325016,
        "file_parentid": 321557,
        "file_timestamp": "2012-07-31T14:05:18Z",
        "file_sha1": "5ccd19a3178e7a834b08408eba3f6b172cb7c854",
        "source_timestamp": "2012-07-31T14:05:18Z",
        "source_bytes": 45643,
        "source_sha1": "efc51ba29c7dacb0739382569f06b35860e11dd3",
        "local_sha256": "579b29f1250b346549522aadc465f7afa0c67b012b5d7ba76b4c6eb0c94a5d12",
        "page_count": 3,
    },
}
EXPECTED_LIVE_UNION = 164
EXPECTED_ROOT_CONTRIBUTOR = "Arbota"
SOURCE_DEFECT_BINDINGS = [
    {
        "id": "AGC-U28-SRC-001",
        "surface": "lecture current semantic source / expanded TeX",
        "source_text": "nach Aufgabe *****",
        "issue": "The proof of the principal-ideal homogenization claim contains an unresolved internal exercise-number placeholder.",
        "reader_handling": "Keep the linked exercise title but do not invent a number; disclose the unresolved source reference.",
    },
    {
        "id": "AGC-U28-SRC-002",
        "surface": "lecture current semantic source / expanded TeX",
        "source_text": "siehe Aufgabe *****",
        "issue": "The counterexample pointer for the non-algebraically-closed case contains an unresolved internal exercise-number placeholder.",
        "reader_handling": "Keep the linked exercise title but do not invent a number; disclose the unresolved source reference.",
    },
]''',
)

for old, new in (
    ('require(len(entries) == 11, "Unit 28 must retain exactly eleven ordered exercises")',
     'require(len(entries) == 14, "Unit 28 must retain exactly fourteen ordered exercises")'),
    ('list(range(1, 12))', 'list(range(1, 15))'),
    ('role = "warm-up" if number <= 7 else "submitted"',
     'role = "warm-up" if number <= 10 else "submitted"'),
    ('"points_displayed_in_worksheet": number >= 8,',
     '"points_displayed_in_worksheet": number >= 11,'),
    ('"starred_in_worksheet": False,',
     '"starred_in_worksheet": number == 10,'),
    ('require(len(toc_lines) == 11, "worksheet TOC exercise count")',
     'require(len(toc_lines) == 14, "worksheet TOC exercise count")'),
    ('require(not any("*" in line for line in toc_lines), "unexpected star topology")',
     'require([i + 1 for i, line in enumerate(toc_lines) if "*" in line] == [10], "star topology")'),
    ('require(len(candidate_pages) == 11, "candidate query must return exactly eleven page records")',
     'require(len(candidate_pages) == 14, "candidate query must return exactly fourteen page records")'),
    ('"warm_up_numbers": list(range(1, 8)),',
     '"warm_up_numbers": list(range(1, 11)),'),
    ('"submitted_numbers": list(range(8, 12)),',
     '"submitted_numbers": list(range(11, 15)),'),
    ('"starred_numbers": [],',
     '"starred_numbers": [10],'),
    ('"exact_candidate_title_count": 11,',
     '"exact_candidate_title_count": 14,'),
    ('require(solutions["exercise_count"] == 11, "exercise count")',
     'require(solutions["exercise_count"] == 14, "exercise count")'),
    ('require(media_closure["reader_media_positions"] == 10 and len(media_closure["assets"]) == 10, "media replay")',
     'require(media_closure["reader_media_positions"] == 4 and len(media_closure["assets"]) == 4, "media replay")'),
):
    generated = replace_once(generated, old, new)

generated = replace_once(
    generated,
    '''        with Image.open(local) as image:
            image.verify()
        with Image.open(local) as image:
            width, height = int(image.width), int(image.height)
            frames = int(getattr(image, "n_frames", 1))''',
    '''        if info["mime"] == "image/svg+xml":
            svg_root = ET.fromstring(data)
            require(svg_root.tag.endswith("svg"), f"SVG root element: {name}")
            width = int(float(svg_root.attrib["width"].removesuffix("px")))
            height = int(float(svg_root.attrib["height"].removesuffix("px")))
            frames = 1
        else:
            with Image.open(local) as image:
                image.verify()
            with Image.open(local) as image:
                width, height = int(image.width), int(image.height)
                frames = int(getattr(image, "n_frames", 1))''',
)

generated = replace_section(
    generated,
    "def verify_source_defects() -> list[dict]:",
    "def official_pdfs_and_media(",
    '''def verify_source_defects() -> list[dict]:
    tex = (OUT / "lecture-28-expanded.tex").read_text(encoding="utf-8")
    html = (OUT / "lecture-28.html").read_text(encoding="utf-8")
    require("nach Aufgabe *****" in tex, "principal-ideal reference defect evidence")
    require("Aufgabe *****." in tex, "counterexample reference defect evidence")
    require("Hauptideal/Homogenisierung/Aufgabe" in html, "principal-ideal link evidence")
    require("R/Projektiver_Abschluss/Homogene_Gleichungen/Aufgabe" in html, "counterexample link evidence")
    require(html.count(">*****</a>") == 2, "rendered unresolved-reference count")
    return SOURCE_DEFECT_BINDINGS''',
)

generated = replace_section(
    generated,
    '        "component_discrepancies": {',
    '        "assets": asset_records,',
    '''        "component_discrepancies": {
            "static_pdf_versus_semantic_revision_boundary": (
                "The official PDFs are unchanged 2012 static witnesses. They are not asserted to be renders "
                "of the frozen 2025 lecture or 2022 worksheet semantic revisions; the expanded TeX captures "
                "are separately byte-bound dynamic surfaces."
            ),
            "dual_pdf_file_page_license_notices": (
                "Each local file page identifies the generated print version with the current "
                "CC BY-SA 4.0 route while retaining the legacy CC BY-SA 2.0 Germany file notice."
            ),
            "media_credit_labels": [
                {
                    "source_parser_name": "Soccerball.svg",
                    "kind": "historical-generic-public-domain-versus-current-CC0-route",
                    "course_embedded_user": "Ranveig",
                    "course_embedded_label": "PD",
                    "current_commons_uploader": "MapGrid",
                    "current_commons_label": "CC0",
                    "handling": "Preserve the historical course credit and use the precise current Commons CC0 component route.",
                },
            ],
        },''',
)

generated = replace_section(
    generated,
    "def write_freeze_note(manifest_path: Path, manifest: dict) -> None:",
    "def main() -> int:",
    '''def write_freeze_note(manifest_path: Path, manifest: dict) -> None:
    pdfs = {item["kind"]: item for item in manifest["official_pdf_witnesses"]}
    solutions = manifest["public_solution_transclusion_closures"]
    roles = manifest["solutions"]["ordered_role_point_and_star_topology"]
    lecture_topology = manifest["transclusion_topology"]["lecture"]
    worksheet_topology = manifest["transclusion_topology"]["worksheet"]
    lines = [
        "# Unit 28 authority freeze",
        "",
        f"Frozen at {manifest['frozen_utc']} from the official German Wikiversity course {COURSE}. This is an authority boundary, not an Indonesian translation checkpoint.",
        "",
        "## Exact source boundary",
        "",
        f"- Course route: pageid {manifest['source_course_surface']['pageid']}, revid {manifest['source_course_surface']['revid']}.",
        f"- Lecture: pageid {manifest['lecture']['pageid']}, revid {manifest['lecture']['revid']}, MediaWiki SHA-1 {manifest['lecture']['mediawiki_sha1']}.",
        f"- Worksheet: pageid {manifest['worksheet']['pageid']}, revid {manifest['worksheet']['revid']}, MediaWiki SHA-1 {manifest['worksheet']['mediawiki_sha1']}.",
        f"- Topic boundary: {TOPIC_HEADING}; {', '.join(ADDITIONAL_TOPIC_HEADINGS)}.",
        f"- Lecture closure: {lecture_topology['with_root']} identities; SHA-256 {lecture_topology['canonical_identity_rows_sha256']}.",
        f"- Worksheet closure: {worksheet_topology['with_root']} identities; SHA-256 {worksheet_topology['canonical_identity_rows_sha256']}.",
        f"- Course author: Holger Brenner. Root-revision contributor: {manifest['root_revision_contributors']['records'][0]['revision_contributor']} (revision provenance, not course authorship).",
        "- Both /latex revisions contain only {{Latex}}. Expanded TeX files are byte-bound dynamic captures, not immutable standalone source revisions.",
        "",
        "## Exercises and solutions",
        "",
        f"Exactly 14 exercises are preserved in order: warm-up 1-10 and submitted 11-14. Exercise 10 alone carries the source star. Submitted displayed points are 3, 4, 3, 3 ({roles['submitted_displayed_point_total']} total); there is no upload exercise.",
        f"All and only public solution numbers are {[item['exercise_number'] for item in solutions]}; exact negative API evidence covers {manifest['solutions']['negative_public_solution_evidence']['negative_numbers']}.",
    ]
    for item in solutions:
        lines.append(
            f"- Solution {item['exercise_number']}: root plus {item['topology']['dependencies']} dependencies = {item['topology']['with_root']} identities; SHA-256 {item['topology']['canonical_identity_rows_sha256']}."
        )
    lines.extend(["", "## Bound source defects", ""])
    for item in manifest["source_defect_bindings"]:
        lines.append(f"- {item['id']}: {item['issue']} Reader handling: {item['reader_handling']}")
    lines.extend([
        "",
        "## Media, PDFs, accessibility, and component rights",
        "",
        "The parser exposes four substantive reader-media positions and exactly two official PDFs. Each media original, Commons description revision, source identity, creator/uploader record, and component license is bound in RIGHTS-unit-28.csv and ASSET_CLOSURE-unit-28.json.",
        "Soccerball.svg carries a historical course PD/Ranveig label and a precise current Commons CC0/MapGrid route; both are preserved. The three Oleg Alexandrov surface images remain public-domain components.",
        f"- Lecture PDF: {pdfs['lecture']['local_bytes']} bytes, {pdfs['lecture']['page_count']} pages, SHA-256 {pdfs['lecture']['local_sha256']}.",
        f"- Worksheet PDF: {pdfs['worksheet']['local_bytes']} bytes, {pdfs['worksheet']['page_count']} pages, SHA-256 {pdfs['worksheet']['local_sha256']}.",
        "The official PDFs are static 2012 witnesses; their accessibility structures and extractable-text counts are recorded exactly. Preserve both the current CC BY-SA 4.0 print/course route and legacy CC BY-SA 2.0 Germany file notice; make no blanket mixed-set claim.",
        "",
        "## Replay boundary",
        "",
        f"Final live replay passed for {manifest['final_live_identity_replay']['semantic_unique_identity_count']} unique Wikiversity semantic identities, both local Wikiversity PDF identities, and {manifest['final_live_identity_replay']['commons_media_identity_count']} Commons media identities.",
        f"Manifest: {manifest_path.relative_to(ROOT).as_posix()}; {manifest_path.stat().st_size} bytes; SHA-256 {base.digest(manifest_path)}.",
        "",
    ])
    FREEZE_NOTE.write_text("\\n".join(lines), encoding="utf-8", newline="\\n")''',
)

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE), "exec"), namespace)
