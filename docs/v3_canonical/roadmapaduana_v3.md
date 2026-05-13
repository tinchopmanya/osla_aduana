---
slug: osla_aduana
entidad: vertical
estado_documento: mirror_do_not_edit_here
tipo_archivo: roadmap
canon_path: C:\dev\osla\osla_aduana\docs\v3_canonical\roadmapaduana_v3.md
supersedes: []
superseded_by: null
fuente_de_verdad: C:\dev\Investigacion_Osla_consolidada\FUENTE_DE_VERDAD_VERTICALES.md
no_usar_como_fuente_de_verdad: true
updated_at: 2026-05-13T02:55:45Z
owner: CODEX_5_5
auto_generated: false
disclaimers: []
mirror_of: C:\dev\Investigacion_Osla_consolidada\NUEVOSDOCUMENTOS_29deabril\roadmapaduana_v3.md
notas: mirror of V3 canonical import
encoding: ascii_puro
---
# ROADMAP ADUANA V3 — OSLA Aduana Trade Evidence Control Tower

**Archivo:** `roadmapaduana_v3.md`
**Fecha de corte:** 2026-04-29
**Proyecto:** OSLA
**Vertical principal:** `osla_aduana`
**Producto:** **OSLA Aduana — Trade Evidence Desk / Aduana Control Tower**
**Módulos absorbidos:** `osla_puerto`, `trade_compliance_audit`, `customs_entry_copilot`, `voxbridge_trade_case_followup`.
**Modo:** 10 agentes core en paralelo, descarga masiva controlada de fuentes públicas, web + API + mobile temprano, IA asistida con humano en loop.

---

## 0. Veredicto ejecutivo V3

`osla_aduana` queda como vertical prioritaria. La V3 no achica la idea; la solidifica.

La versión defendible no es “AI customs global”, ni “clasificador NCM autónomo”, ni “buscador de importaciones”. La versión viva es:

```text
OSLA Aduana V3
= Trade Evidence Desk UY
= régimen + documentos + proveedor/origen + NCM + puerto + voz gobernada + tareas + evidencia + decisión auditada
```

Frase de producto:

> OSLA Aduana convierte documentos, datos públicos, eventos portuarios y conversaciones de comercio exterior en casos operativos auditables, con tareas, evidencia, handoff y revisión humana.

### Mantener de V2

- Aduana como vertical principal.
- Puerto absorbido: AIS, ETA, BL, contenedor, demurrage, proof of delay.
- Descarga masiva controlada de fuentes públicas aprobadas.
- Product Shell común: casos, tareas, evidencia, timeline, decisiones y auditoría.
- ModelOps Cost Router: modelo barato/local/frontier según costo, sensibilidad y riesgo.
- Data Broker: permisos, fuente, PII, storage, OCR, embeddings, modelo permitido.
- Web, API y app móvil temprana.
- 10 agentes paralelos con merge owner único.

### Agregar en V3

- `VoxBridge / Voice Action Gateway` como capa de seguimiento, document requests, handoff y evidencia conversacional.
- Integración con `osla_licita / AI Bidroom` cuando una licitación depende de bienes importados.
- Integración explícita con `supplier_risk_ops`, `senaclaft_evidence_desk`, `backoffice_reconciliation_ops`, `complianceops_uy` y `retail_margin/demanda`.
- Matriz de acciones permitidas/prohibidas para voz, agentes y automatizaciones.
- Testing de voz/policy porque vendors como ElevenLabs/Vapi ya resuelven telefonía y testing básico.
- Endurecimiento de workflow automation: n8n/Airbyte/OSS sí, pero no sin aislamiento, permisos y monitoreo.

---

## 1. Hipótesis central validada

El cambio uruguayo de franquicias/IVA fortalece Aduana porque crea incertidumbre operativa real:

