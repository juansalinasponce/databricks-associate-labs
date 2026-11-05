# Evidencias — Gobierno de siniestros

- Participante / pareja:
- Fecha:
- Catálogo y schema:
- Identidad administradora (`current_user()`):
- Identidad analista (`current_user()`, si existe):
- Principal al que se concedió acceso y membresía utilizada:
- Modalidad: real / demo del instructor / simulación.
- Capacidades no disponibles:

## Matriz propuesta antes de ejecutar

| Perfil | Activo | Operación necesaria | Privilegios mínimos | Quién aprueba |
| --- | --- | --- | --- | --- |
| Analista | Resumen Gold | | | |
| Ingeniero | Tabla Silver | | | |
| Auditor | Activo autorizado | | | |

## Comprobación por fase

Adjunta o enlaza evidencia con identidad, consulta y resultado. En simulación,
escribe **predicción**, sin presentarla como una denegación aplicada por Databricks.

| Fase | Identidad | Vista: observado | Tabla: observado | UPDATE: observado | Evidencia / mensaje |
| --- | --- | --- | --- | --- | --- |
| A — antes de conceder | | | | | |
| B — lectura Gold | | | | | |
| C — revocar Gold | | | | | |
| D — directo + heredado | | | | | |
| E — revocar directo | | | | | |
| F — revocar en schema | | | | | |
| G — mínimo final | | | | | |

## Descubrimiento y responsabilidades

- Descripción del indicador y moneda:
- Fuente y columnas utilizadas:
- Owner técnico mostrado en Catalog:
- Data Owner de negocio ficticio:
- Data Steward: responsabilidad asignada:
- Data Custodian: responsabilidad asignada:
- Tags aplicados o propuestos:
- Lineage observado / diagramado (indicar cuál):
- Si cambia `monto_pagado`, ¿qué consumidor revisarías?:

## Extensión, si se realizó

- Ruta del Volume DEV:
- Ruta del Volume PRD:
- Resultado de listar archivos DEV con el analista:
- Resultado de listar archivos PRD con el analista:
- Resultado de volver a listar DEV después de revocar:
- Cadena de gobierno sobre S3 y control que corresponde a IAM:

## Decisión que reutilizaré

- ¿Por qué la vista satisface la necesidad del analista?:
- ¿Por qué revocar sobre la tabla no retiró el acceso heredado?:
- ¿Un tag descriptivo enmascara datos automáticamente? Explica:
- ¿Qué permiso temporal retiraste y cuál conservaste?:

## Cierre vigente — Power BI Desktop

- Usuario de Databricks utilizado por la conexión: juan.salinas@atokongo.com.
- Grupo confirmado: s14_alumno01_analistas.
- CAN USE del SQL Warehouse verificado:
- Vista conectada: workspace.s14_alumno01_gobierno.gold_siniestros_resumen.
- Resultado de nueva consulta a Gold desde el usuario:
- Mensaje de acceso denegado a Silver y evidencia de identidad:
- Permisos amplios de pruebas anteriores encontrados y retirados:
- Método de conexión: Databricks / OAuth; modo Import.
- Captura de las dos filas en Power BI:
- Totales verificados: 6 siniestros / 3000.00 PEN.
- Estado final: usuario en el grupo, lectura de la vista y uso del warehouse conservados.
- Modalidad del cierre: conexión real / demo / pendiente por entorno.

No incluir credenciales, tokens ni secretos en las capturas.
