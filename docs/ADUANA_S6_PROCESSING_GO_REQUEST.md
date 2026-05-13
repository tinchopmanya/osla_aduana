---
slug: osla_aduana
entidad: vertical
estado_documento: research_candidate
tipo_archivo: otro
canon_path: C:\dev\osla\osla_aduana\docs\ADUANA_S6_PROCESSING_GO_REQUEST.md
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
# Aduana S6 Documental GO Request

Fecha: 2026-05-07
Estado: GO request documental. No ejecuta procesamiento material.

## Rol

OSLA Aduana actua como agente tecnico de runtime y contratos. No descarga, no
abre ZIP/XML, no parsea material, no escribe DB, no ejecuta OCR, no genera
embeddings, no invoca modelos y no mezcla datos con Licita, TCR, Obras ni
Empresa.

Download Captain es el unico responsable de cualquier operacion material de
descarga o preparacion de corpus. Este documento solo fija el contrato que el
runtime offline de Aduana puede consumir despues de una entrega valida.

## Pedido

Solicitar a Download Captain una entrega S6 particionada por anio para preparar
el contrato de runtime:

- `2025`
- `2026`

Cada particion debe quedar aislada por `year` y `run_id`. No se aceptan cruces
2025/2026 en paths, nombres de ZIP, manifests, evidence pointers ni summaries.

## Salida esperada por particion

```text
C:\dev\osla_datalake\aduana\gold\evidence\{year}\source_manifests.jsonl
C:\dev\osla_datalake\aduana\gold\evidence\{year}\evidence_items.jsonl
C:\dev\osla_datalake\aduana\runs\{run_id}\processing_summary.json
```

`run_id` default esperado por el runtime:

```text
aduana_2025_full_process_001
aduana_2026_full_process_001
```

Un `run_id` distinto es aceptable solo si el caller lo pasa explicitamente al
runtime y el mismo valor aparece en todos los artifacts de la particion.

## Contrato S5 -> runtime offline

S5 puede entregar manifests de archivo ZIP sin abrir ZIP/XML. El runtime offline
solo requiere metadata verificable y punteros; nunca requiere payload raw dentro
del repo ni copia material ejecutada por Aduana en este GO documental. Si una
entrega autorizada incluye `bronze_path`, el runtime lo consume como puntero de
metadata fuera de Git para reconciliacion; no convierte `raw_copied` en `true`.

### `SourceManifest` JSONL

Un registro por ZIP fuente:

```json
{
  "source_manifest_id": "source:aduana:{year}:...",
  "run_id": "aduana_{year}_full_process_001",
  "source_key": "uy.dna.public_ftp",
  "year": "{year}",
  "partition": "daily_sample|daily_full|monthly_archive",
  "ftp_path": "DUA Diarios XML/{year}/dd{year}MMDD.zip",
  "quarantine_zip_pointer": "C:\\dev\\osla_quarantine\\uy_dna_public_ftp\\s5_aduana_{year}_material_001\\dd{year}MMDD.zip",
  "bronze_path": "C:\\dev\\osla_datalake\\aduana\\bronze\\uy_dna_public_ftp\\{year}\\daily_sample\\dd{year}MMDD.zip",
  "bytes": 123456,
  "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "material_available_in_quarantine": true,
  "material_opened": false,
  "raw_copied": false,
  "db_writes": 0
}
```

Reglas:

