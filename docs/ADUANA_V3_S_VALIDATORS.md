---
slug: osla_aduana
entidad: vertical
estado_documento: research_candidate
tipo_archivo: otro
canon_path: C:\dev\osla\osla_aduana\docs\ADUANA_V3_S_VALIDATORS.md
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
# Aduana V3-S Validators

Fecha: 2026-05-02
Estado: validadores offline para fixtures sinteticos V3-S. No ejecuta red, FTP, descargas, DB, storage, OCR, embeddings ni modelos.

## 1. Alcance

Este corte agrega `tests/test_v3_s_fixtures_policy.py` como policy gate offline para `fixtures/v3_s/*.json`.

El validador solo lee JSON locales si existen. No crea ni edita fixtures, no abre endpoints, no lista FTP, no descarga datos, no escribe DB/storage y no corre OCR/embeddings.

## 2. Estado actual

Este PR ya incluye JSON directos bajo `fixtures/v3_s/*.json`. El validador recorre ese pack local y falla si falta la carpeta, si no hay JSON, o si aparece cualquier marcador material.

El validador no crea ni edita `fixtures/v3_s/*.json`; solo los lee. La ejecucion completa queda lista para un entorno que tenga `pytest`. En este corte, el repositorio local no tiene `pytest` instalado, por lo que el merge owner ejecuto validacion directa offline de las funciones `test_*` con stub minimo de `pytest`.

## 3. Reglas ejecutables

El test suite valida que cada fixture V3-S:

- exista bajo `fixtures/v3_s/*.json`;
- sea JSON UTF-8 valido;
- tenga marca sintetica (`source_context.is_synthetic = true`, `synthetic.is_synthetic = true` o `mode = synthetic_fixture`);
- use IDs marcados como sinteticos/redacted;
- no contenga URLs ejecutables `http(s)://`, `ftp://`, `sftp://` ni hosts reales de Aduana/VUCE/LUCIA;
- no contenga credenciales, tokens, cookies, claves privadas ni valores tipo secret;
- no contenga emails o datos identitarios sin marca synthetic/redacted;
- no habilite red, FTP, metadata preflight, descargas, DB writes ni storage writes;
- no contenga storage URLs, rutas absolutas reales ni SQL de escritura;
- no declare OCR, embeddings, vector stores ni procesamiento material;
- mantenga `files_downloaded = 0` y `bytes_downloaded = 0`;
- mantenga `ncm_final = null` y `regime_final/regimen_final = null`;
- bloquee acciones VoxBridge prohibidas con `action_status = denied` o `escalated`;
- fuerce `uy.dna.public_ftp` a `state = blocked_until_prereqs_closed`.

## 4. Criterio para SourceManifest

Todo objeto que parezca `SourceManifest` debe usar:

```json
{
  "mode": "synthetic_fixture",
  "files_downloaded": 0,
  "bytes_downloaded": 0,
  "source_policy": {
    "network_allowed": false,
    "db_writes_allowed": false,
    "storage_writes_allowed": false,
    "denylist_applied": true
  }
}
```

Si aparecen `metadata_preflight_allowed` o `download_allowed`, tambien deben ser `false`.

## 5. Criterio para decisiones finales

Los fixtures pueden sugerir regimen probable, documentar faltantes o exigir revision humana. No pueden escribir decision final automatica.

Campos bloqueados:

```json
{
  "ncm_final": null,
  "regime_final": null,
  "regimen_final": null,
  "decided_by": null
}
```

`selected_probable_regime` sigue permitido como sugerencia preliminar si el fixture deja claro que requiere revision humana.

## 6. Criterio para VoxBridge

Acciones prohibidas como `change_ncm_final`, `submit_customs_declaration`, `approve_operation`, `release_goods`, `delete_document` o `access_reserved_dna_or_vuce` solo pueden existir en fixtures si quedan denegadas o escaladas.

Acciones permitidas, por ejemplo `create_document_request`, siguen permitidas cuando no materializan red, DB, storage ni decisiones finales.

## 7. Comandos

Esperado:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_v3_s_fixtures_policy.py -q
git diff --check
```

Si el repo no tiene `.venv`, usar el `python -m pytest` disponible en el entorno.

## 8. Matriz P0/P1/P2

### P0

- Cualquier fixture con red/FTP real, credenciales, datos reales, DB/storage writes, OCR/embeddings, `ncm_final` o `regime_final` no nulos debe fallar.

### P1

- Revisar falsos positivos en datos sinteticos de identidad y ajustar solo dentro del test si el pack crece.
- Ampliar casos VoxBridge denied/escalated si el fixture pack agrega nuevas acciones prohibidas.
- Agregar convenciones finales de nombres si el Fixture Builder formaliza mas tipos de objeto.

### P2

- Convertir estos helpers en modulo reutilizable si aparece un paquete ejecutable de contratos.
- Agregar reporte resumido por archivo cuando haya mas volumen de fixtures.
- Integrar el check al pipeline cuando exista CI para `osla_aduana`.

## 9. Confirmacion operacional

Este corte es documental y de tests offline. No realiza operaciones materiales: cero red, cero FTP, cero descargas, cero DB, cero storage, cero OCR, cero embeddings y cero datos reales.
