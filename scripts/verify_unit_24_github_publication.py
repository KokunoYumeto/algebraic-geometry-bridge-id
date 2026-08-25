#!/usr/bin/env python3
"""Anonymously verify and receipt the cumulative Unit 24 GitHub publication.

The verifier is specialized from the byte-pinned, accepted Unit 21 verifier.
It loads the generated release manifest and local release bytes at runtime, and
binds the commit from the public main branch plus annotated Unit 24 tag (or an
optional caller-supplied commit) instead of embedding a not-yet-created hash.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "verify_unit_21_github_publication.py"
TEMPLATE_SHA256 = "d7c6c65a43ec01acbbb4af7a0545c9297d31628893b4feb1a76ae55ffde94228"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Unit 24 GitHub specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


def materialize_unit21_implementation() -> str:
    """Materialize the accepted Unit 21 verifier without running it."""

    if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
        raise SystemExit("Accepted Unit 21 GitHub verifier is absent or has drifted")
    source = TEMPLATE.read_text(encoding="utf-8")
    marker = '\nnamespace = {"__file__":'
    if source.count(marker) != 1:
        raise SystemExit("Could not isolate the accepted Unit 21 GitHub builder")
    builder = source[: source.index(marker)]
    namespace = {"__file__": str(TEMPLATE), "__name__": "unit21_builder_capture"}
    exec(compile(builder, str(TEMPLATE), "exec"), namespace)
    generated = namespace.get("generated")
    if not isinstance(generated, str):
        raise SystemExit("Accepted Unit 21 GitHub builder yielded no implementation")
    return generated


generated = materialize_unit21_implementation()
for old, new in (
    ("units-01-21", "units-01-24"),
    ("UNIT_21", "UNIT_24"),
    ("unit-21", "unit-24"),
    ("unit_21", "unit_24"),
    ("unit21", "unit24"),
    ("Unit 21", "Unit 24"),
):
    generated = generated.replace(old, new)

generated = replace_once(
    generated,
    'EXPECTED_COMMIT = "5304877a495b39bba9f9d681b086139ba3bd2f4e"',
    'MANIFEST_NAME = "ZENODO_FILE_MANIFEST-unit-24.json"',
)

generated = replace_once(
    generated,
    """def local_descriptor(name: str) -> dict[str, object]:
    path = RELEASE_DIR / name
    if not path.is_file():
        raise FileNotFoundError(path)
    return {"name": name, "bytes": path.stat().st_size, "sha256": sha256(path)}""",
    """def local_descriptor(name: str) -> dict[str, object]:
    path = RELEASE_DIR / name
    if not path.is_file():
        raise FileNotFoundError(path)
    return {"name": name, "bytes": path.stat().st_size, "sha256": sha256(path)}


