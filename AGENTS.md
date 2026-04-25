# AGENTS.md — OslaAduana

## Identidad del proyecto

- **Nombre**: OslaAduana (Inteligencia Aduanera UY)
- **Ranking InvestigaVert**: — Score 4.7)
- **AshRise project_id**: `aduanas`
- **Puerto Postgres**: 5451
- **DB**: aduanas / user: aduanas
- **ICP primario**: Despachante de aduanas habilitado
- **ICP secundario**: Importadores/exportadores medianos (facturación >USD 500K/año)
- **Pricing target**: USD 200-500/usuario/mes
- **Estado validación**: PENDIENTE — requiere validación con despachantes

## Qué es

Plataforma de monitoreo continuo de comercio exterior que cruza DNA (datos aduaneros) + DGI (situación fiscal) + BCU (cotizaciones) + RUPE (proveedores estado) + fuentes internacionales (U.S. Census Trade API, Eurostat Comext) + GLEIF (identificación legal) + GeoNames (geocoding rutas). No es búsqueda one-shot — es sistema con memoria, alertas y scoring ML.

## Problema que resuelve

Un despachante maneja 50-200 operaciones/mes. Hoy revisa manualmente DNA, cruza con DGI, busca antecedentes del importador, calcula aranceles. Pierde 2-4 horas/día en trabajo que un sistema integrado resuelve en segundos. Además, no tiene visibilidad de competidores ni alertas de cambios regulatorios.

## Modelos ML defensibles

1. **Anomaly Detection** (Isolation Forest): predice shipments con riesgo de subfacturación. Accuracy 85-95%.
2. **Trade Flow Forecasting**: predice volúmenes por HS code + origen + temporada.
3. **Competitor Intelligence**: alerta cuando competidor importa producto nuevo.
4. **Regulatory Change Impact**: NLP sobre IMPO para detectar cambios arancelarios.

## Fuentes de datos

### Uruguay
- DNA (Dirección Nacional de Aduanas): operaciones de importación/exportación
- DGI: situación fiscal, facturación electrónica (CFE)
- BCU: cotizaciones, tipo de cambio (API SOAP)
- RUPE: registro proveedores estado
- IMPO API: legislación aduanera

### Internacionales
- U.S. Census International Trade API (Tier A)
- Eurostat Comext API (Tier A)
- GLEIF (CC0): identificación legal global
- GeoNames (CC BY 4.0): geocoding
- Natural Earth (public domain): mapas
- Wikidata (CC0): metadata entidades

## Acceso a datos compartidos (via FDW)

```sql
SELECT * FROM shared.entity WHERE ...;
SELECT * FROM shared.normativa_snapshots WHERE ...;
SELECT * FROM shared.fx_rates WHERE currency_code = 'USD';
```

## Stack técnico

- Backend: FastAPI (Python)
- Frontend: Next.js 15 + Tailwind
- DB: Postgres 16 (puerto 5451)
- ML: scikit-learn + LightGBM + MLflow
- Data pipeline: Airflow + dbt
- Storage: S3-compatible

## Reglas de boundary

1. Repo, base de datos, storage y colas propios.
2. No leer ni escribir directo en la base de otra vertical.
3. Compartir datos solo por FDW read-only desde shared-db.
4. Reusar patrones del núcleo reusable (source discovery, document extraction, identity resolution, alerts/tasks).

## Reglas para agentes

1. **No escribir en shared-db** — solo leer vía FDW
2. **DNA es fuente de verdad** para operaciones aduaneras
3. **Evidence-first**: cada alerta deja fuente, fecha, snippet y confianza
4. **Deterministic-first**: no usar LLM en hot path si existe opción determinista
5. **No afirmar riesgo sin evidencia documental**

## Variables de entorno

```
ASHRISE_BASE_URL=http://localhost:8080
ASHRISE_TOKEN=<token>
ASHRISE_PROJECT_ID=aduanas
```

## Documentación del producto

- **[docs/Producto.md](docs/Producto.md)** — Documento completo del producto: visión, ICP, propuesta de valor, fuentes de datos, modelos ML, competencia, arquitectura, roadmap y métricas. Se actualiza cuando una investigación impacta esta vertical.
- **[docs/Investigaciones.md](docs/Investigaciones.md)** — Log cronológico de investigaciones procesadas que impactan esta vertical: si fortalecen o debilitan la tesis, y qué se actualizó en Producto.md como consecuencia.
- **[docs/ROADMAP.md](docs/ROADMAP.md)** — Milestones técnicos de implementación.

## Contrato AshRise

Al iniciar sesión: leer AGENTS.md → docs/ROADMAP.md → GET /state/aduanas → GET /handoffs/aduanas?status=open
Al cerrar: emitir ashrise-close con run + state_update.
