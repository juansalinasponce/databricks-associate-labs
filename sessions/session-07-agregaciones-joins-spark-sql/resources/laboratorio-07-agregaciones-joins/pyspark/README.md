# Parte PySpark — El mismo laboratorio, paso a paso

## Metadata

| Campo | Valor |
| --- | --- |
| Sesión | 07; alternativa solicitada por el instructor |
| Tipo | GUIDED + PRACTICE |
| Nivel | Fundamental; explicar cada transformación antes de ejecutarla |
| Herramienta | Notebook con lenguaje Python; Catalog Explorer para subir archivos |
| Duración | 120 minutos si se elige esta ruta; no ejecutar ambas rutas completas en ese tiempo |
| Modalidad | PRACTICO_CONDICIONAL con S3; fallback administrado para Free Edition |
| Catálogo y schema | workspace.bronze |
| Datos | Los mismos seis CSV ficticios de pólizas, productos y siniestros |
| Fechas de proceso | current_date() y current_timestamp() del motor Spark |
| Entrega | Notebooks ejecutados, resultados Gold y evidencia de reejecución |

## Contexto de negocio

La aseguradora recibe archivos que agregan pólizas y actualizan primas, productos
y siniestros. Queremos conservar lo recibido y actualizar tablas de consulta sin
volver a cargar los mismos archivos. Esta parte reproduce el flujo SQL con
DataFrames y operaciones Delta desde Python.

## Objetivo de aprendizaje

Leer un DataFrame, limpiar sus columnas, seleccionar la versión más reciente,
actualizar otra tabla y construir indicadores persistentes. Reconocer cómo se
expresan en PySpark las operaciones que ya se practicaron en SQL.

## Qué aprenderás

| Operación conocida en SQL | Equivalente en PySpark |
| --- | --- |
| SELECT, WHERE, columna calculada | select(), filter(), withColumn() |
| GROUP BY y agregaciones con alias | groupBy().agg(), F.count/sum/avg/min/max, alias() |
| INNER, LEFT, RIGHT, FULL JOIN | join(..., "inner/left/right/full") |
| SELECT DISTINCT | dropDuplicates() para filas o claves sin elección de versión |
| COALESCE, IS NULL | F.coalesce(), isNull() |
| UPPER, LOWER, TRIM | F.upper(), F.lower(), F.trim() |
| YEAR, MONTH, DATEDIFF | F.year(), F.month(), F.datediff() |
| ROW_NUMBER() OVER (...) | Window + F.row_number().over(...) |
| MERGE INTO una tabla Delta | DeltaTable.forName(...).merge(...) |

F es el nombre corto de las funciones de Spark. col("prima") identifica una
columna y lit(0) representa un valor fijo. Estas funciones trabajan sobre
columnas completas. No necesitamos programar el procesamiento fila por fila.

## Requisitos previos

1. Completar la preparación del [laboratorio principal](../README.md): ejecutar
   [00-crear-tablas-s3.sql](../00-crear-tablas-s3.sql) en **SQL Editor** una vez.
   Sustituir el bucket en ese archivo y verificar permisos y External Location.
2. Conservar el volumen **workspace.bronze.s07_archivos**, con LOCATION
   `s3://<S3_BUCKET>/landing/sesion-07/`. Las tablas tienen ubicaciones S3
   distintas del volumen. No crear otro volumen sobre el mismo prefijo.
3. Disponer de notebooks Python con compute serverless compatible y Delta Lake.
   `spark`, `display` y `delta.tables` los proporciona Databricks; el participante
   no instala Spark ni crea una SparkSession.

**SQL sigue siendo la ruta principal.** Los notebooks usan las mismas 14 tablas
y el mismo control de archivos que SQL. Elegir una ruta para cada ejecución y
esperar a que termine antes de usar la otra. Si SQL ya procesó las dos entregas,
PySpark encontrará cero pendientes y conservará los resultados actuales.
Para observar la transición, cambiar de ruta antes de subir la segunda entrega.

## Dataset y escenario

Usar [los CSV existentes](../data), sin generar datos nuevos. Cada entrega
contiene un archivo por entidad. El id_lote viene dentro del archivo; no se
escribe como parámetro de ejecución. Las fechas de octubre identifican versiones
ficticias de negocio. Se puede ejecutar el laboratorio cualquier día.

