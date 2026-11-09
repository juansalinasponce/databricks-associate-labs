-- Databricks notebook source
-- MAGIC %md
-- MAGIC # Publicar una vista de negocio
-- MAGIC Ejecuta como cuenta principal despues de 00. Sustituye `workspace` si corresponde.
-- MAGIC La vista conserva la granularidad; no almacena otra copia de las 72 filas.

-- COMMAND ----------

CREATE VIEW workspace.gold_s15_seguros.vw_siniestros_negocio AS
SELECT mes_reporte,
       tipo_seguro,
       estado_siniestro,
       cantidad_siniestros,
       monto_pagado,
       monto_reservado,
       CASE WHEN estado_siniestro = 'CERRADO'
            THEN cantidad_siniestros ELSE 0 END AS cantidad_cerrados,
       DATE '2025-12-31' AS fecha_corte
FROM workspace.gold_s15_seguros.siniestros_mensuales;

-- COMMAND ----------

COMMENT ON TABLE workspace.gold_s15_seguros.vw_siniestros_negocio IS
'Indicadores sinteticos para dashboard. Reportados en 2025, estado y montos acumulados al corte 2025-12-31, moneda PEN. Una fila por mes de reporte, tipo de seguro y estado. Sumar cantidad_siniestros, no contar filas. Cierre: SUM(cantidad_cerrados)/SUM(cantidad_siniestros). Fuente: siniestros_mensuales. Owner de negocio ficticio: Operaciones demo. Carga estatica de entrenamiento.';

-- COMMAND ----------

SELECT *
FROM workspace.gold_s15_seguros.vw_siniestros_negocio
ORDER BY mes_reporte, tipo_seguro, estado_siniestro;
-- Esperado: 72 filas; cantidad_cerrados es 0 para ABIERTO.
