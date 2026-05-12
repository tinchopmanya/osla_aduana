---
status: mirror_do_not_edit_here
mirror_marked_at: 2026-05-12
mirror_of: C:\dev\Investigacion_Osla_consolidada\NUEVOSDOCUMENTOS_29deabril\agentsaduana_v3.md
reason: V3 canonical master copy lives in Investigacion_Osla_consolidada/NUEVOSDOCUMENTOS_29deabril.
do_not_use_for: standalone_editing
---

# AGENTS ADUANA V3 — Contrato de ejecución paralela para OSLA Aduana

**Archivo:** `agentsaduana_v3.md`
**Fecha de corte:** 2026-04-29
**Proyecto:** OSLA Aduana V3
**Modo:** 10 agentes core en paralelo + subagentes temporales.
**Modelos:** Codex GPT-5.5, Claude Opus 4.7, Claude Design, modelos locales/open-weight cuando convenga.
**Producto:** Trade Evidence Desk / Aduana Control Tower con Puerto y VoxBridge absorbidos.

---

## 0. Regla madre

Cada agente debe producir un incremento verificable. No se aceptan entregas que sean solo opinión.

Toda salida debe caer en una de estas categorías:

- código ejecutable;
- contrato/API/schema;
- test/eval;
- documentación operativa;
- decisión arquitectural;
- evidence pack;
- conector de datos;
- pantalla funcional;
- discovery comercial accionable.

La cadena obligatoria de producto:

```text
dato / documento / evento / llamada
    -> alerta
    -> caso
    -> tarea
    -> evidencia
    -> decisión/handoff
    -> auditoría
```

Si un cambio no aporta a esa cadena, se marca `parked`.

---

## 1. Topología de 10 agentes core

| # | Agente | Modelo sugerido | Rol | Ownership principal |
|---:|---|---|---|---|
| 0 | **CodexPadre** | GPT-5.5 Codex | Orquestador, merge owner, CI, releases, decisiones finales | repo completo, `docs/decisions`, `main` |
| 1 | **ArquitectoAduana** | Claude Opus 4.7 | Arquitectura, ADR, contratos, límites legales/técnicos | `docs/adr`, `packages/core_contracts` |
| 2 | **DataBrokerFTP** | GPT-5.5 Codex | Source registry, Data Broker, descarga masiva controlada, manifests | `packages/data_broker`, `packages/mass_ingest` |
| 3 | **RegimenEngine** | GPT-5.5 Codex | Franquicia, IVA, 60%, régimen general, reglas versionadas | `packages/aduana_regime` |
| 4 | **DocIntel** | Claude Opus 4.7 + Codex | Document AI, OCR, extracción, comparación documental | `packages/document_intel` |
| 5 | **TradeCaseEvidence** | GPT-5.5 Codex | Casos, tareas, evidence pack, timeline, audit | `packages/core_contracts`, `apps/api` |
| 6 | **PuertoLight** | GPT-5.5 Codex | Eventos puerto: AIS/ETA/contenedor/demurrage/proof delay | `packages/puerto_events` |
| 7 | **VoxBridgeGateway** | Claude Opus 4.7 + Codex | Voice Action Gateway, adapters, policy, handoff | `packages/voxbridge_gateway` |
| 8 | **ProductUXMobile** | Claude Design + Codex | Web Product Shell + mobile operativo | `apps/web`, `apps/mobile` |
| 9 | **MLEvalsModelOps** | Claude Opus 4.7 + Codex | Model routing, evals, costos, baselines ML, QA automatizado | `packages/modelops_router`, `packages/ml_features`, `docs/evals` |

### Subagentes temporales permitidos

No tienen permiso de merge:

- `GTMResearch`: buyers, pricing, discovery.
- `OSSScout`: OSS útil o competidor.
- `SecurityReviewer`: n8n, webhooks, PII, auth.
- `LicitaBridge`: integración con AI Bidroom.
- `SupplierRiskBridge`: perfil proveedor/entity resolution.
- `CriticalAuditor`: intenta matar el plan.

---

## 2. Reglas de worktrees y ramas

Cada agente trabaja en worktree separado.

```bash
git worktree add ../osla-aduana.wt/<agent-slug> -b agent/<agent-slug>/<task-slug>
```

Ejemplos:

