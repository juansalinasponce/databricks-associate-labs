# AGENTS.md

## 1. Propósito de este archivo

Este archivo define cómo debe trabajar Codex dentro de este repositorio.

Codex debe actuar como **asistente técnico y pedagógico para la construcción de una capacitación corporativa de Databricks Data Engineering y Lakehouse sobre AWS**, creando materiales que puedan utilizarse directamente en sesiones, ejercicios guiados, laboratorios evaluados y un caso integrador.

La prioridad no es producir la mayor cantidad de código posible.

La prioridad es producir materiales:

- técnicamente correctos
- fáciles de ejecutar
- fáciles de explicar
- progresivos
- compatibles con el entorno disponible
- relacionados con situaciones de una aseguradora
- reutilizables por los participantes en sus funciones diarias
- alineados con el syllabus oficial del programa
- alineados como base con Databricks Certified Data Engineer Associate, sin convertir el curso en un banco de preguntas de certificación

## Directriz curricular vigente — énfasis en la plataforma Databricks

Por solicitud del cliente, el objetivo principal es que un grupo diverso de
participantes aprenda a utilizar Databricks como plataforma integral y pueda
elegir la herramienta adecuada ante una necesidad de negocio.

Esta directriz complementa y, cuando exista conflicto, reemplaza la distribución
curricular referencial descrita más adelante en este archivo. La asignación
vigente de módulos y sesiones se encuentra en `Docs/syllabus.md` y
`Docs/cronograma.md`.

Reglas vigentes:

- no modificar el alcance ni los materiales cerrados de la Sesión 1
- mantener Spark, PySpark y Spark SQL a nivel fundamental y aplicado; no orientar
  el programa a especialización avanzada en Spark
- utilizar SQL como vía principal para análisis y mostrar Python, PySpark y
  herramientas visuales como alternativas según el escenario
- incluir actividades explícitas de Workspace, Catalog, Compute, SQL Editor,
  notebooks, Data Ingestion, Visual Data Prep, AI/BI Dashboards, Jobs,
  Pipelines, Alerts, Unity Catalog, MLflow, Genie Code, Genie Agents y
  Databricks Apps
- profundizar en Medallion, pipelines, automatización, dashboards, gobierno,
  trazabilidad y buenas prácticas de uso de la plataforma
- enseñar a decidir entre tabla, vista, notebook, pipeline, dashboard, agente o
  aplicación
- preparar fallback para toda capacidad que dependa del entorno habilitado
- usar las sesiones 6 y 12 para repaso aplicado y evaluación sin contenido nuevo
- reservar los 120 minutos de la Sesión 18 para elaborar el caso de uso final

---

# 2. Contexto oficial del programa

## Programa

**Programa de Especialización en Databricks Data Engineering y Lakehouse sobre AWS**

### Orientación

- Arquitectura Cloud
- AWS
- Databricks
- Apache Spark
- PySpark
- Spark SQL
- Delta Lake
- Lakehouse
- Ingesta
- Lakeflow
- DevOps
- GitHub
- Seguridad
- Gobierno de datos
- Data Products

### Cliente

**La Positiva**

### Duración

**36 horas cronológicas**

### Nivel

**Fundamental a Intermedio**

### Modalidad

**Virtual síncrona**

### Cloud de referencia

**Amazon Web Services**

### Plataforma principal de laboratorio

**Databricks Free Edition**

### Enfoque metodológico

El programa debe mantener aproximadamente:

- **40% conceptual y arquitectura**
- **60% demostraciones, ejercicios y laboratorios**

Codex no debe interpretar "práctico" como "todo debe ser código".

En temas como Cloud, IAM, arquitectura, FinOps, Data Mesh, seguridad o gobierno, una actividad práctica puede consistir en:

- analizar un escenario
- completar una arquitectura
- seleccionar un patrón
- comparar alternativas
- diseñar una estructura
- interpretar una policy
- identificar responsabilidades
- revisar una configuración
- resolver un problema guiado

---

# 3. Fuentes de verdad y orden de prioridad

Antes de crear contenido, Codex debe revisar los archivos existenteses del repositorio.

Usar esta prioridad:

1. instrucciones explícitas del usuario
2. `AGENTS.md`
3. `docs/cronograma.md`, si existe
4. `docs/syllabus.md`, si existe
5. estructura y convenciones ya implementadas en el repositorio
6. documentación oficial de Databricks, AWS o GitHub cuando sea necesario verificar una capacidad cambiante

## Regla crítica sobre el syllabus

Los módulos deben enseñarse en el orden definido en este archivo y en el syllabus.

**No comenzar directamente con Spark, Delta Lake o Medallion.**

El programa inicia con:

1. fundamentos Cloud
2. AWS
3. arquitectura moderna de datos
4. contexto de migración On-Premise a Cloud
5. recién después Databricks y Lakehouse

Los ejercicios iniciales deben reflejar esa secuencia.

## Regla crítica sobre sesiones

El syllabus define módulos y horas, pero la distribución de contenidos por sesión puede ser flexible.

Por tanto:

- no inventar una relación exacta módulo-sesión si `docs/cronograma.md` no la define
- no evaluar un concepto que todavía no haya sido enseñado
- cuando se cree material para una sesión concreta, revisar primero el cronograma
- si el cronograma todavía no existe, organizar el material por **módulo** y dejar preparada su posterior asignación a sesiones

---

# 4. Evaluaciones oficiales del programa

Para este repositorio se utilizará la siguiente distribución:

| Evaluación | Fecha | Referencia | Peso |
| --- | --- | --- | ---: |
| Laboratorio 1 | 05 de octubre de 2026 | Sesión 6 | 30% |
| Laboratorio 2 | 28 de octubre de 2026 | Sesión 12 | 30% |
| Caso Final | 25 de noviembre de 2026 | Sesión 18 | 40% |

Esta distribución debe utilizarse aunque existan tablas referenciales distintas en versiones anteriores de la propuesta.

## Regla de cobertura

Cada evaluación solo puede medir conocimientos impartidos hasta ese momento.

### Laboratorio 1

Antes de diseñarlo:

1. revisar `docs/cronograma.md`
2. identificar exactamente qué contenidos fueron impartidos hasta la Sesión 6
3. construir el laboratorio únicamente con esos contenidos

Si todavía no existe un cronograma definitivo, usar como alcance conservador:

- fundamentos Cloud y AWS
- arquitectura moderna de datos
- Databricks y Lakehouse Fundamentals
- fundamentos de Spark
- DataFrames
- transformaciones básicas con PySpark y Spark SQL

No incluir por defecto:

- Auto Loader avanzado
- MERGE
- arquitectura Medallion completa
- Lakeflow avanzado
- CI/CD
- Unity Catalog avanzado
- Data Mesh

salvo que el cronograma confirme que esos temas ya fueron enseñados.

### Laboratorio 2

Antes de diseñarlo:

1. revisar contenidos impartidos hasta la Sesión 12
2. reutilizar conceptos anteriores
3. aumentar dificultad de forma moderada

Si todavía no existe un cronograma definitivo, el alcance esperado puede incluir:

- Spark
- PySpark
- Spark SQL
- ingesta
- Full e Incremental Load
- CSV, JSON y Parquet
- Delta Lake
- MERGE
- Medallion
- calidad de datos
- modelamiento básico

Lakeflow solo debe evaluarse si ya fue enseñado antes de la evaluación.

### Caso Final

Debe integrar los conocimientos impartidos durante el programa.

No es necesario que cada tema conceptual se implemente técnicamente.

Por ejemplo:

