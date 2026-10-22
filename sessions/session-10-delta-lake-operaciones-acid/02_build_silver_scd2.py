# Databricks notebook source
# ============================================================
# 02 - BRONZE -> SILVER CON SCD TYPE 2
# ============================================================
#
# Objetivo:
#   - detectar cambios reales
#   - generar historial
#   - mantener fecha inicio/fin de vigencia
#   - identificar la versión actual
#
# La fuente ya contiene diferentes versiones de algunos IDs.
# Esto permite visualizar SCD2 desde la primera ejecución.
# ============================================================

# COMMAND ----------
from pyspark.sql import functions as F
from pyspark.sql.window import Window
import uuid

POLIZAS_BRONZE = "workspace.bronze.polizas_medallion"
SINIESTROS_BRONZE = "workspace.bronze.siniestros_medallion"

POLIZAS_SILVER = "workspace.silver.polizas_scd2"
SINIESTROS_SILVER = "workspace.silver.siniestros_scd2"

ID_EJECUCION_SILVER = str(uuid.uuid4())

# COMMAND ----------
# Helper para crear SCD2 desde un histórico de eventos/versiones.

def crear_scd2(df, business_key, tracked_cols, surrogate_name):

    # Hash únicamente de los atributos de negocio.
    # fecha_actualizacion NO entra al hash:
    # si cambió solo el timestamp pero no el contenido,
    # no queremos una nueva versión.
    hash_expr = F.sha2(
        F.concat_ws(
            "||",
            *[
                F.coalesce(F.col(c).cast("string"), F.lit("<NULL>"))
                for c in tracked_cols
            ]
        ),
        256
    )

    df_hash = df.withColumn("hash_registro", hash_expr)

    w_hist = (
        Window
        .partitionBy(business_key)
        .orderBy("fecha_actualizacion")
    )

    # Comparar contra el hash anterior.
    df_cambios = (
        df_hash
        .withColumn("hash_anterior", F.lag("hash_registro").over(w_hist))
        .filter(
            F.col("hash_anterior").isNull()
            | (F.col("hash_registro") != F.col("hash_anterior"))
        )
        .drop("hash_anterior")
    )

    # Volver a ordenar SOLO las versiones que representan cambios.
    w_cambios = (
        Window
        .partitionBy(business_key)
        .orderBy("fecha_actualizacion")
    )

    df_scd2 = (
        df_cambios
        .withColumn(
            "siguiente_fecha",
            F.lead("fecha_actualizacion").over(w_cambios)
        )
        .withColumn(
            "fecha_inicio_vigencia",
            F.col("fecha_actualizacion")
        )
        .withColumn(
            "fecha_fin_vigencia",
            F.when(
                F.col("siguiente_fecha").isNull(),
                F.to_timestamp(F.lit("9999-12-31 23:59:59"))
            ).otherwise(
                F.expr("siguiente_fecha - INTERVAL 1 SECOND")
            )
        )
        .withColumn(
            "es_actual",
            F.col("siguiente_fecha").isNull()
        )
        .withColumn(
            surrogate_name,
            F.sha2(
                F.concat_ws(
                    "||",
                    F.col(business_key),
                    F.date_format(
                        "fecha_actualizacion",
                        "yyyyMMddHHmmss"
                    )
                ),
                256
            )
        )
        .withColumn(
            "fecha_procesamiento",
            F.current_timestamp()
        )
        .withColumn(
            "id_ejecucion",
            F.lit(ID_EJECUCION_SILVER)
        )
        .drop("siguiente_fecha")
        .drop("fecha_actualizacion")
    )

    return df_scd2


# COMMAND ----------
# 1. PÓLIZAS SCD2

df_polizas = spark.table(POLIZAS_BRONZE)

tracked_polizas = [
    "id_asegurado",
    "nro_documento",
    "nombre_asegurado",
    "producto",
    "plan",
    "prima_mensual",
    "suma_asegurada",
    "estado_poliza",
    "canal_venta",
    "departamento",
    "fecha_inicio_poliza",
    "fecha_fin_poliza"
]

df_polizas_scd2 = crear_scd2(
    df_polizas,
    "id_poliza",
    tracked_polizas,
    "sk_poliza_scd2"
)

polizas_cols = spark.table(POLIZAS_SILVER).columns

df_polizas_scd2 = df_polizas_scd2.select(*polizas_cols)

spark.sql(f"TRUNCATE TABLE {POLIZAS_SILVER}")

df_polizas_scd2.write.mode("append").saveAsTable(POLIZAS_SILVER)

print("Versiones SCD2 pólizas:", spark.table(POLIZAS_SILVER).count())

# COMMAND ----------
# 2. SINIESTROS SCD2

df_siniestros = spark.table(SINIESTROS_BRONZE)

tracked_siniestros = [
    "id_poliza",
    "tipo_siniestro",
    "fecha_ocurrencia",
    "fecha_reporte",
    "estado_siniestro",
    "monto_reserva",
    "monto_pagado",
    "canal_reporte",
    "ajustador"
]

df_siniestros_scd2 = crear_scd2(
    df_siniestros,
    "id_siniestro",
    tracked_siniestros,
    "sk_siniestro_scd2"
)

siniestros_cols = spark.table(SINIESTROS_SILVER).columns

df_siniestros_scd2 = df_siniestros_scd2.select(*siniestros_cols)

spark.sql(f"TRUNCATE TABLE {SINIESTROS_SILVER}")

df_siniestros_scd2.write.mode("append").saveAsTable(SINIESTROS_SILVER)

print("Versiones SCD2 siniestros:", spark.table(SINIESTROS_SILVER).count())

# COMMAND ----------
# 3. VALIDAR HISTORIAL DE UNA PÓLIZA

display(
    spark.sql(f"""
        SELECT
            id_poliza,
            plan,
            prima_mensual,
            estado_poliza,
            fecha_inicio_vigencia,
            fecha_fin_vigencia,
            es_actual
        FROM {POLIZAS_SILVER}
        WHERE id_poliza IN ('POL-0006', 'POL-0012')
        ORDER BY id_poliza, fecha_inicio_vigencia
    """)
)

# COMMAND ----------
# 4. VALIDAR HISTORIAL DE SINIESTROS

display(
    spark.sql(f"""
        SELECT
            id_siniestro,
            estado_siniestro,
            monto_reserva,
            monto_pagado,
            fecha_inicio_vigencia,
            fecha_fin_vigencia,
            es_actual
        FROM {SINIESTROS_SILVER}
        WHERE id_siniestro IN ('SIN-0001', 'SIN-0002')
        ORDER BY id_siniestro, fecha_inicio_vigencia
    """)
)
