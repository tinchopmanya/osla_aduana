# Aduana Core Guardrails Runtime

Fecha: 2026-05-06
Estado: corte v0 integrado al runtime offline.

## Objetivo

El runtime offline de Aduana consume `osla-core` 0.3.6 para adjuntar metadata de
guardrails a cada `TradeCase` construido desde evidencia local Gold. Este corte
no abre FTP, no descarga, no lee XML raw, no ejecuta OCR, no escribe DB y no
genera decisiones finales.

## Superficie

- `AduanaDataLake.build_trade_case_from_evidence(...)` devuelve `TradeCase`
  con `core_guardrails`.
- `build_trade_case_guardrails(...)` puede evaluarse de forma aislada para
  casos offline o fixtures.

## Guardrails Incluidos

- `modelops`: ruteo deterministico a clase de modelo para `regime_review`.
  Solo metadata; no se llama ningun proveedor.
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

