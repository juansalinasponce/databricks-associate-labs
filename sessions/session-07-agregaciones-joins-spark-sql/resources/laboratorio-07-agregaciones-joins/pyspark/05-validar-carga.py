# Paso 5 — Validar antes de registrar la entrega como procesada.
from pyspark.sql import functions as F
from delta.tables import DeltaTable

pendientes = spark.table("workspace.bronze.s07_entregas_pendientes").select("id_lote")
polizas = spark.table("workspace.bronze.s07_silver_polizas")
productos = spark.table("workspace.bronze.s07_silver_productos")
siniestros = spark.table("workspace.bronze.s07_silver_siniestros")
gold = spark.table("workspace.bronze.s07_gold_cartera")
resumen = spark.table("workspace.bronze.s07_siniestros_por_poliza")

# Comprobar que las versiones recibidas ya existen o fueron superadas en Silver.
polizas_sin_aplicar = (
    spark.table("workspace.bronze.s07_bronze_polizas").join(pendientes, "id_lote", "left_semi").alias("origen")
    .join(polizas.alias("destino"),
          (F.col("origen.id_poliza") == F.col("destino.id_poliza")) &
          (F.col("origen.fecha_actualizacion").cast("timestamp") <= F.col("destino.fecha_actualizacion")),
          "left_anti")
)
if polizas_sin_aplicar.limit(1).count():
    raise ValueError("Falta aplicar cambios de polizas")
productos_sin_aplicar = (
    spark.table("workspace.bronze.s07_bronze_productos").join(pendientes, "id_lote", "left_semi").alias("origen")
    .join(productos.alias("destino"),
          (F.col("origen.id_producto") == F.col("destino.id_producto")) &
          (F.col("origen.fecha_actualizacion").cast("timestamp") <= F.col("destino.fecha_actualizacion")),
          "left_anti")
)
if productos_sin_aplicar.limit(1).count():
    raise ValueError("Falta aplicar cambios de productos")
siniestros_sin_aplicar = (
    spark.table("workspace.bronze.s07_bronze_siniestros").join(pendientes, "id_lote", "left_semi").alias("origen")
    .join(siniestros.alias("destino"),
          (F.col("origen.id_siniestro") == F.col("destino.id_siniestro")) &
          (F.col("origen.fecha_actualizacion").cast("timestamp") <= F.col("destino.fecha_actualizacion")),
          "left_anti")
)
if siniestros_sin_aplicar.limit(1).count():
    raise ValueError("Falta aplicar cambios de siniestros")

# Una fila por clave en las tablas vigentes.
if polizas.groupBy("id_poliza").count().filter("count > 1").limit(1).count():
    raise ValueError("Polizas duplicadas en Silver")
if productos.groupBy("id_producto").count().filter("count > 1").limit(1).count():
    raise ValueError("Productos duplicados en Silver")
if siniestros.groupBy("id_siniestro").count().filter("count > 1").limit(1).count():
    raise ValueError("Siniestros duplicados en Silver")
if gold.groupBy("id_producto").count().filter("count > 1").limit(1).count():
    raise ValueError("Productos duplicados en Gold")
if resumen.groupBy("id_poliza").count().filter("count > 1").limit(1).count():
    raise ValueError("Polizas duplicadas en el resumen de siniestros")

# first() devuelve una sola fila con los totales, no todos los registros.
totales_polizas = polizas.agg(
    F.count("id_poliza").alias("cantidad"),
    F.coalesce(F.sum(F.when(F.col("estado_poliza") == "ACTIVA", 1).otherwise(0)), F.lit(0)).alias("activas"),
    F.count("prima").alias("informadas"),
    F.coalesce(F.sum("prima"), F.lit(0)).alias("prima"),
).first()
totales_gold = gold.agg(
    F.coalesce(F.sum("cantidad_polizas"), F.lit(0)).alias("cantidad"),
    F.coalesce(F.sum("polizas_activas"), F.lit(0)).alias("activas"),
    F.coalesce(F.sum("primas_informadas"), F.lit(0)).alias("informadas"),
    F.coalesce(F.sum("prima_total"), F.lit(0)).alias("prima"),
    F.coalesce(F.sum("siniestros_reportados"), F.lit(0)).alias("siniestros"),
    F.coalesce(F.sum("siniestros_sin_monto"), F.lit(0)).alias("sin_monto"),
    F.coalesce(F.sum("monto_pagado_registrado"), F.lit(0)).alias("pagado"),
).first()
if totales_polizas.cantidad != totales_gold.cantidad:
    raise ValueError("Revisar cantidad de polizas en Gold")
if totales_polizas.activas != totales_gold.activas:
    raise ValueError("Revisar polizas activas en Gold")
if totales_polizas.informadas != totales_gold.informadas:
    raise ValueError("Revisar primas informadas en Gold")
if totales_polizas.prima != totales_gold.prima:
    raise ValueError("Revisar prima total en Gold")

# Excluir de la conciliacion monetaria los siniestros sin poliza conocida.
asociados = siniestros.join(polizas.select("id_poliza"), "id_poliza", "inner")
totales_siniestros = asociados.agg(
    F.count("id_siniestro").alias("cantidad"),
    (F.count("id_siniestro") - F.count("monto_pagado")).alias("sin_monto"),
    F.coalesce(F.sum("monto_pagado"), F.lit(0)).alias("pagado"),
).first()
if totales_siniestros.cantidad != totales_gold.siniestros:
    raise ValueError("Revisar cantidad de siniestros en Gold")
if totales_siniestros.sin_monto != totales_gold.sin_monto:
    raise ValueError("Revisar siniestros sin monto en Gold")
if totales_siniestros.pagado != totales_gold.pagado:
    raise ValueError("Revisar monto pagado en Gold")
display(siniestros.join(polizas.select("id_poliza"), "id_poliza", "left_anti"))

# Cerrar solamente despues de superar todos los controles.
entregas_validadas = pendientes.withColumn("fecha_proceso", F.current_timestamp())
(
    DeltaTable.forName(spark, "workspace.bronze.s07_control_lotes").alias("destino")
    .merge(entregas_validadas.alias("origen"), "destino.id_lote = origen.id_lote")
    .whenNotMatchedInsertAll().execute()
)
# Si el cierre ya quedo guardado y hubo una falla, repetir libera la pendiente.
(
    DeltaTable.forName(spark, "workspace.bronze.s07_entregas_pendientes").alias("destino")
    .merge(spark.table("workspace.bronze.s07_control_lotes").select("id_lote").alias("origen"),
           "destino.id_lote = origen.id_lote")
    .whenMatchedDelete().execute()
)
display(spark.table("workspace.bronze.s07_control_lotes").orderBy("id_lote"))
display(spark.table("workspace.bronze.s07_entregas_pendientes"))
