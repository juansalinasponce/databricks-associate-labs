# Databricks notebook source
# ============================================================
# 00 - CREAR / VALIDAR CARPETA LANDING
# ============================================================
#
# Entorno de referencia observado:
#   Catalog : workspace
#   Schema  : bronze
#   Volume  : s07_archivos
#
# Ruta que utilizará el laboratorio:
#
# /Volumes/workspace/bronze/s07_archivos/landing/
#
# Los dos CSV deben quedar allí:
#   polizas_seguro.csv
#   siniestros_seguro.csv
# ============================================================

# COMMAND ----------
LANDING = "/Volumes/workspace/bronze/s07_archivos/landing"

dbutils.fs.mkdirs(LANDING)

print("Landing listo:", LANDING)

# COMMAND ----------
# Después de cargar los archivos desde la interfaz de Databricks,
# ejecuta esta celda para comprobarlos.

display(dbutils.fs.ls(LANDING))

# Debes observar:
#   polizas_seguro.csv
#   siniestros_seguro.csv
