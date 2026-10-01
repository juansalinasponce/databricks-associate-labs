# Laboratorio 05 — De Amazon S3 a Delta Lake con PySpark y Spark SQL

## Ficha del laboratorio

| Campo | Valor |
| --- | --- |
| Sesión | 05 — Spark, DataFrames y transformaciones básicas |
| Tipo | `GUIDED` |
| Compatibilidad | `PRACTICO_CONDICIONAL` con fallback `PRACTICO_FREE` |
| Duración sugerida | 75 a 90 minutos |
| Datos | 10,000 pólizas sintéticas |
| Nivel | Fundamental |

## Objetivo

El participante aprenderá a:

- cargar manualmente un archivo CSV en Amazon S3;
- definir objetos y columnas mediante DDL;
- leer una fuente CSV con Spark;
- inspeccionar y transformar un DataFrame con funciones básicas de PySpark;
- usar `col()` de manera consistente para referirse a las columnas;
- guardar el resultado como una tabla Delta cuyos archivos residen en S3;
- consultar el resultado con Spark SQL;
- reconocer `_delta_log` y los archivos Parquet de una tabla Delta.

## Flujo del laboratorio

```text
data/polizas_10000.csv
          |
          | carga manual
          v
s3://<S3_BUCKET>/landing/polizas/polizas_10000.csv
          |
          | lectura y transformación con PySpark
          v
s3://<S3_BUCKET>/bronze/polizas_delta/
          |
          +-- _delta_log/
          +-- part-*.parquet
          |
          v
workspace.bronze.polizas
          |
          v
consultas con Spark SQL
```

## Archivos incluidos

| Archivo | Uso |
| --- | --- |
| `data/polizas_10000.csv` | CSV listo para cargar manualmente en S3 |
| `00_carga_manual_s3.md` | Instrucciones de carga y verificación en S3 |
| `01_ddl_tablas.sql` | DDL separado para el schema y la tabla Delta Bronze |
| `02_etl_pyspark.py` | ETL comentado con las funciones principales de DataFrames |
| `03_spark_sql.sql` | Módulo de consultas y transformaciones básicas con Spark SQL |
| `scripts/generar_polizas.py` | Regenera el CSV de manera reproducible |

## Datos sintéticos y defectos controlados

El archivo contiene exactamente 10,000 filas de datos, además del encabezado.
No contiene información real de personas ni de la aseguradora.

Para que la limpieza tenga un propósito visible, incluye:

- filas duplicadas exactas;
- algunos canales de venta vacíos;
- estados, monedas y canales con espacios o minúsculas;
- fechas y primas almacenadas como texto en el archivo de Landing.

Landing no se registra como schema ni como tabla: es únicamente el prefijo
físico donde se carga manualmente el archivo. El ETL lee ese CSV y escribe la
primera capa de datos como una tabla Delta Bronze.

## Orden de ejecución

1. Cargue `data/polizas_10000.csv` en S3 siguiendo `00_carga_manual_s3.md`.
2. Importe `01_ddl_tablas.sql` como notebook SQL.
3. Reemplace todas las apariciones de `<S3_BUCKET>`.
4. Ejecute el DDL para crear el schema y la tabla Delta Bronze.
5. Importe y ejecute `02_etl_pyspark.py` como notebook Python.
6. Importe y ejecute `03_spark_sql.sql` como notebook SQL.
7. Verifique en S3 la carpeta `bronze/polizas_delta/`.

No escriba Access Keys, Secret Keys ni tokens en los notebooks. El instructor
debe configurar previamente el acceso mediante Unity Catalog e IAM con mínimo
privilegio.

## Uso consistente de `col()`

En el ETL, las expresiones sobre columnas usan una sola forma:

```python
col("nombre_columna")
```

Por ejemplo:

```python
polizas_df.select(col("id_poliza"), col("prima"))
polizas_df.filter(col("estado_poliza") == "ACTIVA")
```

Esto evita mezclar estilos como `df.columna`, `df["columna"]` y
`col("columna")` durante una clase introductoria. Algunos métodos que reciben
configuración, como `fillna`, utilizan nombres de columnas como claves porque
esa es la interfaz propia del método; no son expresiones Spark.

## Resultado esperado

| Comprobación | Resultado esperado |
| --- | ---: |
| Filas del CSV | 10,000 |
| Filas duplicadas eliminadas | 25 |
| Filas finales en Bronze | 9,975 |
| Canales vacíos reemplazados | 40 |
| Productos | 5 |
| Monedas normalizadas | `PEN`, `USD` |

## Opción A — práctica principal

La fuente CSV y la tabla Delta se almacenan físicamente en Amazon S3. Databricks
accede a los prefijos mediante una external location o la configuración
autorizada por el instructor.

## Opción B — fallback para Free Edition

Si el workspace no puede acceder directamente a S3:

1. Cree un Volume administrado, por ejemplo
   `/Volumes/workspace/default/laboratorio_05/`.
2. Cargue manualmente el CSV en una carpeta `landing/polizas/` del Volume.
3. En los tres notebooks, sustituya:

   ```text
   s3://<S3_BUCKET>/landing/polizas/
   s3://<S3_BUCKET>/bronze/polizas_delta/
   ```

   por rutas dentro del Volume.
4. Si no puede crear un Volume, cargue el archivo con **Create table from local
   files** y ejecute las secciones de transformación y consulta sobre esa tabla.

El fallback conserva el aprendizaje de DataFrames, SQL y Delta, aunque la
verificación física se realice en almacenamiento administrado.

## Qué cambia en producción

En producción se reemplazaría la carga manual por un proceso automatizado e
incremental, se agregarían controles de calidad, alertas e idempotencia, y se
evitaría `overwrite` salvo en una recarga completa controlada. El acceso a S3
se concedería mediante roles de IAM y ubicaciones gobernadas, nunca mediante
credenciales incluidas en el código.

## Regenerar el CSV

Desde la raíz del repositorio:

```bash
python3 sessions/session-05-spark-dataframes-transformaciones/resources/laboratorio-05-s3-delta/scripts/generar_polizas.py
```