- Data Mesh puede evaluarse mediante una decisión de diseño
- gobierno puede evaluarse mediante permisos o clasificación conceptual
- FinOps puede evaluarse mediante una recomendación
- arquitectura puede evaluarse mediante un diagrama
- el núcleo práctico debe concentrarse en ingeniería de datos

---

# 5. Contexto de negocio obligatorio

Los ejercicios deben estar orientados a una **compañía aseguradora**, utilizando a La Positiva únicamente como contexto del sector.

## Regla de privacidad y realismo

No asumir que conocemos:

- arquitectura interna real de La Positiva
- nombres de sistemas internos
- tablas internas
- datos reales
- procesos confidenciales
- reglas actuariales reales
- políticas internas

Los escenarios deben ser **sintéticos y ficticios**, pero suficientemente cercanos a la operación de seguros.

Usar nombres neutrales como:

- `aseguradora_demo`
- `seguros_training`
- `polizas`
- `siniestros`
- `asegurados`
- `pagos`
- `productos`
- `coberturas`
- `canales`
- `proveedores`

---

# 6. Principio pedagógico central

Cada ejercicio debe responder a esta pregunta:

> ¿Qué conocimiento nuevo aprenderá el participante y cómo podría reutilizarlo luego en su trabajo diario?

Un ejercicio adecuado debe:

1. introducir uno o pocos conceptos nuevos
2. utilizar un escenario de negocio simple
3. evitar infraestructura innecesaria
4. tener un resultado verificable
5. poder ejecutarse dentro del tiempo disponible
6. explicar la aplicación práctica
7. reutilizar conocimientos anteriores
8. no requerir conocimiento actuarial avanzado

## Evitar

- ejercicios que necesiten comprender un modelo de seguros complejo antes de empezar
- datasets enormes
- arquitecturas artificialmente complejas
- APIs externas innecesarias
- múltiples tecnologías nuevas dentro del mismo ejercicio
- código excesivamente abstracto
- ejemplos como `tabla1`, `tabla2`, `dato_a`
- ejercicios cuyo objetivo técnico no sea evidente

---

# 7. Universo de datos asegurador común

Siempre que sea posible, reutilizar el mismo universo sintético durante el programa.

## Entidades principales

```text
asegurados
    │
    ├── polizas ─── productos
    │      │
    │      ├── coberturas
    │      ├── pagos
    │      └── siniestros
    │
    └── canales
               \
                proveedores / talleres
```

## Dataset base sugerido

### `asegurados`

Campos de ejemplo:

```text
id_asegurado
tipo_documento
numero_documento
nombre
departamento
provincia
distrito
fecha_registro
canal_origen
```

### `polizas`

```text
id_poliza
id_asegurado
id_producto
fecha_inicio
fecha_fin
estado_poliza
prima
moneda
canal_venta
fecha_actualizacion
```

### `productos`

```text
id_producto
nombre_producto
tipo_seguro
segmento
```

### `siniestros`

```text
id_siniestro
id_poliza
fecha_siniestro
fecha_reporte
tipo_siniestro
estado_siniestro
monto_reclamado
monto_aprobado
monto_pagado
fecha_actualizacion
```

### `pagos`

```text
id_pago
id_poliza
fecha_vencimiento
fecha_pago
monto
estado_pago
medio_pago
fecha_actualizacion
```

### `proveedores`

```text
id_proveedor
tipo_proveedor
departamento
estado
```

## Calidad intencional

Los datasets sintéticos deben poder incluir de manera controlada:

- duplicados
- nulos
- mayúsculas y minúsculas inconsistentes
- fechas en formatos distintos
- códigos inválidos
- montos faltantes
- registros tardíos
- cambios de estado
- archivos incrementales
- nuevas columnas en una versión posterior

Estos defectos deben existir solo cuando sirvan para practicar un concepto.

---

# 8. Plataforma tecnológica

El entorno de referencia es:

```text
GitHub
   │
   │ código, notebooks y documentación
   ▼
Databricks Free Edition
   │
   │ procesamiento
   ├──────────────► Delta / tablas / SQL
   │
   ▼
AWS S3
fuente o destino cuando la integración sea viable
```

Las tres tecnologías tienen roles distintos.

## Databricks Free Edition

Es la plataforma principal para prácticas.

## AWS

Es el Cloud de referencia.

AWS debe aparecer desde el inicio del curso debido al syllabus.

## Amazon S3

Es el servicio principal de object storage utilizado para explicar y practicar patrones de almacenamiento cuando el entorno lo permita.

## GitHub

Es el repositorio del curso desde el inicio.

Los conceptos formales de Git, branches, Pull Requests y CI/CD se profundizan en el Módulo 7.

---

# 9. Databricks Free Edition

Codex debe asumir que los estudiantes usan **Databricks Free Edition**.

## Diseño compatible

Los ejercicios deben:

- ser livianos
- evitar grandes volúmenes
- evitar largas ejecuciones
- minimizar concurrencia
- utilizar capacidades disponibles en Free Edition
- tener una alternativa cuando una función empresarial no esté disponible
- evitar depender de configuración de clústeres clásicos
- evitar requisitos de networking empresarial
- evitar dependencias administrativas que el estudiante no pueda gestionar

## No hardcodear capacidades cambiantes

Las capacidades y cuotas de Free Edition pueden cambiar.

Si el ejercicio depende de una función específica:

1. verificar documentación oficial si está disponible
2. indicar el requisito
3. preparar un fallback

Usar la clasificación:

```text
PRACTICO_FREE
PRACTICO_CONDICIONAL
DEMO_INSTRUCTOR
CONCEPTUAL
```

### `PRACTICO_FREE`

Debe poder ejecutarse directamente en Free Edition.

### `PRACTICO_CONDICIONAL`

Depende de cuotas, conectividad o capacidades habilitadas.

### `DEMO_INSTRUCTOR`

El instructor demuestra la funcionalidad.

### `CONCEPTUAL`

Se enseña mediante arquitectura, análisis o explicación.

## Patrón obligatorio de fallback

Cuando exista riesgo de incompatibilidad:

```markdown
## Opción A — práctica principal
Procedimiento usando la capacidad prevista.

## Opción B — fallback para Free Edition
Procedimiento equivalente utilizando almacenamiento administrado,
archivos cargados al workspace o una alternativa compatible.

## Qué cambia en producción
Explicación corta de cómo se implementaría en un entorno empresarial.
```

El estudiante no debe perder una sesión completa solucionando una restricción de la edición gratuita.

---

# 10. AWS y S3

AWS no debe tratarse únicamente como una integración técnica posterior.

El syllabus exige fundamentos Cloud y AWS desde el Módulo 1.

## AWS en el inicio del curso

Antes de comenzar Spark se deben trabajar conceptos como:

- On-Premise vs Cloud
- IaaS, PaaS y SaaS
- elasticidad
- escalabilidad
- alta disponibilidad
- regiones
- Availability Zones
- responsabilidad compartida
- S3
- IAM
- roles y policies
- mínimo privilegio
- VPC a nivel conceptual
- cifrado
- AWS KMS a nivel conceptual
- compute tradicional vs serverless
- FinOps básico
- tagging
- Data Warehouse
- Data Lake
- Lakehouse
- separación Storage / Compute
- migración On-Premise a AWS

## Ejercicios Cloud válidos

Los primeros ejercicios no necesitan ser notebooks.

Ejemplos apropiados:

### Ejercicio Cloud 01 — clasificar servicios

Dado un conjunto de capacidades, identificar:

