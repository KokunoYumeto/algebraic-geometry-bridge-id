#!/usr/bin/env python3
"""Replay and bind the cumulative BGK Units 01--06 common-backend preflight.

The native backend and its authority/source witnesses remain read-only.  This
driver invokes the existing additive, zero-copy adapter twice with
``--preflight`` and writes only the task-local QA receipt.  A public migration
receipt is intentionally deferred until the Zenodo identity has been reserved.
"""

from __future__ import annotations

import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "qa" / "BGK_UNITS_01_06_COMMON_ADAPTER_PREFLIGHT_QA.json"
ADAPTER_PATH = "scripts/generate_common_backend_v1_receipts.py"
NATIVE_ROOT = "backend/bgk-units-01-06"
MODEL_PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."
VERIFICATION_DATE = "2026-08-29"

EXPECTED_FILES: dict[str, tuple[int, str]] = {
    f"{NATIVE_ROOT}/MANIFEST.json": (
        25100,
        "35438f7b9a1c3a833f5f6090041d3ee125fcbbc28c5ef5660579362ac2292e06",
    ),
    f"{NATIVE_ROOT}/records.jsonl": (
        4762198,
        "23e326a4a6c33abb1a4a0b10b91a673a74b056d8eb48e15a7681310d07c86986",
    ),
    "qa/BGK_UNITS_01_06_BACKEND_QA.json": (
        4164,
        "9ea9da9846590730d34ef4dc69749d0538972fef52b0f964fcefdfe9fbc80214",
    ),
    "qa/BGK_UNITS_01_06_READER_QA.json": (
        6369,
        "8c40f147451888e3ab4c2da95d164388c4f5725d37e121f020842da9488e250c",
    ),
    "qa/BGK_UNITS_01_06_VISUAL_QA.json": (
        28173,
        "3c8ed7f411124cbeb3dbaeead04b768606caa4d0789a41235b52df80806b2c68",
    ),
    "qa/BGK_UNITS_01_06_RESPONSIVE_QA.json": (
        16164,
        "755494a526f1d23e81ec797859a12dd9fb6bcea639b5dc53fada4136d7a5b0f0",
    ),
    ADAPTER_PATH: (
        85260,
        "4e0f74c3e3829e7cdbfc00d4edc33168a1b1dd25c8e7fefca0dc4b6906649dee",
    ),
    "backend/common-backend-v1-contract/upstream/backend-v1.v0.41.0.schema.json": (
        126423,
        "3de8d107b1c75db0f8d60c42ef7e3488bc3fcc93f72e955def71a771475cf2b2",
    ),
    "backend/common-backend-v1-contract/upstream/source-format-profile-v1.v0.41.0.schema.json": (
        12228,
        "2bb1429c36236329be94d58205b6123a0266a1e111277e3d303692ca8430e271",
    ),
    "backend/common-backend-v1-contract/upstream/backend-migration-receipt-v1.v0.42.0.schema.json": (
        2563,
        "0147b14972dd562805b3b5f76fac453a9f32a6d298827d3f588316d4a8f5ffe0",
    ),
    "backend/common-backend-v1-contract/upstream/MIGRATION_HANDOFF_V1.v0.42.0.md": (
        5320,
        "83de5379aa08f25fb3fb2774ed8bde99eca76e9a6ba80da9ccf2ee211e5e3a7a",
    ),
    "qa/BGK_UNITS_01_04_COMMON_ADAPTER_PREFLIGHT_QA.json": (
        2266,
        "4034ad13ab0efa3385c7392f0a8d69954b0c6cf3dfcabc9004412eef0f7e6de5",
    ),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def read_bytes(relative_path: str) -> bytes:
    path = (ROOT / relative_path).resolve()
    try:
        path.relative_to(ROOT)
    except ValueError as exc:
        raise RuntimeError(f"Path escaped lane root: {relative_path}") from exc
    return path.read_bytes()


def load_json(relative_path: str) -> dict[str, Any]:
    value = json.loads(read_bytes(relative_path))
    require(isinstance(value, dict), f"Expected JSON object: {relative_path}")
    return value


def file_fact(relative_path: str) -> dict[str, Any]:
    data = read_bytes(relative_path)
    return {"path": relative_path, "bytes": len(data), "sha256": sha256(data)}


def assert_expected_file(relative_path: str) -> dict[str, Any]:
    fact = file_fact(relative_path)
    expected_bytes, expected_sha256 = EXPECTED_FILES[relative_path]
    require(
        (fact["bytes"], fact["sha256"]) == (expected_bytes, expected_sha256),
        f"Frozen identity mismatch for {relative_path}: {fact}",
    )
    return fact


def status_is_pass(value: Any) -> bool:
    return isinstance(value, str) and value.startswith("PASS")


def normalized_stdout(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def run_preflight(native_root: str = NATIVE_ROOT) -> tuple[dict[str, Any], bytes]:
    command = [
        sys.executable,
        ADAPTER_PATH,
        "--native-backend",
        native_root,
        "--preflight",
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"Common adapter preflight failed ({completed.returncode}): {stderr}")
    stdout = normalized_stdout(completed.stdout)
    try:
        summary = json.loads(stdout)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("Common adapter preflight did not emit one UTF-8 JSON object") from exc
    require(isinstance(summary, dict), "Common adapter preflight summary is not an object")
    return summary, stdout


def main() -> int:
    facts = {path: assert_expected_file(path) for path in EXPECTED_FILES}
    adapter_data = read_bytes(ADAPTER_PATH)
    ast.parse(adapter_data.decode("utf-8"), filename=ADAPTER_PATH)

    manifest = load_json(f"{NATIVE_ROOT}/MANIFEST.json")
    backend_qa = load_json("qa/BGK_UNITS_01_06_BACKEND_QA.json")
    reader_qa = load_json("qa/BGK_UNITS_01_06_READER_QA.json")
    visual_qa = load_json("qa/BGK_UNITS_01_06_VISUAL_QA.json")
    responsive_qa = load_json("qa/BGK_UNITS_01_06_RESPONSIVE_QA.json")
    accepted_control = load_json("qa/BGK_UNITS_01_04_COMMON_ADAPTER_PREFLIGHT_QA.json")

    manifest_records = next(
        (
            item
            for item in manifest.get("files", [])
            if item.get("path") == f"{NATIVE_ROOT}/records.jsonl"
        ),
        None,
    )
    require(manifest.get("through_unit") == 6, "Native manifest is not through Unit 6")
    require(manifest.get("record_count") == 4239, "Native manifest record count changed")
    require(manifest.get("model_provenance") == MODEL_PROVENANCE, "Manifest provenance changed")
    require(
        isinstance(manifest_records, dict)
        and manifest_records.get("bytes") == facts[f"{NATIVE_ROOT}/records.jsonl"]["bytes"]
        and manifest_records.get("sha256") == facts[f"{NATIVE_ROOT}/records.jsonl"]["sha256"],
        "Native manifest does not bind the exact records.jsonl bytes",
    )

    require(backend_qa.get("status") == "PASS", "Native backend QA is not PASS")
    require(backend_qa.get("through_unit") == 6, "Native backend QA is not through Unit 6")
    require(backend_qa.get("record_count") == 4239, "Native backend QA record count changed")
    require(backend_qa.get("model_provenance") == MODEL_PROVENANCE, "Backend QA provenance changed")
    require(
        backend_qa.get("manifest_sha256") == facts[f"{NATIVE_ROOT}/MANIFEST.json"]["sha256"]
        and backend_qa.get("records_sha256") == facts[f"{NATIVE_ROOT}/records.jsonl"]["sha256"]
        and backend_qa.get("deterministic_double_replay") is True
        and backend_qa.get("all_export_file_hashes_stable") is True
        and backend_qa.get("json_schema_errors") == 0,
        "Native backend QA does not close the frozen backend",
    )

    for label, receipt in (
        ("reader", reader_qa),
        ("visual", visual_qa),
        ("responsive", responsive_qa),
    ):
        require(receipt.get("through_unit") == 6, f"{label} QA is not through Unit 6")
        require(status_is_pass(receipt.get("status")), f"{label} QA is not PASS")
        require(receipt.get("model_provenance") == MODEL_PROVENANCE, f"{label} QA provenance changed")
    require(
        (backend_qa.get("reader") or {}).get("qa_sha256")
        == facts["qa/BGK_UNITS_01_06_READER_QA.json"]["sha256"],
        "Native backend QA does not bind the exact reader QA receipt",
    )
    require(
        (visual_qa.get("bound_responsive_qa") or {}).get("sha256")
        == facts["qa/BGK_UNITS_01_06_RESPONSIVE_QA.json"]["sha256"],
        "Visual QA does not bind the exact responsive QA receipt",
    )

    require(accepted_control.get("status") == "PASS", "Accepted adapter control is not PASS")
    require(
        status_is_pass((accepted_control.get("classical_regression") or {}).get("status")),
        "Accepted classical-regression control is not PASS",
    )

    first, first_stdout = run_preflight()
    second, second_stdout = run_preflight()
    require(first == second, "Common adapter double replay produced different JSON objects")
    require(first_stdout == second_stdout, "Common adapter double replay produced different stdout bytes")
    require(first.get("status") == "PASS", "Common adapter summary is not PASS")
    require(first.get("native_records") == 4239, "Common adapter native record count changed")
    require(
        first.get("reverse_sha256") == facts[f"{NATIVE_ROOT}/records.jsonl"]["sha256"],
        "Lossless reverse does not reproduce native records.jsonl",
    )
    require(int(first.get("strict_profiles", 0)) > 0, "No strict profiles were bound")
    require(
        int(first.get("strict_profile_witness_files", 0)) > 0,
        "No strict-profile witness files were bound",
    )
    require(int(first.get("foreign_keys_checked", 0)) > 0, "No foreign keys were checked")

    classical_first, classical_first_stdout = run_preflight("backend/units-01-30")
    classical_second, classical_second_stdout = run_preflight("backend/units-01-30")
    require(classical_first == classical_second and classical_first_stdout == classical_second_stdout,
            "Classical common-backend regression replay is nondeterministic")
    accepted_classical = accepted_control["classical_regression"]
    require(classical_first.get("status") == "PASS", "Classical common-backend regression is not PASS")
    require(classical_first.get("native_records") == accepted_classical["native_records"],
            "Classical native record count changed")
    require(classical_first.get("common_records") == accepted_classical["accepted_common_records"],
            "Classical common record count changed")
    require(classical_first.get("virtual_sha256") == accepted_classical["accepted_virtual_sha256"],
            "Classical virtual projection changed")
    require(classical_first.get("reverse_sha256") == accepted_classical["accepted_lossless_reverse_sha256"],
            "Classical lossless reverse changed")

    contract_paths = [
        path for path in EXPECTED_FILES if path.startswith("backend/common-backend-v1-contract/")
    ]
    final_evidence_paths = [
        "qa/BGK_UNITS_01_06_BACKEND_QA.json",
        "qa/BGK_UNITS_01_06_READER_QA.json",
        "qa/BGK_UNITS_01_06_VISUAL_QA.json",
        "qa/BGK_UNITS_01_06_RESPONSIVE_QA.json",
    ]
    projection = {
        "native_records": first["native_records"],
        "common_records": first["common_records"],
        "strict_profiles": first["strict_profiles"],
        "strict_profile_witness_files": first["strict_profile_witness_files"],
        "foreign_keys_checked": first["foreign_keys_checked"],
        "virtual_bytes": first["virtual_bytes"],
        "virtual_sha256": first["virtual_sha256"],
        "lossless_reverse_sha256": first["reverse_sha256"],
        "double_preflight_stdout_identical": True,
        "double_preflight_stdout_sha256": sha256(first_stdout),
        "stdout_normalization": "CRLF normalized to LF before byte comparison",
    }
    receipt = {
        "schema": "ag-bridge-common-backend-v1-preflight-qa-v1",
        "scope": "BGK Units 01-06 cumulative native backend",
        "language": "id-ID",
        "status": "PASS",
        "verification_date": VERIFICATION_DATE,
        "model_provenance": MODEL_PROVENANCE,
        "preflight_driver": file_fact(Path(__file__).relative_to(ROOT).as_posix()),
        "adapter": {
            **facts[ADAPTER_PATH],
            "syntax_parse": "PASS",
            "mode": "additive zero-copy adapter",
            "native_records_mutated": False,
        },
        "contract": [facts[path] for path in contract_paths],
        "native_backend": {
            "path": NATIVE_ROOT,
            "records": manifest["record_count"],
            "records_bytes": facts[f"{NATIVE_ROOT}/records.jsonl"]["bytes"],
            "records_sha256": facts[f"{NATIVE_ROOT}/records.jsonl"]["sha256"],
            "manifest_bytes": facts[f"{NATIVE_ROOT}/MANIFEST.json"]["bytes"],
            "manifest_sha256": facts[f"{NATIVE_ROOT}/MANIFEST.json"]["sha256"],
            "native_qa_path": "qa/BGK_UNITS_01_06_BACKEND_QA.json",
            "native_qa_bytes": facts["qa/BGK_UNITS_01_06_BACKEND_QA.json"]["bytes"],
            "native_qa_sha256": facts["qa/BGK_UNITS_01_06_BACKEND_QA.json"]["sha256"],
        },
        "final_qa_evidence": [
            {
                **facts[path],
                "status": load_json(path)["status"],
            }
            for path in final_evidence_paths
        ],
        "common_projection": projection,
        "classical_regression": {
            "status": "PASS_UNCHANGED_ACCEPTED_BASELINE",
            "method": "two deterministic replays against the exact accepted classical Units 01-30 native backend",
            "accepted_control": facts["qa/BGK_UNITS_01_04_COMMON_ADAPTER_PREFLIGHT_QA.json"],
            "accepted_baseline": accepted_classical,
            "current_adapter": facts[ADAPTER_PATH],
            "current_result": classical_first,
            "double_preflight_stdout_identical": True,
            "double_preflight_stdout_sha256": sha256(classical_first_stdout),
        },
        "checks": {
            "adapter_and_contract_identities_match": True,
            "common_schema_valid": True,
            "strict_profiles_valid": True,
            "witnesses_bound": True,
            "all_foreign_keys_closed": True,
            "lossless_native_round_trip": True,
            "deterministic_double_preflight": True,
            "frozen_native_input_identities_match": True,
            "final_qa_evidence_identities_and_statuses_match": True,
            "accepted_classical_regression_replayed_and_unchanged": True,
            "final_migration_receipt_deferred_until_zenodo_reservation_exists": True,
        },
        "migration_receipt": {
            "emitted": False,
            "reason": "Public Zenodo record identity has not yet been reserved.",
        },
        "credentials_recorded": False,
    }
    output = (json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    OUTPUT_PATH.write_bytes(output)
    require(OUTPUT_PATH.read_bytes() == output, "Preflight QA receipt write/readback mismatch")
    print(
        json.dumps(
            {
                "status": "PASS",
                "output": file_fact(OUTPUT_PATH.relative_to(ROOT).as_posix()),
                "projection": projection,
            },
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
