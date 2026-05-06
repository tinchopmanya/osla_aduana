from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from osla_aduana import AduanaDataLake, EvidenceItem, SourceManifest, build_trade_case_guardrails  # noqa: E402
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


def test_loader_builds_trade_case_from_gold_pointers(tmp_path: Path) -> None:
    root = tmp_path / "aduana"
    evidence_root = root / "gold" / "evidence" / "2026"
    _write_jsonl(evidence_root / "source_manifests.jsonl", [_source_manifest()])
    _write_jsonl(evidence_root / "evidence_items.jsonl", [_evidence_item()])

    lake = AduanaDataLake(root=root)
    manifests = lake.load_source_manifests()
    evidence = lake.load_evidence_items()
    case = lake.build_trade_case_from_evidence()

    assert len(manifests) == 1
    assert len(evidence) == 1
    assert case.status == "ready_for_review"
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


def test_real_datalake_smoke_if_present() -> None:
    root = Path(r"C:\dev\osla_datalake\aduana")
    evidence_path = root / "gold" / "evidence" / "2026" / "evidence_items.jsonl"
    if not evidence_path.exists():
        pytest.skip("local Aduana 2026 data lake is not present")

    lake = AduanaDataLake(root=root)
    summary = lake.load_processing_summary()
    case = lake.build_trade_case_from_evidence(limit=5)

    assert summary["source_zip_count"] == 127
    assert summary["xml_records_parsed"] == 381
    assert summary["db_writes"] == 0
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


def _source_manifest() -> dict[str, object]:
    return {
        "source_manifest_id": "source:test",
        "run_id": "aduana_2026_full_process_001",
        "source_key": "uy.dna.public_ftp",
        "year": "2026",
        "partition": "daily_sample",
        "ftp_path": "DUA Diarios XML/2026/dd20260101.zip",
        "bronze_path": r"C:\dev\osla_datalake\aduana\bronze\uy_dna_public_ftp\2026\daily_sample\dd20260101.zip",
        "bytes": 123,
        "sha256": "a" * 64,
        "raw_copied": True,
        "db_writes": 0,
    }


def _evidence_item() -> dict[str, object]:
    return {
        "evidence_item_id": "evidence:test:000001",
        "run_id": "aduana_2026_full_process_001",
        "source_key": "uy.dna.public_ftp",
        "source_manifest_id": "source:test",
        "evidence_type": "parsed_xml_pointer",
        "ftp_path": "DUA Diarios XML/2026/dd20260101.zip",
        "member_name": "dua.xml",
        "member_sha256": "b" * 64,
        "root_tag": "ROOT",
        "unique_field_count": 10,
        "parsed_record_pointer": "dua_records.jsonl#1",
        "raw_xml_copied_to_gold": False,
        "automatic_decision": False,
    }


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
