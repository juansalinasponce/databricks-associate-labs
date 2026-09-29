# Syllabus

## 1. Información general

| Campo | Definición |
| --- | --- |
| Programa | Especialización en Databricks Data Engineering y Lakehouse sobre AWS |
| Cliente | La Positiva |
| Duración total | 36 horas cronológicas |
| Organización | 18 sesiones de 2 horas |
| Horas de formación | 30 horas |
| Repasos aplicados y evaluados | 4 horas |
| Caso de uso final | 2 horas |
| Participantes | 31 profesionales con perfiles técnicos, analíticos y de negocio |
| Nivel | Fundamental a Intermedio |
| Modalidad | Virtual síncrona |
| Cloud de referencia | Amazon Web Services (AWS) |
| Plataforma principal de práctica | Databricks Free Edition o entorno habilitado por el cliente |
| Enfoque principal | Uso práctico e integral de la plataforma Databricks |

## 2. Propósito del programa

Desarrollar la capacidad de utilizar Databricks como una plataforma integrada
de datos, analítica e inteligencia artificial sobre AWS. Al finalizar, los
participantes podrán identificar qué herramienta utilizar ante una necesidad
concreta, comprender cómo fluye y se gobierna la información, preparar datos,
crear productos analíticos, automatizar procesos y explorar capacidades de IA.

El programa mantiene los fundamentos de Cloud, Lakehouse, Spark y Delta Lake
necesarios para comprender la plataforma, pero no busca especializar al grupo
en programación avanzada con Spark. SQL será la vía principal para análisis;
Python y PySpark se utilizarán cuando aporten valor al procesamiento o permitan
comprender cómo opera Databricks.

## 3. Resultados de aprendizaje

Al finalizar el programa, el participante podrá:

- navegar y organizar recursos en Workspace
- reconocer el propósito de Catalog, Compute, SQL Editor, notebooks, dashboards,
  Jobs, Pipelines, Alerts, Genie, AI/ML y Apps
- elegir entre SQL, Python, PySpark y herramientas visuales según el escenario
- ingerir y preparar datos estructurados y semiestructurados
- explicar y aplicar una arquitectura Medallion simplificada
- crear tablas, vistas, consultas, visualizaciones e indicadores reutilizables
- construir y monitorear un flujo de datos con dependencias
- automatizar una tarea repetitiva de reportería o preparación de datos
- aplicar principios de calidad, trazabilidad, seguridad y mínimo privilegio
- utilizar IA generativa para producir, explicar y validar consultas o código
- consultar datos de negocio con Genie y comprender el alcance de los agentes
- reconocer cuándo conviene un dashboard, una aplicación o un Data Product
- interpretar resultados de un modelo analítico sencillo
- considerar reutilización, costos y buenas prácticas antes de crear nuevos activos

## 4. Enfoque pedagógico

La capacitación mantiene aproximadamente:

- 40% conceptos, arquitectura y criterios de decisión.
- 60% demostraciones, ejercicios y retos aplicados.

Cada tema de plataforma seguirá la secuencia:

```text
Necesidad de negocio
  ↓
Herramienta de Databricks
  ↓
Demostración breve
  ↓
Actividad práctica
  ↓
Resultado verificable
  ↓
Buena práctica de uso
```

La Sesión 1 conserva su contenido actual. Las sesiones 6 y 12 no introducen
contenido nuevo: integran y evalúan lo aprendido. La Sesión 18 reserva sus 120
minutos para elaborar y entregar el caso de uso final.

## 5. Distribución de horas

### Formación

| # | Módulo | Horas |
| ---: | --- | ---: |
| 1 | Fundamentos Cloud, AWS y Arquitectura Moderna de Datos | 4 |
| 2 | Navegación y trabajo en la Plataforma Databricks | 4 |
| 3 | Ingesta y Preparación Visual de Datos | 2 |
| 4 | Lakehouse, Delta Lake y Arquitectura Medallion | 2 |
| 5 | SQL, Python y PySpark aplicados | 2 |
| 6 | Lakeflow Pipelines, Calidad e Ingesta Incremental | 2 |
| 7 | Databricks SQL, Dashboards, Jobs y Alerts | 4 |
| 8 | Unity Catalog, Gobierno y Buenas Prácticas | 4 |
| 9 | Analítica, IA generativa, Genie y Agents | 4 |
| 10 | Databricks Apps, Data Products y Disponibilización | 2 |
|  | **Subtotal de formación** | **30** |

