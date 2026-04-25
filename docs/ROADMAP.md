# ROADMAP — OslaAduana (Inteligencia Aduanera UY)

## Estado actual

MVP operativo con ingesta DNA + DGI + BCU. Scoring básico de operaciones aduaneras. Necesita ML defensibles y product surfaces.

---

## Roadmap integrado

### Fase 1 — MVP + Scoring (semanas 1-8)

**Entidades canónicas:**
- Importador (RUT DGI)
- Operación aduanal (DNA)
- Producto (HS code)
- Proveedor (RUPE)
- Normativa (IMPO)

**Milestones:**
- **M1:** Pipeline DNA → DB (operaciones aduaneras raw)
- **M2:** Crossing DNA + DGI (estado fiscal importador)
- **M3:** BCU integration (cotizaciones, aranceles calculados)
- **M4:** Scoring determinístico (subfacturación, riesgo, anomalías)
- **M5:** Dashboard B2B despachantes (tender explorer)
- **M6:** Alert engine (cambios regulatorios IMPO, nuevos competidores)
- **M7:** Product surface `/product/` (responsive mobile)
- **M8:** Testing + documentation (8 weeks, 50+ test cases)

**ML Pipeline:**
1. Feature engineering: volumen/valor/origen/HS code histórico
2. Anomaly detection model (Isolation Forest): 85-95% accuracy
3. Trade flow forecast (ARIMA baseline → Prophet ensamble)
4. MLflow integration + model serving

**Validation criteria:**
- DNA sync latency <24h
- Scoring latency <200ms/operación
- Anomaly detection recall >90% (false negatives minimized)
- Dashboard usability (SUS >70)

---

### Fase 2 — Predicción y Network (semanas 8-16)

**Milestones:**
- **M9:** Competitor Intelligence (alerta cuando competidor importa nuevo producto)
- **M10:** Regulatory Change Impact (NLP IMPO → scoring impacto arancelario)
- **M11:** Supplier Network Risk (si proveedor cae, quién se ve afectado)
- **M12:** API product (/api/v1/trade/*)

**ML enhancements:**
- Trade flow forecasting (Prophet con seasonality UY)
- LightGBM supplier risk scoring
- GNN network propagation (opcional)

**Validation criteria:**
- Trade forecast RMSE <15%
- Competitor intelligence recall >95%
- API latency <500ms

---

### Fase 3 — Enterprise + Integración (semanas 16-24)

**Milestones:**
- **M13:** Multi-workspace + RBAC (workspace_id, roles, headers)
- **M14:** Advanced auth (OAuth2 + SSO)
- **M15:** Notificaciones (email + webhook)
- **M16:** Bulk export (Excel + API)

**Validation criteria:**
- Auth latency <100ms
- 99.9% uptime SLA
- <100ms export latency

---

### Fase 4 — Escala internacional (meses 6+)

**Milestones:**
- **M17:** Paraguay integration (DNA local)
- **M18:** Global Comext (Eurostat API)
- **M19:** Multilingual UI (ES + EN + PT)
- **M20:** Mobile app (React Native)

---

## Stack especificación

**Backend:**
```
FastAPI + Pydantic + SQLAlchemy 2
Postgres 16 + PostGIS (si se agrega análisis geoespacial)
Airflow para ETL
```

**Frontend:**
```
Next.js 15 + TypeScript
Tailwind CSS
Recharts + Plotly para visualización
```

**ML:**
```
scikit-learn (Isolation Forest, baseline)
LightGBM (clasificación)
Prophet (series temporales)
PyTorch (opcional para DL futuros)
MLflow para versionamiento
```

**Data sources:**
```
DNA API (contacto directo, auth token)
DGI API (si existe)
BCU SOAP (existente)
IMPO REST API
U.S. Census (REST)
Eurostat (REST)
```

---

## Métricas de éxito

| Métrica | Actual | Target M8 | Target M16 |
|---------|--------|-----------|------------|
| Operaciones procesadas | 0 | 50K+ | 500K+ |
| Importadores perfilados | 0 | 5K | 50K |
| DNA latency | N/A | <24h | <6h |
| Anomaly detection accuracy | N/A | 85% | 92% |
| Dashboard MAU | 0 | 20 | 200 |
| MRR | $0 | $300 | $5K |

---

## Dependencies externas

- **DNA:** contacto directo requerido (ADUANAS)
- **DGI:** API access (si público) o acuerdo datos
- **IMPO:** API libre pero requiere parsing robusto
- **U.S. Census Trade API:** requiere API key

---

## Riesgos y mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|--------|-----------|
| DNA API indisponible | Media | Alto | Cached sync, fallback data |
| DGI datos incompletos | Media | Medio | Validación + warnings a usuario |
| Regulación IMPO cambia frecuente | Alta | Medio | Scoring tolerante a cambios |
| Competencia regional | Media | Medio | Defensible por UY data advantage |

---

## Presupuesto estimado (MVP)

| Línea | Costo | Duración |
|-------|-------|----------|
| Ingeniería (3 FTE) | $45K | 6 meses |
| Cloud infra (AWS) | $2K/mes | ongoing |
| Datos (APIs) | $500/mes | ongoing |
| Testing + QA | $5K | 2 meses |
| **Total MVP** | **~$95K** | **6 meses** |

---

## Hitos clave

- **Week 4:** M1-M2 completados, datos DNA fluyendo
- **Week 8:** M4-M5, scoring funcional, dashboard MVP
- **Week 12:** M6-M7, alertas activas, product launch
- **Week 16:** Fase 2 comienza, ML enhancements
