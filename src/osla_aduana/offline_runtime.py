from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


DEFAULT_DATALAKE_ROOT = Path(r"C:\dev\osla_datalake\aduana")


class ContractError(ValueError):
    pass


def _require_str(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ContractError(f"{key} must be a non-empty string")
    return value


def _require_bool(payload: dict[str, Any], key: str) -> bool:
    value = payload.get(key)
    if not isinstance(value, bool):
        raise ContractError(f"{key} must be a boolean")
    return value


def _require_int(payload: dict[str, Any], key: str) -> int:
    value = payload.get(key)
    if not isinstance(value, int):
        raise ContractError(f"{key} must be an integer")
    return value


@dataclass(frozen=True)
class SourceManifest:
    source_manifest_id: str
    run_id: str
    source_key: str
    year: str
    partition: str
    ftp_path: str
    bronze_path: str
    bytes: int
    sha256: str
    raw_copied: bool
    db_writes: int

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SourceManifest":
        item = cls(
            source_manifest_id=_require_str(payload, "source_manifest_id"),
            run_id=_require_str(payload, "run_id"),
            source_key=_require_str(payload, "source_key"),
            year=str(payload.get("year", "")),
            partition=_require_str(payload, "partition"),
            ftp_path=_require_str(payload, "ftp_path"),
            bronze_path=_require_str(payload, "bronze_path"),
            bytes=_require_int(payload, "bytes"),
            sha256=_require_str(payload, "sha256"),
            raw_copied=_require_bool(payload, "raw_copied"),
            db_writes=_require_int(payload, "db_writes"),
        )
        if item.db_writes != 0:
            raise ContractError("SourceManifest cannot declare DB writes")
        if len(item.sha256) != 64:
            raise ContractError("SourceManifest sha256 must be a hex digest")
        return item


@dataclass(frozen=True)
class EvidenceItem:
    evidence_item_id: str
    run_id: str
    source_key: str
    source_manifest_id: str
    evidence_type: str
    ftp_path: str
    member_name: str
    member_sha256: str
    root_tag: str
    unique_field_count: int
    parsed_record_pointer: str
    raw_xml_copied_to_gold: bool
    automatic_decision: bool

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "EvidenceItem":
        item = cls(
            evidence_item_id=_require_str(payload, "evidence_item_id"),
            run_id=_require_str(payload, "run_id"),
            source_key=_require_str(payload, "source_key"),
            source_manifest_id=_require_str(payload, "source_manifest_id"),
            evidence_type=_require_str(payload, "evidence_type"),
            ftp_path=_require_str(payload, "ftp_path"),
            member_name=_require_str(payload, "member_name"),
            member_sha256=_require_str(payload, "member_sha256"),
            root_tag=_require_str(payload, "root_tag"),
            unique_field_count=_require_int(payload, "unique_field_count"),
            parsed_record_pointer=_require_str(payload, "parsed_record_pointer"),
            raw_xml_copied_to_gold=_require_bool(payload, "raw_xml_copied_to_gold"),
            automatic_decision=_require_bool(payload, "automatic_decision"),
        )
        if item.raw_xml_copied_to_gold:
            raise ContractError("EvidenceItem cannot copy raw XML into Gold")
        if item.automatic_decision:
            raise ContractError("EvidenceItem cannot declare automatic decisions")
        if len(item.member_sha256) != 64:
            raise ContractError("EvidenceItem member_sha256 must be a hex digest")
        return item


@dataclass(frozen=True)
class TradeCaseSourceContext:
    intake_channel: str
    source_run_id: str
    source_key: str
    source_manifest_ids: tuple[str, ...]
    raw_payload_embedded: bool = False

    def __post_init__(self) -> None:
        if self.raw_payload_embedded:
            raise ContractError("TradeCase cannot embed raw payloads")


@dataclass(frozen=True)
class TradeCase:
    trade_case_id: str
    status: str
    source_context: TradeCaseSourceContext
    evidence_item_ids: tuple[str, ...]
    tasks: tuple[str, ...] = field(default_factory=tuple)
    automatic_decision: bool = False
    db_writes: int = 0

    def __post_init__(self) -> None:
        if self.automatic_decision:
            raise ContractError("TradeCase cannot declare automatic decisions")
        if self.db_writes != 0:
            raise ContractError("TradeCase offline runtime cannot write DB")


class AduanaDataLake:
    def __init__(self, root: Path | str = DEFAULT_DATALAKE_ROOT, year: str = "2026") -> None:
        self.root = Path(root)
        self.year = year

    @property
    def evidence_root(self) -> Path:
        return self.root / "gold" / "evidence" / self.year

    @property
    def parsed_root(self) -> Path:
        return self.root / "silver" / "dua_parsed" / self.year

    def load_source_manifests(self) -> list[SourceManifest]:
        return [
            SourceManifest.from_dict(row)
            for row in _read_jsonl(self.evidence_root / "source_manifests.jsonl")
        ]

    def load_evidence_items(self) -> list[EvidenceItem]:
        return [
            EvidenceItem.from_dict(row)
            for row in _read_jsonl(self.evidence_root / "evidence_items.jsonl")
        ]

    def load_processing_summary(self) -> dict[str, Any]:
        path = self.root / "runs" / "aduana_2026_full_process_001" / "processing_summary.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def build_trade_case_from_evidence(self, limit: int | None = None) -> TradeCase:
        manifests = self.load_source_manifests()
        evidence = self.load_evidence_items()
        if limit is not None:
            evidence = evidence[:limit]
        source_manifest_ids = tuple(sorted({item.source_manifest_id for item in evidence}))
        return TradeCase(
            trade_case_id=f"trade_case:{self.year}:offline:{len(evidence)}",
            status="ready_for_review",
            source_context=TradeCaseSourceContext(
                intake_channel="public_dataset_local_datalake",
                source_run_id="aduana_2026_full_process_001",
                source_key="uy.dna.public_ftp",
                source_manifest_ids=source_manifest_ids,
            ),
            evidence_item_ids=tuple(item.evidence_item_id for item in evidence),
            tasks=(
                "review_parsed_xml_field_catalog",
                "select_records_for_domain_interpretation",
            ),
        )


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(path)
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows
