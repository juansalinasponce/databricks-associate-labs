# Databricks notebook source
# ============================================================
# EVALUACIÓN 2 GUIADA - 02 SILVER + MERGE
# Window + limpieza + schema evolution + idempotencia
# ============================================================

# COMMAND ----------
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from delta.tables import DeltaTable
import uuid

dbutils.widgets.text("catalog", "workspace")
dbutils.widgets.text(
    "volume_base",
    "/Volumes/workspace/bronze/lapositiva/evaluacion2"
)

catalog = dbutils.widgets.get("catalog")
run_id = str(uuid.uuid4())

BASE = f"{catalog}.bronze.eval2_siniestros_base"
INC = f"{catalog}.bronze.eval2_siniestros_incremental"
PAGOS = f"{catalog}.bronze.eval2_pagos"

SILVER_SIN = f"{catalog}.silver.eval2_siniestros"
SILVER_PAGOS = f"{catalog}.silver.eval2_pagos"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.silver")

# COMMAND ----------
# 1. Última versión del histórico por id_siniestro

w = (
    Window
    .partitionBy("id_siniestro")
    .orderBy(F.col("fecha_actualizacion").desc())
)

base_latest = (
    spark.table(BASE)
    .withColumn("rn", F.row_number().over(w))
    .filter(F.col("rn") == 1)
    .drop("rn")
    .withColumn("fecha_procesamiento", F.current_timestamp())
    .withColumn("id_ejecucion_silver", F.lit(run_id))
)

(
    base_latest.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(SILVER_SIN)
)

print("Silver inicial:", spark.table(SILVER_SIN).count())

# COMMAND ----------
# 2. Deduplicar lote incremental

inc_latest = (
    spark.table(INC)
    .withColumn("rn", F.row_number().over(w))
    .filter(F.col("rn") == 1)
    .drop("rn")
    .withColumn("fecha_procesamiento", F.current_timestamp())
    .withColumn("id_ejecucion_silver", F.lit(run_id))
)

# COMMAND ----------
# 3. MERGE / UPSERT con evolución de schema
# La columna prioridad llega solamente en el incremental.

target = DeltaTable.forName(spark, SILVER_SIN)

def ejecutar_merge():
    (
        target.alias("target")
        .merge(
            inc_latest.alias("source"),
            "target.id_siniestro = source.id_siniestro"
        )
        .withSchemaEvolution()
        .whenMatchedUpdateAll(
            condition=(
                "source.fecha_actualizacion > "
                "target.fecha_actualizacion"
            )
        )
        .whenNotMatchedInsertAll()
        .execute()
    )

ejecutar_merge()
count_1 = spark.table(SILVER_SIN).count()

# Segunda ejecución: mismo lote, mismo resultado.
ejecutar_merge()
count_2 = spark.table(SILVER_SIN).count()

print("Después del MERGE 1:", count_1)
print("Después del MERGE 2:", count_2)
print("Idempotencia OK:", count_1 == count_2)

# COMMAND ----------
# 4. Limpieza de pagos

pagos = (
    spark.table(PAGOS)
    .dropDuplicates(["id_pago"])
    .withColumn(
        "monto_pago",
        F.coalesce(F.col("monto_pago").cast("double"), F.lit(0.0))
    )
    .withColumn(
        "medio_pago",
        F.when(
            F.col("medio_pago").isNull() | (F.trim(F.col("medio_pago")) == ""),
            F.lit("NO_INFORMADO")
        ).otherwise(F.col("medio_pago"))
    )
    .withColumn("fecha_procesamiento", F.current_timestamp())
    .withColumn("id_ejecucion_silver", F.lit(run_id))
)

(
    pagos.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(SILVER_PAGOS)
)

# COMMAND ----------
duplicados = (
    spark.table(SILVER_SIN)
    .groupBy("id_siniestro")
    .count()
    .filter("count > 1")
    .count()
)

print("Silver siniestros:", spark.table(SILVER_SIN).count())
print("Duplicados:", duplicados)
print("Silver pagos:", spark.table(SILVER_PAGOS).count())

spark.table(SILVER_SIN).printSchema()
display(spark.table(SILVER_SIN).orderBy("id_siniestro"))
