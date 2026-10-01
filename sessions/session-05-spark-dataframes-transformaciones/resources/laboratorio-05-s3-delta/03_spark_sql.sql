-- Databricks notebook source
-- MAGIC %md
-- MAGIC # 03 — Módulo básico de Apache Spark SQL
-- MAGIC
-- MAGIC Requisito: ejecutar `01_ddl_tablas.sql` y `02_etl_pyspark.py`.
-- MAGIC Este módulo consulta la tabla Delta creada por el ETL.

-- COMMAND ----------

-- DBTITLE 1,1. Seleccionar catálogo y schema
-- USE CATALOG y USE SCHEMA establecen el contexto de las consultas.
USE CATALOG workspace;
USE SCHEMA bronze;

-- COMMAND ----------

-- DBTITLE 1,2. Revisar columnas y tipos
-- DESCRIBE TABLE muestra el schema y los comentarios definidos mediante DDL.
DESCRIBE TABLE polizas;

-- COMMAND ----------

-- DBTITLE 1,3. Mostrar una muestra
-- SELECT elige columnas; FROM indica la tabla; LIMIT restringe la cantidad.
SELECT
  id_poliza,
  id_producto,
  estado_poliza,
  prima,
  moneda
FROM polizas
LIMIT 20;

-- COMMAND ----------

-- DBTITLE 1,4. Contar registros y valores diferentes
-- COUNT(*) cuenta filas.
-- COUNT(DISTINCT columna) cuenta valores diferentes y excluye NULL.
SELECT
  COUNT(*) AS total_polizas,
  COUNT(DISTINCT id_poliza) AS polizas_distintas,
  COUNT(DISTINCT id_asegurado) AS asegurados_distintos
FROM polizas;

-- COMMAND ----------

-- DBTITLE 1,5. Filtrar con WHERE
-- WHERE conserva filas que cumplen la condición.
-- AND exige que ambas condiciones sean verdaderas.
-- ORDER BY ... DESC ordena desde el importe mayor hacia el menor.
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

-- DBTITLE 1,6. Filtrar una lista y un rango
-- IN comprueba si el valor está dentro de una lista.
-- BETWEEN incluye ambos extremos del rango de fechas.
SELECT
  id_poliza,
  id_producto,
  fecha_inicio,
  fecha_fin
FROM polizas
WHERE id_producto IN ('PROD-AUTO', 'PROD-HOGAR')
  AND fecha_inicio BETWEEN DATE '2025-01-01' AND DATE '2025-12-31'
ORDER BY fecha_inicio, id_poliza
LIMIT 50;

-- COMMAND ----------

-- DBTITLE 1,7. Crear una clasificación con CASE
-- CASE WHEN evalúa condiciones en orden y devuelve una categoría.
-- AS asigna un alias legible a la columna calculada.
SELECT
  id_poliza,
  prima,
  CASE
    WHEN prima < 1000 THEN 'BAJA'
    WHEN prima < 3000 THEN 'MEDIA'
    ELSE 'ALTA'
  END AS segmento_prima_calculado
FROM polizas
ORDER BY prima DESC
LIMIT 20;

-- COMMAND ----------

-- DBTITLE 1,8. Agrupar y calcular indicadores
-- GROUP BY forma un grupo por cada combinación de producto y moneda.
-- SUM suma la prima; AVG calcula el promedio; ROUND muestra dos decimales.
SELECT
  id_producto,
  moneda,
  COUNT(*) AS cantidad_polizas,
  ROUND(SUM(prima), 2) AS prima_total,
  ROUND(AVG(prima), 2) AS prima_promedio,
  MIN(prima) AS prima_minima,
  MAX(prima) AS prima_maxima
FROM polizas
GROUP BY id_producto, moneda
ORDER BY prima_total DESC;

-- COMMAND ----------