- IaaS
- PaaS
- SaaS

y explicar qué responsabilidad conserva el cliente.

### Ejercicio Cloud 02 — flujo de una aseguradora

Partir de:

```text
Sistema On-Premise de pólizas
Archivo diario de siniestros
```

y construir:

```text
On-Premise
    ↓
AWS
    ↓
S3
    ↓
Databricks
    ↓
consumo analítico
```

El objetivo es comprender la arquitectura, no desplegarla.

### Ejercicio Cloud 03 — organizar un bucket

Diseñar:

```text
s3://seguros-training/
    landing/
        polizas/
        siniestros/
        pagos/
    archive/
    output/
```

y explicar la finalidad de cada prefijo.

### Ejercicio Cloud 04 — mínimo privilegio

Comparar una policy conceptual:

```text
S3 lectura
```

contra:

```text
S3 lectura y escritura
```

e identificar cuál corresponde a un consumidor y cuál a un proceso de ingesta.

No utilizar credenciales reales.

### Ejercicio Cloud 05 — Serverless

Comparar un compute tradicional con serverless para una carga esporádica de datos.

### Ejercicio Cloud 06 — arquitectura moderna

Comparar:

```text
Data Warehouse
Data Lake
Lakehouse
```

aplicándolo a datos de pólizas y siniestros.

## Amazon S3 en prácticas posteriores

S3 puede utilizarse como:

- landing zone
- fuente CSV
- fuente JSON
- destino de archivos
- origen de un Full Load
- origen de incrementales
- ejemplo de separación Storage / Compute

### Estructura sugerida

```text
s3://<training-bucket>/
    landing/
        polizas/
        siniestros/
        pagos/
    incremental/
    archive/
    output/
```

## Fallback de S3

La propuesta reconoce que la integración directa con S3 puede depender de las restricciones de Free Edition.

Orden de preferencia:

1. S3 académico, si la integración está validada
2. almacenamiento administrado por Databricks
3. archivos incluidos en el repositorio
4. demostración conceptual de S3

El objetivo del ejercicio no debe fracasar porque S3 no esté disponible.

---

# 11. Seguridad de credenciales

Nunca crear ni versionar:

- AWS Access Key reales
- AWS Secret Access Key reales
- Session Tokens reales
- passwords
- Personal Access Tokens
- secretos de Databricks
- archivos `.env` con secretos
- credenciales dentro de notebooks
- credenciales dentro de capturas o documentación

## Placeholders permitidos

```text
<AWS_ACCOUNT_ID>
<AWS_ROLE_ARN>
<S3_BUCKET>
<S3_PREFIX>
<GITHUB_REPOSITORY>
<DATABRICKS_WORKSPACE>
```

Si se necesita explicar una autenticación, usar valores ficticios.

No pedir al estudiante que pegue secretos en una celda que luego pueda terminar en GitHub.

---

# 12. GitHub

GitHub será el repositorio oficial de código y materiales.

## Desde el inicio

Los participantes pueden:

- clonar o acceder al repositorio
- descargar datasets
- revisar notebooks
- consultar READMEs
- entregar evidencias cuando corresponda

## En el Módulo 7

Se enseñan explícitamente:

- repository
- commit
- branch
- Pull Request
- Code Review
- naming
- parametrización
- separación configuración/código
- CI/CD conceptual
- promoción DEV / TEST / UAT / PRD
- Bundles, YAML, CLI y Terraform a nivel overview cuando corresponda

## Regla para Codex

No adelantar toda la teoría Git en las primeras sesiones solo porque el repositorio está en GitHub.

Antes del Módulo 7, GitHub es principalmente el medio de distribución y versionamiento del curso.

## `.gitignore`

Mantener al menos:

```gitignore
.env
.env.*
*.pem
*.key
credentials.*
secrets.*
.DS_Store
__pycache__/
.ipynb_checkpoints/
```

---

# 13. Estructura curricular oficial

Codex debe utilizar estos módulos como mapa principal.

| # | Módulo | Horas |
| --- | --- | ---: |
| 1 | Fundamentos Cloud, AWS y Arquitectura Moderna de Datos | 4 |
| 2 | Databricks Data Intelligence Platform y Lakehouse Fundamentals | 4 |
| 3 | Apache Spark, PySpark y Spark SQL para Data Engineering | 5 |
| 4 | Ingesta y carga de datos | 4 |
| 5 | Delta Lake, Arquitectura Medallion, Modelamiento y Calidad | 5 |
| 6 | Lakeflow, Orquestación y Automatización de Pipelines | 4 |
| 7 | Ingeniería de Software, Estándares, Git y CI/CD | 3 |
| 8 | Monitoreo, Troubleshooting, Performance y Optimización | 2 |
| 9 | Unity Catalog, Seguridad y Gobierno de Datos | 3 |
| 10 | Data Mesh, Data Products y Disponibilización de Datos | 2 |
| | **Total** | **36** |

No cambiar el orden sin instrucción explícita.

---

# 14. Módulo 1 — Fundamentos Cloud, AWS y Arquitectura Moderna de Datos

## Objetivo pedagógico

El participante debe poder interpretar una arquitectura moderna de datos en AWS y entender por qué Databricks aparece dentro de una estrategia de modernización.

## Temas

- On-Premise a Cloud
- IaaS, PaaS y SaaS
- elasticidad
- escalabilidad
- alta disponibilidad
- Regions
- Availability Zones
- responsabilidad compartida
- S3
- IAM
- roles
- policies
- mínimo privilegio
- VPC conceptual
- cifrado
- KMS conceptual
- compute tradicional vs Serverless
- FinOps básico
- tagging
- Data Warehouse
- Data Lake
- Lakehouse
- Storage / Compute
- migración On-Premise a AWS

## Ejercicios recomendados

### M1-E01 — On-Premise vs Cloud

**Tipo:** conceptual guiado  
**Duración:** 15 a 20 min  
**Caso:** archivos de pólizas procesados en un servidor On-Premise  
**Objetivo:** identificar qué cambia al mover almacenamiento y procesamiento a Cloud

### M1-E02 — IaaS, PaaS y SaaS

**Tipo:** clasificación  
**Duración:** 10 a 15 min  
**Caso:** alternativas para una plataforma de datos  
**Objetivo:** reconocer responsabilidades

### M1-E03 — S3 para datos de seguros

**Tipo:** diseño simple  
**Duración:** 20 min  
**Objetivo:** organizar `landing`, `archive` y `output`

### M1-E04 — IAM y mínimo privilegio

**Tipo:** análisis de policy  
**Duración:** 20 min  
**Objetivo:** diferenciar lectura, escritura y administración

### M1-E05 — Data Warehouse vs Data Lake vs Lakehouse

**Tipo:** comparación  
**Duración:** 20 min  
**Caso:** pólizas, siniestros, JSON y consumo BI

### M1-E06 — Arquitectura objetivo

**Tipo:** práctica guiada con fallback  
**Duración:** 55 min  
**Flujo:** On-Premise → AWS S3 → Databricks → consumidor  
**Actividad:** crear un bucket con nombre globalmente único, cargar datos
sintéticos mediante `aws s3 cp` y `aws s3 sync`, comparar formas de carga y
completar arquitectura y permisos  
**Resultado:** bucket o evidencia simulada, tres object keys, arquitectura
visual y matriz de mínimo privilegio

## Aplicación diaria

Los participantes deben poder interpretar arquitecturas, conversar con equipos Cloud y entender dónde se almacenan y procesan los datos.

---

# 15. Módulo 2 — Databricks Data Intelligence Platform y Lakehouse Fundamentals

