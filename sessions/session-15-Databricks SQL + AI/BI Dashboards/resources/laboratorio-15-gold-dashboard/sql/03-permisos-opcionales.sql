-- Databricks notebook source
-- MAGIC %md
-- MAGIC # Continuidad de gobierno — solo con dos identidades en el mismo workspace
-- MAGIC PRACTICO_CONDICIONAL. No es necesario en un Free Edition personal.
-- MAGIC El grupo de la sesion 14 debe existir y contener al analista.
-- MAGIC Si usaste otro principal, sustituye `s14_alumno01_analistas` en todo el archivo.
-- MAGIC No ejecutes todo el archivo con una sola cuenta: cambia de identidad en la ultima etapa.

-- COMMAND ----------

-- CUENTA PRINCIPAL: inspeccionar permisos antes de conceder.
SELECT current_user() AS identidad;
SHOW GRANTS ON CATALOG workspace;
SHOW GRANTS ON SCHEMA workspace.gold_s15_seguros;
SHOW GRANTS ON TABLE workspace.gold_s15_seguros.siniestros_mensuales;
SHOW GRANTS ON VIEW workspace.gold_s15_seguros.vw_siniestros_negocio;

-- COMMAND ----------

-- CUENTA PRINCIPAL: conservar lectura de los objetos de la sesion 14.
-- Estos permisos solo agregan la nueva vista al consumo del analista.
GRANT USE CATALOG ON CATALOG workspace TO `s14_alumno01_analistas`;
GRANT USE SCHEMA ON SCHEMA workspace.gold_s15_seguros TO `s14_alumno01_analistas`;
GRANT SELECT ON VIEW workspace.gold_s15_seguros.vw_siniestros_negocio
TO `s14_alumno01_analistas`;
-- En SQL Warehouses > Permissions: comprobar CAN USE del warehouse existente.
-- No conceder SELECT sobre todo el schema ni MODIFY para construir el dashboard.

-- COMMAND ----------

-- CAMBIAR A LA SESION DEL ANALISTA: ejecutar cada consulta por separado.
SELECT current_user() AS identidad;

SELECT COUNT(*) AS filas, SUM(cantidad_siniestros) AS total_siniestros
FROM workspace.gold_s15_seguros.vw_siniestros_negocio;
-- Esperado: 72 | 2328.

-- COMMAND ----------

-- ANALISTA: prueba independiente. Esperado: sin acceso directo a la tabla.
-- Si devuelve datos, investigar ownership, grupos y privilegios heredados.
SELECT * FROM workspace.gold_s15_seguros.siniestros_mensuales;
-- No usar al propietario para demostrar aislamiento. No revocar permisos generales.
