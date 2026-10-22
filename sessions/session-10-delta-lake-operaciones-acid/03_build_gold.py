# Databricks notebook source
# ============================================================
# 03 - SILVER -> GOLD
# MODELO DIMENSIONAL
# ============================================================
#
# Se utilizará únicamente la versión ACTUAL de Silver.
#
# Dimensiones:
#   dim_asegurado
#   dim_producto
#   dim_poliza
#   dim_tiempo
#
# Hechos:
#   fact_poliza
#   fact_siniestro
#
# Grain:
#   fact_poliza    = 1 fila por póliza actual
#   fact_siniestro = 1 fila por siniestro actual
# ============================================================

# COMMAND ----------
from pyspark.sql import functions as F
from pyspark.sql.window import Window
import uuid

POLIZAS_SILVER = "workspace.silver.polizas_scd2"
SINIESTROS_SILVER = "workspace.silver.siniestros_scd2"

ID_EJECUCION_GOLD = str(uuid.uuid4())

# COMMAND ----------
# 1. FILTRAR VERSIONES ACTUALES

polizas = spark.table(POLIZAS_SILVER).filter("es_actual = true")
siniestros = spark.table(SINIESTROS_SILVER).filter("es_actual = true")

# COMMAND ----------
# 2. DIM_ASEGURADO
#
# Si un asegurado tuviera varias pólizas,
# elegimos el registro más reciente.

w_aseg = (
    Window
    .partitionBy("id_asegurado")
    .orderBy(F.col("fecha_inicio_vigencia").desc())
)

dim_asegurado = (
    polizas
    .withColumn("rn", F.row_number().over(w_aseg))
    .filter("rn = 1")
    .drop("rn")
    .select(
        F.sha2(F.col("id_asegurado"), 256).alias("sk_asegurado"),
        "id_asegurado",
        "nro_documento",
        "nombre_asegurado",
        "departamento",
        "canal_venta"
    )
    .withColumn("fecha_carga", F.current_timestamp())
    .withColumn("id_ejecucion", F.lit(ID_EJECUCION_GOLD))
)

# COMMAND ----------
# 3. DIM_PRODUCTO

dim_producto = (
    polizas
    .select("producto", "plan")
    .dropDuplicates()
    .withColumn(
        "sk_producto",
        F.sha2(
            F.concat_ws("||", "producto", "plan"),
            256
        )
    )
    .select(
        "sk_producto",
        "producto",
        "plan"
    )
    .withColumn("fecha_carga", F.current_timestamp())
    .withColumn("id_ejecucion", F.lit(ID_EJECUCION_GOLD))
)

# COMMAND ----------
# 4. DIM_POLIZA

dim_poliza = (
    polizas.alias("p")
    .join(
        dim_asegurado.alias("a"),
        F.col("p.id_asegurado") == F.col("a.id_asegurado"),
        "left"
    )
    .join(
        dim_producto.alias("pr"),
        (F.col("p.producto") == F.col("pr.producto"))
        & (F.col("p.plan") == F.col("pr.plan")),
        "left"
    )
    .select(
        F.sha2(F.col("p.id_poliza"), 256).alias("sk_poliza"),
        F.col("p.id_poliza"),
        F.col("a.sk_asegurado"),
        F.col("pr.sk_producto"),
        F.col("p.estado_poliza"),
        F.col("p.fecha_inicio_poliza"),
        F.col("p.fecha_fin_poliza"),
        F.col("p.canal_venta")
    )
    .withColumn("fecha_carga", F.current_timestamp())
    .withColumn("id_ejecucion", F.lit(ID_EJECUCION_GOLD))
)

# COMMAND ----------
# 5. DIM_TIEMPO
#
# Tomamos las fechas mínimas y máximas presentes
# en pólizas y siniestros.

fechas = (
    polizas.select(F.col("fecha_inicio_poliza").alias("fecha"))
    .union(polizas.select(F.col("fecha_fin_poliza").alias("fecha")))
    .union(siniestros.select(F.col("fecha_ocurrencia").alias("fecha")))
    .union(siniestros.select(F.col("fecha_reporte").alias("fecha")))
    .filter("fecha IS NOT NULL")
)

bounds = fechas.agg(
    F.min("fecha").alias("min_fecha"),
    F.max("fecha").alias("max_fecha")
).first()

min_fecha = bounds["min_fecha"]
max_fecha = bounds["max_fecha"]

