#!/usr/bin/env python3
"""Genera un recorte reproducible del universo de pólizas de la sesión 05."""

import csv
from datetime import date, datetime, timedelta
from pathlib import Path


DESTINO = (
    Path(__file__).resolve().parents[2]
    / "assessments/lab-01/student/data/polizas_evaluacion_01.csv"
)
COLUMNAS = (
    "id_poliza", "id_asegurado", "id_producto", "fecha_inicio", "fecha_fin",
    "estado_poliza", "prima", "moneda", "canal_venta", "departamento",
    "fecha_actualizacion",
)
PRODUCTOS = ("PROD-AUTO", "PROD-VIDA", "PROD-HOGAR", "PROD-SALUD", "PROD-VIAJE")
CANALES = ("WEB", "AGENCIA", "BROKER", "CORREDOR", "BANCASEGUROS")
DEPARTAMENTOS = (
    "LIMA", "AREQUIPA", "CUSCO", "LA LIBERTAD", "PIURA", "JUNIN", "LAMBAYEQUE", "ICA"
)


def crear_fila(numero: int) -> dict[str, str]:
    """Conserva identificadores, reglas y fórmulas del generador de la sesión 05."""
    inicio = date(2024, 1, 1) + timedelta(days=(numero * 17) % 900)
    digito = numero % 10
    if digito == 0:
        estado = "CANCELADA"
    elif digito in (1, 2):
        estado = "VENCIDA"
    elif digito == 3:
        estado = "PENDIENTE"
    else:
        estado = "ACTIVA"
    moneda = "USD" if numero % 8 == 0 else "PEN"
    canal = "" if numero <= 40 else CANALES[(numero - 1) % len(CANALES)]
    if numero % 97 == 0:
        estado = f" {estado.lower()} "
    if numero % 131 == 0:
        moneda = f" {moneda.lower()} "
    if numero > 40 and numero % 149 == 0:
        canal = f" {canal.lower()} "
    # Aritmética entera para evitar diferencias de punto flotante en importes.
    prima_centimos = 25_000 + (numero * 53 + 20260930) % 475_000
    return {
        "id_poliza": f"POL-{numero:05d}",
        "id_asegurado": f"ASE-{numero:05d}",
        "id_producto": PRODUCTOS[(numero - 1) % len(PRODUCTOS)],
        "fecha_inicio": inicio.isoformat(),
        "fecha_fin": (inicio + timedelta(days=364)).isoformat(),
        "estado_poliza": estado,
        "prima": f"{prima_centimos // 100}.{prima_centimos % 100:02d}",
        "moneda": moneda,
        "canal_venta": canal,
        "departamento": DEPARTAMENTOS[(numero * 3) % len(DEPARTAMENTOS)],
        "fecha_actualizacion": (
            datetime(2026, 9, 30, 8) + timedelta(seconds=(numero * 11) % 36000)
        ).strftime("%Y-%m-%d %H:%M:%S"),
    }


def main() -> None:
    filas = [crear_fila(numero) for numero in range(1, 476)]
    filas.extend(dict(fila) for fila in filas[:25])
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    with DESTINO.open("w", encoding="utf-8", newline="") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=COLUMNAS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(filas)
    print(f"Generado: {DESTINO} ({len(filas)} filas sintéticas)")


if __name__ == "__main__":
    main()
