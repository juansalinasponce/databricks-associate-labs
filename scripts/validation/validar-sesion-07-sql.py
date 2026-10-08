"""Verifica el SQL incremental con DuckDB 1.4.3, sin Spark ni acceso cloud.

Ejecuta INSERT, MERGE y controles reales de los archivos SQL con conexiones
independientes. Adapta el DDL Delta/S3 a tablas locales, DATEDIFF y assert_true.
COPY INTO se simula con un registro local de archivos cargados; esta prueba
no verifica el historial COPY de Databricks, Delta, volumen, permisos S3 ni Jobs reales.
"""

import csv
import re
import shutil
import tempfile
from decimal import Decimal
from pathlib import Path

import duckdb

from validar_sesion_07_esperados import ESPERADO

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / 'sessions/session-07-agregaciones-joins-spark-sql/resources/laboratorio-07-agregaciones-joins'
SQL_LOTE = ['01-cargar-bronze.sql', '02-preparar-lote.sql', '03-actualizar-detalle.sql',
            '04-actualizar-indicadores.sql', '05-validar-carga.sql']



def sentencias(path):
    text = '\n'.join(line for line in path.read_text().splitlines() if not line.lstrip().startswith('--'))
    return [sql.strip() for sql in re.split(r";(?=(?:[^']*'[^']*')*[^']*$)", text) if sql.strip()]


def adaptar(sql):
    sql = sql.replace('workspace.bronze.', 'bronze.').replace('workspace.bronze', 'bronze')
    sql = sql.replace('CURRENT_TIMESTAMP()', 'CURRENT_TIMESTAMP')
    sql = re.sub(r"\nUSING DELTA\s+LOCATION '[^']+'\s+COMMENT '[^']+'", '', sql)
    sql = re.sub(r'DATEDIFF\((\w+),\s*(\w+)\)', r"DATE_DIFF('day', \2, \1)", sql)
    return sql


