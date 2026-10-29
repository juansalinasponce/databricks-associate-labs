# Evaluación 2 guiada - Seguros

Proyecto Databricks versionado en Bitbucket.

## Datos

Los datasets NO forman parte del repositorio. Se cargan en:

`/Volumes/workspace/bronze/lapositiva/evaluacion2/`

## Código versionado

- `src/01_bronze_eval2.py`
- `src/02_silver_eval2.py`
- `src/03_gold_pipeline_eval2.sql`
- `src/04_validacion_eval2.py`
- `sql/05_validacion_sql.sql`

## Recursos Databricks versionados como código

- `resources/eval2_pipeline.pipeline.yml`
- `resources/eval2_job.job.yml`
- `databricks.yml`

## Flujo

Volume -> Bronze -> Silver/MERGE -> Gold Pipeline -> Validation

## Bundle

Validar:
`databricks bundle validate -t dev`

Desplegar:
`databricks bundle deploy -t dev`

Ejecutar:
`databricks bundle run -t dev eval2_job`

> El Job y el Pipeline se crean en Databricks a partir de los YAML versionados.