### Consolidación y evaluación

| Actividad | Sesión | Horas | Peso |
| --- | ---: | ---: | ---: |
| Repaso aplicado y Evaluación 1 | 6 | 2 | 30% |
| Repaso aplicado y Evaluación 2 | 12 | 2 | 30% |
| Caso de uso final | 18 | 2 | 40% |
|  |  | **6** | **100%** |

**Total del programa: 36 horas.**

## 6. Plan de sesiones

| Sesión | Módulo | Tema principal | Experiencia predominante |
| ---: | --- | --- | --- |
| 1 | M1 | Fundamentos Cloud y transición On-Premise hacia AWS | Conceptual + guiada |
| 2 | M1 | S3, IAM, Lakehouse y arquitectura moderna | Arquitectura + decisiones |
| 3 | M2 | Tour integral de la plataforma Databricks | Demostración + exploración |
| 4 | M2 | Notebooks, SQL Editor, Compute y trabajo multilenguaje | Práctica guiada |
| 5 | M3 | Data Ingestion, Catalog y Visual Data Prep | Práctica guiada |
| 6 | Evaluación | Repaso aplicado y Evaluación 1 | Reto de plataforma |
| 7 | M4 | Delta Lake y Medallion: Bronze, Silver y Gold | Caso práctico |
| 8 | M5 | SQL, Python y PySpark: cuándo usar cada alternativa | Práctica comparativa |
| 9 | M6 | Lakeflow Pipelines, incremental, calidad y trazabilidad | Construcción de flujo |
| 10 | M7 | Databricks SQL, indicadores y AI/BI Dashboards | Taller analítico |
| 11 | M7 | Jobs, Tasks, programación, monitoreo y Alerts | Automatización práctica |
| 12 | Evaluación | Repaso aplicado y Evaluación 2 | Reto integrado |
| 13 | M8 | Unity Catalog, permisos, seguridad y lineage | Práctica + análisis |
| 14 | M8 | Organización, reutilización, Git y eficiencia de recursos | Taller de buenas prácticas |
| 15 | M9 | Modelos analíticos y MLflow desde la perspectiva del usuario | Demostración + práctica |
| 16 | M9 | Genie Code, Genie Agents y asistentes sobre datos | Práctica de IA |
| 17 | M10 | Databricks Apps, Data Products y preparación final | Demo + diseño aplicado |
| 18 | Evaluación | Elaboración del caso de uso final | Evaluación aplicada |

## 7. Desarrollo de las sesiones y actividades

### Sesión 1 — Fundamentos Cloud y transición On-Premise hacia AWS

El alcance y los materiales de esta sesión se conservan sin modificaciones.

**Temas**

- On-Premise y Cloud.
- IaaS, PaaS y SaaS.
- Elasticidad, escalabilidad y alta disponibilidad.
- Regions y Availability Zones.
- Modelo de responsabilidad compartida.
- Seguridad Cloud introductoria.

**Actividad**

Analizar la modernización de un proceso ficticio de pólizas y siniestros desde
infraestructura On-Premise hacia AWS, identificando responsabilidades, ventajas
y riesgos.

### Sesión 2 — S3, IAM, Lakehouse y arquitectura moderna

**Temas**

- Amazon S3: buckets, objetos, prefijos y zonas de datos.
- IAM, roles, policies y mínimo privilegio.
- Cifrado, KMS, VPC y tagging a nivel conceptual.
- Data Warehouse, Data Lake y Lakehouse.
- Separación entre almacenamiento y procesamiento.
- Ubicación de Databricks dentro de una arquitectura moderna sobre AWS.

**Actividad**

