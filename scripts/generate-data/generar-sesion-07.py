"""Genera dos lotes CSV sintéticos para el laboratorio incremental SQL."""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / "sessions/session-07-agregaciones-joins-spark-sql/resources/laboratorio-07-agregaciones-joins"

HEADERS = {
    "polizas": [
        "id_poliza", "id_asegurado", "id_producto", "fecha_inicio", "fecha_fin",
        "estado_poliza", "prima", "moneda", "canal_venta", "departamento",
        "fecha_actualizacion",
    ],
    "productos": [
        "id_producto", "nombre_producto", "tipo_seguro", "segmento",
        "fecha_actualizacion",
    ],
    "siniestros": [
        "id_siniestro", "id_poliza", "fecha_siniestro", "fecha_reporte",
        "estado_siniestro", "monto_pagado", "fecha_actualizacion",
    ],
}

# Cada registro tiene un propósito didáctico; no se necesita aleatoriedad.
POLIZAS_BASE = [
    ("POL001", "ASE001", "P01", "2026-01-01", "2026-12-31", " activa ", "1000.00", "PEN", " digital ", "LIMA", "2026-10-06 09:00:00"),
    ("POL002", "ASE002", "P01", "2026-02-01", "2027-01-31", "ACTIVA", "1500.00", "PEN", "CORREDOR", "LIMA", "2026-10-06 09:00:00"),
    ("POL003", "ASE003", "P01", "2026-03-01", "2027-02-28", "activa", None, "PEN", None, "AREQUIPA", "2026-10-06 09:00:00"),
    ("POL004", "ASE004", "P01", "2025-01-01", "2025-12-31", " vencida ", "1200.00", "PEN", "Digital", "LIMA", "2026-10-06 09:00:00"),
    ("POL005", "ASE005", "P02", "2026-01-15", "2027-01-14", "ACTIVA", "800.00", "PEN", "AGENCIA", "LIMA", "2026-10-06 09:00:00"),
    ("POL006", "ASE006", "P02", "2026-02-15", "2027-02-14", " activa", "1000.00", "PEN", "digital", "CUSCO", "2026-10-06 09:00:00"),
    ("POL007", "ASE007", "P02", "2026-03-15", "2027-03-14", "ACTIVA", "1200.00", "PEN", "CORREDOR", "LIMA", "2026-10-06 09:00:00"),
    ("POL008", "ASE008", "P02", "2025-02-01", "2026-01-31", "VENCIDA", "1000.00", "PEN", None, "CUSCO", "2026-10-06 09:00:00"),
    ("POL009", "ASE009", "P03", "2026-04-01", "2027-03-31", "ACTIVA", "600.00", "PEN", "AGENCIA", "LIMA", "2026-10-06 09:00:00"),
    ("POL010", "ASE010", "P03", "2026-05-01", "2027-04-30", "activa ", "900.00", "PEN", "DIGITAL", "AREQUIPA", "2026-10-06 09:00:00"),
    ("POL011", "ASE011", "P03", "2026-06-01", "2027-05-31", "ACTIVA", "700.00", "PEN", "CORREDOR", "LIMA", "2026-10-06 09:00:00"),
    ("POL012", "ASE012", "P99", "2026-07-01", "2027-06-30", "ACTIVA", "500.00", "PEN", "AGENCIA", "LIMA", "2026-10-06 09:00:00"),
]

PRODUCTOS = [
    ("P01", "Seguro Auto Demo", "AUTO", "PERSONAS", "2026-09-01 08:00:00"),
    ("P02", "Seguro Salud Demo", "SALUD", "PERSONAS", "2026-09-01 08:00:00"),
    ("P03", "Seguro Hogar Demo", "HOGAR", "PERSONAS", "2026-09-01 08:00:00"),
    ("P04", "Seguro Vida Demo", "VIDA", "PERSONAS", "2026-09-01 08:00:00"),
]

