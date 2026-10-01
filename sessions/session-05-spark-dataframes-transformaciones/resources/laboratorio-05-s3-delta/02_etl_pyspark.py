# Databricks notebook source
# MAGIC %md
# MAGIC # 02 — ETL básico con PySpark DataFrames
# MAGIC
# MAGIC Este notebook lee 10,000 pólizas desde Amazon S3, explica las funciones
# MAGIC principales de PySpark, limpia los datos y guarda una tabla Delta en S3.
# MAGIC
# MAGIC Requisito: ejecutar primero `01_ddl_tablas.sql` y reemplazar
# MAGIC `<S3_BUCKET>` en este notebook.

# COMMAND ----------

# DBTITLE 1,1. Importar funciones de Spark
# Importamos únicamente las funciones que se usarán. `col()` será la única forma
# de construir expresiones que hagan referencia a columnas del DataFrame.
from pyspark.sql.functions import (
    avg,
    col,
    count,
    countDistinct,
    current_timestamp,
    lit,
    round,
    sum,
    to_date,
    to_timestamp,
    trim,
    upper,
    when,
)
from pyspark.sql.types import DecimalType

# COMMAND ----------

# DBTITLE 1,2. Definir parámetros del laboratorio
# Centralizar nombres y rutas evita repetir valores dentro de la lógica.
CATALOGO = "workspace"
RUTA_CSV = "s3://<S3_BUCKET>/landing/polizas/polizas_10000.csv"
TABLA_DESTINO = f"{CATALOGO}.bronze.polizas"
RUTA_DELTA = "s3://<S3_BUCKET>/bronze/polizas_delta/"
FECHA_CORTE = "2026-09-30"

# El schema explícito evita depender de inferSchema y conserva los valores del
# archivo de Landing como texto. Las conversiones se muestran más adelante.
SCHEMA_CSV = """
    id_poliza STRING,
    id_asegurado STRING,
    id_producto STRING,
    fecha_inicio STRING,
    fecha_fin STRING,
    estado_poliza STRING,
    prima STRING,
    moneda STRING,
    canal_venta STRING,
    departamento STRING,
    fecha_actualizacion STRING
"""

# COMMAND ----------

# MAGIC %md
# MAGIC ## A. Lectura e inspección
# MAGIC
# MAGIC Un DataFrame es una colección distribuida de filas organizadas en
# MAGIC columnas. Las transformaciones construyen un plan; una acción como
# MAGIC `count()` o `display()` provoca su ejecución.

# COMMAND ----------

# DBTITLE 1,3. Leer directamente el CSV de Landing
# spark.read inicia una lectura de archivos sin registrar Landing como tabla.
# format("csv") indica el formato; schema() aplica la estructura explícita.
# option() configura encabezado, separador y representación de valores nulos.
# load(ruta) crea el DataFrame desde el objeto cargado manualmente en S3.
# `_metadata` ofrece datos técnicos del archivo y es compatible con Unity Catalog.
polizas_raw_df = (
    spark.read
    .format("csv")
    .schema(SCHEMA_CSV)
    .option("header", "true")
    .option("delimiter", ",")
    .option("encoding", "UTF-8")
    .option("nullValue", "")
    .load(RUTA_CSV)
    .select(
        col("*"),
        col("_metadata.file_name").alias("_archivo_origen"),
        col("_metadata.file_path").alias("_ruta_origen"),
    )
)

# COMMAND ----------

# DBTITLE 1,4. Mostrar una muestra
# limit(n) conserva solamente n filas.
# display(df) es una función de Databricks que ejecuta el plan y muestra el resultado.
display(polizas_raw_df.limit(10))

# COMMAND ----------

# DBTITLE 1,5. Revisar nombres y tipos
# printSchema() imprime la estructura del DataFrame. El schema de lectura conserva
# todos los campos como STRING para representar la forma en que llegaron.
polizas_raw_df.printSchema()

# COMMAND ----------

# DBTITLE 1,6. Contar las filas recibidas
# count() es una acción: Spark ejecuta la lectura y devuelve un número a Python.
total_entrada = polizas_raw_df.count()
print(f"Filas recibidas: {total_entrada:,}")

# COMMAND ----------

