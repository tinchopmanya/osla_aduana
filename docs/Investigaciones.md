---
slug: osla_aduana
entidad: vertical
estado_documento: legacy_do_not_use_as_truth
tipo_archivo: otro
canon_path: C:\dev\osla\osla_aduana\docs\Investigaciones.md
supersedes: []
superseded_by: C:\dev\Investigacion_Osla_consolidada\OK\verticales\osla_aduana\product.md
fuente_de_verdad: C:\dev\Investigacion_Osla_consolidada\FUENTE_DE_VERDAD_VERTICALES.md
no_usar_como_fuente_de_verdad: true
updated_at: 2026-05-13T02:55:45Z
owner: CODEX_5_5
auto_generated: false
disclaimers: []
mirror_of: null
notas: satellite product/roadmap/agents legacy pointer
encoding: ascii_puro
---
# Investigaciones — OslaAduana

> Log cronológico de investigaciones que impactan esta vertical.
> Cada entrada documenta: fuente, fecha, impacto (fortalece/debilita), y qué se actualizó en Producto.md.

---

<!-- FORMATO DE ENTRADA:

## [YYYY-MM-DD] — Título de la investigación
- **Archivo fuente**: `docs_obsoletosinvestigacion_codex/nombre.md` o `docs_obsoletosinvestigacion_claude/nombre.md`
- **Impacto**: FORTALECE | DEBILITA | NEUTRO
- **Resumen del impacto**: Qué dice la investigación y cómo afecta a OslaAduana
- **Cambios en Producto.md**: Qué secciones se actualizaron y por qué

-->

