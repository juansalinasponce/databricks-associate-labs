# Dashboard del Data Product DP-SEG-016

El dashboard y Genie consumen el mismo producto y el mismo ambiente. La vista
de consumo ya combina ambos hechos en un grano común para evitar duplicación.

## 1. Crear el dataset

1. En **Dashboards → Create dashboard**, o la opción equivalente, crea
   **`DP-SEG-016 - DEV - Dashboard`**.
2. Elige el SQL Warehouse existente con el que validaste `workspace.s16`.
3. En **Data → Add SQL dataset**, pega únicamente el SELECT de
   [04-dataset-dashboard.sql](sql/04-dataset-dashboard.sql).
4. Nombra el dataset **Indicadores DP-SEG-016**. Debe mostrar **108 filas**.

No se pega el CREATE ni el INSERT en un dataset. Tampoco se importa el Excel
otra vez: se consulta la vista registrada. El procedimiento general está en
[crear un dashboard](https://docs.databricks.com/aws/en/dashboards/tutorials/create-dashboard).

## 2. Configurar visualizaciones

En **Canvas**, añade widgets con el mismo dataset. Selecciona explícitamente
la agregación **SUM** de cada medida:

| Tipo | Título | Campos | Control sin filtros |
| --- | --- | --- | ---: |
| Counter/KPI | Siniestros reportados | SUM(cantidad_siniestros) | 2328 |
| Counter/KPI | Pagado al corte (PEN) | SUM(monto_pagado) | 1546800.00 |
| Counter/KPI | Pólizas emitidas | SUM(cantidad_polizas_emitidas) | 23220 |
| Counter/KPI | Prima emitida (PEN) | SUM(prima_emitida) | 9846000.00 |
| Line | Siniestros por mes de reporte | X mes_referencia, orden por fecha; Y SUM(cantidad_siniestros) | 12 puntos; enero 150 |
| Bar | Pagado por tipo de seguro (PEN) | X tipo_seguro; Y SUM(monto_pagado) | AUTO lidera con 630600.00 |
| Table | Indicadores por canal | canal, SUM(cantidad_siniestros), SUM(cantidad_polizas_emitidas), SUM(prima_emitida) | Tres canales |

Agrega un texto visible:

> DP-SEG-016 · DEV · Datos sintéticos de 2025 · Corte 31/12/2025 · PEN.
> Mes de referencia: reporte para siniestros; emisión para pólizas.
> Los montos de siniestros son acumulados al corte. No representan pagos del mes.

Ordena fechas como fechas. Para validar, muestra montos completos con dos
decimales; después puedes abreviarlos. Las cantidades no son un recuento de
filas: cada fila contiene medidas agregadas.

## 3. Añadir filtros y comprobarlos

Añade tres filtros, todos vinculados a **Indicadores DP-SEG-016**:

- Tipo de seguro → `tipo_seguro`.
- Canal → `canal`.
- Mes de referencia → `mes_referencia`, tipo rango de fechas.

Comprueba que afecten a todos los widgets. Selecciona **AUTO**, **DIRECTO** y
el rango **01/01/2025–31/01/2025**. Aplica la selección si la UI lo requiere:

| Indicador | Resultado |
| --- | ---: |
| Siniestros | 25 |
| Pagado PEN | 20500.00 |
| Pólizas emitidas | 135 |
| Prima emitida PEN | 81000.00 |

Contrasta con Q6 de `03-validar-y-consultar.sql`. Limpia los filtros y comprueba
los totales anuales de nuevo. Todos los KPIs deben utilizar el mismo dataset;
no crees otro dataset de totales sin los campos de filtro.

## 4. Opcional: porcentaje de cierre

Si está disponible **Custom calculation → Calculated measure**, crea
`ratio_cierre` sobre el dataset:

```sql
SUM(cantidad_cerrados) / NULLIF(SUM(cantidad_siniestros), 0)
```

Utilízala en un KPI con formato **Percentage**, dos decimales: **76.03%** sin
filtros y **80.00%** para enero/AUTO/DIRECTO. El formato porcentual multiplica
por 100 para mostrarlo; no lo hagas también en la medida. No calcules promedio
de porcentajes por fila. Si la función no está disponible, usa Q3/Q6 como control.
Véase [cálculos de dashboards](https://docs.databricks.com/aws/en/dashboards/manage/data-modeling/custom-calculations).

## 5. Publicar y vincular Genie

1. Revisa cifras, títulos y ambiente. Publica para tu uso si la opción está
   disponible. Si no puedes publicar, conserva el borrador como evidencia.
2. Revisa las credenciales de publicación. Con permisos individuales se utiliza
   el acceso de cada lector; con permisos compartidos se usa el del publicador.
   No se exige compartir con otras cuentas para completar la clase.
3. Si está disponible **Settings → General → Enable Genie → Link existing
   Genie Agent**, vincula `DP-SEG-016 - DEV - Genie` y publica de nuevo.
4. Pregunta: «Para enero de 2025, AUTO y DIRECTO, ¿cuántos siniestros se
   reportaron y cuál fue el monto pagado al corte 31/12/2025?». Esperado:
   **25** y **PEN 20500.00**. Incluye los filtros en la pregunta, aunque estén
   seleccionados en el dashboard.

Las credenciales y la publicación se explican en
[compartir dashboards](https://docs.databricks.com/aws/en/dashboards/share/share).
Un Genie vinculado mantiene su propia configuración de permisos; los filtros
del dashboard no se transfieren a su chat. Si se genera un Genie automático,
su contexto procede de los datasets publicados y puede incluir columnas que
no se muestran en widgets. Véase
[Genie con dashboards](https://docs.databricks.com/aws/en/dashboards/genie-spaces).

## Problemas frecuentes y fallback

| Síntoma | Comprobación |
| --- | --- |
| Muestra 108 siniestros | Usar SUM(cantidad_siniestros), no COUNT(*) |
| Prima duplicada | Consumir vw_indicadores; evitar join directo entre hechos |
| KPI no responde al filtro | Revisar dataset, campo vinculado y alcance del filtro |
| Fechas en orden alfabético | Usar mes_referencia DATE como eje |
| Genie devuelve otro período | Incluir los filtros en la pregunta y revisar su SQL |
| Vista no encontrada | Comprobar workspace, catálogo, ambiente y ejecución de 00–02 |
| Cambió Excel, pero no el dashboard | Regenerar SQL, ejecutar 01 y refrescar el dataset; republicar cambios de diseño |

Si no está disponible el dashboard, ejecuta `04` en SQL Editor, crea una
visualización de línea y otra de barras y entrega el diseño de KPIs y filtros.
Si falta Genie, conserva el dashboard y valida las preguntas con SQL.

Fuentes oficiales consultadas el **11 de noviembre de 2026**.