# DBTITLE 1,7. Seleccionar columnas con col()
# select(...) proyecta únicamente las columnas indicadas.
# col("nombre") crea una expresión Column; se usa el mismo estilo en todo el ETL.
polizas_muestra_df = polizas_raw_df.select(
    col("id_poliza"),
    col("id_producto"),
    col("estado_poliza"),
    col("prima"),
    col("moneda"),
)
display(polizas_muestra_df.limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ## B. Limpieza y conversión de tipos
# MAGIC
# MAGIC `withColumn()` crea una columna o reemplaza una existente. Las llamadas
# MAGIC se encadenan para que cada regla permanezca visible y fácil de explicar.

# COMMAND ----------

# DBTITLE 1,8. Normalizar texto y convertir tipos
polizas_typed_df = (
    polizas_raw_df
    # trim() elimina espacios al inicio y al final del texto.
    # upper() convierte el texto a mayúsculas para unificar categorías.
    .withColumn("id_poliza", upper(trim(col("id_poliza"))))
    .withColumn("id_asegurado", upper(trim(col("id_asegurado"))))
    .withColumn("id_producto", upper(trim(col("id_producto"))))
    .withColumn("estado_poliza", upper(trim(col("estado_poliza"))))
    .withColumn("moneda", upper(trim(col("moneda"))))
    .withColumn("canal_venta", upper(trim(col("canal_venta"))))
    .withColumn("departamento", upper(trim(col("departamento"))))
    # to_date() interpreta un texto con el patrón indicado y devuelve DATE.
    .withColumn("fecha_inicio", to_date(col("fecha_inicio"), "yyyy-MM-dd"))
    .withColumn("fecha_fin", to_date(col("fecha_fin"), "yyyy-MM-dd"))
    # cast() convierte el texto de prima a un número decimal de dos posiciones.
    .withColumn("prima", col("prima").cast(DecimalType(12, 2)))
    # to_timestamp() convierte fecha y hora de texto a TIMESTAMP.
    .withColumn(
        "fecha_actualizacion",
        to_timestamp(col("fecha_actualizacion"), "yyyy-MM-dd HH:mm:ss"),
    )
)

display(polizas_typed_df.limit(10))

# COMMAND ----------

# DBTITLE 1,9. Completar canales vacíos
# fillna(diccionario) reemplaza valores NULL. Las claves son nombres de columnas
# requeridos por la interfaz del método; las expresiones siguen utilizando col().
polizas_completas_df = polizas_typed_df.fillna(
    {"canal_venta": "SIN_INFORMACION"}
)

# COMMAND ----------

# DBTITLE 1,10. Crear columnas derivadas con when()
# when(condición, valor).otherwise(valor) equivale a CASE WHEN de SQL.
# lit() crea un valor literal dentro de una expresión Spark.
polizas_derivadas_df = (
    polizas_completas_df
    .withColumn(
        "estado_vigencia",
        when(
            (col("fecha_inicio") <= to_date(lit(FECHA_CORTE)))
            & (col("fecha_fin") >= to_date(lit(FECHA_CORTE)))
            & (col("estado_poliza") == lit("ACTIVA")),
            lit("VIGENTE"),
        ).otherwise(lit("NO_VIGENTE")),
    )
    .withColumn(
        "segmento_prima",
        when(col("prima") < lit(1_000), lit("BAJA"))
        .when(col("prima") < lit(3_000), lit("MEDIA"))
        .otherwise(lit("ALTA")),
    )
)

# COMMAND ----------

# DBTITLE 1,11. Filtrar registros válidos
# filter(condición) conserva solo las filas que cumplen la expresión booleana.
# isNotNull() comprueba que exista un valor después de la conversión de tipos.
polizas_validas_df = polizas_derivadas_df.filter(
    col("id_poliza").isNotNull()
    & col("fecha_inicio").isNotNull()
    & col("fecha_fin").isNotNull()
    & col("prima").isNotNull()
    & (col("prima") >= lit(0))
)

# COMMAND ----------

# DBTITLE 1,12. Eliminar filas completamente duplicadas
# dropDuplicates() sin argumentos elimina filas idénticas en todas sus columnas.
# El CSV contiene 25 duplicados exactos creados con propósito pedagógico.
polizas_unicas_df = polizas_validas_df.dropDuplicates()

# COMMAND ----------

# DBTITLE 1,13. Añadir columnas técnicas y ordenar el schema
# current_timestamp() registra cuándo se ejecutó el proceso.
# alias() cambia el nombre mostrado por una expresión.
polizas_bronze_df = (
    polizas_unicas_df
    .withColumn("_fecha_proceso", current_timestamp())
    .select(
        col("id_poliza"),
        col("id_asegurado"),
        col("id_producto"),
        col("fecha_inicio"),
        col("fecha_fin"),
        col("estado_poliza"),
        col("prima"),
        col("moneda"),
        col("canal_venta"),
        col("departamento"),
        col("fecha_actualizacion"),
        col("estado_vigencia"),
        col("segmento_prima"),
        col("_archivo_origen"),
        col("_ruta_origen"),
        col("_fecha_proceso"),
    )
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## C. Agregaciones básicas
# MAGIC
# MAGIC Las agregaciones reducen varias filas a indicadores de resumen.

# COMMAND ----------

# DBTITLE 1,14. Resumir pólizas por producto
# groupBy() forma grupos con valores iguales.
# agg() permite calcular varias métricas por cada grupo.
# count() cuenta filas; countDistinct() cuenta valores diferentes.
# sum() suma importes; avg() calcula el promedio; round() limita decimales.
# orderBy(...desc()) ordena de mayor a menor.
resumen_producto_df = (
    polizas_bronze_df
    .groupBy(col("id_producto"))
    .agg(
        count(lit(1)).alias("cantidad_polizas"),
        countDistinct(col("id_asegurado")).alias("asegurados_unicos"),
        round(sum(col("prima")), 2).alias("prima_total"),
        round(avg(col("prima")), 2).alias("prima_promedio"),
    )
    .orderBy(col("prima_total").desc())
)
display(resumen_producto_df)

# COMMAND ----------

# DBTITLE 1,15. Comparar cantidades antes de escribir
total_salida = polizas_bronze_df.count()
print(f"Filas de entrada : {total_entrada:,}")
print(f"Filas de salida  : {total_salida:,}")
print(f"Duplicados quitados: {total_entrada - total_salida:,}")

assert total_entrada == 10_000, "La fuente debe contener exactamente 10,000 filas"
assert total_salida == 9_975, "La salida esperada después de deduplicar es 9,975"

# COMMAND ----------

# MAGIC %md
# MAGIC ## D. Escritura Delta en Amazon S3
# MAGIC
# MAGIC La escritura se ejecuta una sola vez, después de validar el resultado.

# COMMAND ----------

# DBTITLE 1,16. Guardar físicamente la tabla Delta en S3
# write inicia la configuración de salida.
# format("delta") selecciona Delta Lake.
# mode("overwrite") reemplaza la versión anterior para poder repetir el laboratorio.
# option("overwriteSchema", "true") permite actualizar el schema en esta práctica.
# save(ruta) materializa archivos Parquet y el directorio _delta_log en S3.
(
    polizas_bronze_df.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .save(RUTA_DELTA)
)

# COMMAND ----------

# DBTITLE 1,17. Actualizar y consultar la tabla registrada
# REFRESH TABLE solicita que Databricks actualice la metadata observable.
spark.sql(f"REFRESH TABLE {TABLA_DESTINO}")

resultado_df = spark.table(TABLA_DESTINO)
display(resultado_df.orderBy(col("id_poliza")).limit(20))

# COMMAND ----------

# DBTITLE 1,18. Consultar el mismo DataFrame con Spark SQL
# createOrReplaceTempView() publica una vista temporal válida en esta sesión.
# spark.sql() ejecuta una consulta SQL y devuelve otro DataFrame.
polizas_bronze_df.createOrReplaceTempView("vw_polizas_bronze")

resumen_sql_df = spark.sql("""
    SELECT
      estado_vigencia,
      COUNT(*) AS cantidad_polizas,
      ROUND(SUM(prima), 2) AS prima_total
    FROM vw_polizas_bronze
    GROUP BY estado_vigencia
    ORDER BY cantidad_polizas DESC
""")
display(resumen_sql_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resultado verificable
# MAGIC
# MAGIC - La entrada tiene 10,000 filas.
# MAGIC - La salida Bronze tiene 9,975 filas después de eliminar 25 duplicados.
# MAGIC - `canal_venta` ya no contiene nulos.
# MAGIC - Fechas, timestamp y prima tienen tipos adecuados.
# MAGIC - En S3 existen `_delta_log/` y archivos `part-*.parquet`.
