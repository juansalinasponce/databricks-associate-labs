-- Databricks notebook source
-- MAGIC %md
-- MAGIC # Solución de referencia — uso exclusivo del instructor
-- MAGIC Fuente creada con las once columnas STRING. Sustituir workspace,
-- MAGIC default y p07 por el catálogo, schema e identificador asignados.
-- MAGIC Ejecutar cada celda en orden. La fuente no se modifica.

-- COMMAND ----------

USE CATALOG workspace;
USE SCHEMA default;

-- COMMAND ----------

DESCRIBE TABLE polizas_fuente_e1_p07;

-- COMMAND ----------

SELECT * FROM polizas_fuente_e1_p07 LIMIT 10;

-- COMMAND ----------

SELECT COUNT(*) AS filas_entrada FROM polizas_fuente_e1_p07;

-- COMMAND ----------

-- Vista de preparación en la sesión del notebook SQL.
-- La deduplicación se hace antes de añadir datos técnicos de una ejecución.
CREATE OR REPLACE TEMP VIEW polizas_tipos_e1 AS
SELECT DISTINCT
  id_poliza,
  id_asegurado,
  id_producto,
  CAST(fecha_inicio AS DATE) AS fecha_inicio,
  CAST(fecha_fin AS DATE) AS fecha_fin,
  UPPER(TRIM(estado_poliza)) AS estado_poliza,
  CAST(prima AS DECIMAL(12,2)) AS prima,
  UPPER(TRIM(moneda)) AS moneda,
  CASE
    WHEN canal_venta IS NULL OR TRIM(canal_venta) = '' THEN 'SIN_INFORMACION'
    ELSE UPPER(TRIM(canal_venta))
  END AS canal_venta,
  departamento,
  CAST(fecha_actualizacion AS TIMESTAMP) AS fecha_actualizacion
FROM polizas_fuente_e1_p07;

-- COMMAND ----------

-- El dataset solo contiene duplicados exactos, sin versiones conflictivas.
CREATE OR REPLACE TABLE polizas_preparadas_e1_p07
USING DELTA AS
SELECT
  *,
  CASE
    WHEN estado_poliza = 'ACTIVA'
      AND fecha_inicio <= DATE '2026-09-30'
      AND fecha_fin >= DATE '2026-09-30'
    THEN 'VIGENTE'
    ELSE 'NO_VIGENTE'
  END AS estado_vigencia
FROM polizas_tipos_e1;

-- COMMAND ----------

DESCRIBE TABLE polizas_preparadas_e1_p07;

-- COMMAND ----------

SELECT
  COUNT(*) AS filas_salida,
  COUNT(DISTINCT id_poliza) AS polizas_distintas,
  SUM(CASE WHEN canal_venta IS NULL OR TRIM(canal_venta) = '' THEN 1 ELSE 0 END)
    AS canales_faltantes
FROM polizas_preparadas_e1_p07;

-- COMMAND ----------

SELECT
  id_producto,
  moneda,
  COUNT(*) AS cantidad_polizas,
  ROUND(SUM(prima), 2) AS prima_total,
  ROUND(AVG(prima), 2) AS prima_promedio
FROM polizas_preparadas_e1_p07
WHERE estado_vigencia = 'VIGENTE'
GROUP BY id_producto, moneda
ORDER BY prima_total DESC, id_producto, moneda;

-- COMMAND ----------

-- Usar esta salida para el gráfico de barras: X producto, Y cantidad.
SELECT id_producto, COUNT(*) AS cantidad_polizas
FROM polizas_preparadas_e1_p07
WHERE estado_vigencia = 'VIGENTE' AND moneda = 'PEN'
GROUP BY id_producto
ORDER BY id_producto;

-- COMMAND ----------

SELECT id_producto, ROUND(SUM(prima), 2) AS prima_total_pen
FROM polizas_preparadas_e1_p07
WHERE estado_vigencia = 'VIGENTE' AND moneda = 'PEN'
GROUP BY id_producto
ORDER BY prima_total_pen DESC, id_producto
LIMIT 1;

-- COMMAND ----------

DESCRIBE DETAIL polizas_preparadas_e1_p07;
