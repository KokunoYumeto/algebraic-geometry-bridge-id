#!/usr/bin/env python3
"""Authorized Units 1--6 payload refresh for the cumulative Unit 7 backend.

The frozen Units 1--6 export remains the identity/topology baseline.  The
2026-08-22 Indonesian terminology QA changed only reader wording and four
terminology-control rows.  This module rebuilds the affected content payloads
and hashes from the current source while failing closed on every structural
field and on every text delta outside the two authorized substitutions.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable


FIELD_PATTERN = re.compile(
    r"(?<![\w])medan(?![\w])",
    flags=re.IGNORECASE | re.UNICODE,
)
QUOTIENT_PATTERN = re.compile(
    r"(gelanggang(?:-gelanggang)?)(\s+)hasil bagi(nya)?",
    flags=re.IGNORECASE,
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s+\{#([^}]+)\}\s*$")
PRIOR_SOURCE_RE = re.compile(
    r"^source/id-ID/(?:lecture|worksheet)-0[1-6](?:-solutions)?\.md$"
)
MIGRATED_TERM_IDS = {"AGT-0004", "AGT-0027", "AGT-0028", "AGT-0030"}


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _text_digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def authorized_text(text: str) -> str:
    """Apply exactly the two terminology substitutions recorded by QA."""

    def field_replacement(match: re.Match[str]) -> str:
        return "Lapangan" if match.group(0)[0] == "M" else "lapangan"

    updated = FIELD_PATTERN.sub(field_replacement, text)

    def quotient_replacement(match: re.Match[str]) -> str:
        stem = match.group(1)
        if stem[0] == "G":
            stem = "G" + stem[1:]
        return stem + match.group(2) + "faktor" + (match.group(3) or "")

    return QUOTIENT_PATTERN.sub(quotient_replacement, updated)


def _strip_yaml(lines: list[str]) -> list[str]:
    if not lines or lines[0].strip() != "---":
        return lines
    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration as exc:
        raise RuntimeError("Unclosed YAML frontmatter") from exc
    return [""] * (end + 1) + lines[end + 1 :]


def _segment_type(content: str) -> str:
    if content.startswith("!["):
        return "figure_reference"
    if content.startswith("$$") or content.startswith("\\["):
        return "display_math"
    if content.startswith(("- ", "1. ", "2. ", "3. ")):
        return "list"
    if content.startswith("\\begin") or content.startswith("\\end"):
        return "raw_tex"
    return "prose"


def _source_rows(root: Path, receipt: dict[str, Any]) -> list[tuple[str, Path]]:
    after_by_path = {row["path"]: row for row in receipt["after"]}
    before_by_path = {row["path"]: row for row in receipt["before"]}
    if set(after_by_path) != set(before_by_path):
        raise RuntimeError("Terminology migration before/after path sets differ")
    selected: list[tuple[str, Path]] = []
    for relative in sorted(after_by_path):
        if not PRIOR_SOURCE_RE.fullmatch(relative):
            continue
        path = root / relative
        if not path.is_file():
            raise RuntimeError(f"Migrated source is absent: {relative}")
        actual = _digest(path)
        if actual != after_by_path[relative]["sha256"]:
            raise RuntimeError(
                f"Migrated source hash mismatch: {relative} {actual} != "
                f"{after_by_path[relative]['sha256']}"
            )
        selected.append((relative, path))
    if len(selected) != 18:
        raise RuntimeError(f"Expected 18 prior reader source files, found {len(selected)}")
    return selected


def _validate_receipt(receipt: dict[str, Any]) -> None:
    if receipt.get("schema") != "ag-bridge-terminology-migration-v1":
        raise RuntimeError("Unexpected terminology migration receipt schema")
    replacements = {row["concept"]: row for row in receipt.get("replacements", [])}
    if replacements.get("field", {}).get("occurrences") != 117:
        raise RuntimeError("Field migration receipt is not the frozen 117-occurrence boundary")
    if replacements.get("quotient ring", {}).get("occurrences") != 22:
        raise RuntimeError("Quotient-ring migration receipt is not the frozen 22-occurrence boundary")
    post = receipt.get("post_counts", {})
    if post != {
        "medan": 0,
        "lapangan": 117,
        "quotient_ring_old": 0,
        "gelanggang_faktor": 22,
    }:
        raise RuntimeError(f"Unexpected terminology post-count boundary: {post}")


def _structural_projection(record: dict[str, Any]) -> dict[str, Any]:
    """Remove only fields authorized to change as reader/term content."""

    projected = json.loads(_canonical(record))
    projected["content_sha256"] = None
    entity_class = projected["entity_class"]
    if entity_class == "unit":
        projected["payload"].pop("title_markdown", None)
        projected["payload"].pop("source_file_sha256", None)
    elif entity_class == "segment":
        projected["payload"].pop("markdown", None)
    elif entity_class == "term":
        projected["payload"] = {}
    elif entity_class in {"exercise", "solution"}:
        projected["provenance"].pop("indexed_unit_record_sha256", None)
    return projected


def _top_level_diff(before: dict[str, Any], after: dict[str, Any]) -> list[str]:
    return sorted(key for key in before if before[key] != after[key])


def refresh_baseline(
    *,
    root: Path,
    baseline_records: list[dict[str, Any]],
    records: list[dict[str, Any]],
    terminology_path: Path,
    migration_receipt_path: Path,
    canonical: Callable[[Any], str] = _canonical,
    text_digest: Callable[[str], str] = _text_digest,
    digest: Callable[[Path], str] = _digest,
) -> dict[str, Any]:
    """Mutate baseline record objects only on authorized content surfaces."""

    receipt = json.loads(migration_receipt_path.read_text(encoding="utf-8"))
    _validate_receipt(receipt)
    source_rows = _source_rows(root, receipt)
    baseline_by_id = {row["stable_id"]: row for row in baseline_records}
    if len(baseline_by_id) != len(baseline_records):
        raise RuntimeError("Duplicate stable ID in Units 1--6 baseline")
    original_by_id = {
        stable_id: json.loads(canonical(row)) for stable_id, row in baseline_by_id.items()
    }

    refreshed_unit_ids: set[str] = set()
    refreshed_segment_ids: set[str] = set()
    segment_text_changes: dict[str, dict[str, int]] = {}
    preexisting_logged_text_deltas: dict[str, list[str]] = {}

    correction_targets: defaultdict[str, set[str]] = defaultdict(set)
    for row in baseline_records:
        if row["entity_class"] != "correction":
            continue
        for target in row.get("payload", {}).get("affected_unit_ids", []):
            correction_targets[target].add(row["stable_id"])

    def covering_corrections(stable_id: str) -> list[str]:
        covered: set[str] = set()
        cursor: str | None = stable_id
        visited: set[str] = set()
        while cursor and cursor not in visited:
            visited.add(cursor)
            covered.update(correction_targets.get(cursor, set()))
            parent = baseline_by_id.get(cursor, {}).get("parent_id")
            cursor = parent if isinstance(parent, str) else None
        return sorted(covered)

    for relative, path in source_rows:
        file_hash = digest(path)
        lines = _strip_yaml(path.read_text(encoding="utf-8").splitlines())
        heading_rows: list[tuple[int, int, str, str]] = []
        for index, line in enumerate(lines):
            match = HEADING_RE.match(line)
            if match:
                heading_rows.append((index, len(match.group(1)), match.group(2), match.group(3)))

        expected_units: set[str] = set()
        for position, (line_index, level, title, identifier) in enumerate(heading_rows):
            expected_units.add(identifier)
            if identifier not in baseline_by_id:
                raise RuntimeError(f"Current heading stable ID absent from baseline: {identifier}")
            record = baseline_by_id[identifier]
            if record["entity_class"] != "unit":
                raise RuntimeError(f"Heading ID is not a unit record: {identifier}")
            expected_path = f"{relative}#{identifier}"
            expected_locator = f"{relative}:{line_index + 1}"
            if record["path"] != expected_path or record["source_locator"] != expected_locator:
                raise RuntimeError(f"Heading topology/line locator changed: {identifier}")
            next_boundary = len(lines)
            for next_index, next_level, _, _ in heading_rows[position + 1 :]:
                if next_level <= level:
                    next_boundary = next_index
                    break
            region = "\n".join(lines[line_index:next_boundary]).strip() + "\n"
            old_title = record["payload"]["title_markdown"]
            if title != authorized_text(old_title):
                raise RuntimeError(f"Unauthorized heading-text delta: {identifier}")
            record["content_sha256"] = text_digest(region)
            record["payload"]["title_markdown"] = title
            record["payload"]["source_file_sha256"] = file_hash
            refreshed_unit_ids.add(identifier)

        baseline_units_for_file = {
            row["stable_id"]
            for row in baseline_records
            if row["entity_class"] == "unit"
            and isinstance(row.get("path"), str)
            and row["path"].startswith(relative + "#")
        }
        if expected_units != baseline_units_for_file:
            missing = sorted(baseline_units_for_file - expected_units)
            added = sorted(expected_units - baseline_units_for_file)
            raise RuntimeError(
                f"Heading stable-ID closure changed in {relative}: missing={missing}, added={added}"
            )

        active_id: str | None = None
        counters: defaultdict[str, int] = defaultdict(int)
        block: list[tuple[int, str]] = []
        expected_segments: set[str] = set()

        def flush() -> None:
            nonlocal block
            current = block
            block = []
            if not current:
                return
            if active_id is None:
                raise RuntimeError(f"Content precedes first heading in {relative}")
            first_line = current[0][0]
            content = "\n".join(line for _, line in current).strip()
            if not content or (content.startswith("<!--") and content.endswith("-->")):
                return
            counters[active_id] += 1
            segment_id = f"{active_id}.seg-{counters[active_id]:03d}"
            expected_segments.add(segment_id)
            if segment_id not in baseline_by_id:
                raise RuntimeError(f"Current segment stable ID absent from baseline: {segment_id}")
            record = baseline_by_id[segment_id]
            if record["entity_class"] != "segment" or record["parent_id"] != active_id:
                raise RuntimeError(f"Segment topology changed: {segment_id}")
            expected_locator = f"{relative}:{first_line}"
            if record["path"] != expected_locator or record["source_locator"] != expected_locator:
                raise RuntimeError(f"Segment line locator changed: {segment_id}")
            expected_type = _segment_type(content)
            if record["payload"].get("segment_type") != expected_type:
                raise RuntimeError(f"Segment type changed: {segment_id}")
            old_text = record["payload"]["markdown"]
            expected_terminology_only = authorized_text(old_text)
            if content != expected_terminology_only:
                corrections = covering_corrections(segment_id)
                if not corrections:
                    raise RuntimeError(f"Unlogged preexisting segment-text delta: {segment_id}")
                preexisting_logged_text_deltas[segment_id] = corrections
            if content != old_text:
                segment_text_changes[segment_id] = {
                    "field_replacements": len(FIELD_PATTERN.findall(old_text)),
                    "quotient_ring_replacements": len(QUOTIENT_PATTERN.findall(old_text)),
                }
            record["content_sha256"] = text_digest(content)
            record["payload"]["markdown"] = content
            refreshed_segment_ids.add(segment_id)

        for line_number, line in enumerate(lines, start=1):
            heading = HEADING_RE.match(line)
            if heading:
                flush()
                active_id = heading.group(3)
            elif not line.strip():
                flush()
            else:
                block.append((line_number, line))
        flush()

        baseline_segments_for_file = {
            row["stable_id"]
            for row in baseline_records
            if row["entity_class"] == "segment"
            and isinstance(row.get("source_locator"), str)
            and row["source_locator"].startswith(relative + ":")
        }
        if expected_segments != baseline_segments_for_file:
            missing = sorted(baseline_segments_for_file - expected_segments)
            added = sorted(expected_segments - baseline_segments_for_file)
            raise RuntimeError(
                f"Segment stable-ID closure changed in {relative}: missing={missing}, added={added}"
            )

    # Typed family projections carry the current indexed-unit hash and content
    # hash but retain their stable IDs, parents, order, paths, and family shape.
    refreshed_typed_ids: set[str] = set()
    for record in baseline_records:
        if record["entity_class"] not in {"exercise", "solution"}:
            continue
        parent_id = record.get("parent_id")
        if parent_id not in refreshed_unit_ids:
            continue
        unit = baseline_by_id[parent_id]
        record["content_sha256"] = unit["content_sha256"]
        record["provenance"]["indexed_unit_record_sha256"] = text_digest(canonical(unit))
        refreshed_typed_ids.add(record["stable_id"])

    # Refresh only the four evidence-backed terminology records already in the
    # baseline.  The Unit 7 exporter adds AGT-0051--0054 separately.
    terminology_rows = {row["term_id"]: row for row in _read_csv(terminology_path)}
    refreshed_term_ids: set[str] = set()
    refreshed_concept_ids: set[str] = set()
    for term_id in sorted(MIGRATED_TERM_IDS):
        row = terminology_rows.get(term_id)
        if row is None:
            raise RuntimeError(f"Migrated terminology row absent: {term_id}")
        stable_id = f"term.{term_id.lower()}.id-id"
        term = baseline_by_id.get(stable_id)
        if term is None or term["entity_class"] != "term":
            raise RuntimeError(f"Migrated term record absent: {stable_id}")
        row_hash = text_digest("\u241f".join(row.values()))
        term["content_sha256"] = row_hash
        term["status"] = row["status"]
        term["payload"] = {
            "source_language": row["source_language"],
            "source_term": row["source_term"],
            "preferred_target": row["preferred_target"],
            "rejected_or_variant": row["rejected_or_variant"],
            "scope": row["scope"],
            "rationale": row["rationale"],
        }
        concept_id = term["parent_id"]
        concept = baseline_by_id.get(concept_id)
        if concept is None or concept["entity_class"] != "concept":
            raise RuntimeError(f"Migrated concept record absent: {concept_id}")
        concept["content_sha256"] = row_hash
        refreshed_term_ids.add(stable_id)
        refreshed_concept_ids.add(concept_id)

    # Both lists contain the same record objects; prove that remains true.
    records_by_id = {row["stable_id"]: row for row in records}
    for stable_id, row in baseline_by_id.items():
        if records_by_id.get(stable_id) is not row:
            raise RuntimeError(f"Baseline mutation is not reflected in cumulative record list: {stable_id}")

    changed_ids = sorted(
        stable_id
        for stable_id, before in original_by_id.items()
        if before != baseline_by_id[stable_id]
    )
    changed_by_class = Counter(baseline_by_id[stable_id]["entity_class"] for stable_id in changed_ids)
    allowed_top_level = {
        "unit": {"content_sha256", "payload"},
        "segment": {"content_sha256", "payload"},
        "exercise": {"content_sha256", "provenance"},
        "solution": {"content_sha256", "provenance"},
        "term": {"content_sha256", "payload"},
        "concept": {"content_sha256"},
    }
    change_inventory: list[dict[str, Any]] = []
    for stable_id in changed_ids:
        before = original_by_id[stable_id]
        after = baseline_by_id[stable_id]
        entity_class = after["entity_class"]
        diff_keys = _top_level_diff(before, after)
        if set(diff_keys) - allowed_top_level.get(entity_class, set()):
            raise RuntimeError(
                f"Unauthorized top-level baseline change for {stable_id}: {diff_keys}"
            )
        if _structural_projection(before) != _structural_projection(after):
            raise RuntimeError(f"Prior non-text/structural record surface changed: {stable_id}")
        change_inventory.append(
            {
                "stable_id": stable_id,
                "entity_class": entity_class,
                "changed_top_level_fields": diff_keys,
                "before_record_sha256": text_digest(canonical(before)),
                "after_record_sha256": text_digest(canonical(after)),
            }
        )

    field_total = sum(row["field_replacements"] for row in segment_text_changes.values())
    quotient_total = sum(row["quotient_ring_replacements"] for row in segment_text_changes.values())
    # Counts here cover Units 1--6 only; the full 117/22 receipt also includes Unit 7.
    prior_text = "\n".join(
        (root / relative).read_text(encoding="utf-8") for relative, _ in source_rows
    )
    if FIELD_PATTERN.search(prior_text) or QUOTIENT_PATTERN.search(prior_text):
        raise RuntimeError("Old terminology remains in Units 1--6 reader source")

    inventory_json = canonical(change_inventory)
    return {
        "schema": "ag-bridge-authorized-baseline-payload-refresh-v1",
        "baseline_record_count": len(baseline_records),
        "baseline_stable_ids_preserved": True,
        "baseline_structural_projection_preserved": True,
        "changed_record_count": len(changed_ids),
        "changed_record_ids_sha256": text_digest("\n".join(changed_ids) + "\n"),
        "change_inventory_sha256": text_digest(inventory_json),
        "changed_by_class": dict(sorted(changed_by_class.items())),
        "changed_record_ids": changed_ids,
        "change_inventory": change_inventory,
        "refreshed_source_files": [relative for relative, _ in source_rows],
        "refreshed_unit_count": len(refreshed_unit_ids),
        "refreshed_segment_count": len(refreshed_segment_ids),
        "refreshed_typed_family_count": len(refreshed_typed_ids),
        "migrated_term_ids": sorted(MIGRATED_TERM_IDS),
        "migrated_term_record_ids": sorted(refreshed_term_ids),
        "migrated_concept_ids": sorted(refreshed_concept_ids),
        "changed_segment_count": len(segment_text_changes),
        "preexisting_logged_text_delta_count": len(preexisting_logged_text_deltas),
        "preexisting_logged_text_deltas": dict(sorted(preexisting_logged_text_deltas.items())),
        "prior_unit_segment_replacements": {
            "field": field_total,
            "quotient_ring": quotient_total,
        },
        "migration_receipt_path": migration_receipt_path.relative_to(root).as_posix(),
        "migration_receipt_sha256": digest(migration_receipt_path),
    }


def audit_exported_refresh(
    *,
    root: Path,
    baseline_records: list[dict[str, Any]],
    cumulative_records: list[dict[str, Any]],
    terminology_path: Path,
    migration_receipt_path: Path,
) -> dict[str, Any]:
    """Independently reconstruct and compare the authorized refreshed baseline."""

    baseline_copy = json.loads(json.dumps(baseline_records, ensure_ascii=False))
    records_copy = list(baseline_copy)
    expected = refresh_baseline(
        root=root,
        baseline_records=baseline_copy,
        records=records_copy,
        terminology_path=terminology_path,
        migration_receipt_path=migration_receipt_path,
    )
    cumulative_by_id = {row["stable_id"]: row for row in cumulative_records}
    if len(cumulative_by_id) != len(cumulative_records):
        raise RuntimeError("Duplicate stable ID in cumulative backend")
    baseline_ids = {row["stable_id"] for row in baseline_records}
    if not baseline_ids <= cumulative_by_id.keys():
        raise RuntimeError("Cumulative backend dropped prior stable IDs")
    expected_by_id = {row["stable_id"]: row for row in baseline_copy}
    mismatches = [
        stable_id
        for stable_id in sorted(baseline_ids)
        if cumulative_by_id[stable_id] != expected_by_id[stable_id]
    ]
    if mismatches:
        raise RuntimeError(f"Cumulative baseline refresh mismatch: {mismatches[:10]}")
    return expected
