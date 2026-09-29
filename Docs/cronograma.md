# Cronograma operativo — 18 sesiones / 36 horas

## 1. Propósito

Este documento asigna el syllabus a 18 sesiones de 2 horas y define qué
conocimientos pueden utilizarse en cada evaluación.

La orientación vigente prioriza el uso práctico e integral de Databricks para
participantes técnicos, analíticos y de negocio. Spark se enseña a nivel
fundamental y aplicado; la selección y utilización correcta de las herramientas
de la plataforma es el eje principal.

## 2. Distribución

```text
15 sesiones de formación × 2 h = 30 h
 2 repasos aplicados       × 2 h =  4 h
 1 caso de uso final       × 2 h =  2 h
                                  ------
                                   36 h
```

La Sesión 1 se conserva sin modificaciones. Las sesiones 6 y 12 no introducen
contenido nuevo. La Sesión 18 utiliza sus 120 minutos para la elaboración y
entrega del caso de uso final.

## 3. Evaluaciones

| Sesión | Fecha | Actividad | Peso |
| ---: | --- | --- | ---: |
| 6 | 05 de octubre de 2026 | Repaso aplicado y Evaluación 1 | 30% |
| 12 | 28 de octubre de 2026 | Repaso aplicado y Evaluación 2 | 30% |
| 18 | 25 de noviembre de 2026 | Caso de uso final | 40% |

## 4. Secuencia pedagógica

```text
Cloud y AWS
  ↓
Mapa de la plataforma Databricks
  ↓
Navegación, SQL, notebooks e ingesta visual
  ↓
Delta Lake y Medallion
  ↓
SQL, Python y PySpark aplicados
  ↓
Pipelines, calidad y automatización
  ↓
Dashboards, Jobs y Alerts
  ↓
Gobierno y buenas prácticas
  ↓
Analítica, Genie y Agents
  ↓
Apps y Data Products
  ↓
Caso de uso final
```

## 5. Vista general

| Sesión | Bloque | Tema | Tipo |
| ---: | --- | --- | --- |
| 1 | M1 | Fundamentos Cloud y transición On-Premise → AWS | `CONCEPT` + `GUIDED` |
| 2 | M1 | S3, AWS CLI, IAM, Lakehouse y arquitectura moderna | `GUIDED` + `PRACTICE` |
| 3 | M2 | Tour integral de Databricks | `DEMO` + `GUIDED` |
| 4 | M2 | Notebooks, SQL Editor, Compute y lenguajes | `GUIDED` + `PRACTICE` |
| 5 | M3 | Data Ingestion, Catalog y Visual Data Prep | `GUIDED` + `PRACTICE` |
| 6 | Evaluación | Repaso aplicado y Evaluación 1 | `GUIDED` + `ASSESSMENT` |
| 7 | M4 | Delta Lake y Medallion | `GUIDED` + `PRACTICE` |
| 8 | M5 | SQL, Python y PySpark aplicados | `GUIDED` + `PRACTICE` |
| 9 | M6 | Lakeflow Pipelines, incremental y calidad | `GUIDED` + `PRACTICE` |
| 10 | M7 | Databricks SQL y AI/BI Dashboards | `GUIDED` + `PRACTICE` |
| 11 | M7 | Jobs, Tasks, monitoreo y Alerts | `DEMO` + `PRACTICE` |
| 12 | Evaluación | Repaso aplicado y Evaluación 2 | `GUIDED` + `ASSESSMENT` |
| 13 | M8 | Unity Catalog, seguridad y lineage | `CONCEPT` + `PRACTICE` |
| 14 | M8 | Organización, Git y eficiencia | `GUIDED` + `PRACTICE` |
| 15 | M9 | Modelos analíticos y MLflow | `DEMO` + `PRACTICE` |
| 16 | M9 | Genie Code, Genie Agents y asistentes | `GUIDED` + `PRACTICE` |
| 17 | M10 | Databricks Apps y Data Products | `DEMO` + `GUIDED` |
| 18 | Evaluación | Elaboración del caso de uso final | `ASSESSMENT` |

## 6. Resultado operativo por sesión

