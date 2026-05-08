from __future__ import annotations

import argparse
import json
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Literal, Sequence

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from osla_core.base import SharedBase
from osla_core.data_broker import BrokerDecision, BrokerRequest, DataBrokerClient

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
    broker_envelope_generated: bool
    broker_envelope_operation: str | None
    broker_envelope_decision: str | None
    broker_envelope_resource_count: int
    broker_envelope_bytes_total: int
    broker_envelope_manifest_required: bool
    broker_envelope: dict[str, object]
    readiness_status: str
    readiness_checks: dict[str, bool]
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
            f"- broker_envelope_generated: `{str(self.broker_envelope_generated).lower()}`",
            f"- broker_envelope_operation: `{self.broker_envelope_operation}`",
            f"- broker_envelope_decision: `{self.broker_envelope_decision}`",
            f"- broker_envelope_resource_count: `{self.broker_envelope_resource_count}`",
            f"- broker_envelope_bytes_total: `{self.broker_envelope_bytes_total}`",
            f"- broker_envelope_manifest_required: `{str(self.broker_envelope_manifest_required).lower()}`",
            f"- broker_envelope_request_id: `{self.broker_envelope.get('request_id')}`",
            f"- broker_envelope_decision_id: `{self.broker_envelope.get('decision_id')}`",
            f"- readiness_status: `{self.readiness_status}`",
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


@dataclass(frozen=True)
class OfflineBrokerMetadataEnvelope:
    request_id: str
    decision_id: str
    decision: str
    proposed_operation: str
    vertical_slug: str | None
    source_key: str | None
    resource_count: int
    bytes_total: int
    manifest_required: bool
    manifest_count: int
    metadata_only: bool
    material_operation_allowed: bool
    requested_artifact_kinds: tuple[str, ...] = ()
    allowed_artifact_kinds: tuple[str, ...] = ()
    pointer_manifest: tuple[dict[str, object], ...] = field(default_factory=tuple)
    decision_json: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "request_id": self.request_id,
            "decision_id": self.decision_id,
            "decision": self.decision,
            "proposed_operation": self.proposed_operation,
            "vertical_slug": self.vertical_slug,
            "source_key": self.source_key,
            "resource_count": self.resource_count,
            "bytes_total": self.bytes_total,
            "manifest_required": self.manifest_required,
            "manifest_count": self.manifest_count,
            "metadata_only": self.metadata_only,
            "material_operation_allowed": self.material_operation_allowed,
            "requested_artifact_kinds": list(self.requested_artifact_kinds),
            "allowed_artifact_kinds": list(self.allowed_artifact_kinds),
            "pointer_manifest": [dict(entry) for entry in self.pointer_manifest],
            "decision_json": dict(self.decision_json),
        }


class MemorySessionManager:
    """In-memory broker DB used only to create a smoke envelope."""

    def __init__(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        self.factory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
        SharedBase.metadata.create_all(self.engine)

    @contextmanager
    def session(self):
        session = self.factory()
        try:
            yield session
        finally:
            session.close()


def run_offline_guardrails_smoke(
    *,
    root: Path | str = DEFAULT_DATALAKE_ROOT,
    year: str = "2026",
    limit: int | None = 5,
) -> AduanaOfflineSmokeReport:
    lake = AduanaDataLake(root=root, year=year)
    readiness = lake.build_readiness_report()
    manifests = lake.load_source_manifests()
    trade_case = lake.build_trade_case_from_evidence(limit=limit)
    broker_envelope = _build_offline_broker_envelope(trade_case=trade_case, manifests=manifests)
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
        broker_envelope_generated=True,
        broker_envelope_operation=broker_envelope.proposed_operation,
        broker_envelope_decision=broker_envelope.decision,
        broker_envelope_resource_count=broker_envelope.resource_count,
        broker_envelope_bytes_total=broker_envelope.bytes_total,
        broker_envelope_manifest_required=broker_envelope.manifest_required,
        broker_envelope=broker_envelope.to_dict(),
        readiness_status=readiness.status,
        readiness_checks=readiness.checks,
        raw_payload_included=data_broker.get("raw_payload_included") is True
        or trade_case.source_context.raw_payload_embedded,
        automatic_decision=trade_case.automatic_decision or guardrails.get("automatic_decision") is True,
        db_writes=trade_case.db_writes,
        final_ncm_allowed=domain.get("final_ncm_allowed") is True,
        final_regime_allowed=domain.get("final_regime_allowed") is True,
    )
    if not readiness.ready:
        return _failed(report)
    if len(manifests) < len(trade_case.source_context.source_manifest_ids):
        return _failed(report)
    if _has_blocked_flag(report):
        return _failed(report)
    return report


