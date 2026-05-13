---
slug: osla_aduana
entidad: vertical
estado_documento: runtime_implementation_doc
tipo_archivo: runtime
canon_path: C:\dev\osla\osla_aduana\docs\ADUANA_V3_R_OFFLINE_CONTRACTS.md
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
# Aduana V3-R Offline Contracts

Fecha: 2026-05-02
Estado: contrato documental offline. No ejecuta red, FTP, descarga, parseo, OCR, embeddings, DB, storage ni migraciones.

## 1. Veredicto

El corte tecnico seguro para `osla_aduana` es `offline_contracts_and_policy_v0`.

Este documento define contratos canonicos y fixtures sinteticos para:

- `TradeCase`
- `EvidenceItem`
- `SourceManifest`
- `RegimenEngine v0`
- `VoxBridge action policy`

No define runtime material. No habilita acceso a DNA, VUCE, LUCIA, FTP, APIs externas, DB, storage, OCR, embeddings ni decision automatica final de NCM/regimen.

## 2. Principios no negociables

- Aduana es `Trade Evidence Desk / Aduana Control Tower`.
- Todo output operativo debe terminar en caso, tarea, evidencia, decision humana o auditoria.
- `DNA` puede ser fuente canonica futura, pero en este corte no se toca ninguna fuente real.
- `PuertoLight` es modulo/evento adjuntable a `TradeCase`; no es vertical separada.
- `VoxBridge` coordina follow-up y handoff; no decide ni instruye juridicamente.
- `RegimenEngine v0` sugiere regimen probable con explicacion y disclaimer; no emite decision legal final.
- Todo fixture de este corte es sintetico y debe ser identificable como tal.

## 3. Alcance V3-R

### Incluido

- Contratos YAML/JSON-like versionados.
- Enumeraciones cerradas para estados, fuentes, sensibilidad y acciones.
- Fixtures sinteticos para pruebas futuras offline.
- Invariantes que deberian convertirse en tests unitarios cuando exista paquete ejecutable.
- Matriz P0/P1/P2.
- Siguiente corte tecnico seguro.

### Excluido

- FTP real o metadata preflight.
- Red, descargas, listado remoto o apertura de contenido.
- DB, storage, colas, migraciones o pipelines.
- OCR, embeddings, modelos ML o parsers documentales.
- Uso de datos reales de clientes, DNA, VUCE, LUCIA, DGI, BCU, IMPO o vendors.
- Decision final automatica de NCM, regimen, liberacion, filing, costos o instrucciones legales.

## 4. Versionado de contratos

```yaml
contract_pack:
  name: aduana_offline_contracts
  version: v0.1.0
  status: draft_offline
  owner: ArquitectoAduana
  consumer_candidates:
    - TradeCaseEvidence
    - DataBrokerFTP
    - RegimenEngine
    - VoxBridgeGateway
    - ProductUXMobile
  compatibility_rule: additive_changes_only_until_runtime_exists
```

Regla: cualquier cambio futuro que elimine campos, cambie semantica de estados o permita material real requiere ADR o documento de decision.

## 5. Contrato `TradeCase`

`TradeCase` es el contenedor operativo. Agrupa partes, documentos, items, faltantes, regimen probable, riesgos, tareas, evidencia, timeline y revision humana.

```yaml
TradeCase:
  schema_version: aduana.trade_case.v0
  id: string
  tenant_id: string
  created_at: datetime
  updated_at: datetime
  buyer_type: courier | despachante | importador | forwarder | marketplace | licita
  status: intake | needs_documents | ready_for_review | in_review | waiting_external | ready_for_broker | closed_ok | closed_with_risk | cancelled
  source_context:
    intake_channel: manual | client_upload | voice_event | public_dataset_fixture | synthetic_seed
    source_manifest_id: string?
    is_synthetic: boolean
  parties:
    - TradeParty
  documents:
    - TradeDocument
  items:
    - TradeItem
  missing_requirements:
    - MissingRequirement
  regime_assessment: RegimeAssessment?
  risks:
    - RiskSignal
  tasks:
    - Task
  evidence_item_ids:
    - string
  evidence_pack_id: string?
  timeline:
    - TimelineEvent
  human_reviewer_id: string?
  audit:
    created_by: string
    last_action_by: string
    policy_flags:
      - string
```

### Subcontratos

