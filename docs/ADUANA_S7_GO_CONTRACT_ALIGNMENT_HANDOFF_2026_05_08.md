---
slug: osla_aduana
entidad: vertical
estado_documento: runtime_implementation_doc
tipo_archivo: handoff
canon_path: C:\dev\osla\osla_aduana\docs\ADUANA_S7_GO_CONTRACT_ALIGNMENT_HANDOFF_2026_05_08.md
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
# Aduana S7 GO Contract Alignment Handoff 2026-05-08

Estado: S7 aplicado en runtime/tests/docs. No commit.

Veredicto: GO condicionado para S6 processing GO documental.

## Decision de alcance

Se eligio runtime + tests + docs, no docs-only.

Motivo:

- `processing_summary.source_zip_count` ya era el contrato real del runtime; no
  se agrego alias para `quarantine_zip_pointer_count` porque ocultaria un
  summary incompatible con tests/runtime.
- `SourceManifest.raw_copied=True` no tenia bloqueo claro. Se agrego un check
  minimo en `SourceManifest.from_dict(...)` para que el GO documental falle con
  `ContractError`.

## Semantica S7

- `source_zip_count` es el campo canonico requerido en
  `processing_summary.json`.
- `quarantine_zip_pointer_count` no es alias aceptado por el runtime offline y
  su presencia es NO-GO contractual.
- `raw_copied` significa payload raw ZIP/XML copiado por/para este carril a
  repo, Gold, outputs de Aduana o area material controlada por el GO.
- Un `quarantine_zip_pointer` o `bronze_path` fuera de Git es metadata de
  puntero; no vuelve `raw_copied=True`.
- Para S6 documental, `SourceManifest.raw_copied` debe ser `false`.
- `EvidenceItem`, cuando exista, debe traer `member_name`, `member_sha256`,
  `root_tag` y `parsed_record_pointer` como strings no vacios; no se aceptan
  placeholders `null`.
- `member_sha256` debe ser SHA256 hexadecimal de 64 caracteres cuando aplique a
  un miembro ZIP/XML derivado.
- Sin GO material/procesamiento separado, no se emiten `EvidenceItem`
  placeholder; `evidence_items.jsonl` queda vacio y
  `processing_summary.evidence_items=0`.

## Findings

P0: 0.

P1:

- CG-S6-F01 cerrado. El GO request ahora usa `source_zip_count` y declara que
  `quarantine_zip_pointer_count` es NO-GO si aparece en el summary. Tests
  negativos: `test_readiness_report_requires_source_zip_count` y
  `test_readiness_report_rejects_quarantine_zip_pointer_count_alias`.
- CG-S6-F02 cerrado. `SourceManifest.raw_copied=True` ahora levanta
  `ContractError` y bloquea readiness/smoke documental. Tests negativos:
  `test_contracts_reject_db_writes_and_raw_copies` y
  `test_readiness_report_rejects_raw_copied_source_manifest`; smoke negativo:
  `test_offline_guardrails_smoke_rejects_raw_copied_source_manifest`.

P2:

- El repo no tiene `.\.venv\Scripts\python.exe`, por lo que el check literal
  pedido no puede ejecutarse desde este checkout. Se ejecuto la suite con el
  runner ya usado por Aduana/Nucleus y `PYTHONPATH` local.
- El smoke contra `C:\dev\osla_datalake\aduana` queda opt-in mediante
  `OSLA_ADUANA_RUN_REAL_DATALAKE_SMOKE=1` para que la suite S7 por defecto no
  toque payloads ni datalake real. En una ejecucion opt-in, artifacts reales con
  `raw_copied=True` son NO-GO contractual.

## Archivos modificados

- `docs/ADUANA_S6_PROCESSING_GO_REQUEST.md`
- `docs/ADUANA_RUNTIME_HANDOFF_2026_05_07.md`
- `docs/ADUANA_S7_GO_CONTRACT_ALIGNMENT_HANDOFF_2026_05_08.md`
- `src/osla_aduana/offline_runtime.py`
- `tests/test_offline_runtime.py`
- `tests/test_offline_smoke.py`

## Tests literales

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
```

Resultado: no ejecutable en este checkout; `.\.venv\Scripts\python.exe` no
existe.

```powershell
$env:PYTHONPATH='C:\dev\osla\osla_aduana\src;C:\dev\nucleus\src'
C:\dev\nucleus\.venv\Scripts\python.exe -m pytest tests -q
```

Resultado:

```text
46 passed, 1 skipped in 1.74s
```

```powershell
git diff --check
```

Resultado: pass.

```powershell
$raw = @(rg --files -g '*.zip' -g '*.xml' -g '*.pdf' -g '*.csv' -g '*.xlsx' -g '*.parquet' -g '!reports/**' -g '!.git/**' -g '!.venv/**' -g '!.pytest_cache/**' -g '!.mypy_cache/**' -g '!.ruff_cache/**' -g '!__pycache__/**')
"RG_MATCH_COUNT=$($raw.Count)"
$raw
```

Resultado: pass, `RG_MATCH_COUNT=0` y sin rutas listadas.

## Veredicto

GO condicionado para S6 processing GO documental.

Condiciones:

- Download Captain debe entregar `processing_summary.source_zip_count`; no se
  acepta `quarantine_zip_pointer_count` como campo adicional ni reemplazo.
- Todos los `SourceManifest` del carril documental deben declarar
  `raw_copied=false`.
- Los `EvidenceItem` no pueden usar `null` en campos que el runtime exige como
  strings; si no hay procesamiento material autorizado, no se emiten
  placeholders.
- No se autoriza red, FTP, RETR, descargas, parseo, OCR, embeddings, modelos,
  DB writes persistentes ni apertura de ZIP/XML/PDF/CSV/XLSX/PARQUET.
- Artifacts reales que contradigan este contrato quedan en NO-GO hasta que el
  owner material entregue metadata corregida; este agente no modifica
  quarantine/datalake payloads.