- nuevo tope anual de USD 800;
- hasta tres compras/franquicias por año;
- IVA salvo excepciones;
- régimen simplificado de 60% con mínimo USD 20;
- no hay reset del contador en mayo 2026;
- operadores postales/couriers pasan a ser actores tributarios centrales;
- excepción actual desde EE.UU. bajo condiciones específicas;
- registro de empresas extranjeras para exoneración;
- RG 12/2026 introduce transición/prórroga parcial y evidencia que el régimen está en ajuste.

Dolor vendible:

```text
No sé qué régimen aplica, qué documento falta, qué debo explicar al cliente,
qué parte es tributaria, qué parte es logística, qué parte necesita despachante,
y cómo dejo evidencia si hay reclamo, retención o demora.
```

OSLA Aduana vende cierre de ese caos.

---

## 2. A quién vender primero

| Prioridad | Buyer | Dolor | Oferta inicial |
|---:|---|---|---|
| 1 | Couriers/casilleros/operadores postales | Reclamos por IVA/franquicia, documentación, pagos, explicación al cliente. | `CourierOps + Régimen 800 + Evidence Pack + VoxBridge follow-up`. |
| 2 | Despachantes | Faltantes, NCM/origen/proveedor, coordinación, evidencia. | `Trade Evidence Desk` para 10-50 operaciones/mes. |
| 3 | Importadores pyme/e-commerce | Costo final, régimen, margen, proveedor, stock. | Simulador operativo + expediente documental. |
| 4 | Freight forwarders/agentes marítimos | ETA, contenedor, BL, demoras, demurrage, prueba de atraso. | Puerto Light + case evidence. |
| 5 | Proveedores del Estado/licita | Ofertar bienes importados sin controlar costo/plazo/NCM/origen. | Aduana integrada a AI Bidroom. |

---

## 3. Principios de diseño

1. No clasificar NCM como verdad legal final; solo sugerencia y revisión humana.
2. No reemplazar despachante.
3. No asumir DNA/VUCE operativa sin permiso, convenio o carga explícita.
4. Sí hacer descarga masiva controlada de fuentes públicas: manifest, hash, throttle, schema drift, dedupe, sensibilidad, auditoría.
5. No construir voz propia; usar vendors y gobernar acciones vía VoxBridge.
6. No construir dashboards muertos; cada pantalla debe producir tarea/evidencia/decisión/handoff.
7. No usar GPT/Opus para todo; enrutar por costo y sensibilidad.
8. Mobile temprano, pero acotado: estado, faltantes, upload, aprobación y handoff.
9. Evidence Pack obligatorio para cada caso.
10. Todo output debe registrar fuente, fecha, documento, modelo/cálculo, costo y responsable.

---

## 4. Arquitectura objetivo

```text
MEF / DNA público / FTP público / IMPO / ARCE / Uruguay XXI / ANP-AIS / documentos cliente / llamadas
  -> Data Broker
  -> Ingestion + Manifest Store
  -> Document Intelligence
  -> Regime Engine
  -> Supplier / Entity Resolution
  -> Puerto Events
  -> Trade Case Service
  -> Tasks / Evidence / Timeline / Audit
  -> VoxBridge Action Gateway
  -> API / Web / Mobile
  -> Human Review
```

| Componente | Función |
|---|---|
| `data_broker` | Permisos, sensibilidad, PII, storage, OCR, embeddings, modelo permitido. |
| `mass_ingest` | Descarga masiva controlada de fuentes públicas, manifests, hashes, diffs. |
| `aduana_regime` | Franquicia, IVA, 60%, general, obsequio, excepción USA, reglas versionadas. |
| `document_intel` | Factura, packing, certificado, BL/AWB, orden, email, comprobante. |
| `trade_case` | Caso operativo: operación, documentos, estado, riesgos, tareas. |
| `evidence_engine` | Evidence Pack formal y auditable. |
| `puerto_events` | AIS/ETA/contenedor/BL/demurrage/proof delay. |
| `voxbridge_gateway` | Acciones canónicas desde llamadas/chat vendors. |
| `modelops_router` | Local/barato/frontier según sensibilidad, costo y criticidad. |
| `api_gateway` | REST/webhooks/MCP. |
| `web_shell` | Control tower operativa. |
| `mobile_ops` | App para estado, faltantes, adjuntos y handoff. |