```text
agent/data-broker/source-registry
agent/regime-engine/iva-franquicia-2026
agent/doc-intel/invoice-extraction
agent/voxbridge/action-policy
agent/mobile/document-upload
```

### Prohibido

- Trabajar directo sobre `main`.
- Dos agentes modificando el mismo archivo core sin coordinación de CodexPadre.
- Crear migraciones incompatibles en paralelo sin ADR.
- Cambiar contratos públicos sin avisar a dependientes.
- Tocar `.env` o secretos.
- Agregar vendor/SDK pesado sin ADR.
- Construir features fuera de la cadena caso/tarea/evidencia.
- Hacer scraping o acceso a fuente reservada sin Data Broker.

### Merge

Solo `CodexPadre` mergea.

Antes de merge:

- tests pasan;
- lint/format si existe;
- contratos actualizados;
- docs mínimas;
- evidence pack del cambio;
- riesgos declarados;
- no hay secretos;
- no rompe ownership de otro agente.

---

## 3. Modelo de cierre obligatorio

Cada agente entrega este bloque al final de su sesión:

```markdown
## cierre-agente
agente: <nombre>
branch: <branch>
worktree: <path>
status: completed | blocked | failed
summary: |
  Qué se hizo en 2-5 frases.
files_touched:
  - path
commands_run:
  - command
validation:
  - test/lint/manual check
risks:
  - riesgo o []
contracts_changed:
  - contrato o []
next_step:
  Una frase.
merge_ready: true | false
```

CodexPadre consolida estos cierres en `docs/runlogs/YYYY-MM-DD.md`.

---

## 4. Decisión de modelos

| Tarea | Modelo por defecto | Escalamiento |
|---|---|---|
| Código backend/API/test | Codex GPT-5.5 | Claude Opus 4.7 para arquitectura o bugs difíciles. |
| Arquitectura/ADR/contratos complejos | Claude Opus 4.7 | Codex implementa después. |
| UI/prototipos/slides/demo | Claude Design + Codex | Humano decide estilo final. |
| Extracción documental simple | Modelo local/barato | Frontier si baja confianza o documento crítico. |
| Documento sensible | Local primero | Frontier solo con redacción/policy. |
| Voz/transcripción/resumen | Vendor + modelo barato | Frontier si hay ambigüedad legal/operativa. |
| NCM/HS sugerido | Local/RAG/heurística | Frontier + despachante para revisión. |
| Decisión final | Nunca IA sola | Humano obligatorio. |

Regla:

```text
modelo caro solo si el caso lo justifica y queda registrado costo/modelo/motivo.
```

---

## 5. Ownership por carpeta

| Carpeta | Owner primario | Owners secundarios |
|---|---|---|
| `packages/core_contracts` | ArquitectoAduana | TradeCaseEvidence |
| `packages/data_broker` | DataBrokerFTP | ArquitectoAduana, MLEvalsModelOps |
| `packages/mass_ingest` | DataBrokerFTP | SecurityReviewer |
| `packages/aduana_regime` | RegimenEngine | ArquitectoAduana |
| `packages/document_intel` | DocIntel | MLEvalsModelOps |
| `packages/puerto_events` | PuertoLight | TradeCaseEvidence |
| `packages/voxbridge_gateway` | VoxBridgeGateway | MLEvalsModelOps, SecurityReviewer |
| `packages/modelops_router` | MLEvalsModelOps | DataBrokerFTP |
| `apps/api` | TradeCaseEvidence | RegimenEngine, VoxBridgeGateway |
| `apps/web` | ProductUXMobile | TradeCaseEvidence |
| `apps/mobile` | ProductUXMobile | VoxBridgeGateway |
| `docs/adr` | ArquitectoAduana | CodexPadre |
| `docs/evals` | MLEvalsModelOps | CriticalAuditor |

---

## 6. Contratos canónicos

### TradeCase

```yaml
TradeCase:
  id: string
  tenant_id: string
  buyer_type: courier | despachante | importador | forwarder | marketplace | licita
  status: intake | needs_documents | ready_for_review | in_review | waiting_external | ready_for_broker | closed_ok | closed_with_risk | cancelled
  parties: [TradeParty]
  documents: [TradeDocument]
  items: [TradeItem]
  regime_assessment: RegimeAssessment?
  risks: [RiskSignal]
  tasks: [Task]
  evidence_pack_id: string?
  timeline: [TimelineEvent]
  human_reviewer_id: string?
```

