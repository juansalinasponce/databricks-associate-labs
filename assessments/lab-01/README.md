# Evaluación 1 — Cloud, Databricks y preparación de pólizas

## Ficha

| Campo | Valor |
| --- | --- |
| Sesión y fecha | 06 — 05 de octubre de 2026 |
| Cobertura | Materiales de las sesiones 01 a 05 |
| Tipo | `ASSESSMENT` |
| Nivel | Fundamental |
| Duración de esta versión | 120 minutos |
| Teoría / práctica | 45 / 60 minutos |
| Instrucciones y break | 5 / 10 minutos |
| Puntaje interno propuesto | Teoría: 40; práctica: 60; total: 100 |
| Peso oficial | 30% de la nota del programa |
| Entorno principal | Databricks Free Edition; S3 opcional |

La petición menciona 90 minutos, pero los bloques solicitados suman 120.
Esta versión conserva los bloques de 45 + 60 + 15 minutos y las dos horas de
la sesión previstas en el cronograma. La duración queda como supuesto de
diseño pendiente de confirmación del docente. No aplicar esta versión en 90
minutos recortando el tiempo de los participantes.

## Agenda

| Minutos desde el inicio | Bloque | Duración |
| --- | --- | ---: |
| 00–05 | Explicación de instrucciones y entregables | 5 min |
| 05–50 | Evaluación teórica individual | 45 min |
| 50–60 | Break | 10 min |
| 60–120 | Un ejercicio práctico y entrega | 60 min |

La entrega está incluida en los 60 minutos de práctica. No se introduce
contenido nuevo. Los 5 minutos iniciales explican el procedimiento, no resuelven
preguntas ni demuestran transformaciones.

## Materiales

- [Guía del participante](student/README.md).
- [Evaluación teórica](student/evaluacion-teorica.md).
- [Ejercicio práctico](student/ejercicio-practico.md).
- [Plantilla de notebook](student/plantilla_evaluacion.py).
- [Dataset sintético](student/data/polizas_evaluacion_01.csv).
- [Revisión de cobertura](instructor/cobertura-sesiones-01-05.md).
- [Guía del instructor y rúbrica](instructor/README.md).
- [Respuestas de teoría](instructor/respuestas-teoria.md).
- [Solución SQL](instructor/solucion.sql).
- [Solución PySpark](instructor/solucion_pyspark.py).
- [Validador de resultado](instructor/validar_resultado.py).
- [Resultados de referencia](instructor/resultados-esperados.json).

Compartir únicamente la carpeta `student/` durante la evaluación. Los archivos
del instructor son para preparación y corrección; una carpeta en un repositorio
público no constituye un control de acceso. Distribuir el paquete del estudiante
y conservar las soluciones fuera del acceso de los participantes hasta el cierre.

## Criterio de diseño

Un caso de aseguradora ficticia, una sola entidad y un archivo de 500 filas.
Se evalúan selección de herramientas, carga, inspección, preparación básica,
consulta e interpretación. SQL es la vía recomendada; PySpark es equivalente
y no concede puntos adicionales. No se exige implementar Medallion completo,
MERGE, streaming, Jobs, Pipelines, dashboards ni funciones administrativas.

## Compatibilidad

La carga de archivos permite crear tablas Delta administradas y revisar los
tipos en la interfaz; requiere compute disponible y permiso de creación en el
schema. El instructor comprueba estas condiciones antes de la evaluación.
[Documentación oficial de carga](https://docs.databricks.com/aws/en/ingestion/create-or-modify-table).

Free Edition utiliza compute serverless sujeto a cuotas. No se pide crear un
clúster clásico ni resolver restricciones del entorno durante la prueba.
[Limitaciones oficiales](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations).

## Estado

Material preparado en el repositorio. No se ha creado ni publicado un formulario
en Google Forms. La teoría puede trasladarse a Forms; los dos casos abiertos
requieren corrección manual y el tiempo se controla por el instructor.
