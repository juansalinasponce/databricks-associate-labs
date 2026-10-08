# Guía del instructor — Laboratorio incremental SQL y parte PySpark

## Preparación

La ruta principal establece cargas incrementales, tablas persistentes y SQL
paso a paso para negocio y analistas. La [parte PySpark](../pyspark/README.md)
reproduce el flujo con DataFrames y Delta, incluidos ejercicios y automatización
con notebooks Python. Ambas rutas comparten tablas y control; ejecutarlas
secuencialmente y mantener un solo Job activo. El laboratorio integra Delta/Medallion de
la Sesión 07 con las consultas solicitadas y prepara Jobs como continuación.
No modifica Docs/cronograma.md, Docs/syllabus.md ni evaluaciones oficiales.

Antes de clase:

1. Validar SQL Warehouse y una External Location que cubra el prefijo S3 de la práctica.
2. Reemplazar <S3_BUCKET> en 00 y ejecutarlo desde SQL Editor: crea el volumen
   externo workspace.bronze.s07_archivos y las tablas. Las rutas no deben solaparse.
3. Preparar USE CATALOG, USE SCHEMA y READ/WRITE VOLUME para los participantes.
   [permisos-volumen.sql](permisos-volumen.sql) contiene el ejemplo con grupo ficticio.
   El creador necesita CREATE VOLUME y CREATE EXTERNAL VOLUME en la ubicación autorizada.
4. Crear las carpetas polizas, productos y siniestros desde Catalog Explorer.
5. Preparar los SQL 01–06 como consultas de SQL Editor y archivos de Workspace.
   Probar la primera entrega subida desde Databricks; reservar la segunda.
6. Preparar fallback de volumen/tablas administradas si S3 no está habilitado.
7. Para PySpark, crear notebooks Python con los archivos 01–06 de pyspark y
   probar compute serverless, DeltaTable y COPY INTO desde spark.sql. Explicar
   cada sección comentada; no sumar dos recorridos completos a los 120 minutos.

Si se ejecutó el DDL anterior, CREATE TABLE IF NOT EXISTS no modifica sus columnas.
Revisar DESCRIBE TABLE y usar [migracion-fecha-carga.sql](migracion-fecha-carga.sql)
solo en las tablas Bronze que no tienen fecha_carga. Después ejecutar 00 para
crear volumen y pendientes. Los registros antiguos conservan fecha_carga NULL;
las nuevas cargas toman CURRENT_DATE(). No borrar tablas ni alterar fechas históricas.

## Conducción de la sesión

Trabajar directamente en SQL Editor, ejecutando sentencias por selección.
Los comentarios explican cada paso. No se crean parámetros de fecha ni se
cambian valores antes de procesar la segunda entrega. El participante sube los
CSV desde Databricks y el volumen escribe en su LOCATION S3.

Distinguir id_lote (identificador en CSV), fecha_actualizacion (momento del cambio),
fecha_carga (CURRENT_DATE) y fecha_proceso (CURRENT_TIMESTAMP). Ambas entregas
pueden cargarse el mismo día; si se suben juntas, el proceso elige la versión
más reciente por clave y cierra ambas. Para ver la transición, cargarlas por separado.

Antes de ejecutar, preguntar qué tabla se lee, qué tabla se modifica y qué
representa una fila. El objetivo es explicar un flujo cotidiano. El DDL y los
permisos están preparados; no se escriben desde cero durante la actividad.

La ruta ocupa 120 minutos: 48 de explicación y 72 de ejecución. La configuración
completa del Job tiene 30–40 minutos adicionales y utiliza tareas SQL / File;
seguir la [guía de automatización](automatizacion/README.md).

## Resultados por producto

| Lote | Producto | Pólizas | Activas | Primas informadas | Prima total | Promedio | Mínimo | Máximo | Siniestros | Sin monto | Monto registrado |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2026-10-06 | P01 | 4 | 3 | 3 | 3,700 | 1,233.33 | 1,000 | 1,500 | 3 | 1 | 800 |
| 2026-10-06 | P02 | 4 | 3 | 4 | 4,000 | 1,000.00 | 800 | 1,200 | 2 | 0 | 600 |
| 2026-10-06 | P03 | 3 | 3 | 3 | 2,200 | 733.33 | 600 | 900 | 3 | 0 | 400 |
| 2026-10-06 | P99 | 1 | 1 | 1 | 500 | 500.00 | 500 | 500 | 0 | 0 | 0 |
| 2026-10-07 | P01 | 4 | 3 | 4 | 4,900 | 1,225.00 | 1,000 | 1,600 | 3 | 0 | 1,000 |
| 2026-10-07 | P02 | 4 | 3 | 4 | 4,200 | 1,050.00 | 800 | 1,400 | 2 | 0 | 500 |
| 2026-10-07 | P03 | 4 | 4 | 4 | 3,400 | 850.00 | 600 | 1,200 | 5 | 0 | 950 |
| 2026-10-07 | P99 | 1 | 1 | 1 | 500 | 500.00 | 500 | 500 | 0 | 0 | 0 |

El nombre final de P03 es Seguro Hogar Integral Demo. SIN009 queda fuera de
los indicadores porque POL999 no se suministró; sus 100 PEN se muestran aparte.
No convertir la prima desconocida de POL003 en cero en el primer lote.

