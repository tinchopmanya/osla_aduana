---
slug: osla_aduana
entidad: vertical
estado_documento: mirror_do_not_edit_here
tipo_archivo: otro
canon_path: C:\dev\osla\osla_aduana\docs\v3_canonical\aduana__chatgpt_29_04_2026_v3.md
supersedes: []
superseded_by: null
fuente_de_verdad: C:\dev\Investigacion_Osla_consolidada\FUENTE_DE_VERDAD_VERTICALES.md
no_usar_como_fuente_de_verdad: true
updated_at: 2026-05-13T02:55:45Z
owner: CODEX_5_5
auto_generated: false
disclaimers: []
mirror_of: C:\dev\Investigacion_Osla_consolidada\NUEVOSDOCUMENTOS_29deabril\aduana__chatgpt_29_04_2026_v3.md
notas: mirror of V3 canonical import
encoding: ascii_puro
---
# aduana__chatgpt_29_04_2026_v3.md

**Fecha de corte:** 29 de abril de 2026
**Versión:** V3
**Vertical:** `osla_aduana` / Comercio exterior Uruguay
**Cambio V3:** integración de VoxBridge/Neytiri como capa de seguimiento, handoff y acción controlada para operaciones aduaneras.

---

## 0. Veredicto V3

`osla_aduana` sigue viva, pero no como “AI customs global” ni como clasificador NCM autónomo.

La versión defendible es:

```text
OSLA Aduana = Trade Evidence Desk UY
```

Y la V3 agrega:

```text
VoxBridge = canal seguro para seguimiento de operaciones, faltantes documentales, handoffs con despachante/importador y creación de tareas.
```

No significa que Aduana se vuelva una central telefónica. Significa que las llamadas/interacciones operativas dejan evidencia.

---

## 1. Producto V3

### Qué hace

Para una operación de comercio exterior:

```text
factura / packing / certificado / NCM / proveedor / origen / llamada / email
  -> extracción documental
  -> validación preliminar
  -> alerta de inconsistencia
  -> caso operativo
  -> tareas
  -> follow-up por voz/chat si aplica
  -> evidencia
  -> decisión humana
  -> historial por proveedor/NCM/origen
```

### Qué NO hace

- No reemplaza despachante.
- No clasifica NCM como verdad legal final.
- No automatiza filing aduanero.
- No usa DNA/VUCE operativa sin permiso, convenio o carga explícita.
- No vende scraping de importaciones ajenas.
- No promete reducción arancelaria.

---

## 2. Por qué VoxBridge suma en Aduana

El workflow aduanero real tiene mucho follow-up:

- falta factura;
- falta packing;
- falta certificado;
- proveedor no contestó;
- despachante necesita aclaración;
- importador pregunta estado;
- compras necesita saber costo/plazo;
- ventas necesita saber si llega para una licitación;
- contabilidad necesita documento para pago;
- un caso debe escalar a humano.

Hoy eso queda en llamadas, WhatsApp, emails o memoria humana.

VoxBridge puede transformar ese ruido en:

```text
interacción -> acción canónica -> policy -> tarea/evidencia/handoff
```

---

## 3. Arquitectura Aduana V3

```text
Documentos cliente / operación / NCM / proveedor / origen
  -> Data Broker
  -> ModelOps Router
  -> Trade Evidence Case
  -> Supplier Risk / Perfil Proveedor
  -> ComplianceOps si aplica
  -> VoxBridge para seguimiento y handoff
  -> Evidence Pack
  -> cierre auditado
```

---

## 4. VoxBridge en Aduana

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

### Acciones prohibidas al inicio

```text
change_ncm_final
submit_customs_declaration
approve_operation
change_costs
release_goods
send_legal_instruction_without_review
delete_document
```

### Casos de uso

#### Caso 1: faltante documental

```text
Trade case detecta falta de packing list
  -> VoxBridge contacta o atiende al proveedor/importador
  -> crea document_request
  -> adjunta transcript/resumen
  -> marca tarea pendiente
```

#### Caso 2: consulta de estado

