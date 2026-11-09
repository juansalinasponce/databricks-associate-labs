# Crear el dashboard de siniestros

Usa la vista `workspace.gold_s15_seguros.vw_siniestros_negocio` preparada en
`00` y `01`. Trabaja como analista si está habilitado, o como propietario en
tu Free Edition personal. Las rutas de interfaz pueden variar.

## 1. Crear un único dataset

1. En **New → Dashboard** o **Dashboards → Create dashboard**, crea
   `S15 - Siniestros 2025`.
2. Selecciona el SQL Warehouse existente con el que consultaste la vista.
3. En **Data → Add SQL dataset**, pega **solo** esta consulta:

   ```sql
   SELECT mes_reporte, tipo_seguro, estado_siniestro,
          cantidad_siniestros, monto_pagado, monto_reservado,
          cantidad_cerrados, fecha_corte
   FROM workspace.gold_s15_seguros.vw_siniestros_negocio
   ```

4. Ejecuta y nombra el dataset **Siniestros Negocio**. Debe devolver 72 filas.

El dataset utiliza la vista permanente; no necesita conexión externa, hostname,
token ni una copia CSV. No pegues los `CREATE`, el `INSERT` ni todas las consultas
de validación en el dataset. Consulta el
[tutorial oficial de creación](https://docs.databricks.com/aws/en/dashboards/tutorials/create-dashboard).

## 2. Añadir indicadores y gráficos

En **Canvas**, añade un widget de visualización. Selecciona **Siniestros
Negocio**, el tipo de visual y los campos del panel de configuración. Para cada
campo numérico selecciona explícitamente **SUM**. Repite para cada fila:

| Visual | Título | Configuración | Control sin filtros |
| --- | --- | --- | --- |
| Counter / KPI | Total de siniestros | Valor `SUM(cantidad_siniestros)` | 2328 |
| Counter / KPI | Monto pagado (PEN) | Valor `SUM(monto_pagado)` | 1546800.00 |
| Counter / KPI | Monto reservado ficticio (PEN) | Valor `SUM(monto_reservado)` | 946800.00 |
| Line | Siniestros por mes de reporte | X `mes_reporte`, granularidad mes y orden ascendente; Y `SUM(cantidad_siniestros)` | 12 puntos, de 150 a 238 |
| Bar | Pagado por tipo de seguro (PEN) | X `tipo_seguro`; Y `SUM(monto_pagado)` | AUTO lidera con 630600.00 |

Organiza los tres KPIs arriba y los gráficos debajo. Agrega un texto:
**Datos sintéticos. Reportados en 2025. Estado y montos acumulados al corte
31/12/2025. Moneda PEN.** Conserva las fechas como fechas, no como nombres
alfabéticos de meses. Para verificar cifras, muestra valores completos, sin
abreviar a miles o millones; después puedes cambiar el formato.

Los campos cuantitativos admiten distintas agregaciones, por lo que hay que
comprobar la elegida en cada visual:
[configuración de visualizaciones](https://docs.databricks.com/aws/en/dashboards/manage/visualizations).

## 3. Conectar y probar los filtros

1. Añade un **Filter** con selección única o múltiple y campo
   **Siniestros Negocio → tipo_seguro**. Título: `Tipo de seguro`.
2. Añade un filtro de **Date range** asociado a
   **Siniestros Negocio → mes_reporte**. Título: `Mes de reporte`.
3. Comprueba que todos los widgets usan ese dataset y que ambos filtros se
   aplican a todos ellos. No crees un dataset de totales separado para los KPIs.
4. Selecciona **AUTO** y el rango **01/01/2025–31/01/2025**. Si aparece **Apply**,
   aplícalo. Debes ver 50 siniestros, PEN 41000 pagados y PEN 20000 reservados.
5. La línea debe mostrar solo enero y las barras solo AUTO. Contrasta con la
   consulta 6 de `02-consultas-y-validacion.sql`.
6. Limpia ambos filtros y verifica otra vez los totales anuales.

Un filtro visual segmenta el análisis; los permisos de datos se controlan
aparte. El dashboard y Ask Genie pueden utilizar todas las filas y columnas
incluidas en el dataset según su modo de acceso.

## 4. Opcional: porcentaje de cierre y tabla por estado

En **Data**, selecciona el dataset → **Custom calculation**. Crea una
**Calculated measure** llamada `ratio_cierre` con esta expresión:

```sql
SUM(cantidad_cerrados) / NULLIF(SUM(cantidad_siniestros), 0)
```

En Canvas, crea un Counter/KPI con esa medida y formato **Percentage**, dos
decimales. No multipliques por 100 en la medida si el formato lo hace: el valor
base es aproximadamente `0.7603` y se muestra como **76.03%**. Si eliges formato
decimal, muestra `100 * ratio` con título `Porcentaje de cierre`.

La medida debe recalcularse sobre las sumas del filtro. No promedies porcentajes
de filas ni sumes porcentajes. Con enero/AUTO debe mostrar **80.00%**. Si no está
disponible el cálculo, deja los tres KPIs principales y verifica el porcentaje
con la consulta 2 de `02`.

Añade una tabla o donut con `estado_siniestro` y `SUM(cantidad_siniestros)`:
ABIERTO 558 y CERRADO 1770. Los cálculos agregados se explican en
[custom calculations](https://docs.databricks.com/aws/en/dashboards/manage/data-modeling/custom-calculations).

## 5. Publicar y probar el acceso

1. Sin filtros activos, revisa títulos, cifras, dataset y texto de contexto.
2. Pulsa **Publish**. Si se ofrece **Individual data permissions / credenciales
   del lector**, elígelo para continuar el ejercicio de permisos: cada lector
   utiliza su propio acceso a la vista. Conserva el dashboard para tu uso.
3. Si el entorno permite compartir y tienes al analista preparado, concede
   solo **CAN VIEW** al principal acordado y abre el dashboard publicado desde
   esa identidad. Los privilegios de la vista y el uso del warehouse se comprueban
   por separado; no necesitas conceder escritura en Gold.
4. Si solo se ofrece **Shared data permissions / credenciales del publicador**,
   úsalo para la demo personal y anota el modo. En ese caso el lector consume con
   permisos del publicador: el dashboard no prueba su acceso SQL propio.
5. Si no puedes publicar, conserva el borrador y las capturas como resultado;
   la publicación queda como demo. Los cambios posteriores del borrador requieren
   publicar de nuevo para aparecer en la versión publicada.

La diferencia entre credenciales compartidas e individuales y el procedimiento
de publicación están en [compartir un dashboard](https://docs.databricks.com/aws/en/dashboards/share/share).

## 6. Preguntar con Ask Genie

Si aparece **Settings → General → Enable Genie**, comprueba que esté activado
y publica de nuevo. En la versión publicada, abre **Ask Genie** y sigue
[GENIE.md](GENIE.md). No necesitas crear un agente independiente para completar
la práctica. Si la opción no aparece, continúa con Genie Code o con el SQL de
referencia y marca Ask Genie como no disponible.

El Genie asociado puede acceder al conjunto de resultados del dataset, incluso
a campos no mostrados en un widget. Por eso el dataset incluye solo indicadores
sintéticos de consumo. El modo de credenciales también afecta al Genie generado
con el dashboard: [Genie con dashboards](https://docs.databricks.com/aws/en/dashboards/genie-spaces).

## Si algo no coincide

| Síntoma | Comprobación concreta |
| --- | --- |
| KPI muestra 72 | Cambia COUNT por SUM de `cantidad_siniestros` |
| KPI no cambia con el filtro | Revisa campo vinculado, alcance y dataset del widget |
| Línea no muestra 12 meses | Limpia filtros y revisa granularidad/orden de `mes_reporte` |
| Porcentaje aparece 7603% | Quita la multiplicación por 100 si usas formato Percentage |
| Tabla/vista no encontrada | Comprueba catálogo, schema, preparación y workspace |
| Vista funciona, dashboard falla | Revisa warehouse seleccionado y credenciales de publicación |
| Se alcanzó una cuota | Usa el fallback del README; no crees más recursos para eludirla |

Fuentes oficiales consultadas el **9 de noviembre de 2026**. La interfaz y las
capacidades se verifican en el Free Edition de la clase.