---

## 5. Estructura de repo recomendada

```text
/apps
  /api
  /web
  /mobile
  /admin
/packages
  /core_contracts
  /data_broker
  /mass_ingest
  /aduana_regime
  /document_intel
  /supplier_profile
  /puerto_events
  /voxbridge_gateway
  /modelops_router
  /ml_features
  /connectors
/docs
  /adr
  /decisions
  /research
  /runbooks
  /schemas
  /prompts
/data
  /manifests
  /samples
  /fixtures
```

---

## 6. Roadmap por fases

## Fase 0 — Preparación y contratos (Día 0-3)

Entregables:

- Repo base.
- `AGENTS.md`, `ROADMAP.md`, `PRODUCT.md`.
- Worktrees por agente.
- Contratos iniciales: `TradeCase`, `TradeDocument`, `EvidenceItem`, `Task`, `SourceManifest`, `RegimeDecision`, `VoiceActionEvent`.
- ADR 001: Aduana no reemplaza despachante ni decide NCM final.
- ADR 002: descarga masiva controlada de fuentes públicas.
- ADR 003: vendors de voz no tocan sistemas críticos directo.

Criterio de salida:

```text
10 worktrees + contratos + CI mínimo + ADRs iniciales.
```

---

## Fase 1 — Data Broker + Source Registry (Día 3-10)

Fuentes iniciales:

| Fuente | Tipo | Política V3 |
|---|---|---|
| MEF régimen envíos postales | Pública | Descargar/monitorear. |
| DNA Compras Web y Envíos | Pública | Descargar/monitorear. |
| DNA FTP anónimo | Pública/técnica | Descarga masiva controlada. |
| DNA FTP reservado LUCIA | Restringida | No acceder sin usuario/permiso. |
| IMPO JSON | Pública | Descargar/monitorear. |
| ARCE/RUPE/OCDS | Pública | Descargar si aporta a proveedor/licitación. |
| Uruguay XXI/SIE | Pública/agregada | Descargar/normalizar si hay endpoint/archivo. |
| ANP/AIS | Mixta | Público/comercial/convenio según proveedor. |
| Documentos cliente | Privada autorizada | Procesar con permiso explícito. |
| Llamadas/VoxBridge | Privada autorizada | Transcript/resumen con consentimiento/policy. |

Entregables:

- `source_registry.yml`
- `source_policy.yml`
- `pii_policy.yml`
- `storage_policy.yml`
- `model_policy.yml`
- CLI: `osla source check <source_id>`
- Endpoint: `GET /sources`, `POST /sources/{id}/validate-run`

---

## Fase 2 — Descarga masiva controlada / FTP público (Día 7-18)

Permitido:

- listar directorios públicos/anónimos;
- descargar en lote con límite de velocidad;
- registrar manifests;
- calcular hash;
- detectar nuevos/modificados/eliminados;
- guardar raw immutable;
- parsear solo si Data Broker habilita;
- alertar schema drift;
- deduplicar;
- pausar si hay error, bloqueo o cambio brusco.

No permitido:

- entrar a directorios reservados sin usuario LUCIA y autorización;
- evadir controles;
- scraping agresivo;
- publicar datos sensibles;
- enviar raw completo a modelos frontier sin clasificación.

Entregables:

- `ftp_inventory_job`
- `ftp_download_job`
- `manifest_store`
- `schema_probe`
- `hash_index`
- `raw_zone`, `parsed_zone`, `quarantine_zone`
- dashboard admin de ingesta;
- runbook de pausa.

Criterio:

```text
Primera corrida metadata-only + raw controlado + manifest + reporte schema drift.
```

---

## Fase 3 — Regime Engine 2026 (Día 10-22)

Reglas iniciales:

