#!/usr/bin/env python3
"""Anonymous complete-BGK release/raw/Pages verification, never publication.

Reuses the proven Unit06 repository/tag/public-web fallback logic. Default
execution verifies existing public bytes; --local-preflight makes no network
request. No token, netrc, browser or Git executable is used. At most two
attempts per ordinary GET; Pages has three single-attempt checks. No workers.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from urllib.parse import quote
import requests
import verify_bgk_units_01_06_github_publication as prior
import publish_bgk_units_01_30_zenodo as zenodo

ROOT = prior.ROOT
TAG = 'bgk-unit-30'
TITLE = 'Bundel, Berkas, dan Kohomologi — Unit 1–30 Lengkap, Bahasa Indonesia'
RELEASE = ROOT / 'release/bgk-units-01-30'
MIGRATION = zenodo.MIGRATION_RECEIPT
PDF_NAME = 'bundel-berkas-dan-kohomologi-id-units-01-30.pdf'
NAMES = tuple(name.replace('01-06', '01-30') for name in prior.PACKAGE_NAMES)
SESSION = requests.Session()
SESSION.trust_env = False  # no ambient netrc credentials or auth-bearing proxy
SESSION.headers.update({'User-Agent': 'Codex-D100-BGK-Units-01-30-public-verifier'})

def get(url, *, headers=None, attempts=2, stream=False):
    for attempt in range(attempts):
        try:
            response = SESSION.get(url, headers=headers, timeout=(15, 45), stream=stream)
            if response.status_code == 403 and response.headers.get('X-RateLimit-Remaining') == '0':
                response.close()
                raise prior.AnonymousApiRateLimited('GitHub anonymous REST quota exhausted')
            if response.status_code in (429, 500, 502, 503, 504) and attempt + 1 < attempts:
                response.close()
                time.sleep(3)
                continue
            response.raise_for_status()
            return response
        except (requests.Timeout, requests.ConnectionError):
            if attempt + 1 == attempts:
                raise
            time.sleep(3)
    raise RuntimeError('Bounded GET exhausted')

def api_get(url):
    with get(url) as response:
        value = response.json()
    if not isinstance(value, dict):
        raise RuntimeError('Expected GitHub API object')
    return value

def stream_fact(url, *, attempts=2):
    # A dropped stream restarts only this read-only file, never the release.
    for attempt in range(attempts):
        try:
            with get(url, stream=True, attempts=1) as response:
                digest, size = hashlib.sha256(), 0
                for chunk in response.iter_content(1024 * 1024):
                    if chunk:
                        digest.update(chunk)
                        size += len(chunk)
                return {'bytes': size, 'sha256': digest.hexdigest()}
        except (requests.Timeout, requests.ConnectionError, requests.exceptions.ChunkedEncodingError):
            if attempt + 1 == attempts:
                raise
            time.sleep(3)
        except requests.HTTPError as exc:
            if exc.response is None or exc.response.status_code not in (429, 500, 502, 503, 504) or attempt + 1 == attempts:
                raise
            exc.response.close()
            time.sleep(3)
    raise RuntimeError('Bounded stream exhausted')

def configure():
    prior.TAG = TAG
    prior.EXPECTED_TITLE = TITLE
    prior.RELEASE_URL = f'{prior.WEB_ROOT}/releases/tag/{TAG}'
    prior.EXPANDED_ASSETS_URL = f'{prior.WEB_ROOT}/releases/expanded_assets/{TAG}'
    prior.RECEIPT = ROOT / 'qa/BGK_UNITS_01_30_GITHUB_PUBLICATION.json'
    prior.api_get = api_get
    prior.public_get = get
    prior.stream_fact = stream_fact

def local_contract():
    # These publisher helpers are strictly local validators, not API actions.
    manifest, qa, new = zenodo.release_contract()
    if set(new) != set(NAMES):
        raise RuntimeError('Complete30 nine-file inventory mismatch')
    reservation = zenodo.load(zenodo.RESERVATION)
    migration = zenodo.migration_fact(reservation, new)
    receipt = zenodo.load(zenodo.PUBLICATION_RECEIPT)
    rb = receipt.get('anonymous_public_byte_readback') or {}
    record = receipt.get('record') or {}
    if not (receipt.get('status') == 'PASS' and record.get('concept_doi') == zenodo.CONCEPT_DOI
            and record.get('version') == zenodo.VERSION
            and record.get('doi') == reservation['doi']
            and rb.get('credential_used') is False and rb.get('files_expected') == 18
            and rb.get('files_verified') == 18 and rb.get('all_size_and_sha256_matches') is True):
        raise RuntimeError('Complete30 Zenodo public receipt absent or inconsistent')
    rows = {row['name']: row for row in rb.get('files', [])}
    expected = {**new, zenodo.MIGRATION_PUBLIC_NAME: migration}
    for name, fact in expected.items():
        row = rows.get(name, {})
        prior.require_fact(f'Zenodo receipt {name}', {'bytes': row.get('bytes'), 'sha256': row.get('sha256')}, fact)
    files = {name: RELEASE / name for name in NAMES}
    files[MIGRATION.name] = MIGRATION
    raw = {'README.md': ROOT / 'README.md', 'docs/bgk/index.html': ROOT / 'docs/bgk/index.html',
           f'docs/bgk/{PDF_NAME}': ROOT / 'docs/bgk' / PDF_NAME,
           'qa/BGK_UNITS_01_30_ZENODO_PUBLICATION.json': zenodo.PUBLICATION_RECEIPT,
           MIGRATION.relative_to(ROOT).as_posix(): MIGRATION}
    # The exact nine packaged artifacts must also exist at the peeled commit.
    raw.update({path.relative_to(ROOT).as_posix(): path for name, path in files.items() if name in NAMES})
    pages = {'index.html': raw['docs/bgk/index.html'], PDF_NAME: raw[f'docs/bgk/{PDF_NAME}']}
    prior.require_fact('docs HTML', prior.local_fact(pages['index.html']), prior.local_fact(RELEASE / NAMES[1]))
    prior.require_fact('docs PDF', prior.local_fact(pages[PDF_NAME]), prior.local_fact(RELEASE / NAMES[0]))
    return files, raw, pages

def verify_pages(files):
    for attempt in range(3):
        rows = []
        try:
            for name, path in files.items():
                url = prior.PAGES_ROOT if name == 'index.html' else prior.PAGES_ROOT + quote(name)
                fact = stream_fact(url, attempts=1)
                prior.require_fact(f'Pages {name}', fact, prior.local_fact(path))
                rows.append({'path': name, **fact, 'url': url, 'public_readback': True, 'credential_used': False})
            return rows
        except (requests.RequestException, RuntimeError):
            if attempt == 2:
                raise
            time.sleep(10)
    raise RuntimeError('Pages deployment not yet byte-identical; rerun verifier later, do not republish')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--local-preflight', action='store_true')
    parser.add_argument('--tag-object')
    parser.add_argument('--content-commit')
    args = parser.parse_args()
    configure()
    files, raw, pages = local_contract()
    if args.local_preflight:
        print(json.dumps({'status': 'PASS_LOCAL', 'network': False, 'writes': False, 'release_files': len(files), 'raw_files': len(raw), 'pages_files': len(pages)}))
        return
    tag_object = prior.require_sha(args.tag_object or '', '--tag-object')
    commit = prior.require_sha(args.content_commit or '', '--content-commit')
    repository = prior.verify_repository()
    tag = prior.verify_tag(tag_object, commit)
    release, assets = prior.verify_release(files)
    raw_rows = prior.verify_raw(commit, raw)
    page_rows = verify_pages(pages)
    payload = {'schema': 'ag-bridge-bgk-github-publication-receipt-v1', 'status': 'PASS',
        'repository': repository, 'content_commit': commit, 'tag': tag,
        'release': {'url': prior.RELEASE_URL, 'tag': TAG, 'title': TITLE, 'published_at': release.get('published_at'), 'draft': False, 'prerelease': False},
        'coverage': {'classical_units_complete': 30, 'bgk_units_complete': 30, 'bgk_units_total': 30, 'two_course_source_units_complete': 60, 'two_course_source_units_total': 60, 'full_d100_lane_complete': False, 'original_bridge_mastery_capstone': 'not_in_this_release'},
        'anonymous_public_byte_readback': {'verified_at': datetime.now(timezone.utc).isoformat(), 'credential_used': False, 'release_assets': assets, 'raw_commit_files': raw_rows, 'pages_files': page_rows, 'release_assets_verified': len(assets), 'raw_commit_files_verified': len(raw_rows), 'pages_files_verified': len(page_rows), 'all_size_and_sha256_matches': True},
        'metadata': {'language': 'id-ID', 'reader_first': True, 'exact_model_provenance': prior.MODEL_PROVENANCE, 'non_endorsement_disclosed': True, 'course_text_and_translation_license': 'CC BY-SA 4.0', 'component_rights_preserved': True},
        'credential_handling': {'authenticated_requests_used_for_public_readback': False, 'credential_value_logged_or_persisted': False}}
    print(json.dumps({'status': 'PASS', 'receipt': prior.atomic_receipt(payload)}, indent=2))

if __name__ == '__main__':
    main()