```yaml
TradeParty:
  id: string
  role: importer | exporter | despachante | forwarder | carrier | supplier | buyer | broker | unknown
  display_name: string
  country_code: string?
  tax_id_ref: string?
  sensitivity: public | internal | confidential | pii | restricted

TradeDocument:
  id: string
  document_type: commercial_invoice | packing_list | bill_of_lading | airway_bill | certificate_origin | permit | receipt | email | voice_summary | other
  status: missing | received | needs_review | accepted_for_review | rejected
  evidence_item_id: string?
  page_refs:
    - string
  sensitivity: public | internal | confidential | pii | restricted
  synthetic_note: string?

TradeItem:
  id: string
  description: string
  quantity: number?
  unit: string?
  declared_value_usd: number?
  origin_country_code: string?
  suggested_ncm: string?
  suggested_ncm_confidence: number?
  ncm_final: null
  notes:
    - string

MissingRequirement:
  id: string
  requirement_type: document | clarification | human_review | source_owner_decision | license_review
  description: string
  blocking: boolean
  owner_role: importer | despachante | broker | osla_source_owner | human_reviewer

RiskSignal:
  id: string
  risk_type: missing_document | low_confidence | restricted_source_attempt | license_unknown | regime_uncertain | sensitivity_high | policy_denied
  severity: low | medium | high | critical
  evidence_item_id: string?
  explanation: string

Task:
  id: string
  title: string
  status: open | in_progress | blocked | done | cancelled
  owner_role: importer | despachante | broker | osla_operator | human_reviewer
  due_at: datetime?
  linked_evidence_item_id: string?

TimelineEvent:
  id: string
  occurred_at: datetime
  event_type: case_created | document_requested | evidence_added | regime_assessed | voice_action | policy_denied | human_reviewed | status_changed | closed
  actor_type: system | human | voice_gateway | fixture_generator
  summary: string
  evidence_item_id: string?
```

### Invariantes

- `source_context.is_synthetic` debe ser `true` para todos los fixtures V3-R.
- `ncm_final` debe ser `null` en todos los fixtures y outputs automaticos.
- `human_reviewer_id` es obligatorio para `closed_ok` y `closed_with_risk`.
- `ready_for_broker`, `closed_ok` y `closed_with_risk` requieren al menos un `EvidenceItem`.
- Si existe `RiskSignal.risk_type = restricted_source_attempt`, el caso no puede pasar a `ready_for_broker`.

## 6. Contrato `EvidenceItem`

`EvidenceItem` es la unidad minima de auditabilidad. No contiene documento completo; contiene referencia, hash sintetico o excerpt seguro.

```yaml
EvidenceItem:
  schema_version: aduana.evidence_item.v0
  id: string
  source_id: string
  source_type: public_web | public_ftp | client_document | voice_event | manual | api | model_output | synthetic_fixture
  captured_at: datetime
  source_ref: string
  excerpt_or_hash: string
  model_used: string?
  cost_estimate_usd: number?
  confidence: number?
  human_validated: boolean
  sensitivity: public | internal | confidential | pii | restricted
  retention_policy: fixture_only | no_persist | standard | restricted_hold
  synthetic:
    is_synthetic: boolean
    generator: string?
    real_source_touched: boolean
  audit:
    created_by: string
    policy_flags:
      - string
```

### Invariantes

- `synthetic.real_source_touched` debe ser `false` en V3-R.
- `source_type = synthetic_fixture` debe usar `retention_policy = fixture_only`.
- `sensitivity = restricted` bloquea modelo frontier, OCR, embeddings y acciones automaticas.
- `excerpt_or_hash` no debe contener documentos completos ni datos personales reales.
- `model_used` y `cost_estimate_usd` deben ser `null` salvo fixtures de `model_output`.

## 7. Contrato `SourceManifest`

`SourceManifest` describe una corrida de fuente. En V3-R solo se permite manifest sintetico.

```yaml
SourceManifest:
  schema_version: aduana.source_manifest.v0
  source_id: string
  run_id: string
  run_started_at: datetime
  run_finished_at: datetime?
  mode: metadata_only | raw_download | parse | diff | synthetic_fixture
  state: planned | allowed_offline | denied_by_policy | blocked_until_prereqs_closed | completed_offline
  files_seen: number
  files_downloaded: number
  bytes_downloaded: number
  hashes_changed: number
  schema_warnings:
    - string
  quarantine_count: number
  source_policy:
    access_class: public | public_restricted | client_provided | commercial | reserved | unknown
    license_status: approved | unknown_needs_review | denied | not_applicable
    allowlist_applied: boolean
    denylist_applied: boolean
    network_allowed: boolean
    db_writes_allowed: boolean
    storage_writes_allowed: boolean
  audit:
    owner_review_required: boolean
    human_owner: string?
    notes:
      - string
```

