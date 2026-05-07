from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from osla_aduana import (  # noqa: E402
    AduanaDataLake,
    EvidenceItem,
    SourceManifest,
    build_trade_case_guardrails,
    default_run_id_for_year,
)
from osla_aduana.offline_runtime import ContractError  # noqa: E402


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
    )


def test_contracts_reject_db_writes_and_raw_gold_copy() -> None:
    source = _source_manifest()
    source["db_writes"] = 1
    with pytest.raises(ContractError):
        SourceManifest.from_dict(source)

    evidence = _evidence_item()
    evidence["raw_xml_copied_to_gold"] = True
    with pytest.raises(ContractError):
        EvidenceItem.from_dict(evidence)

    evidence = _evidence_item()
    evidence["automatic_decision"] = True
    with pytest.raises(ContractError):
        EvidenceItem.from_dict(evidence)


def test_contracts_reject_non_hex_sha256_digests() -> None:
    source = _source_manifest()
    source["sha256"] = "g" * 64
    with pytest.raises(ContractError, match="64-character hex digest"):
        SourceManifest.from_dict(source)

    evidence = _evidence_item()
    evidence["member_sha256"] = "z" * 64
    with pytest.raises(ContractError, match="64-character hex digest"):
        EvidenceItem.from_dict(evidence)


def test_loader_builds_trade_case_from_gold_pointers(tmp_path: Path) -> None:
    root = tmp_path / "aduana"
    evidence_root = root / "gold" / "evidence" / "2026"
    _write_jsonl(evidence_root / "source_manifests.jsonl", [_source_manifest()])
    _write_jsonl(evidence_root / "evidence_items.jsonl", [_evidence_item()])
    _write_processing_summary(root)

    lake = AduanaDataLake(root=root)
    manifests = lake.load_source_manifests()
    evidence = lake.load_evidence_items()
    case = lake.build_trade_case_from_evidence()
    readiness = lake.build_readiness_report()

    assert len(manifests) == 1
    assert len(evidence) == 1
    assert readiness.ready is True
    assert readiness.status == "ready_for_review"
    assert readiness.checks["bronze_reconciled"] is True
    assert readiness.to_dict()["evidence_items"] == 1
    assert case.status == "ready_for_review"
    assert case.source_context.source_run_id == "aduana_2026_full_process_001"
    assert case.db_writes == 0
    assert case.automatic_decision is False
    assert case.source_context.raw_payload_embedded is False
    assert case.evidence_item_ids == ("evidence:test:000001",)
    assert case.core_guardrails["contract_version"] == "aduana-core-guardrails-v0"
    assert case.core_guardrails["modelops"]["selected_model_id"] == "frontier-review"
    assert case.core_guardrails["modelops"]["human_review_required"] is True
    assert case.core_guardrails["voxbridge"]["policy_status"] == "allowed"
    assert case.core_guardrails["data_broker"]["material_operation_allowed"] is False
    assert case.core_guardrails["domain_controls"]["human_review_required"] is True


def test_loader_rejects_evidence_without_source_manifest(tmp_path: Path) -> None:
    root = tmp_path / "aduana"
    evidence_root = root / "gold" / "evidence" / "2026"
    _write_jsonl(evidence_root / "source_manifests.jsonl", [])
    _write_jsonl(evidence_root / "evidence_items.jsonl", [_evidence_item()])

    lake = AduanaDataLake(root=root)

    with pytest.raises(ContractError, match="unknown SourceManifest"):
        lake.build_trade_case_from_evidence()


def test_readiness_report_flags_summary_mismatch(tmp_path: Path) -> None:
    root = tmp_path / "aduana"
    evidence_root = root / "gold" / "evidence" / "2026"
    _write_jsonl(evidence_root / "source_manifests.jsonl", [_source_manifest()])
    _write_jsonl(evidence_root / "evidence_items.jsonl", [_evidence_item()])
    _write_processing_summary(root, bronze_zip_count=2)

    lake = AduanaDataLake(root=root)
    report = lake.build_readiness_report()

    assert report.ready is False
    assert report.status == "attention_required"
    assert report.checks["bronze_reconciled"] is False
    assert report.checks["evidence_reconciled"] is True


def test_loader_uses_custom_year_and_run_id(tmp_path: Path) -> None:
    root = tmp_path / "aduana"
    evidence_root = root / "gold" / "evidence" / "2025"
    source = _source_manifest(year="2025", run_id="aduana_2025_probe_001")
    evidence = _evidence_item(year="2025", run_id="aduana_2025_probe_001")
    _write_jsonl(evidence_root / "source_manifests.jsonl", [source])
    _write_jsonl(evidence_root / "evidence_items.jsonl", [evidence])
    _write_processing_summary(root, year="2025", run_id="aduana_2025_probe_001")

    lake = AduanaDataLake(root=root, year="2025", run_id="aduana_2025_probe_001")
    case = lake.build_trade_case_from_evidence(limit=1)
    readiness = lake.build_readiness_report()

    assert default_run_id_for_year("2025") == "aduana_2025_full_process_001"
    assert lake.run_id == "aduana_2025_probe_001"
    assert case.trade_case_id == "trade_case:2025:offline:1"
    assert case.source_context.source_run_id == "aduana_2025_probe_001"
    assert readiness.year == "2025"
    assert readiness.run_id == "aduana_2025_probe_001"


