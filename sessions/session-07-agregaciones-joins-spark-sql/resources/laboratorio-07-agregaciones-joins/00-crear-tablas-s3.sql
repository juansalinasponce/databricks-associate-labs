-- 00 — Crear las tablas del laboratorio en S3
-- Ejecutar las sentencias en orden. Tablas en workspace.bronze.

-- Ejecutar directamente en SQL Editor. Preparacion unica del instructor.
USE CATALOG workspace;
CREATE SCHEMA IF NOT EXISTS workspace.bronze;
USE SCHEMA bronze;

-- El prefijo debe pertenecer a una External Location autorizada.
-- Este volumen contiene solo los CSV; las tablas Delta tienen otras ubicaciones.
CREATE EXTERNAL VOLUME IF NOT EXISTS workspace.bronze.s07_archivos
LOCATION 's3://<S3_BUCKET>/landing/sesion-07/'
COMMENT 'Archivos de seguros cargados desde Databricks';

DESCRIBE VOLUME workspace.bronze.s07_archivos;

CREATE TABLE IF NOT EXISTS workspace.bronze.s07_bronze_polizas (
  id_lote STRING,
  id_poliza STRING,
  id_asegurado STRING,
  id_producto STRING,
  fecha_inicio STRING,
  fecha_fin STRING,
  estado_poliza STRING,
  prima STRING,
  moneda STRING,
  canal_venta STRING,
  departamento STRING,
  fecha_actualizacion STRING,
  fecha_carga DATE
)
USING DELTA
LOCATION 's3://<S3_BUCKET>/bronze/sesion-07/s07_bronze_polizas/'
COMMENT 'Entregas originales; conserva versiones y duplicados de origen';

CREATE TABLE IF NOT EXISTS workspace.bronze.s07_bronze_productos (
  id_lote STRING,
  id_producto STRING,
  nombre_producto STRING,
  tipo_seguro STRING,
  segmento STRING,
  fecha_actualizacion STRING,
  fecha_carga DATE
)
USING DELTA
LOCATION 's3://<S3_BUCKET>/bronze/sesion-07/s07_bronze_productos/'
COMMENT 'Entregas originales; conserva versiones y duplicados de origen';

CREATE TABLE IF NOT EXISTS workspace.bronze.s07_bronze_siniestros (
  id_lote STRING,
  id_siniestro STRING,
  id_poliza STRING,
  fecha_siniestro STRING,
  fecha_reporte STRING,
  estado_siniestro STRING,
  monto_pagado STRING,
  fecha_actualizacion STRING,
  fecha_carga DATE
)
USING DELTA
LOCATION 's3://<S3_BUCKET>/bronze/sesion-07/s07_bronze_siniestros/'
COMMENT 'Entregas originales; conserva versiones y duplicados de origen';

CREATE TABLE IF NOT EXISTS workspace.bronze.s07_lote_polizas (
  id_lote STRING,
  id_poliza STRING,
  id_asegurado STRING,
  id_producto STRING,
  fecha_inicio DATE,
  fecha_fin DATE,
  estado_poliza STRING,
  prima DECIMAL(12,2),
  moneda STRING,
  canal_venta STRING,
  departamento STRING,
  fecha_actualizacion TIMESTAMP
)
USING DELTA
LOCATION 's3://<S3_BUCKET>/output/sesion-07/s07_lote_polizas/'
COMMENT 'Cambios limpios por lote; una fila por lote y clave';

CREATE TABLE IF NOT EXISTS workspace.bronze.s07_silver_polizas (
  id_lote STRING,
  id_poliza STRING,
  id_asegurado STRING,
  id_producto STRING,
  fecha_inicio DATE,
  fecha_fin DATE,
  estado_poliza STRING,
  prima DECIMAL(12,2),
  moneda STRING,
  canal_venta STRING,
  departamento STRING,
  fecha_actualizacion TIMESTAMP
)
USING DELTA
LOCATION 's3://<S3_BUCKET>/silver/sesion-07/s07_silver_polizas/'
COMMENT 'Estado vigente de cada clave; se actualiza con MERGE';

CREATE TABLE IF NOT EXISTS workspace.bronze.s07_lote_productos (
  id_lote STRING,
  id_producto STRING,
  nombre_producto STRING,
  tipo_seguro STRING,
  segmento STRING,
  fecha_actualizacion TIMESTAMP
)
USING DELTA
LOCATION 's3://<S3_BUCKET>/output/sesion-07/s07_lote_productos/'
COMMENT 'Cambios limpios por lote; una fila por lote y clave';

