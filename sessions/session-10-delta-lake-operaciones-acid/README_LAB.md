# Laboratorio Medallion — Seguros

## Objetivo

Construir una arquitectura:

```text
Volume / S3 Landing
        ↓
Bronze
        ↓
Silver SCD Type 2
        ↓
Gold dimensional
```

utilizando dos archivos:

- `polizas_seguro.csv`
- `siniestros_seguro.csv`

## Entorno utilizado

```text
Catalog : workspace

Schemas:
workspace.bronze
workspace.silver
workspace.gold

Volume:
workspace.bronze.s07_archivos

Landing:
/Volumes/workspace/bronze/s07_archivos/landing/
```

## Archivos a cargar en Landing

Copiar:

```text
polizas_seguro.csv
siniestros_seguro.csv
```

a:

```text
/Volumes/workspace/bronze/s07_archivos/landing/
```

La estructura debe quedar:

```text
s07_archivos/
└── landing/
    ├── polizas_seguro.csv
    └── siniestros_seguro.csv
```

---

## Orden de ejecución

### Paso 0 — opcional

Importar y ejecutar:

`00_crear_landing.py`

para crear/listar la carpeta Landing.

### Paso 1

Ejecutar desde SQL Editor:

`00_setup_delta_tables.sql`

Crea:

### Bronze

- `workspace.bronze.polizas_medallion`
- `workspace.bronze.siniestros_medallion`

### Silver

- `workspace.silver.polizas_scd2`
- `workspace.silver.siniestros_scd2`

### Gold

Dimensiones:

- `workspace.gold.dim_asegurado`
- `workspace.gold.dim_producto`
- `workspace.gold.dim_poliza`
- `workspace.gold.dim_tiempo`

Hechos:

- `workspace.gold.fact_poliza`
- `workspace.gold.fact_siniestro`

---

## Paso 2 — Bronze

Importar como notebook:

`01_load_bronze.py`

El script:

1. lee los CSV desde el Volume
2. aplica schemas
3. agrega columnas técnicas
4. carga tablas Delta Bronze

Columnas técnicas:

```text
fecha_ingestion
origen_sistema
archivo_origen
id_ejecucion
```

---

## Paso 3 — Silver SCD Type 2

Importar:

`02_build_silver_scd2.py`

El script detecta cambios por hash y genera:

```text
hash_registro
fecha_inicio_vigencia
fecha_fin_vigencia
es_actual
fecha_procesamiento
```

Ejemplo:

```text
POL-0006

ACTIVA
01/01 ───────────── 15/04

ACTIVA / nueva prima
16/04 ───────────── 20/06

CANCELADA
21/06 ───────────── 9999
```

La finalidad es mantener trazabilidad completa de los cambios.

---

## Paso 4 — Gold

Importar:

`03_build_gold.py`

Se utilizan solamente:

```text
es_actual = true
```

de las tablas Silver.

El modelo resultante:

```text
                dim_asegurado
                      │
                      │
dim_producto ─── dim_poliza
      │               │
      └───────────────┤
                      ↓
               fact_siniestro

dim_tiempo ───────────┘
```

También se crea:

```text
fact_poliza
```

---

## Grain

### fact_poliza

```text
1 fila por póliza actual
```

### fact_siniestro

```text
1 fila por siniestro actual
```

---

## Paso 5 — Validación

Ejecutar:

`04_validacion.sql`

Validar:

- cantidad Bronze
- historial Silver
- una sola versión `es_actual = true`
- dimensiones Gold
- hechos Gold
- consulta estrella
- métricas
- ubicación física Delta

---

## Conceptos cubiertos

- Amazon S3 / Volumes
- Bronze / Silver / Gold
- Delta Lake
- columnas técnicas
- trazabilidad
- hash de cambios
- SCD Type 2
- dimensiones
- hechos
- surrogate keys
- grain
- arquitectura Medallion
- modelo estrella
