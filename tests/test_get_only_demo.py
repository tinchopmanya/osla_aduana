from __future__ import annotations

import json
from pathlib import Path

import pytest

from osla_aduana import AduanaGetOnlyDemoStore
from osla_aduana.offline_runtime import ContractError


def test_get_only_store_loads_synthetic_trade_cases() -> None:
    store = AduanaGetOnlyDemoStore()

    cases = store.list_trade_cases()
    summaries = store.case_summaries()
    policy = store.fixture_policy()

    assert len(cases) == 3
    assert len(summaries) == 3
    assert policy["network_allowed"] is False
    assert policy["ocr_allowed"] is False
    assert policy["db_writes_allowed"] is False
    assert all(summary["synthetic_only"] is True for summary in summaries)
    assert all(summary["ncm_final"] is None for summary in summaries)
    assert all(summary["regime_final"] is None for summary in summaries)


def test_get_only_store_returns_defensive_copies() -> None:
    store = AduanaGetOnlyDemoStore()

    case = store.get_trade_case("tc_syn_missing_docs_0001")
    case["status"] = "mutated"

    assert store.get_trade_case("tc_syn_missing_docs_0001")["status"] == "needs_documents"


def test_get_only_store_rejects_final_ncm(tmp_path: Path) -> None:
    _write_minimal_fixture_root(tmp_path, ncm_final="1234.56.78.90")

    with pytest.raises(ContractError, match="ncm_final"):
        AduanaGetOnlyDemoStore(tmp_path)


def test_get_only_store_rejects_automatic_decision(tmp_path: Path) -> None:
    _write_minimal_fixture_root(tmp_path, automatic_decision=True)

    with pytest.raises(ContractError, match="automatic_decision"):
        AduanaGetOnlyDemoStore(tmp_path)


def test_get_only_store_rejects_raw_payload(tmp_path: Path) -> None:
    _write_minimal_fixture_root(tmp_path, raw_payload={"secret": "blocked"})

    with pytest.raises(ContractError, match="raw_payload"):
        AduanaGetOnlyDemoStore(tmp_path)


def _write_minimal_fixture_root(
    root: Path,
    *,
    ncm_final: str | None = None,
    automatic_decision: bool = False,
    raw_payload: object | None = None,
) -> None:
    root.mkdir(parents=True, exist_ok=True)
    (root / "index.json").write_text(
        json.dumps(
            {
                "schema_version": "test.index",
                "offline_guards": {
                    "network_allowed": False,
                    "ocr_allowed": False,
                    "db_writes_allowed": False,
                    "automatic_ncm_final_allowed": False,
                    "automatic_regime_final_allowed": False,
                },
            }
        ),
        encoding="utf-8",
    )
    (root / "trade_cases.json").write_text(
        json.dumps(
            {
                "schema_version": "test.trade_cases",
                "trade_cases": [
                    {
                        "id": "tc_test",
                        "status": "needs_documents",
                        "buyer_type": "despachante",
                        "items": [{"ncm_final": ncm_final}],
                        "automatic_decision": automatic_decision,
                        "raw_payload": raw_payload,
                        "tasks": [],
                        "missing_requirements": [],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
