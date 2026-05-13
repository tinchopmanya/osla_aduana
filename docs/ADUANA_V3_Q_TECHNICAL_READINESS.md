---
slug: osla_aduana
entidad: vertical
estado_documento: research_candidate
tipo_archivo: otro
canon_path: C:\dev\osla\osla_aduana\docs\ADUANA_V3_Q_TECHNICAL_READINESS.md
supersedes: []
superseded_by: null
fuente_de_verdad: C:\dev\Investigacion_Osla_consolidada\FUENTE_DE_VERDAD_VERTICALES.md
no_usar_como_fuente_de_verdad: true
updated_at: 2026-05-13T02:55:45Z
owner: CODEX_5_5
auto_generated: false
disclaimers: []
mirror_of: null
notas: unclassified satellite markdown
encoding: ascii_puro
---
# Aduana V3-Q Technical Readiness

Fecha: 2026-05-02
Estado: readiness tecnico documental. No ejecuta red, FTP, descarga, OCR, embeddings, DB ni storage.

## 1. Veredicto ejecutivo

`osla_aduana` no esta listo para un primer corte tecnico con ejecucion real. Esta listo para un corte cero de contratos, fixtures, policy gates y tests offline.

El repo observado contiene documentacion (`AGENTS.md`, `docs/Producto.md`, `docs/Investigaciones.md`, `docs/ROADMAP.md`) pero no contiene paquetes, apps, schemas ejecutables, tests, conectores, storage, OCR, embeddings ni pipelines. Por lo tanto, cualquier afirmacion previa de "producto operativo", "DNA fluyendo" o "DB conectada" queda tratada como roadmap/historia no verificable dentro de este repo.

La fuente canonica V3 redefine Aduana como:

```text
Trade Evidence Desk / Aduana Control Tower
```

Cadena obligatoria:

```text
documento / dato publico / evento puerto / llamada / carga cliente
  -> TradeCase
  -> faltantes
  -> regimen probable
  -> NCM sugerido
  -> tareas
  -> evidencia
  -> decision humana / handoff
  -> auditoria
```

## 2. Estado por componente

| Componente | Estado real en repo | Estado V3 canonico | Readiness |
|---|---|---|---|
| TradeCase | No implementado. No hay schema ni API. | Documentado como contrato canonico. | Bloqueado hasta crear contrato versionado y tests offline. |
| EvidenceItem | No implementado. | Documentado como contrato canonico. | Bloqueado hasta schema, fixture y reglas de sensibilidad. |
| SourceManifest | No implementado. | Documentado como contrato canonico. | Bloqueado hasta manifest offline y ledger sin DB. |
| Data Broker FTP | No implementado. | Objetivo V3, pero FTP real esta bloqueado por V3-P. | P0 blocked: allowlist ejecutable vacia, licencia FTP completa unknown. |
| RegimenEngine | No implementado. | Obligatorio para regimen probable, no final juridico. | Aspiracional hasta reglas versionadas y fixtures. |
| DocIntel | No implementado. | Obligatorio para extraccion documental con evidencia. | Aspiracional; no OCR, no embeddings, no modelos hasta policy. |
| PuertoLight | No implementado. | Absorbido como eventos adjuntables a TradeCase. | Aspiracional; no vertical separada. |
| VoxBridge follow-up | No implementado. | Follow-up, faltantes, handoff y estados; no voz generica. | Aspiracional hasta policy offline allowed/denied. |
| Product/UI/API | No implementado. | Debe servir caso/tarea/evidencia. | Fuera de readiness V3-Q salvo contratos base. |

## 3. Implementado, documentado, aspiracional

### Implementado observable

- Repo Git inicial con `AGENTS.md`.
- Carpeta `docs/`.
- Documentacion historica de producto, investigaciones y roadmap.
- No hay evidencia local de backend, frontend, paquetes, pipelines, DB, tests, CI, OCR, embeddings o conectores.

### Documentado canonico V3

- Nombre producto: `Trade Evidence Desk / Aduana Control Tower`.
- Contratos conceptuales: `TradeCase`, `EvidenceItem`, `SourceManifest`, `VoiceActionEvent`.
- Data Broker como unica via para fuentes publicas, FTP, cliente, voz y fuentes comerciales.
- FTP publico DNA como objetivo futuro, no habilitado.
- RegimenEngine con decision humana obligatoria.
- DocIntel con source/page/confidence/model tracking.
- PuertoLight absorbido, no `OSLA Puerto` como vertical separada.
- VoxBridge como canal auditado de follow-up, no plataforma de voz.

### Aspiracional / no listo

- Cualquier ingestion real DNA, DGI, VUCE, LUCIA, IMPO o FTP.
- Cualquier descarga masiva, preflight FTP, listado remoto, parseo, OCR o embedding.
- Cualquier escritura a DB/storage.
- Cualquier claim de NCM final, regimen final o aprobacion operativa automatica.
- Cualquier scoring ML, anomaly detection, forecasting o dashboard productivo.

