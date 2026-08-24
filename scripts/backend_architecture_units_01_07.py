#!/usr/bin/env python3
"""Apply the controlling two-volume O016/D100 backend architecture.

This adapter changes no reader/source authority and renames no record.  It
updates three stale Unit 1 architecture records, retains Napkin as optional
evidence, and adds the required BGK resource, rights, and course relation.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


COURSE_ID = "course.o016-d100.algebraic-geometry-bridge"
CLASSICAL_RESOURCE_ID = "resource.brenner.algebraische-kurven.2025-2026"
BGK_RESOURCE_ID = "resource.brenner.buendel-garben-kohomologie.2019-2020"
BGK_RIGHTS_ID = "rights.brenner-bgk-course-text.cc-by-sa-4.0"
BGK_RELATION_ID = "relation.units0107.architecture-bgk-required"
NAPKIN_RESOURCE_ID = "resource.chen.infinitely-large-napkin"
NAPKIN_RELATION_ID = "relation.unit01.0003"
LOCAL_RESOURCE_ID = "resource.algebraic-geometry-bridge-id.editorial-layer"
EDITORIAL_RIGHTS_ID = "rights.derivative-editorial.cc-by-sa-4.0"
CUMULATIVE_EDITION_ID = "edition.algebraic-geometry-bridge-id.units-01-07.2026-08-22"
WORKFLOW_ID = "workflow.o016-d100.algebraic-geometry-bridge-id"
SCHEMA = "ag-bridge-backend-record"
SCHEMA_VERSION = "1.0.0"
DECISION_RELATIVE = "00_control/SCHEME_BRIDGE_DECISION.md"
DECISION_BYTES = 3549
DECISION_SHA256 = "edbbec013ed190cfd33a08d5901aeda3d94d4c068e39ed8d7d0888f8adb213f2"
GOAL_RELATIVE = "00_control/CURRENT_GOAL_AND_WORKFLOW.md"
HANDOFF_WORKSPACE_RELATIVE = (
    "outputs/01a01ec1-e685-70d0-b022-211396334723/curriculum_logbook/"
    "43_O016_SELECTION_AND_EXISTING_TASK_HANDOFF_20260822.md"
)
HANDOFF_BYTES = 12781
HANDOFF_SHA256 = "6128f2637fafc55772483e01eb38c23cff79490d614045936edb8b41cd56c851"
BGK_URL = (
    "https://de.wikiversity.org/wiki/"
    "Kurs:B%C3%BCndel,_Garben_und_Kohomologie_(Osnabr%C3%BCck_2019-2020)"
)
BRENNER_LICENSE_URL = (
    "https://de.wikiversity.org/wiki/"
    "Holger_Brenner/Lizenzerkl%C3%A4rung?oldid=1073083"
)
BGK_ROUTE_UNITS = [*range(2, 16), *range(23, 28)]


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def text_digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def make_record(
    entity_class: str,
    stable_id: str,
    *,
    timestamp: str,
    source_local_id: str | None = None,
    parent_id: str | None = None,
    order: int | None = None,
    path: str | None = None,
    resource_id: str | None = None,
    edition_id: str | None = None,
    source_locator: str | None = None,
    content_sha256: str | None = None,
    language: str = "und",
    translation_state: str = "source_frozen",
    provenance: dict[str, Any] | None = None,
    concept_ids: list[str] | None = None,
    prerequisite_ids: list[str] | None = None,
    rights_id: str | None = None,
    status: str = "active",
    supersedes: str | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "entity_class": entity_class,
        "stable_id": stable_id,
        "source_local_id": source_local_id,
        "parent_id": parent_id,
        "order": order,
        "path": path,
        "resource_id": resource_id,
        "edition_id": edition_id,
        "source_locator": source_locator,
        "content_sha256": content_sha256,
        "language": language,
        "translation_state": translation_state,
        "provenance": provenance or {},
        "concept_ids": sorted(set(concept_ids or [])),
        "prerequisite_ids": sorted(set(prerequisite_ids or [])),
        "rights_id": rights_id,
        "status": status,
        "timestamp": timestamp,
        "responsible_workflow": WORKFLOW_ID,
        "supersedes": supersedes,
        "payload": payload or {},
    }


def _changed_fields(before: dict[str, Any], after: dict[str, Any]) -> list[str]:
    return sorted(key for key in before if before[key] != after[key])


def _changed_payload_fields(before: dict[str, Any], after: dict[str, Any]) -> list[str]:
    before_payload = before.get("payload", {})
    after_payload = after.get("payload", {})
    return sorted(
        key
        for key in set(before_payload) | set(after_payload)
        if before_payload.get(key) != after_payload.get(key)
    )


def apply_architecture_correction(
    *, root: Path, records: list[dict[str, Any]], timestamp: str
) -> dict[str, Any]:
    """Apply and inventory the exact controlling architecture correction."""

    decision_path = root / DECISION_RELATIVE
    workspace_root = root.parents[2]
    handoff_path = workspace_root / HANDOFF_WORKSPACE_RELATIVE
    decision_sha = digest(decision_path)
    if decision_path.stat().st_size != DECISION_BYTES or decision_sha != DECISION_SHA256:
        raise RuntimeError("Immutable local architecture decision identity changed")
    if handoff_path.is_file():
        if handoff_path.stat().st_size != HANDOFF_BYTES:
            raise RuntimeError("Controlling O016 handoff byte count changed")
        if digest(handoff_path) != HANDOFF_SHA256:
            raise RuntimeError("Controlling O016 handoff SHA-256 changed")
    by_id = {row["stable_id"]: row for row in records}
    if len(by_id) != len(records):
        raise RuntimeError("Duplicate stable ID before architecture correction")

    required_existing = {COURSE_ID, NAPKIN_RESOURCE_ID, NAPKIN_RELATION_ID}
    missing = sorted(required_existing - by_id.keys())
    if missing:
        raise RuntimeError(f"Required architecture baseline records absent: {missing}")
    forbidden_existing = {BGK_RESOURCE_ID, BGK_RIGHTS_ID, BGK_RELATION_ID} & by_id.keys()
    if forbidden_existing:
        raise RuntimeError(f"BGK architecture records already exist: {sorted(forbidden_existing)}")

    originals = {
        stable_id: json.loads(canonical(by_id[stable_id]))
        for stable_id in sorted(required_existing)
    }
    decision_binding = {
        "architecture_decision_path": DECISION_RELATIVE,
        "architecture_decision_sha256": decision_sha,
        "goal_path": GOAL_RELATIVE,
        "controlling_handoff_workspace_path": HANDOFF_WORKSPACE_RELATIVE,
        "controlling_handoff_bytes": HANDOFF_BYTES,
        "controlling_handoff_sha256": HANDOFF_SHA256,
    }

    course = by_id[COURSE_ID]
    course["content_sha256"] = HANDOFF_SHA256
    course["provenance"] = {**course.get("provenance", {}), **decision_binding}
    course["payload"] = {
        **course.get("payload", {}),
        "role": "Algebraic Geometry Bridge",
        "dominant_spine": (
            "Holger Brenner, Algebraische Kurven (Osnabrück 2025–2026), followed by "
            "Bündel, Garben und Kohomologie (Osnabrück 2019–2020)"
        ),
        "bounded_extent": (
            "complete 30-lecture/30-worksheet classical volume; complete "
            "30-lecture/30-worksheet BGK second volume; concentrated BGK Units "
            "2–15 and 23–27 route; original seam, mastery, integration, and capstone"
        ),
        "curriculum_admission": "two_volume_brenner_architecture_selected",
        "classical_volume_resource_id": CLASSICAL_RESOURCE_ID,
        "required_second_volume_resource_id": BGK_RESOURCE_ID,
        "concentrated_bgk_route_units": BGK_ROUTE_UNITS,
        "original_layer": {
            "terminology_and_prerequisite_seam": True,
            "worked_mastery_items_per_route_unit": 3,
            "solved_integrative_problems": 12,
            "stacks_navigation_capstone": True,
            "oral_proof_rubric": True,
        },
        "napkin_disposition": "optional reference evidence only; never a required donor or dependency",
    }

    napkin = by_id[NAPKIN_RESOURCE_ID]
    napkin["provenance"] = {**napkin.get("provenance", {}), **decision_binding}
    napkin["payload"] = {
        **napkin["payload"],
        "use_in_lane": "optional explanation and comparison evidence only",
        "required_course_material": False,
        "required_donor": False,
        "required_dependency": False,
    }
    napkin["content_sha256"] = text_digest(canonical(napkin["payload"]))

    napkin_relation = by_id[NAPKIN_RELATION_ID]
    napkin_relation["content_sha256"] = text_digest(
        f"optional_reference\u241f{COURSE_ID}\u241f{NAPKIN_RESOURCE_ID}"
    )
    napkin_relation["provenance"] = {
        **napkin_relation.get("provenance", {}),
        **decision_binding,
    }
    napkin_relation["payload"] = {
        "relation_type": "optional_reference",
        "subject_id": COURSE_ID,
        "object_id": NAPKIN_RESOURCE_ID,
        "scope": "frozen Part XX explanation/comparison evidence only; never required course material, donor, or dependency",
    }

    bgk_resource = make_record(
        "resource",
        BGK_RESOURCE_ID,
        timestamp=timestamp,
        source_local_id="Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)",
        source_locator=BGK_URL,
        content_sha256=None,
        language="de",
        translation_state="queued",
        provenance=decision_binding,
        rights_id=BGK_RIGHTS_ID,
        status="required_second_volume_pending_complete_authority_freeze",
        payload={
            "title": "Bündel, Garben und Kohomologie (Osnabrück 2019–2020)",
            "creator": "Holger Brenner",
            "host": "German Wikiversity",
            "role_in_lane": "required complete second volume",
            "observed_course_root_revision": 1052895,
            "lecture_count": 30,
            "worksheet_count": 30,
            "required_complete_source_order": True,
            "concentrated_route_units": BGK_ROUTE_UNITS,
            "concentrated_route_unit_count": 19,
            "official_pdf": {
                "role": "visual/build witness pending complete live authority freeze",
                "pages": 265,
                "bytes": 2104862,
                "sha256": "87655cf7e96dc0eaa185ca49a374dc9e25f4b739670495f423279aa332fce66c",
            },
            "exercise_surface_observed": 495,
            "public_solution_surface_observed": 25,
            "authority_state": "complete byte-level MediaWiki freeze not yet performed",
        },
    )
    bgk_rights = make_record(
        "rights",
        BGK_RIGHTS_ID,
        timestamp=timestamp,
        source_local_id="Holger Brenner license declaration",
        resource_id=BGK_RESOURCE_ID,
        source_locator=BRENNER_LICENSE_URL,
        content_sha256=None,
        language="de",
        translation_state="queued",
        provenance=decision_binding,
        status="pending_complete_authority_freeze",
        payload={
            "license": "CC BY-SA 4.0",
            "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
            "creator": "Holger Brenner",
            "scope": "BGK course text and semantic course pages; Commons media excluded",
            "attribution_required": True,
            "share_alike_required": True,
            "component_media_rights_separate": True,
            "authority_state": "license declaration observed; byte-level freeze pending",
        },
    )
    bgk_relation = make_record(
        "relation",
        BGK_RELATION_ID,
        timestamp=timestamp,
        order=333,
        resource_id=LOCAL_RESOURCE_ID,
        edition_id=CUMULATIVE_EDITION_ID,
        source_locator=DECISION_RELATIVE,
        content_sha256=text_digest(
            f"requires_complete_volume\u241f{COURSE_ID}\u241f{BGK_RESOURCE_ID}"
        ),
        translation_state="built",
        provenance=decision_binding,
        rights_id=EDITORIAL_RIGHTS_ID,
        payload={
            "relation_type": "requires_complete_volume",
            "subject_id": COURSE_ID,
            "object_id": BGK_RESOURCE_ID,
            "scope": "all 30 BGK lectures and 30 worksheets in source order",
            "concentrated_route_units": BGK_ROUTE_UNITS,
            "original_connective_layer_required": True,
        },
    )
    records.extend([bgk_resource, bgk_rights, bgk_relation])

    changed_existing: list[dict[str, Any]] = []
    for stable_id in sorted(required_existing):
        before = originals[stable_id]
        after = by_id[stable_id]
        changed_existing.append(
            {
                "stable_id": stable_id,
                "changed_top_level_fields": _changed_fields(before, after),
                "changed_payload_fields": _changed_payload_fields(before, after),
                "before_record_sha256": text_digest(canonical(before)),
                "after_record_sha256": text_digest(canonical(after)),
            }
        )

    added = [bgk_resource, bgk_rights, bgk_relation]
    return {
        "schema": "ag-bridge-two-volume-architecture-correction-v1",
        "decision_path": DECISION_RELATIVE,
        "decision_sha256": decision_sha,
        "goal_path": GOAL_RELATIVE,
        "controlling_handoff_workspace_path": HANDOFF_WORKSPACE_RELATIVE,
        "controlling_handoff_bytes": HANDOFF_BYTES,
        "controlling_handoff_sha256": HANDOFF_SHA256,
        "existing_stable_ids_preserved": True,
        "changed_existing_record_count": len(changed_existing),
        "changed_existing_records": changed_existing,
        "added_record_count": len(added),
        "added_records": [
            {
                "stable_id": row["stable_id"],
                "entity_class": row["entity_class"],
                "record_sha256": text_digest(canonical(row)),
            }
            for row in added
        ],
        "napkin_required_dependency_count": 0,
        "required_bgk_relation_id": BGK_RELATION_ID,
        "required_bgk_route_units": BGK_ROUTE_UNITS,
    }


def audit_architecture_export(
    *,
    root: Path,
    terminology_refreshed_baseline: list[dict[str, Any]],
    cumulative_records: list[dict[str, Any]],
    timestamp: str,
) -> dict[str, Any]:
    """Reconstruct the architecture delta and compare every affected record."""

    expected_records = json.loads(json.dumps(terminology_refreshed_baseline, ensure_ascii=False))
    summary = apply_architecture_correction(
        root=root,
        records=expected_records,
        timestamp=timestamp,
    )
    expected_by_id = {row["stable_id"]: row for row in expected_records}
    cumulative_by_id = {row["stable_id"]: row for row in cumulative_records}
    if len(expected_by_id) != len(expected_records):
        raise RuntimeError("Duplicate stable ID in reconstructed architecture export")
    if len(cumulative_by_id) != len(cumulative_records):
        raise RuntimeError("Duplicate stable ID in cumulative architecture export")
    protected_ids = set(row["stable_id"] for row in terminology_refreshed_baseline)
    protected_ids.update(row["stable_id"] for row in summary["added_records"])
    mismatches = [
        stable_id
        for stable_id in sorted(protected_ids)
        if cumulative_by_id.get(stable_id) != expected_by_id.get(stable_id)
    ]
    if mismatches:
        raise RuntimeError(f"Architecture export mismatch: {mismatches[:10]}")
    return summary