- Franquicia 3 envíos/año.
- Tope anual USD 800.
- IVA salvo excepciones.
- EE.UU. hasta USD 200 sin IVA bajo condiciones actuales.
- No reset en mayo 2026.
- Régimen simplificado 60% con mínimo USD 20.
- Máximo USD 800 por envío en simplificado.
- Peso máximo 20 kg.
- Exclusiones IMESI.
- Obsequio familiar como caso separado.
- Operador postal responsable.
- Fecha relevante: liberación/entrega/condición que corresponda según fuente, no solo compra.

Entregables:

- `RegimeInput`, `RegimeDecision`, `RegimeEvidence`, `RegimeRuleVersion`.
- Unit tests por escenario.
- Endpoint: `POST /regime/evaluate`.
- UI: “por qué aplica este régimen”.

Criterio:

```text
20 escenarios testados: USA <=200, China <=800, supera cupo, 4º envío, obsequio, simplificado, IMESI, peso >20kg, etc.
```

---

## Fase 4 — Document Intelligence (Día 12-30)

Documentos:

- factura comercial;
- invoice;
- packing list;
- certificado de origen;
- BL/AWB;
- comprobante de pago;
- orden de compra;
- email de proveedor;
- documento escaneado.

Stack sugerido:

- Docling para PDF/DOCX/HTML a Markdown/JSON.
- OCR/MinerU o alternativa para PDFs complejos.
- LLM local/barato para extracción simple.
- Frontier solo para casos complejos/ambiguos.

Entregables:

- `document_upload`
- `document_type_classifier`
- `field_extractor`
- `invoice_vs_packing_checker`
- `origin_certificate_checker`
- `document_gap_detector`
- evidencia por campo: fuente, página, confianza, modelo.

---

## Fase 5 — Trade Case + Evidence Pack (Día 18-35)

Estados:

```text
intake
needs_documents
ready_for_review
in_review
waiting_external
ready_for_broker
closed_ok
closed_with_risk
cancelled
```

Entregables:

- API CRUD de casos.
- Task board.
- Evidence Pack exportable.
- Timeline auditado.
- Estado visible para cliente/importador/despachante.

Criterio:

```text
Un caso nace desde documento, avanza por tareas, acumula evidencia y cierra con revisión humana.
```

---

## Fase 6 — VoxBridge Trade Follow-up (Día 25-45)

Vendors iniciales:

- ElevenLabs: transfer to human + webhooks post-call.
- Vapi: test suites y voice testing.
- Retell: opción fase 2.

Acciones permitidas:

```text
lookup_trade_case
lookup_missing_documents
create_document_request
create_task
update_basic_status
escalate_to_broker
escalate_to_importer
summarize_call_to_case
```

Acciones prohibidas:

```text
change_ncm_final
submit_customs_declaration
approve_operation
change_costs
release_goods
send_legal_instruction_without_review
delete_document
```

Entregables:

- `VoiceActionEvent` schema.
- `ActionPolicy` schema.
- Adapter ElevenLabs webhook.
- Adapter Vapi test harness.
- Endpoint: `POST /voice/events`.
- Endpoint: `POST /actions/execute` con policy check.
- UI: Voice timeline dentro del caso.

Criterio:

```text
Una llamada simulada crea document_request y otra intenta cambiar NCM final y es bloqueada por policy.
```

---

## Fase 7 — Puerto Light dentro de Aduana (Día 30-55)

No construir OSLA Puerto completo. Construir eventos útiles:

- buque/BL/contenedor;
- ETA;
- cambio ETA;
- estado en puerto si hay fuente;
- demora probable;
- demurrage estimate;
- proof of delay;
- hold documental/aduanero si se carga por cliente.

Entregables:

- `PortEvent`
- `ContainerEvent`
- `DelayEvidence`
- `DemurrageEstimate`
- UI: pestaña Puerto del TradeCase.

---

## Fase 8 — Web Product Shell (Día 20-60)

Pantallas:

