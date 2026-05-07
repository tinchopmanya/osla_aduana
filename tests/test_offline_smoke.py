from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from osla_aduana.offline_smoke import main, run_offline_guardrails_smoke  # noqa: E402


def test_offline_guardrails_smoke_reports_safe_runtime(tmp_path: Path) -> None:
    root = _seed_datalake(tmp_path)

    report = run_offline_guardrails_smoke(root=root, limit=1)

    assert report.status == "passed"
    assert report.trade_case_id == "trade_case:2026:offline:1"
    assert report.evidence_items == 1
    assert report.source_manifests == 1
    assert report.model_route_status == "blocked"
    assert report.selected_model_id is None
    assert report.model_human_review_required is True
    assert report.voxbridge_action == "lookup_trade_case"
    assert report.voxbridge_policy_status == "allowed"
    assert report.data_broker_metadata_only is True
    assert report.data_broker_material_operation_allowed is False
    assert report.broker_envelope_generated is True
    assert report.broker_envelope_operation == "metadata_observation"
    assert report.broker_envelope_decision == "approved_metadata_only"
    assert report.broker_envelope_resource_count == 1
    assert report.broker_envelope_bytes_total == 0
    assert report.broker_envelope_manifest_required is False
    assert report.broker_envelope["decision"] == "approved_metadata_only"
    assert report.broker_envelope["source_key"] == "uy.dna.public_ftp"
    assert report.broker_envelope["vertical_slug"] == "osla_aduana"
    assert report.broker_envelope["metadata_only"] is True
    assert report.broker_envelope["material_operation_allowed"] is False
    assert report.broker_envelope["allowed_artifact_kinds"] == []
    assert report.broker_envelope["requested_artifact_kinds"] == ["metadata_pointer"]
    assert report.broker_envelope["decision_json"]["allow_material_reads"] is False
    assert report.broker_envelope["decision_json"]["allow_model_use"] is False
    assert report.broker_envelope["pointer_manifest"][0]["declared_size_bytes"] == 123
    assert report.readiness_status == "ready_for_review"
    assert report.readiness_checks["hashes_verified"] is True
    assert report.readiness_checks["no_models_used"] is True
    assert report.raw_payload_included is False
    assert report.automatic_decision is False
    assert report.db_writes == 0
    assert report.final_ncm_allowed is False
    assert report.final_regime_allowed is False
    assert report.network_used is False
    assert report.storage_write_performed is False


@pytest.mark.parametrize("year", ["2025", "2026"])
def test_offline_guardrails_smoke_supports_year_partitions(tmp_path: Path, year: str) -> None:
    root = _seed_datalake(tmp_path / year, year=year)

    report = run_offline_guardrails_smoke(root=root, year=year, limit=1)

    assert report.status == "passed"
    assert report.year == year
    assert report.trade_case_id == f"trade_case:{year}:offline:1"
    assert report.readiness_status == "ready_for_review"
    assert report.readiness_checks["no_network"] is True
    assert report.readiness_checks["no_db_writes"] is True
    assert report.readiness_checks["no_ocr_processed"] is True
    assert report.readiness_checks["no_embeddings_generated"] is True
    assert report.readiness_checks["no_models_used"] is True
    assert report.raw_payload_included is False


def test_offline_smoke_cli_writes_json_report(tmp_path: Path) -> None:
    root = _seed_datalake(tmp_path / "datalake", year="2025")
    output = tmp_path / "smoke.json"

    exit_code = main(
        ["--root", str(root), "--year", "2025", "--format", "json", "--output", str(output)]
    )

    assert exit_code == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["status"] == "passed"
    assert payload["year"] == "2025"
    assert payload["model_route_status"] == "blocked"
    assert payload["selected_model_id"] is None
    assert payload["data_broker_material_operation_allowed"] is False
    assert payload["broker_envelope_generated"] is True
    assert payload["broker_envelope_operation"] == "metadata_observation"
    assert payload["broker_envelope_resource_count"] == 1
    assert payload["broker_envelope_bytes_total"] == 0
    assert payload["broker_envelope"]["manifest_count"] == 1
    assert payload["broker_envelope"]["bytes_total"] == 0
    assert payload["broker_envelope"]["decision_json"]["allow_material_reads"] is False
    assert payload["readiness_status"] == "ready_for_review"
    assert payload["readiness_checks"]["no_db_writes"] is True
    assert payload["raw_payload_included"] is False