```text
Carga desde la interfaz Databricks → volumen externo en S3
    → Bronze original → entregas pendientes → lote limpio
    → detalle Silver → indicadores Gold → validación y cierre
```

Todos los nombres siguen en workspace.bronze. Los prefijos s07_bronze,
s07_silver y s07_gold describen la función de cada tabla. Los DataFrames son
resultados de trabajo; los pasos guardan los datos en tablas Delta. No se crean
vistas como destino del proceso.

## Actividades

### Paso 1 — Crear los notebooks Python

1. Abrir **Workspace** y crear una carpeta `s07_pyspark`.
2. Elegir **Create → Notebook**, con lenguaje predeterminado **Python**.
3. Crear seis notebooks con los nombres de los archivos 01–06 de esta carpeta.
4. Abrir cada archivo .py del repositorio, copiar su contenido y pegarlo en una
   celda Python del notebook correspondiente. Se pueden separar las secciones
   comentadas en varias celdas, conservando su orden.
5. Seleccionar compute serverless. Ejecutar los notebooks uno por uno, en orden.

El código Python se ejecuta en notebooks Python. Los archivos SQL existentes
continúan ejecutándose directamente en SQL Editor. No agregar comandos de cambio
de lenguaje ni de ejecución de otros notebooks. Cada paso importa sus funciones
y lee sus propias tablas; no depende de variables del notebook anterior.

### Paso 2 — Subir la primera entrega desde Databricks

1. En **Catalog**, abrir workspace → bronze → Volumes → s07_archivos.
2. Crear las carpetas `polizas`, `productos` y `siniestros` si todavía no existen.
3. Usar **Upload files to volume** y seleccionar la carpeta de destino.
4. Subir solamente los tres CSV terminados en `2026-10-06.csv`, cada uno en su
   carpeta. La [guía principal](../README.md) muestra la carga por interfaz.

La carga al volumen externo guarda los CSV en S3. No es necesario utilizar la
consola de AWS. No reemplazar archivos ya procesados: una corrección debe llegar
como un archivo nuevo, con otro id_lote y una fecha_actualizacion posterior.

### Paso 3 — Cargar Bronze incremental

Ejecutar [01-cargar-bronze.py](01-cargar-bronze.py).

1. Revisar la fecha y hora que muestra Spark.
2. Observar las tres llamadas `spark.sql(...)`: ejecutan **COPY INTO**, el mismo
   mecanismo SQL de ingesta. Permite conservar su historial de archivos nuevos
   sin introducir otro sistema de ingesta. El resto del flujo usa DataFrames.
3. Revisar la tabla de entregas pendientes y los conteos por entrega.
4. Si falta una entidad, completar la carga de archivos y volver a ejecutar 01.

Resultado inicial: 13 filas Bronze de pólizas, 4 de productos y 10 de siniestros.
Los duplicados originales se conservan en Bronze. fecha_carga toma CURRENT_DATE()
del motor, sin widgets, parámetros ni una fecha escrita en Python.

### Paso 4 — Limpiar y elegir la versión de cada registro

Ejecutar [02-preparar-lote.py](02-preparar-lote.py).

1. `left_semi` conserva filas de entregas pendientes, sin agregar columnas del
   otro lado. `left_anti` conserva las que no tienen coincidencia; se usa en 01.
2. Leer los select: convierten fechas y montos, normalizan texto y sustituyen
   el canal nulo por SIN_CANAL. Un monto desconocido permanece nulo.
3. Revisar Window: agrupa por entrega y clave, ordena por fecha de actualización
   y deja la fila con posicion = 1.
4. Revisar el MERGE: inserta en s07_lote_* solamente claves que todavía no
   existen para esa entrega. Repetir este paso no agrega duplicados.

Resultado: 12 pólizas, 4 productos y 9 siniestros limpios en la primera entrega.
En estos CSV los empates de versión son duplicados idénticos. Si el origen
entrega versiones distintas con la misma fecha, se necesita otra regla de desempate.

### Paso 5 — Actualizar el detalle vigente

Ejecutar [03-actualizar-detalle.py](03-actualizar-detalle.py).

