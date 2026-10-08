# Paso 6 — Practicar los mismos temas de negocio con DataFrames.
from pyspark.sql import functions as F
from pyspark.sql.window import Window

polizas = spark.table("workspace.bronze.s07_silver_polizas")
productos = spark.table("workspace.bronze.s07_silver_productos")
siniestros = spark.table("workspace.bronze.s07_silver_siniestros")

# select, filter y columna calculada: prima mensual de referencia, sin regla actuarial.
activas = (
    polizas.filter(F.col("estado_poliza") == "ACTIVA")
    .select("id_poliza", "id_producto", "prima", "canal_venta")
    .withColumn("prima_mensual_referencia", F.round(F.col("prima") / 12, 2))
)
display(activas.orderBy("id_poliza"))

# groupBy + agg + alias: count(*) incluye filas; count(prima) excluye nulos.
resumen_productos = polizas.groupBy("id_producto").agg(
    F.count("*").alias("cantidad_polizas"),
    F.count("prima").alias("primas_informadas"),
    F.sum("prima").alias("prima_total"),
    F.round(F.avg("prima"), 2).alias("prima_promedio"),
    F.min("prima").alias("prima_minima"),
    F.max("prima").alias("prima_maxima"),
    F.countDistinct("id_asegurado").alias("asegurados_unicos"),
)
display(resumen_productos.orderBy("id_producto"))

# Seleccionar las columnas necesarias y unir por nombre evita repetir la clave.
catalogo = productos.select("id_producto", "nombre_producto")
display(polizas.join(catalogo, "id_producto", "inner"))
display(polizas.join(catalogo, "id_producto", "left"))
display(polizas.join(catalogo, "id_producto", "right"))
display(polizas.join(catalogo, "id_producto", "full"))

# Cuando ambos lados tienen fecha_actualizacion, calificar y renombrar.
fechas_actualizacion = (
    polizas.alias("p")
    .join(productos.alias("r"), F.col("p.id_producto") == F.col("r.id_producto"), "left")
    .select(
        F.col("p.id_poliza"), F.col("p.id_producto"), F.col("r.nombre_producto"),
        F.col("p.fecha_actualizacion").alias("fecha_actualizacion_poliza"),
        F.col("r.fecha_actualizacion").alias("fecha_actualizacion_producto"),
    )
)
display(fechas_actualizacion)

# dropDuplicates() elimina filas identicas. No sustituye la seleccion por version.
originales = spark.table("workspace.bronze.s07_bronze_polizas")
display(originales.groupBy("id_lote").count().orderBy("id_lote"))
display(originales.dropDuplicates().groupBy("id_lote").count().orderBy("id_lote"))
display(polizas.filter(F.col("prima").isNull()))

# Texto, fechas y fecha actual del servidor.
display(polizas.select(
    "id_poliza", F.lower("canal_venta").alias("canal_minusculas"),
    F.year("fecha_inicio").alias("anio_inicio"),
    F.month("fecha_inicio").alias("mes_inicio"),
    F.current_date().alias("fecha_servidor"),
))
display(siniestros.select(
    "id_siniestro", F.datediff("fecha_reporte", "fecha_siniestro").alias("dias_hasta_reporte"),
))

# Window: dos polizas activas con mayor prima por producto; desempatar por id.
ventana_ranking = Window.partitionBy("id_producto").orderBy(
    F.col("prima").desc(), F.col("id_poliza").asc()
)
ranking = (
    polizas.filter((F.col("estado_poliza") == "ACTIVA") & F.col("prima").isNotNull())
    .withColumn("posicion", F.row_number().over(ventana_ranking))
    .filter(F.col("posicion") <= 2)
    .select("id_producto", "id_poliza", "prima", "posicion")
)
display(ranking.orderBy("id_producto", "posicion"))
display(spark.table("workspace.bronze.s07_gold_cartera").orderBy("id_producto"))

# Practica: crear dos DataFrames y mostrarlos.
# 1. Producto con mayor prima total.
# 2. Cantidad de polizas por canal de venta.