| Sesión | Resultado verificable |
| ---: | --- |
| 1 | Análisis On-Premise frente a Cloud; se mantiene el material existente |
| 2 | Bucket S3 con tres objetos, comparación de cargas, arquitectura y permisos mínimos |
| 3 | Mapa necesidad → herramienta de Databricks |
| 4 | Notebook multilenguaje con consulta, transformación y visualización |
| 5 | Tabla preparada mediante Visual Data Prep o SQL como fallback |
| 6 | Evidencia de navegación, selección de herramientas y análisis básico |
| 7 | Flujo Bronze → Silver → Gold con activos diferenciados |
| 8 | Solución y matriz de elección SQL/Python/PySpark/visual |
| 9 | Pipeline o DAG con ingesta, calidad, dependencia y salida |
| 10 | Dashboard con indicadores, visualizaciones y filtro |
| 11 | Job o diseño equivalente con schedule, error, recuperación y Alert |
| 12 | Flujo integrado desde fuente hasta indicador automatizable |
| 13 | Matriz de permisos y evidencia o interpretación de lineage |
| 14 | Propuesta de organización y activo refactorizado/versionado |
| 15 | Comparación de Runs e interpretación del resultado analítico |
| 16 | Consulta generada y validada; ficha de Genie Agent |
| 17 | Ficha de Data Product y elección dashboard/Agent/App |
| 18 | Solución integrada y decisiones justificadas |

## 7. Alcance por evaluación

### Sesión 6 — Repaso aplicado y Evaluación 1

Puede evaluar únicamente:

- fundamentos Cloud, AWS, S3 e IAM
- Data Warehouse, Data Lake y Lakehouse
- mapa de componentes de Databricks
- Workspace, Catalog, Compute, SQL Editor y notebooks
- ingesta y preparación básica
- elección de la herramienta adecuada

No requiere Spark avanzado, Delta Lake avanzado, Medallion implementado,
Pipelines, dashboards, Jobs, gobierno, IA ni Apps.

### Sesión 12 — Repaso aplicado y Evaluación 2

Puede evaluar lo anterior y además:

- Delta Lake y Medallion
- SQL, Python y PySpark a nivel fundamental
- Full e Incremental Load
- Lakeflow Pipelines, schema e idempotencia
- reglas de calidad
- AI/BI Dashboards
- Jobs, Tasks, Run History y Alerts

No requiere Unity Catalog avanzado, Git/CI-CD, modelos analíticos, Genie Agents
ni Databricks Apps.

### Sesión 18 — Caso de uso final

Integra todos los bloques. No exige implementar cada capacidad. Evalúa:

- selección de herramientas
- preparación o reutilización de datos
- Medallion simplificado y resultado Gold
- indicador o visualización
- diseño de automatización y monitoreo
- seguridad y buenas prácticas
- elección del canal de consumo
- claridad de las decisiones

## 8. Compatibilidad del entorno

| Capacidad | Modalidad principal | Fallback |
| --- | --- | --- |
| Workspace, notebooks, SQL y Catalog | `PRACTICO_FREE` | No aplica |
| Carga de archivos | `PRACTICO_FREE` | Dataset incluido en el repositorio |
| Visual Data Prep | `PRACTICO_CONDICIONAL` | SQL o notebook guiado |
| Lakeflow Pipelines | `PRACTICO_CONDICIONAL` | Ejecución secuencial + DAG |
| AI/BI Dashboards | `PRACTICO_CONDICIONAL` | Visualización de notebook |
| Jobs y Alerts | `PRACTICO_CONDICIONAL` | Demo + plantilla de configuración |
| Unity Catalog administrativo | `DEMO_INSTRUCTOR` | Matriz y simulación de permisos |
| MLflow / modelo | `PRACTICO_CONDICIONAL` | Resultados precalculados |
| Genie Code | `PRACTICO_CONDICIONAL` | Prompt y respuesta preparada |
| Genie Agents | `PRACTICO_CONDICIONAL` | Demo + diseño de agente |
| Databricks Apps | `PRACTICO_CONDICIONAL` | Demo + wireframe |
| Amazon S3 | `PRACTICO_CONDICIONAL` | Storage administrado o archivos locales |

## 9. Caso asegurador común

Se utilizará un universo sintético y ficticio:

```text
asegurados
  └── polizas ── productos
         ├── pagos
         └── siniestros ── proveedores
```

No se utilizarán datos reales ni se asumirán sistemas, reglas o arquitectura
interna de La Positiva.

## 10. Regla de diseño de actividades

Toda actividad debe:

1. partir de una necesidad de negocio
2. identificar la herramienta apropiada de Databricks
3. introducir pocos conceptos nuevos
4. producir un resultado verificable
5. incluir una buena práctica de organización, seguridad o costo
6. ofrecer fallback cuando dependa de una capacidad condicionada
7. evitar programación avanzada innecesaria
8. ser ejecutable dentro de la sesión

## 11. Regla de actualización

Actualizar este documento si cambia:

- la disponibilidad del entorno corporativo
- el acceso a Visual Data Prep, Genie, Agents o Apps
- la duración o fecha de una sesión
- el esquema de evaluación
- la integración directa con Amazon S3

Después de cualquier cambio, revisar la consistencia con `Docs/syllabus.md` y
los materiales de las sesiones ya cerradas.