[respuestas-practica-sql.sql](respuestas-practica-sql.sql) contiene las consultas
breves del cierre. Primer lote: Salud lidera con 4,000 PEN; segundo: Auto con
4,900 PEN. Conteos por canal iniciales: AGENCIA 3, CORREDOR 3, DIGITAL 4,
SIN_CANAL 2; al final DIGITAL pasa a 5.

## Errores frecuentes

| Síntoma | Qué revisar |
| --- | --- |
| Bronze se duplica al repetir | Archivo renombrado/recreado o force = true; no confundir copia dentro del CSV con archivo repetido |
| Prima inicial = 11,900 | Se están sumando filas originales sin deduplicar |
| Cinco filas del segundo CSV se consideran cinco pólizas nuevas | Incluye tres cambios, una alta y una copia exacta del alta |
| P02 conserva la prima de POL007 | Falta recalcular el producto anterior antes del traslado |
| P03 conserva el nombre anterior | Una actualización de producto también debe afectar Gold |
| Monto final = 2,850 | SIN005 se contabilizó dos veces en lugar de actualizar su póliza |
| El promedio incluye cero en POL003 | Desconocido no significa cero; AVG ignora NULL |
| P99 desaparece | Se usó INNER para enriquecer la cartera |
| COUNT(*) da un evento en una póliza sin siniestros | Tras LEFT usar COUNT(s.id_siniestro) |
| Un lote antiguo retrocede una prima | MERGE debe comparar fecha_actualizacion |
| Una corrección reutiliza id_lote | Publicar una entrega nueva; las entregas cerradas son inmutables |
| Falla la recepción de productos sin cambios | Esta práctica requiere al menos una fila por entidad; producción usa manifiesto y permite cero cambios |
| Se ejecuta 05 antes de 04 | Corregir el orden o las dependencias; no registrar cierre manualmente |

## Revisión formativa

Sin peso de evaluación oficial. Verificar que el participante:

- Ubica Bronze, detalle e indicadores desde Catalog.
- Explica archivo nuevo frente a clave nueva.
- Comprueba el mismo resultado tras repetir una entrega.
- Identifica una actualización y un alta mediante las tablas.
- Justifica LEFT, nulos y la agregación de siniestros previa al join.
- Ejecuta dos consultas breves y las utiliza para explicar los indicadores.
- Identifica el paso fallido en un DAG y la evidencia de control.

## Verificación técnica

Ejecutar desde la raíz:

```bash
python3 -m pip install duckdb==1.4.3
python3 scripts/validation/validar-sesion-07-sql.py
```

La dependencia es solo para mantenimiento del repositorio; no se instala en
Databricks ni la necesita el participante. El verificador ejecuta el SQL en
DuckDB con una conexión independiente por archivo. Adapta Delta/S3 a tablas
locales y funciones específicas de Databricks. COPY INTO se simula mediante
un registro de archivos cargados; no se verifican su historial real ni el volumen externo.

Se comprobaron ambos lotes, todas las métricas por producto, joins, ranking,
versiones y reejecución sin cambios cuando no hay entregas nuevas. Un
indicador corrupto y una entrega incompleta se rechazan. Se probaron también
dos entregas en la misma ejecución, fechas del servidor y ausencia de parámetros. También se verificó retirar
el indicador de un producto que pierde su última póliza sin cambiar la prima
total, incluida su reejecución. El acceso real S3, volumen, Delta, COPY INTO y Jobs se
validan en el workspace antes de clase. El alcance y las adaptaciones están
descritos en el propio script.

Para verificar la parte PySpark localmente, usar PySpark 3.5.1, Java 11 y
delta-spark 3.2.0, con los jars delta-spark_2.12 y delta-storage 3.2.0. No instalar
estas dependencias en los notebooks del alumno: Databricks proporciona su runtime.

```bash
python3 -m pip install pyspark==3.5.1 delta-spark==3.2.0
S07_DELTA_JARS=/ruta/delta-spark_2.12-3.2.0.jar,/ruta/delta-storage-3.2.0.jar \
SPARK_LOCAL_IP=127.0.0.1 python3 scripts/validation/validar-sesion-07-pyspark.py
```

Este verificador ejecuta los archivos Python con contextos independientes y
tablas Delta reales locales. Compara todas las métricas Gold, los cuatro joins
y el ranking en ambas entregas; verifica reejecución estable, cierre prematuro
e indicador incorrecto. Adapta catálogo y almacenamiento; COPY INTO usa una
simulación local del registro de archivos. Volumen, permisos S3, historial COPY
y Jobs requieren prueba en Databricks. Los valores esperados de SQL y PySpark
se mantienen en un único archivo de referencia.

Las respuestas de la práctica PySpark están en
[respuestas-practica-pyspark.py](respuestas-practica-pyspark.py), solo para el
instructor. SQL y PySpark deben producir los mismos resultados con estas entregas.

Regenerar los seis CSV con `python3 scripts/generate-data/generar-sesion-07.py`.
Este generador usa solo la biblioteca estándar y produce únicamente los seis CSV. Verificar generación reproducible antes de distribuir.