-- DBTITLE 1,9. Filtrar grupos con HAVING
-- HAVING filtra después de GROUP BY; WHERE filtra antes de agrupar.
SELECT
  canal_venta,
  COUNT(*) AS cantidad_polizas
FROM polizas
GROUP BY canal_venta
HAVING COUNT(*) >= 100
ORDER BY cantidad_polizas DESC;

-- COMMAND ----------

-- DBTITLE 1,10. Comprobar valores nulos
-- IS NULL busca ausencia de valor. El resultado esperado es cero porque el ETL
-- reemplazó los canales vacíos por SIN_INFORMACION.
SELECT COUNT(*) AS canales_nulos
FROM polizas
WHERE canal_venta IS NULL;

-- COMMAND ----------

-- DBTITLE 1,11. Crear una vista reutilizable
-- CREATE OR REPLACE VIEW guarda una consulta lógica; no duplica los datos Delta.
CREATE OR REPLACE VIEW vw_polizas_vigentes AS
SELECT
  id_poliza,
  id_asegurado,
  id_producto,
  prima,
  moneda,
  canal_venta,
  departamento
FROM polizas
WHERE estado_vigencia = 'VIGENTE';

-- COMMAND ----------

-- DBTITLE 1,12. Consultar la vista
SELECT
  departamento,
  COUNT(*) AS polizas_vigentes,
  ROUND(SUM(prima), 2) AS prima_total
FROM vw_polizas_vigentes
GROUP BY departamento
ORDER BY prima_total DESC;

-- COMMAND ----------

-- DBTITLE 1,13. Verificar ubicación física e historial Delta
-- DESCRIBE DETAIL muestra la location de S3 y el formato Delta.
DESCRIBE DETAIL polizas;

-- COMMAND ----------

-- DESCRIBE HISTORY lee el historial de transacciones guardado en _delta_log.
DESCRIBE HISTORY polizas;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Ejercicios para el participante
-- MAGIC
-- MAGIC 1. Cuente las pólizas por `estado_poliza`.
-- MAGIC 2. Calcule la prima promedio por `canal_venta`.
-- MAGIC 3. Muestre las pólizas `VIGENTE` cuya prima sea mayor que 2,500.
-- MAGIC 4. Identifique el producto con la mayor `prima_total`.
-- MAGIC 5. Compare `segmento_prima` con un `CASE` construido por usted.

-- COMMAND ----------

-- DBTITLE 1,14. Espacio para resolver
SELECT 'Reemplace esta consulta con su solución' AS instruccion;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Soluciones de referencia

-- COMMAND ----------

SELECT estado_poliza, COUNT(*) AS cantidad_polizas
FROM polizas
GROUP BY estado_poliza
ORDER BY cantidad_polizas DESC;

-- COMMAND ----------

SELECT canal_venta, ROUND(AVG(prima), 2) AS prima_promedio
FROM polizas
GROUP BY canal_venta
ORDER BY prima_promedio DESC;

-- COMMAND ----------

SELECT id_poliza, id_producto, prima
FROM polizas
WHERE estado_vigencia = 'VIGENTE'
  AND prima > 2500
ORDER BY prima DESC
LIMIT 50;

-- COMMAND ----------

SELECT id_producto, ROUND(SUM(prima), 2) AS prima_total
FROM polizas
GROUP BY id_producto
ORDER BY prima_total DESC
LIMIT 1;

-- COMMAND ----------

SELECT
  segmento_prima,
  CASE
    WHEN prima < 1000 THEN 'BAJA'
    WHEN prima < 3000 THEN 'MEDIA'
    ELSE 'ALTA'
  END AS segmento_recalculado,
  COUNT(*) AS cantidad
FROM polizas
GROUP BY
  segmento_prima,
  CASE
    WHEN prima < 1000 THEN 'BAJA'
    WHEN prima < 3000 THEN 'MEDIA'
    ELSE 'ALTA'
  END
ORDER BY segmento_prima;
