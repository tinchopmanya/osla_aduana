# PRODUCTO ADUANA V3 — OSLA Aduana Trade Evidence Desk

**Archivo:** `productoaduana_v3.md`
**Fecha de corte:** 2026-04-29
**Vertical:** `osla_aduana`
**Producto:** **OSLA Aduana — Trade Evidence Desk / Aduana Control Tower**
**Módulos absorbidos:** Puerto Light, VoxBridge, Trade Compliance Audit, Customs Entry Copilot, Supplier Risk, ComplianceOps, Licita Bridge.
**Modo:** B2B/B2B2C, API-first, mobile temprano, descarga masiva controlada, IA asistida y auditada, humano en loop.

---

## 0. Definición corta

OSLA Aduana es una control tower operativa para comercio exterior uruguayo.

Convierte:

- compras web;
- facturas;
- invoices;
- packing lists;
- certificados de origen;
- NCM/HS declarado;
- proveedor;
- país de origen/procedencia;
- courier/casillero;
- BL/AWB/contenedor;
- eventos de puerto;
- llamadas, emails o mensajes de seguimiento;
- cambios normativos;

En:

1. régimen probable;
2. riesgos e inconsistencias;
3. tareas y faltantes;
4. evidencia documental/logística/conversacional;
5. explicación al cliente o al equipo;
6. handoff a humano/despachante;
7. decisión auditada.

No es calculadora. No es chatbot. No es dashboard. No reemplaza al despachante. No presenta declaraciones automáticamente. Es el expediente vivo de la operación.

---

## 1. Tesis de producto V3

```text
Documento + dato público + evento puerto + conversación
  -> policy
  -> extracción / regla / modelo
  -> caso
  -> tarea
  -> evidencia
  -> humano
  -> cierre auditado
```

La oportunidad nace porque Uruguay cambia el régimen de envíos postales/franquicias en mayo 2026 y genera incertidumbre operativa real: IVA, topes, cupo anual, régimen simplificado, excepciones, courier responsable, registro de empresas extranjeras, transición normativa y preguntas de clientes.

La defensa no está en explicar la norma. La defensa está en:

- documentos privados autorizados;
- reglas versionadas;
- evidencia por campo;
- workflow vivo;
- integración con courier/despachante/importador;
- puerto/logística;
- voz gobernada;
- historial proveedor/NCM/origen;
- humano en loop;
- auditoría.

---

## 2. Qué hace y qué no hace

### Hace

- Evalúa régimen probable: franquicia, IVA, 60%, general, obsequio, excepción USA.
- Carga y procesa documentos.
- Detecta faltantes e inconsistencias.
- Crea casos, tareas y responsables.
- Genera Evidence Pack.
- Permite seguimiento por web, API, mobile y VoxBridge.
- Adjunta evidencia portuaria/logística si existe.
- Alimenta Licita/Bidroom cuando una oferta depende de un bien importado.
- Integra Supplier Risk cuando proveedor/origen importa.
- Registra modelo usado, costo y validación humana.

### No hace

- No reemplaza despachante.
- No decide NCM final.
- No presenta declaraciones.
- No libera mercadería.
- No accede a VUCE/DNA operativa sin permiso.
- No vende datos de importaciones ajenas como curiosidad.
- No promete reducción arancelaria.
- No deja que un vendor de voz toque sistemas críticos directamente.

---

## 3. Buyers y roles

### Buyers principales

| Buyer | Dolor | Producto inicial |
|---|---|---|
| Courier/casillero | Reclamos por IVA/franquicia, pagos, documentación, explicación al cliente. | CourierOps + Régimen 800 + Evidence Pack. |
| Despachante | Faltantes, NCM/origen/proveedor, coordinación, evidencia. | Trade Evidence Desk. |
| Importador/e-commerce | Costo final, régimen, margen, proveedor, stock. | Simulador operativo + expediente. |
| Freight forwarder | ETA, contenedor, demoras, BL, prueba de delay. | Puerto Light + case evidence. |
| Marketplace cross-border | Qué vender, desde dónde, cómo informar IVA/franquicia. | Regime API + customer explanation. |
| Proveedor del Estado/importador | Bien importado dentro de licitación. | Aduana -> AI Bidroom. |