Crear un bucket de entrenamiento con nombre globalmente único, cargar archivos
sintéticos de pólizas, siniestros y pagos mediante `aws s3 cp` y
`aws s3 sync`, y verificar sus object keys. Después, completar la arquitectura
On-Premise → S3 → Databricks → consumo analítico y asignar permisos mínimos a
los perfiles de ingesta, procesamiento, análisis y auditoría.

La práctica se realizará en AWS CloudShell o mediante un perfil AWS CLI con
credenciales temporales. Si el participante no tiene permisos, utilizará un
prefijo aislado de un bucket compartido o una salida simulada.

**Resultado verificable**

Bucket o evidencia simulada con tres objetos organizados, comparación entre
Console, `cp`, `sync` e ingesta automatizada, diagrama de arquitectura y matriz
de permisos mínimos.

### Sesión 3 — Tour integral de la plataforma Databricks

**Temas**

- Data Intelligence Platform.
- Workspace y organización de activos.
- Catalog Explorer.
- Compute y SQL Warehouses.
- SQL Editor y notebooks.
- Data Ingestion y Visual Data Prep.
- AI/BI Dashboards.
- Jobs & Pipelines.
- Alerts.
- Experiments, Models y MLflow.
- Genie Code, Genie Agents y Databricks Apps.

**Actividad**

Realizar una exploración guiada del workspace y completar un mapa
“necesidad → herramienta”. Cada participante deberá localizar los componentes y
seleccionar cuál usaría para consultar datos, preparar información, publicar un
indicador, automatizar una tarea o formular una pregunta de negocio.

**Resultado verificable**

Mapa funcional de la plataforma completado con cinco decisiones justificadas.

### Sesión 4 — Notebooks, SQL Editor, Compute y trabajo multilenguaje

**Temas**

- Creación y organización de notebooks.
- Selección de compute según el trabajo.
- SQL Editor y consultas guardadas.
- Celdas SQL, Python y PySpark.
- Visualizaciones desde resultados.
- Documentación y colaboración.
- Genie Code para generar, explicar y corregir consultas o código.
- Cuándo utilizar notebook, SQL Editor o herramienta visual.

**Actividad**

Explorar una tabla pequeña de pólizas con SQL, reutilizar el resultado desde
Python y revisar una transformación equivalente con PySpark. Utilizar Genie
Code, si está habilitado, para explicar la lógica y proponer una mejora; luego
validar manualmente la respuesta.

**Resultado verificable**

Notebook documentado con una consulta, una transformación sencilla, una
visualización y la explicación de qué lenguaje conviene en cada paso.

### Sesión 5 — Data Ingestion, Catalog y Visual Data Prep

**Temas**

- Carga de archivos CSV, JSON y Excel.
- Creación de tablas desde archivos.
- Navegación y descubrimiento en Catalog Explorer.
- Schema inference y revisión de tipos.
- Visual Data Prep con Lakeflow Designer.
- Operadores visuales de selección, filtro, limpieza y agregación.
- Relación entre transformación visual y código generado.
- Tabla frente a vista y reutilización de activos existentes.

**Actividad principal**

Cargar un archivo sintético de pagos, registrarlo como tabla, identificar su
schema y construir una preparación visual para estandarizar estados, corregir
tipos y calcular un resumen por medio de pago.

**Opción alternativa**

Si Visual Data Prep no está habilitado, realizar la misma preparación mediante
SQL y comparar conceptualmente ambas experiencias.

**Resultado verificable**

Tabla preparada, reglas aplicadas y decisión justificada entre tabla, vista o
salida temporal.

### Sesión 6 — Repaso aplicado y Evaluación 1

No se introduce contenido nuevo.

**Actividad**

Resolver un reto guiado en el que el participante recibe una necesidad de
reportería, identifica las herramientas correctas, localiza o carga un dataset,
explora el Catalog, ejecuta una consulta y presenta una visualización sencilla.

**Conocimientos evaluados**

- fundamentos Cloud, S3 e IAM
- arquitectura Lakehouse
- navegación por Workspace y Catalog
- selección de Compute, SQL Editor o notebook
- ingesta y preparación básica
- elección de la herramienta adecuada

### Sesión 7 — Delta Lake y arquitectura Medallion

**Temas**