## Objetivo pedagógico

Entender la plataforma antes de comenzar a programar intensivamente.

## Temas

- Control Plane
- Compute Plane
- Account
- Workspace
- navegación
- Notebooks
- compute serverless
- SQL Warehouses
- Jobs
- Pipelines
- Git Folders
- Catalog Explorer
- Databricks Runtime
- Lakehouse
- Delta Lake
- Unity Catalog
- workloads
- Data Engineering
- Data Warehousing
- BI y Analytics
- overview ML/AI
- selección de compute
- costos a nivel introductorio
- Well-Architected a nivel introductorio

## Ejercicios recomendados

### M2-E01 — Reconocimiento del workspace

Localizar:

- Workspace
- Notebook
- Catalog Explorer
- SQL
- Jobs

### M2-E02 — Mapa de componentes

Relacionar cada componente con su función.

### M2-E03 — Control Plane vs Compute Plane

Completar un diagrama simple.

### M2-E04 — Selección de workload

Dado un escenario asegurador, escoger:

- Data Engineering
- SQL / Analytics
- otro workload

### M2-E05 — Primer notebook

Crear un notebook mínimo con:

```python
df = spark.createDataFrame(...)
display(df)
```

El objetivo es familiarización, no transformación avanzada.

---

# 16. Módulo 3 — Apache Spark, PySpark y Spark SQL para Data Engineering

## Objetivo pedagógico

Aprender a transformar datos con Spark utilizando ejemplos aseguradores simples.

## Temas

- Driver
- Executors
- Jobs
- Stages
- Tasks
- SparkSession
- DataFrames
- Transformations
- Actions
- Lazy Evaluation
- particiones
- Narrow / Wide Transformations
- Shuffle
- lectura
- escritura
- `select`
- `filter`
- `withColumn`
- nulls
- casts
- `groupBy`
- agregaciones
- `count`
- `countDistinct`
- joins
- union
- deduplicación
- funciones Spark
- Spark SQL
- PySpark
- Spark UI a nivel introductorio
- buenas prácticas

## Ejercicios recomendados

### M3-E01 — Leer pólizas

CSV pequeño de pólizas.

Practicar:

```text
read
schema
show/display
select
filter
```

### M3-E02 — Pólizas vigentes

Crear una columna que identifique pólizas:

```text
ACTIVA
VENCIDA
```

### M3-E03 — Calidad básica

Resolver:

- nulos
- tipos
- duplicados

### M3-E04 — Agregaciones

Calcular:

- pólizas por producto
- prima total por producto
- asegurados únicos

### M3-E05 — Join póliza-producto

Unir:

```text
polizas
+
productos
```

### M3-E06 — Póliza-siniestro

Join `LEFT` para identificar pólizas con y sin siniestro.

### M3-E07 — SQL vs PySpark

Resolver una consulta sencilla en ambas formas.

## Regla

No introducir Delta Lake avanzado mientras el objetivo sea aprender Spark.

---

# 17. Módulo 4 — Ingesta y carga de datos

## Objetivo pedagógico

Comprender patrones de carga y elegir uno según el escenario.

## Temas

- Batch
- Streaming
- Full Load
- Incremental Load
- estructurados
- semiestructurados
- object storage
- COPY INTO
- Auto Loader
- Schema Inference
- Enforcement
- Evolution
- checkpoints
- idempotencia
- reprocesamiento
- Structured Streaming
- CDC
- Lakeflow Connect
- JDBC
- ODBC
- REST API
- volumen
- latencia
- frecuencia
- seguridad
- gobierno

## Ejercicios recomendados

### M4-E01 — Full Load

Cargar `polizas_full.csv`.

### M4-E02 — Incremental diario

Procesar:

```text
siniestros_2026_10_01.csv
siniestros_2026_10_02.csv
```

El objetivo es entender por qué no se reprocesa todo.

### M4-E03 — JSON semiestructurado

Leer un JSON sencillo de notificaciones de siniestros.

### M4-E04 — Schema Evolution

Agregar una nueva columna en un segundo archivo.

### M4-E05 — Idempotencia

Reprocesar el mismo archivo y discutir cómo evitar duplicados.

### M4-E06 — Selección de patrón

Dado un escenario, elegir:

```text
Full
Incremental
Batch
Streaming
```

## Streaming

Mantenerlo fundamental.

No construir una arquitectura de streaming compleja para explicar el concepto.

---

# 18. Módulo 5 — Delta Lake, Medallion, Modelamiento y Calidad

## Objetivo pedagógico

Convertir transformaciones aisladas en un pipeline de datos confiable.

## Temas

- Delta Tables
- transaction log
- ACID
- Managed
- External
- INSERT
- UPDATE
- DELETE
- MERGE
- Upsert
- Time Travel
- Change Data Feed
- OPTIMIZE
- VACUUM
- Liquid Clustering conceptual/práctico según disponibilidad
- Bronze
- Silver
- Gold
- trazabilidad
- replay
- limpieza
- tipificación
- deduplicación
- joins
- reglas de negocio
- métricas
- agregaciones
- dimensiones
- hechos
- SCD Type 1
- SCD Type 2
- calidad
- Data Contracts
- inválidos

## Ejercicios recomendados

### M5-E01 — Crear tabla Delta

Convertir pólizas limpias a Delta.

### M5-E02 — UPDATE y DELETE

Utilizar un dataset muy pequeño para entender operaciones ACID.

### M5-E03 — MERGE de pólizas

```text
polizas_actuales
+
polizas_incremental
↓
MERGE
↓
polizas_actualizadas
```

### M5-E04 — Time Travel

Comparar dos versiones.

### M5-E05 — Medallion

```text
landing/polizas
      ↓
Bronze
      ↓
Silver
      ↓
Gold
```

### M5-E06 — Calidad

Separar:

```text
validos
invalidos
```

con reglas sencillas.

### M5-E07 — Gold

Crear indicadores:

- pólizas activas
- prima total
- siniestros reportados
- monto pagado

### M5-E08 — SCD

Usar una dimensión pequeña como `productos` o `proveedores`.

No utilizar un caso SCD innecesariamente complejo.

---

# 19. Módulo 6 — Lakeflow, Orquestación y Automatización

## Objetivo pedagógico

Pasar de notebooks ejecutados manualmente a un flujo controlado.

## Temas

- Lakeflow Jobs
- Jobs
- Tasks
- DAGs
- dependencias
- parámetros
- scheduling
- triggers
- llegada de archivos
- actualización de tablas
- retries
- Conditional Tasks
- branching
- loops
- errores
- repair
- rerun
- notificaciones
- Spark Declarative Pipelines
- Streaming Tables
- Materialized Views
- automatización
- idempotencia

## Ejercicios recomendados

### M6-E01 — Job de dos tareas

```text
01_ingesta
    ↓
02_transformacion
```

### M6-E02 — Job Medallion

```text
Bronze
  ↓
Silver
  ↓
Gold
```

### M6-E03 — Parametrización

Procesar una fecha recibida como parámetro.

### M6-E04 — Falla y reejecución

Provocar un error controlado y analizar:

- Run History
- retry
- rerun
- repair si está disponible

### M6-E05 — DAG

Diseñar un DAG aunque no todas sus capacidades puedan ejecutarse en Free Edition.

## Free Edition

Si Jobs o Pipelines están limitados por cuota:

- usar demostración del instructor
- proporcionar diagrama
- ejecutar notebooks secuencialmente como fallback
- no cambiar el objetivo pedagógico

---

