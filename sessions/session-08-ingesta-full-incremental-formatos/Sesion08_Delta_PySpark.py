# Databricks notebook source
# ============================================================
# SESIÓN 08 - DELTA LAKE Y CARGAS INCREMENTALES CON PYSPARK
# ============================================================
#
# Objetivo:
#   1. Leer datos desde un Volume o desde Amazon S3.
#   2. Crear una capa Bronze en formato Delta.
#   3. Deduplicar los siniestros usando Window Functions.
#   4. Construir una capa Silver.
#   5. Leer un archivo incremental.
#   6. Aplicar MERGE / UPSERT.
#   7. Validar idempotencia y Schema Evolution.
#
# Dataset utilizado:
#   - siniestros.csv
#   - asegurados.csv
#   - siniestros_incremental_sesion08.csv
#
# IMPORTANTE:
#   - Los archivos de entrada pueden leerse desde un Unity Catalog Volume.
#   - Si el Volume es EXTERNAL y está conectado a S3, físicamente los archivos
#     siguen estando en Amazon S3.
#   - Las tablas Delta de Bronze y Silver se almacenan en rutas S3 separadas.
#     Esto permite visualizar físicamente los archivos .parquet y _delta_log.
#
# ============================================================


# COMMAND ----------
# ============================================================
# 0. CONFIGURACIÓN
# ============================================================
#
# Cambiar estos valores antes de ejecutar.
#
# USE_VOLUME = True:
#   Lee los archivos desde /Volumes/<catalog>/<schema>/<volume>/...
#
# USE_VOLUME = False:
#   Lee directamente desde s3://...
#
# Para este laboratorio podemos usar cualquiera de las dos opciones.

USE_VOLUME = True

CATALOG = "training"

# Schemas donde registraremos las tablas Delta.
BRONZE_SCHEMA = "bronze"
SILVER_SCHEMA = "silver"

# ------------------------------------------------------------
# OPCIÓN A: ARCHIVOS DE ENTRADA DESDE UNITY CATALOG VOLUME
# ------------------------------------------------------------
#
# Ejemplo:
# /Volumes/training/landing/seguros/sesion08/siniestros.csv
#
# Ajustar catalog, schema y volume al ambiente del curso.

VOLUME_BASE = "/Volumes/training/landing/seguros"

VOLUME_SINIESTROS = f"{VOLUME_BASE}/sesion07/siniestros.csv"
VOLUME_ASEGURADOS = f"{VOLUME_BASE}/sesion07/asegurados.csv"
VOLUME_INCREMENTAL = f"{VOLUME_BASE}/sesion08/siniestros_incremental_sesion08.csv"

# ------------------------------------------------------------
# OPCIÓN B: ARCHIVOS DE ENTRADA DIRECTAMENTE DESDE AMAZON S3
# ------------------------------------------------------------

BUCKET = "<TU_BUCKET>"

S3_SINIESTROS = f"s3://{BUCKET}/sesion07/landing/siniestros/siniestros.csv"
S3_ASEGURADOS = f"s3://{BUCKET}/sesion07/landing/asegurados/asegurados.csv"
S3_INCREMENTAL = (
    f"s3://{BUCKET}/sesion08/incremental/siniestros/"
    "siniestros_incremental_sesion08.csv"
)

# ------------------------------------------------------------
# SALIDAS DELTA EN AMAZON S3
# ------------------------------------------------------------
#
# Aquí se almacenarán físicamente:
#   - archivos part-*.parquet
#   - directorio _delta_log
#
# Separamos Bronze y Silver para visualizar la arquitectura por capas.

BRONZE_PATH = f"s3://{BUCKET}/sesion08/bronze/siniestros"
SILVER_PATH = f"s3://{BUCKET}/sesion08/silver/siniestros"

BRONZE_TABLE = f"{CATALOG}.{BRONZE_SCHEMA}.siniestros_s08"
SILVER_TABLE = f"{CATALOG}.{SILVER_SCHEMA}.siniestros_s08"