- Delta Lake y Transaction Log.
- Beneficios ACID y versionamiento.
- Tablas Managed y External.
- Bronze, Silver y Gold.
- Trazabilidad, reprocesamiento y calidad por capa.
- `INSERT`, `UPDATE`, `DELETE`, `MERGE` y Time Travel a nivel aplicado.
- Preparación de Gold para Analytics y BI.

**Actividad**

Clasificar datasets y transformaciones de pólizas, productos y siniestros en la
capa correspondiente; construir una ruta simplificada Bronze → Silver → Gold y
comprobar un cambio de versión en Delta.

**Resultado verificable**

Tres activos diferenciados por capa y una explicación de qué transformación
pertenece a cada una.

### Sesión 8 — SQL, Python y PySpark aplicados

**Temas**

- SQL para consulta, agregación y análisis.
- Python para lógica complementaria y análisis.
- PySpark para transformación distribuida.
- DataFrames, Transformations, Actions y Lazy Evaluation a nivel fundamental.
- `select`, `filter`, `withColumn`, `groupBy` y joins.
- Combinación de lenguajes dentro de un mismo flujo.
- Criterios de elección: perfil, volumen, complejidad, mantenimiento y consumo.

**Actividad**

Resolver un indicador de siniestros primero con SQL y revisar su equivalente en
PySpark. Utilizar Python para una validación o visualización complementaria y
comparar claridad, reutilización y esfuerzo.

**Resultado verificable**

Una solución funcional y una matriz breve que indique cuándo conviene SQL,
Python, PySpark o una preparación visual.

### Sesión 9 — Lakeflow Pipelines, incremental, calidad y trazabilidad

**Temas**

- ETL y ELT dentro de Databricks.
- Batch, Streaming, Full e Incremental Load.
- Lakeflow Pipelines y editor de pipelines.
- Auto Loader y `COPY INTO` a nivel introductorio.
- Schema evolution, checkpoints e idempotencia.
- Expectations y reglas de calidad.
- Dependencias y flujo de origen a consumo.
- Registros válidos e inválidos.

**Actividad principal**

Construir o completar un pipeline de siniestros que reciba archivos diarios,
aplique una regla de calidad y publique una tabla preparada para análisis.

**Opción alternativa**

Cuando Pipelines no esté disponible, ejecutar notebooks secuencialmente y
representar las dependencias mediante un DAG.

**Resultado verificable**

Pipeline o DAG con fuente, transformación, regla de calidad y salida identificadas.

### Sesión 10 — Databricks SQL, indicadores y AI/BI Dashboards

**Temas**

- SQL Warehouse y SQL Editor.
- Consultas guardadas y vistas.
- Datasets para dashboards.
- Indicadores, visualizaciones y filtros.
- Diseño de AI/BI Dashboards.
- Publicación, permisos y experiencia del consumidor.
- Métricas consistentes y reutilización de tablas Gold.
- Cuándo utilizar consulta, vista, dashboard o exportación.

**Actividad**

Construir un dashboard operativo de siniestros con indicadores de cantidad,
monto pagado, estado y evolución temporal. Agregar filtros útiles para un
supervisor y documentar la fuente Gold utilizada.

**Resultado verificable**

Dashboard con al menos tres indicadores, dos visualizaciones y un filtro de negocio.

### Sesión 11 — Jobs, Tasks, programación, monitoreo y Alerts

**Temas**

- Lakeflow Jobs, Tasks y DAGs.
- Dependencias y parámetros.
- Scheduling y triggers.
- Ejecución de notebooks, pipelines y consultas SQL.
- Retries, repair y rerun.
- Run History y monitoreo.
- Manejo de errores y notificaciones.
- Databricks SQL Alerts para métricas de negocio y calidad.
- Automatización de procesos repetitivos de reportería.

**Actividad principal**

Configurar un Job que actualice una tabla Gold y después ejecute la consulta que
alimenta un reporte. Revisar una falla controlada, identificar la tarea afectada
y definir una alerta para una condición de negocio.

**Opción alternativa**

Si la creación de Jobs o Alerts está restringida, realizar la configuración
como demostración y completar el DAG, la condición y el procedimiento de
recuperación en una plantilla.