# 20. Módulo 7 — Ingeniería de Software, Estándares, Git y CI/CD

## Objetivo pedagógico

Enseñar que Data Engineering también requiere prácticas de ingeniería de software.

## Temas

- naming
- taxonomías
- dominios
- DEV
- TEST
- UAT
- PRD
- Catalog
- Schema
- Table
- Job
- Pipeline
- Notebook
- repositorios
- columnas técnicas
- metadata
- logging
- identificador de ejecución
- configuración
- parametrización
- GitHub
- commits
- branches
- Pull Requests
- Code Review
- CI/CD
- promoción
- Bundles
- YAML
- CLI
- Terraform overview

## Ejercicios recomendados

### M7-E01 — Mejorar nombres

Transformar nombres poco claros en una convención estándar.

### M7-E02 — Parametrizar notebook

Separar:

```text
configuración
lógica
```

### M7-E03 — Branch de ejercicio

Crear una rama para una mejora.

### M7-E04 — Commit útil

Practicar un mensaje de commit descriptivo.

### M7-E05 — Pull Request

Crear o simular una revisión.

### M7-E06 — DEV a PRD

Analizar qué debería cambiar entre ambientes y qué no debe hardcodearse.

## CI/CD

Mantener el primer ejercicio sencillo.

No obligar a desplegar Terraform o Bundles completos para enseñar el principio.

---

# 21. Módulo 8 — Monitoreo, Troubleshooting, Performance y Optimización

## Objetivo pedagógico

Aprender a investigar un problema antes de modificar código al azar.

## Temas

- Job Run History
- Spark UI
- Jobs
- Stages
- Tasks
- Shuffle
- skew
- disk spilling
- Broadcast Join
- particionamiento
- paralelismo
- memory conceptual
- Out Of Memory
- library conflicts
- fallos de inicio
- performance
- costo
- FinOps

## Ejercicios recomendados

### M8-E01 — Diagnóstico de ejecución

Dado un error o captura, identificar causa probable.

### M8-E02 — Join grande con dimensión pequeña

Comparar conceptualmente el uso de Broadcast Join.

### M8-E03 — Shuffle

Identificar una operación que provoca shuffle.

### M8-E04 — Checklist

Aplicar:

```text
¿Qué falló?
¿Dónde falló?
¿Qué evidencia tengo?
¿Qué cambiaría?
¿Cómo valido la mejora?
```

## Regla

No crear intencionalmente una carga masiva para provocar problemas de memoria en Free Edition.

Los problemas complejos pueden simularse mediante logs, capturas o ejemplos pequeños.

---

# 22. Módulo 9 — Unity Catalog, Seguridad y Gobierno

## Objetivo pedagógico

Entender cómo se organizan, protegen y gobiernan los datos.

## Temas

- usuarios
- grupos
- Service Principals
- account
- workspace
- mínimo privilegio
- IAM conceptual
- Storage Credentials conceptual/demostrativo
- External Locations conceptual/demostrativo
- Metastore
- Catalog
- Schema
- Tables
- Views
- Volumes
- Ownership
- GRANT
- REVOKE
- DENY
- Lineage
- auditoría
- tags
- Discovery
- Column Masking overview
- Row Filters overview
- RLS overview
- ABAC overview
- Data Owner
- Data Steward
- Data Custodian
- metadata
- calidad
- políticas
- gobierno federado

## Ejercicios recomendados

### M9-E01 — Jerarquía

Crear o identificar:

```text
Catalog
  ↓
Schema
  ↓
Table
```

### M9-E02 — Mínimo privilegio

Dado tres perfiles:

```text
Data Engineer
Data Analyst
Auditor
```

definir permisos mínimos.

### M9-E03 — GRANT

Ejecutar una práctica pequeña si Free Edition lo permite.

### M9-E04 — Lineage

Observar lineage cuando esté disponible.

### M9-E05 — Roles de gobierno

Asignar responsabilidades entre:

- Owner
- Steward
- Custodian

## Regla

No bloquear el módulo por una capacidad administrativa no disponible.

Usar conceptual o demo cuando corresponda.

---

# 23. Módulo 10 — Data Mesh, Data Products y Disponibilización

## Objetivo pedagógico

Cerrar el curso conectando pipelines técnicos con consumo, ownership y reutilización.

## Temas

- Data Mesh
- Domain Ownership
- Data as a Product
- Self-Service Data Platform
- Federated Computational Governance
- cuándo aplicar Data Mesh
- limitaciones
- Data Product
- ownership
- contrato
- schema
- SLA
- SLO
- freshness
- calidad
- seguridad
- lineage
- documentación
- versionamiento
- discoverability
- Databricks SQL
- SQL Warehouse
- Views
- Materialized Views
- BI
- JDBC
- ODBC
- Delta Sharing overview
- Marketplace overview
- Lakehouse Federation overview
- fuente a consumidor

## Ejercicios recomendados

### M10-E01 — Diseñar un Data Product

Ejemplo:

```text
Data Product: Indicadores de Siniestros
Owner: Operaciones
Consumidores: Analítica / Gestión
Tabla Gold: gold_siniestros_resumen
Freshness: diaria
Calidad: monto >= 0
```

### M10-E02 — Contrato mínimo

Definir:

- schema
- owner
- freshness
- reglas de calidad
- consumidores

### M10-E03 — Publicación

Crear una View o consulta de serving cuando sea compatible.

### M10-E04 — Data Mesh

Decidir si un escenario necesita Data Mesh o si sería complejidad innecesaria.

---

# 24. Estrategia de ejercicios

Codex debe trabajar con cinco tipos de actividad.

```text
CONCEPT
DEMO
GUIDED
PRACTICE
ASSESSMENT
```

## `CONCEPT`

Actividad sin código para comprender arquitectura o decisión técnica.

## `DEMO`

El instructor ejecuta o muestra una capacidad.

## `GUIDED`

Los participantes siguen pasos explicados.

## `PRACTICE`

Los participantes resuelven una tarea con ayuda limitada.

## `ASSESSMENT`

Evaluación sin solución visible.

## Distribución recomendada

Una sesión normal puede incluir:

```text
Concepto
   ↓
Demo corta
   ↓
Ejercicio guiado
   ↓
Ejercicio de aplicación
   ↓
Cierre / aplicación diaria
```

No es obligatorio usar todos los pasos en cada sesión.

---

# 25. Plantilla obligatoria para cada ejercicio

Cada ejercicio debe incluir metadatos.

Ejemplo:

```markdown
# M3-E04 — Agregación de pólizas

## Metadata

- Módulo: 3
- Tema: GroupBy y agregaciones
- Tipo: GUIDED
- Duración estimada: 25 min
- Nivel: Fundamental
- Modalidad: PRACTICO_FREE
- Requiere S3: No
- Requiere GitHub: No
- Dataset: polizas.csv
- Conceptos previos: DataFrame, select, filter
```

Luego incluir:

```markdown
## Contexto de negocio

## Objetivo de aprendizaje

## Qué aprenderás

## Requisitos previos

## Dataset

## Escenario

## Actividades

## Resultado esperado

## Validación

## Aplicación en el trabajo diario

## Extensión opcional
```

## Resultado esperado

En ejercicios guiados puede mostrarse.

En evaluaciones no debe revelar la lógica de solución.

---

# 26. Regla "un concepto nuevo por ejercicio"

Como criterio general:

```text
1 ejercicio
≈
1 concepto principal nuevo
+
conceptos anteriores reutilizados
```

Ejemplo correcto:

```text
Nuevo: MERGE
Ya conocido: DataFrame + Delta
```

