-- Databricks notebook source
-- DP-SEG-016 | DEV. Ejecutar después de 00, 01 y 02.
-- Comprueba los objetos persistentes registrados en el catálogo del ambiente.

SHOW TABLES IN workspace.s16;

-- COMMAND ----------

-- Cada resultado debe mostrar Type=MANAGED y Provider=delta en Databricks.
DESCRIBE TABLE EXTENDED workspace.s16.dim_fecha;
DESCRIBE TABLE EXTENDED workspace.s16.dim_producto;
DESCRIBE TABLE EXTENDED workspace.s16.dim_canal;
DESCRIBE TABLE EXTENDED workspace.s16.dim_estado;
DESCRIBE TABLE EXTENDED workspace.s16.fact_polizas;
DESCRIBE TABLE EXTENDED workspace.s16.fact_siniestros;

-- COMMAND ----------

-- Comprueba que los hechos están poblados y que la vista de consumo responde.
-- Excel original: 108 grupos de pólizas y 216 grupos de siniestros.
SELECT 'fact_polizas' AS tabla, COUNT(*) AS filas FROM workspace.s16.fact_polizas
UNION ALL
SELECT 'fact_siniestros', COUNT(*) FROM workspace.s16.fact_siniestros;

SELECT codigo_dp, ambiente, mes_referencia, tipo_seguro, canal,
       cantidad_siniestros, monto_pagado
FROM workspace.s16.vw_indicadores
ORDER BY mes_referencia, tipo_seguro, canal
LIMIT 10;