### Invariantes

- En V3-R `mode` debe ser `synthetic_fixture`.
- Para `uy.dna.public_ftp`, `state` debe ser `blocked_until_prereqs_closed`.
- `files_downloaded` debe ser `0`.
- `bytes_downloaded` debe ser `0`.
- `source_policy.network_allowed` debe ser `false`.
- `source_policy.db_writes_allowed` debe ser `false`.
- `source_policy.storage_writes_allowed` debe ser `false`.
- `source_policy.denylist_applied` debe ser `true`.

## 8. Contrato `RegimenEngine v0`

`RegimenEngine v0` es deterministico y offline. Produce una evaluacion preliminar explicable. No decide regimen final.

```yaml
RegimeAssessment:
  schema_version: aduana.regime_assessment.v0
  assessment_id: string
  trade_case_id: string
  engine_version: regimen_engine.v0.offline
  created_at: datetime
  input_summary:
    buyer_type: string
    item_count: number
    declared_value_usd_total: number?
    origin_country_codes:
      - string
    documents_available:
      - string
  candidate_regimes:
    - CandidateRegime
  selected_probable_regime: string?
  confidence: number
  missing_inputs:
    - string
  explanation:
    - string
  disclaimer: human_review_required_no_legal_advice
  final_decision:
    ncm_final: null
    regime_final: null
    decided_by: null
```

```yaml
CandidateRegime:
  code: franquicia | iva | sesenta_por_ciento | regimen_general | courier | unknown_needs_review
  probability_label: low | medium | high
  rule_hits:
    - string
  rule_misses:
    - string
  required_evidence_item_ids:
    - string
```

### Reglas v0 permitidas

- Clasificar como `unknown_needs_review` si faltan factura, packing, valor declarado u origen.
- Sugerir `regimen_general` solo como probable cuando hay documentacion minima y no hay condicion especial modelada.
- Incluir escenarios sinteticos de `franquicia`, `iva`, `sesenta_por_ciento`, `courier` y `regimen_general` para tests futuros.
- Explicar reglas usadas en lenguaje operativo, no juridico.

### Reglas v0 prohibidas

- Escribir `regime_final`.
- Escribir `ncm_final`.
- Presentar la salida como asesoramiento legal o declaracion aduanera.
- Calcular liquidacion definitiva de tributos.
- Usar OCR, embeddings, LLM o fuentes reales para completar datos faltantes.

## 9. VoxBridge action policy v0

VoxBridge transforma eventos conversacionales en acciones auditadas sobre casos y tareas. En V3-R solo existe policy offline.

```yaml
VoiceActionEvent:
  schema_version: aduana.voice_action_event.v0
  id: string
  vendor: elevenlabs | vapi | retell | manual | synthetic_fixture
  conversation_id: string
  trade_case_id: string?
  requested_action: string
  normalized_action: string
  action_status: allowed | denied | escalated | failed
  policy_reason: string
  transcript_ref: string?
  summary: string
  created_task_id: string?
  evidence_item_id: string?
  sensitivity: public | internal | confidential | pii | restricted
  synthetic:
    is_synthetic: boolean
    real_vendor_touched: boolean
```

### Acciones permitidas

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

### Acciones prohibidas

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

### Invariantes

- Una accion prohibida debe producir `action_status = denied` o `escalated`.
- `restricted` o `pii` no puede generar envio automatico a terceros.
- Toda llamada resumida debe crear o referenciar un `EvidenceItem`.
- Ningun vendor de voz toca sistemas core sin policy gate.
- En V3-R `synthetic.real_vendor_touched` debe ser `false`.

## 10. Fixtures sinteticos minimos

### 10.1 `TradeCase` sintetico con faltantes

