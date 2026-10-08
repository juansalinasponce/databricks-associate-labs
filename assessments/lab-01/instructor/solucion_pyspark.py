# Databricks notebook source
# MAGIC %md
# MAGIC # Solución alternativa PySpark — instructor
# MAGIC Parte de la misma tabla fuente STRING. Reemplazar los nombres completos.
# MAGIC No ejecutar SQL y PySpark sobre la salida de un participante sin copia.

# COMMAND ----------

from pyspark.sql.functions import (
    avg, col, count, lit, round, sum, to_date, to_timestamp, trim, upper, when,
)

TABLA_FUENTE = "workspace.default.polizas_fuente_e1_p07"
TABLA_SALIDA = "workspace.default.polizas_preparadas_e1_p07"
FECHA_CORTE = "2026-09-30"

# COMMAND ----------

fuente_df = spark.table(TABLA_FUENTE)
display(fuente_df.limit(10))
fuente_df.printSchema()
print("Filas de entrada:", fuente_df.count())

# COMMAND ----------

preparadas_df = (
    fuente_df.dropDuplicates()
    .withColumn("estado_poliza", upper(trim(col("estado_poliza"))))
    .withColumn("moneda", upper(trim(col("moneda"))))
    .withColumn("canal_venta", upper(trim(col("canal_venta"))))
    .withColumn(
        "canal_venta",
        when(
            col("canal_venta").isNull() | (col("canal_venta") == lit("")),
            lit("SIN_INFORMACION"),
        ).otherwise(col("canal_venta")),
    )
    .withColumn("fecha_inicio", to_date(col("fecha_inicio"), "yyyy-MM-dd"))
    .withColumn("fecha_fin", to_date(col("fecha_fin"), "yyyy-MM-dd"))
    .withColumn("prima", col("prima").cast("decimal(12,2)"))
    .withColumn(
        "fecha_actualizacion",
        to_timestamp(col("fecha_actualizacion"), "yyyy-MM-dd HH:mm:ss"),
    )
    .withColumn(
        "estado_vigencia",
        when(
            (col("estado_poliza") == lit("ACTIVA"))
            & (col("fecha_inicio") <= to_date(lit(FECHA_CORTE)))
            & (col("fecha_fin") >= to_date(lit(FECHA_CORTE))),
            lit("VIGENTE"),
        ).otherwise(lit("NO_VIGENTE")),
    )
)

# COMMAND ----------

# Tabla administrada: no escribir archivos Delta dentro de un Volume.
preparadas_df.write.format("delta").mode("overwrite").saveAsTable(TABLA_SALIDA)
resultado_df = spark.table(TABLA_SALIDA)
resultado_df.printSchema()
print("Filas de salida:", resultado_df.count())
print(
    "Canales faltantes:",
    resultado_df.filter(col("canal_venta").isNull() | (trim(col("canal_venta")) == "")).count(),
)

# COMMAND ----------

vigentes_df = resultado_df.filter(col("estado_vigencia") == lit("VIGENTE"))
resumen_df = (
    vigentes_df.groupBy(col("id_producto"), col("moneda"))
    .agg(
        count(lit(1)).alias("cantidad_polizas"),
        round(sum(col("prima")), 2).alias("prima_total"),
        round(avg(col("prima")), 2).alias("prima_promedio"),
    )
    .orderBy(col("prima_total").desc(), col("id_producto"), col("moneda"))
)
display(resumen_df)

# COMMAND ----------

grafico_df = (
    vigentes_df.filter(col("moneda") == lit("PEN"))
    .groupBy(col("id_producto"))
    .agg(count(lit(1)).alias("cantidad_polizas"))
    .orderBy(col("id_producto"))
)
display(grafico_df)
# En la interfaz: barras, eje X id_producto, eje Y cantidad_polizas.
display(resumen_df.filter(col("moneda") == lit("PEN")).limit(1))
