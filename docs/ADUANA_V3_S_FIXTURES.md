# Aduana V3-S Fixtures

Fecha: 2026-05-02
Estado: fixtures sinteticos offline para validators/tests. No habilita red, FTP, descarga, DB, storage, OCR, embeddings, parseo documental ni decisiones finales automaticas.

## 1. Objetivo

Este corte materializa fixtures JSON para `Trade Evidence Desk / Aduana Control Tower`.

Los archivos sirven como semilla para validators/tests offline de:

- `TradeCase`
- `EvidenceItem`
- `SourceManifest`
- input/output esperado de `RegimenEngine v0`
- faltantes `DocIntel`
- follow-up gobernado de `VoxBridge`

Todo el pack es inventado, deterministico y seguro para commit. No contiene datos reales, documentos completos, rutas remotas, credenciales, muestras, contenido reservado ni datos de clientes.

## 2. Archivos creados

| Archivo | Contenido | Registros |
|---|---|---:|
| `fixtures/v3_s/index.json` | Indice del pack y guards offline | 1 |
| `fixtures/v3_s/source_manifests.json` | Manifests sinteticos, incluido FTP publico bloqueado | 3 |
| `fixtures/v3_s/evidence_items.json` | Evidencias sinteticas con hashes no reales | 7 |
| `fixtures/v3_s/trade_cases.json` | Casos operativos sinteticos | 3 |
| `fixtures/v3_s/regimen_engine_scenarios.json` | Inputs y outputs esperados de regimen probable | 6 |
| `fixtures/v3_s/docintel_missing_requirements.json` | Faltantes documentales esperados sin OCR/parser | 3 |
| `fixtures/v3_s/voxbridge_followups.json` | Acciones permitidas, escaladas y denegadas | 5 |

## 3. Reglas aplicadas

- Todos los IDs usan prefijos `*_syn_*`.
- Todo `TradeCase.source_context.is_synthetic` es `true`.
- Todo `EvidenceItem.synthetic.real_source_touched` es `false`.
- Todo `SourceManifest.mode` es `synthetic_fixture`.
- Todo `SourceManifest.files_downloaded` y `bytes_downloaded` es `0`.
- Todo `SourceManifest.source_policy.network_allowed`, `db_writes_allowed` y `storage_writes_allowed` es `false`.
- Todo `RegimeAssessment.final_decision.ncm_final` es `null`.
- Todo `RegimeAssessment.final_decision.regime_final` es `null`.
- Todo `VoiceActionEvent.vendor` es `synthetic_fixture`.
- Todo `VoiceActionEvent.synthetic.real_vendor_touched` es `false`.
- Las acciones prohibidas quedan `denied` o `escalated`.

## 4. Casos cubiertos

### TradeCase

- `tc_syn_missing_docs_0001`: intake sintetico con factura, packing y revision humana faltantes.
- `tc_syn_ready_review_0002`: caso con evidencias stub y regimen probable sujeto a revision.
- `tc_syn_policy_block_0003`: intento sintetico bloqueado por policy de fuente restringida.

### RegimenEngine

Los escenarios cubren ramas `unknown_needs_review`, `regimen_general`, `courier`, `franquicia`, `iva` y `sesenta_por_ciento`.

Son fixtures de comportamiento, no de exactitud juridica. Cada expected output declara:

```json
"final_decision": {
  "ncm_final": null,
  "regime_final": null,
  "decided_by": null
}
```

### DocIntel

`docintel_missing_requirements.json` solo modela gap analysis. El archivo declara explicitamente:

- `ocr_allowed: false`
- `parser_allowed: false`
- `embeddings_allowed: false`
- `model_extraction_allowed: false`
- `document_content_available: false`

### VoxBridge

El pack cubre:

- allowed: `create_document_request`
- allowed: `lookup_missing_documents`
- escalated: `send_legal_instruction_without_review`
- denied: `change_ncm_final`
- denied: `access_reserved_dna_or_vuce`

VoxBridge coordina faltantes y handoff; no decide NCM final, regimen final, liberacion, filing, costos ni instrucciones juridicas sin humano.

## 5. P0/P1/P2

### P0

- Los validators ejecutables aun viven fuera de este ownership.
- No existe CI local en este repo que bloquee red o operaciones materiales.
- No existe schema ejecutable versionado para rechazar `ncm_final` o `regime_final` no nulos.
- `SourceManifest` para `uy.dna.public_ftp` queda bloqueado hasta decision humana y prerequisitos de Data Broker.
- No hay permiso de metadata preflight, descarga, storage, DB, OCR, embeddings ni parseo.

### P1

- Convertir los contratos V3-R/V3-S a schemas ejecutables.
- Agregar tests que recorran recursivamente todos los JSON de `fixtures/v3_s`.
- Expandir matriz de documentos y sensibilidad por tipo.
- Agregar mas escenarios VoxBridge para `denied`, `escalated` y sensibilidad `pii`.
- Agregar snapshot de evidence pack completo cuando exista contrato.

### P2

- Crear generador deterministico de fixtures.
- Agregar reporte de coverage de policies.
- Definir naming final de `SourceManifest.id` si el contrato ejecutable lo requiere.
- Conectar estos fixtures a Product Shell solo despues de contracts/tests offline.

## 6. Validacion manual esperada

Comandos usados para este corte:

```powershell
cd C:\dev\osla\osla_aduana
Get-ChildItem -LiteralPath .\fixtures\v3_s -Filter *.json | ForEach-Object { Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json | Out-Null }
git diff --check
```

## 7. Confirmacion

Este entregable es 100% sintetico y offline. No se toco red, FTP, datos reales, contenido reservado, storage, DB, OCR ni embeddings. No se declara descarga aprobada. No hay NCM final automatico ni regimen final automatico.
