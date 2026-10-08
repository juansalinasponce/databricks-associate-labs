# Evaluación teórica 1 — Sesiones 01 a 05

## Metadata

- Tipo: `ASSESSMENT`; nivel: fundamental.
- Duración: 45 minutos.
- Puntaje: 40 puntos.
- Contexto: aseguradora ficticia `aseguradora_demo`.
- Requisitos: conceptos Cloud, AWS, Databricks y datos vistos en las sesiones
  01 a 05; no requiere acceso a AWS ni Databricks.

## Instrucciones

Las preguntas 01 a 15 tienen una sola respuesta correcta y valen 2 puntos cada
una. Las preguntas 16 y 17 son casos abiertos de 5 puntos cada uno. No hay
descuento por una respuesta incorrecta. Reserva aproximadamente 25 minutos
para selección única y 20 minutos para los casos.

Identificador del participante: ____________________

## Selección única — 30 puntos

### 01. Responsabilidad compartida

Una aseguradora guarda archivos en Amazon S3. ¿Qué responsabilidad conserva?

A. Mantener físicamente los discos de AWS.
B. Configurar quién puede acceder a sus objetos y proteger sus datos.
C. Reparar la infraestructura de las Availability Zones.
D. Administrar los edificios de los centros de datos.

### 02. IaaS

El equipo contrata máquinas virtuales y administra su sistema operativo y sus
aplicaciones. ¿Qué modelo describe esta situación?

A. SaaS.
B. PaaS.
C. IaaS.
D. Un servicio sin responsabilidades para el cliente.

### 03. Elasticidad

El procesamiento requiere más recursos durante el cierre mensual y menos
durante el resto del mes. ¿Qué decisión representa elasticidad?

A. Mantener permanentemente la capacidad del pico.
B. Copiar los datos en carpetas con nombres diferentes.
C. Incrementar el tamaño de cada CSV.
D. Aumentar y reducir recursos según la demanda.

### 04. Región y Availability Zones

¿Cuál es la relación correcta?

A. Una región contiene varias Availability Zones.
B. Una Availability Zone contiene todas las regiones del mundo.
C. Son dos nombres para un mismo bucket.
D. Una región representa una tabla de Databricks.

### 05. S3 y procesamiento

En el flujo archivos de pólizas → S3 → Databricks → reporte, ¿qué función
principal cumple S3?

A. Ejecutar las transformaciones PySpark.
B. Administrar los notebooks.
C. Almacenar objetos de datos.
D. Ejecutar las consultas en el SQL Warehouse.

### 06. Lakehouse

¿Qué describe mejor el propósito de una arquitectura Lakehouse?

A. Reemplazar toda necesidad de permisos de acceso.
B. Combinar flexibilidad de almacenamiento con capacidades confiables de
   gestión y análisis de datos.
C. Guardar exclusivamente imágenes y documentos.
D. Ejecutar solo modelos de machine learning.

### 07. Catalog Explorer

Antes de cargar otra copia de pólizas, quieres descubrir si ya existe una
tabla y revisar sus columnas. ¿Dónde comenzarías?

A. En la configuración de un bucket nuevo.
B. En la creación de una máquina virtual.
C. En un editor de diapositivas.
D. En Catalog Explorer.

### 08. Workspace

¿Qué activo organizarías directamente en una carpeta del Workspace?

A. Un notebook con código y explicación del análisis.
B. Los discos físicos de S3.
C. Una Availability Zone.
D. El sistema operativo del proveedor Cloud.

### 09. SQL Editor y SQL Warehouse

Un analista quiere consultar una tabla existente con SQL. ¿Qué combinación
es adecuada?

A. Bucket e IAM como sustitutos del motor SQL.
B. SQL Editor para escribir la consulta y SQL Warehouse para ejecutarla.
C. Workspace sin ningún recurso de ejecución.
D. Un archivo CSV como motor de consulta.

### 10. Notebook

Debes explicar un proceso, ejecutar SQL y revisar una transformación con
Python/PySpark en un mismo documento. ¿Qué herramienta elegirías?

A. Una policy de IAM.
B. El nombre de un bucket.
C. Un notebook.
D. Una Availability Zone.