def _build_offline_broker_envelope(*, trade_case, manifests) -> OfflineBrokerMetadataEnvelope:
    selected_manifest_ids = set(trade_case.source_context.source_manifest_ids)
    selected_manifests = [
        manifest for manifest in manifests if manifest.source_manifest_id in selected_manifest_ids
    ]
    manifest_payload = [
        {
            "resource_key": manifest.source_manifest_id,
            "source_key": manifest.source_key,
            "ftp_path_pointer": manifest.ftp_path,
            "bronze_path_pointer": manifest.bronze_path,
            "declared_size_bytes": manifest.bytes,
            "sha256": manifest.sha256,
        }
        for manifest in selected_manifests
    ]

    manager = MemorySessionManager()
    broker = DataBrokerClient(manager)
    authority = DataBrokerClient(manager, broker_authority=True)
    request = broker.submit_request(
        BrokerRequest(
            requested_by="offline-runtime-smoke",
            business_reason="Aduana offline metadata pointer observation smoke",
            vertical_slug="osla_aduana",
            source_key=trade_case.source_context.source_key,
            resource_count_estimate=len(manifest_payload),
            bytes_estimate=0,
            artifact_kinds_requested=["metadata_pointer"],
            request_json={
                "runtime": "offline",
                "trade_case_id": trade_case.trade_case_id,
                "download_requested": False,
                "material_operations_requested": [],
            },
        )
    )
    decision = authority.record_decision(
        BrokerDecision(
            request_id=request.id,
            decision="approved_metadata_only",
            max_resources=len(manifest_payload),
            max_bytes=0,
            allowed_artifact_kinds=[],
            decision_json={
                "runtime": "offline_smoke",
                "metadata_only": True,
                "manifest_required": False,
                "allow_material_reads": False,
                "allow_material_writes": False,
                "allow_network_access": False,
                "allow_db_writes": False,
                "allow_model_use": False,
                "allowed_operations": ["metadata_observation"],
                "denied_operations": [
                    "download",
                    "storage_write",
                    "artifact_write",
                    "ocr",
                    "embedding",
                    "model",
                    "model_route",
                    "model_inference",
                ],
            },
        ),
        actor="offline-runtime-smoke",
    )
    active_decision = broker.require_active_decision(request.id, operation="metadata_observation")
    return OfflineBrokerMetadataEnvelope(
        request_id=str(request.id),
        decision_id=str(decision.id or active_decision.id),
        decision=active_decision.decision,
        proposed_operation="metadata_observation",
        vertical_slug=request.vertical_slug,
        source_key=request.source_key,
        resource_count=len(manifest_payload),
        bytes_total=0,
        manifest_required=False,
        manifest_count=len(manifest_payload),
        metadata_only=True,
        material_operation_allowed=False,
        requested_artifact_kinds=tuple(request.artifact_kinds_requested),
        allowed_artifact_kinds=tuple(active_decision.allowed_artifact_kinds),
        pointer_manifest=tuple(manifest_payload),
        decision_json=active_decision.decision_json,
    )


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
        or report.model_route_status != "blocked"
        or report.selected_model_id is not None
        or not report.model_human_review_required
        or _broker_decision_flag_enabled(report, "allow_model_use")
        or report.raw_payload_included
        or report.automatic_decision
        or report.db_writes != 0
        or report.final_ncm_allowed
        or report.final_regime_allowed
        or report.network_used
        or report.storage_write_performed
    )


def _broker_decision_flag_enabled(report: AduanaOfflineSmokeReport, key: str) -> bool:
    decision_json = report.broker_envelope.get("decision_json", {})
    return isinstance(decision_json, dict) and decision_json.get(key) is True


def _failed(report: AduanaOfflineSmokeReport) -> AduanaOfflineSmokeReport:
    payload = report.to_dict()
    payload["status"] = "failed"
    return AduanaOfflineSmokeReport(**payload)


if __name__ == "__main__":
    raise SystemExit(main())
