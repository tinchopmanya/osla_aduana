from __future__ import annotations

import json
import sys
from pathlib import Path

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
    assert report.model_route_status == "model_selected"
    assert report.selected_model_id == "frontier-review"
    assert report.model_human_review_required is True
    assert report.voxbridge_action == "lookup_trade_case"
    assert report.voxbridge_policy_status == "allowed"
    assert report.data_broker_metadata_only is True
    assert report.data_broker_material_operation_allowed is False
    assert report.raw_payload_included is False
    assert report.automatic_decision is False
    assert report.db_writes == 0
    assert report.final_ncm_allowed is False
    assert report.final_regime_allowed is False
    assert report.network_used is False
    assert report.storage_write_performed is False


def test_offline_smoke_cli_writes_json_report(tmp_path: Path) -> None:
    root = _seed_datalake(tmp_path / "datalake")
    output = tmp_path / "smoke.json"

    exit_code = main(["--root", str(root), "--format", "json", "--output", str(output)])

    assert exit_code == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["status"] == "passed"
    assert payload["selected_model_id"] == "frontier-review"
    assert payload["data_broker_material_operation_allowed"] is False
    assert payload["raw_payload_included"] is False


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


def _seed_datalake(root: Path) -> Path:
    evidence_root = root / "gold" / "evidence" / "2026"
    evidence_root.mkdir(parents=True)
    _write_jsonl(
        evidence_root / "source_manifests.jsonl",
        [
            {
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
        ],
    )
    _write_jsonl(
        evidence_root / "evidence_items.jsonl",
        [
            {
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
        ],
    )
    return root


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text(
        "".join(json.dumps(row, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
    )
