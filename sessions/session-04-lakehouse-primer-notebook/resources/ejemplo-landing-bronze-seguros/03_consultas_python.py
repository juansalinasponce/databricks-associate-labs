# Databricks notebook source
# MAGIC %md
# MAGIC # 03 — Primer notebook con Python y PySpark
# MAGIC
# MAGIC Requisito: ejecutar primero `01_landing_a_bronze.sql`.
# MAGIC
# MAGIC El objetivo no es aprender programación avanzada. Se utilizará Python para
# MAGIC leer una tabla, mostrar filas, filtrar y agrupar.

# COMMAND ----------

# DBTITLE 1,1. Leer la tabla Bronze
polizas_df = spark.table("workspace.bronze.polizas")

# COMMAND ----------

# DBTITLE 1,2. Mostrar diez registros
display(polizas_df.limit(10))

# COMMAND ----------

# DBTITLE 1,3. Contar registros
total_polizas = polizas_df.count()
print(f"Total de pólizas: {total_polizas}")

# COMMAND ----------

# DBTITLE 1,4. Revisar las columnas y tipos definidos por el DDL
polizas_df.printSchema()

# COMMAND ----------

# DBTITLE 1,5. Seleccionar algunas columnas
columnas_basicas_df = polizas_df.select(
    "id_poliza",
    "id_producto",
    "estado_poliza",
    "prima",
)

display(columnas_basicas_df.limit(20))

# COMMAND ----------

# DBTITLE 1,6. Filtrar pólizas activas
from pyspark.sql.functions import col

polizas_activas_df = polizas_df.filter(col("estado_poliza") == "ACTIVA")
display(polizas_activas_df.limit(20))

# COMMAND ----------

# DBTITLE 1,7. Contar pólizas por estado
resumen_estados_df = (
    polizas_df
    .groupBy("estado_poliza")
    .count()
    .orderBy(col("count").desc())
)

display(resumen_estados_df)

# COMMAND ----------

# DBTITLE 1,8. Calcular prima promedio por producto
from pyspark.sql.functions import avg, round

resumen_productos_df = (
    polizas_df
    .groupBy("id_producto")
    .agg(round(avg("prima"), 2).alias("prima_promedio"))
    .orderBy("id_producto")
)

display(resumen_productos_df)

# COMMAND ----------

# DBTITLE 1,9. Combinar Python con SQL
polizas_df.createOrReplaceTempView("polizas_temporal")

resultado_sql_df = spark.sql("""
    SELECT
      canal_venta,
      COUNT(*) AS cantidad_polizas
    FROM polizas_temporal
    GROUP BY canal_venta
    ORDER BY cantidad_polizas DESC
""")

display(resultado_sql_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Ejercicios
# MAGIC
# MAGIC 1. Filtre las pólizas cuya moneda sea `USD`.
# MAGIC 2. Cuente las pólizas por `canal_venta` usando PySpark.
# MAGIC 3. Muestre `id_poliza`, `id_producto` y `prima` para `PROD-VIDA`.

# COMMAND ----------

# DBTITLE 1,10. Espacio para el participante
# Ejemplo para comenzar:
# polizas_usd_df = polizas_df.filter(col("moneda") == "USD")
# display(polizas_usd_df.limit(20))