SINIESTROS_BASE = [
    ("SIN001", "POL001", "2026-09-05", "2026-09-06", " cerrado ", "300.00", "2026-10-06 10:00:00"),
    ("SIN002", "POL001", "2026-09-12", "2026-09-14", "CERRADO", "500.00", "2026-10-06 10:00:00"),
    ("SIN003", "POL002", "2026-09-20", "2026-09-23", "reportado", None, "2026-10-06 10:00:00"),
    ("SIN004", "POL005", "2026-09-21", "2026-09-22", "CERRADO", "200.00", "2026-10-06 10:00:00"),
    ("SIN005", "POL006", "2026-09-25", "2026-09-28", "cerrado", "400.00", "2026-10-06 10:00:00"),
    ("SIN006", "POL009", "2026-09-27", "2026-10-01", "CERRADO", "150.00", "2026-10-06 10:00:00"),
    ("SIN007", "POL009", "2026-10-02", "2026-10-03", "CERRADO", "250.00", "2026-10-06 10:00:00"),
    ("SIN008", "POL010", "2026-10-03", "2026-10-05", "REPORTADO", "0.00", "2026-10-06 10:00:00"),
    ("SIN009", "POL999", "2026-10-04", "2026-10-06", "CERRADO", "100.00", "2026-10-06 10:00:00"),
]

# La segunda entrega contiene cambios y altas; no repite el snapshot completo.
POLIZAS_DIA_2 = [
    ("POL002", "ASE002", "P01", "2026-02-01", "2027-01-31", "ACTIVA", "1600.00", "PEN", "CORREDOR", "LIMA", "2026-10-07 09:00:00"),
    ("POL003", "ASE003", "P01", "2026-03-01", "2027-02-28", "ACTIVA", "1100.00", "PEN", None, "AREQUIPA", "2026-10-07 09:00:00"),
    ("POL007", "ASE007", "P03", "2026-03-15", "2027-03-14", "ACTIVA", "1200.00", "PEN", "CORREDOR", "LIMA", "2026-10-07 09:00:00"),
    ("POL013", "ASE013", "P02", "2026-10-07", "2027-10-06", " activa ", "1400.00", "PEN", " digital ", "LIMA", "2026-10-07 09:00:00"),
]
SINIESTROS_DIA_2 = [
    ("SIN003", "POL002", "2026-09-20", "2026-09-23", "CERRADO", "200.00", "2026-10-07 10:00:00"),
    ("SIN005", "POL007", "2026-09-25", "2026-09-28", "CERRADO", "400.00", "2026-10-07 10:00:00"),
    ("SIN010", "POL013", "2026-10-07", "2026-10-07", "CERRADO", "300.00", "2026-10-07 10:00:00"),
    ("SIN011", "POL007", "2026-10-07", "2026-10-07", "CERRADO", "150.00", "2026-10-07 10:00:00"),
]
LOTES = {
    "2026-10-06": {
        "polizas": POLIZAS_BASE + [POLIZAS_BASE[1]],
        "productos": PRODUCTOS,
        "siniestros": SINIESTROS_BASE + [SINIESTROS_BASE[0]],
    },
    "2026-10-07": {
        "polizas": POLIZAS_DIA_2 + [POLIZAS_DIA_2[3]],
        "productos": [("P03", "Seguro Hogar Integral Demo", "HOGAR", "PERSONAS", "2026-10-07 08:00:00")],
        "siniestros": SINIESTROS_DIA_2 + [SINIESTROS_DIA_2[2]],
    },
}


def main():
    for id_lote, entidades in LOTES.items():
        for entidad, filas in entidades.items():
            folder = LAB / "data" / entidad
            folder.mkdir(parents=True, exist_ok=True)
            path = folder / f"{entidad}_{id_lote}.csv"
            with path.open("w", encoding="utf-8", newline="") as archivo:
                writer = csv.writer(archivo, lineterminator="\n")
                writer.writerow(["id_lote", *HEADERS[entidad]])
                writer.writerows((id_lote, *fila) for fila in filas)
            print(f"{path.name}: {len(filas)} filas")


if __name__ == "__main__":
    main()
