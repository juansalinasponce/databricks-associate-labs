# Paso 2 — Limpiar y deduplicar solamente las entregas pendientes.
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from delta.tables import DeltaTable

pendientes = spark.table("workspace.bronze.s07_entregas_pendientes").select("id_lote")

# Una fila por entrega y poliza. Mantener la version mas reciente.
# dropDuplicates por clave no garantiza conservar la version mas reciente;
# por eso se utiliza row_number con una ventana ordenada.
ventana_polizas = Window.partitionBy("id_lote", "id_poliza").orderBy(
    F.col("fecha_actualizacion").desc()
)
polizas_limpias = (
    spark.table("workspace.bronze.s07_bronze_polizas")
    .join(pendientes, "id_lote", "left_semi")
    .select(
        "id_lote", "id_poliza", "id_asegurado", "id_producto",
        F.to_date("fecha_inicio").alias("fecha_inicio"),
        F.to_date("fecha_fin").alias("fecha_fin"),
        F.upper(F.trim("estado_poliza")).alias("estado_poliza"),
        F.col("prima").cast("decimal(12,2)").alias("prima"),
        "moneda",
        F.coalesce(F.upper(F.trim("canal_venta")), F.lit("SIN_CANAL")).alias("canal_venta"),
        "departamento",
        F.col("fecha_actualizacion").cast("timestamp").alias("fecha_actualizacion"),
    )
    .withColumn("posicion", F.row_number().over(ventana_polizas))
    .filter(F.col("posicion") == 1)
    .drop("posicion")
)
# Conservar la historia limpia por entrega; repetir no inserta filas existentes.
(
    DeltaTable.forName(spark, "workspace.bronze.s07_lote_polizas").alias("destino")
    .merge(polizas_limpias.alias("origen"),
           "destino.id_lote = origen.id_lote AND destino.id_poliza = origen.id_poliza")
    .whenNotMatchedInsertAll()
    .execute()
)

ventana_productos = Window.partitionBy("id_lote", "id_producto").orderBy(
    F.col("fecha_actualizacion").desc()
)
productos_limpios = (
    spark.table("workspace.bronze.s07_bronze_productos")
    .join(pendientes, "id_lote", "left_semi")
    .select(
        "id_lote", "id_producto",
        "nombre_producto", "tipo_seguro", "segmento",
        F.col("fecha_actualizacion").cast("timestamp").alias("fecha_actualizacion"),
    )
    .withColumn("posicion", F.row_number().over(ventana_productos))
    .filter(F.col("posicion") == 1)
    .drop("posicion")
)
(
    DeltaTable.forName(spark, "workspace.bronze.s07_lote_productos").alias("destino")
    .merge(productos_limpios.alias("origen"),
           "destino.id_lote = origen.id_lote AND destino.id_producto = origen.id_producto")
    .whenNotMatchedInsertAll()
    .execute()
)

ventana_siniestros = Window.partitionBy("id_lote", "id_siniestro").orderBy(
    F.col("fecha_actualizacion").desc()
)
siniestros_limpios = (
    spark.table("workspace.bronze.s07_bronze_siniestros")
    .join(pendientes, "id_lote", "left_semi")
    .select(
        "id_lote", "id_siniestro", "id_poliza",
        F.to_date("fecha_siniestro").alias("fecha_siniestro"),
        F.to_date("fecha_reporte").alias("fecha_reporte"),
        F.upper(F.trim("estado_siniestro")).alias("estado_siniestro"),
        F.col("monto_pagado").cast("decimal(12,2)").alias("monto_pagado"),
        F.col("fecha_actualizacion").cast("timestamp").alias("fecha_actualizacion"),
    )
    .withColumn("posicion", F.row_number().over(ventana_siniestros))
    .filter(F.col("posicion") == 1)
    .drop("posicion")
)
(
    DeltaTable.forName(spark, "workspace.bronze.s07_lote_siniestros").alias("destino")
    .merge(siniestros_limpios.alias("origen"),
           "destino.id_lote = origen.id_lote AND destino.id_siniestro = origen.id_siniestro")
    .whenNotMatchedInsertAll()
    .execute()
)

# Los nulos monetarios se conservan: no conocer un monto no significa monto cero.
display(polizas_limpias.orderBy("id_lote", "id_poliza"))
display(productos_limpios.orderBy("id_lote", "id_producto"))
display(siniestros_limpios.orderBy("id_lote", "id_siniestro"))