### Roles de usuario

| Rol | Permisos |
|---|---|
| `admin_osla` | Configura fuentes, tenants, modelos, policies. |
| `data_broker` | Aprueba fuentes, sensibilidad, storage, OCR, embeddings. |
| `courier_ops` | Crea casos, revisa régimen, gestiona reclamos. |
| `despachante` | Revisa NCM/origen/documentos, cierra revisión humana. |
| `importador` | Carga documentos, consulta estado, responde faltantes. |
| `proveedor` | Sube documentos solicitados, no ve datos sensibles. |
| `forwarder` | Adjunta BL/contenedor/ETA/proof delay. |
| `atencion_cliente` | Ve explicación resumida y estado permitido. |
| `licitaciones_manager` | Consume evidencia para bid/no-bid. |
| `voice_agent_vendor` | Solo invoca acciones permitidas por VoxBridge. |
| `auditor` | Lee evidencia, timeline, decisiones y costos. |

---

## 4. Módulos de producto

### 4.1 Regime Engine

Evalúa régimen y explica por qué.

Inputs:

- país/procedencia declarada;
- residencia fiscal del emisor si aplica;
- valor;
- cantidad de franquicias usadas si el dato está autorizado/cargado;
- peso;
- tipo de producto;
- courier;
- fecha;
- si es obsequio;
- si es persona física/jurídica;
- documentos.

Outputs:

- régimen probable;
- IVA probable;
- 60% simplificado si corresponde;
- evidencia normativa;
- faltantes;
- disclaimers;
- “necesita revisión humana”.

### 4.2 Document Intelligence

Procesa documentos sin prometer decisión final.

Campos:

- proveedor;
- emisor factura;
- país;
- descripción;
- cantidad;
- unidad;
- valor;
- moneda;
- incoterm;
- NCM/HS declarado si aparece;
- peso;
- tracking;
- BL/AWB;
- certificado origen;
- medio de pago si corresponde y si hay permiso.

### 4.3 Consistency Checker

Detecta:

- factura vs packing;
- origen vs certificado;
- proveedor vs factura;
- valor vs orden;
- cantidad vs packing;
- NCM/HS declarado vs descripción;
- documento faltante;
- fecha inconsistente;
- posible caso para humano.

### 4.4 Trade Case

El caso es el centro del producto.

Incluye:

- estado;
- partes;
- documentos;
- items;
- régimen;
- señales de riesgo;
- tareas;
- evidencia;
- timeline;
- conversaciones;
- eventos puerto;
- decisión humana.

### 4.5 Evidence Pack

Exportable y auditable.

Incluye:

- fuentes usadas;
- fragmentos o hashes;
- documentos;
- campos extraídos;
- reglas aplicadas;
- modelo usado;
- costo IA;
- revisión humana;
- tareas;
- resultado;
- limitaciones.

### 4.6 Puerto Light

No es un producto separado. Aporta eventos a la operación.

Eventos:

- ETA;
- cambio ETA;
- buque;
- BL;
- contenedor;
- status cargado manual/API;
- demurrage estimate;
- proof of delay;
- hold/retención si se carga por cliente.

### 4.7 VoxBridge Trade Follow-up

Capa de acciones gobernadas desde voz/chat.

Casos:

- pedir packing list;
- consultar qué falta;
- crear tarea;
- resumir llamada;
- escalar a despachante;
- avisar a importador;
- registrar respuesta del proveedor.

No hace:

- cambiar NCM final;
- aprobar operación;
- liberar mercadería;
- presentar declaración;
- dar instrucción legal final.

### 4.8 Licita Bridge