### EvidenceItem

```yaml
EvidenceItem:
  id: string
  source_id: string
  source_type: public_web | public_ftp | client_document | voice_event | manual | api | model_output
  captured_at: datetime
  source_ref: string
  excerpt_or_hash: string
  model_used: string?
  cost_estimate_usd: number?
  confidence: number?
  human_validated: boolean
  sensitivity: public | internal | confidential | pii | restricted
```

### VoiceActionEvent

```yaml
VoiceActionEvent:
  id: string
  vendor: elevenlabs | vapi | retell | manual
  conversation_id: string
  trade_case_id: string?
  requested_action: string
  action_status: allowed | denied | escalated | failed
  policy_reason: string
  transcript_ref: string?
  summary: string
  created_task_id: string?
  evidence_item_id: string?
```

### SourceManifest

```yaml
SourceManifest:
  source_id: string
  run_id: string
  run_started_at: datetime
  mode: metadata_only | raw_download | parse | diff
  files_seen: number
  files_downloaded: number
  bytes_downloaded: number
  hashes_changed: number
  schema_warnings: [string]
  quarantine_count: number
```

---

## 7. Políticas de Data Broker

| Tipo | Ejemplo | Acción permitida |
|---|---|---|
| Pública web | MEF, DNA Compras Web, IMPO | Descargar/monitorear con atribución. |
| Pública FTP anónima | FTP DNA público | Descarga masiva controlada. |
| Reservada | LUCIA reservado, VUCE operativa | No acceder sin permiso/convenio. |
| Cliente | facturas, packing, BL | Procesar con consentimiento; sensibilidad alta. |
| Conversacional | llamadas, WhatsApp, emails | Transcript/resumen solo con policy/consentimiento. |
| Comercial | AIS provider, data vendor | Según contrato/licencia. |

### Reglas de modelos por sensibilidad

- `public`: puede usar frontier si conviene.
- `internal`: preferir barato/local si no necesita frontier.
- `confidential`: local o frontier con aprobación.
- `pii`: redacción o local primero.
- `restricted`: humano/Data Broker decide.

---

## 8. Acciones VoxBridge

### Permitidas

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

### Prohibidas

```text
change_ncm_final
submit_customs_declaration
approve_operation
change_costs
release_goods
send_legal_instruction_without_review
delete_document
access_reserved_dna_or_vuce
```

Regla:

```text
Voz puede coordinar, consultar, pedir documentos y escalar.
Voz no decide régimen final, NCM final, liberación, filing ni instrucción legal.
```

---

## 9. Prompts operativos por agente

### CodexPadre

```text
Rol: Merge owner de OSLA Aduana V3.
Objetivo: integrar incrementos de 10 agentes sin romper contratos.
Prioridad: contratos, tests, decisiones, CI, docs, seguridad.
No implementes features grandes salvo glue/merge.
Antes de mergear, verifica ownership, tests, evidence y riesgos.
```

### ArquitectoAduana

```text
Rol: arquitecto crítico.
Objetivo: mantener Aduana como Trade Evidence Desk, no AI customs global.
Entrega: ADRs, contratos y decisiones.
Rechaza features que no terminen en caso/tarea/evidencia/decisión.
```

### DataBrokerFTP

```text
Rol: construir Data Broker + descarga masiva controlada.
Objetivo: source registry, manifest store, hash index, schema drift.
Regla: no acceder a fuentes reservadas; no evadir controles; todo run debe ser auditado.
Entrega: conector metadata-only primero, raw después, parse solo con policy.
```

### RegimenEngine

```text
Rol: motor de régimen 2026.
Objetivo: reglas versionadas para franquicia/IVA/60/general/USA/obsequio.
Entrega: tests por escenarios y explicación con evidencia.
Regla: no dar asesoramiento legal definitivo; decisión humana.
```

### DocIntel

```text
Rol: document intelligence.
Objetivo: factura, packing, certificado, BL/AWB, comprobante, emails.
Entrega: extracción con fuente/página/confianza/modelo.
Regla: documentos sensibles local/barato primero; frontier solo con policy.
```

### TradeCaseEvidence