def copiar_archivos(con, sql, landing):
    target, entity = re.search(r"COPY INTO (\S+).*?FROM '/Volumes/workspace/bronze/s07_archivos/(\w+)/'", sql, re.DOTALL).groups()
    target = target.replace('workspace.bronze.', 'bronze.')
    assert "'force' = 'false'" in sql and "'inferSchema' = 'false'" in sql
    assert 'CURRENT_DATE() AS fecha_carga' in sql
    fecha_servidor = con.execute('SELECT CURRENT_DATE()').fetchone()[0]
    for path in sorted((landing / entity).glob('*.csv')):
        key = entity + '/' + path.name
        if con.execute('SELECT COUNT(*) FROM loaded_files WHERE target = ? AND path = ?', [target, key]).fetchone()[0]:
            continue
        with path.open(newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            columns = next(reader)
            rows = [(*tuple(value or None for value in row), fecha_servidor) for row in reader]
        values = ', '.join('?' for _ in [*columns, 'fecha_carga'])
        con.executemany(f'INSERT INTO {target} VALUES ({values})', rows)
        con.execute('INSERT INTO loaded_files VALUES (?, ?)', [target, key])


def ejecutar(database, name, landing):
    # Una conexion por archivo demuestra que el flujo depende de tablas persistentes.
    with duckdb.connect(str(database)) as con:
        con.execute("CREATE OR REPLACE MACRO assert_true(condition, message) AS CASE WHEN condition IS TRUE THEN NULL ELSE error(message) END")
        result = []
        for sql in sentencias(LAB / name):
            if sql.startswith(('USE ', 'DESCRIBE DETAIL', 'CREATE EXTERNAL VOLUME', 'DESCRIBE VOLUME')):
                continue
            if sql.startswith('COPY INTO'):
                copiar_archivos(con, sql, landing)
                continue
            result.append((sql, con.execute(adaptar(sql)).fetchall()))
        return result


def publicar(landing, lote):
    for entity in ['polizas', 'productos', 'siniestros']:
        folder = landing / entity
        folder.mkdir(exist_ok=True)
        shutil.copyfile(LAB / 'data' / entity / f'{entity}_{lote}.csv', folder / f'{entity}_{lote}.csv')


def estado(database):
    with duckdb.connect(str(database)) as con:
        tables = con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'bronze' ORDER BY table_name").fetchall()
        return {name: sorted(con.execute('SELECT * FROM bronze.' + name).fetchall(), key=repr) for (name,) in tables}


def main():
    with tempfile.TemporaryDirectory(prefix='sesion07-sql-') as temp:
        database = Path(temp) / 'validacion.duckdb'
        landing = Path(temp) / 'landing'
        landing.mkdir()
        with duckdb.connect(str(database)) as con:
            con.execute('CREATE TABLE loaded_files (target VARCHAR, path VARCHAR)')
        ejecutar(database, '00-crear-tablas-s3.sql', landing)
        for lote, raw_counts in [('2026-10-06', (13, 4, 10)), ('2026-10-07', (18, 5, 15))]:
            publicar(landing, lote)
            for name in SQL_LOTE:
                ejecutar(database, name, landing)
                if name == '01-cargar-bronze.sql' and lote == '2026-10-07':
                    try:
                        ejecutar(database, '05-validar-carga.sql', landing)
                    except duckdb.Error as error:
                        assert 'Falta aplicar cambios' in str(error), error
                    else:
                        raise AssertionError('Se cerro una entrega antes de aplicar sus cambios')
                    print('OK: no se permite cerrar una entrega antes de aplicar los cambios')
            actual = estado(database)
            assert [len(actual['s07_bronze_' + e]) for e in ['polizas','productos','siniestros']] == list(raw_counts)
            with duckdb.connect(str(database)) as con:
                assert con.execute('SELECT * FROM bronze.s07_gold_cartera ORDER BY id_producto').fetchall() == ESPERADO[lote]
                assert con.execute('SELECT COUNT(*) FROM bronze.s07_control_lotes WHERE id_lote = ?', [lote]).fetchone()[0] == 1
                assert con.execute('SELECT COUNT(*) FROM bronze.s07_entregas_pendientes').fetchone()[0] == 0
                for entity in ['polizas', 'productos', 'siniestros']:
                    assert con.execute(f'SELECT COUNT(*) FROM bronze.s07_bronze_{entity} WHERE fecha_carga != CURRENT_DATE() OR fecha_carga IS NULL').fetchone()[0] == 0
            consultas = ejecutar(database, '06-consultas-negocio.sql', landing)
            joins = [rows for sql,rows in consultas if 'JOIN' in sql]
            assert [len(rows) for rows in joins] == ([11,12,12,13,12] if lote.endswith('06') else [12,13,13,14,13])
            ranking = next(rows for sql,rows in consultas if 'QUALIFY posicion' in sql)
            assert len(ranking) == 7
            expected_first = [('P01','POL002',Decimal('1500'),1), ('P02','POL007',Decimal('1200'),1), ('P03','POL010',Decimal('900'),1), ('P99','POL012',Decimal('500'),1)]
            expected_second = [('P01','POL002',Decimal('1600'),1), ('P02','POL013',Decimal('1400'),1), ('P03','POL007',Decimal('1200'),1), ('P99','POL012',Decimal('500'),1)]
            assert [row for row in ranking if row[-1] == 1] == (expected_first if lote.endswith('06') else expected_second)
            for name in SQL_LOTE:
                ejecutar(database, name, landing)
            assert estado(database) == actual, 'Reejecutar el mismo lote cambio las tablas'
            print(f'OK {lote}: metricas completas, joins, ranking, archivos nuevos y reejecucion sin cambios', flush=True)
        # Reprocesar una entrega anterior no debe retroceder el estado vigente.
        before = estado(database)
        for name in SQL_LOTE:
            ejecutar(database, name, landing)
        assert estado(database) == before
        print('OK: ejecutar sin archivos nuevos conserva versiones vigentes y totales actuales')

        # Caso limite: mover la unica poliza de P99 deja ese producto sin cartera.
        for entity, key, value in [('polizas','id_poliza','POL012'), ('productos','id_producto','P01'), ('siniestros','id_siniestro','SIN001')]:
            with (LAB / 'data' / entity / f'{entity}_2026-10-06.csv').open(newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                columns = reader.fieldnames
                row = next(row for row in reader if row[key] == value)
            row['id_lote'] = '2026-10-08'
            row['fecha_actualizacion'] = '2026-10-08 09:00:00'
            if entity == 'polizas':
                row['id_producto'] = 'P01'
            with (landing / entity / f'{entity}_2026-10-08.csv').open('w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=columns)
                writer.writeheader()
                writer.writerow(row)
            if entity == 'polizas':
                # Detectar una entrega incompleta; conservar la pendiente para recuperarla.
                try:
                    ejecutar(database, '01-cargar-bronze.sql', landing)
                except duckdb.Error as error:
                    assert 'Falta el archivo' in str(error), error
                else:
                    raise AssertionError('Se acepto una entrega incompleta')
                partial = estado(database)
                assert partial['s07_gold_cartera'] == before['s07_gold_cartera']
                assert partial['s07_control_lotes'] == before['s07_control_lotes']
                assert len(partial['s07_entregas_pendientes']) == 1
                print('OK: una entrega incompleta se rechaza y queda pendiente para recuperar')
        for name in SQL_LOTE:
            ejecutar(database, name, landing)
        with duckdb.connect(str(database)) as con:
            assert con.execute("SELECT COUNT(*) FROM bronze.s07_gold_cartera WHERE id_producto = 'P99'").fetchone()[0] == 0
            assert con.execute("SELECT prima_total FROM bronze.s07_gold_cartera WHERE id_producto = 'P01'").fetchone()[0] == 5400
            assert con.execute('SELECT SUM(prima_total) FROM bronze.s07_gold_cartera').fetchone()[0] == 13000
        stable = estado(database)
        for name in SQL_LOTE:
            ejecutar(database, name, landing)
        assert estado(database) == stable
        print('OK: retirar el indicador de un producto sin cartera conserva la prima total y admite reejecucion')
        # Una falla en los indicadores debe impedir dar por validado el resultado.
        with duckdb.connect(str(database)) as con:
            con.execute("UPDATE bronze.s07_gold_cartera SET prima_total = prima_total + 1 WHERE id_producto = 'P01'")
        try:
            ejecutar(database, '05-validar-carga.sql', landing)
        except duckdb.Error as error:
            assert 'Revisar prima total' in str(error), error
        else:
            raise AssertionError('El validador no detecto un indicador incorrecto')
        print('OK: el control SQL rechaza un indicador incorrecto')

        # Ambas entregas se suben antes de ejecutar: los MERGE no deben recibir claves duplicadas.
        combined = Path(temp) / 'combinado.duckdb'
        combined_landing = Path(temp) / 'combinado'
        combined_landing.mkdir()
        with duckdb.connect(str(combined)) as con:
            con.execute('CREATE TABLE loaded_files (target VARCHAR, path VARCHAR)')
        ejecutar(combined, '00-crear-tablas-s3.sql', combined_landing)
        for entrega in ['2026-10-06', '2026-10-07']:
            publicar(combined_landing, entrega)
        for name in SQL_LOTE:
            ejecutar(combined, name, combined_landing)
        with duckdb.connect(str(combined)) as con:
            assert con.execute('SELECT * FROM bronze.s07_gold_cartera ORDER BY id_producto').fetchall() == ESPERADO['2026-10-07']
            assert con.execute('SELECT COUNT(*) FROM bronze.s07_control_lotes').fetchone()[0] == 2
        combined_state = estado(combined)
        for name in SQL_LOTE:
            ejecutar(combined, name, combined_landing)
        assert estado(combined) == combined_state
        print('OK: dos entregas en la misma ejecucion, fecha del servidor y reejecucion sin parametros')


if __name__ == '__main__':
    main()