# Elegimos automáticamente la ruta de lectura.
SINIESTROS_INPUT = VOLUME_SINIESTROS if USE_VOLUME else S3_SINIESTROS
ASEGURADOS_INPUT = VOLUME_ASEGURADOS if USE_VOLUME else S3_ASEGURADOS
INCREMENTAL_INPUT = VOLUME_INCREMENTAL if USE_VOLUME else S3_INCREMENTAL

print("Ruta siniestros :", SINIESTROS_INPUT)
print("Ruta asegurados :", ASEGURADOS_INPUT)
print("Ruta incremental:", INCREMENTAL_INPUT)


# COMMAND ----------
# ============================================================
# 1. IMPORTS
# ============================================================
#
# Importamos solamente las funciones que necesitamos.
#
# col():
#   Permite referenciar una columna.
#
# to_date():
#   Convierte texto a fecha.
#
# to_timestamp():
#   Convierte texto a timestamp.
#
# row_number() + Window:
#   Nos permite quedarnos con el registro más reciente por siniestro.
#
# DeltaTable:
#   API de Delta Lake para realizar UPDATE, DELETE y MERGE desde Python.

from pyspark.sql.functions import (
    col,
    to_date,
    to_timestamp,
    row_number,
)

from pyspark.sql.window import Window
from delta.tables import DeltaTable


# COMMAND ----------
# ============================================================
# 2. CREAR LOS SCHEMAS LÓGICOS EN UNITY CATALOG
# ============================================================
#
# Bronze:
#   Datos cercanos al origen.
#
# Silver:
#   Datos limpios, deduplicados y preparados para consumo.

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{BRONZE_SCHEMA}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SILVER_SCHEMA}")

print("Schemas listos.")


# COMMAND ----------
# ============================================================
# 3. FULL LOAD - LEER SINIESTROS DESDE VOLUME O S3
# ============================================================
#
# En la primera ejecución procesamos el dataset completo.
# Esto representa un FULL LOAD.
#
# Inicialmente Spark lee las columnas del CSV como texto.
# Después convertimos los campos a los tipos adecuados.

df_siniestros_raw = (
    spark.read
         .option("header", True)
         .csv(SINIESTROS_INPUT)
)

print("Registros leídos:", df_siniestros_raw.count())

display(df_siniestros_raw.limit(10))


# COMMAND ----------
# ============================================================
# 4. TIPIFICAR LOS DATOS
# ============================================================
#
# Convertimos:
#   fecha_siniestro      -> DATE
#   fecha_actualizacion  -> TIMESTAMP
#   monto_reserva        -> DOUBLE
#
# Esto ayuda a trabajar correctamente con fechas y valores numéricos.

df_siniestros = (
    df_siniestros_raw
    .withColumn(
        "fecha_siniestro",
        to_date(col("fecha_siniestro"), "yyyy-MM-dd")
    )
    .withColumn(
        "fecha_actualizacion",
        to_timestamp(col("fecha_actualizacion"), "yyyy-MM-dd HH:mm:ss")
    )
    .withColumn(
        "monto_reserva",
        col("monto_reserva").cast("double")
    )
)

df_siniestros.printSchema()

display(df_siniestros.limit(10))


# COMMAND ----------
# ============================================================
# 5. CREAR LA CAPA BRONZE EN DELTA LAKE
# ============================================================
#
# mode("overwrite"):
#   En este laboratorio representa la carga inicial / Full Load.
#
# format("delta"):
#   Spark almacenará los datos utilizando Delta Lake.
#
# Delta físicamente genera:
#   - archivos .parquet
#   - carpeta _delta_log
#
# Todo queda almacenado en Amazon S3.

(
    df_siniestros.write
    .format("delta")
    .mode("overwrite")
    .save(BRONZE_PATH)
)

print("Bronze creado en:", BRONZE_PATH)


# COMMAND ----------
# ============================================================
# 6. REGISTRAR LA TABLA BRONZE
# ============================================================
#
# Los archivos están físicamente en S3.
# Ahora registramos una tabla para consultarlos por nombre.
#
# Ejemplo:
# training.bronze.siniestros_s08

