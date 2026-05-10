# Aduana V3 Reconciliation TODO

**Estado:** guarda documental para evitar que docs legacy se usen como roadmap vigente.

## Regla De Precedencia

Los documentos V3 en `docs/v3_canonical/` y los contratos `ADUANA_V3_*` prevalecen sobre `Producto.md`, `ROADMAP.md` e `Investigaciones.md` cuando haya contradiccion.

## Contradicciones A Reconciliar

| Legacy / riesgo | Correccion V3 |
| --- | --- |
| Plataforma o dashboard amplio de comercio exterior. | Trade Evidence Desk con casos, evidencia, tareas, decision humana y audit trail. |
| MVP operativo con DNA, DGI y BCU como integraciones directas. | No afirmar integraciones reales sin Data Broker, politicas de fuente, manifests, allowlists y licencia verificada. |
| Scoring de riesgo, NCM/HS, regimen u origen como resultado final. | NCM, regimen, origen, tributos y decisiones finales requieren humano; el sistema solo prepara evidencia y checks. |
| Automatizar hold/release, filing o presentacion. | Prohibido sin contrato futuro y GO explicito; V3 no los habilita. |
| Usar Aduana como vertical aislada de Puerto/Importa sin frontera. | Aduana debe reconciliarse con Puerto/Importa por flujo logistico, pero sin absorber verticales hasta que el contrato lo defina. |

## Estado Real Verificable

Hay documentos y validadores V3, runtime offline y fixtures/policies. No tratar como hecho actual:

- UI de producto final.
- API productiva.
- DB productiva.
- conectores vivos a DNA/DGI/BCU.
- procesamiento automatico completo 2025/2026 como vertical lista.

## Checklist De Reconciliacion

- [ ] Reescribir o reemplazar `Producto.md` para que apunte a V3.
- [ ] Reescribir o reemplazar `ROADMAP.md` para separar aspiracional, actual y bloqueado.
- [ ] Marcar `Investigaciones.md` como input historico si contradice V3.
- [ ] Definir frontera Aduana/Puerto/Importa antes de prometer integracion de flujo completa.
- [ ] Mantener Data Broker como prerequisito para fuentes externas.
- [ ] Mantener prohibiciones de decision automatica, scraping, filing y payload real sin GO exacto.

## Stop Rule

Si un agente encuentra una instruccion legacy que pide dashboard, scoring, NCM final, regimen final, hold/release, filing o integracion viva, debe parar y citar este archivo antes de ejecutar.