```yaml
schema_version: aduana.trade_case.v0
id: tc_syn_0001
tenant_id: tenant_syn_osla
created_at: "2026-05-02T12:00:00-03:00"
updated_at: "2026-05-02T12:00:00-03:00"
buyer_type: despachante
status: needs_documents
source_context:
  intake_channel: synthetic_seed
  source_manifest_id: sm_syn_0001
  is_synthetic: true
parties:
  - id: party_syn_importer
    role: importer
    display_name: Importador Sintetico SA
    country_code: UY
    tax_id_ref: rut_synthetic_redacted
    sensitivity: internal
documents:
  - id: doc_syn_invoice
    document_type: commercial_invoice
    status: missing
    evidence_item_id: null
    page_refs: []
    sensitivity: confidential
    synthetic_note: "Documento no materializado; fixture offline."
items:
  - id: item_syn_001
    description: "Repuesto industrial sintetico para prueba"
    quantity: 10
    unit: unit
    declared_value_usd: 1200
    origin_country_code: CN
    suggested_ncm: null
    suggested_ncm_confidence: null
    ncm_final: null
    notes:
      - "No usar como clasificacion real."
missing_requirements:
  - id: mr_syn_invoice
    requirement_type: document
    description: "Falta factura comercial sintetica."
    blocking: true
    owner_role: importer
regime_assessment: null
risks:
  - id: risk_syn_missing_invoice
    risk_type: missing_document
    severity: medium
    evidence_item_id: null
    explanation: "No se puede evaluar regimen probable sin factura."
tasks:
  - id: task_syn_request_invoice
    title: "Solicitar factura comercial"
    status: open
    owner_role: importer
    due_at: null
    linked_evidence_item_id: null
evidence_item_ids: []
evidence_pack_id: null
timeline:
  - id: tle_syn_created
    occurred_at: "2026-05-02T12:00:00-03:00"
    event_type: case_created
    actor_type: fixture_generator
    summary: "Caso sintetico creado para contrato offline V3-R."
    evidence_item_id: null
human_reviewer_id: null
audit:
  created_by: fixture_generator
  last_action_by: fixture_generator
  policy_flags:
    - synthetic_only
```

### 10.2 `EvidenceItem` sintetico

```yaml
schema_version: aduana.evidence_item.v0
id: ev_syn_0001
source_id: synthetic.fixture.manual
source_type: synthetic_fixture
captured_at: "2026-05-02T12:05:00-03:00"
source_ref: "fixture://aduana/v3-r/evidence/0001"
excerpt_or_hash: "sha256:synthetic-not-real-0001"
model_used: null
cost_estimate_usd: null
confidence: 1.0
human_validated: false
sensitivity: internal
retention_policy: fixture_only
synthetic:
  is_synthetic: true
  generator: aduana_v3_r_doc
  real_source_touched: false
audit:
  created_by: fixture_generator
  policy_flags:
    - no_real_content
    - no_network
```

### 10.3 `SourceManifest` sintetico para FTP bloqueado

```yaml
schema_version: aduana.source_manifest.v0
source_id: uy.dna.public_ftp
run_id: run_syn_ftp_blocked_0001
run_started_at: "2026-05-02T12:10:00-03:00"
run_finished_at: "2026-05-02T12:10:00-03:00"
mode: synthetic_fixture
state: blocked_until_prereqs_closed
files_seen: 0
files_downloaded: 0
bytes_downloaded: 0
hashes_changed: 0
schema_warnings:
  - "FTP real bloqueado; manifest sintetico sin red."
quarantine_count: 0
source_policy:
  access_class: public_restricted
  license_status: unknown_needs_review
  allowlist_applied: true
  denylist_applied: true
  network_allowed: false
  db_writes_allowed: false
  storage_writes_allowed: false
audit:
  owner_review_required: true
  human_owner: null
  notes:
    - "No habilita metadata preflight."
    - "No extrapola licencia DAG del catalogo al FTP completo."
```

### 10.4 `RegimeAssessment` sintetico

```yaml
schema_version: aduana.regime_assessment.v0
assessment_id: ra_syn_0001
trade_case_id: tc_syn_0001
engine_version: regimen_engine.v0.offline
created_at: "2026-05-02T12:15:00-03:00"
input_summary:
  buyer_type: despachante
  item_count: 1
  declared_value_usd_total: 1200
  origin_country_codes:
    - CN
  documents_available: []
candidate_regimes:
  - code: unknown_needs_review
    probability_label: high
    rule_hits:
      - missing_commercial_invoice
      - missing_supporting_documents
    rule_misses:
      - cannot_confirm_general_regime
    required_evidence_item_ids: []
selected_probable_regime: unknown_needs_review
confidence: 0.2
missing_inputs:
  - commercial_invoice
  - packing_list
  - human_broker_review
explanation:
  - "Fixture offline: faltan documentos minimos para sugerir regimen probable."
  - "La salida no decide regimen ni NCM final."
disclaimer: human_review_required_no_legal_advice
final_decision:
  ncm_final: null
  regime_final: null
  decided_by: null
```

### 10.5 `VoiceActionEvent` permitido

