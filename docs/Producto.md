# Producto — OslaAduana

> Nota 2026-05-10: este documento es legacy hasta su reconciliacion completa
> con `docs/v3_canonical/`. Si contradice el pack V3, gana el pack V3. No usar
> este archivo para reintroducir dashboard, scoring legal final, NCM final,
> filing automatico ni reemplazo del despachante.

> Última actualización: 2026-04-24
> Estado: PENDIENTE validación con despachantes

## Índice
1. [Visión del Producto](#1-visión-del-producto)
2. [Problema que Resuelve](#2-problema-que-resuelve)
3. [Cliente Ideal (ICP)](#3-cliente-ideal-icp)
4. [Propuesta de Valor](#4-propuesta-de-valor)
5. [Fuentes de Datos](#5-fuentes-de-datos)
6. [Modelos ML Defensibles](#6-modelos-ml-defensibles)
7. [Competencia y Diferenciación](#7-competencia-y-diferenciación)
8. [Arquitectura Técnica](#8-arquitectura-técnica)
9. [Roadmap Resumido](#9-roadmap-resumido)
10. [Métricas de Éxito](#10-métricas-de-éxito)
11. [Riesgos y Mitigaciones](#11-riesgos-y-mitigaciones)
12. [Referencias de Investigación](#12-referencias-de-investigación)

---

## 1. Visión del Producto

**OslaAduana** es la plataforma de inteligencia aduanera #1 en Uruguay (Score 4.7 en ranking interno) que transforma el trabajo manual de despachantes de aduanas en un sistema de monitoreo continuo, predictivo e integrado.

No es una herramienta de búsqueda one-shot. Es un **sistema con memoria**, que cruza múltiples fuentes de datos en tiempo real, genera alertas inteligentes, calcula riesgos mediante modelos ML y entrega insights competitivos que hoy los despachantes encuentran de forma fragmentada y tardía.

La visión es convertir el comercio exterior uruguayo en un ecosistema transparente, eficiente y predecible, donde las decisiones se toman sobre datos, no sobre intuición.

---

## 2. Problema que Resuelve

### El flujo actual (manual y fragmentado)

Un despachante habilitado maneja **50-200 operaciones mensuales**. Hoy el workflow es:

1. **Revisión manual de DNA** (Dirección Nacional de Aduanas): datos crudos de importación/exportación sin contexto
2. **Validación cruzada con DGI** (Dirección General Impositiva): corroborar situación fiscal del importador
3. **Búsqueda de antecedentes**: Google, redes, bases de datos desactualizadas
4. **Cálculo manual de aranceles**: códigos HS, tasas IMPO, excepciones
5. **Alertas perdidas**: cambios regulatorios, nuevos competidores, subdeclaraciones

### Costo en tiempo

- **2-4 horas/día** perdidas en tareas que un sistema integrado resuelve en **segundos**
- Sin visibilidad de competidores: el despachante no sabe si su cliente importa un producto que antes no importaba
- Sin alertas de cambios arancelarios: se entera cuando ya afectó la operación
- Sin detección de subfacturación: riesgo regulatorio silencioso

### Impacto en el negocio

- **Despachantes**: operaciones lentas, clientes insatisfechos, imposibilidad de crecer sin triplicar staff
- **Importadores/exportadores**: no acceden a datos de competencia, pierden oportunidades, no pueden optimizar costos
- **DNA/Estado**: capacidad limitada para detectar fraude y anomalías

---

## 3. Cliente Ideal (ICP)

### ICP Primario: Despachante de Aduanas Habilitado

- **Rango**: 5-30 empleados en la operación
- **Volumen**: 50-200 operaciones mensuales
- **Presupuesto disponible**: USD 200-500/usuario/mes (soportado por margen operativo)
- **Problema más agudo**: pérdida de tiempo en verificaciones manuales y búsqueda de información
- **Ganancia buscada**: cerrar operaciones 10x más rápido, reducir errores regulatorios

### ICP Secundario: Importadores/Exportadores medianos

- **Rango de facturación**: > USD 500K/año
- **Necesidad**: visibilidad de competencia, predicción de aranceles, optimización de rutas comerciales
- **Presupuesto**: USD 300-800/mes por inteligencia de mercado
- **Acceso**: vía dashboard de consulta (modelo B2B2C a través del despachante)

### Personas clave

1. **Operador de aduanas** (despachante): usuario diario, valida la plataforma
2. **Gerente administrativo** (despachante): comprador, decide ROI
3. **Importador/exportador** (cliente final): usuario secundario, genera datos de contexto

---

## 4. Propuesta de Valor

### Para Despachantes

| Beneficio | Métrica |
|-----------|---------|
| **Ahorro de tiempo** | 2-4 horas/día → operaciones en segundos |
| **Reducción de errores** | Anomaly detection ML detecta subfacturaciones no obvias |
| **Escalabilidad** | Misma operación con 3x más volumen sin hiring |
| **Diferenciación competitiva** | Único con visibilidad de competencia en tiempo real |
| **Conformidad regulatoria** | Alertas automáticas de cambios IMPO e irregularidades |

### Para Importadores/Exportadores

| Beneficio | Métrica |
|-----------|---------|
| **Inteligencia de mercado** | Saben qué importan competidores, cuándo, de dónde |
| **Predicción de costos** | Modelos ML estiman aranceles 85%+ accurados |
| **Optimización de rutas** | Identifican alternativas de proveedores / puertos más baratos |
| **Alertas comerciales** | Notificados de cambios arancelarios antes que la competencia |

### Propuesta de Valor Expandida — Estrategia Multi-Cluster

**Anti-LLM Score & Buyer Validation (Vendor gap 5.0, Fortaleza IA 5.0, Buyer pain 5.0, WTP 4.5)** — Sigue siendo la mejor combinación de moat local, buyer real y entrada comercial. Wedge: perfil 360 importador/exportador cruzando DNA+UruguayXXI+RUPE+DGI+ARCE+IMPO+sanciones.

**OslaAduana como núcleo de DNA ecosystem:**

- **Cluster "Comercio Exterior"** (Customs + Company + Port + AgroExport): USD 700/mes bundle
  - Cross-sell Aduana → Puerto: 60% de los clientes (navieros, agencieros)
  - Cross-sell Aduana → Company: 45% de los clientes (importadores medianos)
  - DNA es "Rosetta Stone": un cliente paga una vez por DNA integrado, accede a 4 verticals

**Diferenciador clave**

**Integración nativa + ML enfocado en anomalías aduaneras**: nadie más cruza DNA + RUPE + ARCE + DGI + BCU + fuentes internacionales + modelos específicos de fraude/riesgo aduanero en Uruguay.

---


La investigación Ola 004 confirma que la base para Customs Intelligence es defendible: Census+Eurostat+UN/LOCODE+WPI+SMDG+BIC. El ranking final (019) ubica Customs en #2 con 90 puntos — el monitoreo continuo de operaciones aduaneras con datos locales UY es altamente resiliente a frontier AI.
## 5. Fuentes de Datos

### Fuentes Locales (Uruguay) — Tier A (acceso garantizado)

| Fuente | Formato | Cobertura | Calidad | Uso |
|--------|---------|-----------|---------|-----|
| **DNA** (Dirección Nacional de Aduanas) | API REST pública | Todas las operaciones aduaneras UY | 5/5 | Core: cruces, análisis |
| **RUPE** (Registro Único de Personas) | CSV mensual | Personas físicas / jurídicas | 4/5 | Verificación de identidad |
| **ARCE** (Admin. Compras Estatales) | API OCDS tiempo real | Licitaciones públicas | 4/5 | Contexto empresarial |
| **VUCE** (Ventanilla Única) | Requiere credenciales | Documentos aduanales | 5/5 | Validación operaciones |
| **DGI** (Dirección General Impositiva) | API SOAP / consulta lookup | Registros fiscales, RUT | 4/5 | Validación de operadores |
| **BCU** (Banco Central Uruguay) | API SOAP | Cotizaciones USD/UYU | 4/5 | Cálculos de aranceles |
| **IMPO** (Instituto Mexicano del Petróleo) | API pública | Cambios arancelarios, códigos HS | 4/5 | Alertas de cambios |

**Viabilidad general: 5/5** — Todas las fuentes core son públicas (DNA, RUPE, ARCE) o bajo costo (VUCE con credenciales institucionales).

### Fuentes Internacionales — Tier A (acceso abierto o bajo costo)

Tier A Global Sources Added (040-043):
- **U.S. Census Trade Statistics** (REST API): Import/export data monthly by HS6, country, value, weight, transport mode. Open data desde 2024.
- **PatentsView** (CC BY 4.0): Patent data para análisis de innovación de importadores.
- **Copernicus Sentinel** (CC comercial): Imágenes multiespectrales para análisis de puertos/logistics.

### Fuentes Internacionales — Tier A (acceso abierto o bajo costo)

| Fuente | Formato | Cobertura | Uso |
|--------|---------|-----------|-----|
| **U.S. Census Trade API** | REST JSON | Importaciones/exportaciones USA | Benchmarking de volúmenes HS code |
| **Eurostat Comext** | API REST | Comercio intra-EU | Inteligencia de mercado europeo |
| **GLEIF** | API REST (CC0) | Registro global de entidades | Validación de empresas importadoras |
| **GeoNames** | API REST (CC BY 4.0) | Información geográfica de puertos | Geocodificación, rutas comerciales |
| **Natural Earth** | Descarga (Public Domain) | Datos geográficos de fronteras | Mapas de rutas comerciales |
| **Wikidata** | API SPARQL (CC0) | Información de productos, empresas | Enriquecimiento contextual |

### Fuentes NO usadas (restricciones)

- **UN Comtrade**: Términos restrictivos para uso comercial. Excluido del stack inicial.

---


### Fuentes Internacionales — Investigaciones 004-019

| Fuente | Cobertura | Licencia | Investigación |
|--------|-----------|----------|--------|
| **GLEIF (CC0)** | Matching de importadores/exportadores globales | CC0 | Ola 004 |
| **OFAC Sanctions + World Bank debarred** | Compliance screening de contrapartes | Público | Ola 004 |
| **U.S. Census trade data** | Port data mensual por HS6, país, valor, peso, modo transporte, con API | Gratis (desde 2024) | Ola 004 |
| **Eurostat Comext** | APIs gratuitas, reuse comercial con atribución | CC BY (con restricciones) | Ola 004 |
| **SMDG Terminal Codes** | Child codes de UN/LOCODE para terminales de contenedores | Fair use | Ola 004 |
| **BIC Facility Codes** | Depots/yards container-side | Fair use | Ola 004 |
| **World Bank LPI** | Benchmark logístico por país | Público | Ola 004 |
### APIs UY documentadas (036+038)

**DNA Aduanas portal** (REST, 48h delay): descarga de operaciones aduanales.

**DGI RUT Verification** (REST JSON, real-time): verificación de estado tributario de importadores/exportadores.

**DGI CFE WebServices** (SOAP/REST, e-factura): consulta de comprobantes fiscales emitidos.

**BCU Cotizaciones** (SOAP XML, diario): cotizaciones de moneda extranjera.

**catalogodatos.gub.uy**: 2,673+ datasets públicos UY disponibles para reutilización.

### Internacionales (036+038)

**UN Comtrade API v2**: Trade data global por país, HS code, flujo (import/export).

**WTO Tariff Data API** (apiportal.wto.org): tarifas arancelarias por país y acuerdo comercial.

**WITS (World Bank)**: trade statistics integrado, tariffs, preferential access.

**ComexStat Brasil** (API+paquete R comexr): datos de importación/exportación Brasil, libre acceso.

### ALERTA CRÍTICA (036+038)

**Muchas APIs UY no documentadas públicamente** — requiere ingeniería directa (reverse-engineering de VUCE, DNA portal, DGI endpoints). Viabilidad sigue siendo 4-5/5 pero requiere negociación formal con AGESIC/DNA desde mes 1.


## 6. Modelos ML Defensibles

### 6.1 Anomaly Detection — Subfacturación (Isolation Forest)

**Objetivo**: Detectar operaciones importadoras subdeclaradas (fraude aduanero).

**Entrada**: 
- Precio unitario declarado (USD/kg)
- Código HS del producto
- País de origen
- Volumen
- Histórico de importador

**Modelo**: Isolation Forest (scikit-learn)
- Entrenamiento: 12 meses de DNA
- Features: desviación de precio respecto a histograma del HS code, ratio volumen/valor atípico, patrón temporal

**Métricas**:
- Precision: 85-95% (pocos falsos positivos, confía DNA)
- Recall: 70-80% (detecta la mayoría de casos reales)

**Output**: Score 0-100 (riesgo), alertas en dashboard

---

### 6.2 Trade Flow Forecasting — Pronóstico de Volúmenes (Prophet)

**Objetivo**: Predecir volúmenes futuros de importación/exportación por HS code.

**Entrada**:
- Series temporales de volúmenes de DNA (diarios/semanales)
- Estacionalidad comercial (ej: rubros agrícolas)
- Cambios arancelarios IMPO
- Datos económicos (BCU: tasas, tipo de cambio)

**Modelo**: Facebook Prophet
- Descomposición de tendencia + estacionalidad
- Intervalos de confianza 80/95%

**Métricas**:
- MAPE (Mean Absolute Percentage Error): < 15% en 90 días
- Detecta cambios de tendencia 2-4 semanas antes que competencia

**Output**: Gráficos interactivos, alertas si "caída anómala" detectable

---

### 6.3 Competitor Intelligence — Monitoreo de Importadores (Rule Engine + Clustering)

**Objetivo**: Alertar a despachantes/importadores si sus competidores importan productos nuevos.

**Entrada**:
- DNA filtrado por importador X
- Historial de códigos HS importados
- Nuevas operaciones del período

**Modelo**: 
- Rule-based (si importador Y nunca importó HS code Z, genera alerta)
- K-means clustering de perfiles de importación (tipos de producto)

**Métricas**:
- Cobertura: 100% de cambios de patrón de importación
- Lead time: 1-2 días vs. competencia (que descubre manualmente)

**Output**: Notificaciones push, reporte en dashboard

---

### 6.4 Regulatory Change Impact — Alertas de Cambios Arancelarios (NLP + Rule Engine)

**Objetivo**: Detectar cambios en tasas IMPO y predecir impacto en operaciones.

**Entrada**:
- Feeds de IMPO (cambios arancelarios)
- Registro de cambios históricos
- Texto de resoluciones (PDF/HTML)

**Modelo**:
- NLP (regex + keyword matching, luego transformers si escala)
- Linking: HS code afectado + tarifa vieja/nueva
- Cálculo de impacto: (tarifa_nueva - tarifa_vieja) * volumen_mensual

**Métricas**:
- Recall en detección de cambios: 100% (crítico)
- Tiempo de propagación a cliente: < 4 horas vs. semana promedio

**Output**: Alertas críticas, simulations "¿cuánto cuesta si sube 5%?"

---

## 7. Competencia y Diferenciación

### Benchmark Internacional — Score Interno 4.8 (#1 en InvestigaVert ranking)

**Competidor Principal Local:**
- **SmartDATA** (UY): Plataforma legacy sin AI. Riesgo 3/5, capacidad IA 1/5. Warehouse histórico de DUAs/NCM; consultas sectoriales; benchmark por NCM. **Debilidad crítica: solo tiene comex, no cruza otras fuentes locales**. No integra DGI, RUPE, ARCE, sanciones. Score competitivo: 3.2 vs nuestro 4.8.
- **Grupo EPP/Track&Trace**: Operativo sin IA (riesgo 2/5, IA 1/5). Trazabilidad básica post-importación.
- **MAP/Softcargo**: Legacy LATAM, no moat local.
- **Terminales portuarias**: Datos fragmentados, no integrados.

**Landscape Global:**
- **ImportGenius** (USA): Base de bills of lading con predicción de importación. Costo: **USD 1,499/mes** solo para acceso a datos, sin ML avanzado.
- **Panjiva/S&P Global**: Cobertura global trade, pero enterprise-only (>USD 5K/mes). No optimizada para LATAM ni MIPYMES.
- **Descartes Datamyne**: Logística + customs, enterprise-only.
- **Kpler**: Especializada en commodity trading (petróleo, grano). Enterprise-only.

**Hallazgo clave:** 19/21 verticals aduanales globales NO tienen competitor nativo competitivo en LATAM. Uruguay está bajo-atendido.

**Datos-platforms dominan top 5 internacionalmente** (Eurostat, UN Comtrade, Trade Lens), pero ninguno integra ML + DNA + DGI + RUPE + ARCE de forma nativa.

### Diferenciadores clave

1. **Integración única DNA + RUPE + ARCE + DGI + IMPO**: La combinación es **10x más valiosa que ImportGenius** (que solo ofrece bills of lading).
2. **ML específico de fraude aduanero**: Isolation Forest en subfacturación es defensible.
3. **Alertas en tiempo real**: cambios regulatorios, competencia, anomalías.
4. **Dashboard intuitivo**: convertir crudo de DNA en decisiones visuales.
5. **Soporte a múltiples ICP**: despachantes + importadores (vs. solo uno).
6. **DNA es "Rosetta Stone" para 4 verticals**: DNA DNA+RUPE+ARCE sirve también OslaCompany, OslaPuerto, OslaAgroExport.

6. **DNA es "Rosetta Stone" para 4 verticals**: DNA DNA+RUPE+ARCE sirve también OslaCompany, OslaPuerto, OslaAgroExport.

### Competidores globales primer mundo (032+034)

**Webb Fontaine Zerø** (WCO 2026): Plataforma de customs cloud-native con LLMs integrados en cada capa aduanali (ingestion, classification, risk, release). Operando en 100+ países. Amenaza: arquitectura superior pero mercado enterprise.

**Digicust** (Austria, €2.3M pre-Series A dic 2025): 500K+ declaraciones procesadas, 99% accuracy en classification HS. Amenaza directa en LATAM si entra. Ventaja: densidad de datos EU, no entienden workflows UY.

**Export Genius** (USA, lanzó AI Smart Search abr 2026): Amenaza directa pero limitada a datos públicos (bills of lading públicos, UN Comtrade). No integra datos gubernamentales locales como DNA+DGI.

**CommodityAI** (YC W26): Enfocado en traders de commodities (granos, petróleo), no en despacho de aduanas. Diferente mercado.

**Brasil LATAM leader**: ComexStat + PUCOMEX son estándares; MDIC + SECEX controlan datos. Oportunidad de replicar arquitectura UY a Argentina (mayor mercado) antes que competencia regional.

Conclusión: **Ventana de 12-18 meses para consolidar posición en UY antes que Webb Fontaine o Digicust entren LATAM.**

---

## 8. Arquitectura Técnica

### Stack

```
Frontend:        Next.js 15 (React, TypeScript, Tailwind)
Backend:         FastAPI (Python async)
Data Pipeline:   Airflow, dbt, MLflow
ML:              scikit-learn, LightGBM, Prophet
Database:        PostgreSQL 16
Infrastructure:  Docker, deployment TBD (AWS/Azure/local)
```

### Componentes principales

```
┌─────────────────────────────────────────┐
│        Frontend (Next.js 15)             │
│  Dashboard • Alertas • Reports • Settings│
└────────────────┬────────────────────────┘
                 │ REST API (JSON)
┌────────────────▼────────────────────────┐
│      Backend (FastAPI)                   │
│  Auth • CRUD • Jobs • WebSocket alerts   │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┼────────────────┐
    │            │                │
    ▼            ▼                ▼
 ┌─────┐    ┌─────────┐      ┌──────────┐
 │ DB  │    │ ML Svc  │      │Scheduler │
 │ PG  │    │(MLflow) │      │(Airflow) │
 └─────┘    └─────────┘      └──────────┘
    │            │                │
    └────────────┼────────────────┘
                 │
    ┌────────────┼────────────────┐
    │            │                │
    ▼            ▼                ▼
┌────────┐ ┌──────────┐  ┌──────────┐
│  DNA   │ │   DGI    │  │   BCU    │
│  API   │ │   API    │  │   API    │
└────────┘ └──────────┘  └──────────┘

Plus: U.S. Census, Eurostat, GLEIF, GeoNames
```

### Data Flow

1. **Ingestion** (Airflow): 
   - DNA: descarga diaria (06:00 UTC)
   - DGI: queries batch (08:00 UTC)
   - BCU: cotizaciones cada 30 min
   - IMPO: scrape cambios arancelarios diarios
   - Internacionales: semanal/mensual

2. **Processing** (dbt):
   - Normalización de esquemas
   - Cálculos derivados (aranceles, anomalías)
   - Staging → Production

3. **ML Training** (MLflow):
   - Isolation Forest: semanal
   - Prophet: diario (nuevos datos)
   - Competitor clustering: mensual

4. **Real-time Scoring** (FastAPI):
   - Scoring de nuevas operaciones: < 500ms
   - WebSocket para alertas push

---

## 9. Roadmap Resumido

### Fase 1: MVP (Meses 1-6) — ~USD 95K

**Objetivo**: Validar ICP primario (despachantes), product-market fit.

**Hitos**:
- M1-2: Setup infraestructura, APIs DNA/DGI/BCU conectadas
- M2-3: Dashboard básico + CRUD de operaciones
- M3-4: ML primera versión (Anomaly Detection v0.1)
- M4-5: Alpha testing con 3-5 despachantes
- M5-6: MVP launch, métricas baseline (50K ops/mes, 85% anomaly detection)

**Deliverables**:
- Dashboard funcional (Next.js)
- API FastAPI con autenticación
- Pipeline Airflow básico
- Modelos ML en MLflow
- Database schema production

---

### Fase 2: Expansión (Meses 7-12) — ~USD 150K

**Objetivo**: Escalar a 10+ despachantes, mejorar ML, agregar ICP secundario.

**Hitos**:
- M7-8: Forecasting model (Prophet) v1.0
- M8-9: Competitor intelligence engine
- M9-10: Dashboard para importadores (ICP secundario)
- M10-11: Regulatory alerts NLP
- M11-12: Optimizaciones de performance, hardening

**Métricas target**:
- 20 despachantes activos
- 200K operaciones procesadas/mes
- MRR $300
- Dashboard MAU: 50+

---

### Fase 3: Internacionalización (Meses 13+)

- Réplica de modelo en Argentina (más grande que UY)
- Integración Mercosur (Brasil, Paraguay)
- Expansion a clientes B2B2C (trading companies)

---

## 10. Métricas de Éxito

### SAM & Market Sizing (Year 1)

**Target Addressable Market:**
- **Despachantes habilitados:** 150 (conversión esperada 2-5%) = 3-8 clientes
- **Importadores grandes:** 350 (conversión 3-5%) = 10-18 clientes
- **Traders:** 750 (conversión 1-2%) = 8-15 clientes
- **Meta clientes Year 1:** 27 (escenario base)

**Revenue Model:**
- **ARPU:** USD 250/mes por despachante
- **ARR Year 1 realista:** USD 60K (27 clientes × USD 250/mes = USD 81K proyectado, conservador USD 60K)
- **Year 2:** ARR USD 200K (80 clientes, ARPU USD 250/mes)
- **Year 3:** ARR USD 400K (160 clientes, ARPU USD 250/mes)

**Capital & Burn:**
- **Burn rate:** USD 18K/mes (4 personas: 1 CTO, 1 data eng, 1 BDR, 1 ops)
- **Burn anual:** USD 216K
- **Break-even:** Year 2 (revenue USD 200K vs burn USD 250K anticipated)
- **Profitability:** Year 3+ (revenue USD 400K, margin >40%)

**Strategic Funding Plan:**
- **Seed Round:** USD 1M (18 meses runway)
- **Series A:** USD 5M (Year 2, upon validating ARR USD 200K+)

**Tiempo-a-Revenue:** 3-4 meses (primeras operaciones pagadas)

**Strategic Expansion Plan:**
- **Year 1:** Customs Uruguay (meta USD 1.2M ARR con 5+ clientes enterprise)
- **Year 2:** Customs Argentina + Company (meta USD 3M ARR regional)
- **Year 3:** AgroExport (meta USD 6M ARR, cluster Trade integrado)

### Métricas de Producto

| Métrica | Target M8 | Target M12 | Indicador |
|---------|-----------|-----------|-----------|
| **Ticket promedio** | USD 200/mes | USD 200/mes | Revenue por cliente |
| **Ciclo de venta** | 60 días | 60 días | Pipeline |
| **Mercado saturado** | 2/5 | 2/5 | Oportunidad |
| **Defensibilidad datos** | 5/5 | 5/5 | Moat |

 | 50K/mes | 200K/mes | Demanda de mercado |
| **Anomaly Detection Precision** | 85% | 90% | Calidad ML |
| **Dashboard MAU** | 20 | 50 | Adoption |
| **Alerts triggered** | 500/mes | 2K/mes | Valor entregado |
| **Tiempo promedio operación** | 2h → 10min | 2h → 5min | Eficiencia |

### Métricas de Negocio

| Métrica | Target M8 | Target M12 | Indicador |
|---------|-----------|-----------|-----------|
| **MRR** | USD 3K | USD 15K | Revenue |
| **Despachantes activos** | 5-10 | 15-20 | Market penetration |
| **Churn** | < 5% | < 3% | Retention |
| **NPS** | > 50 | > 70 | Satisfacción |
| **COGS % revenue** | 30% | 25% | Eficiencia operativa |

### Métricas Técnicas

| Métrica | Target |
|---------|--------|
| **API latency (p95)** | < 500ms |
| **Dashboard load time (p95)** | < 2s |
| **Data freshness (DNA)** | < 24h |
| **Uptime** | 99.5% |
| **DB query latency (p95)** | < 200ms |

---

## 11. Riesgos y Mitigaciones

### Riesgo 1: Acceso a datos DNA restringido

**Riesgo**: DNA rechaza integración o pone límites de rate-limiting.

**Probabilidad**: Media (tramite burocrático)

**Impacto**: MVP no viable (sin datos core)

**Mitigación**:
- Solicitar acceso formal (vía AGESIC) desde mes 1
- Plan B: vender via despachantes (acceso indirecto vía ellos)
- Plan C: agregar peso de fuentes internacionales

---

### Riesgo 2: Modelo ML no detecta casos reales

**Riesgo**: Isolation Forest tiene falsos negativos altos; despachantes no confían.

**Probabilidad**: Baja-Media (necesita tuning)

**Impacto**: Retención baja, reputación

**Mitigación**:
- Validación temprana con 3-5 despachantes (M3)
- Métricas híbridas (reglas + ML) en MVP
- Feedback loop: etiquetado manual de casos (month 4+)

---

### Riesgo 3: Competencia imita modelo

**Riesgo**: Otro actor integra DNA + DGI + ML.

**Probabilidad**: Baja (hay barrera técnica + relacional)

**Impacto**: Diferenciador erosionado

**Mitigación**:
- Enfocarse en UX/experiencia (switching cost)
- Integrar cuanto antes (first mover advantage)
- Data network effect: más operaciones → mejor ML

---

### Riesgo 4: Cambios regulatorios (IMPO, DNA)

**Riesgo**: DNA cambia formato de datos o IMPO restricciones de acceso.


### Alertas de Investigaciones 004-019

**ALERTA UN Comtrade:** Prohíbe copia, automated downloading, redistribución y explotación comercial sin permiso previo por escrito (Ola 004).

**ALERTA FRED:** No usar para pricing/ML (Ola 002).

**Ranking final (019):** Customs #2 con 90 puntos en resiliencia a frontier AI. Monitoreo continuo + classification layer + fuentes locales UY (DNA, VUCE) = moat sólido.

---



### Riesgo 5: Defensibilidad vs IA (032)

**Riesgo**: IA genérica (Claude, GPT, Gemini) con datos públicos (Comtrade, Eurostat, bills of lading públicos) cubre ~40% de la funcionalidad.

**Probabilidad**: Alta (AI frontiers avanzan)

**Impacto**: Margen de precios presionado

**Mitigación**:
- **Moat no es el reporte sino el sistema local**: IA genérica NO tiene acceso a DNA (datos gubernamentales UY), DGI (tributario), VUCE (documentos aduanales), ATRAS (historial de aduanas).
- **60% funcionalidad requiere datos integrados locales**: Detección de anomalías, scoring de importadores, alertas de cambios regulatorios, compliance UY-specific.
- **No existen GPTs especializados en aduanas UY**: Webb Fontaine, Digicust, Export Genius no tienen integración DNA+DGI+VUCE como nosotros.
- **Scoring de defensibilidad: 4/5 MUY DEFENDIBLE** (032): monitoreo continuo + entity resolution local + modelos ML específicos aduanales = resiliente a frontier AI.


## 12. Referencias de Investigación

Investigaciones codex implementadas:
- Ola 004: Trade data sources, UN Comtrade restrictions, Census API
- Ola 019: Ranking final de verticales
- Ola 011: GovTech/Public Sector AI

---

## ACTUALIZACIONES INVESTIGACIONES 020-031

### 4. Propuesta de Valor — APPEND

Investigaciones 020-031 confirman Customs como vertical #1 de entrada. La IA mata lo one-shot pero no reemplaza ingesta recurrente, entity resolution local, monitoreo persistente, auditabilidad ni workflow. El moat está en el sistema local de datos y workflow, no en el reporte. Overlay sobre flujo existente del despachante: alertas, benchmark, scoring por actor/NCM/régimen, timeline unificada. No reemplazar sistema central del despachante sino complementarlo. Uruguay-first en venta, Mercosur-first en arquitectura.

### 3. Cliente Ideal (ICP) — APPEND

Buyer validado (026): despachantes, responsables de operaciones, gerentes logística/comex, owners y CFOs en pymes y medianas. Dolor diario y caro. VUCE 2024: 239 procesos, 653.814 líneas, ahorro privado >USD 114M. Ciclo de venta estimado: 45-75 días.

### 7. Competencia y Diferenciación — APPEND

Gigantes globales (023): Altana Serie C USD 200M (jul 2024, valuación USD 1B, FedRAMP High feb 2026), Sayari inversión USD 228M (ene 2024, 10.6B+ registros, 250+ jurisdicciones), Descartes USD 729M revenue FY2026, project44 cash flow positivo y +48% new ARR. Lo ocupado es enterprise/global. Lo abierto es capa local UY. COMEX AI (UY, 2026): UYU 399/consulta, Pro UYU 4.990/mes — WTP visible por AI-native comex uruguayo.

### 9. Roadmap Resumido — APPEND

Secuencia confirmada: Customs→Company→Agro. Primer salto geográfico: Paraguay (NCM/Mercosur, DNIT integra RUC). Sprint comercial inmediato: 10-15 conversaciones, 5 demos, 2 pilotos pagos en 30 días. Core portable por WCO Data Model 4.2.0 y NCM/Sistema Armonizado.

### 10. Métricas de Éxito — APPEND

Sizing (029): núcleo exportador UY ~960 empresas. Modelo base 24-36 meses: ~70 cuentas × USD 250/mes = USD 210K ARR. Uruguay solo no alcanza para mejor outcome — expansión regional temprana necesaria.

### 8. Arquitectura Técnica — APPEND

Gap global vs local (024): core portable (WCO Data Model 4.2.0, NCM/Sistema Armonizado en Mercosur). Edge local: workflows del despachante, organismos intervinientes, puertos, zonas francas, excepciones regulatorias. Diseñar Mercosur-first en arquitectura desde día 1.

### 11. Riesgos y Mitigaciones — APPEND

- IA agéntica 2026 (025): ChatGPT deep research + MCP, Claude Research 5-45 min, Gemini Deep Research Max. Resuelven bien research ad hoc, due diligence preliminar y narrativa. NO reemplazan: ingesta recurrente de fuentes locales rotas, entity resolution, monitoreo persistente, auditabilidad, workflow. Customs mejora posición relativa vs verticales textuales.
