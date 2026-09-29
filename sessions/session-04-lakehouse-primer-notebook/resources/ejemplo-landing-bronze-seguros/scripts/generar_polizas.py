#!/usr/bin/env python3
"""Genera 10 000 pólizas sintéticas y reproducibles para la Sesión 04."""

import csv
from datetime import date, datetime, timedelta
from pathlib import Path


TOTAL_REGISTROS = 10_000
ARCHIVO_SALIDA = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "polizas_2026_09_28.csv"
)

PRODUCTOS = ("PROD-AUTO", "PROD-VIDA", "PROD-HOGAR", "PROD-SALUD")
CANALES = ("WEB", "AGENCIA", "BROKER", "CORREDOR", "BANCASEGUROS")


def obtener_estado(numero: int) -> str:
    """Distribuye estados de forma simple y predecible."""
    ultimo_digito = numero % 10
    if ultimo_digito == 0:
        return "CANCELADA"
    if ultimo_digito in (1, 2):
        return "VENCIDA"
    if ultimo_digito == 3:
        return "PENDIENTE"
    return "ACTIVA"


def generar_filas():
    fecha_base = date(2024, 6, 1)
    actualizacion_base = datetime(2026, 9, 28, 8, 0, 0)

    for numero in range(1, TOTAL_REGISTROS + 1):
        fecha_inicio = fecha_base + timedelta(days=(numero * 13) % 500)
        fecha_fin = fecha_inicio + timedelta(days=364)
        prima = 300 + ((numero * 37) % 470_000) / 100

        yield {
            "id_poliza": f"POL-{numero:05d}",
            "id_asegurado": f"ASE-{((numero - 1) % 7_500) + 1:05d}",
            "id_producto": PRODUCTOS[(numero - 1) % len(PRODUCTOS)],
            "fecha_inicio": fecha_inicio.isoformat(),
            "fecha_fin": fecha_fin.isoformat(),
            "estado_poliza": obtener_estado(numero),
            "prima": f"{prima:.2f}",
            "moneda": "USD" if numero % 8 == 0 else "PEN",
            "canal_venta": CANALES[(numero - 1) % len(CANALES)],
            "fecha_actualizacion": (
                actualizacion_base + timedelta(seconds=numero % 28_800)
            ).strftime("%Y-%m-%d %H:%M:%S"),
        }


def main() -> None:
    ARCHIVO_SALIDA.parent.mkdir(parents=True, exist_ok=True)
    columnas = (
        "id_poliza",
        "id_asegurado",
        "id_producto",
        "fecha_inicio",
        "fecha_fin",
        "estado_poliza",
        "prima",
        "moneda",
        "canal_venta",
        "fecha_actualizacion",
    )

    with ARCHIVO_SALIDA.open("w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=columnas)
        writer.writeheader()
        writer.writerows(generar_filas())

    print(f"Archivo generado: {ARCHIVO_SALIDA}")
    print(f"Registros: {TOTAL_REGISTROS}")


if __name__ == "__main__":
    main()
