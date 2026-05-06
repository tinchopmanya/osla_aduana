from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal, Sequence

from osla_aduana.offline_runtime import AduanaDataLake, ContractError, DEFAULT_DATALAKE_ROOT


SmokeFormat = Literal["json", "markdown"]


@dataclass(frozen=True)
class AduanaOfflineSmokeReport:
    status: str
    datalake_root: str
    year: str
    trade_case_id: str
    evidence_items: int
    source_manifests: int
    task_count: int
    model_route_status: str
    selected_model_id: str | None
    model_human_review_required: bool
    voxbridge_action: str | None
    voxbridge_policy_status: str | None
    data_broker_metadata_only: bool
    data_broker_material_operation_allowed: bool
    raw_payload_included: bool
    automatic_decision: bool
    db_writes: int
    final_ncm_allowed: bool
    final_regime_allowed: bool
    network_used: bool = False
    storage_write_performed: bool = False

    @property
    def passed(self) -> bool:
        return self.status == "passed"

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)

    def to_markdown(self) -> str:
        lines = [
            "# Aduana Offline Guardrails Smoke",
            "",
            f"- status: `{self.status}`",
            f"- datalake_root: `{self.datalake_root}`",
            f"- year: `{self.year}`",
            f"- trade_case_id: `{self.trade_case_id}`",
            f"- evidence_items: `{self.evidence_items}`",
            f"- source_manifests: `{self.source_manifests}`",
            f"- task_count: `{self.task_count}`",
            f"- model_route_status: `{self.model_route_status}`",
            f"- selected_model_id: `{self.selected_model_id}`",
            f"- model_human_review_required: `{str(self.model_human_review_required).lower()}`",
            f"- voxbridge_action: `{self.voxbridge_action}`",
            f"- voxbridge_policy_status: `{self.voxbridge_policy_status}`",
            f"- data_broker_metadata_only: `{str(self.data_broker_metadata_only).lower()}`",
            f"- data_broker_material_operation_allowed: `{str(self.data_broker_material_operation_allowed).lower()}`",
            f"- raw_payload_included: `{str(self.raw_payload_included).lower()}`",
            f"- automatic_decision: `{str(self.automatic_decision).lower()}`",
            f"- db_writes: `{self.db_writes}`",
            f"- final_ncm_allowed: `{str(self.final_ncm_allowed).lower()}`",
            f"- final_regime_allowed: `{str(self.final_regime_allowed).lower()}`",
            f"- network_used: `{str(self.network_used).lower()}`",
            f"- storage_write_performed: `{str(self.storage_write_performed).lower()}`",
        ]
        return "\n".join(lines)


@dataclass(frozen=True)
class AduanaOfflineSmokeErrorReport:
    status: str
    datalake_root: str
    year: str
    error_type: str
    message: str
    network_used: bool = False
    storage_write_performed: bool = False
    db_writes: int = 0

    @property
    def passed(self) -> bool:
        return False

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)

    def to_markdown(self) -> str:
        return "\n".join(
            [
                "# Aduana Offline Guardrails Smoke",
                "",
                "- status: `error`",
                f"- datalake_root: `{self.datalake_root}`",
                f"- year: `{self.year}`",
                f"- error_type: `{self.error_type}`",
                f"- message: {self.message}",
                "- network_used: `false`",
                "- storage_write_performed: `false`",
                "- db_writes: `0`",
            ]
        )


def run_offline_guardrails_smoke(
    *,
    root: Path | str = DEFAULT_DATALAKE_ROOT,
    year: str = "2026",
    limit: int | None = 5,
) -> AduanaOfflineSmokeReport:
    lake = AduanaDataLake(root=root, year=year)
    manifests = lake.load_source_manifests()
    trade_case = lake.build_trade_case_from_evidence(limit=limit)
    guardrails = trade_case.core_guardrails
    modelops = guardrails.get("modelops", {})
    voxbridge = guardrails.get("voxbridge", {})
    data_broker = guardrails.get("data_broker", {})
    domain = guardrails.get("domain_controls", {})

    report = AduanaOfflineSmokeReport(
        status="passed",
        datalake_root=str(Path(root)),
        year=year,
        trade_case_id=trade_case.trade_case_id,
        evidence_items=len(trade_case.evidence_item_ids),
        source_manifests=len(trade_case.source_context.source_manifest_ids),
        task_count=len(trade_case.tasks),
        model_route_status=str(modelops.get("model_route_status")),
        selected_model_id=modelops.get("selected_model_id"),
        model_human_review_required=modelops.get("human_review_required") is True,
        voxbridge_action=voxbridge.get("action"),
        voxbridge_policy_status=voxbridge.get("policy_status"),
        data_broker_metadata_only=data_broker.get("metadata_only") is True,
        data_broker_material_operation_allowed=data_broker.get("material_operation_allowed") is True,
        raw_payload_included=data_broker.get("raw_payload_included") is True
        or trade_case.source_context.raw_payload_embedded,
        automatic_decision=trade_case.automatic_decision or guardrails.get("automatic_decision") is True,
        db_writes=trade_case.db_writes,
        final_ncm_allowed=domain.get("final_ncm_allowed") is True,
        final_regime_allowed=domain.get("final_regime_allowed") is True,
    )
    if len(manifests) < len(trade_case.source_context.source_manifest_ids):
        return _failed(report)
    if _has_blocked_flag(report):
        return _failed(report)
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Aduana offline TradeCase guardrails smoke.")
    parser.add_argument("--root", default=str(DEFAULT_DATALAKE_ROOT))
    parser.add_argument("--year", default="2026")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--output", help="Optional output path for the report.")
    args = parser.parse_args(argv)

    try:
        report = run_offline_guardrails_smoke(root=args.root, year=args.year, limit=args.limit)
    except (FileNotFoundError, ContractError, json.JSONDecodeError) as exc:
        report = AduanaOfflineSmokeErrorReport(
            status="error",
            datalake_root=str(Path(args.root)),
            year=args.year,
            error_type=exc.__class__.__name__,
            message=str(exc),
        )
    rendered = report.to_json() if args.format == "json" else report.to_markdown()
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0 if report.passed else 1


def _has_blocked_flag(report: AduanaOfflineSmokeReport) -> bool:
    return (
        report.data_broker_material_operation_allowed
        or report.raw_payload_included
        or report.automatic_decision
        or report.db_writes != 0
        or report.final_ncm_allowed
        or report.final_regime_allowed
        or report.network_used
        or report.storage_write_performed
    )


def _failed(report: AduanaOfflineSmokeReport) -> AduanaOfflineSmokeReport:
    payload = report.to_dict()
    payload["status"] = "failed"
    return AduanaOfflineSmokeReport(**payload)


if __name__ == "__main__":
    raise SystemExit(main())