```text
Rol: convertir outputs en caso operativo.
Objetivo: API de TradeCase, Task, EvidencePack, Timeline.
Entrega: un caso debe poder nacer, avanzar, tener tareas/evidencia y cerrarse.
```

### PuertoLight

```text
Rol: módulo portuario absorbido.
Objetivo: eventos de ETA, BL, contenedor, delay, demurrage, proof of delay.
No construir OSLA Puerto completo.
Entrega: eventos adjuntables a TradeCase.
```

### VoxBridgeGateway

```text
Rol: Voice Action Gateway.
Objetivo: recibir eventos de vendors, convertirlos a acciones canónicas, aplicar policy y dejar evidencia.
No construir STT/TTS propio.
Probar una acción permitida y una prohibida.
```

### ProductUXMobile

```text
Rol: web + mobile operativo.
Objetivo: Product Shell para casos/tareas/evidencia y app móvil para upload/estado/faltantes.
No crear dashboard decorativo.
Cada pantalla debe responder qué falta, quién actúa y con qué evidencia.
```

### MLEvalsModelOps

```text
Rol: evals y costo/calidad.
Objetivo: model routing, evals de extracción, evals de régimen, voice policy tests, costo por caso.
Regla: ML complejo solo después de baselines.
```

---

## 10. Matriz de validación

| Área | Tests mínimos |
|---|---|
| Regime Engine | 20 escenarios, snapshot de explicación. |
| Data Broker | source allowed/denied, sensitivity routing, restricted block. |
| FTP ingest | metadata-only, raw limited, hash diff, quarantine. |
| Document Intel | extracción factura/packing/certificado con confidence. |
| Evidence Pack | cada claim tiene source/evidence. |
| VoxBridge | action allowed, action denied, human escalation. |
| Puerto Light | delay/proof event adjunto a caso. |
| Web | flujo intake -> task -> evidence -> close. |
| Mobile | upload documento -> case update. |
| ModelOps | costo/modelo registrado por operación. |

---

## 11. Criterios de calidad

Un incremento está listo para merge si:

- tiene tests o validación manual documentada;
- no rompe contratos;
- no introduce secretos;
- tiene logging/audit donde corresponde;
- respeta Data Broker;
- actualiza docs si cambia comportamiento;
- deja claro qué no hace;
- no duplica verticales;
- aporta al workflow operativo.

---

## 12. Mapa de conflictos probable

| Conflicto | Agentes | Resolución |
|---|---|---|
| Contratos de `TradeCase` | Arquitecto, TradeCaseEvidence, UI | Arquitecto propone, Padre aprueba. |
| Campos de régimen | RegimenEngine, UI, Evidence | RegimenEngine owner. |
| Document schema | DocIntel, Evidence, ML | DocIntel owner; Evidence consume. |
| Policies | DataBroker, VoxBridge, ModelOps | DataBroker owner; VoxBridge ejecuta. |
| API endpoints | TradeCase, UI, Mobile | TradeCase owner; UI no inventa. |
| Estado de tarea | Evidence, VoxBridge, Mobile | Core contracts mandan. |
| Vendor SDKs | VoxBridge, Security | ADR obligatorio. |

---

## 13. Seguridad operativa

- n8n solo self-host, actualizado, detrás de VPN o red interna.
- No exponer webhooks administrativos sin autenticación/HMAC.
- No ejecutar code nodes con permisos amplios.
- Los vendors de voz envían eventos a VoxBridge, no a sistemas core.
- Cada webhook se valida por firma, tenant, action policy y rate limit.
- Los documentos privados no salen a frontier sin policy.
- Los logs no guardan secretos ni documentos completos si no corresponde.

---

## 14. Definition of Done global

```text
Un incremento está terminado cuando puede demostrarse sobre un TradeCase real o fixture:
input -> policy -> procesamiento -> tarea/evidencia -> decisión/handoff -> audit log.
```

---

## Fuentes y validaciones usadas en V3

- Archivos mergeados: V2 de roadmap/agents/product + `aduana__chatgpt_29_04_2026_v3.md` + `verticals_chatgpt_29_04_2026_v3.md` + `propuesta_cambio_licitaciones_v3.md`.
- Validación web: MEF/DNA régimen 2026, DNA FTP, Claude Opus 4.7/Claude Design, GitHub Copilot usage billing, ElevenLabs, Vapi, n8n, Docling, Airbyte, Flexport, Digicust.
