# Ejemplo básico — Landing, Bronze, SQL y Python

## Ficha de la actividad

| Campo | Valor |
| --- | --- |
| Sesión | 4 — Lakehouse y primer notebook |
| Tipo | `GUIDED` |
| Compatibilidad | `PRACTICO_CONDICIONAL` con fallback `PRACTICO_FREE` |
| Duración | 45 a 60 minutos |
| Datos | 10,000 pólizas sintéticas |
| Nivel | Básico |

## Objetivo

El participante aprenderá a:

- reconocer el prefijo Landing de S3 como la zona donde reside el CSV original;
- crear metadata con instrucciones DDL;
- crear el schema `bronze` y una tabla Delta administrada;
- cargar 10,000 registros en Bronze;
- ejecutar consultas básicas con Databricks SQL;
- leer y consultar la misma tabla desde un notebook Python/PySpark;
- localizar la metadata en Unity Catalog y los datos en almacenamiento.

## Flujo de la práctica

```text
Amazon S3: landing/polizas/polizas_2026_09_28.csv
                 10,000 registros
                 |
                 v
workspace.bronze.polizas
Tabla Delta: permite consultas SQL y Python
```

## Archivos incluidos

| Archivo | Uso |
| --- | --- |
| `data/polizas_2026_09_28.csv` | Fuente con 10,000 pólizas sintéticas |
| `01_landing_a_bronze.sql` | DDL, metadata y carga desde Amazon S3 |
| `02_consultas_sql_basicas.sql` | Consultas y ejercicios con Databricks SQL |
| `03_consultas_python.py` | Notebook básico de Python/PySpark |
| `scripts/generar_polizas.py` | Regenera el CSV de manera reproducible |

## Orden de ejecución

### 1. Crear Bronze desde Landing de S3

Importe y ejecute `01_landing_a_bronze.sql`.

El notebook utiliza DDL para crear:

```text
workspace
└── bronze
    └── Table: polizas (Delta administrada)
```

El archivo original debe haberse cargado previamente en el bucket utilizado en
la Sesión 02:

```text
s3://<S3_BUCKET>/landing/polizas/polizas_2026_09_28.csv
```

Antes de ejecutar, reemplace `<S3_BUCKET>` en todas sus apariciones en el notebook.
El instructor debe haber configurado el acceso de Databricks a esa ubicación
mediante Unity Catalog e IAM. No se utilizan credenciales dentro del notebook.

La validación debe devolver:

```text
cantidad_registros
------------------
10000
```

### 2. Practicar Databricks SQL

Importe `02_consultas_sql_basicas.sql`. Incluye ejemplos de:

- `SELECT` y `LIMIT`;
- `COUNT`;
- `WHERE`;
- `ORDER BY`;
- `GROUP BY`;
- `SUM` y `AVG`;
- filtros de fecha;
- expresiones `CASE`.

Al final contiene cuatro ejercicios y sus soluciones de referencia.

### 3. Practicar con Python

Importe `03_consultas_python.py`. El notebook utiliza PySpark únicamente para:

- leer una tabla con `spark.table`;
- mostrar registros con `display`;
- contar filas;
- revisar el schema;
- seleccionar columnas;
- filtrar registros;
- agrupar datos;
- ejecutar una consulta SQL desde Python.

## DDL utilizado

DDL significa **Data Definition Language**. En esta práctica se utiliza para
crear y documentar objetos, no para consultar sus filas.

```sql
CREATE SCHEMA IF NOT EXISTS workspace.bronze;

CREATE OR REPLACE TABLE workspace.bronze.polizas (
  id_poliza STRING COMMENT 'Identificador único de la póliza',
  fecha_inicio DATE COMMENT 'Fecha de inicio de vigencia',
  prima DECIMAL(12, 2) COMMENT 'Importe de la prima'
)
USING DELTA;
```

El notebook completo define trece columnas y comentarios para cada campo.

## ¿Dónde residen los datos y la metadata?

| Elemento | Qué contiene | Cómo observarlo |
| --- | --- | --- |
| Landing | CSV original | `s3://<S3_BUCKET>/landing/polizas/` |
| Bronze | Archivos Delta con 10,000 registros | `location` devuelto por `DESCRIBE DETAIL` |
| Unity Catalog | Nombre de tabla, columnas, tipos, comentarios, owner y permisos | Catalog Explorer, `DESCRIBE TABLE` e `INFORMATION_SCHEMA` |
| Delta Lake | Metadata transaccional y versiones | `_delta_log` dentro de la ubicación Delta |
| Tabla Bronze | Trazabilidad por registro | `_archivo_origen`, `_ruta_origen` y `_fecha_ingesta` |

El schema `bronze` es un contenedor lógico. No es una carpeta donde se escriben
directamente las filas. Unity Catalog administra la relación entre el nombre
`workspace.bronze.polizas` y la ubicación física de la tabla Delta.

## Resultado esperado del dataset

| Comprobación | Resultado |
| --- | ---: |
| Filas | 10,000 |
| Pólizas distintas | 10,000 |
| Asegurados distintos | 7,500 |
| Productos | 4 |
| Canales de venta | 5 |
| Estados | 4 |

## Opción B — fallback para Free Edition

Si Databricks Free Edition no puede leer directamente el bucket S3:

1. Cree un Volume administrado dentro de un schema permitido.
2. Cargue el CSV incluido en `data/` al Volume.
3. Sustituya la ruta S3 de `read_files` por una ruta como:

   ```text
   /Volumes/workspace/default/archivos_fuente/polizas_2026_09_28.csv
   ```

4. Si tampoco se puede crear un Volume, use **Create table from local files** y
   ejecute los notebooks de consultas sobre la tabla resultante.

El fallback conserva el objetivo de practicar metadata, SQL y Python. Debe
explicarse que en la arquitectura principal Landing reside en Amazon S3.

## Qué cambia en producción

En esta práctica, Landing ya reside en Amazon S3. En un entorno empresarial, el
prefijo se gobierna mediante una external location o un external volume. El
acceso debe utilizar roles de IAM y mínimo privilegio, sin credenciales dentro
del notebook. La ingesta repetitiva normalmente se automatiza; aquí se utiliza
`INSERT OVERWRITE` para mantener el flujo sencillo y repetible.

## Regenerar el dataset

Desde la raíz del repositorio:

```bash
python3 sessions/session-04-lakehouse-primer-notebook/resources/ejemplo-landing-bronze-seguros/scripts/generar_polizas.py
```