**Resultado verificable**

DAG con tareas, dependencia, horario, parámetro, estrategia de error y alerta.

### Sesión 12 — Repaso aplicado y Evaluación 2

No se introduce contenido nuevo.

**Actividad**

Resolver un reto integrado desde una fuente de datos hasta su consumo: elegir
la herramienta de preparación, ubicar cada resultado en Bronze, Silver o Gold,
aplicar una transformación con SQL o PySpark, definir el pipeline, crear un
indicador y proponer su automatización.

**Conocimientos evaluados**

- uso y selección de herramientas de Databricks
- arquitectura Medallion y Delta Lake
- SQL, Python y PySpark a nivel fundamental
- ingesta Full o Incremental
- pipeline, calidad e idempotencia
- dashboard, Job, monitoreo y Alert

### Sesión 13 — Unity Catalog, permisos, seguridad y lineage

**Temas**

- Metastore, Catalog, Schema, Table, View y Volume.
- Descubrimiento y documentación de datos.
- Usuarios, grupos y Service Principals.
- Ownership y permisos.
- `GRANT`, `REVOKE` y mínimo privilegio.
- Lineage y trazabilidad.
- Tags y clasificación.
- Row Filters, Column Masking y ABAC como overview.
- Storage Credentials y External Locations a nivel conceptual.

**Actividad**

Organizar activos de pólizas y siniestros dentro de Catalog y Schema, asignar
permisos mínimos a un Data Engineer, un analista y un supervisor, y observar o
interpretar el lineage desde la tabla Silver hasta el dashboard.

**Resultado verificable**

Matriz de permisos y recorrido de lineage con origen, transformación y consumidor.

### Sesión 14 — Organización, reutilización, Git y eficiencia de recursos

**Temas**

- Cuándo utilizar tabla, vista, notebook, pipeline, consulta o dashboard.
- Reutilización y prevención de duplicidad.
- Naming, folders, dominios y ambientes.
- Separación entre configuración y lógica.
- Parámetros, metadata y logging.
- Git Folders, commits, branches y Pull Requests.
- CI/CD y promoción como overview.
- Bundles, YAML, CLI y Terraform como overview.
- Selección eficiente de compute, costos y FinOps.

**Actividad**

Revisar un workspace desorganizado, detectar duplicidades y proponer una
estructura reutilizable. Refactorizar un notebook para separar configuración y
lógica, registrar el cambio en Git o simular el flujo de revisión.

**Resultado verificable**

Propuesta de organización, activo corregido y checklist de buenas prácticas.

### Sesión 15 — Modelos analíticos y MLflow

**Temas**

- De la pregunta de negocio al modelo analítico.
- Preparación de variables y separación de datos.
- Diferencia entre análisis descriptivo y predictivo.
- Experiments y Runs en MLflow.
- Parámetros, métricas y artefactos.
- Interpretación de resultados y limitaciones.
- AutoML y Model Serving como overview.
- Gobierno de modelos y uso responsable.

**Actividad principal**

Partir de una tabla Gold preparada para analizar pagos tardíos, ejecutar o
revisar un modelo sencillo ya parametrizado y comparar dos Runs en MLflow. El
objetivo será interpretar métricas y limitaciones, no programar un algoritmo
avanzado.

**Opción alternativa**

Si el entrenamiento o MLflow está restringido, analizar capturas y resultados
precalculados manteniendo la toma de decisiones.

**Resultado verificable**

Selección justificada de un Run y explicación de qué decisión permite apoyar.

### Sesión 16 — Genie Code, Genie Agents y asistentes sobre datos

**Temas**

- IA generativa dentro de Databricks.
- Genie Code para SQL, Python, notebooks, pipelines y dashboards.
- Buenas prácticas de prompting y validación humana.
- Riesgos de respuestas incorrectas y control de permisos.
- Genie Agents para preguntas sobre datos de negocio.
- Contexto, instrucciones, términos, ejemplos y datos certificados.
- Consulta conversacional y revisión del SQL generado.
- AI Playground y agentes personalizados como overview.

**Actividad principal**

