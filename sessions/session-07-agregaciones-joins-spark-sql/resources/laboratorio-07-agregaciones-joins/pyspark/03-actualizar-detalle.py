# Paso 3 — Actualizar el detalle vigente y registrar productos afectados.
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from delta.tables import DeltaTable

pendientes = spark.table("workspace.bronze.s07_entregas_pendientes").select("id_lote")
polizas_lote = spark.table("workspace.bronze.s07_lote_polizas").join(pendientes, "id_lote", "left_semi")
productos_lote = spark.table("workspace.bronze.s07_lote_productos").join(pendientes, "id_lote", "left_semi")
siniestros_lote = spark.table("workspace.bronze.s07_lote_siniestros").join(pendientes, "id_lote", "left_semi")

# Si una poliza cambia de producto, recalcular tanto el anterior como el nuevo.
productos_nuevos = polizas_lote.select("id_lote", "id_producto")
productos_anteriores = (
    polizas_lote.alias("cambio")
    .join(spark.table("workspace.bronze.s07_silver_polizas").alias("actual"),
          F.col("cambio.id_poliza") == F.col("actual.id_poliza"), "inner")
    .select(F.col("cambio.id_lote"), F.col("actual.id_producto"))
)

# Si un siniestro cambia de poliza, conservar el producto de su poliza anterior.
productos_siniestros_anteriores = (
    siniestros_lote.alias("cambio")
    .join(spark.table("workspace.bronze.s07_silver_siniestros").alias("siniestro"),
          F.col("cambio.id_siniestro") == F.col("siniestro.id_siniestro"), "inner")
    .join(spark.table("workspace.bronze.s07_silver_polizas").alias("poliza"),
          F.col("siniestro.id_poliza") == F.col("poliza.id_poliza"), "inner")
    .select(F.col("cambio.id_lote"), F.col("poliza.id_producto"))
)
afectados_antes = (
    productos_nuevos.unionByName(productos_anteriores)
    .unionByName(productos_lote.select("id_lote", "id_producto"))
    .unionByName(productos_siniestros_anteriores)
    .dropDuplicates(["id_lote", "id_producto"])
)
# Guardar esta lista ANTES de cambiar Silver permite recuperar una falla posterior.
(
    DeltaTable.forName(spark, "workspace.bronze.s07_productos_afectados").alias("destino")
    .merge(afectados_antes.alias("origen"),
           "destino.id_lote = origen.id_lote AND destino.id_producto = origen.id_producto")
    .whenNotMatchedInsertAll()
    .execute()
)

# Puede haber varias entregas pendientes: elegir una sola version por clave.
ventana_polizas = Window.partitionBy("id_poliza").orderBy(
    F.col("fecha_actualizacion").desc(), F.col("id_lote").desc()
)
polizas_recientes = (
    polizas_lote.withColumn("posicion", F.row_number().over(ventana_polizas))
    .filter(F.col("posicion") == 1).drop("posicion")
)
(
    DeltaTable.forName(spark, "workspace.bronze.s07_silver_polizas").alias("destino")
    .merge(polizas_recientes.alias("origen"), "destino.id_poliza = origen.id_poliza")
    .whenMatchedUpdateAll(condition="origen.fecha_actualizacion > destino.fecha_actualizacion")
    .whenNotMatchedInsertAll()
    .execute()
)

ventana_productos = Window.partitionBy("id_producto").orderBy(
    F.col("fecha_actualizacion").desc(), F.col("id_lote").desc()
)
productos_recientes = (
    productos_lote.withColumn("posicion", F.row_number().over(ventana_productos))
    .filter(F.col("posicion") == 1).drop("posicion")
)
(
    DeltaTable.forName(spark, "workspace.bronze.s07_silver_productos").alias("destino")
    .merge(productos_recientes.alias("origen"), "destino.id_producto = origen.id_producto")
    .whenMatchedUpdateAll(condition="origen.fecha_actualizacion > destino.fecha_actualizacion")
    .whenNotMatchedInsertAll()
    .execute()
)

ventana_siniestros = Window.partitionBy("id_siniestro").orderBy(
    F.col("fecha_actualizacion").desc(), F.col("id_lote").desc()
)
siniestros_recientes = (
    siniestros_lote.withColumn("posicion", F.row_number().over(ventana_siniestros))
    .filter(F.col("posicion") == 1).drop("posicion")
)
(
    DeltaTable.forName(spark, "workspace.bronze.s07_silver_siniestros").alias("destino")
    .merge(siniestros_recientes.alias("origen"), "destino.id_siniestro = origen.id_siniestro")
    .whenMatchedUpdateAll(condition="origen.fecha_actualizacion > destino.fecha_actualizacion")
    .whenNotMatchedInsertAll()
    .execute()
)

# Agregar el producto de la nueva poliza del siniestro, usando Silver actualizado.
afectados_despues = (
    siniestros_lote.alias("cambio")
    .join(spark.table("workspace.bronze.s07_silver_polizas").alias("poliza"),
          F.col("cambio.id_poliza") == F.col("poliza.id_poliza"), "inner")
    .select(F.col("cambio.id_lote"), F.col("poliza.id_producto"))
    .dropDuplicates(["id_lote", "id_producto"])
)
(
    DeltaTable.forName(spark, "workspace.bronze.s07_productos_afectados").alias("destino")
    .merge(afectados_despues.alias("origen"),
           "destino.id_lote = origen.id_lote AND destino.id_producto = origen.id_producto")
    .whenNotMatchedInsertAll()
    .execute()
)

display(spark.table("workspace.bronze.s07_silver_polizas").orderBy("id_poliza"))
