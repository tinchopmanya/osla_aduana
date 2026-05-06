# Aduana Offline Guardrails Smoke

Fecha: 2026-05-06
Estado: smoke CLI local.

## Comando

```powershell
python -m osla_aduana.offline_smoke --format markdown
python -m osla_aduana.offline_smoke --format json --output C:\dev\osla_datalake\aduana\runs\aduana_guardrails_smoke.json
osla-aduana-core-guardrails-smoke --format json
```

## Alcance

El smoke carga `SourceManifest` y `EvidenceItem` desde Gold local, construye un
`TradeCase` offline y valida que `core_guardrails` permanezca en postura segura.

No hace:

- red;
- FTP;
- lectura de ZIP/XML raw;
- OCR;
- embeddings;
- DB writes;
- storage writes.

## Señales Verificadas

- `modelops.model_route_status = model_selected`.
- `modelops.selected_model_id = frontier-review`.
- `modelops.human_review_required = true`.
- `voxbridge.action = lookup_trade_case`.
- `voxbridge.policy_status = allowed`.
- `data_broker.metadata_only = true`.
- `data_broker.material_operation_allowed = false`.
- `raw_payload_included = false`.
- `automatic_decision = false`.
- `final_ncm_allowed = false`.
- `final_regime_allowed = false`.

Si el datalake no existe o el contrato falla, el CLI devuelve exit code `1` y
emite un reporte `status = error` sin traceback.
