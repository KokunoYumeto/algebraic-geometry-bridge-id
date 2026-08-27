#!/usr/bin/env python3
"""Anonymously verify and receipt the cumulative Unit 28 GitHub publication.

The accepted Unit 27 verifier is specialized from a pinned byte identity.
``--self-check`` validates only local release bytes and contracts; the normal
mode performs anonymous public readback and never reads an account credential.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "verify_unit_27_github_publication.py"
TEMPLATE_SHA256 = "379a85ec2dc36797652114b4a3f6c0ab61aaafa0de97e7d57208424e14aa1e2d"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Unit 28 GitHub specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


def materialize_unit27_implementation() -> str:
    if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
        raise SystemExit("Accepted Unit 27 GitHub verifier is absent or has drifted")
    source = TEMPLATE.read_text(encoding="utf-8")
    marker = '\nnamespace = {"__file__":'
    if source.count(marker) != 1:
        raise SystemExit("Could not isolate the accepted Unit 27 GitHub builder")
    builder = source[: source.index(marker)]
    namespace = {"__file__": str(TEMPLATE), "__name__": "unit27_builder_capture"}
    exec(compile(builder, str(TEMPLATE), "exec"), namespace)
    generated = namespace.get("generated")
    if not isinstance(generated, str):
        raise SystemExit("Accepted Unit 27 GitHub builder yielded no implementation")
    return generated


generated = materialize_unit27_implementation()
for old, new in (
    ("Units 1–27", "Units 1–28"),
    ("Unit 1–27", "Unit 1–28"),
    ("Units 24–27", "Units 24–28"),
    ("Unit 24–27", "Unit 24–28"),
    ("units_24_27", "units_24_28"),
):
    generated = generated.replace(old, new)

generated = replace_once(
    generated,
    '    if not isinstance(coverage, dict) or coverage.get("through_unit") != 27:',
    '    if not isinstance(coverage, dict) or coverage.get("through_unit") != 28:',
)
generated = replace_once(
    generated,
    '        raise RuntimeError("Unit 27 release must remain a truthful partial 27/30 checkpoint")',
    '        raise RuntimeError("Unit 28 release must remain a truthful partial 28/30 checkpoint")',
)

for old, new in (
    ("units-01-27", "units-01-28"),
    ("UNITS_01_27", "UNITS_01_28"),
    ("UNIT_27", "UNIT_28"),
    ("unit-27", "unit-28"),
    ("unit_27", "unit_28"),
    ("unit27", "unit28"),
    ("Unit 27", "Unit 28"),
):
    generated = generated.replace(old, new)

# Bind all changing coverage to the frozen local candidate.  Reader facts are
# independently pinned here; the backend count is measured only after its
# deterministic export instead of being guessed in advance.
generated = replace_once(
    generated,
    '''    exact_coverage = {
        "pdf_pages": 464,
        "exercises": 657,
        "public_source_solutions": 117,
        "reader_media_positions": 94,
        "backend_records": 20570,
    }
    for key, wanted in exact_coverage.items():
        if coverage.get(key) != wanted:
            raise RuntimeError(
                f"Unit 28 release coverage {key} mismatch: {coverage.get(key)!r} != {wanted!r}"
            )
    candidate_path = ROOT / "qa" / "UNIT_28_RELEASE_CANDIDATE.json"
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    candidate_coverage = candidate.get("coverage") or {}
    candidate_map = {
        "pdf_pages": ((candidate.get("reader") or {}).get("pdf") or {}).get("pages"),
        "exercises": candidate_coverage.get("exercises"),
        "public_source_solutions": candidate_coverage.get("public_source_solutions"),
        "reader_media_positions": candidate_coverage.get("reader_media_positions"),
        "backend_records": candidate_coverage.get("native_backend_records"),
    }
    if candidate_map != exact_coverage:
        raise RuntimeError("Unit 28 release manifest is not bound to the frozen candidate")''',
    '''    candidate_path = ROOT / "qa" / "UNIT_28_RELEASE_CANDIDATE.json"
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    if not isinstance(candidate, dict) or candidate.get("status") != "PASS_RELEASE_READY":
        raise RuntimeError("Unit 28 frozen release candidate is unavailable or not ready")
    candidate_coverage = candidate.get("coverage") or {}
    backend_records = candidate_coverage.get("native_backend_records")
    if not isinstance(backend_records, int) or isinstance(backend_records, bool) or backend_records <= 20570:
        raise RuntimeError("Unit 28 candidate does not extend the 20,570-record Unit 27 backend")
    exact_coverage = {
        "pdf_pages": 476,
        "exercises": 671,
        "public_source_solutions": 118,
        "reader_media_positions": 98,
        "backend_records": backend_records,
    }
    for key, wanted in exact_coverage.items():
        if coverage.get(key) != wanted:
            raise RuntimeError(
                f"Unit 28 release coverage {key} mismatch: {coverage.get(key)!r} != {wanted!r}"
            )
    candidate_map = {
        "pdf_pages": ((candidate.get("reader") or {}).get("pdf") or {}).get("pages"),
        "exercises": candidate_coverage.get("exercises"),
        "public_source_solutions": candidate_coverage.get("public_source_solutions"),
        "reader_media_positions": candidate_coverage.get("reader_media_positions"),
        "backend_records": candidate_coverage.get("native_backend_records"),
    }
    if candidate_map != exact_coverage:
        raise RuntimeError("Unit 28 release manifest is not bound to the frozen candidate")''',
)

# The Unit 28 DOI does not exist until Zenodo reserves the new version.  Bind
# GitHub metadata to the sanitized public Zenodo receipt rather than hard-code
# or predict that identity.
generated = replace_once(
    generated,
    '''    citation_text = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    if 'doi: "10.5281/zenodo.22104692"' not in citation_text:
        raise RuntimeError("Public citation does not bind the Unit 28 Zenodo DOI")''',
    '''    zenodo_receipt_path = ROOT / "qa" / "UNIT_28_ZENODO_PUBLICATION.json"
    zenodo_receipt = json.loads(zenodo_receipt_path.read_text(encoding="utf-8"))
    if not isinstance(zenodo_receipt, dict) or zenodo_receipt.get("status") != "PASS":
        raise RuntimeError("Unit 28 Zenodo publication receipt is unavailable or not PASS")
    zenodo_record = zenodo_receipt.get("record")
    if not isinstance(zenodo_record, dict):
        raise RuntimeError("Unit 28 Zenodo record identity is missing")
    if zenodo_record.get("previous_record_id") != 22104692:
        raise RuntimeError("Unit 28 Zenodo receipt is not the successor of record 22104692")
    publication_doi = zenodo_record.get("doi")
    if not isinstance(publication_doi, str) or not publication_doi.startswith("10.5281/zenodo."):
        raise RuntimeError("Unit 28 Zenodo DOI is invalid")
    if publication_doi == "10.5281/zenodo.22104692":
        raise RuntimeError("Unit 28 Zenodo receipt reuses the Unit 27 DOI")
    citation_text = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    if f'doi: "{publication_doi}"' not in citation_text:
        raise RuntimeError("Public citation does not bind the Unit 28 Zenodo DOI")''',
)

# Add a truly offline contract check.  It validates the exact eight local
# release files and the frozen lineage/tag facts, and does not instantiate an
# HTTP session.
generated = replace_once(
    generated,
    "def main() -> None:",
    '''def self_check() -> dict:
    expected, manifest = load_release_contract()
    candidate = json.loads(
        (ROOT / "qa" / "UNIT_28_RELEASE_CANDIDATE.json").read_text(encoding="utf-8")
    )
    publication = candidate.get("publication") or {}
    if ((publication.get("github") or {}).get("target_tag")) != TAG:
        raise RuntimeError("Unit 28 candidate GitHub tag mismatch")
    if ((publication.get("zenodo") or {}).get("previous_record_id")) != 22104692:
        raise RuntimeError("Unit 28 candidate Zenodo predecessor mismatch")
    if list(expected) != FILES or len(expected) != 8:
        raise RuntimeError("Unit 28 release is not the exact eight-file inventory")
    for relative in ("CITATION.cff", "README.md", "LICENSE.md", "docs/index.html", "docs/algebraic-geometry-bridge-id-units-01-28.pdf"):
        repository_descriptor(relative)
    return {
        "status": "PASS",
        "mode": "offline_local_contract_check",
        "version": manifest.get("version"),
        "tag": TAG,
        "files": len(expected),
        "credential_read": False,
        "network_called": False,
        "receipt_written": False,
    }


def main() -> None:''',
)
generated = replace_once(
    generated,
    '''    parser = argparse.ArgumentParser()
    parser.add_argument("--wait-seconds", type=int, default=300)
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    result = verify(args.wait_seconds, args.expected_commit)''',
    '''    parser = argparse.ArgumentParser()
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--wait-seconds", type=int, default=300)
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    if args.self_check:
        print(json.dumps(self_check(), indent=2))
        return
    result = verify(args.wait_seconds, args.expected_commit)''',
)

# GitHub's unauthenticated REST core limit is intentionally small.  Preserve
# the accepted REST verification when it is available, but make a rate-limit
# response non-fatal by switching to independent anonymous public surfaces:
# smart-HTTP refs, fixed release downloads, fixed-commit raw bytes, public HTML,
# and Pages.  The fallback never reads a credential and still fails closed on
# the caller-pinned commit and every locally frozen byte identity.
generated = replace_once(
    generated,
    "import json\nimport time",
    "import json\nimport os\nimport subprocess\nimport time",
)

verify_start = generated.index(
    "def verify(wait_seconds: int, expected_commit: str | None = None) -> dict[str, object]:"
)
verify_end = generated.index("\ndef self_check() -> dict:", verify_start)
generated = generated[:verify_start] + r'''def valid_commit(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 40
        and all(character in "0123456789abcdef" for character in value)
    )


def api_core_rate_limit_403(exc: requests.HTTPError) -> bool:
    response = exc.response
    if response is None or response.status_code != 403:
        return False
    if not response.url.startswith("https://api.github.com/"):
        return False
    remaining = response.headers.get("X-RateLimit-Remaining")
    try:
        message = response.text[:4096].lower()
    except Exception:
        message = ""
    return remaining == "0" or "api rate limit exceeded" in message


def html_metadata_surface(
    session: requests.Session,
    url: str,
    required_markers: list[str],
    label: str,
) -> dict[str, object]:
    response = session.get(
        url,
        headers={"Accept": "text/html,application/xhtml+xml"},
        timeout=120,
    )
    response.raise_for_status()
    content_type = response.headers.get("Content-Type", "")
    if "text/html" not in content_type.lower():
        raise RuntimeError(f"{label} did not return HTML: {content_type!r}")
    payload = response.content
    if len(payload) < 1024:
        raise RuntimeError(f"{label} returned implausibly short HTML")
    text = payload.decode(response.encoding or "utf-8", errors="replace")
    missing = [marker for marker in required_markers if marker not in text]
    if missing:
        raise RuntimeError(f"{label} is missing required public markers: {missing}")
    return {
        "url": url,
        "final_url": response.url,
        "status_code": response.status_code,
        "content_type": content_type,
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "required_markers_present": required_markers,
        "anonymous_readback": True,
    }


def anonymous_smart_http_refs(expected_commit: str) -> dict[str, object]:
    repository_url = f"https://github.com/{OWNER}/{REPOSITORY}.git"
    wanted = {
        "refs/heads/main",
        f"refs/tags/{TAG}",
        f"refs/tags/{TAG}^{{}}",
    }
    environment = dict(os.environ)
    environment.update(
        {
            "GIT_TERMINAL_PROMPT": "0",
            "GCM_INTERACTIVE": "Never",
        }
    )
    command = [
        "git",
        "-c",
        "credential.helper=",
        "ls-remote",
        repository_url,
        "refs/heads/main",
        f"refs/tags/{TAG}",
        f"refs/tags/{TAG}^{{}}",
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "Anonymous Git smart-HTTP ref verification failed "
            f"with exit code {completed.returncode}"
        )
    refs: dict[str, str] = {}
    for raw_line in completed.stdout.splitlines():
        parts = raw_line.split("\t", 1)
        if len(parts) != 2 or parts[1] not in wanted:
            continue
        if parts[1] in refs:
            raise RuntimeError(f"Duplicate smart-HTTP ref: {parts[1]}")
        refs[parts[1]] = parts[0]
    if set(refs) != wanted:
        raise RuntimeError(f"Anonymous smart-HTTP ref inventory mismatch: {sorted(refs)}")
    if any(not valid_commit(value) for value in refs.values()):
        raise RuntimeError("Anonymous smart-HTTP returned an invalid object identity")
    if refs["refs/heads/main"] != expected_commit:
        raise RuntimeError("Anonymous smart-HTTP main does not match the pinned commit")
    if refs[f"refs/tags/{TAG}^{{}}"] != expected_commit:
        raise RuntimeError("Anonymous smart-HTTP annotated tag does not target the pinned commit")
    if refs[f"refs/tags/{TAG}"] == expected_commit:
        raise RuntimeError("Unit 28 public tag is not independently represented as an annotated tag")
    return {
        "transport": "anonymous_git_smart_http",
        "repository_url": repository_url,
        "credential_helper_disabled": True,
        "terminal_prompt_disabled": True,
        "main_commit": refs["refs/heads/main"],
        "annotated_tag_object": refs[f"refs/tags/{TAG}"],
        "dereferenced_tag_commit": refs[f"refs/tags/{TAG}^{{}}"],
    }


def verify(wait_seconds: int, expected_commit: str | None = None) -> dict[str, object]:
    expected, release_manifest = load_release_contract()
    if expected_commit is not None and not valid_commit(expected_commit):
        raise RuntimeError(f"Invalid caller-pinned commit: {expected_commit!r}")
    session = requests.Session()
    session.headers.update(
        {
            "Accept": "application/vnd.github+json",
            "User-Agent": "ag-bridge-id-public-readback",
            "Cache-Control": "no-cache",
        }
    )

    metadata_mode = "anonymous_github_rest_api"
    api_rate_limit: dict[str, object] | None = None
    smart_http: dict[str, object] | None = None
    try:
        branch = request_json(session, f"{API}/branches/main")
        branch_commit = (branch.get("commit") or {}).get("sha")
        if not valid_commit(branch_commit):
            raise RuntimeError(f"Invalid public main commit identity: {branch_commit!r}")
        if expected_commit is not None and branch_commit != expected_commit:
            raise RuntimeError(
                f"Public main commit differs from caller binding: {branch_commit} != {expected_commit}"
            )

        tag_ref = request_json(session, f"{API}/git/ref/tags/{TAG}")
        tag_object = tag_ref.get("object") or {}
        if tag_object.get("type") != "tag" or not valid_commit(tag_object.get("sha")):
            raise RuntimeError("Unit 28 is not an annotated tag")
        annotated = request_json(session, f"{API}/git/tags/{tag_object['sha']}")
        if annotated.get("object", {}).get("type") != "commit":
            raise RuntimeError("Annotated Unit 28 tag does not target a commit")
        if annotated.get("object", {}).get("sha") != branch_commit:
            raise RuntimeError("Annotated Unit 28 tag targets the wrong commit")

        release = request_json(session, f"{API}/releases/tags/{TAG}")
        assets = release.get("assets")
        if not isinstance(assets, list) or len(assets) != len(FILES):
            raise RuntimeError("GitHub release does not expose exactly eight assets")
        by_name = {item.get("name"): item for item in assets if isinstance(item, dict)}
        if set(by_name) != set(FILES):
            raise RuntimeError(f"GitHub release asset inventory mismatch: {sorted(by_name)}")
        asset_urls = {}
        for name in FILES:
            direct_url = (
                f"https://github.com/{OWNER}/{REPOSITORY}/releases/download/{TAG}/{name}"
            )
            if by_name[name].get("browser_download_url") != direct_url:
                raise RuntimeError(f"GitHub API returned a noncanonical asset URL for {name}")
            asset_urls[name] = direct_url
        release_published_utc = release.get("published_at")
    except requests.HTTPError as exc:
        if not api_core_rate_limit_403(exc):
            raise
        if expected_commit is None:
            raise RuntimeError(
                "A caller-pinned commit is required for rate-limit-independent verification"
            ) from exc
        response = exc.response
        api_rate_limit = {
            "detected": True,
            "status_code": 403,
            "url": response.url if response is not None else None,
            "x_ratelimit_remaining": (
                response.headers.get("X-RateLimit-Remaining") if response is not None else None
            ),
        }
        metadata_mode = "anonymous_direct_surfaces_after_api_core_rate_limit"
        smart_http = anonymous_smart_http_refs(expected_commit)
        branch_commit = smart_http["main_commit"]
        tag_object = {"sha": smart_http["annotated_tag_object"], "type": "tag"}
        asset_urls = {
            name: f"https://github.com/{OWNER}/{REPOSITORY}/releases/download/{TAG}/{name}"
            for name in FILES
        }
        release_published_utc = None

    fixed_release_url = f"https://github.com/{OWNER}/{REPOSITORY}/releases/tag/{TAG}"
    fixed_commit_url = f"https://github.com/{OWNER}/{REPOSITORY}/commit/{branch_commit}"
    release_html = html_metadata_surface(
        session,
        fixed_release_url,
        [TAG, REPOSITORY],
        "GitHub release/tag HTML",
    )
    commit_html = html_metadata_surface(
        session,
        fixed_commit_url,
        [branch_commit, REPOSITORY],
        "GitHub commit HTML",
    )

    verified_assets = []
    for name in FILES:
        actual = readback(session, asset_urls[name])
        verify_equal(actual, expected[name], f"GitHub release asset {name}")
        verified_assets.append(
            {
                "name": name,
                "bytes": actual["bytes"],
                "sha256": actual["sha256"],
                "download_url": asset_urls[name],
                "public_readback": True,
            }
        )

    raw_html = readback(
        session,
        f"https://raw.githubusercontent.com/{OWNER}/{REPOSITORY}/{branch_commit}/docs/index.html",
    )
    raw_pdf = readback(
        session,
        f"https://raw.githubusercontent.com/{OWNER}/{REPOSITORY}/{branch_commit}/docs/"
        "algebraic-geometry-bridge-id-units-01-28.pdf",
    )
    verify_equal(raw_html, expected["kurva-aljabar-id-unit-28.html"], "raw commit HTML")
    verify_equal(raw_pdf, expected["kurva-aljabar-id-unit-28.pdf"], "raw commit PDF")
    raw_metadata: dict[str, dict[str, object]] = {}
    for relative in ("CITATION.cff", "README.md", "LICENSE.md"):
        local = repository_descriptor(relative)
        actual = readback(
            session,
            f"https://raw.githubusercontent.com/{OWNER}/{REPOSITORY}/{branch_commit}/{relative}",
        )
        verify_equal(actual, local, f"raw commit {relative}")
        raw_metadata[relative] = {**actual, "match": True}

    zenodo_receipt_path = ROOT / "qa" / "UNIT_28_ZENODO_PUBLICATION.json"
    zenodo_receipt = json.loads(zenodo_receipt_path.read_text(encoding="utf-8"))
    if not isinstance(zenodo_receipt, dict) or zenodo_receipt.get("status") != "PASS":
        raise RuntimeError("Unit 28 Zenodo publication receipt is unavailable or not PASS")
    zenodo_record = zenodo_receipt.get("record")
    if not isinstance(zenodo_record, dict):
        raise RuntimeError("Unit 28 Zenodo record identity is missing")
    if zenodo_record.get("previous_record_id") != 22104692:
        raise RuntimeError("Unit 28 Zenodo receipt is not the successor of record 22104692")
    publication_doi = zenodo_record.get("doi")
    if not isinstance(publication_doi, str) or not publication_doi.startswith("10.5281/zenodo."):
        raise RuntimeError("Unit 28 Zenodo DOI is invalid")
    if publication_doi == "10.5281/zenodo.22104692":
        raise RuntimeError("Unit 28 Zenodo receipt reuses the Unit 27 DOI")
    citation_text = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    if f'doi: "{publication_doi}"' not in citation_text:
        raise RuntimeError("Public citation does not bind the Unit 28 Zenodo DOI")

    deadline = time.monotonic() + wait_seconds
    pages_html = wait_for_pages(
        session,
        f"{PAGES}/",
        expected["kurva-aljabar-id-unit-28.html"],
        deadline,
    )
    pages_pdf = wait_for_pages(
        session,
        f"{PAGES}/algebraic-geometry-bridge-id-units-01-28.pdf",
        expected["kurva-aljabar-id-unit-28.pdf"],
        deadline,
    )

    receipt = {
        "schema": "ag-bridge-github-publication-receipt-v2",
        "status": "PASS",
        "verified_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repository": f"https://github.com/{OWNER}/{REPOSITORY}",
        "release_manifest": {
            **local_descriptor(MANIFEST_NAME),
            "through_unit": release_manifest["coverage"]["through_unit"],
            "planned_units": release_manifest["coverage"]["planned_units"],
            "full_edition_complete": release_manifest["coverage"]["full_edition_complete"],
            "source_course_boundary": release_manifest["rights"]["source_course_boundary"],
        },
        "metadata_verification": {
            "mode": metadata_mode,
            "api_core_rate_limit": api_rate_limit,
            "smart_http": smart_http,
            "surfaces_used": [
                "github_rest_api" if metadata_mode == "anonymous_github_rest_api" else "git_smart_http",
                "github_release_tag_html",
                "github_commit_html",
                "fixed_release_download_urls",
                "fixed_commit_raw_githubusercontent",
                "github_pages",
            ],
            "release_tag_html": release_html,
            "commit_html": commit_html,
        },
        "branch": {
            "name": "main",
            "commit": branch_commit,
            "caller_pinned_commit": expected_commit,
            "anonymous_api_readback": metadata_mode == "anonymous_github_rest_api",
            "anonymous_smart_http_readback": smart_http is not None,
        },
        "tag": {
            "name": TAG,
            "annotated_tag_object": tag_object["sha"],
            "target_type": "commit",
            "target_commit": branch_commit,
            "anonymous_api_readback": metadata_mode == "anonymous_github_rest_api",
            "anonymous_smart_http_readback": smart_http is not None,
        },
        "release": {
            "url": fixed_release_url,
            "published_utc": release_published_utc,
            "published_utc_available_via_api": release_published_utc is not None,
            "assets_expected": len(FILES),
            "assets_verified": len(verified_assets),
            "credential_used_for_readback": False,
            "all_size_and_sha256_matches": True,
            "files": verified_assets,
        },
        "raw_commit_readback": {
            "credential_used": False,
            "commit": branch_commit,
            "html": {**raw_html, "match": True},
            "pdf": {**raw_pdf, "match": True},
            "metadata": raw_metadata,
        },
        "pages_readback": {
            "credential_used": False,
            "reader": {**pages_html, "match": True},
            "pdf": {**pages_pdf, "match": True},
        },
        "credential_handling": {
            "public_readback_used_anonymous_requests": True,
            "git_credential_helper_disabled_for_smart_http": smart_http is not None,
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

''' + generated[verify_end:]

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE), "exec"), namespace)