```text
importador llama: “¿cómo está la operación X?”
  -> VoxBridge permite lookup
  -> responde estado resumido
  -> si hay bloqueo, escala a despachante
```

#### Caso 3: handoff a despachante

```text
voice agent detecta inconsistencia NCM/origen
  -> no decide
  -> crea caso de revisión
  -> handoff a despachante
  -> evidencia
```

#### Caso 4: operación ligada a licitación

```text
licitación requiere producto importado
  -> Aduana informa riesgo de llegada/costo/documentos
  -> Bidroom recibe alerta
  -> decisión bid/no-bid incorpora evidencia
```

---

## 5. Fuentes de datos V3

### Seguras para MVP

| Fuente | Uso |
|---|---|
| Documentos del cliente | Factura, packing, certificados, órdenes, emails. |
| NCM aportado por cliente/despachante | Campo central, no verdad final automática. |
| Proveedor/origen cargado | Perfil y riesgo. |
| IMPO JSON | Normativa pública asociada si aplica. |
| ARCE/RUPE | Si el importador/proveedor participa en licitaciones o vende al Estado. |
| BCU/INE/Uruguay XXI | Contexto macro/sectorial si se valida fuente. |
| VoxBridge events | Llamadas, handoffs, follow-ups, document requests. |

### Restringidas

| Fuente | Restricción |
|---|---|
| DNA operativa | Solo con convenio, fuente pública aprobada o carga explícita del cliente. |
| VUCE operativa | No asumir acceso. |
| DGI/BPS privados | Solo cliente/convenio/fuente pública clara. |
| Datos de terceros | No scraping dudoso. |

---

## 6. Qué verticales fortalecen Aduana

| Vertical/módulo | Aporte a Aduana |
|---|---|
| `modelops_cost_router` | Procesa documentos con menor costo y escala casos complejos. |
| `data_broker_mcp` | Controla acceso a documentos/fuentes y permisos. |
| `voice_action_gateway / VoxBridge` | Seguimiento, faltantes, estado, handoff y evidencia conversacional. |
| `supplier_risk_ops` | Perfil proveedor exterior/local, documentos, historial, alertas. |
| `complianceops_uy` | Cambios normativos/regulatorios aplicables a operación. |
| `senaclaft_evidence_desk` | Si hay debida diligencia por contraparte/operación sensible. |
| `ai_bidroom / licita` | Si la importación depende de licitación o entrega al Estado. |
| `backoffice_reconciliation_ops` | Factura/pago/orden/remito/operación. |
| `retail_margin/demanda` | Impacto de costo/importación sobre margen/stock. |
| `energy_bill/cold_chain` | Para bienes sensibles, refrigerados o con logística energética. |

---

## 7. ML/IA útil

| Función | Uso |
|---|---|
| Extracción documental | Factura, packing, certificados, emails. |
| Entity resolution | Proveedor, importador, aliases, razón social. |
| Clasificación tentativa | Tipo documental, operación, NCM sugerido no vinculante. |
| Consistency check | Documento vs NCM/origen/proveedor/cantidades. |
| Anomaly detection | Costos, cantidades, proveedor recurrente, lead time. |
| Model routing | Local/barato/frontier según sensibilidad/riesgo. |
| Call summarization | Resumen de llamadas con importador/despachante/proveedor. |
| Task recommendation | Faltantes y próximos pasos. |

---

## 8. Competencia y amenaza

### Amenaza global

Alta si Aduana intenta competir con:

- Flexport AI customs;
- HS classification global;
- tariff optimization;
- customs filing automation;
- trade compliance enterprise.

### Amenaza ChatGPT/Claude

Alta para:

- leer documentos;
- resumir reglas;
- sugerir NCM;
- armar checklist.

Menor para:

- expediente vivo;
- documentos privados;
- workflow;
- human-in-loop;
- handoff;
- evidencia;
- integración con licitaciones/proveedores/backoffice.

### Amenaza VoxBridge/voice platforms

Los vendors de voz ya tienen tools, transfers, tests y PII redaction. Por eso Aduana no debe construir voz propia. Debe usar VoxBridge solo para acciones controladas del expediente.

---

## 9. MVP Aduana V3

### Duración

