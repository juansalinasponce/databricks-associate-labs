# Clave teórica — uso exclusivo del instructor

## Selección única

Cada acierto vale 2 puntos; máximo 30. No descontar errores.

| Pregunta | Respuesta | Fundamento |
| ---: | :---: | --- |
| 01 | B | El cliente define acceso y protección de su información. |
| 02 | C | En IaaS administra el SO y las aplicaciones sobre recursos virtuales. |
| 03 | D | Ajusta recursos hacia arriba y hacia abajo según la demanda. |
| 04 | A | Una región contiene varias AZ. |
| 05 | C | S3 aporta almacenamiento de objetos. |
| 06 | B | Lakehouse combina flexibilidad con gestión y análisis confiables. |
| 07 | D | Catalog permite descubrir tablas y revisar metadata. |
| 08 | A | Workspace organiza notebooks y otros artefactos de trabajo. |
| 09 | B | Editor: autoría; warehouse: ejecución de SQL. |
| 10 | C | Un notebook reúne narrativa, código y resultados. |
| 11 | D | Driver coordina; Executors ejecutan tareas sobre particiones. |
| 12 | A | `filter` prepara el plan; `count` es una acción. |
| 13 | C | Un importe requiere un tipo numérico para análisis. |
| 14 | B | `GROUP BY` y `COUNT(*)` producen el conteo por producto. |
| 15 | D | `_delta_log` registra transacciones y versiones de Delta. |

## Caso 16 — 5 puntos

Respuesta esperada, con redacción o diagrama equivalente:

```text
Sistema On-Premise → S3 landing → Databricks → S3 output → analista
```

| Evidencia observable | Puntos |
| --- | ---: |
| Flujo con fuente, landing, preparación, resultado y consumidor | 1 |
| Diferencia entre almacenamiento en S3 y procesamiento en Databricks | 1 |
| Ingesta: escritura en landing, sin administración total | 1 |
| Proceso: lectura de landing y escritura en output | 1 |
| Analista: lectura de output; no requiere acceso raw a landing | 1 |

La matriz es de capacidades funcionales, no una policy exhaustiva. Un proceso
que verifica lo que escribió podría necesitar lectura adicional, debidamente
justificada. No exigir nombres de acciones IAM ni permisos administrativos.

## Caso 17 — 5 puntos

| Evidencia observable | Puntos |
| --- | ---: |
| Reutiliza la tabla existente y evita una copia innecesaria | 1 |
| Elige SQL Editor + warehouse o notebook SQL con compute y lo justifica | 1 |
| Distingue el editor/notebook del recurso que ejecuta el cálculo | 1 |
| Normaliza estado: espacios exteriores y mayúsculas; verifica categorías | 1 |
| Convierte prima a numérico; verifica schema y una suma coherente | 1 |

Aceptar SQL o PySpark y vocabulario equivalente. No exigir una vista nueva,
un dashboard o una solución Medallion. Una elección de notebook bien explicada
obtiene el mismo puntaje que SQL Editor.

## Corrección

Las respuestas abiertas se revisan manualmente. No reducir puntos por ortografía
si la decisión técnica es clara. Otorgar puntos de cada evidencia aunque otra
parte del caso sea incorrecta. Registrar un comentario breve por pérdida de puntos.
