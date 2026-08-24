#!/usr/bin/env python3
"""Anonymously verify and receipt the cumulative Unit 15 GitHub publication."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
RELEASE_DIR = ROOT / "release" / "unit-15"
RECEIPT = ROOT / "qa" / "UNIT_15_GITHUB_PUBLICATION.json"
OWNER = "KokunoYumeto"
REPOSITORY = "algebraic-geometry-bridge-id"
TAG = "unit-15"
EXPECTED_COMMIT = "aada4c2320a79e5dcdce0d7fa767c67dd0b24a9e"
API = f"https://api.github.com/repos/{OWNER}/{REPOSITORY}"
PAGES = f"https://{OWNER.lower()}.github.io/{REPOSITORY}"
FILES = [
    "kurva-aljabar-id-unit-15.pdf",
    "kurva-aljabar-id-unit-15.html",
    "kurva-aljabar-id-unit-15-source.zip",
    "kurva-aljabar-id-unit-15-authority-witnesses.zip",
    "BUILD_RECEIPT-unit-15.json",
    "LICENSE-unit-15.md",
    "ZENODO_FILE_MANIFEST-unit-15.json",
    "MIGRATION_RECEIPT.json",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def local_descriptor(name: str) -> dict[str, object]:
    path = RELEASE_DIR / name
    if not path.is_file():
        raise FileNotFoundError(path)
    return {"name": name, "bytes": path.stat().st_size, "sha256": sha256(path)}


def request_json(session: requests.Session, url: str) -> dict:
    response = session.get(url, timeout=60)
    response.raise_for_status()
    value = response.json()
    if not isinstance(value, dict):
        raise RuntimeError(f"Expected JSON object from {url}")
    return value


def readback(session: requests.Session, url: str) -> dict[str, object]:
    digest = hashlib.sha256()
    size = 0
    with session.get(url, stream=True, timeout=120) as response:
        response.raise_for_status()
        for chunk in response.iter_content(1024 * 1024):
            if chunk:
                size += len(chunk)
                digest.update(chunk)
    return {"url": url, "bytes": size, "sha256": digest.hexdigest()}


def verify_equal(actual: dict[str, object], expected: dict[str, object], label: str) -> None:
    if actual["bytes"] != expected["bytes"] or actual["sha256"] != expected["sha256"]:
        raise RuntimeError(
            f"{label} mismatch: expected {expected['bytes']}/{expected['sha256']}, "
            f"found {actual['bytes']}/{actual['sha256']}"
        )


def wait_for_pages(
    session: requests.Session,
    url: str,
    expected: dict[str, object],
    deadline: float,
) -> dict[str, object]:
    last: dict[str, object] | None = None
    while True:
        cache_busted = f"{url}?unit-15={int(time.time())}"
        try:
            last = readback(session, cache_busted)
            if (
                last["bytes"] == expected["bytes"]
                and last["sha256"] == expected["sha256"]
            ):
                last["url"] = url
                return last
        except requests.RequestException:
            pass
        if time.monotonic() >= deadline:
            raise RuntimeError(f"GitHub Pages did not converge to Unit 15 bytes: {last}")
        time.sleep(5)


def verify(wait_seconds: int) -> dict[str, object]:
    expected = {name: local_descriptor(name) for name in FILES}
    session = requests.Session()
    session.headers.update(
        {
            "Accept": "application/vnd.github+json",
            "User-Agent": "ag-bridge-id-public-readback",
            "Cache-Control": "no-cache",
        }
    )

    branch = request_json(session, f"{API}/branches/main")
    branch_commit = branch["commit"]["sha"]
    if branch_commit != EXPECTED_COMMIT:
        raise RuntimeError(f"Unexpected public main commit: {branch_commit}")

    tag_ref = request_json(session, f"{API}/git/ref/tags/{TAG}")
    tag_object = tag_ref["object"]
    if tag_object["type"] != "tag":
        raise RuntimeError("Unit 15 is not an annotated tag")
    annotated = request_json(session, f"{API}/git/tags/{tag_object['sha']}")
    if annotated["object"]["type"] != "commit":
        raise RuntimeError("Annotated Unit 15 tag does not target a commit")
    if annotated["object"]["sha"] != EXPECTED_COMMIT:
        raise RuntimeError("Annotated Unit 15 tag targets the wrong commit")

    release = request_json(session, f"{API}/releases/tags/{TAG}")
    assets = release.get("assets")
    if not isinstance(assets, list) or len(assets) != len(FILES):
        raise RuntimeError("GitHub release does not expose exactly eight assets")
    by_name = {item.get("name"): item for item in assets if isinstance(item, dict)}
    if set(by_name) != set(FILES):
        raise RuntimeError(f"GitHub release asset inventory mismatch: {sorted(by_name)}")
    verified_assets = []
    for name in FILES:
        asset = by_name[name]
        actual = readback(session, asset["browser_download_url"])
        verify_equal(actual, expected[name], f"GitHub release asset {name}")
        verified_assets.append(
            {
                "name": name,
                "bytes": actual["bytes"],
                "sha256": actual["sha256"],
                "download_url": asset["browser_download_url"],
                "public_readback": True,
            }
        )

    raw_html = readback(
        session,
        f"https://raw.githubusercontent.com/{OWNER}/{REPOSITORY}/{EXPECTED_COMMIT}/docs/index.html",
    )
    raw_pdf = readback(
        session,
        f"https://raw.githubusercontent.com/{OWNER}/{REPOSITORY}/{EXPECTED_COMMIT}/docs/"
        "algebraic-geometry-bridge-id-units-01-15.pdf",
    )
    verify_equal(raw_html, expected["kurva-aljabar-id-unit-15.html"], "raw commit HTML")
    verify_equal(raw_pdf, expected["kurva-aljabar-id-unit-15.pdf"], "raw commit PDF")

    deadline = time.monotonic() + wait_seconds
    pages_html = wait_for_pages(
        session,
        f"{PAGES}/",
        expected["kurva-aljabar-id-unit-15.html"],
        deadline,
    )
    pages_pdf = wait_for_pages(
        session,
        f"{PAGES}/algebraic-geometry-bridge-id-units-01-15.pdf",
        expected["kurva-aljabar-id-unit-15.pdf"],
        deadline,
    )

    receipt = {
        "schema": "ag-bridge-github-publication-receipt-v1",
        "status": "PASS",
        "verified_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repository": f"https://github.com/{OWNER}/{REPOSITORY}",
        "branch": {
            "name": "main",
            "commit": EXPECTED_COMMIT,
            "anonymous_api_readback": True,
        },
        "tag": {
            "name": TAG,
            "annotated_tag_object": tag_object["sha"],
            "target_type": "commit",
            "target_commit": EXPECTED_COMMIT,
            "anonymous_api_readback": True,
        },
        "release": {
            "url": release["html_url"],
            "published_utc": release["published_at"],
            "assets_expected": len(FILES),
            "assets_verified": len(verified_assets),
            "credential_used_for_readback": False,
            "all_size_and_sha256_matches": True,
            "files": verified_assets,
        },
        "raw_commit_readback": {
            "credential_used": False,
            "html": {**raw_html, "match": True},
            "pdf": {**raw_pdf, "match": True},
        },
        "pages_readback": {
            "credential_used": False,
            "reader": {**pages_html, "match": True},
            "pdf": {**pages_pdf, "match": True},
        },
        "credential_handling": {
            "public_readback_used_anonymous_requests": True,
            "credential_value_logged_or_persisted": False,
            "credential_file_path_recorded": False,
        },
    }
    RECEIPT.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    reread = json.loads(RECEIPT.read_text(encoding="utf-8"))
    if reread != receipt:
        raise RuntimeError("GitHub publication receipt readback mismatch")
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wait-seconds", type=int, default=300)
    args = parser.parse_args()
    result = verify(args.wait_seconds)
    print(
        json.dumps(
            {
                "status": result["status"],
                "commit": result["branch"]["commit"],
                "tag_object": result["tag"]["annotated_tag_object"],
                "release_assets_verified": result["release"]["assets_verified"],
                "pages_verified": True,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