Cuando una licitación requiere bienes importados:

```text
Bidroom detecta bien importado
  -> crea TradeCase Aduana
  -> Aduana informa riesgo/costo/plazo/documentos
  -> Bidroom incorpora evidencia
  -> humano decide bid/no-bid
```

---

## 5. Fuentes de datos

### Fuentes públicas / controladas

| Fuente | Uso |
|---|---|
| MEF régimen envíos postales | Reglas, FAQ, interpretación pública. |
| DNA Compras Web y Envíos | Normativa, consultas públicas, guías. |
| DNA FTP anónimo | Descarga masiva controlada, metadata/raw/parse según policy. |
| IMPO JSON | Normativa, decretos, resoluciones. |
| ARCE/RUPE/OCDS | Proveedores/licitaciones/relaciones con Estado. |
| Uruguay XXI/SIE | Comercio exterior agregado/contexto. |
| BCU/INE | Tipo de cambio/contexto macro. |
| ANP/AIS/comercial | Puerto Light si hay fuente permitida/licencia. |

### Fuentes privadas/autorizadas

| Fuente | Uso |
|---|---|
| Documentos cliente | Principal fuente de valor. |
| Histórico operaciones cliente | Riesgo, demoras, proveedores, documentos recurrentes. |
| Emails/llamadas | Seguimiento y evidencia si hay policy. |
| Sistemas courier/importador | API/webhook si hay convenio. |
| Credenciales shipping line | Solo si cliente autoriza. |

### Fuentes restringidas

| Fuente | Regla |
|---|---|
| DNA operativa | Solo convenio, pública aprobada o carga explícita. |
| VUCE operativa | No asumir acceso. |
| DGI/BPS privados | No usar sin base legal/cliente/convenio. |
| FTP reservado LUCIA | No acceder sin usuario/permiso. |

---

## 6. Flujos principales

### Flujo A — Courier / Régimen 800

```text
compra + factura + país + courier
  -> Regime Engine
  -> IVA/franquicia/60/general probable
  -> faltantes
  -> explicación al cliente
  -> tarea si falta documento
  -> evidence pack
```

### Flujo B — Despachante / expediente documental

```text
invoice + packing + certificado + NCM declarado
  -> Document Intel
  -> consistency checker
  -> riesgos
  -> tareas
  -> revisión despachante
  -> cierre auditado
```

### Flujo C — Importador/e-commerce

```text
producto/proveedor/origen/documentos
  -> simulación régimen/costo/riesgo
  -> impacto margen/stock si hay datos
  -> decisión importar/no importar/revisar
```

### Flujo D — Puerto / demora

```text
BL/contenedor/buque/ETA
  -> Puerto Light
  -> delay/proof/demurrage
  -> tarea o reclamo
  -> evidencia adjunta al TradeCase
```

### Flujo E — VoxBridge / faltante documental

```text
TradeCase necesita packing
  -> VoxBridge contacta/atiende
  -> crea document_request
  -> resume interacción
  -> evidencia
  -> tarea actualizada
```

### Flujo F — Licita / producto importado

```text
licitación pide equipo importado
  -> AI Bidroom detecta dependencia aduanera
  -> Aduana crea trade case
  -> costo/plazo/riesgo/evidencia
  -> decisión bid/no-bid
```

---

## 7. UX/UI

### Web Product Shell

Pantallas:

1. **Operaciones**: lista con riesgo, estado y próximo paso.
2. **Detalle Trade Case**: documentos, régimen, tareas, evidencia.
3. **Document Comparison**: factura vs packing vs certificado.
4. **Regime View**: explicación de IVA/franquicia/60/general.
5. **Evidence Pack**: exportable.
6. **Puerto Events**: BL, ETA, contenedor, delay.
7. **VoxBridge Timeline**: llamadas, summaries, acciones, handoffs.
8. **Data Broker Admin**: fuentes y políticas.
9. **Ingestion Monitor**: FTP/jobs/manifests/schema drift.
10. **ModelOps**: costo y modelo por caso.

