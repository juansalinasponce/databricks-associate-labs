# Guía del instructor — Evaluación 1

## Antes de iniciar

1. Confirmar el supuesto de 120 minutos y anunciar los bloques 5 + 45 + 10 + 60.
2. Revisar [la cobertura](cobertura-sesiones-01-05.md) y confirmar que las prácticas
   de las sesiones 04 y 05 fueron efectivamente realizadas por el grupo.
3. Compartir únicamente `student/`, sin clave, soluciones ni resultados esperados.
4. Definir si se permiten apuntes o IA y comunicarlo antes del inicio. Propuesta:
   teoría sin consulta; práctica con apuntes y materiales de sesiones anteriores,
   sin colaboración entre participantes. La política de IA queda a decisión docente.
5. Comprobar acceso a Workspace, Catalog, carga de archivos y compute serverless;
   asignar catálogo, schema e identificadores individuales. No usar tablas comunes
   como salidas de varios alumnos.
6. Hacer una ejecución de la solución en el workspace del curso. La verificación
   local del repositorio no sustituye esta comprobación de UI, permisos y cuotas.
7. Tener una fuente de respaldo con las once columnas STRING. Cargar el CSV sin
   inferencia de tipos y comprobar 500 filas antes de iniciar.
8. Si se emplea Google Forms, copiar la teoría y configurar 15 preguntas de opción
   múltiple de 2 puntos y 2 preguntas abiertas de 5 puntos. Revisar manualmente
   estas últimas y liberar notas después de la revisión. No confiar en el formulario
   como temporizador: el instructor abre y cierra la recepción en los horarios.

## Agenda de conducción

| Desde inicio | Actividad |
| --- | --- |
| 00–05 | Explicar entregas, tiempo, nombres de tablas y procedimiento de contingencia. |
| 05–50 | Teoría; atender únicamente dudas del enunciado. |
| 50–60 | Break; cerrar la recepción de teoría. |
| 60–120 | Práctica; reservar sus últimos 5 minutos para entrega. |

No dar soluciones durante el break ni ampliar el alcance con una demostración
nueva. Aplicar el mismo criterio de ayuda a todos.

## Rúbrica práctica — 60 puntos

| Criterio | Evidencia y distribución | Máximo |
| --- | --- | ---: |
| Fuente e inspección | Ingesta o configuración explicada en fallback: 2; muestra y conteo: 2; schema: 2; dos defectos observados: 2. | 8 |
| Preparación | Texto normalizado: 4; canales faltantes: 3; prima/fechas/timestamp tipados: 5; duplicados exactos: 3; vigencia inclusiva con estado ACTIVA: 3. | 18 |
| Tabla y controles | Salida consultable y nombre aislado: 3; Catalog y schema final: 2; conteos y diferencia explicados: 3; control de canales faltantes: 2. | 10 |
| Reporte | Solo VIGENTE: 3; grupos producto + moneda: 3; conteo/suma/promedio correctos: 5; orden y decimales: 1; producto líder en PEN e interpretación: 2. | 14 |
| Comunicación y entrega | Gráfico de cantidad por producto para PEN: 4; elección de herramienta y función del compute: 2; registro/storage/fallback: 2; código y evidencias identificables: 2. | 10 |
| Total | | 60 |

Aplicar puntaje por evidencia; no todo o nada. En tipado, distribuir 2 puntos
a prima, 2 a las dos fechas y 1 a timestamp. En métricas, distribuir 1 a conteo,
2 a suma y 2 a promedio. No descontar de nuevo por cada cifra derivada de un mismo
error de limpieza: registrar el error origen y valorar el procedimiento correcto
en el reporte. El validador ayuda a contrastar resultados, no asigna la nota.

La teoría vale 40 puntos. La evaluación suma 100; si el programa usa escala
vigesimal, `nota_e1 = puntos / 5`. Su aporte a la nota final es
`nota_e1 × 0.30`. No modificar los pesos de las otras evaluaciones ni inventar
un umbral de aprobación.

## Resultados y validación

Consultar `resultados-esperados.json`. Ejecutar `validar_resultado.py` en el
workspace, cambiando únicamente `TABLA_SALIDA` al nombre del alumno. Validar una
tabla del instructor primero. El validador muestra discrepancias y usa `assert`;
no compartirlo antes de cerrar la recepción.

Para revisar el código: `solucion.sql` es la referencia principal y
`solucion_pyspark.py` ofrece una alternativa. Ambos parten de la fuente con
las once columnas STRING. El gráfico se configura en la interfaz y se revisa
visualmente; no se simula como un dashboard publicado.

## Opción A — práctica principal

Carga local de CSV → tabla fuente STRING → preparación SQL o PySpark → tabla
Delta administrada → reporte y visualización. S3 solo cuando esté previamente
validado para todo el grupo. No se crean clústeres clásicos ni nuevas ubicaciones
externas durante la evaluación.

## Opción B — fallback para Free Edition

- **Carga bloqueada:** entregar una tabla fuente de respaldo con los mismos datos
  y tipos. Puntuar ingesta por su configuración explicada y la inspección realizada.
- **Creación de tablas bloqueada:** proporcionar un schema con permisos o aceptar
  un resultado en vista temporal/DataFrame. Revisar el código de escritura propuesto;
  el instructor puede ejecutarlo en una salida aislada. No penalizar el permiso.
- **Cuota agotada o caída:** detener el reloj del afectado y registrar el incidente.
  Recibir el código y las decisiones, y completar la evidencia funcional en una
  ventana equivalente con compute disponible. No atribuir puntaje de ejecución
  sin verificar ni marcar la prueba incompleta como un fallo técnico del alumno.
- **Visualización no disponible:** aceptar captura de la tabla de resultados y
  especificación de barras, eje X producto, eje Y cantidad, filtro PEN, interpretada.

No otorgar bonificaciones por acceso S3 o por resolver ambas implementaciones.

## Qué cambia en producción

Los accesos se gobiernan con roles y permisos, las tablas se organizan por
dominio y los procesos se automatizan. El examen se limita al flujo ya practicado
en las sesiones 04 y 05, con almacenamiento administrado para reducir dependencias.

Los archivos CSV pueden estar en Volumes, pero las tablas Delta se crean como
tablas administradas; no se almacena una tabla Delta dentro de un Volume.
[Guía oficial de Volumes](https://docs.databricks.com/aws/en/volumes/).

## Errores frecuentes

- Comparar `activa` sin normalizar o conservar espacios exteriores.
- Sustituir NULL y dejar canales vacíos como cadena vacía.
- Deduplicar después de añadir un identificador diferente por fila.
- Conservar solo VIGENTE en la tabla preparada, perdiendo las demás pólizas.
- Usar fecha de hoy en lugar de la fecha de corte fija.
- Excluir fecha_inicio o fecha_fin cuando coinciden con el corte.
- Agrupar solo por producto y sumar PEN con USD.
- Graficar prima_total cuando el enunciado solicita cantidad_polizas.
- Sobrescribir `workspace.bronze.polizas` de las sesiones anteriores.

## Regenerar datos y verificación local

Desde la raíz del repositorio:

```bash
python3 scripts/generate-data/generar_evaluacion_01.py
python3 scripts/validation/validar_evaluacion_01_local.py
```

El generador reproduce las primeras 475 pólizas y los primeros 25 duplicados
del universo de la sesión 05. No utiliza información real ni aleatoriedad.
La verificación local compara el dataset con el oráculo de referencia, comprueba
la lógica SQL en SQLite con adaptaciones explícitas de dialecto y revisa la
sintaxis Python. No certifica ejecución de Spark ni acceso a Databricks.