spark.sql(f"""
CREATE TABLE IF NOT EXISTS {BRONZE_TABLE}
USING DELTA
LOCATION '{BRONZE_PATH}'
""")

display(
    spark.sql(f"""
        SELECT *
        FROM {BRONZE_TABLE}
        LIMIT 10
    """)
)


# COMMAND ----------
# ============================================================
# 7. VERIFICAR FÍSICAMENTE LOS ARCHIVOS DELTA EN S3
# ============================================================
#
# Esta validación permite relacionar el concepto del PPT:
#
# Delta Lake =
#   Parquet
#   +
#   _delta_log
#
# dbutils.fs.ls() lista los archivos del directorio S3.

archivos_bronze = dbutils.fs.ls(BRONZE_PATH)

display(archivos_bronze)

# Debemos observar:
#   _delta_log/
#   part-0000....parquet


# COMMAND ----------
# ============================================================
# 8. DEDUPLICACIÓN CON WINDOW FUNCTION
# ============================================================
#
# En siniestros.csv existen múltiples versiones de un mismo id_siniestro.
#
# Objetivo:
#   Conservar solamente la versión MÁS RECIENTE.
#
# partitionBy("id_siniestro"):
#   Crea un grupo por cada siniestro.
#
# orderBy(fecha_actualizacion DESC):
#   Coloca primero el registro más reciente.
#
# row_number():
#   Asigna 1, 2, 3... dentro de cada grupo.

ventana_siniestro = (
    Window
    .partitionBy("id_siniestro")
    .orderBy(col("fecha_actualizacion").desc())
)

df_latest = (
    df_siniestros
    .withColumn(
        "rn",
        row_number().over(ventana_siniestro)
    )
    .filter(col("rn") == 1)
    .drop("rn")
)

print("Registros antes de deduplicar :", df_siniestros.count())
print("Registros después de deduplicar:", df_latest.count())

display(df_latest.limit(10))


# COMMAND ----------
# ============================================================
# 9. LEER ASEGURADOS PARA ENRIQUECER SILVER
# ============================================================
#
# Reutilizamos lo aprendido en la Sesión 07:
#   JOIN entre DataFrames.
#
# El maestro de asegurados aporta:
#   nombre
#   segmento
#   ciudad

df_asegurados = (
    spark.read
         .option("header", True)
         .csv(ASEGURADOS_INPUT)
)

display(df_asegurados.limit(10))


# COMMAND ----------
# ============================================================
# 10. JOIN SINIESTROS + ASEGURADOS
# ============================================================
#
# Usamos LEFT JOIN:
#   Queremos conservar todos los siniestros aunque algún asegurado
#   no tenga correspondencia en el maestro.
#
# Esta será nuestra versión inicial de Silver.
#
# IMPORTANTE:
#   Todavía NO existe la columna canal_reporte.
#   Esa columna llegará después en el archivo incremental y nos
#   servirá para demostrar Schema Evolution.

df_silver_inicial = (
    df_latest.alias("s")
    .join(
        df_asegurados.alias("a"),
        col("s.id_asegurado") == col("a.id_asegurado"),
        "left"
    )
    .select(
        col("s.id_siniestro"),
        col("s.id_asegurado"),
        col("s.fecha_siniestro"),
        col("s.tipo_siniestro"),
        col("s.estado_siniestro"),
        col("s.monto_reserva"),
        col("s.fecha_actualizacion"),
        col("s.departamento_siniestro"),
        col("a.nombre"),
        col("a.segmento"),
        col("a.ciudad"),
    )
)

display(df_silver_inicial.limit(10))


# COMMAND ----------
# ============================================================
# 11. CREAR SILVER EN FORMATO DELTA
# ============================================================
#
# Esta es nuevamente una carga inicial.
# Guardamos el resultado deduplicado y enriquecido como Delta.

(
    df_silver_inicial.write
    .format("delta")
    .mode("overwrite")
    .save(SILVER_PATH)
)