### Mobile

Funciones:

- ver operaciones;
- recibir alerta;
- subir documento;
- responder faltante;
- aprobar/rechazar tarea;
- ver estado resumido;
- escalar a humano;
- ver explicación corta.

No mobile:

- dashboard complejo;
- mapa portuario pesado;
- NCM final;
- edición profunda de reglas.

---

## 8. API y webhooks

### REST API inicial

```text
POST /trade-cases
GET  /trade-cases/{id}
POST /trade-cases/{id}/documents
POST /trade-cases/{id}/tasks
POST /regime/evaluate
POST /evidence-packs/{id}/export
POST /voice/events
POST /actions/execute
POST /port/events
GET  /sources
POST /sources/{id}/validate-run
```

### Webhooks

```text
case.created
document.missing
document.received
regime.assessed
task.created
task.overdue
voice.action_allowed
voice.action_denied
voice.handoff
port.delay_detected
evidence.pack_ready
```

---

## 9. ML / IA

### IA útil

| Función | Valor |
|---|---|
| Document classification | Alto, M1. |
| Field extraction | Alto, M1. |
| Consistency check | Alto, M1/M2. |
| NCM suggestion | Medio, no vinculante. |
| Supplier/entity resolution | Alto, defendible. |
| Anomaly ranking | Medio/alto, requiere datos. |
| Delay prediction | Medio, requiere Puerto/histórico. |
| Call summarization | Medio/alto, con policy. |
| Task recommendation | Alto si se mantiene acotado. |
| Model routing | Core, por costo/privacidad. |

### IA que no debe decidir sola

- NCM final;
- régimen final sensible;
- aprobación operación;
- filing;
- liberación;
- respuesta legal;
- cambio de costos final.

---

## 10. Stack técnico recomendado

| Capa | Opción |
|---|---|
| Backend | FastAPI o .NET 8, decidir por repo/equipo. |
| DB | PostgreSQL + JSONB + pgvector opcional. |
| Queue | Redis/RQ/Celery o similar. |
| Object storage | MinIO/S3. |
| Frontend | Next.js/React. |
| Mobile | Expo/React Native. |
| Document AI | Docling + OCR + LLM local/frontier. |
| Ingestion | Python jobs + Airbyte/n8n controlado si aporta. |
| Policy | OPA o motor propio simple inicial. |
| Observability | Langfuse + logs app. |
| Model router | LiteLLM/Portkey o wrapper propio. |
| Voice | ElevenLabs + Vapi inicialmente. |
| AIS/Puerto | Provider comercial o fuente pública permitida. |

---

## 11. Competencia y defensa

### Competidores globales

- Flexport: customs brokerage, AI compliance audit, tariff tools, global logistics.
- Digicust: AI customs declarations, document control, tariff classification, integrations.
- Altana: supply chain intelligence/trade enforcement.
- Classification tools: HS/NCM global, tariff API.
- Freight/visibility platforms: contenedor, puerto, ETA.

### Defensa OSLA

No competir por ser “mejor AI global”. Competir por:

- Uruguay;
- régimen 2026;
- documentos reales del cliente;
- despachante/importador/courier workflow;
- Evidence Pack;
- Puerto Light;
- VoxBridge governed actions;
- Licita bridge;
- Data Broker;
- ModelOps cost/privacy;
- integración legacy/local.

---

## 12. Ofertas comerciales

### Oferta 1 — CourierOps Régimen 800

Para couriers/casilleros.

Incluye:

- régimen probable;
- evidencia;
- explicación cliente;
- tareas/faltantes;
- API/webhook;
- VoxBridge opcional.

Precio inicial: USD 300-800/mes + setup.

### Oferta 2 — Trade Evidence Desk

Para despachantes/importadores.

Incluye:

- carga documental;
- extraction;
- consistency;
- tareas;
- evidence pack;
- revisión humana.