### 11. Driver y Executors

¿Qué reparto de funciones corresponde al modelo fundamental de Spark?

A. El Driver almacena buckets y los Executors asignan permisos IAM.
B. Los Executors diseñan el reporte y el Driver define regiones.
C. El Driver sustituye el almacenamiento de S3.
D. El Driver coordina la ejecución y los Executors procesan tareas sobre
   particiones de datos.

### 12. Transformación y acción

Observa este fragmento de PySpark:

```python
activas_df = polizas_df.filter(col("estado_poliza") == "ACTIVA")
cantidad = activas_df.count()
```

¿Cuál es la interpretación correcta?

A. `filter` construye una transformación y `count` solicita un resultado que
   dispara la ejecución del plan.
B. `filter` crea un bucket y `count` cambia los permisos.
C. Ambas líneas únicamente cambian los comentarios de la tabla.
D. `count` devuelve otro DataFrame sin solicitar resultados.

### 13. Schema y prima

La prima llega como texto `"1250.50"` y necesitas sumar importes. ¿Qué harías?

A. Mantenerla como texto y ordenar alfabéticamente.
B. Convertirla en un nombre de tabla.
C. Revisar el schema y convertirla a un tipo numérico adecuado.
D. Eliminar todas las filas que contienen una prima.

### 14. Agregación SQL

¿Qué consulta cuenta las pólizas por producto?

A. `SELECT id_producto FROM polizas LIMIT 1;`
B. `SELECT id_producto, COUNT(*) AS cantidad FROM polizas GROUP BY id_producto;`
C. `SELECT COUNT(*) FROM polizas WHERE id_producto IS NULL;`
D. `SELECT * FROM polizas ORDER BY id_producto;`

### 15. Delta básico

En el almacenamiento de una tabla Delta observas archivos Parquet y
`_delta_log/`. ¿Para qué sirve este último?

A. Para guardar contraseñas de acceso a S3.
B. Para almacenar los notebooks del Workspace.
C. Para sustituir los archivos que contienen las filas.
D. Para registrar las transacciones y versiones de la tabla.

## Casos de aplicación — 10 puntos

### 16. Arquitectura y mínimo privilegio — 5 puntos

Un sistema On-Premise entrega diariamente un CSV de pólizas. El proceso de
ingesta deposita ese archivo en `landing/`; Databricks lee los originales y
escribe resultados en `output/`. Un analista solo necesita consultar los
resultados preparados y no debe modificarlos.

1. Describe el flujo desde la fuente hasta el analista e identifica dónde se
   almacenan y dónde se procesan los datos.
2. Indica el permiso mínimo del proceso de ingesta sobre `landing/`, del
   proceso de Databricks sobre `landing/` y `output/`, y del analista sobre
   `output/`. Explica por qué el analista no necesita acceso a `landing/`.

Responde en 6 a 10 líneas o con un diagrama y una tabla breve. No escribas una
policy JSON ni utilices credenciales.

### 17. Herramientas y preparación — 5 puntos

En Catalog Explorer encuentras una tabla de pólizas preparada y documentada.
Un compañero propone volver a subir el mismo CSV y crear otra copia para
responder cuántas pólizas activas hay por producto. También existe un CSV
nuevo con estados como `" activa "` y primas almacenadas como texto.

1. Para la consulta sobre la tabla existente, elige el activo y la herramienta
   que usarías, explica la función del compute y justifica tu decisión sobre
   crear otra copia.
2. Para el CSV nuevo, describe dos preparaciones necesarias antes de calcular
   indicadores y cómo comprobarías que tuvieron efecto.

Responde en 6 a 10 líneas. Puedes mencionar SQL o PySpark; no se exige código.

## Resultado esperado y validación

Entrega 15 alternativas seleccionadas y las dos respuestas abiertas. Revisa
que cada caso tenga decisiones y justificaciones, y que hayas respondido
todas sus partes.

## Aplicación en el trabajo diario

Estas decisiones permiten interpretar la ruta de archivos de seguros, solicitar
permisos acotados, reutilizar tablas existentes y elegir el entorno adecuado
para preparar y consultar datos.

## Extensión opcional

No aplica durante la evaluación.
