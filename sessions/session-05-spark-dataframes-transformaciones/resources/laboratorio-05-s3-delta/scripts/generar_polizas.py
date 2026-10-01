#!/usr/bin/env python3
"""Genera 10,000 pólizas sintéticas y reproducibles para el Laboratorio 05."""

import csv
from datetime import date, datetime, timedelta
from pathlib import Path


TOTAL_FILAS = 10_000
TOTAL_DUPLICADOS = 25
TOTAL_CANALES_VACIOS = 40
SEMILLA_LOGICA = 20260930

ARCHIVO_SALIDA = (
    Path(__file__).resolve().parent.parent / "data" / "polizas_10000.csv"
)

PRODUCTOS = (
    "PROD-AUTO",
    "PROD-VIDA",
    "PROD-HOGAR",
    "PROD-SALUD",
    "PROD-VIAJE",
)
CANALES = ("WEB", "AGENCIA", "BROKER", "CORREDOR", "BANCASEGUROS")
DEPARTAMENTOS = (
    "LIMA",
    "AREQUIPA",
    "CUSCO",
    "LA LIBERTAD",
    "PIURA",
    "JUNIN",
    "LAMBAYEQUE",
    "ICA",
)
COLUMNAS = (
    "id_poliza",
    "id_asegurado",
    "id_producto",
    "fecha_inicio",
    "fecha_fin",
    "estado_poliza",
    "prima",
    "moneda",
    "canal_venta",
    "departamento",
    "fecha_actualizacion",
)


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


def crear_fila(numero: int) -> dict[str, str]:
    """Crea una póliza ficticia y agrega variaciones controladas de calidad."""
    fecha_inicio = date(2024, 1, 1) + timedelta(days=(numero * 17) % 900)
    fecha_fin = fecha_inicio + timedelta(days=364)
    prima = 250 + ((numero * 53 + SEMILLA_LOGICA) % 475_000) / 100

    estado = obtener_estado(numero)
    moneda = "USD" if numero % 8 == 0 else "PEN"
    canal = CANALES[(numero - 1) % len(CANALES)]

    # Las variaciones permiten demostrar trim(), upper() y fillna().
    if numero % 97 == 0:
        estado = f" {estado.lower()} "
    if numero % 131 == 0:
        moneda = f" {moneda.lower()} "
    if numero <= TOTAL_CANALES_VACIOS:
        canal = ""
    elif numero % 149 == 0:
        canal = f" {canal.lower()} "

    return {
        "id_poliza": f"POL-{numero:05d}",
        "id_asegurado": f"ASE-{((numero - 1) % 7_500) + 1:05d}",
        "id_producto": PRODUCTOS[(numero - 1) % len(PRODUCTOS)],
        "fecha_inicio": fecha_inicio.isoformat(),
        "fecha_fin": fecha_fin.isoformat(),
        "estado_poliza": estado,
        "prima": f"{prima:.2f}",
        "moneda": moneda,
        "canal_venta": canal,
        "departamento": DEPARTAMENTOS[(numero * 3) % len(DEPARTAMENTOS)],
        "fecha_actualizacion": (
            datetime(2026, 9, 30, 8, 0, 0)
            + timedelta(seconds=(numero * 11) % 36_000)
        ).strftime("%Y-%m-%d %H:%M:%S"),
    }


def generar_filas():
    """Produce 9,975 pólizas únicas y 25 duplicados exactos: 10,000 filas."""
    filas_unicas = [
        crear_fila(numero)
        for numero in range(1, TOTAL_FILAS - TOTAL_DUPLICADOS + 1)
    ]

    yield from filas_unicas
    yield from filas_unicas[:TOTAL_DUPLICADOS]


def main() -> None:
    ARCHIVO_SALIDA.parent.mkdir(parents=True, exist_ok=True)

    with ARCHIVO_SALIDA.open("w", newline="", encoding="utf-8") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        writer.writeheader()
        writer.writerows(generar_filas())

    print(f"Archivo generado: {ARCHIVO_SALIDA}")
    print(f"Filas de datos: {TOTAL_FILAS}")
    print(f"Duplicados exactos: {TOTAL_DUPLICADOS}")
    print(f"Canales vacíos en filas únicas: {TOTAL_CANALES_VACIOS}")


if __name__ == "__main__":
    main()
