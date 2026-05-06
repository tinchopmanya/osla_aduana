from __future__ import annotations

import json
import string
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

from osla_aduana.core_guardrails import build_trade_case_guardrails


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


def _require_sha256(payload: dict[str, Any], key: str) -> str:
    value = _require_str(payload, key)
    if len(value) != 64 or any(char not in string.hexdigits for char in value):
        raise ContractError(f"{key} must be a 64-character hex digest")
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
            sha256=_require_sha256(payload, "sha256"),
            raw_copied=_require_bool(payload, "raw_copied"),
            db_writes=_require_int(payload, "db_writes"),
        )
        if item.db_writes != 0:
            raise ContractError("SourceManifest cannot declare DB writes")
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
            member_sha256=_require_sha256(payload, "member_sha256"),
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
    core_guardrails: dict[str, Any] = field(default_factory=dict)
    automatic_decision: bool = False
    db_writes: int = 0

    def __post_init__(self) -> None:
        if self.automatic_decision:
            raise ContractError("TradeCase cannot declare automatic decisions")
        if self.db_writes != 0:
            raise ContractError("TradeCase offline runtime cannot write DB")


@dataclass(frozen=True)
class DataLakeReadinessReport:
    run_id: str
    status: str
    year: str
    source_zip_count: int
    bronze_zip_count: int
    source_bytes: int
    bronze_bytes: int
    source_manifests: int
    evidence_items: int
    xml_records_parsed: int
    xml_parse_errors: int
    zip_member_errors: int
    hash_mismatches: int
    ocr_candidates: int
    ocr_files_processed: int
    db_writes: int
    network_used: bool
    raw_files_written_to_repo: bool
    checks: dict[str, bool]
    next_actions: tuple[str, ...]

    @property
    def ready(self) -> bool:
        return self.status == "ready_for_review"

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "status": self.status,
            "year": self.year,
            "source_zip_count": self.source_zip_count,
            "bronze_zip_count": self.bronze_zip_count,
            "source_bytes": self.source_bytes,
            "bronze_bytes": self.bronze_bytes,
            "source_manifests": self.source_manifests,
            "evidence_items": self.evidence_items,
            "xml_records_parsed": self.xml_records_parsed,
            "xml_parse_errors": self.xml_parse_errors,
            "zip_member_errors": self.zip_member_errors,
            "hash_mismatches": self.hash_mismatches,
            "ocr_candidates": self.ocr_candidates,
            "ocr_files_processed": self.ocr_files_processed,
            "db_writes": self.db_writes,
            "network_used": self.network_used,
            "raw_files_written_to_repo": self.raw_files_written_to_repo,
            "checks": self.checks,
            "next_actions": list(self.next_actions),
        }


class AduanaDataLake:
    def __init__(
        self,
        root: Path | str = DEFAULT_DATALAKE_ROOT,
        year: str = "2026",
        run_id: str | None = None,
    ) -> None:
        self.root = Path(root)
        self.year = year
        self.run_id = run_id or default_run_id_for_year(year)

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
        path = self.root / "runs" / self.run_id / "processing_summary.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def build_readiness_report(self) -> DataLakeReadinessReport:
        summary = self.load_processing_summary()
        manifests = self.load_source_manifests()
        evidence = self.load_evidence_items()
        checks = {
            "hashes_verified": int(summary.get("hash_mismatches", -1)) == 0,
            "bronze_reconciled": summary.get("source_zip_count") == summary.get("bronze_zip_count")
            and summary.get("source_bytes") == summary.get("bronze_bytes"),
            "manifests_reconciled": int(summary.get("source_manifests", -1)) == len(manifests),
            "evidence_reconciled": int(summary.get("evidence_items", -1)) == len(evidence),
            "zip_members_clean": int(summary.get("zip_member_errors", -1)) == 0,
            "xml_parse_clean": int(summary.get("xml_parse_errors", -1)) == 0,
            "no_db_writes": int(summary.get("db_writes", -1)) == 0,
            "no_network": summary.get("network_used") is False,
            "no_raw_files_in_repo": summary.get("raw_files_written_to_repo") is False,
        }
        status = "ready_for_review" if all(checks.values()) else "attention_required"
        return DataLakeReadinessReport(
            run_id=_summary_str(summary, "run_id"),
            status=status,
            year=str(summary.get("year", self.year)),
            source_zip_count=_summary_int(summary, "source_zip_count"),
            bronze_zip_count=_summary_int(summary, "bronze_zip_count"),
            source_bytes=_summary_int(summary, "source_bytes"),
            bronze_bytes=_summary_int(summary, "bronze_bytes"),
            source_manifests=len(manifests),
            evidence_items=len(evidence),
            xml_records_parsed=_summary_int(summary, "xml_records_parsed"),
            xml_parse_errors=_summary_int(summary, "xml_parse_errors"),
            zip_member_errors=_summary_int(summary, "zip_member_errors"),
            hash_mismatches=_summary_int(summary, "hash_mismatches"),
            ocr_candidates=_summary_int(summary, "ocr_candidates"),
            ocr_files_processed=_summary_int(summary, "ocr_files_processed"),
            db_writes=_summary_int(summary, "db_writes"),
            network_used=summary.get("network_used") is True,
            raw_files_written_to_repo=summary.get("raw_files_written_to_repo") is True,
            checks=checks,
            next_actions=(
                "review_dua_field_catalog",
                "select_human_review_sample",
                "attach_evidence_pointers_to_trade_case",
            ),
        )

    def build_trade_case_from_evidence(self, limit: int | None = None) -> TradeCase:
        manifests = self.load_source_manifests()
        evidence = self.load_evidence_items()
        if limit is not None:
            evidence = evidence[:limit]
        source_manifest_ids = tuple(sorted({item.source_manifest_id for item in evidence}))
        known_manifest_ids = {item.source_manifest_id for item in manifests}
        missing_manifest_ids = sorted(set(source_manifest_ids) - known_manifest_ids)
        if missing_manifest_ids:
            raise ContractError(f"Evidence references unknown SourceManifest ids: {missing_manifest_ids}")
        case = TradeCase(
            trade_case_id=f"trade_case:{self.year}:offline:{len(evidence)}",
            status="ready_for_review",
            source_context=TradeCaseSourceContext(
                intake_channel="public_dataset_local_datalake",
                source_run_id=self.run_id,
                source_key="uy.dna.public_ftp",
                source_manifest_ids=source_manifest_ids,
            ),
            evidence_item_ids=tuple(item.evidence_item_id for item in evidence),
            tasks=(
                "review_parsed_xml_field_catalog",
                "select_records_for_domain_interpretation",
            ),
        )
        return replace(case, core_guardrails=build_trade_case_guardrails(trade_case=case))


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(path)
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def default_run_id_for_year(year: str) -> str:
    clean_year = str(year)
    if not clean_year.isdigit() or len(clean_year) != 4:
        raise ContractError("year must be a four-digit string")
    return f"aduana_{clean_year}_full_process_001"


def _summary_int(summary: dict[str, Any], key: str) -> int:
    value = summary.get(key)
    if not isinstance(value, int):
        raise ContractError(f"processing_summary.{key} must be an integer")
    return value


def _summary_str(summary: dict[str, Any], key: str) -> str:
    value = summary.get(key)
    if not isinstance(value, str) or not value:
        raise ContractError(f"processing_summary.{key} must be a non-empty string")
    return value