spark.sql(f"""
CREATE TABLE IF NOT EXISTS {SILVER_TABLE}
USING DELTA
LOCATION '{SILVER_PATH}'
""")

print("Silver inicial:", spark.table(SILVER_TABLE).count(), "registros.")

display(spark.table(SILVER_TABLE).limit(10))


# COMMAND ----------
# ============================================================
# 12. LEER EL ARCHIVO INCREMENTAL
# ============================================================
#
# Ahora simulamos el siguiente día / lote.
#
# El archivo incremental contiene:
#   - siniestros nuevos
#   - siniestros ya existentes que cambiaron
#   - varias versiones de algunos IDs
#   - una NUEVA columna: canal_reporte
#
# A diferencia del FULL LOAD, ahora procesaremos únicamente cambios.

df_incremental_raw = (
    spark.read
         .option("header", True)
         .csv(INCREMENTAL_INPUT)
)

print("Filas físicas del incremental:", df_incremental_raw.count())

display(df_incremental_raw)


# COMMAND ----------
# ============================================================
# 13. TIPIFICAR EL INCREMENTAL
# ============================================================

df_incremental = (
    df_incremental_raw
    .withColumn(
        "fecha_siniestro",
        to_date(col("fecha_siniestro"), "yyyy-MM-dd")
    )
    .withColumn(
        "fecha_actualizacion",
        to_timestamp(col("fecha_actualizacion"), "yyyy-MM-dd HH:mm:ss")
    )
    .withColumn(
        "monto_reserva",
        col("monto_reserva").cast("double")
    )
)

df_incremental.printSchema()


# COMMAND ----------
# ============================================================
# 14. DEDUPLICAR EL ARCHIVO INCREMENTAL
# ============================================================
#
# Antes de hacer MERGE debemos evitar que varias filas de origen
# intenten actualizar la misma fila de destino.
#
# Nos quedamos con la última versión por id_siniestro.

df_incremental_latest = (
    df_incremental
    .withColumn(
        "rn",
        row_number().over(ventana_siniestro)
    )
    .filter(col("rn") == 1)
    .drop("rn")
)

print("Filas incremental antes :", df_incremental.count())
print("Filas incremental únicas:", df_incremental_latest.count())

display(df_incremental_latest)


# COMMAND ----------
# ============================================================
# 15. ENRIQUECER EL INCREMENTAL CON ASEGURADOS
# ============================================================
#
# Igual que en Silver inicial, agregamos datos del asegurado.
#
# Pero ahora también conservamos:
#   canal_reporte
#
# Esta columna nueva servirá para explicar Schema Evolution.

df_incremental_final = (
    df_incremental_latest.alias("s")
    .join(
        df_asegurados.alias("a"),
        col("s.id_asegurado") == col("a.id_asegurado"),
        "left"
    )
    .select(
        col("s.id_siniestro"),
        col("s.id_asegurado"),
        col("s.fecha_siniestro"),
        col("s.tipo_siniestro"),
        col("s.estado_siniestro"),
        col("s.monto_reserva"),
        col("s.fecha_actualizacion"),
        col("s.departamento_siniestro"),
        col("a.nombre"),
        col("a.segmento"),
        col("a.ciudad"),
        col("s.canal_reporte"),      # NUEVA COLUMNA
    )
)

display(df_incremental_final)


# COMMAND ----------
# ============================================================
# 16. MERGE / UPSERT CON SCHEMA EVOLUTION
# ============================================================
#
# MERGE realiza dos operaciones:
#
#   Si id_siniestro YA EXISTE:
#       UPDATE
#
#   Si id_siniestro NO EXISTE:
#       INSERT
#
# Además usamos:
#   withSchemaEvolution()
#
# para permitir que la nueva columna canal_reporte se agregue
# a la tabla Delta Silver.
#
# Solo actualizamos si la fecha de origen es más reciente.
#
# Esto evita reemplazar una fila nueva con información antigua.

