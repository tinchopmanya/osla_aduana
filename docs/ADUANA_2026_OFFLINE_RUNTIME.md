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

## Reglas

- `db_writes` debe ser `0`.
- `automatic_decision` debe ser `false`.
- `raw_xml_copied_to_gold` debe ser `false`.
- `TradeCase` no embebe raw payloads.
- El runtime carga punteros de evidencia, no contenido raw.

## Verificacion

```text
14 passed
```

Runner usado:

```text
C:\dev\osla\osla_licita\.venv\Scripts\python.exe -m pytest
```
