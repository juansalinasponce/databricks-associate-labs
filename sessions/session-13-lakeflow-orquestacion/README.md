# Sesión 13 — Despliegue básico Bronze → Silver

Material preparado para la PPT `Sesion13_Despliegue_Produccion_Databricks_DMC.pptx`
y la solicitud del docente de introducir Bundles con un ejemplo mínimo.

- [Laboratorio: paso a paso desde Databricks](resources/laboratorio-13-bundle-bronze-silver/README.md)
- [Configuración del Bundle](resources/laboratorio-13-bundle-bronze-silver/databricks.yml)
- [CSV sintético de seis filas](resources/laboratorio-13-bundle-bronze-silver/data/polizas.csv)

## Revisión de la PPT para el docente

Se revisaron las 17 diapositivas, incluyendo las láminas incrustadas como imágenes.

| Diapositiva | Observación para explicar el laboratorio |
| --- | --- |
| 4 | La idea «mismo código, distinta configuración» se demuestra con los targets `dev` y `prd`. |
| 5 | El CSV incluido aquí es una muestra sintética distribuible. El despliegue excluye `data/`; el participante carga el archivo en un Volume de cada ambiente. Los datos de negocio reales permanecen fuera de Git. |
| 8 | La PPT denomina la herramienta **Declarative Automation Bundles**, antes **Databricks Asset Bundles**. Para la introducción basta decir «Bundle: código y definición del Job juntos». |
| 9 | El YAML de la lámina es ilustrativo: `volume_base` necesita declararse y asignarse como variable para usarlo en un Bundle. Usar el `databricks.yml` del laboratorio como ejemplo ejecutable. Una ruta `/Volumes/...` puede corresponder a un volumen administrado o externo; la ruta por sí sola no demuestra una conexión con S3. Aquí usamos volúmenes administrados. |
| 10–11 | `validate`, `deploy` y `run` tienen propósitos distintos. Guardar el YAML o ejecutar un notebook no despliega el Bundle. La práctica principal utiliza la interfaz si está habilitada; los comandos quedan como equivalencia opcional. |
| 12–13 | Para empezar basta revisar las dos tareas y repetir la ejecución: los conteos permanecen iguales porque reemplazamos las tablas de la práctica. |
| 16–17 | El laboratorio solicitado simplifica este flujo a dos tareas y dos ambientes. El ciclo de branches y PR puede explicarse después. |

**Ajuste de alcance:** `Docs/cronograma.md` y `Docs/syllabus.md` asignan gobierno a
la sesión 13 y Bundles como overview a la 14. Este material sigue la instrucción
explícita actual del docente y la PPT de despliegue de la sesión 13; no modifica
la planificación general ni las evaluaciones oficiales.

La revisión utiliza exclusivamente archivos locales. Los controles de Bundles
en el navegador y las cuotas del workspace requieren comprobación en el entorno
del instructor; la guía incluye una alternativa sin despliegue.