## 4. Data Broker FTP: readiness especifico

Estado de fuente `uy.dna.public_ftp`:

```yaml
state: blocked_until_source_prereqs_closed
access_class: public_restricted
license_status: unknown_needs_review
allowed_paths: []
reserved_dirs: blocked
lucia_dirs: blocked
real_network: blocked
metadata_preflight: blocked
download: blocked
db_writes: blocked
storage_writes: blocked
```

Regla V3-Q: el primer corte tecnico no puede tocar `ftp://ftp.aduanas.gub.uy`, ni siquiera metadata-only. Lo unico permitido es modelar contratos, fixtures sinteticos, policy evaluators y reportes offline.

Antes de cualquier preflight futuro deben existir:

- owner humano de fuente;
- decision de licencia/terminos por path o dataset;
- allowlist ejecutable no vacia y aprobada;
- denylist dura aplicada;
- throttle/concurrency/stop conditions aprobados;
- salida ledger/reporte sin DB;
- confirmacion de `files_downloaded = 0` y `bytes_downloaded = 0` para metadata-only;
- aprobacion explicita de Data Broker.

## 5. Corte tecnico recomendado

Primer corte tecnico permitido:

```text
offline_contracts_and_policy_v0
```

Alcance:

- crear contratos versionados para `TradeCase`, `EvidenceItem`, `SourceManifest`, `VoiceActionEvent`;
- fixtures sinteticos sin datos reales;
- validadores offline para sensibilidad, source policy y action policy;
- tests unitarios de allowed/denied sin red;
- manifest fake de corrida `metadata_only` con cero archivos descargados y cero bytes;
- matriz de gaps y decisiones pendientes.

Fuera de alcance:

- FTP real;
- descarga o listado remoto;
- OCR;
- embeddings;
- modelos;
- DB/storage;
- integracion con Licita/Core;
- cambios a Docs OSLA consolidados.

## 6. Gaps

### P0

- No existe implementacion local de contratos canonicos.
- `uy.dna.public_ftp` esta bloqueado; allowlist ejecutable actual es vacia.
- Licencia/terminos del FTP completo siguen `unknown_needs_review`.
- No hay Data Broker ejecutable con manifests, hash index, ledger y stop conditions.
- No hay policy guard que impida fuentes reservadas, LUCIA/VUCE, descarga, DB/storage, OCR o embeddings.
- No hay separation test que pruebe que PuertoLight y VoxBridge son modulos absorbidos, no verticales.

### P1

- Docs historicos del repo contradicen V3 al afirmar APIs/ingesta/producto operativo sin evidencia observable.
- Falta owner humano formal para fuente DNA FTP.
- Falta matriz de sensibilidad por tipo de evidencia.
- Falta set minimo de fixtures de TradeCase y EvidenceItem.
- Falta RegimenEngine offline con escenarios de franquicia, IVA, 60%, regimen general y explicacion no juridica.
- Falta VoxBridge policy con una accion permitida y una prohibida.

### P2

- Datasets catalogados DNA parecen mejor primer carril que FTP completo, pero requieren mapeo por dataset/licencia.
- Falta naming final de paquetes y layout tecnico.
- Falta forecast de volumen/bytes/freshness.
- Falta decision de stack minima para contratos y tests.
- Falta roadmap de UI/API una vez existan contratos.

## 7. Debe existir antes del primer corte tecnico de Aduana

Antes del primer corte tecnico con valor real, debe existir al menos:

- `packages/core_contracts` o equivalente con schemas versionados.
- Fixtures sinteticos para caso, evidencia, manifest, regimen y voz.
- Tests offline que fallen si se intenta declarar fuente reservada como publica.
- Tests offline que fallen si `SourceManifest.mode = metadata_only` tiene `files_downloaded > 0` o `bytes_downloaded > 0`.
- Denylist aplicada a nombres/path de LUCIA, VUCE, reservado, privado, credenciales y operadores.
- `RegimenEngine` v0 deterministico con explicacion y disclaimer de revision humana.
- `VoxBridge` action policy v0 con acciones permitidas/prohibidas.
- `PuertoLight` event contract adjuntable a `TradeCase`, sin vertical separada.
- Decision escrita de no DB/storage para este corte.
- Runlog/evidence pack del corte con comandos, validaciones y riesgos.

## 8. No negociables operativos

- Aduana no reemplaza al despachante.
- NCM final y regimen final requieren humano.
- No se accede a DNA/VUCE/LUCIA reservado sin permiso.
- No se usa FTP real hasta cerrar prerequisitos.
- No se parsea, OCR-ea ni embebe como parte de descarga inicial.
- VoxBridge coordina y escala; no decide ni instruye legalmente.
- PuertoLight es modulo absorbido por TradeCase.