@pytest.mark.parametrize("year", ["2025", "2026"])
def test_loader_accepts_year_partitioned_synthetic_datalake(tmp_path: Path, year: str) -> None:
    root = tmp_path / "aduana"
    run_id = default_run_id_for_year(year)
    evidence_root = root / "gold" / "evidence" / year
    source = _source_manifest(year=year, run_id=run_id)
    evidence = _evidence_item(year=year, run_id=run_id)
    _write_jsonl(evidence_root / "source_manifests.jsonl", [source])
    _write_jsonl(evidence_root / "evidence_items.jsonl", [evidence])
    _write_processing_summary(root, year=year, run_id=run_id)

    lake = AduanaDataLake(root=root, year=year)
    readiness = lake.build_readiness_report()
    case = lake.build_trade_case_from_evidence(limit=1)

    assert readiness.ready is True
    assert readiness.year == year
    assert readiness.checks["no_network"] is True
    assert readiness.checks["no_db_writes"] is True
    assert readiness.checks["no_ocr_processed"] is True
    assert readiness.checks["no_embeddings_generated"] is True
    assert case.trade_case_id == f"trade_case:{year}:offline:1"
    assert case.source_context.source_run_id == run_id


def test_loader_rejects_cross_year_manifest_partition(tmp_path: Path) -> None:
    root = tmp_path / "aduana"
    evidence_root = root / "gold" / "evidence" / "2025"
    source = _source_manifest(year="2026", run_id="aduana_2025_full_process_001")
    evidence = _evidence_item(year="2025", run_id="aduana_2025_full_process_001")
    _write_jsonl(evidence_root / "source_manifests.jsonl", [source])
    _write_jsonl(evidence_root / "evidence_items.jsonl", [evidence])
    _write_processing_summary(root, year="2025", run_id="aduana_2025_full_process_001")

    lake = AduanaDataLake(root=root, year="2025")

    with pytest.raises(ContractError, match="does not match datalake year"):
        lake.build_readiness_report()


def test_readiness_report_blocks_ocr_and_embeddings(tmp_path: Path) -> None:
    root = tmp_path / "aduana"
    evidence_root = root / "gold" / "evidence" / "2026"
    _write_jsonl(evidence_root / "source_manifests.jsonl", [_source_manifest()])
    _write_jsonl(evidence_root / "evidence_items.jsonl", [_evidence_item()])
    _write_processing_summary(root, ocr_files_processed=1, embeddings_generated=1)

    lake = AduanaDataLake(root=root)
    report = lake.build_readiness_report()

    assert report.ready is False
    assert report.checks["no_ocr_processed"] is False
    assert report.checks["no_embeddings_generated"] is False


def test_default_run_id_requires_four_digit_year() -> None:
    with pytest.raises(ContractError):
        default_run_id_for_year("25")

    with pytest.raises(ContractError):
        default_run_id_for_year("2024")


def test_real_datalake_smoke_if_present() -> None:
    root = Path(r"C:\dev\osla_datalake\aduana")
    evidence_path = root / "gold" / "evidence" / "2026" / "evidence_items.jsonl"
    if not evidence_path.exists():
        pytest.skip("local Aduana 2026 data lake is not present")

    lake = AduanaDataLake(root=root)
    summary = lake.load_processing_summary()
    readiness = lake.build_readiness_report()
    case = lake.build_trade_case_from_evidence(limit=5)

    assert summary["source_zip_count"] == 127
    assert summary["xml_records_parsed"] == 381
    assert summary["db_writes"] == 0
    assert readiness.status == "ready_for_review"
    assert readiness.source_manifests == 127
    assert readiness.evidence_items == 381
    assert len(case.evidence_item_ids) == 5
    assert len(case.source_context.source_manifest_ids) >= 1
    assert case.core_guardrails["data_broker"]["source_key"] == "uy.dna.public_ftp"


def test_trade_case_guardrails_are_side_effect_free() -> None:
    case_payload = _trade_case_for_guardrail_test()
    guardrails = build_trade_case_guardrails(trade_case=case_payload)

    assert guardrails["contract_version"] == "aduana-core-guardrails-v0"
    assert guardrails["automatic_decision"] is False
    assert guardrails["modelops"]["model_route_status"] == "model_selected"
    assert guardrails["modelops"]["selected_model_id"] == "frontier-review"
    assert guardrails["voxbridge"]["action"] == "lookup_trade_case"
    assert guardrails["data_broker"]["metadata_only"] is True
    assert guardrails["data_broker"]["raw_payload_included"] is False
    assert guardrails["codeguard"]["direct_model_call_allowed"] is False
    assert guardrails["domain_controls"]["final_ncm_allowed"] is False
    assert guardrails["domain_controls"]["final_regime_allowed"] is False


def _source_manifest(year: str = "2026", run_id: str | None = None) -> dict[str, object]:
    run_id = run_id or f"aduana_{year}_full_process_001"
    return {
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


def _evidence_item(year: str = "2026", run_id: str | None = None) -> dict[str, object]:
    run_id = run_id or f"aduana_{year}_full_process_001"
    return {
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


def _write_processing_summary(root: Path, **overrides: object) -> None:
    run_id = str(overrides.get("run_id", "aduana_2026_full_process_001"))
    summary = {
        "run_id": run_id,
        "year": "2026",
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


def _trade_case_for_guardrail_test():
    from osla_aduana.offline_runtime import TradeCase, TradeCaseSourceContext

    return TradeCase(
        trade_case_id="trade_case:synthetic:guardrail",
        status="ready_for_review",
        source_context=TradeCaseSourceContext(
            intake_channel="synthetic_offline_test",
            source_run_id="run:synthetic:guardrail",
            source_key="uy.dna.public_ftp",
            source_manifest_ids=("source:test",),
        ),
        evidence_item_ids=("evidence:test:000001",),
    )
