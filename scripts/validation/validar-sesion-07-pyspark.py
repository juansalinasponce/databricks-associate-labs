"""Verifica los archivos del alumno con Spark 3.5 y Delta Lake 3.2 locales.

Requiere pyspark, delta-spark y S07_DELTA_JARS con los jars delta-spark y
delta-storage separados por coma. Adapta solamente el catalogo workspace y
las ubicaciones S3. COPY INTO se emula con CSV y un registro de archivos.
Los DataFrames y MERGE usan Spark y Delta reales. No prueba permisos,
volumen, historial COPY INTO de Databricks ni ejecuciones Jobs remotas.
"""
import os
import re
import tempfile
from pathlib import Path

from pyspark.sql import SparkSession, functions as F

from validar_sesion_07_esperados import ESPERADO

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / 'sessions/session-07-agregaciones-joins-spark-sql/resources/laboratorio-07-agregaciones-joins'
ARCHIVOS = [
    '01-cargar-bronze.py', '02-preparar-lote.py', '03-actualizar-detalle.py',
    '04-actualizar-indicadores.py', '05-validar-carga.py',
]


def main():
    with tempfile.TemporaryDirectory(prefix='sesion07-pyspark-') as directory:
        folder = Path(directory)
        spark = (
            SparkSession.builder.master('local[2]').appName('validar-sesion-07-pyspark')
            .config('spark.jars', os.environ['S07_DELTA_JARS'])
            .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension')
            .config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog')
            .config('spark.sql.warehouse.dir', str(folder / 'warehouse'))
            .config('spark.sql.shuffle.partitions', '2')
            .config('spark.databricks.delta.snapshotPartitions', '1')
            .config('spark.sql.ansi.enabled', 'true')
            .config('spark.ui.enabled', 'false')
            .getOrCreate()
        )
        spark.sparkContext.setLogLevel('ERROR')
        native_sql = spark.sql
        native_sql('CREATE DATABASE bronze')
        ddl = (LAB / '00-crear-tablas-s3.sql').read_text()
        definitions = re.findall(
            r'CREATE TABLE IF NOT EXISTS workspace.bronze\.(\w+) \((.*?)\)\s*USING DELTA', ddl, re.S
        )
        for table, columns in definitions:
            native_sql(f"CREATE TABLE bronze.{table} ({columns}) USING DELTA LOCATION '{folder / table}'")
        assert len(definitions) == 14
        published = []
        copied = set()

        def local_sql(statement, *args, **kwargs):
            if not statement.strip().startswith('COPY INTO'):
                return native_sql(statement, *args, **kwargs)
            target, entity = re.search(
                r"COPY INTO (\S+).*?FROM '/Volumes/workspace/bronze/s07_archivos/(\w+)/'",
                statement, re.S,
            ).groups()
            assert "'force' = 'false'" in statement
            assert 'CURRENT_DATE() AS fecha_carga' in statement
            for delivery in published:
                key = (entity, delivery)
                if key in copied:
                    continue
                path = LAB / 'data' / entity / f'{entity}_{delivery}.csv'
                schema = spark.table(target).drop('fecha_carga').schema
                raw = spark.read.schema(schema).option('header', True).option('mode', 'FAILFAST').csv(str(path))
                raw.withColumn('fecha_carga', F.current_date()).write.mode('append').insertInto(target)
                copied.add(key)
            return spark.range(0)

        spark.sql = local_sql

        def run(name):
            # Cada archivo recibe un contexto Python nuevo, como una tarea independiente.
            source = (LAB / 'pyspark' / name).read_text().replace('workspace.bronze.', 'bronze.')
            exec(compile(source, name, 'exec'), {'spark': spark, 'display': lambda frame: frame.collect()})

        def state():
            return {table: sorted(spark.table('bronze.' + table).collect(), key=repr)
                    for table, _ in definitions}

        def check_gold(delivery):
            actual = [tuple(row) for row in spark.table('bronze.s07_gold_cartera').orderBy('id_producto').collect()]
            assert actual == ESPERADO[delivery], (actual, ESPERADO[delivery])
            assert spark.table('bronze.s07_entregas_pendientes').count() == 0

        try:
            for delivery, raw_counts in [('2026-10-06', [13, 4, 10]), ('2026-10-07', [18, 5, 15])]:
                published.append(delivery)
                run(ARCHIVOS[0])
                if delivery.endswith('07'):
                    try:
                        run('05-validar-carga.py')
                    except ValueError as error:
                        assert 'Falta aplicar cambios' in str(error)
                    else:
                        raise AssertionError('Se cerro una entrega sin aplicar sus cambios')
                    print('OK: cierre prematuro rechazado', flush=True)
                for name in ARCHIVOS[1:]:
                    run(name)
                check_gold(delivery)
                assert [spark.table('bronze.s07_bronze_' + entity).count()
                        for entity in ['polizas', 'productos', 'siniestros']] == raw_counts
                namespace = {'spark': spark, 'display': lambda frame: frame.collect()}
                source = (LAB / 'pyspark/06-consultas-negocio.py').read_text().replace('workspace.bronze.', 'bronze.')
                exec(compile(source, '06-consultas-negocio.py', 'exec'), namespace)
                assert namespace['ranking'].count() == 7
                join_counts = [namespace['polizas'].join(namespace['catalogo'], 'id_producto', kind).count()
                               for kind in ['inner', 'left', 'right', 'full']]
                assert join_counts == ([11, 12, 12, 13] if delivery.endswith('06') else [12, 13, 13, 14])
                before = state()
                for name in ARCHIVOS:
                    run(name)
                assert state() == before, 'Reejecutar altero las tablas'
                print(f'OK {delivery}: Gold completo, cuatro joins, ranking y reejecucion estable', flush=True)

            # Alterar un indicador debe bloquear la validacion.
            native_sql("UPDATE bronze.s07_gold_cartera SET prima_total = prima_total + 1 WHERE id_producto = 'P01'")
            try:
                run('05-validar-carga.py')
            except ValueError as error:
                assert 'Revisar prima total' in str(error)
            else:
                raise AssertionError('No se detecto el indicador alterado')
            print('OK: indicador incorrecto rechazado', flush=True)
        finally:
            spark.stop()


if __name__ == '__main__':
    main()
