# Aduana S3 Post-Core Handoff 2026-05-07

Estado: GO condicionado para PR Aduana.

## Resumen

Se preparo Aduana para quedar destrabada despues del merge de nucleus
fail-closed, sin ejecutar operaciones materiales. El smoke ahora falla si
ModelOps deja de estar bloqueado por defecto.

## Core / Pin

Verificacion local de `C:\dev\nucleus`:

- `main` / `origin/main`: `b6da69931fbeb0cc396e17bcbe2ce2a041551ab5`.
- Branch fail-closed: `codex/data-broker-fail-closed-network-db`.
- HEAD fail-closed local S3 final: `baae625b1200a6963ee097497f1468fae62fe45e`
  (`Bind broker decisions to source context`).
- Version en branch fail-closed: `osla-core 0.3.8`.
- PR #16 de `osla-core` fue mergeado a `main` con SHA final
  `02cd169c669d0ccb911d6ef6f7b9445f7deca51b`.

Decision S4 post-core: `pyproject.toml` debe pinnear el SHA final mergeado de
core:

```text
osla-core @ git+https://github.com/tinchopmanya/osla-core.git@02cd169c669d0ccb911d6ef6f7b9445f7deca51b
```

## Cambios

Archivos modificados:

- `src/osla_aduana/offline_smoke.py`
- `tests/test_offline_smoke.py`
- `docs/ADUANA_OFFLINE_GUARDRAILS_SMOKE.md`

Implementado:

- hard-fail del smoke si `model_route_status != "blocked"`;
- hard-fail del smoke si `selected_model_id is not None`;
- hard-fail del smoke si `model_human_review_required` deja de ser `true`;
- hard-fail del smoke si el broker envelope declara
  `decision_json.allow_model_use = true`;
- tests parametrizados para drift de ModelOps:
  - modelo seleccionado;
  - route status distinto de `blocked`;
  - falta de human review.

## S6 Documental

`docs/ADUANA_S6_PROCESSING_GO_REQUEST.md` ya queda en postura documental:

- no contiene `bronze_path`;
- no contiene `"raw_copied": true`;
- no contiene `parsed_xml_pointer`;
- usa `quarantine_zip_pointer` como puntero fuera de Git;
- declara `material_opened=false`;
- declara `raw_copied=false`;
- mantiene `member_name`, `member_sha256`, `root_tag` y
  `parsed_record_pointer` en `null` hasta un GO material/procesamiento separado.

No se escribio datalake ni quarantine.

## Subagentes

- Runtime auditor read-only: confirmo el gap de hard-fail en smoke.
- Smoke/test auditor read-only: confirmo cobertura faltante y S6 documental.
- Dependency pin auditor read-only: confirmo que PR #16/fail-closed no esta
  mergeado en `main` local.

## Checks

```powershell
$env:PYTHONPATH='C:\dev\osla\osla_aduana\src;C:\dev\nucleus\src'
C:\dev\nucleus\.venv\Scripts\python.exe -m pytest tests -q
```

Resultado:

```text
43 passed in 0.76s
```

```powershell
git diff --check
```

Resultado: pass.

```powershell
git ls-files | Where-Object { $_ -match '\.(zip|xml|pdf|parquet|sqlite|db|duckdb|pkl|onnx|bin|jpg|jpeg|png|tif|tiff|wav|mp3|mp4|csv|jsonl)$' }
```

Resultado: sin salida.

## Scope Respetado

- No red ni descargas.
- No apertura ZIP/XML.
- No parseo material.
- No DB writes persistentes/materiales.
- No OCR, embeddings ni modelos.
- No datalake/quarantine writes.
- No se toco Licita, nucleus, consolidado ni `osla_eea`.
- No commit.

## Decision

GO condicionado para PR Aduana.

Condicion bloqueante S3 cerrada en S4: nucleus fail-closed PR #16 fue mergeado
y el pin de `osla-core` se actualiza al SHA final mergeado. Aduana debe repetir
tests con el pin final antes de pasar PR #13 a ready.
