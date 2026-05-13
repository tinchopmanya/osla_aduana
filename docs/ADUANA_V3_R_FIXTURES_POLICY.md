---
slug: osla_aduana
entidad: vertical
estado_documento: runtime_implementation_doc
tipo_archivo: contrato
canon_path: C:\dev\osla\osla_aduana\docs\ADUANA_V3_R_FIXTURES_POLICY.md
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
# Aduana V3-R Fixtures Policy

Fecha: 2026-05-02
Estado: politica documental offline para fixtures sinteticos. No habilita runtime material.

## 1. Objetivo

Definir como deben construirse, marcarse y validarse fixtures sinteticos para el corte `offline_contracts_and_policy_v0` de OSLA Aduana.

La politica existe para que los proximos agentes puedan crear tests y contratos sin tocar fuentes reales, contenido reservado, datos de clientes, DB, storage, OCR, embeddings ni red.

## 2. Regla madre

Todo fixture V3-R debe ser:

- sintetico;
- trazable como fixture;
- libre de contenido real;
- seguro para commit;
- incapaz de ser confundido con una decision aduanera final;
- compatible con auditoria futura.

Si un dato no puede verificarse sintetico, se trata como no permitido.

## 3. P0 absolutos

Queda prohibido para fixtures V3-R:

- tocar `ftp://ftp.aduanas.gub.uy` o cualquier red real;
- listar directorios remotos, aunque sea metadata-only;
- descargar ZIP, CSV, XML, PDF, imagenes o binarios;
- abrir contenido real de DNA, VUCE, LUCIA, DGI, BCU, IMPO, cliente o vendor;
- usar credenciales, cookies, tokens, secretos o `.env`;
- escribir DB, storage, buckets, colas o caches persistentes;
- crear migraciones;
- correr OCR, embeddings, parsers documentales o modelos;
- incluir RUT, CI, nombres, telefonos, emails, direcciones o documentos reales;
- afirmar NCM final, regimen final, liberacion, filing, liquidacion o aprobacion automatica.

## 4. Campos obligatorios de sinteticidad

Todo fixture debe incluir una marca equivalente a:

```yaml
synthetic:
  is_synthetic: true
  real_source_touched: false
```

Para voz:

```yaml
synthetic:
  is_synthetic: true
  real_vendor_touched: false
```

Para `TradeCase`:

```yaml
source_context:
  intake_channel: synthetic_seed
  is_synthetic: true
```

Para `SourceManifest`:

```yaml
mode: synthetic_fixture
files_downloaded: 0
bytes_downloaded: 0
source_policy:
  network_allowed: false
  db_writes_allowed: false
  storage_writes_allowed: false
```

## 5. Naming permitido

Usar prefijos que impidan confusion con datos reales:

| Tipo | Prefijo |
|---|---|
| TradeCase | `tc_syn_` |
| EvidenceItem | `ev_syn_` |
| SourceManifest | `sm_syn_` o `run_syn_` |
| RegimeAssessment | `ra_syn_` |
| VoiceActionEvent | `va_syn_` |
| Task | `task_syn_` |
| Party | `party_syn_` |
| Document | `doc_syn_` |
| TimelineEvent | `tle_syn_` |

No usar IDs, codigos o numeros que parezcan extraidos de sistemas reales.

## 6. Datos sinteticos permitidos

Permitido:

- nombres genericos como `Importador Sintetico SA`;
- referencias `fixture://...`;
- hashes obviamente sinteticos como `sha256:synthetic-not-real-0001`;
- paises ISO de ejemplo;
- valores monetarios redondos de prueba;
- descripciones genericas de mercaderia;
- documentos con estado `missing` o `received` sin contenido material;
- transcripts resumidos inventados y marcados como sinteticos.

No permitido:

- copiar snippets de documentos reales;
- usar nombres de empresas uruguayas reales;
- usar RUT/CI reales o plausibles sin marca `redacted`;
- usar URLs reales como si hubieran sido consultadas;
- usar rutas FTP reales como allowlist ejecutable;
- usar archivos locales externos como fixture source;
- incorporar texto de normativa como si fuera una interpretacion vigente.