def load_release_contract() -> tuple[dict[str, dict[str, object]], dict]:
    path = RELEASE_DIR / MANIFEST_NAME
    if not path.is_file():
        raise FileNotFoundError(path)
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Invalid Unit 24 release manifest: {exc}") from exc
    if not isinstance(manifest, dict):
        raise RuntimeError("Unit 24 release manifest must contain an object")
    if manifest.get("schema") != "ag-bridge-release-file-manifest-v2":
        raise RuntimeError("Unexpected Unit 24 release-manifest schema")
    if manifest.get("version") != "unit-24" or manifest.get("language") != "id-ID":
        raise RuntimeError("Unit 24 release-manifest identity mismatch")
    coverage = manifest.get("coverage")
    if not isinstance(coverage, dict) or coverage.get("through_unit") != 24:
        raise RuntimeError("Unit 24 release-manifest coverage mismatch")
    if coverage.get("planned_units") != 30 or coverage.get("full_edition_complete") is not False:
        raise RuntimeError("Unit 24 release must remain a truthful partial 24/30 checkpoint")
    rights = manifest.get("rights")
    if not isinstance(rights, dict):
        raise RuntimeError("Unit 24 release-manifest rights are missing")
    if rights.get("translated_text") != "CC BY-SA 4.0":
        raise RuntimeError("Unit 24 translated-text licence mismatch")
    if rights.get("blanket_payload_license_claimed") is not False:
        raise RuntimeError("Unit 24 release makes an impermissible blanket licence claim")
    if rights.get("source_course_boundary") != {
        "units_01_23": "Algebraische Kurven (Osnabrück 2025–2026)",
        "unit_24": "Algebraische Kurven (Osnabrück 2012)",
    }:
        raise RuntimeError("Unit 24 source-course transition is missing or incorrect")
    if rights.get("unit_24_pdf_component_notices") != [
        "CC BY-SA 4.0 course route",
        "CC BY-SA 2.0 Germany file notice",
    ]:
        raise RuntimeError("Unit 24 PDF component-rights notices are missing")

    zenodo_section = manifest.get("zenodo")
    if not isinstance(zenodo_section, dict):
        raise RuntimeError("Unit 24 release-manifest publication section is missing")
    if zenodo_section.get("reader_first") != FILES[0]:
        raise RuntimeError("Unit 24 release manifest is not reader-first")
    bound = zenodo_section.get("files_excluding_this_manifest")
    if not isinstance(bound, list):
        raise RuntimeError("Unit 24 release-manifest file bindings are missing")
    expected_bound_names = [name for name in FILES if name != MANIFEST_NAME]
    bound_names = [item.get("name") for item in bound if isinstance(item, dict)]
    if bound_names != expected_bound_names:
        raise RuntimeError("Unit 24 release-manifest file order mismatch")

    expected = {name: local_descriptor(name) for name in FILES}
    for index, name in enumerate(expected_bound_names):
        item = bound[index]
        if item.get("bytes") != expected[name]["bytes"] or item.get("sha256") != expected[name]["sha256"]:
            raise RuntimeError(f"Unit 24 release-manifest binding mismatch: {name}")
    return expected, manifest""",
)

generated = replace_once(
    generated,
    "def verify(wait_seconds: int) -> dict[str, object]:\n"
    "    expected = {name: local_descriptor(name) for name in FILES}",
    "def verify(wait_seconds: int, expected_commit: str | None = None) -> dict[str, object]:\n"
    "    expected, release_manifest = load_release_contract()",
)
generated = replace_once(
    generated,
    """    branch_commit = branch["commit"]["sha"]
    if branch_commit != EXPECTED_COMMIT:
        raise RuntimeError(f"Unexpected public main commit: {branch_commit}")""",
    """    branch_commit = branch["commit"]["sha"]
    if (
        not isinstance(branch_commit, str)
        or len(branch_commit) != 40
        or any(character not in "0123456789abcdef" for character in branch_commit)
    ):
        raise RuntimeError(f"Invalid public main commit identity: {branch_commit!r}")
    if expected_commit is not None and branch_commit != expected_commit:
        raise RuntimeError(
            f"Public main commit differs from caller binding: {branch_commit} != {expected_commit}"
        )""",
)
generated = generated.replace("EXPECTED_COMMIT", "branch_commit")

generated = replace_once(
    generated,
    '        "repository": f"https://github.com/{OWNER}/{REPOSITORY}",',
    '        "repository": f"https://github.com/{OWNER}/{REPOSITORY}",\n'
    '        "release_manifest": {\n'
    '            **local_descriptor(MANIFEST_NAME),\n'
    '            "through_unit": release_manifest["coverage"]["through_unit"],\n'
    '            "planned_units": release_manifest["coverage"]["planned_units"],\n'
    '            "full_edition_complete": release_manifest["coverage"]["full_edition_complete"],\n'
    '            "source_course_boundary": release_manifest["rights"]["source_course_boundary"],\n'
    '        },',
)

generated = replace_once(
    generated,
    '    parser.add_argument("--wait-seconds", type=int, default=300)\n'
    '    args = parser.parse_args()\n'
    '    result = verify(args.wait_seconds)',
    '    parser.add_argument("--wait-seconds", type=int, default=300)\n'
    '    parser.add_argument("--expected-commit")\n'
    '    args = parser.parse_args()\n'
    '    result = verify(args.wait_seconds, args.expected_commit)',
)

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE), "exec"), namespace)