delta_silver = DeltaTable.forName(spark, SILVER_TABLE)

(
    delta_silver.alias("target")
    .merge(
        df_incremental_final.alias("source"),
        "target.id_siniestro = source.id_siniestro"
    )
    .withSchemaEvolution()
    .whenMatchedUpdateAll(
        condition="source.fecha_actualizacion > target.fecha_actualizacion"
    )
    .whenNotMatchedInsertAll()
    .execute()
)

print("MERGE ejecutado correctamente.")


# COMMAND ----------
# ============================================================
# 17. VALIDAR EL RESULTADO DEL MERGE
# ============================================================
#
# Comprobamos:
#   - cantidad final
#   - nueva columna canal_reporte
#   - algunos registros actualizados / insertados

df_resultado = spark.table(SILVER_TABLE)

print("Cantidad Silver después del MERGE:", df_resultado.count())

df_resultado.printSchema()

display(
    df_resultado
    .orderBy("id_siniestro")
)


# COMMAND ----------
# ============================================================
# 18. VALIDAR SCHEMA EVOLUTION
# ============================================================
#
# Antes del incremental Silver no tenía canal_reporte.
#
# Después del MERGE con Schema Evolution debe aparecer:
#
#   canal_reporte STRING

display(
    spark.sql(f"""
        DESCRIBE {SILVER_TABLE}
    """)
)


# COMMAND ----------
# ============================================================
# 19. VALIDAR IDEMPOTENCIA
# ============================================================
#
# Idempotencia significa:
#
#   ejecutar nuevamente el MISMO proceso
#   NO debe duplicar la información.
#
# Guardamos el conteo antes de repetir el MERGE.

conteo_antes = spark.table(SILVER_TABLE).count()

# Repetimos exactamente el mismo MERGE.
(
    delta_silver.alias("target")
    .merge(
        df_incremental_final.alias("source"),
        "target.id_siniestro = source.id_siniestro"
    )
    .withSchemaEvolution()
    .whenMatchedUpdateAll(
        condition="source.fecha_actualizacion > target.fecha_actualizacion"
    )
    .whenNotMatchedInsertAll()
    .execute()
)

conteo_despues = spark.table(SILVER_TABLE).count()

print("Conteo antes de repetir MERGE :", conteo_antes)
print("Conteo después de repetir MERGE:", conteo_despues)

if conteo_antes == conteo_despues:
    print("OK - El proceso es idempotente: no generó duplicados.")
else:
    print("REVISAR - El conteo cambió.")


# COMMAND ----------
# ============================================================
# 20. VERIFICAR FÍSICAMENTE SILVER EN AMAZON S3
# ============================================================
#
# Nuevamente relacionamos:
#
# Tabla Delta
#   =
# archivos Parquet
#   +
# _delta_log
#
# La cantidad de archivos físicos puede cambiar después de un MERGE,
# porque Delta crea nuevas versiones de los archivos.

display(
    dbutils.fs.ls(SILVER_PATH)
)


# COMMAND ----------
# ============================================================
# 21. CONSULTA FINAL DESDE PYSPARK
# ============================================================
#
# Podemos consultar la tabla por nombre, sin preocuparnos por
# los archivos físicos.

display(
    spark.sql(f"""
        SELECT
            estado_siniestro,
            COUNT(*) AS cantidad
        FROM {SILVER_TABLE}
        GROUP BY estado_siniestro
        ORDER BY cantidad DESC
    """)
)


# COMMAND ----------
# ============================================================
# FIN DEL LABORATORIO
# ============================================================
#
# Conceptos cubiertos:
#
#   1. Delta Lake sobre Amazon S3
#   2. Full Load
#   3. Bronze / Silver
#   4. Window Functions
#   5. Deduplicación
#   6. Incremental Load
#   7. MERGE / UPSERT
#   8. Schema Evolution
#   9. Idempotencia
#  10. Validación física de _delta_log y Parquet
#
# Siguiente paso:
#   Usar SQL Editor para validar y practicar DML sobre Delta.
