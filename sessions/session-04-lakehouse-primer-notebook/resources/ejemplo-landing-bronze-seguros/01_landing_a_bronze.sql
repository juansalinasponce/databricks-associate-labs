-- Databricks notebook source
-- MAGIC %md
-- MAGIC # 01 — Crear Landing y Bronze con DDL
-- MAGIC
-- MAGIC **Sesión 04 — Lakehouse y primer notebook**
-- MAGIC
-- MAGIC Objetivo: crear la metadata de Bronze, cargar 10,000 pólizas desde
-- MAGIC Amazon S3 y comprobar dónde residen los datos y la metadata.
-- MAGIC
-- MAGIC Si su catálogo no se llama `workspace`, reemplace ese nombre antes de
-- MAGIC ejecutar el notebook.

-- COMMAND ----------

-- DBTITLE 1,1. Crear el schema Bronze
-- DDL: CREATE SCHEMA crea contenedores lógicos en Unity Catalog.
CREATE SCHEMA IF NOT EXISTS workspace.bronze
COMMENT 'Zona de tablas Delta con datos recibidos desde Amazon S3';

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Confirmar el archivo en Amazon S3
-- MAGIC
-- MAGIC El archivo se carga en S3 desde AWS CloudShell o una terminal autorizada,
-- MAGIC siguiendo el patrón utilizado en la Sesión 02:
-- MAGIC
-- MAGIC ```bash
-- MAGIC aws s3 cp data/polizas_2026_09_28.csv \
-- MAGIC   s3://<S3_BUCKET>/landing/polizas/
-- MAGIC ```
-- MAGIC
-- MAGIC Object URI esperada:
-- MAGIC
-- MAGIC `s3://<S3_BUCKET>/landing/polizas/polizas_2026_09_28.csv`
-- MAGIC
-- MAGIC No escriba Access Keys ni otros secretos en este notebook. El acceso a S3
-- MAGIC debe estar configurado previamente por el instructor mediante permisos
-- MAGIC autorizados de Unity Catalog e IAM.

-- COMMAND ----------

-- DBTITLE 1,2. Comprobar que el CSV reside en Landing de S3
-- Reemplace <S3_BUCKET> por el bucket utilizado en la Sesión 02.
LIST 's3://<S3_BUCKET>/landing/polizas/';

-- COMMAND ----------

-- DBTITLE 1,3. Crear la tabla y su metadata mediante DDL
-- CREATE OR REPLACE facilita repetir la práctica desde cero.
CREATE OR REPLACE TABLE workspace.bronze.polizas (
  id_poliza STRING COMMENT 'Identificador único de la póliza',
  id_asegurado STRING COMMENT 'Identificador del asegurado',
  id_producto STRING COMMENT 'Código del producto de seguros',
  fecha_inicio DATE COMMENT 'Fecha de inicio de vigencia',
  fecha_fin DATE COMMENT 'Fecha de fin de vigencia',
  estado_poliza STRING COMMENT 'Estado recibido de la póliza',
  prima DECIMAL(12, 2) COMMENT 'Importe de la prima',
  moneda STRING COMMENT 'Moneda de la prima',
  canal_venta STRING COMMENT 'Canal por el que se vendió la póliza',
  fecha_actualizacion TIMESTAMP COMMENT 'Fecha de actualización en el origen',
  _archivo_origen STRING COMMENT 'Nombre del objeto leído desde S3',
  _ruta_origen STRING COMMENT 'URI completa del objeto en S3',
  _fecha_ingesta TIMESTAMP COMMENT 'Fecha de carga en Bronze'
)
USING DELTA
COMMENT 'Pólizas cargadas desde Amazon S3 para consultas básicas'
TBLPROPERTIES (
  'quality' = 'bronze',
  'source.format' = 'csv',
  'source.system' = 'aseguradora_demo',
  'source.path' = 's3://<S3_BUCKET>/landing/polizas/'
);

-- COMMAND ----------

-- DBTITLE 1,4. Cargar las 10,000 filas desde S3
INSERT OVERWRITE workspace.bronze.polizas
SELECT
  id_poliza,
  id_asegurado,
  id_producto,
  to_date(fecha_inicio, 'yyyy-MM-dd') AS fecha_inicio,
  to_date(fecha_fin, 'yyyy-MM-dd') AS fecha_fin,
  estado_poliza,
  CAST(prima AS DECIMAL(12, 2)) AS prima,
  moneda,
  canal_venta,
  to_timestamp(fecha_actualizacion, 'yyyy-MM-dd HH:mm:ss') AS fecha_actualizacion,
  _metadata.file_name AS _archivo_origen,
  _metadata.file_path AS _ruta_origen,
  current_timestamp() AS _fecha_ingesta
FROM read_files(
  's3://<S3_BUCKET>/landing/polizas/polizas_2026_09_28.csv',
  format => 'csv',
  header => true,
  schema => 'id_poliza STRING, id_asegurado STRING, id_producto STRING, fecha_inicio STRING, fecha_fin STRING, estado_poliza STRING, prima STRING, moneda STRING, canal_venta STRING, fecha_actualizacion STRING'
);

-- COMMAND ----------

-- DBTITLE 1,5. Validar cantidad y muestra
SELECT COUNT(*) AS cantidad_registros
FROM workspace.bronze.polizas;

-- COMMAND ----------

SELECT *
FROM workspace.bronze.polizas
ORDER BY id_poliza
LIMIT 10;

-- COMMAND ----------

-- DBTITLE 1,6. Consultar la metadata de columnas
DESCRIBE TABLE workspace.bronze.polizas;

-- COMMAND ----------

-- DBTITLE 1,7. Consultar la metadata del schema
DESCRIBE SCHEMA EXTENDED workspace.bronze;

-- COMMAND ----------

-- DBTITLE 1,8. Consultar las propiedades de metadata
SHOW TBLPROPERTIES workspace.bronze.polizas;

-- COMMAND ----------

-- DBTITLE 1,9. Consultar formato y ubicación física
DESCRIBE DETAIL workspace.bronze.polizas;

-- COMMAND ----------

-- DBTITLE 1,10. Consultar metadata desde INFORMATION_SCHEMA
SELECT
  table_catalog,
  table_schema,
  table_name,
  table_type,
  data_source_format,
  storage_path,
  table_owner,
  comment
FROM workspace.information_schema.tables
WHERE table_schema = 'bronze'
  AND table_name = 'polizas';

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Interpretación
-- MAGIC
-- MAGIC - El CSV original está en `s3://<S3_BUCKET>/landing/polizas/`.
-- MAGIC - La tabla se consulta por su nombre lógico: `workspace.bronze.polizas`.
-- MAGIC - Unity Catalog conserva nombres, columnas, comentarios, propietario y permisos.
-- MAGIC - `DESCRIBE DETAIL` muestra `location`, donde están los archivos Delta.
-- MAGIC - Delta conserva su historial transaccional en `_delta_log`.
-- MAGIC - Las columnas que comienzan con `_` permiten rastrear la carga de cada fila.
