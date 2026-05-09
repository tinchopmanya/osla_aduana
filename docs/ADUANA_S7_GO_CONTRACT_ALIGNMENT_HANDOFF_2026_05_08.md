# Aduana S7 GO Contract Alignment Handoff 2026-05-08

Estado: S7 contract alignment implementado. Veredicto: GO para S6 processing
GO documental tras correccion local de integracion y ejecucion pytest.

## Objetivo

Cerrar los dos P1 de CodeGuard antes de cualquier S6 processing GO:

- El GO request usaba `quarantine_zip_pointer_count`, pero el runtime exige
  `source_zip_count`.
- El GO request exigia `raw_copied=false`, pero el runtime aceptaba
  `SourceManifest.raw_copied=true`.

## Decision tecnica

Se eligio `runtime+tests`, no docs-only.

Razon:

- El mismatch de summary era corregible en docs sin alias.
- `raw_copied=true` era un estado material peligroso que pasaba por
  `SourceManifest.from_dict(...)`; por eso se agrego un bloqueo minimo en
  runtime.

No se agrego alias para `quarantine_zip_pointer_count`. En S6 documental el
campo requerido sigue siendo `source_zip_count`.

## Cambios

- `docs/ADUANA_S6_PROCESSING_GO_REQUEST.md`
  - `processing_summary.json` ahora documenta `source_zip_count`.
  - Declara que `quarantine_zip_pointer_count` no es alias aceptado.
  - Aclara que `raw_copied=false` significa que no se copio payload raw ZIP/XML
    al repo, Gold, Bronze ni storage propio del runtime para este GO documental.
  - Agrega `SourceManifest.raw_copied=false` como condicion de readiness.
  - Agrega NO-GO para alias `quarantine_zip_pointer_count` y para
    `SourceManifest.raw_copied=true`.

- `src/osla_aduana/offline_runtime.py`
  - `SourceManifest.from_dict(...)` conserva `raw_copied` como metadata flag
    para no romper datalakes/materiales existentes.
  - `build_readiness_report()` agrega el check `no_source_raw_copied`; S6
    documental queda en `attention_required` si cualquier manifest declara
    `raw_copied=true`.

- `tests/test_offline_runtime.py`
  - Helper sintetico `_source_manifest(...)` queda en `raw_copied=false`.
- Nuevo test unitario confirma que `SourceManifest.raw_copied=true` se parsea
  como flag metadata.
- Nuevo negativo de readiness para manifest con `raw_copied=true`.
  - Nuevo negativo para summary que use solo
    `quarantine_zip_pointer_count` en lugar de `source_zip_count`.

## Semantica raw_copied

Para S6 documental, `raw_copied` significa payload raw copiado. No representa un
puntero metadata-only ni bytes declarados.

Consecuencia:

- `raw_copied=false`: compatible con S6 documental.
- `raw_copied=true`: no rompe el loader porque puede existir en datalakes
  materiales previos, pero bloquea readiness documental mediante
  `no_source_raw_copied=false`; requiere un GO material separado y no puede
  declararse listo en este contrato.

## Commit local

No se creo commit local.

## Subagentes

No se usaron subagentes.

## Checks ejecutados

```powershell
if (Test-Path .\.venv\Scripts\python.exe) { .\.venv\Scripts\python.exe -m pytest tests -q } else { $env:PYTHONPATH="C:\dev\agent_worktrees\osla_aduana_codex_s7\src;C:\dev\nucleus\src"; C:\dev\nucleus\.venv\Scripts\python.exe -m pytest tests -q }
```

Resultado literal:

```text
45 passed, 1 skipped
```

Interpretacion: el worktree no tiene `.venv`; se uso
`C:\dev\nucleus\.venv\Scripts\python.exe` con `PYTHONPATH` apuntando al worktree
Aduana y a nucleus. El skip corresponde al datalake local material con
`raw_copied=true`, que queda fuera del contrato S6 documental.

```powershell
git diff --check
```

Resultado literal: sin salida. PASS.

```powershell
Get-ChildItem -Recurse -File -Include *.zip,*.xml,*.pdf,*.csv,*.xlsx,*.parquet | Where-Object { $_.FullName -notmatch '\\.venv\\|\\.git\\|reports\\|\\.codex_logs\\' }
```

Resultado literal: sin salida. PASS.

## P0/P1/P2

- P0: 0.
- P1: 0 abiertos en contrato/codigo tras este cambio.
- P2: 1 deuda residual: crear `.venv` propio de Aduana o documentar runner de
  tests compartido con nucleus.

## Veredicto

GO para S6 processing GO documental:

- NO-GO si un delivery usa `quarantine_zip_pointer_count` sin
  `source_zip_count`.
- NO-GO si cualquier `SourceManifest` declara `raw_copied=true` en el contrato
  documental S6.

## Prohibiciones confirmadas

- No red.
- No FTP.
- No downloads.
- No `RETR`.
- No ZIP/XML/PDF/CSV/XLSX/PARQUET abiertos.
- No parse, OCR, embeddings ni modelos.
- No DB writes persistentes.
- No quarantine/datalake payloads tocados.
- No `C:\dev\osla_eea` tocado.
- No merge a main.
