-- Databricks notebook source
-- MAGIC %md
-- MAGIC # Consultar la vista y contrastar las respuestas de Genie
-- MAGIC Ejecuta como analista o propietario. Sustituye `workspace` si corresponde.
-- MAGIC Cada bloque SELECT es independiente. El dashboard usa SOLO la consulta 1 como dataset.

-- COMMAND ----------

-- 1. Dataset del dashboard: Siniestros Negocio. Conserva campos para los filtros.
SELECT mes_reporte, tipo_seguro, estado_siniestro,
       cantidad_siniestros, monto_pagado, monto_reservado,
       cantidad_cerrados, fecha_corte
FROM workspace.gold_s15_seguros.vw_siniestros_negocio;

-- COMMAND ----------

-- 2. KPIs anuales: contar filas no equivale a contar siniestros.
SELECT SUM(cantidad_siniestros) AS total_siniestros,
       SUM(cantidad_cerrados) AS siniestros_cerrados,
       SUM(cantidad_siniestros) - SUM(cantidad_cerrados) AS siniestros_abiertos,
       SUM(monto_pagado) AS monto_pagado_pen,
       SUM(monto_reservado) AS monto_reservado_pen,
       ROUND(100.0 * SUM(cantidad_cerrados)
             / NULLIF(SUM(cantidad_siniestros), 0), 2) AS porcentaje_cierre
FROM workspace.gold_s15_seguros.vw_siniestros_negocio;
-- Esperado: 2328 | 1770 | 558 | 1546800.00 | 946800.00 | 76.03

-- COMMAND ----------

-- 3. Linea: siniestros por mes de reporte. No es una serie de pagos por fecha de pago.
SELECT mes_reporte, SUM(cantidad_siniestros) AS total_siniestros
FROM workspace.gold_s15_seguros.vw_siniestros_negocio
GROUP BY mes_reporte
ORDER BY mes_reporte;
-- 12 puntos: enero 150, febrero 158, ..., diciembre 238.

-- COMMAND ----------

-- 4. Barras: monto pagado por tipo de seguro, acumulado al corte.
SELECT tipo_seguro, SUM(monto_pagado) AS monto_pagado_pen
FROM workspace.gold_s15_seguros.vw_siniestros_negocio
GROUP BY tipo_seguro
ORDER BY monto_pagado_pen DESC;
-- AUTO 630600.00 | HOGAR 477900.00 | SALUD 438300.00

-- COMMAND ----------

-- 5. Tabla o donut: cantidad por estado al corte.
SELECT estado_siniestro, SUM(cantidad_siniestros) AS total_siniestros
FROM workspace.gold_s15_seguros.vw_siniestros_negocio
GROUP BY estado_siniestro
ORDER BY estado_siniestro;
-- ABIERTO 558 | CERRADO 1770

-- COMMAND ----------

-- 6. Control del filtro del dashboard: enero y AUTO.
SELECT SUM(cantidad_siniestros) AS total_siniestros,
       SUM(monto_pagado) AS monto_pagado_pen,
       SUM(monto_reservado) AS monto_reservado_pen,
       ROUND(100.0 * SUM(cantidad_cerrados)
             / NULLIF(SUM(cantidad_siniestros), 0), 2) AS porcentaje_cierre
FROM workspace.gold_s15_seguros.vw_siniestros_negocio
WHERE mes_reporte = DATE '2025-01-01'
  AND tipo_seguro = 'AUTO';
-- Esperado: 50 | 41000.00 | 20000.00 | 80.00

-- COMMAND ----------

-- 7. La clave de agregacion debe ser unica. Esperado: ninguna fila.
SELECT mes_reporte, tipo_seguro, estado_siniestro, COUNT(*) AS filas
FROM workspace.gold_s15_seguros.vw_siniestros_negocio
GROUP BY mes_reporte, tipo_seguro, estado_siniestro
HAVING COUNT(*) > 1;

-- COMMAND ----------

-- 8. Reglas basicas de los indicadores. Esperado: 0.
SELECT COUNT(*) AS filas_invalidas
FROM workspace.gold_s15_seguros.vw_siniestros_negocio
WHERE mes_reporte IS NULL OR tipo_seguro IS NULL OR estado_siniestro IS NULL
   OR cantidad_siniestros IS NULL OR monto_pagado IS NULL OR monto_reservado IS NULL
   OR cantidad_siniestros < 0 OR monto_pagado < 0 OR monto_reservado < 0
   OR tipo_seguro NOT IN ('AUTO', 'SALUD', 'HOGAR')
   OR estado_siniestro NOT IN ('ABIERTO', 'CERRADO')
   OR (estado_siniestro = 'CERRADO' AND monto_reservado <> 0);
