"""Crea la plantilla S16 o exporta su Excel editado a SQL y CSV, sin conexión cloud.

Requiere openpyxl. Sin --excel crea la plantilla inicial; nunca la sobrescribe.
Con --excel valida y exporta el libro existente para un único ambiente.
"""

import argparse
import csv
import datetime as dt
import re
from decimal import Decimal
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo

ROOT = Path(__file__).resolve().parents[2]
DESTINO = (Path(__file__).resolve().parent.parent if Path(__file__).parent.name == "herramientas"
           else ROOT / "sessions/session-16-Genie/resources/laboratorio-16-data-product")
CODIGO = "DP-SEG-016"
CORTE = dt.date(2025, 12, 31)

# El contrato es fijo para concentrar la clase en matrícula, relaciones y consumo.
ESQUEMAS = {
    "matricula": [
        ("codigo_dp", "STRING", "Identificador estable del único Data Product"),
        ("nombre", "STRING", "Nombre técnico del Data Product"),
        ("dominio", "STRING", "Dominio de negocio ficticio"),
        ("owner_negocio", "STRING", "Rol responsable del producto; no concede permisos UC"),
        ("steward", "STRING", "Rol que revisa definiciones y calidad"),
        ("descripcion", "STRING", "Necesidad que resuelve"),
        ("consumidores", "STRING", "Roles consumidores ficticios"),
        ("freshness_objetivo", "STRING", "Objetivo de actualización; no programa ejecuciones"),
        ("calidad", "STRING", "Reglas del contrato de datos"),
        ("seguridad", "STRING", "Clasificación y acceso previsto"),
        ("slo_objetivo", "STRING", "Objetivo didáctico, no garantía de Free Edition"),
        ("version_contrato", "STRING", "Versión del contrato, independiente del ambiente"),
        ("estado", "STRING", "Estado documental de la matrícula"),
        ("fecha_corte", "DATE", "Fecha de referencia del dataset histórico"),
        ("fuente", "STRING", "Origen sintético de referencia"),
    ],
    "ambientes": [
        ("codigo_dp", "STRING", "Mismo código en todos los ambientes"),
        ("ambiente", "STRING", "DEV, TEST, UAT o PRD"),
        ("catalogo", "STRING", "Catálogo existente autorizado; el script no lo crea"),
        ("esquema", "STRING", "Schema que se creará en el catálogo seleccionado"),
        ("habilitado", "STRING", "SI permite generar SQL; NO conserva solo la referencia"),
        ("nombre_genie", "STRING", "Nombre propuesto; se crea manualmente en la UI"),
        ("nombre_dashboard", "STRING", "Nombre propuesto; se crea manualmente en la UI"),
    ],
    "proceso": [
        ("codigo_proceso", "STRING", "Identificador estable del proceso de referencia"),
        ("codigo_dp", "STRING", "Data Product que publica el proceso"),
        ("nombre", "STRING", "Nombre del proceso de publicación"),
        ("entrada", "STRING", "Fuente de los datos de referencia"),
        ("pasos", "STRING", "Validación y publicación que realiza el proceso"),
        ("salida", "STRING", "Activos que consume el negocio en el ambiente seleccionado"),
        ("ejecucion", "STRING", "Modo efectivo de ejecución; no crea un Job"),
        ("responsable", "STRING", "Rol técnico ficticio"),
    ],
    "dim_fecha": [
        ("id_fecha", "INT", "PK mensual YYYYMM01"),
        ("mes_referencia", "DATE", "Primer día del mes: reporte de siniestros o emisión de pólizas"),
        ("anio", "INT", "Año del mes de referencia"),
        ("mes", "INT", "Número de mes para ordenar"),
        ("nombre_mes", "STRING", "Etiqueta del mes; ordenar por mes_referencia"),
    ],
    "dim_producto": [
        ("id_producto", "INT", "PK del producto ficticio"),
        ("nombre_producto", "STRING", "Nombre del producto de referencia"),
        ("tipo_seguro", "STRING", "AUTO, SALUD o HOGAR"),
    ],
    "dim_canal": [
        ("id_canal", "INT", "PK del canal ficticio"),
        ("canal", "STRING", "Canal atribuido al grupo de pólizas o siniestros"),
    ],
    "dim_estado": [
        ("id_estado", "INT", "PK del estado al corte"),
        ("estado_siniestro", "STRING", "ABIERTO o CERRADO al 2025-12-31"),
    ],
    "fact_polizas": [
        ("id_hecho_poliza", "INT", "PK técnica del grupo; no es un id de póliza individual"),
        ("id_fecha", "INT", "FK a dim_fecha: mes de emisión"),
        ("id_producto", "INT", "FK a dim_producto"),
        ("id_canal", "INT", "FK a dim_canal"),
        ("cantidad_polizas_emitidas", "INT", "Cantidad de emisiones del grupo: usar SUM"),
        ("prima_emitida", "DECIMAL(18,2)", "Prima de las emisiones del grupo en PEN"),
        ("moneda", "STRING", "PEN; no mezclar monedas"),
    ],
    "fact_siniestros": [
        ("id_hecho_siniestro", "INT", "PK técnica del grupo; no es un id de siniestro individual"),
        ("id_fecha", "INT", "FK a dim_fecha: mes de reporte, no fecha de pago ni cierre"),
        ("id_producto", "INT", "FK a dim_producto"),
        ("id_canal", "INT", "FK a dim_canal"),
        ("id_estado", "INT", "FK a dim_estado: estado al corte"),
        ("cantidad_siniestros", "INT", "Cantidad de siniestros del grupo: usar SUM"),
        ("monto_pagado", "DECIMAL(18,2)", "Pago acumulado al corte en PEN, por cohorte de reporte"),
        ("monto_reservado", "DECIMAL(18,2)", "Saldo pendiente ficticio en PEN, sin regla actuarial"),
        ("fecha_corte", "DATE", "Corte único 2025-12-31; no sumar snapshots"),
        ("moneda", "STRING", "PEN; no mezclar monedas"),
    ],
}
DESCRIPCIONES = {
    "matricula": "Una fila: matrícula de un Data Product de referencia.",
    "ambientes": "Cuatro referencias de ambiente para el mismo Data Product; no implica despliegue.",
    "proceso": "Un proceso de referencia que publica el único Data Product; ejecución manual.",
    "dim_fecha": "Una fila por mes de 2025; dimensión mensual compartida.",
    "dim_producto": "Una fila por producto ficticio; no es el registro de Data Products.",
    "dim_canal": "Una fila por canal ficticio.",
    "dim_estado": "Una fila por estado de siniestro al corte 2025-12-31.",
    "fact_polizas": "Una fila por mes de emisión, producto y canal; emisiones de 2025.",
    "fact_siniestros": "Una fila por mes de reporte, producto, canal y estado al corte 2025-12-31.",
}
RELACIONES = [
    (hecho, columna, dimension, columna)
    for hecho in ("fact_polizas", "fact_siniestros")
    for columna, dimension in (("id_fecha", "dim_fecha"),
                              ("id_producto", "dim_producto"), ("id_canal", "dim_canal"))
] + [("fact_siniestros", "id_estado", "dim_estado", "id_estado")]


