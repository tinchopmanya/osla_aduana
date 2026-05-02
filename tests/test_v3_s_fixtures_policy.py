from __future__ import annotations

import json
import re
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "fixtures" / "v3_s"

SAFE_TEXT_MARKERS = (
    "synthetic",
    "sintet",
    "fixture",
    "redacted",
    "fake",
    "dummy",
    "example",
)
SAFE_ID_MARKERS = SAFE_TEXT_MARKERS + ("_syn_", "syn_")

EXECUTABLE_URL_RE = re.compile(
    r"\b(?:https?|ftp|ftps|sftp)://[^\s\"'<>]+",
    re.IGNORECASE,
)
REAL_NETWORK_REF_RE = re.compile(
    r"\b(?:ftp\.)?aduanas\.gub\.uy\b|\b(?:lucia|vuce)\.[a-z0-9.-]+\b",
    re.IGNORECASE,
)
STORAGE_URL_RE = re.compile(
    r"\b(?:s3|gs|az|abfs|wasbs|dbfs)://[^\s\"'<>]+",
    re.IGNORECASE,
)
REAL_PATH_RE = re.compile(
    r"(?:[A-Za-z]:\\|\\\\[^\\]+\\|/(?:var|etc|home|mnt|data|tmp|opt|srv)/)",
    re.IGNORECASE,
)
SQL_WRITE_RE = re.compile(
    r"\b(?:insert\s+into|update\s+[a-z0-9_.]+\s+set|delete\s+from|"
    r"create\s+table|drop\s+table|alter\s+table|copy\s+[a-z0-9_.]+\s+from)\b",
    re.IGNORECASE,
)
SECRET_VALUE_RE = re.compile(
    r"(?:Bearer\s+[A-Za-z0-9._~+/=-]+|Basic\s+[A-Za-z0-9+/=]+|"
    r"AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9_]{20,}|"
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----)",
    re.IGNORECASE,
)
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
MATERIAL_PROCESSING_RE = re.compile(
    r"\b(?:ocr_completed|ocr_extracted|ocr_used|ocr_pages_processed|"
    r"embedding(?:s)?_generated|embedding(?:s)?_created|text-embedding|"
    r"vector_store|vector_index|faiss|pinecone|weaviate)\b",
    re.IGNORECASE,
)

FORBIDDEN_TRUE_KEYS = {
    "network_allowed",
    "ftp_allowed",
    "ftp_real_allowed",
    "metadata_preflight_allowed",
    "download_allowed",
    "db_writes_allowed",
    "database_writes_allowed",
    "storage_writes_allowed",
    "ocr_allowed",
    "ocr_used",
    "embedding_allowed",
    "embeddings_allowed",
    "embedding_used",
    "embeddings_used",
    "real_source_touched",
    "real_vendor_touched",
    "external_source_touched",
    "real_data_used",
    "auto_decided",
    "automatic_decision",
    "auto_approved",
    "approved_automatically",
    "final_decision_allowed",
}
ZERO_ONLY_KEYS = {
    "files_downloaded",
    "bytes_downloaded",
    "bytes_uploaded",
    "bytes_written",
    "db_rows_inserted",
    "rows_inserted",
    "rows_updated",
    "rows_deleted",
    "records_written",
    "storage_objects_written",
    "ocr_pages_processed",
    "embeddings_created",
    "embeddings_generated",
    "vectors_written",
}
FINAL_DECISION_KEYS = {
    "ncm_final",
    "regime_final",
    "regimen_final",
    "final_ncm",
    "final_regime",
    "final_regimen",
}
FORBIDDEN_VOICE_ACTIONS = {
    "change_ncm_final",
    "submit_customs_declaration",
    "approve_operation",
    "change_costs",
    "release_goods",
    "send_legal_instruction_without_review",
    "delete_document",
    "access_reserved_dna_or_vuce",
}
DENIED_OR_ESCALATED = {"denied", "escalated"}


def test_v3_s_fixture_pack_exists_with_json_files() -> None:
    assert FIXTURE_DIR.is_dir(), (
        "fixtures/v3_s is required for V3-S validation. "
        "It is currently missing; this is the open Aduana Fixture Builder gap."
    )

    json_files = sorted(FIXTURE_DIR.glob("*.json"))
    assert json_files, (
        "fixtures/v3_s exists but has no direct *.json files. "
        "V3-S expects synthetic JSON fixtures under fixtures/v3_s/*.json."
    )


