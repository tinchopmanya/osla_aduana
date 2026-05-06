from __future__ import annotations

from typing import Any

from osla_core.modelops import ModelRouteRequest, route_model
from osla_core.voxbridge import VoxBridgeActionRequest, evaluate_voxbridge_action


VERTICAL_SLUG = "osla_aduana"
CORE_GUARDRAILS_CONTRACT_VERSION = "aduana-core-guardrails-v0"
BROKER_REQUIRED_OPERATIONS = ("download", "storage_write", "artifact_write", "ocr", "embedding")


def build_trade_case_guardrails(*, trade_case: Any) -> dict[str, Any]:
    """Return side-effect-free guardrail metadata for an offline TradeCase."""

    route = route_model(
        ModelRouteRequest(
            task_kind="regime_review",
            vertical_slug=VERTICAL_SLUG,
            sensitivity="confidential",
            risk_level="critical",
            estimated_input_tokens=1600,
            estimated_output_tokens=400,
            metadata={
                "trade_case_id": trade_case.trade_case_id,
                "source_key": trade_case.source_context.source_key,
                "surface": "offline_trade_case",
            },
        )
    )
    vox = evaluate_voxbridge_action(
        VoxBridgeActionRequest(
            action="lookup_trade_case",
            vertical_slug=VERTICAL_SLUG,
            actor_id="offline-runtime",
            source_channel="offline_runtime",
            case_id=trade_case.trade_case_id,
            sensitivity="confidential",
            risk_level="high",
        )
    )
    return {
        "contract_version": CORE_GUARDRAILS_CONTRACT_VERSION,
        "vertical_slug": VERTICAL_SLUG,
        "trade_case_id": trade_case.trade_case_id,
        "automatic_decision": False,
        "modelops": route.to_audit_metadata(),
        "voxbridge": {
            **vox.evidence_metadata,
            "policy_status": vox.status,
            "policy_reason": vox.reason,
        },
        "data_broker": _data_broker_posture(
            source_key=trade_case.source_context.source_key,
            source_run_id=trade_case.source_context.source_run_id,
            source_manifest_ids=trade_case.source_context.source_manifest_ids,
        ),
        "codeguard": {
            "contract_version": "codeguard-v0",
            "direct_model_call_allowed": False,
            "raw_cross_vertical_copy_allowed": False,
            "material_operation_without_broker_allowed": False,
        },
        "domain_controls": {
            "human_review_required": True,
            "final_ncm_allowed": False,
            "final_regime_allowed": False,
            "filing_instruction_allowed": False,
        },
    }


def _data_broker_posture(
    *,
    source_key: str,
    source_run_id: str,
    source_manifest_ids: tuple[str, ...],
) -> dict[str, Any]:
    return {
        "contract_version": "data-broker-v0",
        "source_key": source_key,
        "source_run_id": source_run_id,
        "source_manifest_ids": list(source_manifest_ids),
        "material_operation_requested": False,
        "material_operation_allowed": False,
        "metadata_only": True,
        "raw_payload_included": False,
        "broker_required_for": list(BROKER_REQUIRED_OPERATIONS),
        "shared_source_registry_required": True,
    }