dim_tiempo = (
    spark.sql(
        f"""
        SELECT explode(
            sequence(
                to_date('{min_fecha}'),
                to_date('{max_fecha}'),
                interval 1 day
            )
        ) AS fecha
        """
    )
    .withColumn(
        "sk_fecha",
        F.date_format("fecha", "yyyyMMdd").cast("int")
    )
    .withColumn("anio", F.year("fecha"))
    .withColumn("mes", F.month("fecha"))
    .withColumn("nombre_mes", F.date_format("fecha", "MMMM"))
    .withColumn("trimestre", F.quarter("fecha"))
    .withColumn("dia", F.dayofmonth("fecha"))
    .withColumn("dia_semana", F.dayofweek("fecha"))
    .select(
        "sk_fecha",
        "fecha",
        "anio",
        "mes",
        "nombre_mes",
        "trimestre",
        "dia",
        "dia_semana"
    )
    .withColumn("fecha_carga", F.current_timestamp())
    .withColumn("id_ejecucion", F.lit(ID_EJECUCION_GOLD))
)

# COMMAND ----------
# 6. FACT_POLIZA

fact_poliza = (
    polizas.alias("p")
    .join(
        dim_poliza.alias("dp"),
        F.col("p.id_poliza") == F.col("dp.id_poliza"),
        "inner"
    )
    .select(
        F.sha2(
            F.concat_ws(
                "||",
                F.col("p.id_poliza"),
                F.lit("POLIZA")
            ),
            256
        ).alias("sk_fact_poliza"),
        F.col("dp.sk_poliza"),
        F.col("dp.sk_asegurado"),
        F.col("dp.sk_producto"),
        F.date_format(
            "p.fecha_inicio_poliza",
            "yyyyMMdd"
        ).cast("int").alias("sk_fecha_inicio"),
        F.col("p.prima_mensual"),
        F.col("p.suma_asegurada"),
        F.col("p.estado_poliza")
    )
    .withColumn("fecha_carga", F.current_timestamp())
    .withColumn("id_ejecucion", F.lit(ID_EJECUCION_GOLD))
)

# COMMAND ----------
# 7. FACT_SINIESTRO
#
# Aquí se produce la integración de los DOS archivos:
#
# siniestros
#      ↓ id_poliza
# pólizas
#      ↓
# dimensiones de Gold

fact_siniestro = (
    siniestros.alias("s")
    .join(
        dim_poliza.alias("dp"),
        F.col("s.id_poliza") == F.col("dp.id_poliza"),
        "left"
    )
    .select(
        F.sha2(
            F.concat_ws(
                "||",
                F.col("s.id_siniestro"),
                F.lit("SINIESTRO")
            ),
            256
        ).alias("sk_fact_siniestro"),
        F.col("s.id_siniestro"),
        F.col("dp.sk_poliza"),
        F.col("dp.sk_asegurado"),
        F.col("dp.sk_producto"),
        F.date_format(
            "s.fecha_ocurrencia",
            "yyyyMMdd"
        ).cast("int").alias("sk_fecha_ocurrencia"),
        F.date_format(
            "s.fecha_reporte",
            "yyyyMMdd"
        ).cast("int").alias("sk_fecha_reporte"),
        F.col("s.tipo_siniestro"),
        F.col("s.estado_siniestro"),
        F.col("s.monto_reserva"),
        F.col("s.monto_pagado"),
        F.datediff(
            "s.fecha_reporte",
            "s.fecha_ocurrencia"
        ).alias("dias_reporte")
    )
    .withColumn("fecha_carga", F.current_timestamp())
    .withColumn("id_ejecucion", F.lit(ID_EJECUCION_GOLD))
)

# COMMAND ----------
# 8. FUNCIÓN DE REEMPLAZO CONTROLADO

def reemplazar_tabla(df, table_name):
    cols = spark.table(table_name).columns
    spark.sql(f"TRUNCATE TABLE {table_name}")
    (
        df.select(*cols)
        .write
        .mode("append")
        .saveAsTable(table_name)
    )
    print(table_name, "->", spark.table(table_name).count(), "filas")

# COMMAND ----------
# 9. CARGAR GOLD

reemplazar_tabla(dim_asegurado, "workspace.gold.dim_asegurado")
reemplazar_tabla(dim_producto, "workspace.gold.dim_producto")
reemplazar_tabla(dim_poliza, "workspace.gold.dim_poliza")
reemplazar_tabla(dim_tiempo, "workspace.gold.dim_tiempo")
reemplazar_tabla(fact_poliza, "workspace.gold.fact_poliza")
reemplazar_tabla(fact_siniestro, "workspace.gold.fact_siniestro")

# COMMAND ----------
# 10. VALIDACIÓN

display(
    spark.sql("""
        SELECT
            p.producto,
            p.plan,
            f.tipo_siniestro,
            COUNT(*) AS cantidad_siniestros,
            ROUND(SUM(f.monto_reserva), 2) AS reserva_total,
            ROUND(SUM(f.monto_pagado), 2) AS pagado_total
        FROM workspace.gold.fact_siniestro f
        LEFT JOIN workspace.gold.dim_producto p
            ON f.sk_producto = p.sk_producto
        GROUP BY
            p.producto,
            p.plan,
            f.tipo_siniestro
        ORDER BY reserva_total DESC
    """)
)