def test_v3_s_fixture_json_files_are_valid_objects() -> None:
    for fixture_path, payload in _loaded_fixtures():
        assert isinstance(payload, (dict, list)), (
            f"{fixture_path} must contain a JSON object or list of objects, "
            "not a scalar value."
        )


def test_v3_s_fixtures_are_explicitly_synthetic() -> None:
    failures: list[str] = []

    for fixture_path, payload in _loaded_fixtures():
        markers = 0

        for json_path, obj in _walk_objects(payload):
            source_context = obj.get("source_context")
            if isinstance(source_context, dict):
                markers += 1
                if source_context.get("is_synthetic") is not True:
                    failures.append(f"{fixture_path}:{json_path}.source_context.is_synthetic must be true")

            synthetic = obj.get("synthetic")
            if isinstance(synthetic, dict):
                markers += 1
                if synthetic.get("is_synthetic") is not True:
                    failures.append(f"{fixture_path}:{json_path}.synthetic.is_synthetic must be true")
                for key in ("real_source_touched", "real_vendor_touched"):
                    if key in synthetic and synthetic[key] is not False:
                        failures.append(f"{fixture_path}:{json_path}.synthetic.{key} must be false")

            if obj.get("mode") == "synthetic_fixture":
                markers += 1

        if markers == 0:
            failures.append(f"{fixture_path} has no synthetic marker")

    _assert_no_failures(failures)


def test_v3_s_fixture_ids_are_clearly_synthetic() -> None:
    failures: list[str] = []

    for fixture_path, payload in _loaded_fixtures():
        for json_path, key, value in _walk_key_values(payload):
            norm_key = _norm_key(key)
            if norm_key not in {
                "id",
                "tenant_id",
                "trade_case_id",
                "assessment_id",
                "source_manifest_id",
                "evidence_pack_id",
                "evidence_item_id",
                "linked_evidence_item_id",
                "created_task_id",
                "conversation_id",
                "run_id",
                "source_id",
            }:
                continue

            if value is None:
                continue

            if not isinstance(value, str):
                failures.append(f"{fixture_path}:{json_path}.{key} must be a string or null")
                continue

            if norm_key == "source_id" and value == "uy.dna.public_ftp":
                continue

            if not _has_safe_marker(value):
                failures.append(
                    f"{fixture_path}:{json_path}.{key}={value!r} is not marked as synthetic/redacted"
                )

    _assert_no_failures(failures)


def test_v3_s_fixtures_do_not_contain_executable_urls_or_real_network_refs() -> None:
    failures: list[str] = []

    for fixture_path, payload in _loaded_fixtures():
        for json_path, value in _walk_strings(payload):
            if EXECUTABLE_URL_RE.search(value):
                failures.append(f"{fixture_path}:{json_path} contains an executable URL")

            if REAL_NETWORK_REF_RE.search(value):
                failures.append(f"{fixture_path}:{json_path} contains a real network/source reference")

    _assert_no_failures(failures)


def test_v3_s_fixtures_do_not_contain_credentials_or_real_identity_data() -> None:
    failures: list[str] = []

    for fixture_path, payload in _loaded_fixtures():
        for json_path, key, value in _walk_key_values(payload):
            norm_key = _norm_key(key)

            if _looks_like_credential_key(norm_key) and not _empty_false_or_redacted(value):
                failures.append(f"{fixture_path}:{json_path}.{key} contains a credential-like field")

            if isinstance(value, str):
                if SECRET_VALUE_RE.search(value):
                    failures.append(f"{fixture_path}:{json_path}.{key} contains a secret-like value")

                if EMAIL_RE.search(value) and not _email_value_is_safe(value):
                    failures.append(f"{fixture_path}:{json_path}.{key} contains a non-fixture email")

                if _looks_like_identity_key(norm_key) and not _identity_value_is_safe(value):
                    failures.append(
                        f"{fixture_path}:{json_path}.{key}={value!r} is not marked synthetic/redacted"
                    )

    _assert_no_failures(failures)


