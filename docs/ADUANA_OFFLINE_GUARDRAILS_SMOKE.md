---
slug: osla_aduana
entidad: vertical
estado_documento: runtime_implementation_doc
tipo_archivo: runtime
canon_path: C:\dev\osla\osla_aduana\docs\ADUANA_OFFLINE_GUARDRAILS_SMOKE.md
supersedes: []
superseded_by: null
fuente_de_verdad: C:\dev\Investigacion_Osla_consolidada\FUENTE_DE_VERDAD_VERTICALES.md
no_usar_como_fuente_de_verdad: false
updated_at: 2026-05-13T02:55:45Z
owner: CODEX_5_5
auto_generated: false
disclaimers: []
mirror_of: null
notas: runtime/offline/handoff/contract document
encoding: ascii_puro
---
# Aduana Offline Guardrails Smoke

Fecha: 2026-05-06
Estado: smoke CLI local post-core fail-closed.

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
- modelos;
- DB writes persistentes/materiales;
- storage writes.

## Senales Verificadas

- `modelops.model_route_status = blocked`.
- `modelops.selected_model_id = null`.
- `modelops.human_review_required = true`.
- `voxbridge.action = lookup_trade_case`.
- `voxbridge.policy_status = allowed`.
- `data_broker.metadata_only = true`.
- `data_broker.material_operation_allowed = false`.
- `broker_envelope_generated = true`.
- `broker_envelope.operation = metadata_observation`.
- `broker_envelope.decision = approved_metadata_only`.
- `broker_envelope.bytes_total = 0`.
- `broker_envelope.manifest_required = false`.
- `broker_envelope.metadata_only = true`.
- `broker_envelope.material_operation_allowed = false`.
- `broker_envelope.decision_json.allow_material_reads = false`.
- `broker_envelope.decision_json.allow_network_access = false`.
- `broker_envelope.decision_json.allow_db_writes = false`.
- `broker_envelope.decision_json.allow_model_use = false`.
- `raw_payload_included = false`.
- `automatic_decision = false`.
- `final_ncm_allowed = false`.
- `final_regime_allowed = false`.

El smoke falla (`status = failed`) si `modelops.model_route_status` deja de ser
`blocked`, si `modelops.selected_model_id` no es `null` o si
`modelops.human_review_required` deja de ser `true`.

El `broker_envelope` es evidencia de observacion metadata-only in-memory para
auditoria. No ejecuta operacion material, no autoriza descarga, no abre ZIP/XML
raw, no usa red, no invoca modelos y no persiste DB externa. Los bytes de los
ZIP pueden aparecer solo como metadata declarada dentro de `pointer_manifest`;
`broker_envelope.bytes_total` debe permanecer en `0`.

Si el datalake no existe o el contrato falla, el CLI devuelve exit code `1` y
emite un reporte `status = error` sin traceback.
