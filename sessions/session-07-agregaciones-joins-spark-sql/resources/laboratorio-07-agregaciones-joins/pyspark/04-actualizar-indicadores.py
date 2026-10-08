# Paso 4 — Actualizar las tablas de indicadores de los productos afectados.
from pyspark.sql import functions as F
from delta.tables import DeltaTable

pendientes = spark.table("workspace.bronze.s07_entregas_pendientes").select("id_lote")
afectados = (
    spark.table("workspace.bronze.s07_productos_afectados")
    .join(pendientes, "id_lote", "left_semi")
    .select("id_producto").dropDuplicates()
)
polizas = spark.table("workspace.bronze.s07_silver_polizas")
productos = spark.table("workspace.bronze.s07_silver_productos")
siniestros = spark.table("workspace.bronze.s07_silver_siniestros")
polizas_afectadas = polizas.join(afectados, "id_producto", "left_semi")

# Primero resumir los siniestros por poliza. Asi el siguiente join no repite primas.
resumen_siniestros = (
    polizas_afectadas.select("id_poliza")
    .join(siniestros.select("id_poliza", "id_siniestro", "monto_pagado"), "id_poliza", "left")
    .groupBy("id_poliza")
    .agg(
        F.count("id_siniestro").alias("cantidad_siniestros"),
        (F.count("id_siniestro") - F.count("monto_pagado")).alias("siniestros_sin_monto"),
        F.coalesce(F.sum("monto_pagado"), F.lit(0)).cast("decimal(22,2)").alias("monto_pagado_registrado"),
    )
)
(
    DeltaTable.forName(spark, "workspace.bronze.s07_siniestros_por_poliza").alias("destino")
    .merge(resumen_siniestros.alias("origen"), "destino.id_poliza = origen.id_poliza")
    .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
)

# El catalogo tiene una fila por producto y el resumen una fila por poliza.
# Seleccionar solamente sus columnas utiles evita nombres duplicados.
cartera_afectada = (
    polizas_afectadas
    .join(productos.select("id_producto", "nombre_producto"), "id_producto", "left")
    .join(spark.table("workspace.bronze.s07_siniestros_por_poliza"), "id_poliza", "left")
    .withColumn("nombre_producto", F.coalesce("nombre_producto", F.lit("SIN_CATALOGO")))
)
indicadores = (
    cartera_afectada.groupBy("id_producto", "nombre_producto")
    .agg(
        F.count("id_poliza").alias("cantidad_polizas"),
        F.sum(F.when(F.col("estado_poliza") == "ACTIVA", 1).otherwise(0)).alias("polizas_activas"),
        F.count("prima").alias("primas_informadas"),
        F.coalesce(F.sum("prima"), F.lit(0)).cast("decimal(22,2)").alias("prima_total"),
        F.round(F.avg("prima"), 2).cast("decimal(16,2)").alias("prima_promedio"),
        F.min("prima").alias("prima_minima"),
        F.max("prima").alias("prima_maxima"),
        F.coalesce(F.sum("cantidad_siniestros"), F.lit(0)).alias("siniestros_reportados"),
        F.coalesce(F.sum("siniestros_sin_monto"), F.lit(0)).alias("siniestros_sin_monto"),
        F.coalesce(F.sum("monto_pagado_registrado"), F.lit(0)).cast("decimal(32,2)").alias("monto_pagado_registrado"),
    )
)
(
    DeltaTable.forName(spark, "workspace.bronze.s07_gold_cartera").alias("destino")
    .merge(indicadores.alias("origen"), "destino.id_producto = origen.id_producto")
    .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
)

# Si la ultima poliza sale de un producto, retirar solamente ese indicador.
productos_sin_cartera = afectados.join(polizas.select("id_producto"), "id_producto", "left_anti")
(
    DeltaTable.forName(spark, "workspace.bronze.s07_gold_cartera").alias("destino")
    .merge(productos_sin_cartera.alias("origen"), "destino.id_producto = origen.id_producto")
    .whenMatchedDelete().execute()
)

display(spark.table("workspace.bronze.s07_gold_cartera").orderBy("id_producto"))