def test_v3_s_fixtures_do_not_enable_material_io_or_processing() -> None:
    failures: list[str] = []

    for fixture_path, payload in _loaded_fixtures():
        for json_path, key, value in _walk_key_values(payload):
            norm_key = _norm_key(key)

            if norm_key in FORBIDDEN_TRUE_KEYS and _truthy_material_value(value):
                failures.append(f"{fixture_path}:{json_path}.{key} must be false/null/offline")

            if norm_key in ZERO_ONLY_KEYS and _positive_number(value):
                failures.append(f"{fixture_path}:{json_path}.{key} must be 0")

            if isinstance(value, str) and MATERIAL_PROCESSING_RE.search(value):
                failures.append(f"{fixture_path}:{json_path}.{key} references OCR/embeddings/vector processing")

    _assert_no_failures(failures)


def test_v3_s_fixtures_do_not_contain_db_storage_writes_or_real_paths() -> None:
    failures: list[str] = []

    for fixture_path, payload in _loaded_fixtures():
        for json_path, value in _walk_strings(payload):
            if STORAGE_URL_RE.search(value):
                failures.append(f"{fixture_path}:{json_path} contains a storage URL/path")

            if REAL_PATH_RE.search(value):
                failures.append(f"{fixture_path}:{json_path} contains a real filesystem/storage path")

            if SQL_WRITE_RE.search(value):
                failures.append(f"{fixture_path}:{json_path} contains SQL write text")

    _assert_no_failures(failures)


def test_v3_s_fixtures_never_write_final_ncm_or_regime() -> None:
    failures: list[str] = []

    for fixture_path, payload in _loaded_fixtures():
        for json_path, key, value in _walk_key_values(payload):
            norm_key = _norm_key(key)

            if norm_key in FINAL_DECISION_KEYS and value is not None:
                failures.append(f"{fixture_path}:{json_path}.{key} must be null")

            if json_path.endswith(".final_decision") and norm_key == "decided_by" and value is not None:
                failures.append(f"{fixture_path}:{json_path}.{key} must be null")

    _assert_no_failures(failures)


def test_v3_s_forbidden_voice_actions_are_denied_or_escalated() -> None:
    failures: list[str] = []

    for fixture_path, payload in _loaded_fixtures():
        for json_path, obj in _walk_objects(payload):
            action = obj.get("normalized_action")
            if action not in FORBIDDEN_VOICE_ACTIONS:
                continue

            status = obj.get("action_status")
            if status not in DENIED_OR_ESCALATED:
                failures.append(
                    f"{fixture_path}:{json_path} has forbidden action {action!r} "
                    f"with action_status={status!r}; expected denied/escalated"
                )

    _assert_no_failures(failures)


def test_v3_s_source_manifests_block_material_access() -> None:
    failures: list[str] = []

    for fixture_path, payload in _loaded_fixtures():
        for json_path, obj in _walk_objects(payload):
            if not _looks_like_source_manifest(obj):
                continue

            if obj.get("mode") != "synthetic_fixture":
                failures.append(f"{fixture_path}:{json_path}.mode must be synthetic_fixture")

            if obj.get("files_downloaded") != 0:
                failures.append(f"{fixture_path}:{json_path}.files_downloaded must be 0")

            if obj.get("bytes_downloaded") != 0:
                failures.append(f"{fixture_path}:{json_path}.bytes_downloaded must be 0")

            if obj.get("source_id") == "uy.dna.public_ftp" and obj.get("state") != "blocked_until_prereqs_closed":
                failures.append(
                    f"{fixture_path}:{json_path}.state must be blocked_until_prereqs_closed "
                    "for uy.dna.public_ftp"
                )

            policy = obj.get("source_policy")
            if not isinstance(policy, dict):
                failures.append(f"{fixture_path}:{json_path}.source_policy must be present")
                continue

            for flag in ("network_allowed", "db_writes_allowed", "storage_writes_allowed"):
                if policy.get(flag) is not False:
                    failures.append(f"{fixture_path}:{json_path}.source_policy.{flag} must be false")

            for optional_flag in ("metadata_preflight_allowed", "download_allowed"):
                if optional_flag in policy and policy[optional_flag] is not False:
                    failures.append(f"{fixture_path}:{json_path}.source_policy.{optional_flag} must be false")

            if policy.get("denylist_applied") is not True:
                failures.append(f"{fixture_path}:{json_path}.source_policy.denylist_applied must be true")

    _assert_no_failures(failures)


