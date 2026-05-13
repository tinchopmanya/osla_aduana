from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from osla_aduana.offline_runtime import ContractError


FINAL_KEYS = {"ncm_final", "regime_final", "regimen_final"}
BLOCKED_TRUE_KEYS = {
    "automatic_decision",
    "raw_payload_included",
    "raw_payload_embedded",
    "raw_xml_copied_to_gold",
    "network_used",
    "ocr_used",
    "uses_ocr",
    "embeddings_used",
    "db_used",
    "real_source_touched",
    "ftp_allowed",
    "downloads_allowed",
    "db_writes_allowed",
    "storage_writes_allowed",
    "ocr_allowed",
    "embeddings_allowed",
    "declares_download_approval",
    "automatic_ncm_final_allowed",
    "automatic_regime_final_allowed",
    "writes_ncm_final",
    "writes_regime_final",
}
BLOCKED_PAYLOAD_KEYS = {"raw_payload", "raw_xml", "raw_zip", "document_bytes"}


def default_fixture_root() -> Path:
    return Path(__file__).resolve().parents[2] / "fixtures" / "v3_s"


class AduanaGetOnlyDemoStore:
    """Read-only facade over synthetic Aduana fixtures.

    This object intentionally exposes only GET-like accessors. It never downloads,
    writes, OCRs, embeds, or finalizes NCM/regime values.
    """

    def __init__(self, fixture_root: str | Path | None = None) -> None:
        self.fixture_root = Path(fixture_root) if fixture_root is not None else default_fixture_root()
        self._index = self._load_json("index.json")
        self._trade_case_pack = self._load_json("trade_cases.json")
        self._validate_fixture_policy(self._index, "index.json")
        self._validate_fixture_policy(self._trade_case_pack, "trade_cases.json")

    def list_trade_cases(self) -> tuple[dict[str, Any], ...]:
        cases = self._trade_case_pack.get("trade_cases")
        if not isinstance(cases, list):
            raise ContractError("trade_cases.json must contain a trade_cases list")
        return tuple(copy.deepcopy(case) for case in cases)

    def get_trade_case(self, trade_case_id: str) -> dict[str, Any]:
        for case in self.list_trade_cases():
            if case.get("id") == trade_case_id:
                return case
        raise KeyError(f"Unknown synthetic trade case: {trade_case_id}")

    def case_summaries(self) -> tuple[dict[str, Any], ...]:
        summaries: list[dict[str, Any]] = []
        for case in self.list_trade_cases():
            tasks = case.get("tasks") if isinstance(case.get("tasks"), list) else []
            missing = (
                case.get("missing_requirements")
                if isinstance(case.get("missing_requirements"), list)
                else []
            )
            summaries.append(
                {
                    "id": case.get("id"),
                    "status": case.get("status"),
                    "buyer_type": case.get("buyer_type"),
                    "task_count": len(tasks),
                    "missing_requirement_count": len(missing),
                    "ncm_final": _none_if_missing(_find_first_key(case, "ncm_final")),
                    "regime_final": _none_if_missing(_find_first_key(case, "regime_final")),
                    "synthetic_only": True,
                }
            )
        return tuple(summaries)

    def fixture_policy(self) -> dict[str, Any]:
        return copy.deepcopy(self._index.get("offline_guards", {}))

    def _load_json(self, filename: str) -> dict[str, Any]:
        path = self.fixture_root / filename
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ContractError(f"{filename} must contain a JSON object")
        return payload

    def _validate_fixture_policy(self, payload: Any, path: str) -> None:
        if isinstance(payload, dict):
            for key, value in payload.items():
                current_path = f"{path}.{key}"
                if key in FINAL_KEYS and value is not None:
                    raise ContractError(f"{current_path} must be null in GET-only demo")
                if key in BLOCKED_TRUE_KEYS and value is True:
                    raise ContractError(f"{current_path} must be false in GET-only demo")
                if key == "db_writes" and value != 0:
                    raise ContractError(f"{current_path} must be 0 in GET-only demo")
                if key in BLOCKED_PAYLOAD_KEYS and value not in (None, "", [], {}):
                    raise ContractError(f"{current_path} is not allowed in GET-only demo")
                self._validate_fixture_policy(value, current_path)
            return
        if isinstance(payload, list):
            for index, item in enumerate(payload):
                self._validate_fixture_policy(item, f"{path}[{index}]")


def _find_first_key(payload: Any, key: str) -> Any:
    if isinstance(payload, dict):
        if key in payload:
            return payload[key]
        for value in payload.values():
            found = _find_first_key(value, key)
            if found is not _MISSING:
                return found
    if isinstance(payload, list):
        for item in payload:
            found = _find_first_key(item, key)
            if found is not _MISSING:
                return found
    return _MISSING


_MISSING = object()


def _none_if_missing(value: Any) -> Any:
    return None if value is _MISSING else value
