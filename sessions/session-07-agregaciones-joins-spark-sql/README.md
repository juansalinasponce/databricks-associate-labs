# Sesión 07 — SQL Editor, volumen S3 y cargas incrementales

El [laboratorio paso a paso](resources/laboratorio-07-agregaciones-joins/README.md)
se ejecuta directamente en **SQL Editor**, con tablas persistentes en
**workspace.bronze** y fecha de carga automática mediante **CURRENT_DATE()**.

Los participantes suben sus CSV desde Databricks a un volumen externo:

```text
workspace.bronze.s07_archivos
/Volumes/workspace/bronze/s07_archivos/
                 ↕
s3://<S3_BUCKET>/landing/sesion-07/
```

00 crea el volumen externo con LOCATION S3 y las tablas. Después se ejecutan:

1. 01-cargar-bronze: incorpora archivos nuevos y detecta entregas pendientes.
2. 02-preparar-lote: limpia y deduplica las entregas pendientes.
3. 03-actualizar-detalle: aplica altas y versiones más recientes con MERGE.
4. 04-actualizar-indicadores: modifica los productos afectados.
5. 05-validar-carga: valida, registra el cierre con CURRENT_TIMESTAMP() y libera pendientes.
6. 06-consultas-negocio: agregaciones, joins, nulos, fechas, texto y ranking.

Los scripts son archivos SQL para copiar a SQL Editor y ejecutar por sentencias.
Las dos entregas sintéticas pueden procesarse el mismo día sin cambiar fechas.
La [guía de automatización](resources/laboratorio-07-agregaciones-joins/instructor/automatizacion/README.md)
utiliza cinco tareas SQL / File y los mismos scripts, sin parámetros de fecha.

La [parte PySpark paso a paso](resources/laboratorio-07-agregaciones-joins/pyspark/README.md)
ofrece el mismo flujo con DataFrames y MERGE Delta, consultas de negocio y un
Job de cinco notebooks Python. Comparte volumen, tablas y control con SQL;
elegir una ruta por ejecución y mantener una sola automatización activa.

Duración: 120 minutos, con práctica guiada y consultas breves. El DDL y los
permisos se preparan antes de clase; la configuración completa del Job continúa
la demostración de cierre. Los datos físicos de la práctica principal están en S3.

## Alcance

Esta versión sigue la solicitud del instructor para la Sesión 07: SQL Editor,
volumen externo S3, cargas incrementales y automatización. Reutiliza los temas
de Delta/Medallion de Docs/cronograma.md y Docs/syllabus.md y las consultas
solicitadas, sin cambiar la planificación general ni las evaluaciones.
