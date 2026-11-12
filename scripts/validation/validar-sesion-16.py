"""Comprueba Excel, exportación por ambiente, relaciones y SQL S16 con Spark local.

Requiere openpyxl, PySpark y Java. Sustituye Delta por Parquet y Unity Catalog
por un schema local. No valida privilegios, PK/FK de UC, Genie ni el dashboard.
"""

import copy
import importlib.util
import os
import re
import tempfile
from decimal import Decimal
from pathlib import Path

from pyspark.sql import SparkSession

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("generador_s16", ROOT / "scripts/generate-data/generar-sesion-16.py")
generador = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generador)


def sentencias(ruta):
    texto = "\n".join(l for l in ruta.read_text(encoding="utf-8").splitlines()
                      if not l.lstrip().startswith("--"))
    return [s.strip() for s in re.split(r";(?=(?:[^']*'[^']*')*[^']*$)", texto) if s.strip()]


def rechaza(datos, ambiente="DEV"):
    try:
        generador.validar(datos, ambiente)
    except ValueError:
        return
    raise AssertionError("Se aceptó una configuración o un dato inválido")


def main():
    datos = generador.leer_excel(generador.DESTINO / "matricula-data-product.xlsx")
    assert datos == generador.datos_base(), "El Excel ya no coincide con la referencia publicada"
    generador.validar(datos, "DEV")
    rechaza(datos, "TEST")
    malos = copy.deepcopy(datos)
    malos["dim_producto"].append(malos["dim_producto"][0])
    rechaza(malos)
    malos = copy.deepcopy(datos)
    fila = list(malos["fact_siniestros"][0]); fila[2] = 999
    malos["fact_siniestros"][0] = tuple(fila)
    rechaza(malos)
    malos = copy.deepcopy(datos)
    fila = list(malos["fact_siniestros"][0]); fila[6] = Decimal("-1.00")
    malos["fact_siniestros"][0] = tuple(fila)
    rechaza(malos)
    malos = copy.deepcopy(datos)
    fila = list(malos["ambientes"][1]); fila[2] = "workspace"
    malos["ambientes"][1] = tuple(fila)
    rechaza(malos)

    os.environ.setdefault("SPARK_LOCAL_IP", "127.0.0.1")
    with tempfile.TemporaryDirectory(prefix="validar-s16-") as temporal:
        base = Path(temporal)
        # Demuestra que el mismo código puede apuntar a TEST sin generar destinos DEV.
        pruebas = copy.deepcopy(datos)
        fila = list(pruebas["ambientes"][1]); fila[4] = "SI"
        pruebas["ambientes"][1] = tuple(fila)
        generador.exportar(pruebas, "TEST", base / "test")
        ddl_test = (base / "test/sql/00-crear-esquema-y-tablas.sql").read_text()
        assert "CREATE SCHEMA seguros_test.s16" in ddl_test
        assert "CREATE TABLE workspace.s16" not in ddl_test
        assert "'training.codigo_dp'='DP-SEG-016'" in ddl_test
        assert "'training.ambiente'='TEST'" in ddl_test

        # El SQL versionado debe corresponder exactamente al Excel distribuido.
        generador.exportar(datos, "DEV", base / "dev")
        for carpeta in ("sql", "csv"):
            for archivo in (base / "dev" / carpeta).iterdir():
                assert archivo.read_bytes() == (generador.DESTINO / carpeta / archivo.name).read_bytes(), archivo.name

        spark = (SparkSession.builder.master("local[1]").appName("validar-s16")
                 .config("spark.ui.enabled", "false")
                 .config("spark.ui.showConsoleProgress", "false")
                 .config("spark.sql.catalogImplementation", "in-memory")
                 .config("spark.sql.warehouse.dir", str(base / "warehouse"))
                 .config("spark.local.dir", str(base / "scratch"))
                 .config("spark.sql.shuffle.partitions", "1").getOrCreate())
        spark.sparkContext.setLogLevel("ERROR")
        try:
            sql = generador.DESTINO / "sql"

            def ejecutar(texto):
                adaptado = texto.replace("workspace.s16", "s16_local").replace("USING DELTA", "USING PARQUET")
                return [tuple(f) for f in spark.sql(adaptado).collect()]

            for nombre in ("00-crear-esquema-y-tablas.sql", "01-cargar-desde-excel.sql", "02-crear-vistas.sql"):
                for sentencia in sentencias(sql / nombre):
                    ejecutar(sentencia)
            print("SQL de creación, carga y vistas ejecutado.", flush=True)
            consultas = sentencias(sql / "03-validar-y-consultar.sql")
            resultados = [ejecutar(s) for s in consultas]
            print("KPIs:", resultados[2], "Por producto:", resultados[3], flush=True)
            assert len(resultados) == 10
            assert dict(resultados[0]) == {
                "matricula": 1, "ambientes": 4, "proceso": 1,
                "dim_fecha": 12, "dim_producto": 3, "dim_canal": 3, "dim_estado": 2,
                "fact_polizas": 108, "fact_siniestros": 216, "vw_indicadores": 108}
            assert len(resultados[1]) == 4 and {r[0] for r in resultados[1]} == {"DP-SEG-016"}
            assert resultados[2] == [(23220, Decimal("9846000.00"), 2328, 1770,
                                      Decimal("1546800.00"), Decimal("946800.00"), Decimal("76.03"))]
            assert resultados[3] == [("AUTO", 798, Decimal("630600.00")),
                                      ("HOGAR", 432, Decimal("477900.00")),
                                      ("SALUD", 1098, Decimal("438300.00"))]
            assert [r[1] for r in resultados[4]] == list(range(150, 239, 8))
            assert resultados[5] == [(135, Decimal("81000.00"), 25, Decimal("20500.00"), Decimal("80.00"))]
            assert resultados[6] == [("ABIERTO", 558), ("CERRADO", 1770)]
            assert len(resultados[7]) == 7 and all(r[1] == 0 for r in resultados[7])
            assert resultados[8] == [] and resultados[9] == [(0, 0, 0, 0)]
            assert len(ejecutar(sentencias(sql / "04-dataset-dashboard.sql")[0])) == 108
            # La carga repetida no duplica hechos ni indicadores.
            for sentencia in sentencias(sql / "01-cargar-desde-excel.sql"):
                ejecutar(sentencia)
            assert ejecutar(consultas[2]) == resultados[2]
            # Si solo existe un lado del grupo, la vista debe conservar el otro.
            valores = ",".join("(" + ",".join(generador.literal(v) for v in fila) + ")"
                               for fila in datos["fact_polizas"][1:])
            ejecutar("INSERT OVERWRITE s16_local.fact_polizas VALUES " + valores)
            fila = ejecutar("SELECT cantidad_polizas_emitidas, cantidad_siniestros FROM s16_local.vw_indicadores WHERE id_fecha=20250101 AND id_producto=1 AND id_canal=1")
            assert fila == [(0, 25)], "La vista perdió un grupo presente solo en siniestros"
            print("OK: un Data Product, proceso, cuatro ambientes y exportación aislada a TEST.")
            print("OK: Excel y CSV/SQL coherentes; 7 relaciones; 10 consultas y filtros correctos.")
            print("OK: recarga sin duplicación y combinación de hechos sin multiplicar montos.")
            print("Pendiente en Databricks: Delta, Unity Catalog, Genie y dashboard.")
        finally:
            spark.stop()


if __name__ == "__main__":
    main()