- `year` debe ser `2025` o `2026`.
- `ftp_path` debe empezar exactamente con `DUA Diarios XML/{year}/`.
- `quarantine_zip_pointer` debe apuntar fuera de Git y bajo
  `C:\dev\osla_quarantine\`.
- `bronze_path`, cuando exista una entrega ya preparada por el dueño material,
  debe ser un puntero fuera de Git bajo la particion exacta
  `bronze\uy_dna_public_ftp\{year}\{partition}`.
- El nombre del ZIP debe ser `ddYYYYMMDD.zip` o `dmYYYYMM.zip`.
- El `YYYY` del ZIP debe coincidir con `year`.
- Ningun path puede incluir el otro anio soportado como segmento.
- `bytes` debe ser un entero de metadata, sin copiar payload al repo.
- `material_opened` y `raw_copied` deben ser `false` en este GO documental.
- `raw_copied` significa que se copio payload raw ZIP/XML al repo, Gold,
  outputs de Aduana o un area material controlada por este GO. Un puntero
  `quarantine_zip_pointer` o `bronze_path` fuera de Git no cuenta como raw
  copiado, y el valor requerido sigue siendo `false`.
- `sha256` debe ser hexadecimal de 64 caracteres.
- `db_writes` debe ser `0`.

### `EvidenceItem` JSONL

`EvidenceItem` pertenece a una entrega S6 autorizada, no a S5 documental, porque
requiere punteros derivados de procesamiento material ya aprobado fuera de este
agente. En un GO documental sin procesamiento material,
`evidence_items.jsonl` puede quedar vacio y `processing_summary.evidence_items`
debe ser `0`. Si se emite un `EvidenceItem`, debe contener referencias
completas, no XML raw ni placeholders `null`:

```json
{
  "evidence_item_id": "evidence:aduana:{year}:...",
  "run_id": "aduana_{year}_full_process_001",
  "source_key": "uy.dna.public_ftp",
  "source_manifest_id": "source:aduana:{year}:...",
  "evidence_type": "parsed_xml_pointer",
  "ftp_path": "DUA Diarios XML/{year}/dd{year}MMDD.zip",
  "member_name": "dua.xml",
  "member_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "root_tag": "ROOT",
  "unique_field_count": 10,
  "parsed_record_pointer": "silver/dua_parsed/{year}/records.jsonl#1",
  "raw_xml_copied_to_gold": false,
  "automatic_decision": false
}
```

Reglas:

- `run_id` y `source_manifest_id` deben reconciliar contra `SourceManifest`.
- `ftp_path` queda sujeto a las mismas reglas de particion del `year`.
- `member_name`, `member_sha256`, `root_tag` y `parsed_record_pointer` deben
  ser strings no vacios cuando exista el registro; no se aceptan `null`.
- `member_sha256` debe ser un digest SHA256 hexadecimal de 64 caracteres cuando
  aplique a un miembro ZIP/XML derivado.
- Sin GO material/procesamiento separado, no emitir registros `EvidenceItem`
  de placeholder; usar JSONL vacio y summary `evidence_items=0`.
- `raw_xml_copied_to_gold` debe ser `false`.
- `automatic_decision` debe ser `false`.

### `processing_summary.json`

```json
{
  "run_id": "aduana_{year}_full_process_001",
  "year": "{year}",
  "source_zip_count": 0,
  "bronze_zip_count": 0,
  "source_bytes": 0,
  "bronze_bytes": 0,
  "source_manifests": 0,
  "evidence_items": 0,
  "xml_records_parsed": 0,
  "xml_parse_errors": 0,
  "zip_member_errors": 0,
  "hash_mismatches": 0,
  "ocr_candidates": 0,
  "ocr_files_processed": 0,
  "db_writes": 0,
  "network_used": false,
  "raw_files_written_to_repo": false,
  "embeddings_generated": 0,
  "embedding_jobs": 0,
  "model_requests": 0,
  "model_inferences": 0
}
```

Campo canonico requerido: `source_zip_count`. `quarantine_zip_pointer_count` no
es alias aceptado por el runtime offline ni por los tests S7; un summary que lo
incluya, incluso junto a `source_zip_count`, es NO-GO contractual.

Readiness solo puede ser `ready_for_review` si:

- summary `run_id` y `year` coinciden con el runtime;
- `source_zip_count`, `bronze_zip_count`, `source_bytes` y `bronze_bytes`
  quedan reconciliados segun el runtime;
- manifests y evidence items reconciliados;
- `hash_mismatches`, parse errors y member errors son `0`;
- `db_writes = 0`;
- `network_used = false` en el runtime offline;
- `raw_files_written_to_repo = false`;
- OCR y embeddings procesados son `0`;
- requests e inferencias de modelos son `0`.

## Criterio GO/NO-GO para runtime

GO:

- existen los tres artifacts por particion;
- cada artifact es metadata/puntero, no material raw;
- `year` y `run_id` son consistentes;
- `AduanaDataLake(...).build_readiness_report()` devuelve `ready_for_review`;
- `run_offline_guardrails_smoke(...)` devuelve `passed`.

NO-GO:

- cualquier cruce 2025/2026;
- ZIP con anio distinto al runtime;
- summary con `year` o `run_id` distinto;
- summary que incluya `quarantine_zip_pointer_count`;
- `SourceManifest.raw_copied = true`;
- raw XML copiado a Gold;
- DB writes, OCR, embeddings, modelos o decisiones automaticas;
- material de otra vertical o rutas de Licita/TCR/Obras/Empresa.

## Comando de validacion permitido para Aduana

Solo despues de que Download Captain entregue artifacts ya preparados:

```powershell
$env:PYTHONPATH="C:\dev\osla\osla_aduana\src;C:\dev\nucleus\src"
C:\dev\nucleus\.venv\Scripts\python.exe -m pytest tests/test_offline_runtime.py tests/test_offline_smoke.py tests/test_v3_s_fixtures_policy.py -q
git diff --check
```

Este documento no autoriza a OSLA Aduana a ejecutar procesamiento material.