Ejemplo incorrecto:

```text
Nuevo: REST API + OAuth + Auto Loader + MERGE + SCD2 + Workflows
```

en un solo ejercicio introductorio.

---

# 27. Duración de ejercicios

Usar actividades compatibles con una capacitación síncrona.

## Microejercicio

```text
10 a 15 min
```

## Ejercicio corto

```text
20 a 30 min
```

## Ejercicio guiado

```text
30 a 45 min
```

## Laboratorio

Definir duración según cronograma de evaluación.

Codex no debe crear un ejercicio de 90 minutos si el objetivo puede aprenderse en 20 minutos.

---

# 28. Transferencia al trabajo diario

Todo ejercicio práctico debe contener:

```markdown
## Aplicación en el trabajo diario
```

Debe responder con ejemplos concretos.

### Ejemplo

```markdown
La misma lógica de carga incremental puede reutilizarse para procesar
solo los nuevos archivos de siniestros recibidos durante el día,
evitando releer todo el histórico.
```

### Evitar

```text
Este conocimiento será muy útil para tu trabajo.
```

Debe explicar **cómo**.

---

# 29. Diseño de laboratorios evaluados

Los laboratorios deben ser:

- claros
- pequeños
- verificables
- independientes de configuraciones frágiles
- orientados a seguros
- acumulativos en conocimiento
- realizables por un participante que siguió las sesiones

## No convertir la evaluación en troubleshooting de infraestructura

El laboratorio no debe medir si el alumno logra:

- resolver permisos AWS inesperados
- arreglar conectividad
- configurar networking
- superar cuotas de Free Edition
- recuperar secretos
- solucionar un servicio externo caído

Si una integración externa es necesaria, debe estar validada antes.

## Versiones

Cada evaluación debe tener:

```text
student/
instructor/
```

### Student

No contener:

- respuestas
- código final
- hints excesivos
- outputs que revelen la lógica
- rúbrica con detalles que entreguen la solución

### Instructor

Debe contener:

- solución
- resultado esperado
- validadores
- rúbrica
- errores frecuentes
- criterios de corrección
- tiempo estimado

---

# 30. Rúbricas

Las rúbricas deben medir capacidades observables.

Ejemplo para un laboratorio técnico:

| Criterio | Peso interno |
| --- | ---: |
| Lectura o ingesta | 15% |
| Transformaciones | 25% |
| Calidad | 15% |
| Resultado funcional | 20% |
| Uso correcto de conceptos Databricks | 15% |
| Claridad y buenas prácticas | 10% |

Adaptar al contenido realmente enseñado.

No evaluar Delta si Delta no forma parte del alcance.

---

# 31. Caso integrador progresivo

El curso debe evitar laboratorios totalmente aislados.

Usar un caso de seguros que evolucione.

## Fase 1 — Arquitectura

```text
Sistemas fuente
     ↓
AWS S3
     ↓
Databricks
```

## Fase 2 — Transformación

```text
polizas.csv
    ↓
PySpark / SQL
```

## Fase 3 — Ingesta

```text
Full + Incremental
```

## Fase 4 — Lakehouse

```text
Bronze
  ↓
Silver
  ↓
Gold
```

## Fase 5 — Automatización

```text
Job / Pipeline
```

## Fase 6 — Ingeniería de software

```text
GitHub + parámetros + estándares
```

## Fase 7 — Operación

```text
monitoreo + troubleshooting
```

## Fase 8 — Gobierno

```text
Unity Catalog + mínimo privilegio
```

## Fase 9 — Data Product

```text
Gold
 ↓
View / SQL
 ↓
Consumidor
```

---

# 32. Caso Final recomendado

El Caso Final debe utilizar un escenario simple.

## Ejemplo

**Procesamiento diario de pólizas y siniestros**

### Entradas

```text
polizas
siniestros
productos
```

### Flujo

```text
Source / S3
      ↓
Bronze
      ↓
Silver
      ↓
Gold
      ↓
Indicadores
```

### Actividades técnicas posibles

- cargar archivos
- validar schema
- limpiar datos
- eliminar duplicados
- realizar joins
- aplicar MERGE
- construir una tabla Gold
- ejecutar consultas SQL
- documentar arquitectura
- versionar solución
- explicar seguridad
- proponer un Data Product

## Indicadores sencillos

- cantidad de pólizas activas
- prima total
- cantidad de siniestros
- monto reclamado
- monto aprobado
- monto pagado
- siniestros por estado
- pólizas por producto

## No exigir

- modelos actuariales
- machine learning
- scoring de fraude
- pricing
- reservas técnicas
- modelos regulatorios complejos

salvo solicitud expresa.

---

# 33. Notebooks

## Formato preferido para GitHub

Cuando sea posible, preferir notebooks Databricks exportados como `.py` porque son fáciles de revisar en Git.

Ejemplo:

```python
# Databricks notebook source
# MAGIC %md
# MAGIC # M3-E01 — Lectura de pólizas

# COMMAND ----------

from pyspark.sql import functions as F
```

`.ipynb` es válido si existe una razón concreta.

## Estructura de notebook

```text
Título
Objetivo
Contexto
Setup
Carga
Transformación
Validación
Conclusión
Aplicación diaria
```

## Tamaño

Dividir cuando el notebook mezcle demasiados objetivos.

Ejemplo:

```text
00_setup.py
01_ingestion.py
02_transformation.py
03_quality.py
04_gold.py
05_validation.py
```

---

# 34. PySpark

## Preferencia

Usar APIs modernas y legibles.

```python
from pyspark.sql import functions as F
```

Preferir:

```python
F.col()
F.when()
F.to_date()
F.count()
F.sum()
```

sobre lógica Python fila por fila.

## Evitar inicialmente

- UDFs cuando existe función nativa
- código altamente funcional difícil de explicar
- metaprogramación innecesaria
- optimizaciones prematuras

## Objetivo

El estudiante debe poder leer el código y explicar qué hace.

---

# 35. Spark SQL

Los ejercicios deben incluir SQL cuando contribuya al aprendizaje.

Ejemplo:

```sql
SELECT
    estado_poliza,
    COUNT(*) AS cantidad
FROM polizas
GROUP BY estado_poliza
```

Cuando sea pedagógicamente útil, resolver el mismo problema en:

```text
PySpark
Spark SQL
```

y comparar.

---

# 36. Delta Lake

Enseñar Delta progresivamente.

Orden recomendado:

```text
crear tabla
    ↓
leer
    ↓
insertar
    ↓
update / delete
    ↓
MERGE
    ↓
Time Travel
    ↓
optimización y características avanzadas
```

No comenzar con CDF o Liquid Clustering antes de que el participante entienda una tabla Delta.

---

# 37. Arquitectura Medallion

Usar el significado:

## Bronze

- ingesta
- mínima transformación
- metadata
- trazabilidad
- replay

## Silver

- tipificación
- limpieza
- deduplicación
- calidad
- joins
- reglas

## Gold

- métricas
- agregaciones
- datos para consumo

## Ejemplo asegurador

```text
S3 / archivos
     ↓
bronze.polizas
     ↓
silver.polizas
     ↓
gold.polizas_resumen
```

No convertir Gold automáticamente en un modelo dimensional si el ejercicio no lo requiere.

---

# 38. Modelamiento

Introducir modelos de manera progresiva.

Ejemplos sencillos:

```text
dim_producto
dim_asegurado
fact_siniestro
fact_pago
```

Para SCD:

