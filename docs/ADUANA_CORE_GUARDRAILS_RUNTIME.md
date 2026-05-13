---
slug: osla_aduana
entidad: vertical
estado_documento: runtime_implementation_doc
tipo_archivo: runtime
canon_path: C:\dev\osla\osla_aduana\docs\ADUANA_CORE_GUARDRAILS_RUNTIME.md
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
# Aduana Core Guardrails Runtime

Fecha: 2026-05-06
Estado: corte v0 integrado al runtime offline post-core fail-closed.

## Objetivo

El runtime offline de Aduana consume `osla-core` desde el workspace local durante
validacion y debe pinnearse al SHA mergeado de core fail-closed antes de release.
Adjunta metadata de guardrails a cada `TradeCase` construido desde evidencia
local Gold. Este corte no abre FTP, no descarga, no lee XML raw, no ejecuta OCR,
no genera embeddings, no invoca modelos, no escribe DB persistente/material y no
genera decisiones finales.

## Superficie

- `AduanaDataLake.build_trade_case_from_evidence(...)` devuelve `TradeCase`
  con `core_guardrails`.
- `build_trade_case_guardrails(...)` puede evaluarse de forma aislada para
  casos offline o fixtures.

## Guardrails Incluidos

- `modelops`: fail-closed por defecto para `regime_review`. Sin
  `allow_model_use=true` y `policy_reference` explicitos, el estado esperado es
  `blocked`, `selected_model_id = null` y costo `0.0`. Solo metadata; no se
  llama ningun proveedor.
- `voxbridge`: policy sobre `lookup_trade_case`. Solo decision de policy; no
  existe gateway vendor real en este corte.
- `data_broker`: postura metadata-only. Cualquier operacion material futura
  queda marcada como no permitida y requiere broker separado.
- `codeguard`: sin modelo directo, sin copia raw entre verticales y sin
  operacion material fuera de broker.
- `domain_controls`: revision humana obligatoria, sin NCM final, sin regimen
  final y sin instrucciones de filing desde el runtime offline.

## Tests

- `tests/test_offline_runtime.py`
