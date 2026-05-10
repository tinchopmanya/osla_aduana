# Aduana Runtime Handoff 2026-05-07

Estado: runtime offline auditado y handoff listo.

## Alcance ejecutado

- Auditado rechazo de cruces `2025`/`2026` en runtime offline.
- Agregada cobertura de tests para cruce de `processing_summary.year` contra
  runtime default `2026`.
- Agregada cobertura de tests para `EvidenceItem.ftp_path` cruzado entre
  particiones `2025`/`2026`.
- Creado `docs/ADUANA_S6_PROCESSING_GO_REQUEST.md` como pedido documental,
  sin ejecutar procesamiento.
- Definido contrato S5 -> runtime offline para manifests, evidence pointers y
  summary, sin abrir ZIP/XML desde este agente.

## Auditoria de cruces 2025/2026

El runtime rechaza cruces por capas:

- `validate_datalake_year(...)` acepta solo `2025` y `2026`.
- `AduanaDataLake` fija `year` y `run_id` al construir el runtime.
- `build_readiness_report()` rechaza `processing_summary.run_id` distinto al
  runtime.
- `build_readiness_report()` rechaza `processing_summary.year` distinto al
  runtime.
- `load_source_manifests()` rechaza manifests con `year` o `run_id`
  inconsistentes.
- `SourceManifest.ftp_path` debe empezar con `DUA Diarios XML/{year}/`.
- `SourceManifest.bronze_path` debe incluir
  `bronze/uy_dna_public_ftp/{year}/{partition}`.
- `EvidenceItem.ftp_path` debe estar en la particion exacta del runtime.
- Paths FTP/bronze rechazan el otro anio soportado como segmento.
- Nombres `ddYYYYMMDD.zip` y `dmYYYYMM.zip` deben coincidir con el `year` del
  runtime.

Conclusion: el cruce 2025/2026 queda bloqueado antes de readiness y antes de
construir un `TradeCase` para revision.

## Tests agregados

Archivo: `tests/test_offline_runtime.py`

- `test_loader_rejects_default_runtime_with_2025_processing_summary`
- `test_loader_rejects_cross_year_evidence_ftp_path`

Cobertura existente relevante conservada:

- summary `2026` contra runtime `2025`;
- run_id mismatch;
- manifest `year` mismatch;
- FTP path con segmento de otro anio;
- ZIP diario/mensual con anio cruzado;
- bronze path con segmento de otro anio;
- particiones sinteticas `2025` y `2026` aceptadas cuando son consistentes.

## Contrato S5 -> Runtime Offline

S5 puede entregar `SourceManifest` de ZIP sin abrir ZIP/XML. El runtime consume
metadata y punteros, no payload raw:

```text
gold/evidence/{year}/source_manifests.jsonl
gold/evidence/{year}/evidence_items.jsonl
runs/{run_id}/processing_summary.json
```

Reglas minimas:

- `year` en cada artifact debe coincidir con el runtime.
- `run_id` en cada artifact debe coincidir con el runtime.
- FTP path: `DUA Diarios XML/{year}/dd|dm...zip`.
- Bronze path: `bronze/uy_dna_public_ftp/{year}/{partition}/...zip`.
- ZIP filename year debe coincidir con `year`.
- `processing_summary.source_zip_count` es el campo canonico requerido; no se
  acepta `quarantine_zip_pointer_count` como alias.
- `db_writes = 0`.
- `SourceManifest.raw_copied = false` para el GO documental. El campo significa
  payload raw ZIP/XML copiado por/para este carril, no un puntero externo de
  metadata fuera de Git.
- `EvidenceItem`, si existe, debe traer `member_name`, `member_sha256`,
  `root_tag` y `parsed_record_pointer` como strings no vacios; no se aceptan
  placeholders `null`.
- `EvidenceItem.member_sha256` debe ser un digest SHA256 hexadecimal de 64
  caracteres cuando aplique. Si no hay GO material/procesamiento separado, no
  se emiten filas placeholder y `processing_summary.evidence_items` queda en
  `0`.
- `raw_xml_copied_to_gold = false` para evidence.
- `automatic_decision = false`.
- `raw_files_written_to_repo = false`.
- OCR procesado, embeddings y model jobs deben quedar en `0`.

La definicion completa queda en:

```text
docs/ADUANA_S6_PROCESSING_GO_REQUEST.md
```

## Readiness

`DataLakeReadinessReport` marca `ready_for_review` solo si:

- `source_zip_count` y `bronze_zip_count` reconciliados;
- `source_bytes` y `bronze_bytes` reconciliados;
- manifest count y evidence count reconciliados;
- hashes sin mismatch;
- ZIP members y XML parse sin errores declarados;
- cero DB writes;
- cero red usada por el runtime offline;
- cero raw escrito al repo;
- cero OCR procesado;
- cero embeddings generados.
- cero uso de modelos.

## Integracion Data Broker fail-closed

Nucleus quedo endurecido como fail-closed. Aduana no relaja nucleus y adopta
ese contrato:

- `modelops` en runtime offline queda en estado seguro `blocked` si no hay
  `allow_model_use=true` y `policy_reference` explicitos.
- `selected_model_id` debe ser `null`; el runtime offline no asume
  `frontier-review` ni ningun otro modelo.
- El smoke offline ya no solicita preflight material `download`.
- El broker envelope del smoke representa una observacion metadata-only de
  punteros (`metadata_observation`) validada con una decision
  `approved_metadata_only`.
- La decision declara `allow_material_reads=false`,
  `allow_material_writes=false`, `allow_network_access=false`,
  `allow_db_writes=false` y `allow_model_use=false`.
- `broker_envelope_bytes_total=0`: los bytes del ZIP solo aparecen como
  metadata declarada en `pointer_manifest.declared_size_bytes`, no como bytes
  descargados o autorizados para transferencia.
- Readiness incorpora `no_models_used` usando los contadores opcionales
  `model_requests` y `model_inferences`.

Estado seguro documentado: si una futura ejecucion necesita descarga, escritura,
OCR, embeddings, red, DB writes o modelos, debe abrirse una decision explicita
en Data Broker fuera del runtime offline. Este carril no la abre.

## Prohibiciones respetadas

- No se descargo nada.
- No se abrio ningun ZIP/XML.
- No se parseo material.
- No hubo DB writes persistentes ni materiales.
- No hubo OCR.
- No hubo embeddings.
- No hubo modelos.
- No hubo mezcla con Licita, TCR, Obras ni Empresa.

## Checks

```text
PYTHONPATH=C:\dev\osla\osla_aduana\src;C:\dev\nucleus\src
C:\dev\nucleus\.venv\Scripts\python.exe -m pytest tests/test_offline_runtime.py tests/test_offline_smoke.py tests/test_v3_s_fixtures_policy.py -q
```

Resultado:

```text
40 passed in 0.62s
```

`git diff --check`: pass.

`raw nuevo`: 0.

## Archivos tocados

- `tests/test_offline_runtime.py`
- `tests/test_offline_smoke.py`
- `src/osla_aduana/offline_runtime.py`
- `src/osla_aduana/offline_smoke.py`
- `docs/ADUANA_S6_PROCESSING_GO_REQUEST.md`
- `docs/ADUANA_RUNTIME_HANDOFF_2026_05_07.md`
