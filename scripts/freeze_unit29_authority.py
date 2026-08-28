#!/usr/bin/env python3
"""Freeze the bounded official 2012 Unit 29 Wikiversity authority closure."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
UNIT28_WRAPPER = ROOT / "scripts" / "freeze_unit28_authority.py"
UNIT28_WRAPPER_SHA256 = "35a0247855390dcb1a3bc26b8bfe26e8a7e71160e6594aac839c84ef08a8bbfe"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Unit 29 specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


def replace_section(text: str, start: str, end: str, replacement: str) -> str:
    first = text.find(start)
    if first < 0:
        raise SystemExit(f"Unit 29 specialization start marker absent: {start!r}")
    second = text.find(end, first)
    if second < 0:
        raise SystemExit(f"Unit 29 specialization end marker absent: {end!r}")
    return text[:first] + replacement.rstrip() + "\n\n\n" + text[second:]


def materialize_unit28_implementation() -> str:
    if not UNIT28_WRAPPER.is_file() or digest(UNIT28_WRAPPER) != UNIT28_WRAPPER_SHA256:
        raise SystemExit("Reviewed Unit 28 authority wrapper is absent or has drifted")
    source = UNIT28_WRAPPER.read_text(encoding="utf-8")
    marker = '\nnamespace = {"__file__":'
    if source.count(marker) != 1:
        raise SystemExit("Could not isolate the reviewed Unit 28 authority implementation")
    builder = source[: source.index(marker)]
    namespace = {
        "__file__": str(UNIT28_WRAPPER),
        "__name__": "unit28_authority_builder_capture",
    }
    exec(compile(builder, str(UNIT28_WRAPPER), "exec"), namespace)
    generated = namespace.get("generated")
    if not isinstance(generated, str):
        raise SystemExit("Unit 28 authority wrapper yielded no standalone implementation")
    return generated


generated = materialize_unit28_implementation()
for old, new in (
    ("Unit 28", "Unit 29"),
    ("unit-28", "unit-29"),
    ("UNIT_28", "UNIT_29"),
    ("unit28", "unit29"),
    ("AGC-U28", "AGC-U29"),
    ("br-ak-u28", "br-ak-u29"),
    ("lecture-28", "lecture-29"),
    ("worksheet-28", "worksheet-29"),
    ("Vorlesung28", "Vorlesung29"),
    ("Arbeitsblatt28", "Arbeitsblatt29"),
    ("{kind}-28", "{kind}-29"),
):
    generated = generated.replace(old, new)

generated = replace_once(generated, "UNIT = 28", "UNIT = 29")
generated = replace_once(
    generated,
    'LECTURE_TITLE = f"{COURSE}/Vorlesung 28"',
    'LECTURE_TITLE = f"{COURSE}/Vorlesung 29"',
)
generated = replace_once(
    generated,
    'WORKSHEET_TITLE = f"{COURSE}/Arbeitsblatt 28"',
    'WORKSHEET_TITLE = f"{COURSE}/Arbeitsblatt 29"',
)
generated = generated.replace('"unit": 28,', '"unit": 29,')
generated = replace_once(generated, '"unit_number": 28,', '"unit_number": 29,')

generated = replace_section(
    generated,
    'TOPIC_HEADING = "Projektive Varietäten"',
    "EXPECTED_COURSE = {",
    '''TOPIC_HEADING = "Projektion weg von einem Punkt"
ADDITIONAL_TOPIC_HEADINGS = [
    "Abbildungen nach {{math|term= {{op:Projektive Gerade|K}}|SZ=}}",
    "Parametrisierte projektive ebene Kurven",
    "Monomiale projektive Kurven",
]''',
)

generated = replace_section(
    generated,
    "EXPECTED_ENTRIES = {",
    "EXPECTED_LATEX = {",
    '''EXPECTED_ENTRIES = {
    "lecture": {
        "pageid": 51996,
        "revid": 1069408,
        "parentid": 833971,
        "timestamp": "2026-02-05T19:18:37Z",
        "sha1": "6f0742211aeb307841634425937aad9037da51be",
        "wikitext_bytes": 3224,
    },
    "worksheet": {
        "pageid": 50924,
        "revid": 1052757,
        "parentid": 793498,
        "timestamp": "2025-08-27T18:11:31Z",
        "sha1": "0e8dd5d1e5b9bf9552bdbd8f8c61c47ee2a0b726",
        "wikitext_bytes": 1692,
    },
}''',
)

generated = replace_section(
    generated,
    "EXPECTED_LATEX = {",
    "EXPECTED_CLOSURES = {",
    '''EXPECTED_LATEX = {
    "lecture": {
        "pageid": 53378,
        "revid": 806127,
        "parentid": 796347,
        "timestamp": "2022-09-18T07:15:22Z",
        "sha1": "1d092e4f15139d9908d36c4d64a1f4fde570e1ba",
        "wikitext_bytes": 9,
    },
    "worksheet": {
        "pageid": 53022,
        "revid": 806095,
        "parentid": 796314,
        "timestamp": "2022-09-18T07:10:12Z",
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
        "parser_occurrences": 106,
        "unique_exact_titles": 106,
        "dependencies": 106,
        "with_root": 107,
        "canonical_sha256": "87f4ba1e8fb06c51346d5d8fbb105bf2c48e7242a9de2e387906f9608380308b",
    },
    "worksheet": {
        "parser_occurrences": 61,
        "unique_exact_titles": 61,
        "dependencies": 61,
        "with_root": 62,
        "canonical_sha256": "4b6d796d4888b94cfaa1c29811b60ea012118af4af993efd3fd4f23bc5f1229a",
    },
    "solution-02": {
        "parser_occurrences": 16,
        "unique_exact_titles": 16,
        "dependencies": 16,
        "with_root": 17,
        "canonical_sha256": "baafc7ca56b87391f988b7f9b03bf7a4098109451b94b2cec1817fdf0fdb0f86",
    },
    "solution-03": {
        "parser_occurrences": 7,
        "unique_exact_titles": 7,
        "dependencies": 7,
        "with_root": 8,
        "canonical_sha256": "efe168f6a9cec88cc0a21f4e31656747feff0f79c1d6cb30552e615ea9400cd8",
    },
}
EXPECTED_SOLUTIONS = {
    2: {
        "pageid": 21303,
        "revid": 1094621,
        "parentid": 1089317,
        "timestamp": "2026-06-14T16:25:59Z",
        "sha1": "859801fc5d0e4bb16dd1ec72b7af1873ab2f2a4a",
        "wikitext_bytes": 2307,
    },
    3: {
        "pageid": 21573,
        "revid": 1090273,
        "parentid": 959539,
        "timestamp": "2026-05-31T12:45:13Z",
        "sha1": "f0359ee4a15f70916cf5443ab14890f3ac8207dc",
        "wikitext_bytes": 812,
    },
}
EXPECTED_PUBLIC_SOLUTION_NUMBERS: list[int] | None = [2, 3]
EXPECTED_AUTHORED_POINTS: list[int] | None = [2, 4, 3, 3, 4, 3, 3, 3, 3, 5]
EXPECTED_DISPLAYED_POINTS = {6: 3, 7: 3, 8: 3, 9: 3, 10: 5}
EXPECTED_MEDIA_NAMES = [
    "Lemniscate_of_Bernoulli.svg",
    "Tschirnhausen_cubic.png",
]
EXPECTED_COURSE_CREDITS = {
    "Lemniscate_of_Bernoulli.svg": {"author": "", "user": "Zorgit", "repository": "Commons", "license_label": "PD"},
    "Tschirnhausen_cubic.png": {"author": "", "user": "Oleg Alexandrov", "repository": "Commons", "license_label": "PD"},
}
EXPECTED_MEDIA: dict[str, dict] = {
    "Lemniscate_of_Bernoulli.svg": {
        "pageid": 4285176, "revid": 512182780, "parentid": 141013849,
        "timestamp": "2020-11-12T15:39:26Z", "sha1": "f8b8f0465e1f7c5ef3e88ad85e99456ce3d01b24",
        "wikitext_bytes": 368, "source_timestamp": "2010-09-18T22:36:31Z", "source_bytes": 1087,
        "source_sha1": "9c474e2a9ed86aaa7d5a700d311c13b4a05866de", "width": 800, "height": 300,
    },
    "Tschirnhausen_cubic.png": {
        "pageid": 2408689, "revid": 1134413486, "parentid": 1124033583,
        "timestamp": "2025-12-21T08:02:34Z", "sha1": "457e538f54b1164ad87f7b6db252b1c4541edfee",
        "wikitext_bytes": 2240, "source_timestamp": "2007-07-14T16:31:30Z", "source_bytes": 64767,
        "source_sha1": "44a9bbaa597b2fce69ca491335199890546cfb3d", "width": 1100, "height": 1638,
    },
}
EXPECTED_PDFS = {
    "lecture": {
        "file_title": "Datei:Algebraische Kurven (Osnabrück 2012)Vorlesung29.pdf",
        "file_pageid": 53379,
        "file_revid": 325148,
        "file_parentid": 322248,
        "file_timestamp": "2012-08-02T10:21:15Z",
        "file_sha1": "dc79a72b6f301293f130cdeb82cbbd60b6debe51",
        "source_timestamp": "2012-08-02T10:21:15Z",
        "source_bytes": 84904,
        "source_sha1": "23eed466fa4d6473efd9143cd72f2eb319eeac31",
        "local_sha256": "9f7082c66d493cd02a6e4f0579493ad1ba74ddec4b3777517c9ab6daa9610c6d",
        "page_count": 6,
    },
    "worksheet": {
        "file_title": "Datei:Algebraische Kurven (Osnabrück 2012)Arbeitsblatt29.pdf",
        "file_pageid": 54374,
        "file_revid": 325018,
        "file_parentid": 322184,
        "file_timestamp": "2012-07-31T14:08:29Z",
        "file_sha1": "290ec63705242e2b8dccf596ed48a8d1adac9880",
        "source_timestamp": "2012-07-31T14:08:29Z",
        "source_bytes": 81522,
        "source_sha1": "6a783df1c478e4644df12cbbe8db164d9f84076a",
        "local_sha256": "83986d2a9928c6e61ad7afa6d5a890e2b296c15a8706931c8c6da485b05079d2",
        "page_count": 3,
    },
}
EXPECTED_LIVE_UNION = 150
EXPECTED_ROOT_CONTRIBUTORS = {"lecture": "Bocardodarapti", "worksheet": "Arbota"}
SOURCE_DEFECT_BINDINGS = [
    {
        "id": "AGC-U29-SRC-001",
        "surface": "lecture current semantic source / expanded TeX",
        "source_text": "Bei g >= 3 ist die Multiplizität >= 2",
        "issue": "The proof of the degree-d graph theorem switches from d to an undefined g in its final singularity criterion.",
        "reader_handling": "Render d >= 3, label the correction visibly, and retain this exact source binding.",
    },
    {
        "id": "AGC-U29-SRC-002",
        "surface": "worksheet Exercise 7 current semantic source / expanded TeX",
        "source_text": "durch die Matrix [blank] ... (x_0,...,x_n) maps to (x_0,...,x_n)",
        "issue": "The requested projection matrix is blank and the displayed map repeats the input vector instead of giving the projection.",
        "reader_handling": "Preserve the unresolved source surface and disclose it; do not invent a matrix or silently repair the exercise.",
    },
]''',
)

for old, new in (
    ('require(len(entries) == 14, "Unit 29 must retain exactly fourteen ordered exercises")',
     'require(len(entries) == 10, "Unit 29 must retain exactly ten ordered exercises")'),
    ('list(range(1, 15))', 'list(range(1, 11))'),
    ('role = "warm-up" if number <= 10 else "submitted"',
     'role = "warm-up" if number <= 5 else "submitted"'),
    ('"points_displayed_in_worksheet": number >= 11,',
     '"points_displayed_in_worksheet": number >= 6,'),
    ('"starred_in_worksheet": number == 10,',
     '"starred_in_worksheet": number in {2, 3},'),
    ('require(len(toc_lines) == 14, "worksheet TOC exercise count")',
     'require(len(toc_lines) == 10, "worksheet TOC exercise count")'),
    ('require([i + 1 for i, line in enumerate(toc_lines) if "*" in line] == [10], "star topology")',
     'require([i + 1 for i, line in enumerate(toc_lines) if "*" in line] == [2, 3], "star topology")'),
    ('require(len(candidate_pages) == 14, "candidate query must return exactly fourteen page records")',
     'require(len(candidate_pages) == 10, "candidate query must return exactly ten page records")'),
    ('"warm_up_numbers": list(range(1, 11)),',
     '"warm_up_numbers": list(range(1, 6)),'),
    ('"submitted_numbers": list(range(11, 15)),',
     '"submitted_numbers": list(range(6, 11)),'),
    ('"starred_numbers": [10],',
     '"starred_numbers": [2, 3],'),
    ('"exact_candidate_title_count": 14,',
     '"exact_candidate_title_count": 10,'),
    ('require(solutions["exercise_count"] == 14, "exercise count")',
     'require(solutions["exercise_count"] == 10, "exercise count")'),
    ('require(media_closure["reader_media_positions"] == 4 and len(media_closure["assets"]) == 4, "media replay")',
     'require(media_closure["reader_media_positions"] == 2 and len(media_closure["assets"]) == 2, "media replay")'),
    ('require(rev["user"] == EXPECTED_ROOT_CONTRIBUTOR, f"{kind} root contributor drift")',
     'require(rev["user"] == EXPECTED_ROOT_CONTRIBUTORS[kind], f"{kind} root contributor drift")'),
    ('text = (OUT / "lecture-29-expanded.tex").read_text(encoding="utf-8")',
     'text = (OUT / "worksheet-29-expanded.tex").read_text(encoding="utf-8")'),
):
    generated = replace_once(generated, old, new)

generated = replace_section(
    generated,
    "def verify_source_defects() -> list[dict]:",
    "def official_pdfs_and_media(",
    r'''def verify_source_defects() -> list[dict]:
    lecture_tex = (OUT / "lecture-29-expanded.tex").read_text(encoding="utf-8")
    worksheet_tex = (OUT / "worksheet-29-expanded.tex").read_text(encoding="utf-8")
    require(
        re.search(r"\{\s*g\s*\}\s*\{\s*\\geq\s*\}\{\s*3", lecture_tex) is not None,
        "degree-variable source defect evidence",
    )
    require(
        "durch die Matrix" in worksheet_tex and r"\mathdisp {} {  }" in worksheet_tex,
        "blank projection-matrix source defect evidence",
    )
    require(
        worksheet_tex.count(r"\begin{pmatrix}  x_0") >= 2,
        "identity projection-map source defect evidence",
    )
    return SOURCE_DEFECT_BINDINGS''',
)

generated = replace_once(
    generated,
    '        desc_content = desc_rev["slots"]["main"]["content"]',
    '''        desc_content = desc_rev["slots"]["main"]["content"]
        if name == "Lemniscate_of_Bernoulli.svg":
            require("PD-ineligible" in desc_content, "Lemniscate public-domain evidence")
        if name == "Tschirnhausen_cubic.png":
            require(
                "Despite the title this is not the" in desc_content,
                "Tschirnhausen description discrepancy evidence",
            )''',
)

generated = replace_section(
    generated,
    '        "component_discrepancies": {',
    '        "assets": asset_records,',
    '''        "component_discrepancies": {
            "static_pdf_versus_semantic_revision_boundary": (
                "The official PDFs are unchanged 2012 static witnesses. They are not asserted to be renders "
                "of the frozen 2026 lecture or 2025 worksheet semantic revisions; the expanded TeX captures "
                "are separately byte-bound dynamic surfaces."
            ),
            "dual_pdf_file_page_license_notices": (
                "Each local file page identifies the generated print version with the current "
                "CC BY-SA 4.0 route while retaining the legacy CC BY-SA 2.0 Germany file notice."
            ),
            "media_semantic_description": [
                {
                    "source_parser_name": "Tschirnhausen_cubic.png",
                    "course_caption": "Die Tschirnhausen Kubik",
                    "current_commons_description": (
                        "The Commons description explicitly says that, despite its title, the image is not "
                        "the Tschirnhausen cubic because the double-point crossing angle differs."
                    ),
                    "handling": (
                        "Preserve the exact source-used public-domain component and disclose the current "
                        "Commons identification warning; do not present the picture as mathematically authoritative."
                    ),
                },
                {
                    "source_parser_name": "Lemniscate_of_Bernoulli.svg",
                    "course_embedded_user": "Zorgit",
                    "current_commons_artist": "Zorgit",
                    "current_file_uploader": "Georg-Johann",
                    "handling": "Keep artist and upload-revision provenance as distinct fields.",
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
    contributors = {
        row["kind"]: row["revision_contributor"]
        for row in manifest["root_revision_contributors"]["records"]
    }
    lines = [
        "# Unit 29 authority freeze",
        "",
        f"Frozen at {manifest['frozen_utc']} from the official German Wikiversity course {COURSE}. This is an authority boundary, not an Indonesian translation checkpoint.",
        "",
        "## Exact source boundary",
        "",
        f"- Course route: pageid {manifest['source_course_surface']['pageid']}, revid {manifest['source_course_surface']['revid']}.",
        f"- Lecture: pageid {manifest['lecture']['pageid']}, revid {manifest['lecture']['revid']}, MediaWiki SHA-1 {manifest['lecture']['mediawiki_sha1']}.",
        f"- Worksheet: pageid {manifest['worksheet']['pageid']}, revid {manifest['worksheet']['revid']}, MediaWiki SHA-1 {manifest['worksheet']['mediawiki_sha1']}.",
        "- Topic boundary: Projektion weg von einem Punkt; Abbildungen nach P^1_K; "
        "Parametrisierte projektive ebene Kurven; Monomiale projektive Kurven.",
        f"- Lecture closure: {lecture_topology['with_root']} identities; SHA-256 {lecture_topology['canonical_identity_rows_sha256']}.",
        f"- Worksheet closure: {worksheet_topology['with_root']} identities; SHA-256 {worksheet_topology['canonical_identity_rows_sha256']}.",
        f"- Course author: Holger Brenner. Root-revision contributors: lecture {contributors['lecture']}; worksheet {contributors['worksheet']} (revision provenance, not course authorship).",
        "- Both /latex revisions contain only {{Latex}}. Expanded TeX files are byte-bound dynamic captures, not immutable standalone source revisions.",
        "",
        "## Exercises and solutions",
        "",
        f"Exactly 10 exercises are preserved in order: warm-up 1-5 and submitted 6-10. Exercises 2 and 3 carry source stars. Submitted displayed points are 3, 3, 3, 3, 5 ({roles['submitted_displayed_point_total']} total); there is no upload exercise.",
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
        "The parser exposes two substantive reader-media positions and exactly two official PDFs. Every original, description revision, creator/uploader field, component license, byte count, and hash is bound in RIGHTS-unit-29.csv and ASSET_CLOSURE-unit-29.json.",
        "Both figures are public-domain components. The Commons description warns that Tschirnhausen_cubic.png is not actually the named curve; preserve the source-used image but disclose that warning and do not treat it as mathematical authority.",
        f"- Lecture PDF: {pdfs['lecture']['local_bytes']} bytes, {pdfs['lecture']['page_count']} pages, SHA-256 {pdfs['lecture']['local_sha256']}.",
        f"- Worksheet PDF: {pdfs['worksheet']['local_bytes']} bytes, {pdfs['worksheet']['page_count']} pages, SHA-256 {pdfs['worksheet']['local_sha256']}.",
        "The official PDFs are static 2012 witnesses. Preserve both the current CC BY-SA 4.0 print/course route and legacy CC BY-SA 2.0 Germany file notice; make no blanket mixed-set claim.",
        "",
        "## Replay boundary",
        "",
        f"Final live replay passed for {manifest['final_live_identity_replay']['semantic_unique_identity_count']} unique Wikiversity semantic identities, both local Wikiversity PDF identities, and {manifest['final_live_identity_replay']['commons_media_identity_count']} Commons media identities.",
        f"Manifest: {manifest_path.relative_to(ROOT).as_posix()}; {manifest_path.stat().st_size} bytes; SHA-256 {base.digest(manifest_path)}.",
        "",
    ])
    FREEZE_NOTE.write_text("\\n".join(lines), encoding="utf-8", newline="\\n")''',
)

for residue in (
    "Unit 28",
    "unit-28",
    "UNIT_28",
    "AGC-U28",
    "br-ak-u28",
    "lecture-28",
    "worksheet-28",
    "Vorlesung28",
    "Arbeitsblatt28",
):
    if residue in generated:
        raise SystemExit(f"Unit 28 residue survived Unit 29 specialization: {residue}")

generated = replace_section(
    generated,
    '        local_name = urllib.parse.unquote(Path(urllib.parse.urlparse(info["url"]).path).name)',
    '        metadata = info.get("extmetadata", {})',
    '''        original_local_name = urllib.parse.unquote(
            Path(urllib.parse.urlparse(info["url"]).path).name
        )
        original_local = asset_dir / original_local_name
        selected_local_name = original_local_name
        selected_url = info["url"].split("?", 1)[0]
        selected_form = "original"
        original_locally_archived = False
        if (
            original_local.is_file()
            and original_local.stat().st_size == int(info["size"])
            and base.digest(original_local, "sha1") == info["sha1"]
        ):
            data = original_local.read_bytes()
            original_locally_archived = True
        elif name == "Tschirnhausen_cubic.png":
            # Wikimedia's original-file endpoint returned HTTP 429 and explicitly
            # requested use of a listed thumbnail. Freeze one exact official
            # derivative while retaining the original identity separately.
            selected_local_name = "Tschirnhausen_cubic-500.png"
            selected_url = (
                "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/"
                "Tschirnhausen_cubic.png/500px-Tschirnhausen_cubic.png"
            )
            selected_form = "thumbnail_500px"
            shared_candidate = SHARED_ASSETS / selected_local_name
            if (
                shared_candidate.is_file()
                and shared_candidate.stat().st_size == 83502
                and base.digest(shared_candidate)
                == "f3dda9da65db9e431f25ea77eb83f51aed2eff1c191dc1206e0759561ee613c7"
            ):
                data = shared_candidate.read_bytes()
            else:
                data = base.fetch(selected_url)
            require(len(data) == 83502, "Tschirnhausen selected-thumbnail byte count")
            require(
                base.digest_bytes(data)
                == "f3dda9da65db9e431f25ea77eb83f51aed2eff1c191dc1206e0759561ee613c7",
                "Tschirnhausen selected-thumbnail SHA-256",
            )
        else:
            data = base.fetch(info["url"])
            require(len(data) == int(info["size"]), f"Commons byte count: {name}")
            require(base.digest_bytes(data, "sha1") == info["sha1"], f"Commons SHA-1: {name}")
            original_locally_archived = True
        local = asset_dir / selected_local_name
        if not local.is_file() or local.read_bytes() != data:
            base.write_bytes(local, data)
        if selected_form == "original":
            require(len(data) == int(info["size"]), f"Commons byte count: {name}")
            require(base.digest_bytes(data, "sha1") == info["sha1"], f"Commons SHA-1: {name}")
        if info["mime"] == "image/svg+xml" and selected_form == "original":
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
                frames = int(getattr(image, "n_frames", 1))
        expected_dimensions = (
            (int(info["width"]), int(info["height"]))
            if selected_form == "original"
            else (500, 745)
        )
        require((width, height) == expected_dimensions, f"selected media dimensions: {name}")
        shared = SHARED_ASSETS / selected_local_name
        if shared.is_file():
            require(
                shared.stat().st_size == local.stat().st_size and base.digest(shared) == base.digest(local),
                f"shared reader asset collision: {shared}",
            )
        else:
            base.write_bytes(shared, data)''',
)

for old, new in (
    ('            "selected_url": info["url"].split("?", 1)[0],',
     '            "selected_url": selected_url,'),
    ('            "selected_form": "original",',
     '            "selected_form": selected_form,'),
    ('            "source_url": row["original_url"],',
     '            "source_url": row["original_url"],\n                "selected_url": row["selected_url"],\n                "selected_form": row["selected_form"],\n                "original_locally_archived": row["original_locally_archived"],'),
    ('            "original_bytes": int(info["size"]),',
     '            "original_locally_archived": original_locally_archived,\n            "original_bytes": int(info["size"]),'),
):
    generated = replace_once(generated, old, new)

generated = replace_once(
    generated,
    '                "original_locally_archived": row["original_locally_archived"],\n                "local_path": row["local_path"],',
    '                "original_locally_archived": row["original_locally_archived"],\n                "original_bytes": row["original_bytes"],\n                "original_sha1": row["original_sha1"],\n                "original_width": row["original_width"],\n                "original_height": row["original_height"],\n                "local_path": row["local_path"],',
)

generated = replace_once(
    generated,
    '            "dual_pdf_file_page_license_notices": (',
    '''            "original_media_retrieval": {
                "source_parser_name": "Tschirnhausen_cubic.png",
                "original_identity_status": "metadata-bound from the frozen Commons description/imageinfo revision",
                "original_local_archive_status": "not archived at this boundary after the canonical original endpoint returned HTTP 429",
                "selected_reader_derivative": "official Wikimedia 500px thumbnail, byte-bound in the asset records",
                "retry_policy": "retry the original only after external service state changes; this is not a publication or translation hold",
            },
            "dual_pdf_file_page_license_notices": (''',
)

generated = replace_once(
    generated,
    '        "Both figures are public-domain components. The Commons description warns that Tschirnhausen_cubic.png is not actually the named curve; preserve the source-used image but disclose that warning and do not treat it as mathematical authority.",',
    '        "Both figures are public-domain components. The Commons description warns that Tschirnhausen_cubic.png is not actually the named curve; disclose that warning and do not treat the picture as mathematical authority.",\n        "The Tschirnhausen original identity remains frozen from Commons metadata. Because the canonical original endpoint returned HTTP 429, this boundary selects the exact official 500px Wikimedia thumbnail (83,502 bytes; 500x745) and does not falsely claim that the original bytes were locally archived.",',
)

compile(generated, str(Path(__file__).resolve()), "exec")
if sys.argv[1:] == ["--self-check"]:
    print(
        json.dumps(
            {
                "status": "PASS",
                "mode": "offline_specialization_compile",
                "template": UNIT28_WRAPPER.relative_to(ROOT).as_posix(),
                "template_sha256": UNIT28_WRAPPER_SHA256,
                "generated_bytes": len(generated.encode("utf-8")),
                "generated_sha256": hashlib.sha256(generated.encode("utf-8")).hexdigest(),
                "network_called": False,
                "files_written": False,
            },
            indent=2,
        )
    )
else:
    namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
    exec(compile(generated, str(Path(__file__).resolve()), "exec"), namespace)
