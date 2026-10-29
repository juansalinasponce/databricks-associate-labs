# Databricks notebook source
# ============================================================
# EVALUACIÓN 2 GUIADA - 04 VALIDACIÓN
# ============================================================

# COMMAND ----------
dbutils.widgets.text("catalog", "workspace")
catalog = dbutils.widgets.get("catalog")

silver_sin = f"{catalog}.silver.eval2_siniestros"
gold = f"{catalog}.gold.eval2_resumen_siniestros"

count_silver = spark.table(silver_sin).count()

duplicados = (
    spark.table(silver_sin)
    .groupBy("id_siniestro")
    .count()
    .filter("count > 1")
    .count()
)

count_gold = spark.table(gold).count()

print("Silver:", count_silver)
print("Duplicados:", duplicados)
print("Gold:", count_gold)

calidad_ok = (
    "OK"
    if duplicados == 0 and count_gold > 0
    else "ERROR"
)

dbutils.jobs.taskValues.set(
    key="calidad_ok",
    value=calidad_ok
)

print("calidad_ok:", calidad_ok)
display(spark.table(gold))