30 a 45 días si hay documentos reales.

### Qué entra

- 5 operaciones reales;
- carga documental;
- extracción de campos;
- caso operativo;
- tareas/faltantes;
- evidence pack;
- Supplier Risk básico;
- VoxBridge mini para consulta de estado y document request;
- handoff a despachante/humano.

### Qué no entra

- DNA/VUCE integración;
- clasificación NCM definitiva;
- filing aduanero;
- 10 vendors de voz;
- automatización de decisión final.

### Criterio de éxito

- 5 operaciones procesadas;
- al menos 10 faltantes/tareas detectados;
- un despachante/importador valida que el expediente ahorra tiempo;
- un follow-up por voz/chat queda útil como evidencia.

---

## 10. Pricing inicial

| Oferta | Precio tentativo |
|---|---:|
| Auditoría documental por operación | USD 50-150 |
| Pack 10 operaciones | USD 400-1.000 |
| Suscripción importador chico | USD 99-299/mes |
| Suscripción importador mediano | USD 300-800/mes |
| Setup VoxBridge follow-up | USD 500-2.000 |

---

## 11. Roadmap de agentes paralelos para Aduana V3

```text
1 Padre/Merge Owner
1 Data Broker/document policy
1 Document extractor
1 ModelOps router
1 Trade Case backend
1 Evidence Pack
1 Supplier Risk integration
1 Licita integration
1 VoxBridge adapter
1 VoxBridge policy/audit
1 UI Claude Design
1 QA/evals
1 Auditor crítico
2 conectores/document samples
```

---

## 12. Decisión V3 Aduana

Aduana se modifica con VoxBridge.

No porque voz sea el producto, sino porque el proceso aduanero tiene mucha coordinación por fuera del sistema.

Frase V3:

> **OSLA Aduana V3 convierte documentos y conversaciones de comercio exterior en casos operativos auditables, con tareas, evidencia, handoff y revisión humana.**

---

## Fuentes consultadas / contexto verificable

- OpenAI Workspace Agents: https://openai.com/index/introducing-workspace-agents-in-chatgpt/
- OpenAI GPT-5.5: https://openai.com/index/introducing-gpt-5-5/
- Anthropic Claude Opus 4.7: https://www.anthropic.com/news/claude-opus-4-7
- GitHub Copilot premium requests / billing: https://docs.github.com/en/billing/concepts/product-billing/github-copilot-premium-requests
- Microsoft Agent 365: https://www.microsoft.com/en/microsoft-agent-365
- Gemma 4: https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/
- DeepSeek V4 / Reuters: https://www.reuters.com/world/china/deepseek-v4-chinese-ai-model-adapted-huawei-chips-2026-04-24/
- Avoca AI $125M+ / $1B valuation: https://www.prnewswire.com/news-releases/avoca-raises-125m-at-1b-valuation-to-power-americas-services-economy-with-ai-302753962.html
- ElevenLabs transfer to human: https://elevenlabs.io/docs/conversational-ai/customization/tools/system-tools/transfer-to-human
- ElevenLabs tools/webhooks: https://help.elevenlabs.io/hc/en-us/articles/34669011018257-How-to-use-tools-with-Conversational-AI
- Vapi Test Suites / Voice Testing: https://docs.vapi.ai/test/test-suites/ y https://docs.vapi.ai/test/voice-testing
- Retell pricing/security features: https://www.retellai.com/pricing
- Retell PII redaction changelog: https://www.retellai.com/changelog
- VoiceAIWrapper multi-provider/white-label voice AI: https://voiceaiwrapper.com/
- VoiceAIWrapper HIPAA/healthcare agency use case: https://voiceaiwrapper.com/uses/hipaa-compliant-voice-ai-white-label
- ARCE datos abiertos / RUPE / OCDS: https://www.gub.uy/agencia-reguladora-compras-estatales/datos-y-estadisticas/datos-abiertos
- IMPO datos abiertos JSON: https://www.impo.com.uy/datos-abiertos/
- URSEA datos abiertos: https://www.gub.uy/unidad-reguladora-servicios-energia-agua/datos-y-estadisticas/datos-abiertos
