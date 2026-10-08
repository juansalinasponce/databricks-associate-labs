# Respuestas del instructor; ejecutar despues de completar las cargas.
from pyspark.sql import functions as F

# Producto con mayor prima total: desempatar por id_producto.
producto_mayor_prima = (
    spark.table("workspace.bronze.s07_gold_cartera")
    .select("id_producto", "nombre_producto", "prima_total")
    .orderBy(F.col("prima_total").desc(), F.col("id_producto").asc())
    .limit(1)
)
display(producto_mayor_prima)

# Cantidad de polizas por canal, usando el detalle vigente.
polizas_por_canal = (
    spark.table("workspace.bronze.s07_silver_polizas")
    .groupBy("canal_venta")
    .agg(F.count("id_poliza").alias("cantidad_polizas"))
    .orderBy("canal_venta")
)
display(polizas_por_canal)