1. Dashboard de casos con riesgo/faltantes.
2. Detalle de Trade Case.
3. Document Comparison View.
4. Regime Decision View.
5. Evidence Pack View.
6. Task Board.
7. VoxBridge Timeline.
8. Puerto Events View.
9. Admin Data Broker.
10. Admin Ingestion Monitor.

Regla UX:

```text
Cada pantalla responde: qué falta, quién debe actuar, con qué evidencia y cuál es el siguiente paso.
```

---

## Fase 9 — Mobile Ops (Día 35-70)

Stack: Expo / React Native.

Funciones:

- ver operaciones;
- recibir alerta;
- subir documento/foto;
- aprobar/rechazar tarea;
- consultar estado resumido;
- escalar a humano.

Criterio:

```text
Un importador recibe alerta, sube documento desde el celular y el caso actualiza evidencia.
```

---

## Fase 10 — ML/Evals/ModelOps (Día 20-75)

Baselines antes de ML complejo:

- reglas de régimen;
- heurísticas de faltantes;
- fuzzy matching descripción/NCM;
- z-score simple valor/peso si hay datos;
- promedios históricos por proveedor/categoría si hay cliente.

ML útil:

| Modelo | Fase | Nota |
|---|---|---|
| Document type classifier | M1 | Alta utilidad. |
| Field extraction confidence | M1 | Necesario. |
| NCM suggestion no vinculante | M2 | Humano decide. |
| Inconsistency ranking | M2 | Prioriza revisión. |
| Supplier/entity resolution | M2 | Defendible. |
| Delay/risk prediction | M3 | Requiere histórico. |
| Puerto ETA/demurrage | M3 | Requiere feed/eventos. |

Criterio:

```text
Cada caso muestra costo IA, modelo usado, confianza y escalamiento humano.
```

---

## Fase 11 — API-first / partner layer (Día 45-90)

Endpoints:

```text
POST /api/v1/trade-cases
GET  /api/v1/trade-cases/{id}
POST /api/v1/documents
POST /api/v1/regime/evaluate
POST /api/v1/tasks
POST /api/v1/voice/events
POST /api/v1/webhooks/document-request
GET  /api/v1/evidence-packs/{id}
```

Webhooks:

```text
case.created
document.missing
document.received
regime.assessed
task.created
voice.handoff
port.delay_detected
case.ready_for_review
```

---

## Fase 12 — Pilotos y GTM (Día 30-90)

| Piloto | Objetivo | Métrica |
|---|---|---|
| Courier/casillero | Régimen + faltantes + explicación cliente | 20 casos. |
| Despachante | Evidence Desk documental | 10 operaciones, 10+ tareas/faltantes. |
| Importador/e-commerce | Simulación + evidencia + mobile upload | 5 operaciones. |
| Licita | Producto importado para oferta | 1 bid/no-bid con evidencia. |
| Forwarder | Puerto event + proof delay | 5 eventos logísticos útiles. |

Pricing inicial:

| Oferta | Precio |
|---|---:|
| Auditoría por operación | USD 50-150 |
| Pack 10 operaciones | USD 400-1.000 |
| CourierOps starter | USD 300-800/mes |
| Despachante Pro | USD 500-1.500/mes |
| Importador/e-commerce | USD 199-800/mes |
| Setup VoxBridge | USD 500-2.000 |
| API/webhook partner | desde USD 499/mes |

---

## 7. Uso de OSS y vendors

| Necesidad | Herramienta | Decisión |
|---|---|---|
| Workflows internos | n8n | Sí, self-host aislado; cuidado con code nodes y exposición pública. |
| Data integration | Airbyte | Útil para conectores y data movement. |
| Document conversion | Docling | Prioritario para PDF/DOCX/HTML. |
| OCR/PDF complejo | MinerU/OCR alternativo | Validar con documentos reales. |
| LLM local | Ollama/vLLM/llama.cpp | Para privacidad y costo. |
| Observability | Langfuse | Traces, prompts, evals, costos. |
| Gateway/model routing | LiteLLM/Portkey/simple propio | Según complejidad. |
| Policy | OPA o motor simple inicial | Acciones permitidas/prohibidas. |
| Voice vendors | ElevenLabs + Vapi | No construir voz propia. |
| Mobile | Expo/React Native | MVP rápido si contratos listos. |

