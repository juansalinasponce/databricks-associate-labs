-- Databricks notebook source
-- MAGIC %md
-- MAGIC # 01 — DDL de la tabla Delta Bronze
-- MAGIC
-- MAGIC DDL significa **Data Definition Language**. Se utiliza para crear y
-- MAGIC documentar objetos como schemas y tablas.
-- MAGIC
-- MAGIC En este laboratorio, Landing es únicamente el prefijo de Amazon S3 donde
-- MAGIC se carga manualmente el CSV. No se crea un schema ni una tabla Landing.
-- MAGIC El primer objeto registrado en Databricks pertenece a la capa Bronze.
-- MAGIC
-- MAGIC Antes de ejecutar, reemplace `<S3_BUCKET>` por el bucket autorizado.

-- COMMAND ----------

-- DBTITLE 1,1. Seleccionar el catálogo
-- USE CATALOG cambia el catálogo activo para las instrucciones posteriores.
-- Si su catálogo no se llama workspace, cambie el nombre en todo el laboratorio.
USE CATALOG workspace;

-- COMMAND ----------

-- DBTITLE 1,2. Crear el schema Bronze
-- CREATE SCHEMA IF NOT EXISTS crea el contenedor solo si todavía no existe.
CREATE SCHEMA IF NOT EXISTS bronze
COMMENT 'Primera capa Delta creada a partir de archivos cargados en Landing';

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Tabla Delta externa de Bronze
-- MAGIC
-- MAGIC `USING DELTA` establece el formato. `LOCATION` hace que los archivos
-- MAGIC físicos se materialicen en el prefijo Bronze de S3. El CSV original
-- MAGIC permanece en Landing y PySpark lo lee directamente por su ruta.

-- COMMAND ----------

-- DBTITLE 1,3. Crear la tabla Delta de destino
CREATE TABLE IF NOT EXISTS bronze.polizas (
  id_poliza STRING COMMENT 'Identificador único de la póliza',
  id_asegurado STRING COMMENT 'Identificador sintético del asegurado',
  id_producto STRING COMMENT 'Código normalizado del producto',
  fecha_inicio DATE COMMENT 'Fecha de inicio convertida a DATE',
  fecha_fin DATE COMMENT 'Fecha de fin convertida a DATE',
  estado_poliza STRING COMMENT 'Estado en mayúsculas y sin espacios laterales',
  prima DECIMAL(12, 2) COMMENT 'Importe de la prima convertido a número decimal',
  moneda STRING COMMENT 'Código de moneda normalizado',
  canal_venta STRING COMMENT 'Canal normalizado; SIN_INFORMACION cuando estaba vacío',
  departamento STRING COMMENT 'Departamento normalizado',
  fecha_actualizacion TIMESTAMP COMMENT 'Fecha de actualización convertida a TIMESTAMP',
  estado_vigencia STRING COMMENT 'Clasificación VIGENTE o NO_VIGENTE al 2026-09-30',
  segmento_prima STRING COMMENT 'Clasificación BAJA, MEDIA o ALTA',
  _archivo_origen STRING COMMENT 'Nombre del archivo CSV de Landing',
  _ruta_origen STRING COMMENT 'URI del archivo CSV de Landing',
  _fecha_proceso TIMESTAMP COMMENT 'Fecha y hora de ejecución del ETL'
)
USING DELTA
LOCATION 's3://<S3_BUCKET>/bronze/polizas_delta/'
COMMENT 'Pólizas convertidas de CSV a Delta mediante PySpark'
TBLPROPERTIES (
  'quality' = 'bronze',
  'source.format' = 'csv',
  'source.system' = 'aseguradora_demo',
  'source.path' = 's3://<S3_BUCKET>/landing/polizas/polizas_10000.csv',
  'delta.enableChangeDataFeed' = 'false'
);

-- COMMAND ----------

-- DBTITLE 1,4. Revisar columnas, tipos y comentarios
-- DESCRIBE TABLE muestra la definición lógica registrada en el catálogo.
DESCRIBE TABLE bronze.polizas;

-- COMMAND ----------

-- DBTITLE 1,5. Revisar formato y ubicación física
-- DESCRIBE DETAIL devuelve información técnica, incluida la propiedad location.
DESCRIBE DETAIL bronze.polizas;