## [2026-04-22] — Competidores UY
- **Archivo fuente**: `docs_obsoletosinvestigacion_codex/001_CompetidoresUY.md`
- **Impacto**: FORTALECE
- **Resumen del impacto**: SmartDATA es competidor legacy sin IA. Data-platforms dominan top 5. Score 4.5 (#1 ranking) confirma liderazgo de OSLA.
- **Cambios en Producto.md**: Competencia

---

## [2026-04-22] — Benchmark Internacional
- **Archivo fuente**: `docs_obsoletosinvestigacion_codex/002_BenchmarkInternacional.md`
- **Impacto**: FORTALECE
- **Resumen del impacto**: ImportGenius cobra $1499/mes solo por BL. Cruce DNA+RUPE+ARCE+DGI+IMPO vale 10x más. 19/21 verticales sin competidor LATAM nativo. Moat absoluto.
- **Cambios en Producto.md**: Competencia, Propuesta de Valor

---

## [2026-04-22] — Riesgos Regulatorios
- **Archivo fuente**: `docs_obsoletosinvestigacion_codex/003_RiesgosRegulatorios.md`
- **Impacto**: FORTALECE
- **Resumen del impacto**: Riesgo regulatorio 1.25 (VERDE). DNA+RUPE+ARCE son datos públicos. Decreto 54/2017 respalda uso comercial.
- **Cambios en Producto.md**: Riesgos

---

## [2026-04-23] — Fuentes de Datos
- **Archivo fuente**: `docs_obsoletosinvestigacion_codex/004_FuentesDeDatos.md`
- **Impacto**: FORTALECE
- **Resumen del impacto**: DNA API REST pública 5/5 calidad. RUPE CSV mensual 4/5. ARCE API OCDS tiempo real 4/5. Viabilidad 5/5.
- **Cambios en Producto.md**: Fuentes de Datos

---

## [2026-04-24] — Sinergias Entre Verticales
- **Archivo fuente**: `docs_obsoletosinvestigacion_codex/005_SinergiasEntreVerticales.md`
- **Impacto**: FORTALECE
- **Resumen del impacto**: DNA es "Rosetta Stone" para 4 verticales. Cluster Trade (Customs+Company+Port+AgroExport). Bundle "Comercio Exterior" USD 700/mes. Cross-sell Customs→Company 45%.
- **Cambios en Producto.md**: Propuesta de Valor, Roadmap

---

## [2026-04-23] — Fuentes Globales Gratis y Con Permiso (Ola 001)
- **Archivo fuente**: `docs_obsoletosinvestigacion_codex/006_FuentesGlobalesGratisYConPermiso_Ola001.md`
- **Impacto**: FORTALECE
- **Resumen del impacto**: GLEIF (CC0) como columna vertebral para identidad legal global de importadores/exportadores. Wikidata (CC0) para linking semántico entre empresas, jurisdicciones y sectores. GeoNames para normalización de orígenes/destinos. Stack GLEIF+GeoNames+Wikidata+Natural Earth directamente útil para company matching en customs intelligence, compliance y deduplicación de actores comerciales.
- **Cambios en Producto.md**: Fuentes de Datos

---

## [2026-04-23] — Fuentes Globales Por Vertical (Ola 003)
- **Archivo fuente**: `docs_obsoletosinvestigacion_codex/008_FuentesGlobalesPorVertical_Ola003.md`
- **Impacto**: FORTALECE
- **Resumen del impacto**: Para Customs Intelligence el bloque más fuerte es OFAC+World Bank debarred firms+Companies House+SEC EDGAR para compliance screening de contrapartes. TED+USAspending para procurement intelligence cruzada con trade. World Bank LPI para benchmark logístico por país. Precios deben apoyarse en owners primarios (BLS, Eurostat, FAOSTAT, CFTC), no en FRED.
- **Cambios en Producto.md**: Fuentes de Datos, Riesgos

---

## [2026-04-23] — AIS, Puertos, Terminales y Feeds de Comercio (Ola 004)
- **Archivo fuente**: `docs_obsoletosinvestigacion_codex/009_AISPuertosTerminalesFeedsComercio_Ola004.md`
- **Impacto**: FORTALECE
- **Resumen del impacto**: U.S. Census trade data ahora gratis (antes suscripción) — port data mensual por HS6, país, valor, peso y modo de transporte, con API. Eurostat Comext con APIs gratuitas y reuse comercial con atribución. ALERTA: UN Comtrade prohíbe copia, automated downloading, redistribución y explotación comercial sin permiso previo por escrito. SMDG Terminal Codes y BIC Facility Codes útiles para normalización de terminales en manifiestos.
- **Cambios en Producto.md**: Fuentes de Datos, Riesgos

---

## [2026-04-23] — Verticales Públicas UY — Ranking Final
- **Archivo fuente**: `docs_obsoletosinvestigacion_codex/019_VerticalesPublicasUYFinal.md`
- **Impacto**: FORTALECE
- **Resumen del impacto**: Customs Intelligence rankeada #2 con 90 puntos sobre 100 en resiliencia a IA frontier. Criterio: monitoreo continuo + classification layer + fuentes locales UY (DNA, VUCE, manifiestos). Frontier AI no reemplaza monitoring/compliance/scoring porque requiere datos locales, actualización continua y workflow regulatorio específico. Verticales tipo monitoring > one-shot.
- **Cambios en Producto.md**: Propuesta de Valor, Riesgos

---

## [2026-04-23] — Amenaza IA Actualizada + Defensibilidad Real Frente a IA Agéntica
- **Archivo fuente**: `docs_obsoletosinvestigacion_codex/020_AmenazaIAActualizada.md` + `docs_obsoletosinvestigacion_codex/025_DefensibilidadRealFrenteAIAAgentica.md`
- **Impacto**: FORTALECE
- **Resumen del impacto**: Customs Intelligence sale como la vertical MÁS defendible frente a IA. La IA mata lo one-shot (research, memos, comparativas) pero no reemplaza: ingesta recurrente de fuentes locales rotas, entity resolution local, monitoreo persistente, auditabilidad ni workflow real. Customs mejora su posición relativa porque su moat está en el sistema local de datos y workflow, no en el reporte. Matriz 025: "muy defendible si baja al flujo real".
- **Cambios en Producto.md**: Propuesta de Valor, Riesgos

---

## [2026-04-23] — Niche vs Broad + Timing + Gigantes Ocultos
- **Archivo fuente**: `docs_obsoletosinvestigacion_codex/021_NicheVsBroadYSecuenciaDeExpansion.md` + `docs_obsoletosinvestigacion_codex/022_TimingYSaturacionComercial.md` + `docs_obsoletosinvestigacion_codex/023_GigantesOcultosYFunding.md`
- **Impacto**: FORTALECE
- **Resumen del impacto**: Customs confirmada como mejor punta de lanza. Niche first con data hub compartido. Secuencia: Customs→Company→Agro. Timing 2026: categoría viva globalmente (project44, FourKites, Descartes empujan AI+compliance). Gigantes: Altana Serie C USD 200M (jul 2024, valuación USD 1B), Sayari inversión USD 228M (ene 2024), Descartes USD 729M revenue FY2026, project44 cash flow positivo. Lo ocupado es enterprise/global. Lo abierto es la capa local con datos UY, workflow de operador y trazabilidad aterrizada.
- **Cambios en Producto.md**: Competencia, Propuesta de Valor, Roadmap

---

## [2026-04-23] — Gap Global vs Gap Local
- **Archivo fuente**: `docs_obsoletosinvestigacion_codex/024_GapGlobalVsGapLocal.md`
- **Impacto**: FORTALECE
- **Resumen del impacto**: Customs tiene core portable (WCO Data Model 4.2.0, NCM/Sistema Armonizado en MERCOSUR), pero edge local (workflows del despachante, organismos intervinientes, puertos, zonas francas). Veredicto: Uruguay-first en venta, Mercosur-first en arquitectura. Paraguay como mejor primer salto geográfico (comparte NCM/Mercosur, DNIT integra RUC con actores aduaneros).
- **Cambios en Producto.md**: Roadmap, Arquitectura

---

## [2026-04-23] — Buyer Real, Pain Real y WTP + Competencia Real
- **Archivo fuente**: `docs_obsoletosinvestigacion_codex/026_BuyerRealPainRealYWTP.md` + `docs_obsoletosinvestigacion_codex/027_CompetenciaRealEIngresoAgilAbril2026.md`
- **Impacto**: FORTALECE
- **Resumen del impacto**: Buyer clarísimo: despachantes, gerentes logística/comex, owners/CFOs pymes. Dolor diario y caro. VUCE 2024: 239 procesos, 653.814 líneas, ahorro privado acumulado >USD 114M. ANP recoge reclamos de exportadores sobre costos portuarios, almacenaje y demoras. Entrada correcta: no reemplazar sistema central del despachante, sino overlay de alertas, benchmark, scoring por actor/NCM/régimen, timeline unificada. Ciclo de venta estimado: 45-75 días.
- **Cambios en Producto.md**: ICP, Propuesta de Valor, Métricas

---

## [2026-04-23] — Sizing, Unit Economics y Validación de Mercado
- **Archivo fuente**: `docs_obsoletosinvestigacion_codex/029_SizingYUnitEconomics.md` + `docs_obsoletosinvestigacion_codex/030_ValidacionRapidaConMercadoReal.md`
- **Impacto**: FORTALECE
- **Resumen del impacto**: Núcleo exportador UY: ~960 empresas (787 mipymes = 82% de exportadoras, Uruguay XXI 2024). Modelo base 24-36 meses: ~70 cuentas × USD 250/mes = USD 210K ARR. COMEX AI ya existe en UY: UYU 399/consulta, Pro UYU 4.990/mes → WTP visible por software AI-native de comex uruguayo. Uruguay solo no alcanza para mejor outcome — expansión regional temprana necesaria. Sprint comercial: 10-15 conversaciones, 5 demos, 2 pilotos pagos en 30 días.
- **Cambios en Producto.md**: Métricas, Competencia, Roadmap

---

## [2026-04-23] — Amenaza IA Full + Soluciones Primer Mundo + Gap LATAM
- **Archivo fuente**: `docs_obsoletosinvestigacion_codex/032_AmenazaIA2026_Full.md` + `docs_obsoletosinvestigacion_codex/034_SolucionesPrimerMundo2026.md` + `docs_obsoletosinvestigacion_codex/035_GapLATAMvsUY.md`
- **Impacto**: FORTALECE
- **Resumen del impacto**: Defensibilidad Customs: 4/5 (MUY DEFENDIBLE). IA genérica cubre ~40% de funcionalidad; falta 60% que requiere datos gubernamentales integrados (DUA, SIRA). No hay GPTs especializados en aduanas UY en OpenAI GPT Store. Competidores concretos: Export Genius lanzó "AI Smart Search" (abr 2026) para trade global — amenaza directa pero limitada a datos públicos. CommodityAI (YC W26) para commodity traders. Webb Fontaine Zerø (WCO 2026, 100+ países, LLMs en cada capa aduanal). Digicust (Austria, €2.3M, 500K+ declaraciones, 99% accuracy). Brasil lidera LATAM con ComexStat y PUCOMEX. LATAM B2B SaaS +28% YoY.
- **Cambios en Producto.md**: Competencia, Fuentes de Datos, Riesgos

---

## [2026-04-23] — Fuentes de Datos Internacionales + Ultra Profunda + Tabla Referencia
- **Archivo fuente**: `docs_obsoletosinvestigacion_codex/033_FuentesDatosInternacionales.md` + `docs_obsoletosinvestigacion_codex/036_FuentesDatosUltraProfunda.md` + `docs_obsoletosinvestigacion_codex/038_TablaReferenciaFuentesDatos.md`
- **Impacto**: FORTALECE
- **Resumen del impacto**: Catálogo de 150+ fuentes con URLs y APIs documentadas. APIs UY clave: DNA Aduanas portal (REST, 48h delay), DGI RUT Verification (REST JSON, real-time), DGI CFE WebServices (SOAP/REST, e-factura), BCU Cotizaciones (SOAP XML, diario). Internacionales: UN Comtrade API v2, WTO Tariff Data API, WITS (World Bank), ComexStat Brasil (API+paquete R). catalogodatos.gub.uy tiene 2,673+ datasets. ALERTA: muchas APIs UY no están públicamente documentadas — requiere ingeniería directa o contacto institucional.
- **Cambios en Producto.md**: Fuentes de Datos, Arquitectura

## [2026-04-23] — Ranking final anti-LLM de verticales y scoring competitivo estructurado

**Archivos fuente:** `040_VerticalesPublicasUYFinal_v2.md`, `041_ResumenTotalVerticales.md`, `043_InvestigacionVerticales21x7.json`
**Impacto:** FORTALECE
**Resumen del impacto:** Customs Intelligence confirma score final **4.8/5** (#1 de 21 verticales) en ranking que pondera defensa anti-IA, vendor gap, buyer pain, WTP y competencia adversa. El JSON estructurado con 147 competidores revela scoring detallado: buyer=5, WTP=5, mercado saturado=2, defensibilidad por datos=5, ticket estimado USD 200/mes, ciclo de venta 60 días. Competidores mapeados: SmartDATA (CIU) con riesgo 3/5 pero IA 1/5 (legacy), Grupo EPP operativo sin IA, MAP/Softcargo, terminales portuarias. Wedge recomendado: perfil 360 del importador/exportador cruzando DNA+Uruguay XXI+RUPE+DGI+ARCE+IMPO+sanciones con alertas y benchmarking competitivo preoperacional. La síntesis de 17 olas confirma que Customs nunca bajó de #1 porque cada ola la reforzó por caminos distintos.
**Cambios en Producto.md:** Competencia (#7), Propuesta de Valor (#4), ICP (#3), Métricas (#10)

## [2026-04-23] — Fuentes globales gratuitas con permiso comercial (documento original completo)

**Archivo fuente:** `042_FuentesGlobalesGratisOriginal.md`
**Impacto:** FORTALECE
**Resumen del impacto:** Documento original de 17KB con clasificación Tier A/B de fuentes globales gratuitas con permiso comercial verificado. Para Customs: Copernicus Sentinel (CC, uso comercial permitido), U.S. Census Bureau open data (trade statistics, scoring comercial), PatentsView (CC BY 4.0, scouting tecnológico), OpenAlex (CC0, research intelligence). Las fuentes Tier A tienen permisos muy limpios (CC0, CC BY 4.0, dominio público). Este archivo es la fuente original de la Ola 001 pero con el doble de detalle incluyendo URLs exactas, condiciones de licencia y potencial de aplicación por vertical.
**Cambios en Producto.md:** Fuentes de Datos (#5)

## [2026-04-23] — Cálculos de viabilidad numérica, matriz de riesgo regulatorio y fuentes de datos profundas UY

**Archivos fuente:** `048_MatrizRiesgoRegulatorio.md`, `051_Ola4FuentesDatosProfundas.md`, `055_AnalisisNicheVsBroad_Full.md`, `056_CalculoViabilidadNumerico.md`
**Impacto:** FORTALECE
**Resumen del impacto:** Cálculos numéricos detallan SAM Customs Year 1: 150 despachantes (conversión 2-5%), 350 importadores grandes (conversión 3-5%), 750 traders (conversión 1-2%) = 27 clientes meta, ARPU USD 250/mes, ARR realista USD 60K. Burn rate: USD 18K/mes (4 personas) = USD 216K/año. Break-even Year 2 (revenue USD 200K vs burn USD 250K). Year 3: profit USD 100K+ (revenue USD 400K). Plan estratégico: Customs UY Year 1 ($1.2M ARR meta), expansión AR + Company Year 2 ($3M ARR), Agro Year 3 ($6M ARR). Capital requerido: seed USD 1M, Series A USD 5M Year 2. Matriz regulatoria: Customs en zona "Alto Potencial + Riesgo Moderado" — el riesgo viene de regulación aduanera, no de datos. Fuentes profundas: DGI e-Factura (SOAP Web Service), BCU API Cotizaciones (SOAP), catalogodatos.gub.uy como hub central.
**Cambios en Producto.md:** Métricas (#10), Roadmap (#9), Fuentes de Datos (#5)

## [2026-04-25] — Resumen Total Olas 001-013 (Consolidación)

- **Archivo fuente:** `docs_obsoletosinvestigacion_codex/062_ResumenTotalOlas001a013.md`
- **Impacto:** NEUTRO
- **Resumen del impacto:** Documento de referencia que consolida las 13 olas de investigación previas en un único archivo de 95KB. No aporta información nueva sino que unifica los hallazgos ya propagados individualmente (scoring anti-LLM, fuentes de datos, competencia, viabilidad numérica, riesgo regulatorio, niche vs broad). Útil como índice maestro de toda la investigación realizada.
- **Cambios en Producto.md:** Ninguno (contenido ya propagado en batches anteriores).

## [2026-04-25] — Referencia cruzada: ML Colusión en Licitaciones

- **Archivo fuente:** `docs_obsoletosinvestigacion_codex/063_FortalecerRoadmapLicitaciones.md`
- **Impacto:** NEUTRO
- **Resumen del impacto:** El modelo GNN de colusión para osla_licita usa datos de ARCE y DGI que son compartidos con osla_aduana vía FDW. El patrón de detección de anomalías (LSTM Autoencoder) podría replicarse para detección de subfacturación en comercio exterior. Referencia técnica para posible reutilización de modelos.
- **Cambios en Producto.md:** Ninguno directo. Nota para consideración futura en sección #6 (Modelos ML).
