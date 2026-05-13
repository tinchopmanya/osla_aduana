---
slug: osla_aduana
entidad: vertical
estado_documento: mirror_do_not_edit_here
tipo_archivo: readme
canon_path: C:\dev\osla\osla_aduana\docs\v3_canonical\README.md
supersedes: []
superseded_by: null
fuente_de_verdad: C:\dev\Investigacion_Osla_consolidada\FUENTE_DE_VERDAD_VERTICALES.md
no_usar_como_fuente_de_verdad: true
updated_at: 2026-05-13T02:55:45Z
owner: CODEX_5_5
auto_generated: false
disclaimers: []
mirror_of: C:\dev\Investigacion_Osla_consolidada\NUEVOSDOCUMENTOS_29deabril\README.md
notas: mirror of V3 canonical import
encoding: ascii_puro
---
# Aduana V3 Canonical Pack

Estado: canon operativo preservado desde los documentos V3 entregados por Martin.
Fecha de preservacion: 2026-05-10.

Este directorio guarda las ultimas versiones V3 de Aduana para que no dependan
de archivos en `Downloads` ni del historial de chat.

## Archivos preservados

- `agentsaduana_v3.md`: contrato de ejecucion paralela y roles de agentes.
- `aduana__chatgpt_29_04_2026_v3.md`: sintesis V3 de producto y VoxBridge.
- `productoaduana_v3.md`: definicion canonica de producto.
- `roadmapaduana_v3.md`: roadmap canonico V3.

## Regla de precedencia

Si `docs/Producto.md` o `docs/ROADMAP.md` contradicen este pack V3, gana este
directorio hasta que esos documentos legacy sean reconciliados.

La direccion correcta de producto es:

```text
OSLA Aduana = Trade Evidence Desk / Aduana Control Tower
```

No debe reconstruirse como dashboard, clasificador NCM autonomo, filing
automatico, scoring legal final ni reemplazo del despachante.

## Proximo sprint recomendado

Crear un sprint `Aduana V3 Product/Roadmap Reconciliation` que:

1. convierta `docs/Producto.md` y `docs/ROADMAP.md` en documentos alineados con
   V3;
2. mantenga una seccion legacy solo como historia;
3. conecte el runtime offline actual con fases V3 reales;
4. liste que partes V3 ya estan implementadas, parciales o pendientes;
5. bloquee claims de NCM final, regimen final, hold/release, filing, DNA/VUCE
   reservado y fuentes reales sin Data Broker.