CREATE TABLE IF NOT EXISTS workspace.bronze.s07_silver_productos (
  id_lote STRING,
  id_producto STRING,
  nombre_producto STRING,
  tipo_seguro STRING,
  segmento STRING,
  fecha_actualizacion TIMESTAMP
)
USING DELTA
LOCATION 's3://<S3_BUCKET>/silver/sesion-07/s07_silver_productos/'
COMMENT 'Estado vigente de cada clave; se actualiza con MERGE';

CREATE TABLE IF NOT EXISTS workspace.bronze.s07_lote_siniestros (
  id_lote STRING,
  id_siniestro STRING,
  id_poliza STRING,
  fecha_siniestro DATE,
  fecha_reporte DATE,
  estado_siniestro STRING,
  monto_pagado DECIMAL(12,2),
  fecha_actualizacion TIMESTAMP
)
USING DELTA
LOCATION 's3://<S3_BUCKET>/output/sesion-07/s07_lote_siniestros/'
COMMENT 'Cambios limpios por lote; una fila por lote y clave';

CREATE TABLE IF NOT EXISTS workspace.bronze.s07_silver_siniestros (
  id_lote STRING,
  id_siniestro STRING,
  id_poliza STRING,
  fecha_siniestro DATE,
  fecha_reporte DATE,
  estado_siniestro STRING,
  monto_pagado DECIMAL(12,2),
  fecha_actualizacion TIMESTAMP
)
USING DELTA
LOCATION 's3://<S3_BUCKET>/silver/sesion-07/s07_silver_siniestros/'
COMMENT 'Estado vigente de cada clave; se actualiza con MERGE';

CREATE TABLE IF NOT EXISTS workspace.bronze.s07_productos_afectados (
  id_lote STRING,
  id_producto STRING
)
USING DELTA
LOCATION 's3://<S3_BUCKET>/output/sesion-07/s07_productos_afectados/'
COMMENT 'Productos que deben recalcularse para el lote';

CREATE TABLE IF NOT EXISTS workspace.bronze.s07_siniestros_por_poliza (
  id_poliza STRING,
  cantidad_siniestros BIGINT,
  siniestros_sin_monto BIGINT,
  monto_pagado_registrado DECIMAL(22,2)
)
USING DELTA
LOCATION 's3://<S3_BUCKET>/silver/sesion-07/s07_siniestros_por_poliza/'
COMMENT 'Resumen persistente de siniestros por poliza';

CREATE TABLE IF NOT EXISTS workspace.bronze.s07_gold_cartera (
  id_producto STRING,
  nombre_producto STRING,
  cantidad_polizas BIGINT,
  polizas_activas BIGINT,
  primas_informadas BIGINT,
  prima_total DECIMAL(22,2),
  prima_promedio DECIMAL(16,2),
  prima_minima DECIMAL(12,2),
  prima_maxima DECIMAL(12,2),
  siniestros_reportados BIGINT,
  siniestros_sin_monto BIGINT,
  monto_pagado_registrado DECIMAL(32,2)
)
USING DELTA
LOCATION 's3://<S3_BUCKET>/gold/sesion-07/s07_gold_cartera/'
COMMENT 'Indicadores vigentes; se actualizan solo los productos afectados';

CREATE TABLE IF NOT EXISTS workspace.bronze.s07_control_lotes (
  id_lote STRING,
  fecha_proceso TIMESTAMP
)
USING DELTA
LOCATION 's3://<S3_BUCKET>/output/sesion-07/s07_control_lotes/'
COMMENT 'Lotes con detalle e indicadores validados';

CREATE TABLE IF NOT EXISTS workspace.bronze.s07_entregas_pendientes (
  id_lote STRING,
  fecha_recepcion DATE
)
USING DELTA
LOCATION 's3://<S3_BUCKET>/output/sesion-07/s07_entregas_pendientes/'
COMMENT 'Entregas recibidas que aun deben completar sus transformaciones';

DESCRIBE DETAIL workspace.bronze.s07_bronze_polizas;
DESCRIBE DETAIL workspace.bronze.s07_silver_polizas;
DESCRIBE DETAIL workspace.bronze.s07_gold_cartera;
