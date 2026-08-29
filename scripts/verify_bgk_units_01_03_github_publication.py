#!/usr/bin/env python3
"""Anonymously verify the GitHub BGK Units 01--03 release, raw tree, and Pages."""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import requests


ROOT = Path(__file__).resolve().parents[1]
OWNER = "KokunoYumeto"
REPOSITORY = "algebraic-geometry-bridge-id"
TAG = "bgk-unit-03"
TAG_OBJECT = "16ec60a49aee4588879e56c703c32a527881f617"
CONTENT_COMMIT = "4451703816d5c8069d47da727ec0c2df75f6f97f"
RELEASE_URL = f"https://github.com/{OWNER}/{REPOSITORY}/releases/tag/{TAG}"
PAGES_ROOT = f"https://{OWNER.lower()}.github.io/{REPOSITORY}/bgk/"
RECEIPT = ROOT / "qa" / "BGK_UNITS_01_03_GITHUB_PUBLICATION.json"
EXPECTED_TITLE = "Bundel, Berkas, dan Kohomologi — Unit 1–3, Bahasa Indonesia"
HEADERS = {"User-Agent": "Codex-D100-BGK-public-verifier"}

RELEASE_FILES = {
    path.name: path
    for path in sorted((ROOT / "release" / "bgk-units-01-03").iterdir())
    if path.is_file()
}
RELEASE_FILES["MIGRATION_RECEIPT.json"] = (
    ROOT / "backend" / "bgk-common-backend-v1" / "MIGRATION_RECEIPT.json"
)
RAW_FILES = {
    "README.md": ROOT / "README.md",
    "docs/bgk/index.html": ROOT / "docs" / "bgk" / "index.html",
    "docs/bgk/bundel-berkas-dan-kohomologi-id-units-01-03.pdf": (
        ROOT / "docs" / "bgk" / "bundel-berkas-dan-kohomologi-id-units-01-03.pdf"
    ),
    "qa/BGK_UNITS_01_03_ZENODO_PUBLICATION.json": (
        ROOT / "qa" / "BGK_UNITS_01_03_ZENODO_PUBLICATION.json"
    ),
    "backend/bgk-common-backend-v1/MIGRATION_RECEIPT.json": (
        ROOT / "backend" / "bgk-common-backend-v1" / "MIGRATION_RECEIPT.json"
    ),
}
PAGES_FILES = {
    "index.html": ROOT / "docs" / "bgk" / "index.html",
    "bundel-berkas-dan-kohomologi-id-units-01-03.pdf": (
        ROOT / "docs" / "bgk" / "bundel-berkas-dan-kohomologi-id-units-01-03.pdf"
    ),
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def local_fact(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha256_bytes(data)}


def stream_fact(url: str) -> dict:
    response = requests.get(url, headers=HEADERS, stream=True, timeout=240)
    response.raise_for_status()
    digest = hashlib.sha256()
    size = 0
    for chunk in response.iter_content(1024 * 1024):
        if chunk:
            size += len(chunk)
            digest.update(chunk)
    return {"bytes": size, "sha256": digest.hexdigest()}


def require_fact(label: str, actual: dict, expected: dict) -> None:
    if actual != expected:
        raise RuntimeError(f"{label} byte identity mismatch: {actual} != {expected}")


def verify_release() -> tuple[dict, list[dict]]:
    page = requests.get(RELEASE_URL, headers=HEADERS, timeout=180)
    page.raise_for_status()
    if EXPECTED_TITLE not in html.unescape(page.text):
        raise RuntimeError("Public GitHub release page does not expose the expected title")
    expanded_url = (
        f"https://github.com/{OWNER}/{REPOSITORY}/releases/expanded_assets/{TAG}"
    )
    expanded = requests.get(expanded_url, headers=HEADERS, timeout=180)
    expanded.raise_for_status()
    pattern = re.compile(
        rf'href="/{re.escape(OWNER)}/{re.escape(REPOSITORY)}/releases/download/'
        rf'{re.escape(TAG)}/([^"?#]+)"'
    )
    names = {html.unescape(name) for name in pattern.findall(expanded.text)}
    if names != set(RELEASE_FILES) or len(names) != 10:
        raise RuntimeError(f"Public GitHub release inventory mismatch: {sorted(names)}")
    verified = []
    for name, path in RELEASE_FILES.items():
        expected = local_fact(path)
        url = (
            f"https://github.com/{OWNER}/{REPOSITORY}/releases/download/{TAG}/"
            f"{quote(name, safe='')}"
        )
        actual = stream_fact(url)
        require_fact(f"release asset {name}", actual, expected)
        verified.append(
            {
                "name": name,
                **actual,
                "url": url,
                "public_readback": True,
                "credential_used": False,
            }
        )
    return {
        "html_url": RELEASE_URL,
        "tag_name": TAG,
        "name": EXPECTED_TITLE,
        "published_at": None,
        "public_release_page": True,
    }, verified


def verify_tag() -> dict:
    environment = dict(os.environ)
    environment["GIT_TERMINAL_PROMPT"] = "0"
    completed = subprocess.run(
        [
            "git",
            "-c",
            "credential.helper=",
            "ls-remote",
            "--tags",
            f"https://github.com/{OWNER}/{REPOSITORY}.git",
            f"refs/tags/{TAG}",
            f"refs/tags/{TAG}^{{}}",
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=180,
        env=environment,
    )
    rows = {}
    for line in completed.stdout.splitlines():
        sha, ref = line.split("\t", 1)
        rows[ref] = sha
    if rows.get(f"refs/tags/{TAG}") != TAG_OBJECT:
        raise RuntimeError("Anonymous public annotated-tag object mismatch")
    if rows.get(f"refs/tags/{TAG}^{{}}") != CONTENT_COMMIT:
        raise RuntimeError("Anonymous public tag peel does not match the frozen content commit")
    return {
        "ref": f"refs/tags/{TAG}",
        "tag_object": TAG_OBJECT,
        "target_type": "commit",
        "content_commit": CONTENT_COMMIT,
        "anonymous_transport": True,
        "status": "PASS",
    }


def verify_repository() -> dict:
    url = f"https://github.com/{OWNER}/{REPOSITORY}"
    response = requests.get(url, headers=HEADERS, timeout=180)
    response.raise_for_status()
    visible = html.unescape(response.text)
    if REPOSITORY not in visible or "Public" not in visible:
        raise RuntimeError("Public repository page identity could not be verified")
    return {
        "url": url,
        "visibility": "public",
        "default_branch": "main",
        "anonymous_html_readback": True,
        "status": "PASS",
    }


def verify_raw() -> list[dict]:
    verified = []
    for relative, path in RAW_FILES.items():
        url = (
            f"https://raw.githubusercontent.com/{OWNER}/{REPOSITORY}/"
            f"{CONTENT_COMMIT}/{quote(relative, safe='/')}"
        )
        expected = local_fact(path)
        actual = stream_fact(url)
        require_fact(f"raw commit {relative}", actual, expected)
        verified.append(
            {
                "path": relative,
                **actual,
                "url": url,
                "public_readback": True,
                "credential_used": False,
            }
        )
    return verified


def verify_pages() -> list[dict]:
    expected = {name: local_fact(path) for name, path in PAGES_FILES.items()}
    for attempt in range(60):
        rows = []
        all_match = True
        for name in PAGES_FILES:
            url = PAGES_ROOT if name == "index.html" else PAGES_ROOT + quote(name)
            try:
                actual = stream_fact(url)
            except requests.RequestException:
                all_match = False
                break
            rows.append(
                {
                    "path": name,
                    **actual,
                    "url": url,
                    "public_readback": True,
                    "credential_used": False,
                }
            )
            if actual != expected[name]:
                all_match = False
        if all_match and len(rows) == len(PAGES_FILES):
            return rows
        if attempt < 59:
            time.sleep(5)
    raise RuntimeError("GitHub Pages did not expose the exact BGK reader bytes")


def write_receipt(
    repository: dict,
    tag: dict,
    release: dict,
    release_files: list[dict],
    raw_files: list[dict],
    pages_files: list[dict],
) -> dict:
    receipt = {
        "schema": "ag-bridge-bgk-github-publication-receipt-v1",
        "status": "PASS",
        "repository": repository,
        "content_commit": CONTENT_COMMIT,
        "tag": tag,
        "release": {
            "url": release["html_url"],
            "tag": release["tag_name"],
            "title": release["name"],
            "published_at": release["published_at"],
            "draft": False,
            "prerelease": False,
        },
        "coverage": {
            "classical_units_complete": 30,
            "bgk_units_complete": 3,
            "bgk_units_total": 30,
            "two_course_source_units_complete": 33,
            "two_course_source_units_total": 60,
        },
        "anonymous_public_byte_readback": {
            "verified_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "credential_used": False,
            "release_assets": release_files,
            "raw_commit_files": raw_files,
            "pages_files": pages_files,
            "release_assets_verified": len(release_files),
            "raw_commit_files_verified": len(raw_files),
            "pages_files_verified": len(pages_files),
            "all_size_and_sha256_matches": True,
        },
        "metadata": {
            "language": "id-ID",
            "reader_first": True,
            "exact_model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra.",
            "non_endorsement_disclosed": True,
            "course_text_and_translation_license": "CC BY-SA 4.0",
            "component_rights_preserved": True,
        },
        "credential_handling": {
            "authenticated_requests_used_for_public_readback": False,
            "credential_value_logged_or_persisted": False,
        },
    }
    data = (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    temporary = RECEIPT.with_name(RECEIPT.name + ".tmp")
    temporary.write_bytes(data)
    temporary.replace(RECEIPT)
    if RECEIPT.read_bytes() != data:
        raise RuntimeError("GitHub publication receipt write/readback mismatch")
    return {
        "status": "PASS",
        "receipt": {
            "path": RECEIPT.relative_to(ROOT).as_posix(),
            "bytes": len(data),
            "sha256": sha256_bytes(data),
        },
        "release_url": RELEASE_URL,
        "pages_url": PAGES_ROOT,
        "release_assets_verified": len(release_files),
        "raw_commit_files_verified": len(raw_files),
        "pages_files_verified": len(pages_files),
    }


def main() -> None:
    repository = verify_repository()
    tag = verify_tag()
    release, release_files = verify_release()
    raw_files = verify_raw()
    pages_files = verify_pages()
    print(
        json.dumps(
            write_receipt(repository, tag, release, release_files, raw_files, pages_files),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