def datos_base():
    """Conserva los totales S15 y distribuye sus grupos en tres canales ficticios."""
    meses = "Enero Febrero Marzo Abril Mayo Junio Julio Agosto Septiembre Octubre Noviembre Diciembre".split()
    datos = {
        "matricula": [(CODIGO, "dp_siniestros_operativos", "Siniestros", "Operaciones demo",
                       "Calidad demo", "Indicadores de siniestros y contexto de emisión de pólizas",
                       "Supervisor demo; Analista demo", "Diaria a las 08:00 America/Lima (objetivo)",
                       "PK únicas; FK válidas; cantidades y montos >= 0; PEN; corte único",
                       "Sintético; uso formativo; lectura según permisos Unity Catalog",
                       "99% de cargas antes de 08:00 (referencia conceptual sin SLA contratado)",
                       "1.0.0", "REFERENCIA", CORTE, "S15 sintético + canales y emisiones sintéticos")],
        "ambientes": [(CODIGO, env, cat, "s16", "SI" if env == "DEV" else "NO",
                       f"{CODIGO} - {env} - Genie", f"{CODIGO} - {env} - Dashboard")
                      for env, cat in (("DEV", "workspace"), ("TEST", "seguros_test"),
                                       ("UAT", "seguros_uat"), ("PRD", "seguros_prd"))],
        "proceso": [("PRC-SEG-016", CODIGO, "Publicación de indicadores de seguros",
                     "Hojas de matrícula, dimensiones y hechos de este Excel",
                     "Validar contrato → exportar SQL → crear s16 → cargar → publicar vistas → verificar KPIs",
                     "<catalogo>.s16.vw_indicadores; Genie; AI/BI Dashboard",
                     "Manual para la clase; sin Job ni programación activa", "Ingeniería de datos demo")],
        "dim_fecha": [(20250001 + mes * 100, dt.date(2025, mes, 1), 2025, mes, nombre)
                      for mes, nombre in enumerate(meses, 1)],
        "dim_producto": [(1, "Auto demo", "AUTO"), (2, "Salud demo", "SALUD"), (3, "Hogar demo", "HOGAR")],
        "dim_canal": [(1, "DIRECTO"), (2, "CORREDOR"), (3, "DIGITAL")],
        "dim_estado": [(1, "ABIERTO"), (2, "CERRADO")],
        "fact_polizas": [], "fact_siniestros": [],
    }
    for mes in range(1, 13):
        for prod in range(1, 4):
            # Fórmulas equivalentes a los 72 grupos del laboratorio S15.
            cerrados = (40 + 2 * (mes - 1), 60 + 2 * (mes - 1), 20 + mes - 1)[prod - 1]
            abiertos = (10, 15, 5)[prod - 1] + mes - 1
            for estado, cantidad in ((1, abiertos), (2, cerrados)):
                pagado = cantidad * ((100, 50, 150)[prod - 1] if estado == 1 else (1000, 500, 1500)[prod - 1])
                reservado = cantidad * (2000, 800, 3000)[prod - 1] if estado == 1 else 0
                cantidades = (cantidad // 2, cantidad * 3 // 10)
                cantidades += (cantidad - sum(cantidades),)
                for canal, numero in enumerate(cantidades, 1):
                    # Montos proporcionales a la cantidad, manteniendo el total original.
                    datos["fact_siniestros"].append((
                        len(datos["fact_siniestros"]) + 1, 20250001 + mes * 100, prod, canal,
                        estado, numero, Decimal(pagado) * numero / cantidad,
                        Decimal(reservado) * numero / cantidad, CORTE, "PEN"))
            for canal in range(1, 4):
                cantidad = 100 + 10 * mes + 20 * prod + 5 * canal
                datos["fact_polizas"].append((
                    len(datos["fact_polizas"]) + 1, 20250001 + mes * 100, prod, canal,
                    cantidad, Decimal(cantidad * (600, 400, 300)[prod - 1]), "PEN"))
    return datos


def escribir_excel(ruta, datos):
    libro = Workbook()
    libro.remove(libro.active)
    hojas = {"LEEME": (["paso", "instruccion"], [
        ("1. Matrícula", "Un solo Data Product: DP-SEG-016. Edita la única fila de matricula; conserva los encabezados."),
        ("2. Ambientes", "DEV usa workspace.s16. TEST/UAT/PRD son referencias NO habilitadas. El catálogo destino debe existir."),
        ("3. Código", "codigo_dp permanece igual entre ambientes. version_contrato cambia cuando cambia el contrato."),
        ("4. Exportar", "Ejecuta generar-sesion-16.py --excel <archivo> --ambiente DEV --salida <carpeta>. El Excel no contiene macros."),
        ("5. Crear", "Revisa y ejecuta SQL 00, 01 y 02 en Databricks. Solo ejecutar el generador no crea objetos en cloud."),
        ("6. Consumir", "Configura Genie y dashboard con las guías. Su creación no es automática."),
        ("7. Medidas", "SUM de cantidades y montos. COUNT(*) cuenta grupos. Usa vw_indicadores para combinar hechos."),
        ("8. Tiempo", "2025 histórico, corte 2025-12-31. Freshness diaria es un objetivo; no hay Job programado."),
        ("9. Privacidad", "Datos sintéticos; sin personas, credenciales ni reglas internas del cliente."),
    ])}
    hojas.update({nombre: ([c[0] for c in cols], datos[nombre]) for nombre, cols in ESQUEMAS.items()})
    hojas["activos"] = (["codigo_dp", "objeto", "tipo", "grano_o_proposito"],
                        [(CODIGO, n, "DIMENSION" if n.startswith("dim_") else "HECHO", DESCRIPCIONES[n])
                         for n in ESQUEMAS if n.startswith(("dim_", "fact_"))]
                        + [(CODIGO, "vw_indicadores", "VISTA", "Mes + producto + canal; consumo conjunto sin multiplicar hechos")])
    hojas["relaciones"] = (["tabla_hija", "columna_fk", "tabla_padre", "columna_pk", "cardinalidad"],
                           [r + ("MUCHOS_A_UNO",) for r in RELACIONES])
    hojas["metricas"] = (["metrica", "fuente", "expresion", "significado"], [
        ("Siniestros reportados", "fact_siniestros", "SUM(cantidad_siniestros)", "No COUNT(*): cada fila es un grupo"),
        ("Monto pagado PEN", "fact_siniestros", "SUM(monto_pagado)", "Acumulado al corte, agrupado por mes de reporte"),
        ("Porcentaje de cierre", "vw_indicadores", "100 * SUM(cantidad_cerrados) / NULLIF(SUM(cantidad_siniestros),0)", "Estado al corte; no velocidad de atención"),
        ("Pólizas emitidas", "fact_polizas", "SUM(cantidad_polizas_emitidas)", "Emisiones del mes; no pólizas vigentes ni expuestas"),
        ("Prima emitida PEN", "fact_polizas", "SUM(prima_emitida)", "No calcular siniestralidad con esta prima de emisión"),
    ])
    hojas["diccionario"] = (["hoja", "columna", "tipo_sql", "descripcion"],
                            [(n, *c) for n, cols in ESQUEMAS.items() for c in cols])
    for nombre, (encabezados, filas) in hojas.items():
        hoja = libro.create_sheet(nombre)
        hoja.append(encabezados)
        for fila in filas:
            hoja.append([float(v) if isinstance(v, Decimal) else v for v in fila])
        hoja.freeze_panes = "B2"
        hoja.sheet_view.showGridLines = False
        hoja.sheet_properties.tabColor = "7030A0" if nombre in ("matricula", "ambientes") else "007DBA"
        for celda in hoja[1]:
            celda.fill = PatternFill("solid", fgColor="18234B")
            celda.font = Font(color="FFFFFF", bold=True)
            celda.alignment = Alignment(wrap_text=True, vertical="center")
        hoja.row_dimensions[1].height = 32
        tabla = Table(displayName=f"s16_{nombre}", ref=hoja.dimensions)
        tabla.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
        hoja.add_table(tabla)
        for columna in hoja.columns:
            letra = columna[0].column_letter
            hoja.column_dimensions[letra].width = min(48, max(18, max(len(str(c.value or "")) for c in columna) + 2))
            for celda in columna[1:]:
                celda.alignment = Alignment(vertical="top", wrap_text=True)
                if isinstance(celda.value, dt.date):
                    celda.number_format = "yyyy-mm-dd"
                if columna[0].value in ("prima_emitida", "monto_pagado", "monto_reservado"):
                    celda.number_format = '#,##0.00'
        if nombre in ("matricula", "ambientes", "LEEME", "metricas"):
            for i in range(2, hoja.max_row + 1):
                hoja.row_dimensions[i].height = 66
    for columna, valores in (("B", '"DEV,TEST,UAT,PRD"'), ("E", '"SI,NO"')):
        validacion = DataValidation(type="list", formula1=valores)
        validacion.errorTitle = "Valor fuera del catálogo"
        validacion.error = "Selecciona un valor de la lista."
        validacion.showErrorMessage = True
        libro["ambientes"].add_data_validation(validacion)
        validacion.add(f"{columna}2:{columna}5")
    libro.active = 1
    libro.save(ruta)


def convertir(valor, tipo):
    if valor is None or str(valor).strip() == "":
        raise ValueError("El contrato de referencia no permite celdas vacías")
    if tipo == "INT":
        decimal = Decimal(str(valor))
        if decimal != decimal.to_integral_value():
            raise ValueError(f"Se esperaba entero: {valor}")
        return int(decimal)
    if tipo.startswith("DECIMAL"):
        numero = Decimal(str(valor))
        if (not numero.is_finite() or abs(numero) >= Decimal("1e16")
                or numero != numero.quantize(Decimal("0.01"))):
            raise ValueError(f"Monto inválido o con más de dos decimales: {valor}")
        return numero.quantize(Decimal("0.01"))
    if tipo == "DATE":
        return valor.date() if isinstance(valor, dt.datetime) else (
            valor if isinstance(valor, dt.date) else dt.date.fromisoformat(str(valor)))
    return str(valor).strip()


def leer_excel(ruta):
    libro = load_workbook(ruta, data_only=False)
    datos = {}
    for nombre, columnas in ESQUEMAS.items():
        hoja = libro[nombre]
        filas = list(hoja.values)
        if tuple(filas[0]) != tuple(c[0] for c in columnas):
            raise ValueError(f"Encabezados distintos al contrato: {nombre}")
        datos[nombre] = []
        for fila in filas[1:]:
            if all(v is None for v in fila):
                continue
            if any(isinstance(v, str) and v.startswith("=") for v in fila):
                raise ValueError(f"Usa valores, no fórmulas, en {nombre}")
            datos[nombre].append(tuple(convertir(v, c[1]) for v, c in zip(fila, columnas)))
    libro.close()
    return datos


def validar(datos, ambiente):
    if len(datos["matricula"]) != 1:
        raise ValueError("Debe existir exactamente un Data Product")
    codigo = datos["matricula"][0][0]
    if not re.fullmatch(r"DP-[A-Z]+-[0-9]{3}", codigo):
        raise ValueError("Código esperado: DP-SEG-016 o el mismo patrón")
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", datos["matricula"][0][11]):
        raise ValueError("Versión esperada: mayor.menor.parche, por ejemplo 1.0.0")
    if len(datos["proceso"]) != 1 or datos["proceso"][0][1] != codigo:
        raise ValueError("Se requiere un proceso vinculado al único Data Product")
    ambientes = datos["ambientes"]
    if len(ambientes) != 4 or {r[1] for r in ambientes} != {"DEV", "TEST", "UAT", "PRD"}:
        raise ValueError("Se requieren cuatro referencias únicas DEV/TEST/UAT/PRD")
    for fila in ambientes:
        if fila[0] != codigo or fila[4] not in ("SI", "NO"):
            raise ValueError("Código o habilitación inconsistente en ambientes")
        if not all(re.fullmatch(r"[a-z][a-z0-9_]*", n) for n in fila[2:4]):
            raise ValueError("Catálogo y schema deben usar snake_case sin espacios")
        if fila[3] != "s16":
            raise ValueError("Este contrato utiliza el schema s16")
    if len({r[2:4] for r in ambientes}) != 4:
        raise ValueError("Cada ambiente debe tener un destino distinto")
    elegido = next(r for r in ambientes if r[1] == ambiente)
    if elegido[4] != "SI":
        raise ValueError(f"{ambiente} es solo referencia: configura catálogo y habilitado=SI en el Excel")
    for nombre, filas in datos.items():
        if not filas:
            raise ValueError(f"Hoja sin datos: {nombre}")
        if nombre.startswith(("dim_", "fact_")):
            if len({r[0] for r in filas}) != len(filas):
                raise ValueError(f"PK duplicada en {nombre}")
            if any(r[0] <= 0 for r in filas):
                raise ValueError(f"PK no positiva en {nombre}")
    for hija, fk, padre, pk in RELACIONES:
        idx = [c[0] for c in ESQUEMAS[hija]].index(fk)
        if not {r[idx] for r in datos[hija]} <= {r[0] for r in datos[padre]}:
            raise ValueError(f"FK huérfana: {hija}.{fk}")
    for nombre in ("fact_polizas", "fact_siniestros"):
        columnas = [c[0] for c in ESQUEMAS[nombre]]
        grano = ("id_fecha", "id_producto", "id_canal") + (("id_estado",) if nombre == "fact_siniestros" else ())
        claves = [tuple(r[columnas.index(c)] for c in grano) for r in datos[nombre]]
        if len(set(claves)) != len(claves):
            raise ValueError(f"Grano duplicado en {nombre}")
        for fila in datos[nombre]:
            for columna, valor in zip(columnas, fila):
                if columna.startswith(("cantidad_", "monto_", "prima_")) and valor < 0:
                    raise ValueError(f"Medida negativa: {nombre}.{columna}")
            if fila[-1] != "PEN":
                raise ValueError("El contrato admite solamente PEN")
    corte = datos["matricula"][0][13]
    if corte != CORTE or {r[-2] for r in datos["fact_siniestros"]} != {corte}:
        raise ValueError("Corte del contrato y hechos debe ser 2025-12-31")
    for clave, fecha, anio, mes, _ in datos["dim_fecha"]:
        if anio != 2025 or fecha != dt.date(anio, mes, 1) or clave != int(fecha.strftime("%Y%m%d")):
            raise ValueError("Dimensión mensual incoherente con 2025")
    if {r[1] for r in datos["dim_estado"]} != {"ABIERTO", "CERRADO"}:
        raise ValueError("Estados esperados: ABIERTO y CERRADO")
    return elegido


def literal(valor):
    if isinstance(valor, dt.date):
        return "DATE '" + valor.isoformat() + "'"
    if isinstance(valor, (int, Decimal)):
        return str(valor)
    # Evita escapes de SQL y separadores que complicarían ejecutar por bloques.
    if any(c in str(valor) for c in ("\\", "\x00")):
        raise ValueError("No se admiten backslash ni NUL en el contrato")
    return "'" + str(valor).replace("'", "''") + "'"


def exportar(datos, ambiente, salida):
    elegido = validar(datos, ambiente)
    plantillas = Path(__file__).with_name("sesion-16-plantillas")
    archivos_plantilla = sorted(plantillas.glob("*.sql"))
    if len(archivos_plantilla) != 4:
        raise ValueError("Faltan las cuatro plantillas SQL junto al generador")
    for filas in datos.values():
        for fila in filas:
            for valor in fila:
                literal(valor)
    catalogo, esquema = elegido[2:4]
    prefijo = f"{catalogo}.{esquema}"
    codigo, version = datos["matricula"][0][0], datos["matricula"][0][11]
    sql_dir, csv_dir = salida / "sql", salida / "csv"
    sql_dir.mkdir(parents=True, exist_ok=True)
    csv_dir.mkdir(parents=True, exist_ok=True)
    inicio = (f"-- Databricks notebook source\n-- {codigo} | {ambiente} | contrato {version}\n"
              f"-- Destino único: {prefijo}. Datos sintéticos. Revisar antes de ejecutar.\n")
    crear = [inicio, f"CREATE SCHEMA {prefijo} COMMENT {literal(codigo + ' - ' + ambiente + ' - formación S16')};"]
    carga, relaciones = [inicio, "-- INSERT OVERWRITE reemplaza únicamente los datos de estas tablas didácticas."], [inicio]
    for nombre, columnas in ESQUEMAS.items():
        definiciones = [f"  {col} {tipo} NOT NULL COMMENT {literal(desc)}" for col, tipo, desc in columnas]
        crear.append(f"CREATE TABLE {prefijo}.{nombre} (\n" + ",\n".join(definiciones)
                     + f"\n) USING DELTA\nCOMMENT {literal(DESCRIPCIONES[nombre])}\n"
                     + f"TBLPROPERTIES ('training.codigo_dp'={literal(codigo)}, 'training.ambiente'={literal(ambiente)}, "
                     + f"'training.version_contrato'={literal(version)});")
        columnas_sql = ", ".join(c[0] for c in columnas)
        valores = ",\n".join("  (" + ", ".join(literal(v) for v in fila) + ")" for fila in datos[nombre])
        carga.append(f"INSERT OVERWRITE {prefijo}.{nombre} ({columnas_sql})\nVALUES\n{valores};")
        with (csv_dir / f"{nombre}.csv").open("w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo, lineterminator="\n")
            escritor.writerow([c[0] for c in columnas])
            escritor.writerows(datos[nombre])
        if nombre.startswith(("dim_", "fact_")):
            relaciones.append(f"ALTER TABLE {prefijo}.{nombre} ADD CONSTRAINT pk_{nombre} PRIMARY KEY ({columnas[0][0]});")
    for hija, fk, padre, pk in RELACIONES:
        relaciones.append(f"ALTER TABLE {prefijo}.{hija} ADD CONSTRAINT fk_{hija}_{fk} "
                          f"FOREIGN KEY ({fk}) REFERENCES {prefijo}.{padre} ({pk});")
    (sql_dir / "00-crear-esquema-y-tablas.sql").write_text("\n\n-- COMMAND ----------\n\n".join(crear) + "\n", encoding="utf-8")
    (sql_dir / "01-cargar-desde-excel.sql").write_text("\n\n-- COMMAND ----------\n\n".join(carga) + "\n", encoding="utf-8")
    (sql_dir / "05-relaciones-opcionales.sql").write_text("\n\n".join(relaciones) + "\n", encoding="utf-8")
    for ruta in archivos_plantilla:
        contenido = ruta.read_text(encoding="utf-8").replace("{{NAMESPACE}}", prefijo).replace("{{CODIGO_DP}}", codigo).replace("{{AMBIENTE}}", ambiente)
        (sql_dir / ruta.name).write_text(contenido, encoding="utf-8")
    print(f"OK: {codigo}, ambiente {ambiente}, destino {prefijo}; SQL y CSV en {salida}")
    print("No se crearon objetos en Databricks. Ejecuta 00, 01, 02 y valida con 03.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--excel", type=Path, help="Libro existente; nunca se modifica")
    parser.add_argument("--ambiente", choices=("DEV", "TEST", "UAT", "PRD"), default="DEV")
    parser.add_argument("--salida", type=Path, default=DESTINO)
    args = parser.parse_args()
    ruta = args.excel or args.salida / "matricula-data-product.xlsx"
    if args.excel is None and not ruta.exists():
        args.salida.mkdir(parents=True, exist_ok=True)
        escribir_excel(ruta, datos_base())
    exportar(leer_excel(ruta), args.ambiente, args.salida)


if __name__ == "__main__":
    main()
