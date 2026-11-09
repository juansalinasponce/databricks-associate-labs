"""Valida el dataset, la vista y las consultas reales de sesión 15 con Spark local.

Requiere PySpark y Java compatibles. Ejecutar desde cualquier carpeta:
    python3 scripts/validation/validar-sesion-15-sql.py

Adapta el catálogo a un schema local y DELTA a PARQUET. Omite COMMENT ON,
específico de Databricks en este entorno. No prueba Delta, Unity Catalog,
permisos, Free Edition, Genie ni la interfaz o publicación del dashboard.
No necesita credenciales ni conexión cloud; usa almacenamiento temporal.
"""

import datetime
import os
import re
import tempfile
from decimal import Decimal
from pathlib import Path

from pyspark.sql import SparkSession

ROOT = Path(__file__).resolve().parents[2]
SQL = ROOT / (
    "sessions/session-15-Databricks SQL + AI/BI Dashboards/"
    "resources/laboratorio-15-gold-dashboard/sql"
)


def sentencias(nombre):
    contenido = "\n".join(
        linea for linea in (SQL / nombre).read_text(encoding="utf-8").splitlines()
        if not linea.lstrip().startswith("--")
    )
    return [s.strip() for s in re.split(r";(?=(?:[^']*'[^']*')*[^']*$)", contenido)
            if s.strip()]


def adaptar(sentencia):
    return (sentencia.replace("workspace.gold_s15_seguros", "s15_gold_local")
            .replace("USING DELTA", "USING PARQUET"))


def main():
    os.environ.setdefault("SPARK_LOCAL_IP", "127.0.0.1")
    with tempfile.TemporaryDirectory(prefix="validar-sesion15-") as carpeta:
        spark = (SparkSession.builder.master("local[1]")
                 .appName("validar-sesion-15-sql")
                 .config("spark.ui.enabled", "false")
                 .config("spark.sql.catalogImplementation", "in-memory")
                 .config("spark.sql.warehouse.dir", str(Path(carpeta) / "warehouse"))
                 .config("spark.local.dir", str(Path(carpeta) / "scratch"))
                 .config("spark.sql.shuffle.partitions", "1")
                 .getOrCreate())
        spark.sparkContext.setLogLevel("ERROR")
        try:
            for nombre in ["00-preparar-gold.sql", "01-crear-vista.sql"]:
                for sentencia in sentencias(nombre):
                    if not sentencia.startswith("COMMENT ON"):
                        spark.sql(adaptar(sentencia)).collect()

            def consultar(sentencia):
                return [tuple(fila) for fila in spark.sql(adaptar(sentencia)).collect()]

            resultados = [consultar(s) for s in sentencias("02-consultas-y-validacion.sql")]
            assert len(resultados) == 8, "Faltan consultas del laboratorio"
            assert len(resultados[0]) == 72, "El dataset no contiene 72 grupos"
            assert resultados[1] == [(2328, 1770, 558, Decimal("1546800.00"),
                                      Decimal("946800.00"), Decimal("76.03"))]
            assert resultados[2] == [(datetime.date(2025, mes, 1), cantidad)
                                     for mes, cantidad in enumerate(
                                         [150, 158, 166, 174, 182, 190,
                                          198, 206, 214, 222, 230, 238], start=1)]
            assert resultados[3] == [("AUTO", Decimal("630600.00")),
                                     ("HOGAR", Decimal("477900.00")),
                                     ("SALUD", Decimal("438300.00"))]
            assert resultados[4] == [("ABIERTO", 558), ("CERRADO", 1770)]
            assert resultados[5] == [(50, Decimal("41000.00"),
                                      Decimal("20000.00"), Decimal("80.00"))]
            assert resultados[6] == [], "Hay claves duplicadas"
            assert resultados[7] == [(0,)], "Hay filas invalidas"

            esperadas = {(datetime.date(2025, mes, 1), tipo, estado)
                         for mes in range(1, 13)
                         for tipo in ["AUTO", "SALUD", "HOGAR"]
                         for estado in ["ABIERTO", "CERRADO"]}
            assert {fila[:3] for fila in resultados[0]} == esperadas
            for fila in resultados[0]:
                _, _, estado, cantidad, _, _, cerrados, corte = fila
                assert cerrados == (cantidad if estado == "CERRADO" else 0)
                assert corte == datetime.date(2025, 12, 31)

            # Repetir la carga debe conservar tanto el detalle como las métricas.
            carga = next(s for s in sentencias("00-preparar-gold.sql")
                         if s.startswith("INSERT OVERWRITE"))
            spark.sql(adaptar(carga)).collect()
            repetidos = [consultar(s) for s in sentencias("02-consultas-y-validacion.sql")]
            assert sorted(repetidos[0]) == sorted(resultados[0])
            assert repetidos[1:] == resultados[1:], "La recarga cambio los indicadores"
            print("OK: 72 grupos, 12 meses, vista, 8 consultas, KPIs y filtros correctos.")
            print("OK: recargar con INSERT OVERWRITE conserva filas e indicadores.")
            print("Pendiente en Databricks: Delta, permisos, Genie y dashboard.")
        finally:
            spark.stop()


if __name__ == "__main__":
    main()