## 7. Politica de sensibilidad

| Sensibilidad | Uso en fixture | Restricciones |
|---|---|---|
| `public` | Datos inventados no personales. | No implica fuente publica real. |
| `internal` | Caso operativo sintetico. | Default recomendado. |
| `confidential` | Simula documentos cliente. | Sin contenido material. |
| `pii` | Evitar salvo test de policy. | Debe estar redacted/fake y no enviarse. |
| `restricted` | Solo para probar bloqueo. | No puede disparar acciones automaticas. |

Regla: fixtures que simulan `restricted` solo existen para probar denegacion.

## 8. Source policy para `uy.dna.public_ftp`

Estado obligatorio en V3-R:

```yaml
source_id: uy.dna.public_ftp
state: blocked_until_prereqs_closed
access_class: public_restricted
license_status: unknown_needs_review
network_allowed: false
metadata_preflight_allowed: false
download_allowed: false
db_writes_allowed: false
storage_writes_allowed: false
```

No se puede pasar a una decision `approved_metadata_only` hasta cerrar lo definido en `ADUANA_FTP_SOURCE_PREREQS.md`:

- owner humano de fuente;
- licencia/terminos por path o dataset;
- allowlist aprobada y no vacia;
- denylist dura;
- throttling/concurrency/stop conditions;
- ledger/reporte sin DB;
- confirmacion de `files_downloaded = 0`;
- confirmacion de `bytes_downloaded = 0`;
- aprobacion explicita de Data Broker.

## 9. Denylist dura

Todo policy evaluator futuro debe bloquear referencias que contengan o normalicen patrones como:

```text
lucia
vuce
reservado
reservada
privado
privada
credencial
credential
password
secret
token
cookie
operador
usuario
login
```

Tambien debe bloquear intentos de:

- acceso a directorios reservados;
- uso de credenciales LUCIA;
- uso de datos cliente sin consentimiento;
- extrapolar licencia DAG de datasets catalogados al FTP completo.

## 10. Politica RegimenEngine fixture

Los fixtures de regimen deben probar comportamiento, no exactitud juridica.

### Permitido

- Casos `unknown_needs_review`.
- Casos de `franquicia`, `iva`, `sesenta_por_ciento`, `courier` y `regimen_general` como escenarios sinteticos.
- Explicaciones operativas: "falta factura", "requiere revision humana", "documentacion insuficiente".
- Confidence baja/media/alta como etiqueta de test.

### Prohibido

- `regime_final` distinto de `null`.
- `ncm_final` distinto de `null`.
- Liquidacion definitiva de tributos.
- Citas legales extensas o interpretaciones normativas como conclusion final.
- Recomendaciones que sustituyan al despachante.

Fixture minimo esperado:

```yaml
final_decision:
  ncm_final: null
  regime_final: null
  decided_by: null
disclaimer: human_review_required_no_legal_advice
```

## 11. Politica VoxBridge fixture

Los fixtures de voz deben cubrir al menos una accion permitida y una prohibida.

### Allowed baseline

```yaml
normalized_action: create_document_request
action_status: allowed
policy_reason: "Accion permitida: solicitar documento faltante y crear tarea."
```

### Denied baseline

```yaml
normalized_action: change_ncm_final
action_status: denied
policy_reason: "Accion prohibida: NCM final requiere humano."
```

### Escalated baseline

```yaml
normalized_action: send_legal_instruction_without_review
action_status: escalated
policy_reason: "Requiere revision humana antes de cualquier instruccion legal."
```

VoxBridge nunca puede:

- cambiar NCM final;
- aprobar operacion;
- presentar declaracion aduanera;
- cambiar costos;
- liberar mercaderia;
- borrar documentos;
- acceder a DNA/VUCE/LUCIA reservado.

## 12. Evidence policy

Cada fixture que haga un claim operativo debe referenciar evidencia o declarar faltante.

Permitido:

```yaml
evidence_item_id: ev_syn_0001
excerpt_or_hash: "sha256:synthetic-not-real-0001"
```

Permitido para faltantes:

```yaml
evidence_item_id: null
missing_requirements:
  - requirement_type: document
```

