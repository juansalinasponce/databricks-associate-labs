# Sesión 15 — Databricks SQL, AI/BI Dashboards y Genie

Continuación del laboratorio 14: pasar de una vista gobernada a un dashboard
de siniestros con un año de historia sintética.

El participante aprenderá a consultar una vista Gold, validar consultas creadas
con Genie y construir indicadores con filtros. Se reutilizan SQL, tablas Delta,
vistas, Unity Catalog y mínimo privilegio.

## Material para la clase

- [Laboratorio guiado y orden de ejecución](resources/laboratorio-15-gold-dashboard/README.md).
- [SQL para crear y poblar Gold](resources/laboratorio-15-gold-dashboard/sql/00-preparar-gold.sql).
- [SQL para crear la vista](resources/laboratorio-15-gold-dashboard/sql/01-crear-vista.sql).
- [Construcción del dashboard](resources/laboratorio-15-gold-dashboard/DASHBOARD.md).
- [Consultas con Genie](resources/laboratorio-15-gold-dashboard/GENIE.md).
- [Paquete descargable](resources/laboratorio-15-gold-dashboard.zip).

La cuenta principal prepara `workspace.gold_s15_seguros`, una tabla con 72
filas y una vista de negocio. El analista consume esa vista. Si cada participante
usa su propio Free Edition, ejecuta la preparación en su propio workspace.
Los permisos de un workspace no conectan automáticamente cuentas independientes.

## Organización de los 120 minutos

| Bloque | Minutos | Resultado |
| --- | ---: | --- |
| Conceptos y recorrido de la PPT | 35 | Diferenciar tabla, vista, dataset, warehouse y dashboard |
| Preparar Gold y la vista | 20 | 72 filas; enero–diciembre de 2025 |
| Generar y validar SQL con Genie | 15 | Una consulta explicada y contrastada |
| Construir el dashboard | 30 | Indicadores, línea, barras y filtros |
| Publicar y probar Ask Genie si está disponible | 10 | Dashboard publicado o borrador validado |
| Revisión y aplicación al trabajo | 10 | Evidencias y decisión de consumo |

## Relación con la PPT de la sesión 15

Se revisaron las 12 diapositivas de `Sesion15_Databricks SQL + AI_BI Dashboards.pptx`,
incluidas las imágenes que contienen el contenido.

| Diapositiva | Aplicación en el laboratorio |
| --- | --- |
| 3–4 | Del dato gobernado al análisis del negocio |
| 5–7 | SQL Warehouse existente, consulta y dataset |
| 8 | Vista lógica sobre tabla Gold; materialized view como comparación conceptual |
| 9–10 | Genie Code para generar SQL y Ask Genie para consultar el dashboard |
| 11 | Cantidad, estados, montos, porcentaje de cierre, líneas, barras y filtros |
| 12 | Gold → vista → dataset → dashboard → preguntas |

Para aislar la práctica se utiliza `workspace.gold_s15_seguros`, equivalente al
rol de `workspace.gold` en la PPT. No se alteran los objetos de la sesión 14.

Precisiones para explicar: el warehouse es el recurso de cómputo SQL; la vista
guarda una consulta; el dataset define los datos del dashboard. Una vista
consulta los datos vigentes de su fuente, pero un dashboard puede mostrar
resultados en caché hasta su actualización. La actualización de una materialized
view depende de su configuración; no se implementa en esta práctica.

**Ajuste de alcance:** `Docs/cronograma.md` y `Docs/syllabus.md` sitúan modelos
analíticos/MLflow en la sesión 15. Este material sigue la solicitud explícita
del docente y la PPT entregada para esta sesión, continuando el laboratorio 14.
No modifica el cronograma ni las evaluaciones.

Capacidades contrastadas con documentación oficial el **9 de noviembre de
2026**; las fuentes están en las guías. La aplicación de permisos, la ejecución
SQL y la construcción del dashboard deben comprobarse en el workspace.

## Validación técnica para mantener el material

Desde la raíz del repositorio, con PySpark y Java compatibles:

```bash
python3 scripts/validation/validar-sesion-15-sql.py
```

El validador ejecuta la carga, la vista y las ocho consultas con Spark local;
comprueba cobertura del año, KPIs, filtros y repetición de la carga. Usa Parquet
en lugar de Delta y un schema local. No valida Unity Catalog, permisos, Genie
ni la interfaz del dashboard. Los estudiantes ejecutan únicamente SQL en
Databricks; no necesitan instalar estas herramientas locales.