```yaml
schema_version: aduana.voice_action_event.v0
id: va_syn_allowed_0001
vendor: synthetic_fixture
conversation_id: conv_syn_0001
trade_case_id: tc_syn_0001
requested_action: "Pedir factura comercial al importador"
normalized_action: create_document_request
action_status: allowed
policy_reason: "Accion permitida: solicitar documento faltante y crear tarea."
transcript_ref: "fixture://aduana/v3-r/voice/allowed-0001"
summary: "Llamada sintetica solicita completar factura comercial."
created_task_id: task_syn_request_invoice
evidence_item_id: ev_syn_0001
sensitivity: internal
synthetic:
  is_synthetic: true
  real_vendor_touched: false
```

### 10.6 `VoiceActionEvent` prohibido

```yaml
schema_version: aduana.voice_action_event.v0
id: va_syn_denied_0001
vendor: synthetic_fixture
conversation_id: conv_syn_0002
trade_case_id: tc_syn_0001
requested_action: "Cambiar NCM final y aprobar la operacion"
normalized_action: change_ncm_final
action_status: denied
policy_reason: "Accion prohibida: NCM final y aprobacion operativa requieren humano."
transcript_ref: "fixture://aduana/v3-r/voice/denied-0001"
summary: "Solicitud sintetica denegada por policy."
created_task_id: null
evidence_item_id: ev_syn_0001
sensitivity: internal
synthetic:
  is_synthetic: true
  real_vendor_touched: false
```

## 11. Validaciones offline esperadas

Cuando exista `packages/core_contracts` o equivalente, los primeros tests deben cubrir:

- Fixture `TradeCase` valido con `is_synthetic = true`.
- Rechazo si `ncm_final` no es `null`.
- Rechazo si `closed_ok` no tiene `human_reviewer_id`.
- Rechazo si `EvidenceItem.synthetic.real_source_touched = true`.
- Rechazo si `SourceManifest.files_downloaded > 0` en V3-R.
- Rechazo si `SourceManifest.bytes_downloaded > 0` en V3-R.
- Rechazo si `uy.dna.public_ftp` tiene `network_allowed = true`.
- Rechazo si `SourceManifest` omite denylist.
- `RegimenEngine v0` devuelve `unknown_needs_review` cuando faltan documentos.
- `RegimenEngine v0` nunca escribe `ncm_final` ni `regime_final`.
- VoxBridge permite `create_document_request`.
- VoxBridge deniega `change_ncm_final`.
- VoxBridge deniega `access_reserved_dna_or_vuce`.
- `PuertoLight` futuro solo adjunta eventos a `TradeCase`, no crea vertical separada.

## 12. Matriz P0/P1/P2

### P0

- No existe paquete ejecutable de contratos.
- No existe validador offline que haga cumplir invariantes.
- No existe test que bloquee red, descarga, DB/storage, OCR o embeddings.
- `uy.dna.public_ftp` sigue bloqueado por licencia/terminos y owner humano.
- No hay decision humana formal para habilitar source preflight.
- No existe `RegimenEngine v0` implementado.
- No existe policy ejecutable de VoxBridge.
- No hay separacion probada de PuertoLight como modulo absorbido.

### P1

- Falta convertir estos contratos en schemas concretos.
- Falta fixture pack versionado en archivos.
- Falta matriz completa de sensibilidad por documento.
- Falta set de 20 escenarios de regimen offline.
- Falta set de acciones VoxBridge allowed/denied/escalated.
- Falta evidence pack offline con snapshots esperados.
- Docs historicos siguen conteniendo claims aspiracionales que contradicen readiness V3-Q.

### P2

- Definir layout final: `packages/core_contracts`, `packages/aduana_regime`, `packages/voxbridge_gateway`.
- Elegir stack minimo de schemas y tests.
- Definir naming de IDs, timestamps y tenancy.
- Mapear datasets DNA catalogados como candidato futuro distinto del FTP completo.
- Diseñar UI/API despues de contratos ejecutables.

## 13. Siguiente corte tecnico seguro

```text
v3-s-core-contracts-fixtures-tests-offline
```

Alcance recomendado:

- Crear `packages/core_contracts` o equivalente.
- Materializar schemas para `TradeCase`, `EvidenceItem`, `SourceManifest`, `RegimeAssessment` y `VoiceActionEvent`.
- Agregar fixtures sinteticos como archivos.
- Agregar tests unitarios sin red.
- Agregar policy guards para P0.
- Generar runlog local que confirme cero red, cero descargas, cero DB/storage, cero OCR/embeddings.

No incluir:

- FTP real.
- Metadata preflight.
- Conectores.
- Parsers.
- Migraciones.
- UI.
- Decision final automatica de NCM/regimen.