1. Observar cómo se guarda el producto anterior antes de actualizar una póliza.
2. Leer cada ventana: entre todas las entregas pendientes, elige una versión
   por clave para evitar múltiples coincidencias en MERGE.
3. `whenMatchedUpdateAll` actualiza las columnas cuando la versión recibida es
   más reciente. `whenNotMatchedInsertAll` inserta una clave nueva.
4. Las tablas de lote y Silver tienen las mismas columnas: por eso las variantes
   All pueden copiar las columnas por nombre. No habilitar evolución automática
   del esquema para este ejercicio.
5. Comparar las claves y versiones del resultado con las tablas de lote.

La lista s07_productos_afectados persiste antes y después de los cambios. Permite
recalcular ambos productos si una póliza se mueve, y recuperar un paso fallido.

### Paso 6 — Actualizar otra tabla con indicadores

Ejecutar [04-actualizar-indicadores.py](04-actualizar-indicadores.py).

1. Resumir los siniestros por póliza antes de unirlos a las primas: así una
   póliza con dos siniestros no duplica su prima.
2. Revisar groupBy y agg: count, sum, avg, min y max reciben alias claros.
3. Observar el LEFT JOIN al catálogo: P99 aparece como SIN_CATALOGO.
4. Verificar que MERGE actualiza los productos afectados en s07_gold_cartera.
5. Si un producto pierde su última póliza, se retira solamente su indicador.

Se recalcula la cartera vigente de los productos afectados. Las demás filas de
Gold se conservan; no se suma ciegamente el importe de cada archivo recibido.

### Paso 7 — Validar y cerrar

Ejecutar [05-validar-carga.py](05-validar-carga.py).

1. Comprobar que todas las versiones recibidas llegaron al detalle vigente.
2. Revisar unicidad y conciliaciones entre Silver y Gold.
3. Revisar SIN009: su póliza POL999 no existe y sus 100 PEN quedan fuera del
   monto asociado a la cartera; el registro se conserva para revisión.
4. El cierre registra fecha_proceso con F.current_timestamp(). Pendientes queda
   vacía solamente después de validar. Ante un error, corregir y repetir 01–05.

### Paso 8 — Practicar agregaciones, joins y funciones

Ejecutar [06-consultas-negocio.py](06-consultas-negocio.py) por secciones.
Comparar los resultados con [06-consultas-negocio.sql](../06-consultas-negocio.sql).
El archivo cubre las transformaciones básicas, las cinco agregaciones, alias,
los cuatro joins, columnas duplicadas, dropDuplicates, nulos, fechas, texto y ranking.

Resolver las dos actividades al final: producto con mayor prima total y pólizas
por canal. Explicar con palabras qué hace cada transformación antes de ejecutarla.

### Paso 9 — Subir el incremental y probar una reejecución

1. Subir los tres CSV terminados en `2026-10-07.csv` a las mismas carpetas.
2. Ejecutar nuevamente los notebooks 01–05 sin cambiar fechas ni código.
3. Ejecutar 06 para comparar prima, ranking y distribución por producto.
4. Repetir 01–05 sin subir archivos. Los conteos, montos y fechas de cierre
   anteriores deben conservarse. También pueden recibirse ambas entregas antes
   de ejecutar: el resultado final debe coincidir con la segunda entrega.

## Resultado esperado

| Evidencia | Primera entrega | Después del incremental |
| --- | ---: | ---: |
| Pólizas en Bronze | 13 | 18 |
| Pólizas en detalle Silver | 12 | 13 |
| Prima total conocida | 10,400 PEN | 13,000 PEN |
| Monto pagado asociado registrado | 1,800 PEN | 2,450 PEN |
| Pólizas con prima desconocida | 1 | 0 |
| Siniestros asociados con monto desconocido | 1 | 0 |
| Productos en Gold | 4 | 4 |
| Entregas cerradas | 1 | 2 |
| Entregas pendientes al finalizar | 0 | 0 |

El monto conocido no convierte los pagos nulos en pagos confirmados de cero.
La primera entrega tiene 10 pólizas activas; el incremental deja 11.

## Validación

Entregar evidencia de los conteos Bronze/Silver, las cuatro filas Gold, el
ranking de siete filas y las tablas de control y pendientes. Ejecutar 01–05
otra vez y demostrar que no cambian las filas ni los montos. Mostrar en una
consulta SQL Editor que las tablas creadas por PySpark son consultables con SQL.

