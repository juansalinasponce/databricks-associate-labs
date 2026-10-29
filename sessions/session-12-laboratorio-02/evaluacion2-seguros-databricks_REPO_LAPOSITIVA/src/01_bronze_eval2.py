# Databricks notebook source
# ============================================================
# EVALUACIÓN 2 GUIADA - 01 BRONZE
# Volume -> Delta Bronze
# ============================================================

# COMMAND ----------
from pyspark.sql import functions as F
from pyspark.sql.types import *
import uuid

# Job parameters. Cuando se ejecuta manualmente, estos widgets
# también funcionan como valores por defecto.
dbutils.widgets.text("catalog", "workspace")
dbutils.widgets.text(
    "volume_base",
    "/Volumes/workspace/bronze/lapositiva/evaluacion2"
)

catalog = dbutils.widgets.get("catalog")
volume_base = dbutils.widgets.get("volume_base")
run_id = str(uuid.uuid4())

base_path = f"{volume_base}/siniestros/siniestros_eval2_base.csv"
inc_path = f"{volume_base}/siniestros/siniestros_eval2_incremental.csv"
pagos_path = f"{volume_base}/pagos/pagos_eval2.csv"

# COMMAND ----------
# Schemas

schema_siniestros_base = StructType([
    StructField("id_siniestro", StringType(), True),
    StructField("id_asegurado", StringType(), True),
    StructField("tipo_siniestro", StringType(), True),
    StructField("fecha_ocurrencia", DateType(), True),
    StructField("fecha_reporte", DateType(), True),
    StructField("estado_siniestro", StringType(), True),
    StructField("monto_reserva", DoubleType(), True),
    StructField("departamento", StringType(), True),
    StructField("canal_reporte", StringType(), True),
    StructField("fecha_actualizacion", TimestampType(), True),
])

schema_siniestros_incremental = StructType(
    schema_siniestros_base.fields + [
        StructField("prioridad", StringType(), True)
    ]
)

schema_pagos = StructType([
    StructField("id_pago", StringType(), True),
    StructField("id_siniestro", StringType(), True),
    StructField("fecha_pago", DateType(), True),
    StructField("monto_pago", DoubleType(), True),
    StructField("estado_pago", StringType(), True),
    StructField("medio_pago", StringType(), True),
])

# COMMAND ----------
def read_csv(path, schema):
    return (
        spark.read
        .option("header", True)
        .option("dateFormat", "yyyy-MM-dd")
        .option("timestampFormat", "yyyy-MM-dd HH:mm:ss")
        .schema(schema)
        .csv(path)
    )

def add_metadata(df, filename):
    return (
        df
        .withColumn("fecha_ingestion", F.current_timestamp())
        .withColumn("archivo_origen", F.lit(filename))
        .withColumn("id_ejecucion", F.lit(run_id))
    )

df_base = add_metadata(
    read_csv(base_path, schema_siniestros_base),
    "siniestros_eval2_base.csv"
)

df_inc = add_metadata(
    read_csv(inc_path, schema_siniestros_incremental),
    "siniestros_eval2_incremental.csv"
)

df_pagos = add_metadata(
    read_csv(pagos_path, schema_pagos),
    "pagos_eval2.csv"
)

# COMMAND ----------
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.bronze")

tables = {
    f"{catalog}.bronze.eval2_siniestros_base": df_base,
    f"{catalog}.bronze.eval2_siniestros_incremental": df_inc,
    f"{catalog}.bronze.eval2_pagos": df_pagos,
}

for table_name, df in tables.items():
    (
        df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(table_name)
    )
    print(f"{table_name}: {df.count()} filas")
    df.printSchema()

display(df_base.limit(10))
