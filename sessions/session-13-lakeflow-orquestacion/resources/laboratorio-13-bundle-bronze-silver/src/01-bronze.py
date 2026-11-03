# Databricks notebook source
# MAGIC %md
# MAGIC # 01 — Bronze: conservar el archivo recibido
# MAGIC Leemos seis pólizas sintéticas sin corregirlas y guardamos una tabla Delta.
# MAGIC El Job entrega los parámetros; los widgets también permiten ejecución manual.

# COMMAND ----------

import re
from pyspark.sql import functions as F

dbutils.widgets.text("catalog", "workspace")
dbutils.widgets.text("participante", "alumno01")
dbutils.widgets.dropdown("ambiente", "dev", ["dev", "prd"])

catalog = dbutils.widgets.get("catalog")
participante = dbutils.widgets.get("participante")
ambiente = dbutils.widgets.get("ambiente")

assert re.fullmatch(r"[a-z][a-z0-9_]*", participante), "Usa un identificador como alumno01."
assert ambiente in ("dev", "prd"), "Ambiente permitido: dev o prd."
assert re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", catalog), "Usa un catálogo de nombre simple."

schema = f"s13_{participante}_{ambiente}"
tabla_bronze = f"{catalog}.{schema}.bronze_polizas"
ruta_csv = f"/Volumes/{catalog}/{schema}/entrada/polizas.csv"
print(f"Ambiente: {ambiente} | Origen: {ruta_csv} | Destino: {tabla_bronze}")

# COMMAND ----------

# Todas las columnas de negocio entran como texto: la limpieza corresponde a Silver.
df_polizas = (
    spark.read
    .option("header", True)
    .schema("id_poliza STRING, estado_poliza STRING, prima STRING")
    .csv(ruta_csv)
    .withColumn("archivo_origen", F.lit(ruta_csv))
    .withColumn("fecha_ingesta", F.current_timestamp())
)

# Full Load de la muestra: una nueva ejecución reemplaza solo esta tabla del laboratorio.
df_polizas.write.format("delta").mode("overwrite").saveAsTable(tabla_bronze)

# COMMAND ----------

display(spark.table(tabla_bronze))
assert spark.table(tabla_bronze).count() == 6, "La muestra original debe contener seis filas."

# COMMAND ----------

# MAGIC %md
# MAGIC **Resultado:** seis filas, incluido un duplicado y una prima negativa.
# MAGIC En el trabajo diario esta capa permite revisar lo recibido antes de limpiarlo.