Utilizar Genie Code para generar o explicar una consulta y validarla contra los
datos. Configurar o explorar un Genie Agent conectado a indicadores Gold de
siniestros, formular preguntas de negocio y revisar la trazabilidad de las
respuestas.

**Opción alternativa**

Si Genie Agents no está habilitado, utilizar una demostración grabada o guiada
y diseñar las instrucciones, preguntas de ejemplo y controles del asistente.

**Resultado verificable**

Consulta validada y ficha de un asistente con propósito, fuentes, usuarios,
preguntas admitidas y límites.

### Sesión 17 — Databricks Apps, Data Products y preparación final

**Temas**

- Databricks Apps y casos de uso empresariales.
- Aplicaciones conectadas a Databricks SQL y Unity Catalog.
- Diferencia entre dashboard, Genie Agent y aplicación.
- Data Product: owner, consumidores, contrato y documentación.
- Freshness, calidad, seguridad, SLA y SLO.
- Views, sharing y disponibilización.
- Data Mesh y ownership por dominio a nivel introductorio.
- Preparación y criterios del caso de uso final.

**Actividad principal**

Explorar o desplegar una aplicación sencilla conectada a datos Gold y definir
un Data Product de indicadores de siniestros. Comparar si la necesidad debe
resolverse con un dashboard, Genie Agent o Databricks App.

**Opción alternativa**

Si Apps no está habilitado, revisar la aplicación como demo y construir su
wireframe, recursos, permisos y flujo de datos.

**Resultado verificable**

Ficha de Data Product y decisión justificada del canal de consumo.

### Sesión 18 — Caso de uso final

Los 120 minutos se destinan íntegramente a elaborar y entregar una solución
integrada para una aseguradora ficticia. Los datasets, plantillas y activos base
estarán disponibles antes de iniciar.

**Actividad**

El participante deberá resolver una necesidad de información operativa y:

- seleccionar las herramientas adecuadas de Databricks
- preparar o reutilizar los datos proporcionados
- aplicar una estructura Medallion simplificada
- crear una tabla o vista Gold verificable
- construir un indicador y su visualización
- proponer la automatización y el monitoreo del flujo
- establecer permisos y buenas prácticas mínimas
- explicar cómo podría consumirse mediante dashboard, Genie Agent o App
- entregar evidencias y decisiones justificadas

No se exige implementar todas las funcionalidades de la plataforma. La
evaluación prioriza la selección correcta de herramientas, la integración del
flujo y la capacidad de conectar el resultado con una necesidad del negocio.

## 8. Estrategia de evaluación

| Evaluación | Fecha | Alcance | Peso |
| --- | --- | --- | ---: |
| Repaso aplicado y Evaluación 1 | 05 de octubre de 2026 | Sesiones 1 a 5 | 30% |
| Repaso aplicado y Evaluación 2 | 28 de octubre de 2026 | Sesiones 1 a 11 | 30% |
| Caso de uso final | 25 de noviembre de 2026 | Integración del programa | 40% |

Las evaluaciones medirán la capacidad de aplicar y seleccionar herramientas,
no la memorización de comandos ni la programación avanzada con Spark.

### Evaluación 1

Comprueba fundamentos Cloud y Lakehouse, navegación en Databricks, uso de
Workspace, Catalog, Compute, SQL Editor, notebooks, ingesta y preparación
básica. No requiere Spark avanzado.

### Evaluación 2

Añade Delta Lake, Medallion, elección entre SQL/Python/PySpark, pipelines,
calidad, dashboards, Jobs, monitoreo y Alerts. No evalúa funcionalidades de IA,
Apps o gobierno presentadas después de la Sesión 12.

### Caso de uso final

Integra plataforma, datos y negocio. El participante debe entregar una solución
acotada y funcional, acompañada por decisiones justificadas de automatización,
gobierno y consumo.

## 9. Matriz de cobertura solicitada por el cliente