- comenzar con Type 1
- introducir Type 2 con una dimensión pequeña
- utilizar pocas columnas
- explicar claramente `fecha_inicio`, `fecha_fin` y `es_actual`

---

# 39. Calidad de datos

Las reglas deben ser comprensibles.

Ejemplos:

```text
id_poliza no nulo
id_siniestro no nulo
prima >= 0
monto_pagado >= 0
fecha_fin >= fecha_inicio
estado dentro de catálogo permitido
```

Separar cuando sea útil:

```text
valid
invalid
```

Toda regla debe tener una razón de negocio.

---

# 40. Automatización

Los Jobs deben comenzar pequeños.

Primer ejemplo:

```text
Task A
  ↓
Task B
```

Luego:

```text
Bronze
  ↓
Silver
  ↓
Gold
```

Solo después agregar:

- condiciones
- retries
- parámetros
- loops
- triggers

---

# 41. Monitoreo y troubleshooting

Enseñar método, no adivinanza.

Usar siempre:

```text
1. identificar síntoma
2. revisar evidencia
3. localizar componente
4. formular hipótesis
5. realizar cambio mínimo
6. volver a medir
```

Crear logs o errores controlados para prácticas.

No provocar incidentes costosos.

---

# 42. Gobierno y seguridad

Mantener separación entre:

```text
autenticación
autorización
gobierno
```

Usar principio de mínimo privilegio en todos los escenarios.

Ejemplo:

```text
Data Engineer
    → escritura Silver

Data Analyst
    → lectura Gold

Auditor
    → lectura de objetos autorizados
```

No asumir que esta matriz representa la organización real del cliente.

---

# 43. Data Products

Un Data Product del curso debe tener como mínimo:

```text
nombre
dominio
owner
descripción
schema
consumidores
freshness
calidad
seguridad
SLA/SLO conceptual
versionamiento
```

Ejemplo:

```text
Nombre: dp_siniestros_operativos
Dominio: Siniestros
Owner: <rol ficticio>
Freshness: diaria
Tabla principal: gold.siniestros_operativos
```

---

# 44. Datasets

## Tamaño

Preferir datasets pequeños.

Orientación:

```text
100 a 5,000 filas
```

para la mayoría de ejercicios.

Se puede usar más cuando exista una razón pedagógica, pero no para simular "Big Data" artificialmente.

## Generación

Guardar scripts reproducibles en:

```text
scripts/generate-data/
```

Usar una semilla cuando exista aleatoriedad.

Ejemplo:

```python
random.seed(42)
```

## Privacidad

Todo dato debe ser sintético.

No usar:

- DNI reales
- nombres reales de asegurados
- correos reales
- teléfonos reales
- pólizas reales
- siniestros reales

---

# 45. Estructura del repositorio

Mantener una estructura similar a:

```text
databricks-associate-training/
│
├── AGENTS.md
├── README.md
├── .gitignore
├── LICENSE
│
├── docs/
│   ├── syllabus.md
│   ├── cronograma.md
│   ├── environment.md
│   ├── standards.md
│   └── resources.md
│
├── datasets/
│   ├── README.md
│   ├── raw/
│   ├── incremental/
│   ├── sample/
│   └── generated/
│
├── modules/
│   ├── module-01-cloud-aws/
│   ├── module-02-databricks/
│   ├── module-03-spark/
│   ├── module-04-ingestion/
│   ├── module-05-delta-medallion/
│   ├── module-06-lakeflow/
│   ├── module-07-git-cicd/
│   ├── module-08-monitoring/
│   ├── module-09-governance/
│   └── module-10-data-products/
│
├── sessions/
│   └── README.md
│
├── assessments/
│   ├── lab-01/
│   │   ├── student/
│   │   └── instructor/
│   ├── lab-02/
│   │   ├── student/
│   │   └── instructor/
│   └── final-case/
│       ├── student/
│       └── instructor/
│
├── images/
│   ├── architecture/
│   ├── concepts/
│   ├── infographics/
│   ├── covers/
│   └── assessments/
│
├── scripts/
│   ├── generate-data/
│   ├── validation/
│   └── utilities/
│
└── config/
    ├── README.md
    └── example.env
```

## `modules/`

Contiene material curricular por módulo.

## `sessions/`

Solo debe utilizarse cuando exista un cronograma que asigne contenido a sesiones concretas.

No duplicar todo el material de `modules/`.

Se pueden crear archivos de sesión que referencien recursos existentes.

---

# 46. Estructura por módulo

Ejemplo:

```text
modules/module-03-spark/
├── README.md
├── theory/
├── demos/
├── exercises/
│   ├── guided/
│   └── practice/
├── notebooks/
├── visuals/
└── instructor/
```

## `README.md`

Debe incluir:

- objetivo
- temas
- prerequisites
- resultados de aprendizaje
- recursos
- ejercicios
- aplicación diaria

---

# 47. Visuales

La capacitación debe utilizar visuales para simplificar conceptos.

Herramientas previstas:

- **Archify** para arquitecturas y diagramas técnicos
- **ChatGPT Images** para infografías y láminas conceptuales
- **Mermaid** para diagramas versionables
- **Codex** para definir técnicamente qué debe mostrar el visual

## Codex no debe improvisar arte binario

Cuando se necesite una imagen:

1. definir objetivo pedagógico
2. identificar audiencia
3. definir componentes
4. definir flujo
5. definir mensaje principal
6. recomendar formato
7. crear especificación

## Estructura

```text
visuals/
├── README.md
├── architecture-spec.md
├── concept-spec.md
└── prompts.md
```

## Archify

Usar preferentemente para:

- On-Premise → AWS → Databricks
- S3 + Databricks
- Control Plane / Compute Plane
- Spark Driver / Executors
- Batch vs Streaming
- Full vs Incremental
- Medallion
- Lakeflow DAG
- Git / CI/CD flow
- Unity Catalog hierarchy
- Data Product
- flujo end-to-end

## ChatGPT Images

Usar preferentemente para:

- portada
- infografía
- comparación visual
- concepto abstracto
- resumen de módulo
- lámina de recapitulación

## Mermaid

Usar cuando el diagrama:

- sea simple
- deba versionarse como código
- no requiera iconografía oficial

---

# 48. Plantilla para especificación visual

```markdown
# Visual: Arquitectura de ingesta de siniestros

## Objetivo pedagógico
Explicar cómo un archivo recibido llega desde object storage hasta una tabla Silver.

## Herramienta recomendada
Archify

## Formato
16:9 horizontal

## Componentes
- Sistema fuente
- AWS S3
- Databricks
- Bronze
- Silver
- Gold

## Flujo
Sistema fuente → S3 → Bronze → Silver → Gold

## Mensaje principal
Separar ingesta, limpieza y consumo.

## Restricciones
- poco texto
- máximo 6 componentes principales
- no mostrar servicios no explicados
```

---

# 49. Estándar visual

Preferir:

- diseño corporativo
- 16:9 para láminas
- poco texto
- jerarquía clara
- flechas simples
- iconografía correcta
- consistencia entre módulos

Evitar:

- arquitecturas saturadas
- 20 servicios en una sola lámina
- flechas cruzadas
- componentes que no se explican
- logos solo por decoración

---

# 50. Soluciones del docente

Las soluciones deben vivir fuera del material del estudiante.

Ejemplo:

```text
instructor/
├── solution.py
├── expected-results.md
├── rubric.md
└── troubleshooting.md
```

No enlazar desde el README del estudiante a estas soluciones.

---

# 51. Validaciones automáticas

Cuando sea razonable, crear validadores en:

```text
scripts/validation/
```