Precio: USD 50-150 por operación o USD 500-1.500/mes.

### Oferta 3 — Aduana + Licita

Para proveedores del Estado con bienes importados.

Incluye:

- riesgo costo/plazo/importación;
- evidence pack para bid/no-bid;
- integración AI Bidroom.

Precio: por licitación o suscripción.

### Oferta 4 — Puerto Delay Evidence

Para forwarders/importadores.

Incluye:

- ETA/cambio ETA;
- contenedor/BL;
- proof of delay;
- demurrage estimate;
- evidencia para reclamo.

Precio: add-on.

---

## 13. Demo recomendada

### Demo narrativa

```text
Un courier recibe una compra desde China y otra desde EE.UU.
OSLA evalúa régimen, detecta falta de documento, crea tarea.
El importador llama para consultar estado.
VoxBridge responde lo permitido, crea document_request y escala si hay duda.
Luego aparece un delay de puerto.
Puerto Light agrega proof of delay.
El caso se cierra con Evidence Pack.
```

### Demo técnica

- 2 documentos PDF.
- 1 régimen USA <=200.
- 1 régimen China con IVA.
- 1 intento de acción prohibida por voz bloqueado.
- 1 documento subido desde mobile.
- 1 evidence pack exportado.

---

## 14. Roadmap comercial

### Semana 1-2

- Conseguir 3 conversaciones: courier/casillero, despachante, importador.
- Pedir 5 documentos reales anonimizados.
- Validar pricing por operación.

### Semana 3-4

- Demo funcional con documentos.
- Primer piloto gratis/cobrado barato.
- Validar qué duele más: régimen, documentos, reclamos o seguimiento.

### Mes 2

- 1 cliente piloto pago.
- API/webhook para courier o despachante.
- Mobile upload.

### Mes 3

- 20-50 operaciones procesadas.
- Evidence packs reales.
- Pricing ajustado.
- Decidir avance/kill.

---

## 15. Riesgos de producto

| Riesgo | Mitigación |
|---|---|
| Quedar como calculadora de IVA | Siempre caso/tarea/evidencia. |
| Quedar como chatbot | UI/API/workflow primero; voz solo canal gobernado. |
| Competir con Digicust/Flexport | Foco UY, documentos cliente, régimen local, despachante humano. |
| Falta de datos reales | Discovery y pilotos antes de ML. |
| Datos privados mal usados | Data Broker obligatorio. |
| App mobile distrae | Mobile solo upload/estado/faltantes. |
| FTP masivo riesgoso | Manifests, throttle, policy, no reservado. |
| Voice vendor lock-in | Adapters canónicos; Vapi/ElevenLabs al inicio. |

---

## 16. One-pager comercial

**OSLA Aduana ordena operaciones de comercio exterior en Uruguay.**

Cuando cambia el régimen, falta un documento, el cliente no entiende por qué paga IVA, el proveedor no responde, el contenedor se demora o una licitación depende de un producto importado, OSLA crea un expediente operativo con tareas, evidencia y responsables.

No reemplaza al despachante. No decide NCM final. No presenta declaraciones. Organiza el trabajo, reduce incertidumbre y deja evidencia.

```text
Factura + packing + proveedor + origen + NCM + courier + puerto + llamada
  -> caso
  -> tareas
  -> evidencia
  -> decisión humana
  -> auditoría
```

---

## Fuentes y validaciones usadas en V3

- Archivos mergeados: V2 de roadmap/agents/product + `aduana__chatgpt_29_04_2026_v3.md` + `verticals_chatgpt_29_04_2026_v3.md` + `propuesta_cambio_licitaciones_v3.md`.
- Validación web: MEF/DNA régimen 2026, DNA FTP, Claude Opus 4.7/Claude Design, GitHub Copilot usage billing, ElevenLabs, Vapi, n8n, Docling, Airbyte, Flexport, Digicust.
