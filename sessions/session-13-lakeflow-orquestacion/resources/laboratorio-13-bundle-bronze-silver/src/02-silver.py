# Databricks notebook source
# MAGIC %md
# MAGIC # 02 — Silver: preparar pólizas para consulta
# MAGIC Reutilizamos Bronze, estandarizamos el estado, tipificamos la prima,
# MAGIC excluimos la prima negativa y eliminamos el duplicado exacto de negocio.
# MAGIC La transformación se expresa en SQL.

# COMMAND ----------

import re

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
tabla_silver = f"{catalog}.{schema}.silver_polizas"
print(f"Ambiente: {ambiente} | Origen: {tabla_bronze} | Destino: {tabla_silver}")

# COMMAND ----------

spark.sql(f"""
    CREATE OR REPLACE TABLE {tabla_silver}
    USING DELTA
    COMMENT 'Pólizas sintéticas limpias para consulta. Laboratorio de la sesión 13.'
    AS
    SELECT DISTINCT
        TRIM(id_poliza) AS id_poliza,
        UPPER(TRIM(estado_poliza)) AS estado_poliza,
        CAST(prima AS DECIMAL(10, 2)) AS prima
    FROM {tabla_bronze}
    WHERE CAST(prima AS DECIMAL(10, 2)) >= 0
""")

# COMMAND ----------

display(spark.sql(f"SELECT * FROM {tabla_silver} ORDER BY id_poliza"))

resultado = spark.sql(f"""
    SELECT COUNT(*) AS filas, COUNT(DISTINCT id_poliza) AS polizas,
           SUM(prima) AS prima_total,
           SUM(CASE WHEN estado_poliza = 'ACTIVA' THEN 1 ELSE 0 END) AS activas
    FROM {tabla_silver}
""").first()

assert resultado.filas == resultado.polizas == 4, "Se esperan cuatro pólizas únicas."
assert resultado.prima_total == 3500, "La prima total esperada es 3500.00."
assert resultado.activas == 3, "Se esperan tres pólizas activas."
print("Validación correcta: 4 pólizas, 3 activas, prima total 3500.00.")

# COMMAND ----------

# MAGIC %md
# MAGIC **Aplicación diaria:** un analista consulta una tabla preparada sin repetir la limpieza.
# MAGIC `DISTINCT` alcanza para este duplicado exacto; cambios distintos para una misma póliza
# MAGIC necesitarían otra regla, por ejemplo conservar la actualización más reciente.