Ejemplos:

- schema esperado
- columnas existentes
- conteos controlados
- ausencia de duplicados
- valores no negativos
- tabla creada

## Regla de evaluación

El validador no debe revelar la solución.

Debe comprobar el resultado.

---

# 52. Código y estilo

## Código

Debe ser:

- simple
- legible
- reproducible
- pedagógico
- modular cuando aporte claridad

## Comentarios

Comentar el **por qué**, no cada línea.

## Nombres

Usar nombres claros:

```text
df_polizas
df_siniestros
df_productos
```

Evitar:

```text
df1
df2
x
tmp2
```

salvo variables temporales obvias.

## Idioma

Documentación en español.

Conceptos oficiales y APIs pueden mantenerse en inglés.

---

# 53. Convenciones de nombres

Archivos:

```text
kebab-case
```

Notebooks secuenciales:

```text
00-setup.py
01-read-policies.py
02-transform-policies.py
03-quality-checks.py
```

Tablas y columnas:

```text
snake_case
```

Ejemplo:

```text
silver.polizas
gold.siniestros_resumen
fecha_actualizacion
monto_pagado
```

---

# 54. Configuración

Nunca hardcodear valores de entorno en la lógica principal.

Usar variables como:

```python
catalog_name = "<CATALOG_NAME>"
schema_name = "<SCHEMA_NAME>"
volume_name = "<VOLUME_NAME>"
s3_bucket = "<S3_BUCKET>"
```

Cuando se pueda, centralizar configuración en un notebook o archivo de setup.

---

# 55. README de un ejercicio

Debe poder entenderse sin la presencia del instructor.

Debe indicar:

- qué hará el estudiante
- por qué lo hará
- qué necesita
- cuánto demora
- qué debe entregar
- cómo sabe si terminó

No incluir explicación ambigua como:

```text
Procesar los datos correctamente.
```

Preferir:

```text
Eliminar duplicados por `id_poliza` conservando el registro con la
`fecha_actualizacion` más reciente.
```

solo cuando esa regla ya haya sido enseñada o forme parte explícita del requerimiento.

---

# 56. Criterios de aceptación para material nuevo

Antes de considerar terminado cualquier ejercicio, validar:

## Currículo

- corresponde al módulo correcto
- no adelanta contenido no enseñado
- tiene un objetivo concreto

## Negocio

- utiliza contexto asegurador
- no requiere reglas actuariales complejas
- usa datos sintéticos

## Técnica

- es compatible con el entorno o tiene fallback
- no contiene secretos
- rutas y nombres son coherentes
- código es reproducible

## Pedagogía

- dificultad adecuada
- tiempo razonable
- resultado verificable
- aplicación diaria explicada

## Evaluación

- no filtra soluciones
- instructor y student están separados cuando corresponde

## Visual

- si un diagrama mejora el concepto, existe especificación visual o Mermaid

---

# 57. Proceso obligatorio para Codex al recibir una tarea

Cuando el usuario diga, por ejemplo:

```text
Crea el ejercicio del Módulo 3 sobre joins
```

Codex debe:

1. leer `AGENTS.md`
2. revisar `docs/syllabus.md` si existe
3. revisar `docs/cronograma.md` si la tarea menciona una sesión
4. revisar archivos del módulo
5. identificar conceptos ya enseñados
6. seleccionar un caso asegurador sencillo
7. decidir si requiere S3
8. decidir compatibilidad Free Edition
9. reutilizar datasets existentes si es posible
10. crear el material de estudiante
11. crear solución solo si fue solicitada o si la estructura del módulo la requiere
12. crear validación
13. crear especificación visual si aporta valor
14. actualizar README o índice del módulo
15. comprobar que no existan secretos ni respuestas filtradas

---

# 58. Proceso para crear un laboratorio completo

Cuando el usuario solicite:

```text
Crea el Laboratorio 1
```

Codex no debe empezar escribiendo código inmediatamente.

Debe:

1. revisar el cronograma hasta la sesión correspondiente
2. listar competencias evaluables
3. excluir contenidos futuros
4. definir un escenario asegurador
5. limitar cantidad de entidades
6. definir tiempo
7. definir entregables
8. definir rúbrica
9. identificar dependencias de Free Edition
10. evitar S3 si no está garantizado
11. preparar fallback
12. crear dataset sintético
13. crear versión student
14. crear versión instructor
15. crear validadores
16. ejecutar o revisar estáticamente la solución
17. comprobar que la versión student no revele respuestas

---

# 59. Proceso para crear una sesión

Cuando el usuario solicite material de una sesión:

1. revisar el cronograma
2. identificar módulo y temas
3. definir 2 a 4 objetivos de aprendizaje
4. elegir conceptos
5. elegir una demo corta
6. elegir 1 o 2 ejercicios
7. indicar tiempo aproximado
8. incluir aplicación aseguradora
9. incluir visual cuando ayude
10. preparar código compatible con Free Edition

No convertir cada sesión en un mini proyecto.

---

# 60. Qué no debe hacer Codex

Codex no debe:

- saltarse los fundamentos Cloud del inicio
- asumir que todo el curso comienza con Databricks
- crear ejercicios genéricos de retail si existe un equivalente sencillo de seguros
- usar datos personales reales
- inventar sistemas internos de La Positiva
- introducir más tecnología de la necesaria
- exigir AWS si Free Edition impide la integración
- guardar credenciales
- crear ejercicios que dependan de servicios de pago no autorizados
- usar capacidades enterprise como requisito sin fallback
- mezclar solución del docente con versión de estudiante
- enseñar conceptos futuros dentro de evaluaciones
- crear notebooks de cientos de líneas para un concepto básico
- utilizar complejidad como sinónimo de calidad
- convertir el curso en preparación exclusiva para el examen
- enseñar herramientas fuera del syllabus sin explicar por qué son necesarias

---

# 61. Qué sí debe optimizar Codex

Priorizar:

```text
claridad
    >
complejidad
```

```text
aplicación práctica
    >
cantidad de funcionalidades
```

```text
reutilización diaria
    >
ejemplo artificial
```

```text
ejercicio ejecutable
    >
arquitectura imposible de probar
```

```text
concepto entendido
    >
código sofisticado
```

---

# 62. Resultado esperado del repositorio

Al finalizar el programa, el repositorio debe permitir observar una evolución clara:

```text
Cloud y AWS
    ↓
Arquitectura moderna
    ↓
Databricks
    ↓
Spark
    ↓
Ingesta
    ↓
Delta Lake
    ↓
Medallion
    ↓
Lakeflow
    ↓
Git / CI-CD
    ↓
Monitoreo
    ↓
Gobierno
    ↓
Data Product
```

Y el caso asegurador debe evolucionar paralelamente:

```text
archivos de pólizas y siniestros
            ↓
almacenamiento
            ↓
lectura
            ↓
transformación
            ↓
calidad
            ↓
Delta
            ↓
Bronze / Silver / Gold
            ↓
automatización
            ↓
versionamiento
            ↓
gobierno
            ↓
consumo
```

Ese flujo constituye la guía principal para crear ejercicios, laboratorios y el Caso Final.

---

# 63. Principio final

El éxito de un laboratorio no se mide por cuántas funcionalidades de Databricks utiliza.

Se mide por si el participante:

1. comprende el concepto
2. puede ejecutarlo
3. puede explicar qué hizo
4. puede reconocer cuándo usarlo
5. puede reutilizarlo posteriormente en una situación real de Data Engineering

Todo material generado por Codex debe contribuir a ese objetivo.