## Automatización — Job de notebooks PySpark

Esta continuación toma 30–40 minutos adicionales, igual que la ruta SQL.

1. Abrir **Jobs & Pipelines → Create → Job** y nombrarlo
   `s07_cartera_incremental_pyspark`.
2. Crear tareas de tipo **Notebook**, con Source = Workspace. Seleccionar los
   notebooks Python que se probaron y compute serverless disponible.
3. Configurar el orden de dependencias y **Run if = All succeeded**:

   | Tarea | Notebook | Depends on |
   | --- | --- | --- |
   | cargar_bronze | 01-cargar-bronze | Ninguna |
   | preparar_lote | 02-preparar-lote | cargar_bronze |
   | actualizar_detalle | 03-actualizar-detalle | preparar_lote |
   | actualizar_indicadores | 04-actualizar-indicadores | actualizar_detalle |
   | validar_carga | 05-validar-carga | actualizar_indicadores |

4. No configurar parámetros de fecha. 00 es preparación única; 06 es consulta
   de negocio y queda fuera del Job.
5. Revisar que **Run as** tenga acceso a los notebooks, READ VOLUME, USE CATALOG,
   USE SCHEMA y SELECT/MODIFY sobre las tablas utilizadas.
6. Configurar **Max concurrent runs = 1** y un reintento por tarea. Coordinar
   con el Job SQL: la concurrencia de un Job no impide que otro escriba a la vez.
   Mantener una sola ruta de carga activa sobre estas tablas.
7. Elegir **Run now**. Revisar las cinco tareas en Run History y consultar Gold
   desde SQL Editor. Repetir Run now sin archivos nuevos y verificar estabilidad.
8. Preparar un horario diario, por ejemplo 08:00 America/Lima, después de recibir
   los tres archivos completos. Mantenerlo pausado durante las pruebas.
9. Si falla una tarea, revisar el error y corregir la causa. Repetir Run now o
   usar Repair run si está disponible. Las tablas pendientes conservan entregas
   fallidas de días anteriores: no se filtran solo por la fecha del día.

El Job PySpark usa notebooks y compute Python. El [Job SQL](../instructor/automatizacion/README.md)
continúa usando archivos .sql y SQL Warehouse. Los resultados se intercambian
mediante tablas persistentes, sin variables compartidas entre tareas.

## Opción A — práctica principal

Usar el volumen externo con LOCATION S3 y las tablas externas preparadas con 00.
Subir los archivos desde Databricks y ejecutar los notebooks y el Job PySpark.

## Opción B — fallback para Free Edition

Si S3 no está habilitado, aplicar la preparación administrada de la guía
principal: volumen con el mismo nombre y tablas sin LOCATION. Las rutas /Volumes
y el código Python se conservan; esta alternativa no acredita el S3 académico.
Si Jobs está limitado, ejecutar los notebooks 01–05 en orden manualmente y
observar la automatización en el entorno del instructor.

## Qué cambia en producción

Validar la recepción completa con un manifiesto, ampliar controles de calidad
y definir bajas y desempates. Este laboratorio supone entregas cerradas e
inmutables con al menos una fila por entidad. La carga es incremental por archivo
y por versión de clave; la búsqueda de pendientes consulta el historial Bronze.
No se presenta como un proceso CDC de alto volumen.

## Aplicación en el trabajo diario

SQL permite al analista consultar las tablas y construir indicadores con su
lenguaje habitual. PySpark permite expresar el mismo trabajo como transformaciones
de DataFrames en un notebook. Elegir la ruta que el equipo pueda mantener y
automatizar después de verificar los resultados.

## Extensión opcional

Procesar la primera entrega con SQL y la segunda con PySpark, de manera secuencial,
y explicar por qué el control compartido evita volver a cargar los archivos.

## Documentación oficial

- [MERGE desde Python y requisitos de coincidencia](https://docs.databricks.com/aws/en/delta/merge).
- [Tareas Notebook en Jobs](https://docs.databricks.com/aws/en/jobs/tasks/notebook).
- [COPY INTO](https://docs.databricks.com/aws/en/sql/language-manual/delta-copy-into).
- [Limitaciones de Free Edition](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations).