| Necesidad | Sesiones principales | Actividad |
| --- | --- | --- |
| Workspace, Catalog y Compute | 3, 4, 5, 13 | Exploración, carga, consulta y organización |
| SQL Editor, SQL, Python y PySpark | 4, 8 | Flujo multilenguaje y comparación práctica |
| Data Ingestion y Visual Data Prep | 5, 9 | Carga, preparación visual y pipeline |
| Delta Lake y Medallion | 7, 9 | Bronze → Silver → Gold |
| Dashboards y Analytics | 10 | Dashboard operativo de siniestros |
| Jobs, Tasks y Pipelines | 9, 11 | Pipeline y automatización de reportería |
| Monitoreo, errores y Alerts | 11 | Falla controlada, recuperación y alerta |
| Gobierno, seguridad y lineage | 13 | Permisos por perfil y trazabilidad |
| Organización, Git y costos | 14 | Revisión y refactorización del workspace |
| Modelos analíticos y MLflow | 15 | Comparación e interpretación de Runs |
| IA generativa y Genie Code | 4, 16 | Generación, explicación y validación |
| Genie Agents y asistentes | 16 | Consulta conversacional sobre tablas Gold |
| Databricks Apps | 17 | Demo o aplicación conectada a datos |
| Data Products y consumo | 17, 18 | Selección de dashboard, agente o App |

## 10. Caso asegurador transversal

Los ejercicios emplearán una aseguradora ficticia y datos 100% sintéticos. No
se asumirán sistemas, arquitectura, datos ni reglas internas de La Positiva.

```text
asegurados
  └── polizas ── productos
         ├── pagos
         └── siniestros ── proveedores
```

El caso evolucionará progresivamente:

```text
Fuente
  ↓
Ingesta y Catalog
  ↓
Bronze → Silver → Gold
  ↓
SQL y Analytics
  ↓
Dashboard y Alert
  ↓
Job y monitoreo
  ↓
Gobierno
  ↓
Genie Agent / App / Data Product
```

## 11. Compatibilidad y alternativas

Las capacidades disponibles pueden variar entre Databricks Free Edition y el
entorno corporativo. Cada práctica dependiente de una función específica tendrá:

```text
Opción A — práctica principal en la funcionalidad prevista
Opción B — alternativa compatible o simulación guiada
Qué cambia en un entorno empresarial
```

Las prácticas se clasificarán como:

- `PRACTICO_FREE`: ejecutable directamente en Free Edition.
- `PRACTICO_CONDICIONAL`: depende de permisos, cuotas o funciones habilitadas.
- `DEMO_INSTRUCTOR`: demostrado por el instructor.
- `CONCEPTUAL`: análisis, diseño o selección de herramienta.

Ninguna evaluación dependerá obligatoriamente del acceso directo a S3, de
permisos administrativos ni de una función no habilitada para el participante.

## 12. Buenas prácticas transversales

Durante todas las actividades se reforzará:

- revisar si el activo ya existe antes de crear uno nuevo
- utilizar tablas Gold y vistas compartidas para evitar duplicidad
- elegir la herramienta más simple que resuelva la necesidad
- documentar propósito, owner, fuente y consumidores
- utilizar nombres claros y organización por dominio
- separar configuración, lógica y presentación
- aplicar mínimo privilegio
- validar resultados generados por IA
- considerar consumo, mantenimiento y costo
- proteger credenciales y datos sensibles

## 13. Requisitos de los participantes

- Conocimientos básicos de datos y reportería.
- Conocimientos básicos de SQL deseables.
- No se requiere experiencia avanzada en programación o Spark.
- Laptop con navegador y acceso a Internet.
- Cuenta Databricks Free Edition o acceso al entorno habilitado.
- Cuenta GitHub para las actividades de versionamiento.

## 14. Entregables del programa

- Presentaciones y guías por sesión.
- Mapa funcional de la plataforma Databricks.
- Ejercicios de navegación, ingesta y preparación visual.
- Notebooks y consultas SQL de ejemplo.
- Pipeline Medallion con reglas de calidad.
- Dashboard e indicador operativo.
- Job, DAG, estrategia de monitoreo y Alert.
- Matriz de permisos y evidencia de lineage.
- Ejercicio de MLflow e interpretación analítica.
- Ficha de Genie Agent o asistente.
- Demo o diseño de Databricks App.
- Ficha de Data Product.
- Dos repasos aplicados y un caso de uso final.
