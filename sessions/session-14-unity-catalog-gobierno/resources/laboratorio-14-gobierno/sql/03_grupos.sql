-- Databricks notebook source
-- MAGIC %md
-- MAGIC # S14-G01 — Acceso mediante un grupo de cuenta
-- MAGIC Guía: GRUPOS.md. No ejecutar todo: detenerse entre etapas para las pruebas.
-- MAGIC Cambia workspace y alumno01 en todas las apariciones.
-- MAGIC Usa el grupo s14_alumno01_analistas del laboratorio principal. Si ya existe, no lo vuelvas a crear.
-- MAGIC Si en tu entorno tiene otro nombre, reemplázalo en todos los GRANT, REVOKE y comprobaciones.
-- MAGIC No se crean grupos mediante GRANT. El propietario administra datos; el administrador de identidades mantiene integrantes.
-- MAGIC Este ejercicio es complementario: para el cierre actual puedes pasar de 01/02 a 04.
-- MAGIC Si usas a Juan en el papel de Ana y lo retiras del grupo, reincorpóralo antes de 04.

-- COMMAND ----------

-- 0. PROPIETARIO: confirmar la fuente existente. No repetir el setup ni el INSERT.
SELECT current_user() AS propietario;
SELECT COUNT(*) AS filas, SUM(monto_pagado) AS monto_pagado_total
FROM workspace.s14_alumno01_gobierno.silver_siniestros;
-- Muestra original: 6 filas / 3000.00 PEN.

-- COMMAND ----------

-- 1. PROPIETARIO: un schema nuevo evita reutilizar concesiones del ejercicio anterior.
-- Si existe, detenerse y elegir otro sufijo; no borrar ni reemplazar objetos.
CREATE SCHEMA workspace.s14_alumno01_grupos
COMMENT 'Ejercicio de grupos de cuenta y acceso a indicadores sinteticos.';

CREATE VIEW workspace.s14_alumno01_grupos.gold_siniestros_resumen AS
SELECT estado_siniestro, COUNT(*) AS cantidad_siniestros,
       SUM(monto_pagado) AS monto_pagado_total
FROM workspace.s14_alumno01_gobierno.silver_siniestros
GROUP BY estado_siniestro;

SHOW GRANTS ON CATALOG workspace;
SHOW GRANTS ON SCHEMA workspace.s14_alumno01_grupos;
SHOW GRANTS ON VIEW workspace.s14_alumno01_grupos.gold_siniestros_resumen;
-- PARAR. Ana está en el grupo, Luis fuera; ninguno debe poder consultar aún.

-- COMMAND ----------

-- 2A. ADMINISTRADOR AUTORIZADO: solo si el grupo necesita USE CATALOG.
-- Si ya lo recibe por otra vía, omite esta celda.
GRANT USE CATALOG ON CATALOG workspace TO `s14_alumno01_analistas`;

-- COMMAND ----------

-- 2B. PROPIETARIO: conceder al grupo, sin concesiones individuales.
GRANT USE SCHEMA ON SCHEMA workspace.s14_alumno01_grupos TO `s14_alumno01_analistas`;
GRANT SELECT ON VIEW workspace.s14_alumno01_grupos.gold_siniestros_resumen TO `s14_alumno01_analistas`;
SHOW GRANTS ON VIEW workspace.s14_alumno01_grupos.gold_siniestros_resumen;
-- PARAR. Ana lee; Luis no. Las consultas de usuario están al final del archivo.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 3. Administrar integrantes desde la interfaz
-- MAGIC Agregar a Luis al grupo. Comprobar membresía y lectura: ambos leen.
-- MAGIC Retirar solo a Ana de Members, conservando cuenta y acceso independiente al workspace.
-- MAGIC Esperar propagación y comprobar: Ana no lee; Luis sí. No ejecutar otro GRANT.
-- MAGIC El propietario conserva esta evidencia de que el permiso del grupo no cambió:

-- COMMAND ----------

SHOW GRANTS ON VIEW workspace.s14_alumno01_grupos.gold_siniestros_resumen;

-- COMMAND ----------

-- 4. PROPIETARIO: retirar la lectura de todo el grupo.
REVOKE SELECT ON VIEW workspace.s14_alumno01_grupos.gold_siniestros_resumen FROM `s14_alumno01_analistas`;
SHOW GRANTS ON VIEW workspace.s14_alumno01_grupos.gold_siniestros_resumen;
-- PARAR. Luis pertenece al grupo pero no lee; Ana tampoco lee.
-- Final: SELECT retirado. No revocar automáticamente USE CATALOG ni borrar identidades.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Consultas para copiar a la sesión de cada analista
-- MAGIC No ejecutarlas como propietario para validar denegaciones. Repetir tras cada etapa.
-- MAGIC Ejecutar cada consulta completa por separado; registrar identidad y mensaje exacto.

-- COMMAND ----------

SELECT current_user() AS usuario,
       is_account_group_member('s14_alumno01_analistas') AS pertenece_al_grupo;

-- COMMAND ----------

SELECT * FROM workspace.s14_alumno01_grupos.gold_siniestros_resumen
ORDER BY estado_siniestro;
-- Cuando existe lectura: ABIERTO 3 / 300.00; CERRADO 3 / 2700.00.
-- Un fallo de cuota, compute o sintaxis no demuestra una revocación.
