# Aduana 2026 Offline Runtime

Fecha: 2026-05-05
Estado: runtime offline implementado.

## Objetivo

Permitir que `osla_aduana` consuma el data lake local de Aduana 2026 sin leer
raw XML desde Git, sin escribir DB y sin emitir decisiones automaticas.

## Data lake esperado

```text
C:\dev\osla_datalake\aduana
```

Entradas principales:

- `gold\evidence\2026\source_manifests.jsonl`
- `gold\evidence\2026\evidence_items.jsonl`
- `runs\aduana_2026_full_process_001\processing_summary.json`

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
- `DataLakeReadinessReport` debe reconciliar summary, manifests y evidence
  pointers antes de marcar el corpus como `ready_for_review`.

## Corte local Aduana 2026

El data lake local observado para `aduana_2026_full_process_001` declara:

- 127 ZIPs fuente copiados a bronze;
- 124.311.905 bytes fuente y bronze reconciliados;
- 381 miembros XML manifestados;
- 381 registros XML parseados;
- 127 `SourceManifest`;
- 381 `EvidenceItem`;
- 0 hash mismatches;
- 0 parse errors;
- 0 OCR candidates;
- 0 DB writes;
- `network_used=false`;
- `raw_files_written_to_repo=false`.

Estado runtime esperado: `ready_for_review`.

## Verificacion

```text
14 passed
```

Runner usado:

```text
C:\dev\osla\osla_licita\.venv\Scripts\python.exe -m pytest
```
