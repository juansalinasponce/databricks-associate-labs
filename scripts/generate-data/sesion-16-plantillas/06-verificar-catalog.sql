-- Databricks notebook source
-- {{CODIGO_DP}} | {{AMBIENTE}}. Ejecutar después de 00, 01 y 02.
-- Comprueba los objetos persistentes registrados en el catálogo del ambiente.

SHOW TABLES IN {{NAMESPACE}};

-- COMMAND ----------

-- Cada resultado debe mostrar Type=MANAGED y Provider=delta en Databricks.
DESCRIBE TABLE EXTENDED {{NAMESPACE}}.dim_fecha;
DESCRIBE TABLE EXTENDED {{NAMESPACE}}.dim_producto;
DESCRIBE TABLE EXTENDED {{NAMESPACE}}.dim_canal;
DESCRIBE TABLE EXTENDED {{NAMESPACE}}.dim_estado;
DESCRIBE TABLE EXTENDED {{NAMESPACE}}.fact_polizas;
DESCRIBE TABLE EXTENDED {{NAMESPACE}}.fact_siniestros;

-- COMMAND ----------

-- Comprueba que los hechos están poblados y que la vista de consumo responde.
-- Excel original: 108 grupos de pólizas y 216 grupos de siniestros.
SELECT 'fact_polizas' AS tabla, COUNT(*) AS filas FROM {{NAMESPACE}}.fact_polizas
UNION ALL
SELECT 'fact_siniestros', COUNT(*) FROM {{NAMESPACE}}.fact_siniestros;

SELECT codigo_dp, ambiente, mes_referencia, tipo_seguro, canal,
       cantidad_siniestros, monto_pagado
FROM {{NAMESPACE}}.vw_indicadores
ORDER BY mes_referencia, tipo_seguro, canal
LIMIT 10;