def _fixture_files_or_skip() -> list[Path]:
    if not FIXTURE_DIR.is_dir():
        pytest.skip("fixtures/v3_s is not present yet; Aduana Fixture Builder gap")

    fixture_files = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixture_files:
        pytest.skip("fixtures/v3_s has no direct *.json files yet; Aduana Fixture Builder gap")

    return fixture_files


def _loaded_fixtures() -> Iterator[tuple[Path, Any]]:
    for fixture_path in _fixture_files_or_skip():
        try:
            yield fixture_path, json.loads(fixture_path.read_text(encoding="utf-8"))
        except UnicodeDecodeError as exc:
            pytest.fail(f"{fixture_path} must be UTF-8 JSON: {exc}")
        except json.JSONDecodeError as exc:
            pytest.fail(f"{fixture_path} is not valid JSON: {exc}")


def _walk(value: Any, json_path: str = "$") -> Iterator[tuple[str, Any]]:
    yield json_path, value

    if isinstance(value, dict):
        for key, child in value.items():
            yield from _walk(child, f"{json_path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, f"{json_path}[{index}]")


def _walk_objects(value: Any) -> Iterator[tuple[str, dict[str, Any]]]:
    for json_path, node in _walk(value):
        if isinstance(node, dict):
            yield json_path, node


def _walk_strings(value: Any) -> Iterator[tuple[str, str]]:
    for json_path, node in _walk(value):
        if isinstance(node, str):
            yield json_path, node


def _walk_key_values(value: Any) -> Iterator[tuple[str, str, Any]]:
    for json_path, node in _walk(value):
        if isinstance(node, dict):
            for key, child in node.items():
                yield json_path, str(key), child


def _norm_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", key.lower()).strip("_")


def _has_safe_marker(value: str) -> bool:
    lower = value.lower()
    return any(marker in lower for marker in SAFE_ID_MARKERS)


def _looks_like_credential_key(norm_key: str) -> bool:
    return any(
        marker in norm_key
        for marker in (
            "password",
            "passwd",
            "secret",
            "token",
            "api_key",
            "apikey",
            "access_key",
            "private_key",
            "credential",
            "cookie",
            "authorization",
            "bearer",
        )
    )


def _looks_like_identity_key(norm_key: str) -> bool:
    return norm_key in {
        "display_name",
        "party_name",
        "company_name",
        "empresa",
        "razon_social",
        "tax_id",
        "tax_id_ref",
        "rut",
        "ci",
        "document_number",
        "email",
        "phone",
        "telefono",
        "address",
        "direccion",
    }


def _empty_false_or_redacted(value: Any) -> bool:
    if value in (None, False, 0, ""):
        return True
    if isinstance(value, str):
        lower = value.lower()
        return lower in {"none", "null", "redacted", "synthetic_redacted", "not_applicable"} or _has_safe_marker(value)
    return False


def _identity_value_is_safe(value: str) -> bool:
    if value == "":
        return True
    return _has_safe_marker(value)


def _email_value_is_safe(value: str) -> bool:
    if _has_safe_marker(value):
        return True
    return all(
        match.group(0).lower().endswith(("@example.com", "@example.invalid", "@test.invalid"))
        for match in EMAIL_RE.finditer(value)
    )


def _truthy_material_value(value: Any) -> bool:
    if value in (None, False, 0, "", [], {}):
        return False
    if isinstance(value, str):
        return value.strip().lower() not in {"false", "no", "none", "null", "0", "offline", "blocked", "denied"}
    return True


def _positive_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def _looks_like_source_manifest(obj: dict[str, Any]) -> bool:
    return (
        obj.get("schema_version") == "aduana.source_manifest.v0"
        or "source_policy" in obj
        or {"files_downloaded", "bytes_downloaded"}.issubset(obj)
    )


def _assert_no_failures(failures: Iterable[str]) -> None:
    failures = list(failures)
    assert not failures, "V3-S fixture policy violations:\n" + "\n".join(
        f"- {failure}" for failure in failures
    )
