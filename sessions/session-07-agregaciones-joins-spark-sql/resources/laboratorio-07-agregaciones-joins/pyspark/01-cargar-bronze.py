# Paso 1 — Cargar archivos nuevos y detectar entregas pendientes.
# Ejecutar en un notebook Python de Databricks, despues del DDL 00.
from pyspark.sql import functions as F
from delta.tables import DeltaTable

# Fechas calculadas por Spark; no introducir una fecha manual.
display(spark.range(1).select(
    F.current_date().alias("fecha_servidor"),
    F.current_timestamp().alias("hora_servidor"),
))

# COPY INTO es una sentencia SQL de ingesta llamada desde Python.
# Conserva el historial de archivos y evita volver a cargar el mismo archivo.
# Las transformaciones posteriores utilizan la API de DataFrames.

spark.sql("""
COPY INTO workspace.bronze.s07_bronze_polizas
FROM (
  SELECT
    id_lote,
    id_poliza,
    id_asegurado,
    id_producto,
    fecha_inicio,
    fecha_fin,
    estado_poliza,
    prima,
    moneda,
    canal_venta,
    departamento,
    fecha_actualizacion,
    CURRENT_DATE() AS fecha_carga
  FROM '/Volumes/workspace/bronze/s07_archivos/polizas/'
)
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'false', 'nullValue' = '', 'mode' = 'FAILFAST')
COPY_OPTIONS ('force' = 'false', 'mergeSchema' = 'false');
""")

spark.sql("""
COPY INTO workspace.bronze.s07_bronze_productos
FROM (
  SELECT
    id_lote,
    id_producto,
    nombre_producto,
    tipo_seguro,
    segmento,
    fecha_actualizacion,
    CURRENT_DATE() AS fecha_carga
  FROM '/Volumes/workspace/bronze/s07_archivos/productos/'
)
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'false', 'nullValue' = '', 'mode' = 'FAILFAST')
COPY_OPTIONS ('force' = 'false', 'mergeSchema' = 'false');
""")

spark.sql("""
COPY INTO workspace.bronze.s07_bronze_siniestros
FROM (
  SELECT
    id_lote,
    id_siniestro,
    id_poliza,
    fecha_siniestro,
    fecha_reporte,
    estado_siniestro,
    monto_pagado,
    fecha_actualizacion,
    CURRENT_DATE() AS fecha_carga
  FROM '/Volumes/workspace/bronze/s07_archivos/siniestros/'
)
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'false', 'nullValue' = '', 'mode' = 'FAILFAST')
COPY_OPTIONS ('force' = 'false', 'mergeSchema' = 'false');
""")

# Las tres tablas contienen las entregas recibidas, con su fecha de carga.
polizas = spark.table("workspace.bronze.s07_bronze_polizas")
productos = spark.table("workspace.bronze.s07_bronze_productos")
siniestros = spark.table("workspace.bronze.s07_bronze_siniestros")
control = spark.table("workspace.bronze.s07_control_lotes")

recibidas = (
    polizas.select("id_lote", "fecha_carga")
    .unionByName(productos.select("id_lote", "fecha_carga"))
    .unionByName(siniestros.select("id_lote", "fecha_carga"))
    .join(control.select("id_lote"), "id_lote", "left_anti")
    .groupBy("id_lote")
    .agg(F.min("fecha_carga").alias("fecha_recepcion"))
)

# Insertar pendientes nuevas. Las anteriores permanecen hasta validar la carga.
(
    DeltaTable.forName(spark, "workspace.bronze.s07_entregas_pendientes")
    .alias("destino")
    .merge(recibidas.alias("origen"), "destino.id_lote = origen.id_lote")
    .whenNotMatchedInsertAll()
    .execute()
)
pendientes = spark.table("workspace.bronze.s07_entregas_pendientes")

# Cada entrega del laboratorio debe incluir al menos una fila de cada entidad.
if pendientes.join(polizas.select("id_lote"), "id_lote", "left_anti").limit(1).count():
    raise ValueError("Falta el archivo de polizas de una entrega pendiente")
if pendientes.join(productos.select("id_lote"), "id_lote", "left_anti").limit(1).count():
    raise ValueError("Falta el archivo de productos de una entrega pendiente")
if pendientes.join(siniestros.select("id_lote"), "id_lote", "left_anti").limit(1).count():
    raise ValueError("Falta el archivo de siniestros de una entrega pendiente")

display(pendientes.orderBy("id_lote"))
display(polizas.groupBy("id_lote", "fecha_carga").count().orderBy("id_lote"))
