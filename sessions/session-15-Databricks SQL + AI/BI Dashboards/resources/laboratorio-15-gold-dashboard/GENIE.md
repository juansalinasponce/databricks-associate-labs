# Usar Genie para consultar Gold

En esta práctica se usan dos experiencias: **Genie Code** ayuda a escribir y
explicar SQL en el editor; **Ask Genie** permite hacer preguntas desde el
dashboard publicado cuando está habilitado. Se apoyan en los datos y permisos
del entorno: [experiencias de Genie](https://docs.databricks.com/aws/en/genie/).

## Genie Code en SQL Editor — actividad principal

1. Confirma que puedes consultar
   `workspace.gold_s15_seguros.vw_siniestros_negocio`.
2. En **SQL Editor**, selecciona el warehouse existente y abre el panel
   **Genie Code**. Adjunta la vista como contexto con el selector o `@` si aparece;
   incluye siempre su nombre completo en el prompt.
3. Envía el siguiente prompt. Pide mostrar el SQL antes de ejecutarlo.

```text
Genera una consulta Databricks SQL de solo lectura usando exclusivamente
workspace.gold_s15_seguros.vw_siniestros_negocio.
Quiero la cantidad de siniestros por mes de reporte durante 2025,
ordenada de enero a diciembre.
Cada fila ya es un resumen por mes, tipo de seguro y estado.
Usa SUM(cantidad_siniestros), no COUNT(*).
El campo mes_reporte es DATE. El corte del dataset es 2025-12-31.
No crees ni modifiques objetos. Muéstrame el SQL antes de ejecutarlo
y explica GROUP BY en una frase.
```

4. Revisa el nombre de la vista, las columnas, la agregación, el año y el orden.
   Comprueba que no use `CURRENT_DATE()` ni cambie datos.
5. Ejecuta la consulta revisada. Debe mostrar 12 meses: enero 150 y diciembre
   238. Compárala con la consulta 3 de `sql/02-consultas-y-validacion.sql`.
6. Conserva el prompt, el SQL y una explicación breve de por qué usaste `SUM`.

La ayuda integrada se documenta en
[SQL Editor y Genie Code](https://docs.databricks.com/aws/en/sql/user/sql-editor/).

**Segunda pregunta, si queda tiempo:**

```text
Usando solo workspace.gold_s15_seguros.vw_siniestros_negocio,
muestra el monto pagado acumulado al corte por tipo_seguro para los
siniestros reportados en 2025. Usa SUM(monto_pagado), moneda PEN,
y orden descendente. Genera solo SELECT y explica el resultado.
```

Control: AUTO 630600.00, HOGAR 477900.00, SALUD 438300.00. Contrasta con la
consulta 4 del archivo `02`.

## Ayuda para armar el dashboard — opcional

Después de crear el dataset manualmente, puedes abrir Genie Code en el
dashboard y pedir:

```text
Usa el dataset existente Siniestros Negocio basado en
workspace.gold_s15_seguros.vw_siniestros_negocio.
Añade tres indicadores: SUM(cantidad_siniestros), SUM(monto_pagado)
y SUM(monto_reservado), una línea de cantidad por mes_reporte y
barras de monto_pagado por tipo_seguro. Montos en PEN.
Añade filtros de tipo_seguro y mes_reporte para todos los widgets.
Mantén un único dataset y muestra el corte 2025-12-31 en un texto.
No modifiques la tabla ni la vista. No publiques ni compartas todavía.
```

Comprueba cada agregación y el filtro enero/AUTO con la guía manual. Si falta
esta asistencia, continúa con [DASHBOARD.md](DASHBOARD.md). Las capacidades
dependen del entorno:
[Genie Code para dashboards](https://docs.databricks.com/aws/en/dashboards/manage/dashboard-agent).

## Ask Genie en el dashboard publicado — cierre condicionado al entorno

Limpia los filtros, abre **Ask Genie** y formula preguntas con año y corte
explícitos. Las cifras siguientes corresponden al dataset completo:

| Pregunta | Control SQL | Resultado esperado |
| --- | --- | --- |
| ¿Cuántos siniestros se reportaron en 2025? Suma cantidad_siniestros. | Consulta 2 | 2328 |
| ¿Cuál es el monto pagado acumulado al corte por tipo de seguro para los reportados en 2025? | Consulta 4 | AUTO: PEN 630600, el mayor |
| ¿Cuántos están abiertos y cerrados al 31/12/2025? | Consulta 5 | 558 y 1770 |
| Para los reportados en enero de 2025 de AUTO, ¿cuál es la cantidad, el monto pagado y el porcentaje de cierre al corte? | Consulta 6 | 50; PEN 41000; 80.00% |

Si preguntas por cierre, especifica que la fórmula es
`100.0 * SUM(cantidad_cerrados) / SUM(cantidad_siniestros)`.
No supongas que los filtros actuales de una visual coinciden con el alcance
de la respuesta: comprueba el período y tipo que Genie utilizó.

En cada respuesta, expande el SQL o los detalles de consulta si la interfaz los
ofrece. Revisa fuente, filtros y sumas; ejecuta el SQL de control en SQL Editor.
Si no muestra SQL, registra esa limitación y conserva la comparación numérica.
Una explicación de IA no es evidencia suficiente para publicar un KPI.

El Genie generado junto al dashboard utiliza su contexto publicado; no se
requiere editar instrucciones de un agente automático ni crear otro recurso.
La disponibilidad y el modo de acceso están descritos en
[Genie asociado a dashboards](https://docs.databricks.com/aws/en/dashboards/genie-spaces).

## Si Genie no está disponible

Lee un prompt, escribe o utiliza la consulta equivalente de `02` y justifica
su agregación. Conserva las mismas preguntas y resultados esperados, indicando
**simulación sin Genie**. No se exige cambiar a otra edición de Databricks.

Fuentes oficiales consultadas el **9 de noviembre de 2026**.