No permitido:

- claims sin evidencia y sin faltante;
- excerpts largos;
- contenido real;
- documentos completos en YAML/JSON;
- hashes de archivos reales.

## 13. PuertoLight en fixtures

PuertoLight puede aparecer solo como evento adjuntable a `TradeCase`.

Permitido futuro:

```yaml
event_type: puerto_delay_reported
trade_case_id: tc_syn_0001
evidence_item_id: ev_syn_port_0001
```

Prohibido:

- crear una vertical `OSLA Puerto`;
- crear flujo independiente que no termine en `TradeCase`;
- usar AIS, ETA, contenedores o proveedores comerciales reales en V3-R.

## 14. Tests futuros esperados

Primer paquete de tests offline:

| Test | Resultado esperado |
|---|---|
| `test_fixture_ids_have_syn_prefix` | pasa |
| `test_no_real_source_touched` | pasa |
| `test_source_manifest_zero_downloads` | pasa |
| `test_ftp_network_denied` | pasa |
| `test_denylist_blocks_lucia_vuce_reserved` | pasa |
| `test_regime_final_is_null` | pasa |
| `test_ncm_final_is_null` | pasa |
| `test_voice_allowed_create_document_request` | pasa |
| `test_voice_denied_change_ncm_final` | pasa |
| `test_restricted_sensitivity_blocks_auto_action` | pasa |

## 15. Review checklist antes de merge futuro

- El fixture contiene `is_synthetic: true`.
- El fixture contiene `real_source_touched: false` o `real_vendor_touched: false`.
- No hay URLs o rutas reales que parezcan consultadas.
- No hay datos personales o empresariales reales.
- No hay contenido documental real.
- No hay `files_downloaded` o `bytes_downloaded` mayor a cero.
- No hay `network_allowed: true`.
- No hay `db_writes_allowed: true` ni `storage_writes_allowed: true`.
- No hay `ncm_final` ni `regime_final`.
- Acciones VoxBridge prohibidas quedan `denied` o `escalated`.
- El caso termina en tarea, evidencia, faltante, handoff o decision humana.

## 16. P0/P1/P2

### P0

- Estado historico V3-R: la policy no estaba implementada como validador ejecutable en este corte.
- Estado actualizado V3-S: `fixtures/v3_s/*.json` y `tests/test_v3_s_fixtures_policy.py` materializan fixtures y validator offline. Este documento queda subordinado a `docs/ADUANA_V3_S_FIXTURES.md` y `docs/ADUANA_V3_S_VALIDATORS.md`.
- No existe CI que bloquee red o descargas.
- No existe detector automatizado de contenido real o secretos.
- V3-S agrega policy gate offline para VoxBridge, `ncm_final = null` y `regime_final = null`; el gap restante es CI/schema versionado, no la ausencia total de validator.

### P1

- Falta definir formato final de fixtures: YAML, JSON o Python objects.
- Falta decidir ubicacion: `packages/core_contracts/fixtures` o `tests/fixtures`.
- Falta matriz completa de documentos y sensibilidad.
- Falta set amplio de regimenes sinteticos.
- Falta set amplio de acciones VoxBridge.
- Falta snapshot de evidence pack offline.

### P2

- Agregar generador de fixtures deterministico.
- Agregar linter de fixtures.
- Agregar reporte de coverage de policies.
- Agregar docs de contribucion para nuevos fixtures.
- Mapear datasets catalogados DNA como carril futuro separado del FTP completo.

## 17. Siguiente corte tecnico seguro

```text
v3-s-fixtures-policy-enforced-offline
```

Entregables:

- fixtures sinteticos versionados en archivos;
- schemas ejecutables;
- policy evaluator offline;
- tests unitarios sin red;
- reporte local con cero red, cero descargas, cero DB/storage, cero OCR/embeddings;
- matriz de denied cases para FTP, VUCE, LUCIA, VoxBridge y RegimenEngine.

Fuera de alcance:

- red real;
- FTP metadata preflight;
- acceso a documentos;
- OCR/embeddings;
- DB/storage;
- migraciones;
- decision final automatica.