def test_offline_guardrails_smoke_fails_when_readiness_requires_attention(tmp_path: Path) -> None:
    root = _seed_datalake(tmp_path, hash_mismatches=1)

    report = run_offline_guardrails_smoke(root=root, limit=1)

    assert report.status == "failed"
    assert report.readiness_status == "attention_required"
    assert report.readiness_checks["hashes_verified"] is False
    assert report.network_used is False
    assert report.db_writes == 0


def test_offline_smoke_cli_returns_json_error_without_traceback(tmp_path: Path, capsys) -> None:
    missing_root = tmp_path / "missing"

    exit_code = main(["--root", str(missing_root), "--format", "json"])

    assert exit_code == 1
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["status"] == "error"
    assert payload["error_type"] == "FileNotFoundError"
    assert payload["network_used"] is False
    assert payload["storage_write_performed"] is False
    assert payload["db_writes"] == 0
    assert captured.err == ""


def _seed_datalake(root: Path, year: str = "2026", **summary_overrides: object) -> Path:
    run_id = str(summary_overrides.get("run_id", f"aduana_{year}_full_process_001"))
    evidence_root = root / "gold" / "evidence" / year
    evidence_root.mkdir(parents=True)
    _write_jsonl(
        evidence_root / "source_manifests.jsonl",
        [
            {
                "source_manifest_id": "source:test",
                "run_id": run_id,
                "source_key": "uy.dna.public_ftp",
                "year": year,
                "partition": "daily_sample",
                "ftp_path": f"DUA Diarios XML/{year}/dd{year}0101.zip",
                "bronze_path": (
                    rf"C:\dev\osla_datalake\aduana\bronze\uy_dna_public_ftp\{year}"
                    r"\daily_sample"
                    rf"\dd{year}0101.zip"
                ),
                "bytes": 123,
                "sha256": "a" * 64,
                "raw_copied": True,
                "db_writes": 0,
            }
        ],
    )
    _write_jsonl(
        evidence_root / "evidence_items.jsonl",
        [
            {
                "evidence_item_id": "evidence:test:000001",
                "run_id": run_id,
                "source_key": "uy.dna.public_ftp",
                "source_manifest_id": "source:test",
                "evidence_type": "parsed_xml_pointer",
                "ftp_path": f"DUA Diarios XML/{year}/dd{year}0101.zip",
                "member_name": "dua.xml",
                "member_sha256": "b" * 64,
                "root_tag": "ROOT",
                "unique_field_count": 10,
                "parsed_record_pointer": "dua_records.jsonl#1",
                "raw_xml_copied_to_gold": False,
                "automatic_decision": False,
            }
        ],
    )
    _write_processing_summary(root, year=year, **summary_overrides)
    return root


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text(
        "".join(json.dumps(row, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
    )


def _write_processing_summary(root: Path, year: str = "2026", **overrides: object) -> None:
    run_id = str(overrides.get("run_id", f"aduana_{year}_full_process_001"))
    summary = {
        "run_id": run_id,
        "year": year,
        "source_zip_count": 1,
        "bronze_zip_count": 1,
        "source_bytes": 123,
        "bronze_bytes": 123,
        "source_manifests": 1,
        "evidence_items": 1,
        "xml_records_parsed": 1,
        "xml_parse_errors": 0,
        "zip_member_errors": 0,
        "hash_mismatches": 0,
        "ocr_candidates": 0,
        "ocr_files_processed": 0,
        "db_writes": 0,
        "network_used": False,
        "raw_files_written_to_repo": False,
    }
    summary.update(overrides)
    path = root / "runs" / run_id / "processing_summary.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary), encoding="utf-8")
