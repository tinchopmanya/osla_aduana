---
slug: osla_aduana
entidad: vertical
estado_documento: runtime_implementation_doc
tipo_archivo: runtime
canon_path: C:\dev\osla\osla_aduana\docs\ADUANA_2026_OFFLINE_RUNTIME.md
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
# Aduana 2026 Offline Runtime

Fecha: 2026-05-05
Estado: runtime offline implementado; contrato post-core fail-closed pendiente de
pin a core mergeado.

## Objetivo

Permitir que `osla_aduana` consuma el data lake local de Aduana 2026 sin leer
raw XML desde Git, sin escribir DB persistente/material, sin invocar modelos y
sin emitir decisiones automaticas.

## Data lake esperado

```text
C:\dev\osla_datalake\aduana
```

Entradas principales:

- `gold\evidence\2026\source_manifests.jsonl`
- `gold\evidence\2026\evidence_items.jsonl`
- `runs\aduana_2026_full_process_001\processing_summary.json`

El runtime acepta `year` y `run_id` para que el mismo contrato pueda consumir
futuros cortes 2025 o probes sin hardcodear el run 2026.

## Contratos implementados

- `SourceManifest`
- `EvidenceItem`
- `TradeCaseSourceContext`
- `TradeCase`
- `AduanaDataLake`
- `DataLakeReadinessReport`

## Reglas

- `db_writes` debe ser `0`.
- `automatic_decision` debe ser `false`.
- `raw_xml_copied_to_gold` debe ser `false`.
- `TradeCase` no embebe raw payloads.
- El runtime carga punteros de evidencia, no contenido raw.
- El smoke offline observa metadata de punteros con `broker_envelope.operation =
  metadata_observation`, `broker_envelope.decision = approved_metadata_only` y
  `broker_envelope.bytes_total = 0`.
- `modelops` debe quedar fail-closed por defecto:
  `model_route_status = blocked` y `selected_model_id = null` salvo decision
  explicita futura con `allow_model_use=true` y `policy_reference`.
- `DataLakeReadinessReport` debe reconciliar summary, manifests y evidence
  pointers antes de marcar el corpus como `ready_for_review`.

## Corte local Aduana 2026 observado

El data lake local observado previamente para `aduana_2026_full_process_001`
declara metadata de corpus ya preparado. Esta seccion es historica/auditiva: no
autoriza a este agente a descargar, abrir ZIP/XML, parsear material ni ejecutar
procesamiento nuevo.

- 127 ZIPs fuente declarados en bronze por entrega externa previa;
- 124.311.905 bytes fuente y bronze reconciliados;
- 381 miembros XML manifestados;
- 381 registros XML declarados en summary como parseados por entrega externa previa;
- 127 `SourceManifest`;
- 381 `EvidenceItem`;
- 0 hash mismatches;
- 0 parse errors;
- 0 OCR candidates;
- 0 DB writes;
- 0 model requests/inferences esperados para readiness post-core;
- `network_used=false`;
- `raw_files_written_to_repo=false`.

Estado runtime esperado solo despues de validar los artifacts ya preparados:
`ready_for_review`.

## Verificacion

```text
40 passed
```

Runner usado:

```text
C:\dev\nucleus\.venv\Scripts\python.exe -m pytest tests -q
```
