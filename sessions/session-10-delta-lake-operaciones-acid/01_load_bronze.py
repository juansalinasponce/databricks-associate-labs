# Databricks notebook source
# ============================================================
# 01 - LANDING -> BRONZE
# ============================================================
#
# Lee directamente desde:
#
# /Volumes/workspace/bronze/s07_archivos/landing/
#
# y carga:
#
# workspace.bronze.polizas_medallion
# workspace.bronze.siniestros_medallion
#
# Además agrega columnas técnicas.
# ============================================================

# COMMAND ----------
# 1. CONFIGURACIÓN

from pyspark.sql import functions as F
from pyspark.sql.types import *
import uuid

LANDING = "/Volumes/workspace/bronze/s07_archivos/landing"

POLIZAS_FILE = f"{LANDING}/polizas_seguro.csv"
SINIESTROS_FILE = f"{LANDING}/siniestros_seguro.csv"

POLIZAS_TABLE = "workspace.bronze.polizas_medallion"
SINIESTROS_TABLE = "workspace.bronze.siniestros_medallion"

ID_EJECUCION = str(uuid.uuid4())
ORIGEN = "CORE_SEGUROS"

print("ID ejecución:", ID_EJECUCION)

# COMMAND ----------
# 2. SCHEMA DE PÓLIZAS

schema_polizas = StructType([
    StructField("id_poliza", StringType(), True),
    StructField("id_asegurado", StringType(), True),
    StructField("nro_documento", StringType(), True),
    StructField("nombre_asegurado", StringType(), True),
    StructField("producto", StringType(), True),
    StructField("plan", StringType(), True),
    StructField("prima_mensual", DecimalType(18,2), True),
    StructField("suma_asegurada", DecimalType(18,2), True),
    StructField("estado_poliza", StringType(), True),
    StructField("canal_venta", StringType(), True),
    StructField("departamento", StringType(), True),
    StructField("fecha_inicio_poliza", DateType(), True),
    StructField("fecha_fin_poliza", DateType(), True),
    StructField("fecha_actualizacion", TimestampType(), True)
])

# COMMAND ----------
# 3. LEER PÓLIZAS

df_polizas = (
    spark.read
    .option("header", True)
    .option("dateFormat", "yyyy-MM-dd")
    .option("timestampFormat", "yyyy-MM-dd HH:mm:ss")
    .schema(schema_polizas)
    .csv(POLIZAS_FILE)
)

# Columnas técnicas de Bronze.
df_polizas = (
    df_polizas
    .withColumn("fecha_ingestion", F.current_timestamp())
    .withColumn("origen_sistema", F.lit(ORIGEN))
    .withColumn("archivo_origen", F.lit("polizas_seguro.csv"))
    .withColumn("id_ejecucion", F.lit(ID_EJECUCION))
)

print("Pólizas leídas:", df_polizas.count())
display(df_polizas)

# COMMAND ----------
# 4. SCHEMA DE SINIESTROS

schema_siniestros = StructType([
    StructField("id_siniestro", StringType(), True),
    StructField("id_poliza", StringType(), True),
    StructField("tipo_siniestro", StringType(), True),
    StructField("fecha_ocurrencia", DateType(), True),
    StructField("fecha_reporte", DateType(), True),
    StructField("estado_siniestro", StringType(), True),
    StructField("monto_reserva", DecimalType(18,2), True),
    StructField("monto_pagado", DecimalType(18,2), True),
    StructField("canal_reporte", StringType(), True),
    StructField("ajustador", StringType(), True),
    StructField("fecha_actualizacion", TimestampType(), True)
])

# COMMAND ----------
# 5. LEER SINIESTROS

df_siniestros = (
    spark.read
    .option("header", True)
    .option("dateFormat", "yyyy-MM-dd")
    .option("timestampFormat", "yyyy-MM-dd HH:mm:ss")
    .schema(schema_siniestros)
    .csv(SINIESTROS_FILE)
)

df_siniestros = (
    df_siniestros
    .withColumn("fecha_ingestion", F.current_timestamp())
    .withColumn("origen_sistema", F.lit(ORIGEN))
    .withColumn("archivo_origen", F.lit("siniestros_seguro.csv"))
    .withColumn("id_ejecucion", F.lit(ID_EJECUCION))
)

print("Siniestros leídos:", df_siniestros.count())
display(df_siniestros)

# COMMAND ----------
# 6. CARGA BRONZE
#
# TRUNCATE + APPEND permite repetir el laboratorio
# sin duplicar la carga inicial.

spark.sql(f"TRUNCATE TABLE {POLIZAS_TABLE}")
spark.sql(f"TRUNCATE TABLE {SINIESTROS_TABLE}")

df_polizas.write.mode("append").saveAsTable(POLIZAS_TABLE)
df_siniestros.write.mode("append").saveAsTable(SINIESTROS_TABLE)

# COMMAND ----------
# 7. VALIDACIÓN

print("Bronze pólizas    :", spark.table(POLIZAS_TABLE).count())
print("Bronze siniestros :", spark.table(SINIESTROS_TABLE).count())

display(
    spark.sql(f"""
        SELECT id_poliza, estado_poliza, prima_mensual, fecha_actualizacion
        FROM {POLIZAS_TABLE}
        ORDER BY id_poliza, fecha_actualizacion
    """)
)
