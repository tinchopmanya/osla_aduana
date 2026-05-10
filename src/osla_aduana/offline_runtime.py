from __future__ import annotations

import json
import re
import string
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

from osla_aduana.core_guardrails import build_trade_case_guardrails


DEFAULT_DATALAKE_ROOT = Path(r"C:\dev\osla_datalake\aduana")
SUPPORTED_DATALAKE_YEARS = ("2025", "2026")
DUA_FTP_PARENT_TEMPLATE = "DUA Diarios XML/{year}"
DAILY_ZIP_RE = re.compile(r"^dd(?P<year>20\d{2})\d{4}\.zip$", re.IGNORECASE)
MONTHLY_ZIP_RE = re.compile(r"^dm(?P<year>20\d{2})\d{2}\.zip$", re.IGNORECASE)


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
        if item.raw_copied:
            raise ContractError("SourceManifest.raw_copied must be false for S6 documental GO")
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
        year = validate_datalake_year(year)
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
        manifests = [
            SourceManifest.from_dict(row)
            for row in _read_jsonl(self.evidence_root / "source_manifests.jsonl")
        ]
        for manifest in manifests:
            self._require_source_manifest_partition(manifest)
        return manifests

    def load_evidence_items(self) -> list[EvidenceItem]:
        evidence = [
            EvidenceItem.from_dict(row)
            for row in _read_jsonl(self.evidence_root / "evidence_items.jsonl")
        ]
        for item in evidence:
            self._require_evidence_partition(item)
        return evidence

    def load_processing_summary(self) -> dict[str, Any]:
        path = self.root / "runs" / self.run_id / "processing_summary.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def build_readiness_report(self) -> DataLakeReadinessReport:
        summary = self.load_processing_summary()
        _reject_legacy_summary_aliases(summary)
        summary_run_id = _summary_str(summary, "run_id")
        summary_year = _summary_year(summary)
        if summary_run_id != self.run_id:
            raise ContractError(
                f"processing_summary.run_id {summary_run_id} "
                f"does not match runtime run_id {self.run_id}"
            )
        if summary_year != self.year:
            raise ContractError(
                f"processing_summary.year {summary_year} does not match datalake year {self.year}"
            )
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
            "no_source_raw_copied": all(not manifest.raw_copied for manifest in manifests),
            "no_ocr_processed": _summary_optional_int(summary, "ocr_files_processed") == 0,
            "no_embeddings_generated": _summary_optional_int(summary, "embeddings_generated") == 0
            and _summary_optional_int(summary, "embedding_jobs") == 0,
            "no_models_used": _summary_optional_int(summary, "model_requests") == 0
            and _summary_optional_int(summary, "model_inferences") == 0,
        }
        status = "ready_for_review" if all(checks.values()) else "attention_required"
        return DataLakeReadinessReport(
            run_id=summary_run_id,
            status=status,
            year=summary_year,
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

    def _require_source_manifest_partition(self, manifest: SourceManifest) -> None:
        if manifest.year != self.year:
            raise ContractError(
                f"SourceManifest {manifest.source_manifest_id} year {manifest.year} "
                f"does not match datalake year {self.year}"
            )
        if manifest.run_id != self.run_id:
            raise ContractError(
                f"SourceManifest {manifest.source_manifest_id} run_id {manifest.run_id} "
                f"does not match runtime run_id {self.run_id}"
            )
        _require_ftp_path_partition(manifest.ftp_path, self.year, "ftp_path")
        _require_bronze_path_partition(manifest.bronze_path, self.year, manifest.partition, "bronze_path")

    def _require_evidence_partition(self, item: EvidenceItem) -> None:
        if item.run_id != self.run_id:
            raise ContractError(
                f"EvidenceItem {item.evidence_item_id} run_id {item.run_id} "
                f"does not match runtime run_id {self.run_id}"
            )
        _require_ftp_path_partition(item.ftp_path, self.year, "ftp_path")


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(path)
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def default_run_id_for_year(year: str) -> str:
    clean_year = validate_datalake_year(year)
    return f"aduana_{clean_year}_full_process_001"


def validate_datalake_year(year: str) -> str:
    clean_year = str(year)
    if not clean_year.isdigit() or len(clean_year) != 4:
        raise ContractError("year must be a four-digit string")
    if clean_year not in SUPPORTED_DATALAKE_YEARS:
        supported = ", ".join(SUPPORTED_DATALAKE_YEARS)
        raise ContractError(f"year must be one of: {supported}")
    return clean_year


def _require_ftp_path_partition(path: str, year: str, key: str) -> None:
    normalized = _normalize_path(path)
    expected_prefix = f"{DUA_FTP_PARENT_TEMPLATE.format(year=year)}/"
    if not normalized.startswith(expected_prefix):
        raise ContractError(f"{key} must start with exact year partition {expected_prefix}")
    _require_no_other_supported_year_segments(normalized, year, key)
    _require_zip_filename_year(_path_segments(normalized)[-1], year, key)


def _require_bronze_path_partition(path: str, year: str, partition: str, key: str) -> None:
    normalized = _normalize_path(path)
    segments = _path_segments(normalized)
    expected_segments = ("bronze", "uy_dna_public_ftp", year, partition)
    if not _contains_subsequence(tuple(segment.lower() for segment in segments), expected_segments):
        expected = "/".join(expected_segments)
        raise ContractError(f"{key} must include exact bronze partition {expected}")
    _require_no_other_supported_year_segments(normalized, year, key)
    _require_zip_filename_year(segments[-1], year, key)


def _normalize_path(path: str) -> str:
    return path.replace("\\", "/").strip("/")


def _path_segments(path: str) -> list[str]:
    return [segment for segment in _normalize_path(path).split("/") if segment]


def _contains_subsequence(segments: tuple[str, ...], expected: tuple[str, ...]) -> bool:
    if len(expected) > len(segments):
        return False
    return any(
        segments[index : index + len(expected)] == expected
        for index in range(len(segments) - len(expected) + 1)
    )


def _require_no_other_supported_year_segments(path: str, year: str, key: str) -> None:
    segments = set(_path_segments(path))
    for supported_year in SUPPORTED_DATALAKE_YEARS:
        if supported_year != year and supported_year in segments:
            raise ContractError(f"{key} must not include year partition {supported_year}")


def _require_zip_filename_year(file_name: str, year: str, key: str) -> None:
    match = DAILY_ZIP_RE.fullmatch(file_name) or MONTHLY_ZIP_RE.fullmatch(file_name)
    if match is None:
        raise ContractError(f"{key} file name must be an Aduana dd/dm ZIP with year {year}")
    if match.group("year") != year:
        raise ContractError(f"{key} file name year {match.group('year')} does not match datalake year {year}")


def _summary_int(summary: dict[str, Any], key: str) -> int:
    value = summary.get(key)
    if not isinstance(value, int):
        raise ContractError(f"processing_summary.{key} must be an integer")
    return value


def _reject_legacy_summary_aliases(summary: dict[str, Any]) -> None:
    if "quarantine_zip_pointer_count" in summary:
        raise ContractError(
            "processing_summary.quarantine_zip_pointer_count is not accepted; "
            "use source_zip_count"
        )


def _summary_optional_int(summary: dict[str, Any], key: str) -> int:
    value = summary.get(key, 0)
    if not isinstance(value, int):
        raise ContractError(f"processing_summary.{key} must be an integer")
    return value


def _summary_year(summary: dict[str, Any]) -> str:
    return validate_datalake_year(_summary_str(summary, "year"))


def _summary_str(summary: dict[str, Any], key: str) -> str:
    value = summary.get(key)
    if not isinstance(value, str) or not value:
        raise ContractError(f"processing_summary.{key} must be a non-empty string")
    return value
