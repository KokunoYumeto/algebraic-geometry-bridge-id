#!/usr/bin/env python3
"""Anonymously verify the BGK Units 01--06 GitHub release, tree, and Pages.

The annotated-tag object and peeled content commit are mandatory command-line
inputs because those identities do not exist until the owner publishes the
verified boundary.  The verifier uses only anonymous GitHub HTTP APIs/raw
downloads (no Git command and no credential), streams every release asset,
checks selected raw files at the exact commit, polls Pages for exact bytes, and
writes a sanitized receipt only after complete byte identity succeeds.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, unquote

import requests


ROOT = Path(__file__).resolve().parents[1]
OWNER = "KokunoYumeto"
REPOSITORY = "algebraic-geometry-bridge-id"
TAG = "bgk-unit-06"
EXPECTED_TITLE = "Bundel, Berkas, dan Kohomologi — Unit 1–6, Bahasa Indonesia"
MODEL_PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."
RELEASE_DIR = ROOT / "release" / "bgk-units-01-06"
MIGRATION_RECEIPT = ROOT / "backend" / "bgk-common-backend-v1" / "MIGRATION_RECEIPT.json"
ZENODO_RECEIPT = ROOT / "qa" / "BGK_UNITS_01_06_ZENODO_PUBLICATION.json"
RECEIPT = ROOT / "qa" / "BGK_UNITS_01_06_GITHUB_PUBLICATION.json"
API = f"https://api.github.com/repos/{OWNER}/{REPOSITORY}"
WEB_ROOT = f"https://github.com/{OWNER}/{REPOSITORY}"
GIT_INFO_REFS = f"{WEB_ROOT}.git/info/refs?service=git-upload-pack"
RELEASE_URL = f"https://github.com/{OWNER}/{REPOSITORY}/releases/tag/{TAG}"
EXPANDED_ASSETS_URL = f"{WEB_ROOT}/releases/expanded_assets/{TAG}"
PAGES_ROOT = f"https://{OWNER.lower()}.github.io/{REPOSITORY}/bgk/"
HEADERS = {"User-Agent": "Codex-D100-BGK-Units-01-06-public-verifier"}

PACKAGE_NAMES = (
    "01_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-06.pdf",
    "02_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-06.html",
    "03_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-06_source.zip",
    "04_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-06_native-backend.zip",
    "05_LICENSE_AND_COMPONENT_RIGHTS.md",
    "06_README.md",
    "07_RELEASE_MANIFEST.json",
    "08_SHA256SUMS.txt",
    "09_RELEASE_CANDIDATE_QA.json",
)
MIGRATION_ASSET_NAME = "MIGRATION_RECEIPT.json"
PDF_DOC_NAME = "bundel-berkas-dan-kohomologi-id-units-01-06.pdf"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def local_fact(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise RuntimeError(f"Required local file missing: {path}")
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha256_bytes(data)}


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"Invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"Expected JSON object: {path}")
    return value


def require_sha(value: str, label: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", value):
        raise RuntimeError(f"{label} must be an exact lowercase 40-hex Git object ID")
    return value


def local_release_files() -> dict[str, Path]:
    actual = {path.name for path in RELEASE_DIR.iterdir() if path.is_file()} if RELEASE_DIR.is_dir() else set()
    if actual != set(PACKAGE_NAMES):
        raise RuntimeError(f"Units 01--06 release inventory mismatch: {sorted(actual)}")
    manifest = load_json(RELEASE_DIR / "07_RELEASE_MANIFEST.json")
    qa = load_json(RELEASE_DIR / "09_RELEASE_CANDIDATE_QA.json")
    if (
        manifest.get("status") != "partial_coherent_checkpoint"
        or manifest.get("included_units") != list(range(1, 7))
        or manifest.get("model_provenance") != MODEL_PROVENANCE
        or qa.get("status") != "PASS"
        or (qa.get("scope_truth") or {}).get("bgk_units_complete") != 6
        or qa.get("model_provenance") != MODEL_PROVENANCE
        or (qa.get("reader_first") or {}).get("lexicographically_first_file") != PACKAGE_NAMES[0]
    ):
        raise RuntimeError("Local release is not the verified Units 01--06 contract")
    gates = qa.get("exact_gate_hashes") or {}
    for key in ("reader_qa", "visual_qa", "backend_qa", "common_adapter_qa"):
        row = gates.get(key) or {}
        path = ROOT / str(row.get("path", ""))
        if not path.is_file() or local_fact(path) != {"bytes": row.get("bytes"), "sha256": row.get("sha256")}:
            raise RuntimeError(f"Exact local QA gate hash missing or drifted: {key}")
    files = {name: RELEASE_DIR / name for name in PACKAGE_NAMES}
    declared = {item.get("path"): item for item in manifest.get("files", [])}
    if set(declared) != set(PACKAGE_NAMES[:6]):
        raise RuntimeError("Release manifest payload inventory drifted")
    for name in declared:
        if local_fact(files[name]) != {"bytes": declared[name].get("bytes"), "sha256": declared[name].get("sha256")}:
            raise RuntimeError(f"Release manifest does not bind {name}")
    checksum_rows: dict[str, str] = {}
    for line in files["08_SHA256SUMS.txt"].read_text(encoding="ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\\/]+)", line)
        if not match or match.group(2) in checksum_rows:
            raise RuntimeError("Malformed or duplicate release checksum row")
        checksum_rows[match.group(2)] = match.group(1)
    expected_checksum_names = set(PACKAGE_NAMES) - {"08_SHA256SUMS.txt", "09_RELEASE_CANDIDATE_QA.json"}
    if set(checksum_rows) != expected_checksum_names:
        raise RuntimeError("Release checksum inventory drifted")
    for name, expected in checksum_rows.items():
        if local_fact(files[name])["sha256"] != expected:
            raise RuntimeError(f"Release checksum mismatch: {name}")
    return files


def validate_migration() -> None:
    receipt = load_json(MIGRATION_RECEIPT)
    source = receipt.get("source") or {}
    coverage = receipt.get("coverage") or {}
    validation = receipt.get("validation") or {}
    transformation = receipt.get("transformation") or {}
    if (
        receipt.get("schema_name") != "interlanguage-math-modular-backend-migration-receipt"
        or coverage.get("through_unit") != 6
        or source.get("through_unit") != 6
        or source.get("manifest", {}).get("path") != "backend/bgk-units-01-06/MANIFEST.json"
        or source.get("manifest", {}).get("sha256") != local_fact(ROOT / "backend" / "bgk-units-01-06" / "MANIFEST.json")["sha256"]
        or validation.get("result") != "pass"
        or validation.get("deterministic_double_replay") is not True
        or validation.get("lossless_native_reverse") is not True
        or transformation.get("model_provenance") != MODEL_PROVENANCE
        or receipt.get("credentials_recorded") is not False
    ):
        raise RuntimeError("Migration receipt is not the exact validated Units 01--06 adapter")


def validate_zenodo_receipt() -> None:
    receipt = load_json(ZENODO_RECEIPT)
    record = receipt.get("record") or {}
    readback = receipt.get("anonymous_public_byte_readback") or {}
    if (
        receipt.get("status") != "PASS"
        or record.get("concept_doi") != "10.5281/zenodo.22059686"
        or record.get("version") != "ak-unit-30+bgk-unit-06"
        or readback.get("credential_used") is not False
        or readback.get("files_expected") != 18
        or readback.get("files_verified") != 18
        or readback.get("all_size_and_sha256_matches") is not True
    ):
        raise RuntimeError("Zenodo receipt is not the complete Units 01--06 public readback")
    rows = {item.get("name"): item for item in readback.get("files", [])}
    expected_local = {name: RELEASE_DIR / name for name in PACKAGE_NAMES}
    expected_local["10_BGK_MIGRATION_RECEIPT.json"] = MIGRATION_RECEIPT
    for name, path in expected_local.items():
        item = rows.get(name) or {}
        if local_fact(path) != {"bytes": item.get("bytes"), "sha256": item.get("sha256")}:
            raise RuntimeError(f"Zenodo public receipt does not bind local release file: {name}")


class AnonymousApiRateLimited(RuntimeError):
    """The unauthenticated REST quota is exhausted; public web/Git remain usable."""


def api_get(url: str) -> dict:
    response = requests.get(url, headers=HEADERS, timeout=180)
    if response.status_code == 403 and response.headers.get("X-RateLimit-Remaining") == "0":
        raise AnonymousApiRateLimited("GitHub anonymous REST quota exhausted")
    response.raise_for_status()
    value = response.json()
    if not isinstance(value, dict):
        raise RuntimeError(f"Expected GitHub API object: {url}")
    return value


def public_get(url: str, *, headers: dict[str, str] | None = None) -> requests.Response:
    response = requests.get(url, headers=headers or HEADERS, timeout=180)
    response.raise_for_status()
    return response


def stream_fact(url: str) -> dict[str, object]:
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


def verify_repository() -> dict:
    try:
        value = api_get(API)
        if value.get("full_name") != f"{OWNER}/{REPOSITORY}" or value.get("private") is not False or value.get("visibility") != "public":
            raise RuntimeError("Public repository identity/visibility mismatch")
        return {
            "url": value["html_url"],
            "visibility": "public",
            "default_branch": value.get("default_branch"),
            "anonymous_api_readback": True,
            "status": "PASS",
        }
    except AnonymousApiRateLimited:
        page = public_get(WEB_ROOT).content.decode("utf-8")
        if (
            f'octolytics-dimension-repository_nwo" content="{OWNER}/{REPOSITORY}"' not in page
            or 'octolytics-dimension-repository_public" content="true"' not in page
        ):
            raise RuntimeError("Anonymous public repository page did not prove identity and visibility")
        return {
            "url": WEB_ROOT,
            "visibility": "public",
            "default_branch": "main",
            "anonymous_api_readback": False,
            "anonymous_public_web_readback": True,
            "api_fallback_reason": "anonymous_rest_quota_exhausted",
            "status": "PASS",
        }


def verify_tag(tag_object: str, content_commit: str) -> dict:
    try:
        ref = api_get(f"{API}/git/ref/tags/{quote(TAG, safe='')}")
        target = ref.get("object") or {}
        if target.get("type") != "tag" or target.get("sha") != tag_object:
            raise RuntimeError("Anonymous annotated-tag object mismatch")
        tag = api_get(f"{API}/git/tags/{tag_object}")
        peeled = tag.get("object") or {}
        if peeled.get("type") != "commit" or peeled.get("sha") != content_commit:
            raise RuntimeError("Anonymous tag peel does not match the frozen content commit")
        transport = {"anonymous_api_transport": True}
    except AnonymousApiRateLimited:
        response = public_get(GIT_INFO_REFS, headers={**HEADERS, "Git-Protocol": "version=1"})
        tag_ref = re.search(
            rb"([0-9a-f]{40}) refs/tags/" + re.escape(TAG.encode("ascii")) + rb"(?:\x00|[\r\n])",
            response.content,
        )
        peeled_ref = re.search(
            rb"([0-9a-f]{40}) refs/tags/" + re.escape((TAG + "^{}").encode("ascii")) + rb"(?:\x00|[\r\n])",
            response.content,
        )
        if not tag_ref or tag_ref.group(1).decode("ascii") != tag_object:
            raise RuntimeError("Anonymous Git smart-HTTP annotated-tag object mismatch")
        if not peeled_ref or peeled_ref.group(1).decode("ascii") != content_commit:
            raise RuntimeError("Anonymous Git smart-HTTP tag peel mismatch")
        transport = {
            "anonymous_api_transport": False,
            "anonymous_git_smart_http_transport": True,
            "api_fallback_reason": "anonymous_rest_quota_exhausted",
        }
    return {
        "ref": f"refs/tags/{TAG}",
        "tag_object": tag_object,
        "target_type": "commit",
        "content_commit": content_commit,
        **transport,
        "status": "PASS",
    }


def verify_release(release_files: dict[str, Path]) -> tuple[dict, list[dict]]:
    try:
        release = api_get(f"{API}/releases/tags/{quote(TAG, safe='')}")
        if (
            release.get("tag_name") != TAG
            or release.get("name") != EXPECTED_TITLE
            or release.get("draft") is not False
            or release.get("prerelease") is not False
        ):
            raise RuntimeError("Public GitHub release metadata mismatch")
        assets = {item.get("name"): item for item in release.get("assets", [])}
    except AnonymousApiRateLimited:
        page = public_get(RELEASE_URL).content.decode("utf-8")
        expanded = public_get(EXPANDED_ASSETS_URL).content.decode("utf-8")
        if EXPECTED_TITLE not in page or TAG not in page or "Pre-release" in page:
            raise RuntimeError("Anonymous public release page metadata mismatch")
        pattern = re.compile(
            rf"/{re.escape(OWNER)}/{re.escape(REPOSITORY)}/releases/download/{re.escape(TAG)}/([^\"?]+)"
        )
        names = [unquote(name) for name in pattern.findall(expanded)]
        if len(names) != len(set(names)):
            raise RuntimeError("Anonymous expanded release inventory contains duplicate assets")
        assets = {
            name: {
                "name": name,
                "browser_download_url": f"{WEB_ROOT}/releases/download/{TAG}/{quote(name)}",
            }
            for name in names
        }
        published = re.search(r'<relative-time[^>]+datetime="([^"]+)"', page)
        release = {
            "html_url": RELEASE_URL,
            "tag_name": TAG,
            "name": EXPECTED_TITLE,
            "draft": False,
            "prerelease": False,
            "published_at": published.group(1) if published else None,
            "anonymous_public_web_readback": True,
            "api_fallback_reason": "anonymous_rest_quota_exhausted",
        }
    if set(assets) != set(release_files) or len(assets) != 10:
        raise RuntimeError(f"Public GitHub release inventory mismatch: {sorted(assets)}")
    verified = []
    for name in sorted(release_files):
        expected = local_fact(release_files[name])
        url = assets[name]["browser_download_url"]
        actual = stream_fact(url)
        require_fact(f"release asset {name}", actual, expected)
        verified.append({"name": name, **actual, "url": url, "public_readback": True, "credential_used": False})
    return release, verified


def verify_raw(content_commit: str, raw_files: dict[str, Path]) -> list[dict]:
    verified = []
    for relative, path in raw_files.items():
        url = f"https://raw.githubusercontent.com/{OWNER}/{REPOSITORY}/{content_commit}/{quote(relative, safe='/')}"
        expected = local_fact(path)
        actual = stream_fact(url)
        require_fact(f"raw commit {relative}", actual, expected)
        verified.append({"path": relative, **actual, "url": url, "public_readback": True, "credential_used": False})
    return verified


def verify_pages(pages_files: dict[str, Path]) -> list[dict]:
    expected = {name: local_fact(path) for name, path in pages_files.items()}
    for attempt in range(60):
        rows = []
        all_match = True
        for name in pages_files:
            url = PAGES_ROOT if name == "index.html" else PAGES_ROOT + quote(name)
            try:
                actual = stream_fact(url)
            except requests.RequestException:
                all_match = False
                break
            rows.append({"path": name, **actual, "url": url, "public_readback": True, "credential_used": False})
            if actual != expected[name]:
                all_match = False
        if all_match and len(rows) == len(pages_files):
            return rows
        if attempt < 59:
            time.sleep(5)
    raise RuntimeError("GitHub Pages did not expose the exact Units 01--06 reader bytes")


def atomic_receipt(value: dict) -> dict:
    data = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    temporary = RECEIPT.with_name(RECEIPT.name + ".tmp")
    temporary.write_bytes(data)
    os.replace(temporary, RECEIPT)
    if RECEIPT.read_bytes() != data:
        raise RuntimeError("GitHub publication receipt write/readback mismatch")
    return {"path": RECEIPT.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha256_bytes(data)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag-object", required=True, help="exact lowercase 40-hex annotated-tag object")
    parser.add_argument("--content-commit", required=True, help="exact lowercase 40-hex peeled content commit")
    args = parser.parse_args()
    tag_object = require_sha(args.tag_object, "--tag-object")
    content_commit = require_sha(args.content_commit, "--content-commit")

    package_files = local_release_files()
    validate_migration()
    validate_zenodo_receipt()
    release_files = {**package_files, MIGRATION_ASSET_NAME: MIGRATION_RECEIPT}
    raw_files = {
        "README.md": ROOT / "README.md",
        "docs/bgk/index.html": ROOT / "docs" / "bgk" / "index.html",
        f"docs/bgk/{PDF_DOC_NAME}": ROOT / "docs" / "bgk" / PDF_DOC_NAME,
        "qa/BGK_UNITS_01_06_ZENODO_PUBLICATION.json": ZENODO_RECEIPT,
        "backend/bgk-common-backend-v1/MIGRATION_RECEIPT.json": MIGRATION_RECEIPT,
    }
    pages_files = {
        "index.html": ROOT / "docs" / "bgk" / "index.html",
        PDF_DOC_NAME: ROOT / "docs" / "bgk" / PDF_DOC_NAME,
    }
    if local_fact(raw_files["docs/bgk/index.html"]) != local_fact(RELEASE_DIR / PACKAGE_NAMES[1]):
        raise RuntimeError("GitHub docs HTML is not the release HTML")
    if local_fact(raw_files[f"docs/bgk/{PDF_DOC_NAME}"]) != local_fact(RELEASE_DIR / PACKAGE_NAMES[0]):
        raise RuntimeError("GitHub docs PDF is not the release PDF")

    repository = verify_repository()
    tag = verify_tag(tag_object, content_commit)
    release, release_assets = verify_release(release_files)
    raw = verify_raw(content_commit, raw_files)
    pages = verify_pages(pages_files)
    receipt_value = {
        "schema": "ag-bridge-bgk-github-publication-receipt-v1",
        "status": "PASS",
        "repository": repository,
        "content_commit": content_commit,
        "tag": tag,
        "release": {
            "url": release["html_url"],
            "tag": release["tag_name"],
            "title": release["name"],
            "published_at": release.get("published_at"),
            "draft": False,
            "prerelease": False,
        },
        "coverage": {
            "classical_units_complete": 30,
            "bgk_units_complete": 6,
            "bgk_units_total": 30,
            "two_course_source_units_complete": 36,
            "two_course_source_units_total": 60,
        },
        "anonymous_public_byte_readback": {
            "verified_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "credential_used": False,
            "release_assets": release_assets,
            "raw_commit_files": raw,
            "pages_files": pages,
            "release_assets_verified": len(release_assets),
            "raw_commit_files_verified": len(raw),
            "pages_files_verified": len(pages),
            "all_size_and_sha256_matches": True,
        },
        "metadata": {
            "language": "id-ID",
            "reader_first": True,
            "exact_model_provenance": MODEL_PROVENANCE,
            "non_endorsement_disclosed": True,
            "course_text_and_translation_license": "CC BY-SA 4.0",
            "component_rights_preserved": True,
        },
        "credential_handling": {
            "authenticated_requests_used_for_public_readback": False,
            "credential_value_logged_or_persisted": False,
        },
    }
    receipt = atomic_receipt(receipt_value)
    print(
        json.dumps(
            {
                "status": "PASS",
                "receipt": receipt,
                "release_url": RELEASE_URL,
                "pages_url": PAGES_ROOT,
                "release_assets_verified": len(release_assets),
                "raw_commit_files_verified": len(raw),
                "pages_files_verified": len(pages),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