---

## 8. Riesgos y mitigaciones

| Riesgo | Severidad | Mitigación |
|---|---:|---|
| Alcance demasiado amplio | Alta | Trade Evidence Desk como core; Puerto/Vox/Licita son módulos. |
| Calculadora B2C | Alta | B2B/B2B2C con casos/evidencia. |
| Competir con Flexport/Digicust | Alta | Foco UY, documentos cliente, régimen local, humano. |
| FTP cambia schema | Alta | Manifests, schema drift, quarantine, rollback. |
| Datos privados mal usados | Crítica | Data Broker obligatorio. |
| VoxBridge thin wrapper | Alta | Modelo canónico de acciones + policy + evidence. |
| n8n inseguro | Alta | Aislar, actualizar, restringir permisos y code nodes. |
| Mobile distrae | Media | Solo upload/estado/faltantes/handoff. |
| ML prematuro | Media | Baselines y evals antes de modelos complejos. |
| Sin documentos reales | Alta | Discovery obligatorio. |

---

## 9. Criterios de avance / muerte

### Advance 30 días

- 5 operaciones reales o semi-reales.
- 10+ faltantes/tareas detectados.
- Regime Engine con 20 escenarios.
- Evidence Pack generado.
- Voz simulada crea tarea y bloquea acción prohibida.
- FTP público inventory + manifest funciona.
- Cliente potencial valida ahorro de tiempo.

### Advance 60 días

- 1 piloto real.
- 20+ casos.
- Mobile upload operativo.
- API/webhook básico.
- Data Broker activo.
- Costo IA por caso visible.

### Kill / pivot

- Nadie entrega documentos.
- El usuario prefiere ChatGPT manual y no ve workflow.
- No hay buyer dispuesto a pagar.
- El MVP depende de DNA/VUCE operativa no disponible.
- Los agentes no mantienen coherencia sin sobrecosto.

---

## 10. Orden recomendado para 10 agentes

```text
Día 0-3:
  Padre + Arquitecto + contratos.

Día 3-10:
  Data Broker + Source Registry + Regime Engine + Document Intel skeleton.

Día 7-18:
  FTP massive controlled + Regime tests + TradeCase API.

Día 18-35:
  Evidence Pack + Web shell + VoxBridge adapter + document flows.

Día 30-55:
  Puerto light + Mobile app + ModelOps evals.

Día 45-90:
  API/webhooks + pilots + hardening + GTM.
```

---

## Fuentes y validaciones usadas en V3

### Archivos internos mergeados
- `roadmapaduana_v2.md`
- `agentsaduana_v2.md`
- `productoaduana_v2.md`
- `aduana__chatgpt_29_04_2026_v3.md`
- `verticals_chatgpt_29_04_2026_v3.md`
- `propuesta_cambio_licitaciones_v3.md`
- Olas de investigación `osla_aduana_*` y `osla_puerto_*` incorporadas en V2.

### Fuentes web verificadas al 29/04/2026
- MEF — Guía de preguntas frecuentes sobre régimen de envíos postales/franquicias.
- MEF — Decreto 50/2026 / régimen envíos postales.
- DNA — Compras Web y Envíos.
- DNA — RG 12/2026.
- DNA — exoneración IVA desde EE.UU.
- DNA — Sitio FTP detallado.
- Anthropic — Claude Opus 4.7 y Claude Design.
- GitHub — Copilot usage-based billing / AI Credits.
- ElevenLabs — transfer to human y webhooks.
- Vapi — Test Suites / Voice Testing.
- n8n, Docling, Airbyte.
- Flexport Winter 2026, Digicust AI Customs.
