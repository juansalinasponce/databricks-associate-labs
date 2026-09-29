-- Databricks notebook source
-- MAGIC %md
-- MAGIC # 02 — Consultas básicas con Databricks SQL
-- MAGIC
-- MAGIC Requisito: ejecutar primero `01_landing_a_bronze.sql`.

-- COMMAND ----------

-- DBTITLE 1,1. Seleccionar el catálogo y el schema
USE CATALOG workspace;
USE SCHEMA bronze;

-- COMMAND ----------

-- DBTITLE 1,2. Ver una muestra de datos
SELECT *
FROM polizas
LIMIT 20;

-- COMMAND ----------

-- DBTITLE 1,3. Contar todas las pólizas
SELECT COUNT(*) AS total_polizas
FROM polizas;

-- COMMAND ----------

-- DBTITLE 1,4. Filtrar pólizas activas en soles
SELECT
  id_poliza,
  id_producto,
  prima,
  canal_venta
FROM polizas
WHERE estado_poliza = 'ACTIVA'
  AND moneda = 'PEN'
ORDER BY prima DESC
LIMIT 20;

-- COMMAND ----------

-- DBTITLE 1,5. Contar pólizas por estado
SELECT
  estado_poliza,
  COUNT(*) AS cantidad_polizas
FROM polizas
GROUP BY estado_poliza
ORDER BY cantidad_polizas DESC;

-- COMMAND ----------

-- DBTITLE 1,6. Calcular indicadores por producto
SELECT
  id_producto,
  COUNT(*) AS cantidad_polizas,
  ROUND(SUM(prima), 2) AS prima_total,
  ROUND(AVG(prima), 2) AS prima_promedio
FROM polizas
GROUP BY id_producto
ORDER BY prima_total DESC;

-- COMMAND ----------

-- DBTITLE 1,7. Consultar un rango de fechas
SELECT
  id_poliza,
  fecha_inicio,
  fecha_fin,
  estado_poliza
FROM polizas
WHERE fecha_inicio BETWEEN DATE '2025-01-01' AND DATE '2025-03-31'
ORDER BY fecha_inicio, id_poliza
LIMIT 50;

-- COMMAND ----------

-- DBTITLE 1,8. Crear una clasificación con CASE
SELECT
  id_poliza,
  prima,
  CASE
    WHEN prima < 1000 THEN 'PRIMA BAJA'
    WHEN prima < 3000 THEN 'PRIMA MEDIA'
    ELSE 'PRIMA ALTA'
  END AS clasificacion_prima
FROM polizas
ORDER BY prima DESC
LIMIT 20;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Ejercicios
-- MAGIC
-- MAGIC 1. Contar las pólizas por `canal_venta`.
-- MAGIC 2. Mostrar solamente las pólizas del producto `PROD-AUTO`.
-- MAGIC 3. Calcular la prima promedio por `moneda`.
-- MAGIC 4. Encontrar la póliza con la prima más alta.

-- COMMAND ----------

-- DBTITLE 1,9. Espacio para resolver los ejercicios
SELECT 'Reemplace esta consulta con su solución' AS instruccion;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Soluciones de referencia

-- COMMAND ----------

SELECT canal_venta, COUNT(*) AS cantidad
FROM polizas
GROUP BY canal_venta
ORDER BY cantidad DESC;

-- COMMAND ----------

SELECT *
FROM polizas
WHERE id_producto = 'PROD-AUTO'
LIMIT 20;

-- COMMAND ----------

SELECT moneda, ROUND(AVG(prima), 2) AS prima_promedio
FROM polizas
GROUP BY moneda;

-- COMMAND ----------

SELECT id_poliza, prima
FROM polizas
ORDER BY prima DESC
LIMIT 1;
