-- Databricks notebook source
-- MAGIC %md
-- MAGIC # Cierre — Publicar solo la vista para Power BI
-- MAGIC Ejecuta como propietario/administrador autorizado, por etapas; no recrea ni carga datos.
-- MAGIC Usuario: juan.salinas@atokongo.com. Grupo: s14_alumno01_analistas.
-- MAGIC Vista: workspace.s14_alumno01_gobierno.gold_siniestros_resumen.
-- MAGIC Revisa USUARIO_PRUEBA.md. Los permisos del warehouse se configuran desde su interfaz.
-- MAGIC El alcance de este archivo son los activos del laboratorio; revisa otras vías de acceso.
-- MAGIC No ejecutar las celdas del analista desde la sesión del propietario.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 0. Antes del cierre: confirmar membresía y accesos de Juan
-- MAGIC Si realizaste 03 y retiraste a Juan del grupo, vuelve a agregarlo desde
-- MAGIC Settings → Identity and access → Groups → s14_alumno01_analistas → Members.
-- MAGIC Conserva su acceso al mismo workspace y CAN USE del warehouse. Espera la propagación.
-- MAGIC GRANT concede permisos al grupo, pero no agrega al usuario como integrante.

-- COMMAND ----------

-- 1. INSPECCIÓN: confirmar que la identidad administradora es la original.
SELECT current_user() AS administrador;
SHOW GRANTS ON CATALOG workspace;
SHOW GRANTS ON SCHEMA workspace.s14_alumno01_gobierno;
SHOW GRANTS ON TABLE workspace.s14_alumno01_gobierno.silver_siniestros;
SHOW GRANTS ON VIEW workspace.s14_alumno01_gobierno.gold_siniestros_resumen;
-- PARAR y revisar: SELECT heredado, ALL PRIVILEGES, MANAGE, ownership y otros grupos.
-- Retira cualquier concesión excesiva desde donde se originó antes de validar exclusividad.
-- No cambies permisos de grupos generales como users o account users.

-- COMMAND ----------

-- 2. Retirar lectura/escritura concedidas previamente al grupo en los datos del laboratorio.
REVOKE SELECT, MODIFY ON SCHEMA workspace.s14_alumno01_gobierno FROM `s14_alumno01_analistas`;
REVOKE SELECT, MODIFY ON TABLE workspace.s14_alumno01_gobierno.silver_siniestros FROM `s14_alumno01_analistas`;

-- COMMAND ----------

-- 3. Retirar también concesiones individuales previas sobre esos datos, si existían.
-- Se mantienen el usuario, sus membresías y el acceso al workspace/warehouse.
REVOKE SELECT, MODIFY ON SCHEMA workspace.s14_alumno01_gobierno FROM `juan.salinas@atokongo.com`;
REVOKE SELECT, MODIFY ON TABLE workspace.s14_alumno01_gobierno.silver_siniestros FROM `juan.salinas@atokongo.com`;
REVOKE SELECT ON VIEW workspace.s14_alumno01_gobierno.gold_siniestros_resumen FROM `juan.salinas@atokongo.com`;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Concesiones más amplias o en otros objetos — solo si se encontraron
-- MAGIC Si hubo SELECT sobre el catálogo para el grupo o el usuario, revócalo en ese alcance.
-- MAGIC Si ALL PRIVILEGES u otro grupo sigue aportando acceso, REVOKE SELECT en Silver no basta.
-- MAGIC Si se hizo el ejercicio 03, retira también sus concesiones de lectura al grupo en
-- MAGIC workspace.s14_alumno01_grupos desde Catalog → Permissions, si aún siguen activas.
-- MAGIC Las sentencias siguientes son ejemplos comentados para los alcances inspeccionados.

-- COMMAND ----------

-- REVOKE SELECT, MODIFY ON CATALOG workspace FROM `s14_alumno01_analistas`;
-- REVOKE SELECT, MODIFY ON CATALOG workspace FROM `juan.salinas@atokongo.com`;
-- REVOKE SELECT ON SCHEMA workspace.s14_alumno01_grupos FROM `s14_alumno01_analistas`;
-- REVOKE SELECT ON VIEW workspace.s14_alumno01_grupos.gold_siniestros_resumen FROM `s14_alumno01_analistas`;

-- COMMAND ----------

-- 4A. Conceder uso del catálogo solo si falta y tienes autoridad sobre él.
-- Si el grupo ya tiene USE CATALOG, omite esta celda.
GRANT USE CATALOG ON CATALOG workspace TO `s14_alumno01_analistas`;

-- COMMAND ----------

-- 4B. Publicar únicamente la lectura de la vista a través del grupo.
GRANT USE SCHEMA ON SCHEMA workspace.s14_alumno01_gobierno TO `s14_alumno01_analistas`;
GRANT SELECT ON VIEW workspace.s14_alumno01_gobierno.gold_siniestros_resumen TO `s14_alumno01_analistas`;
SHOW GRANTS ON VIEW workspace.s14_alumno01_gobierno.gold_siniestros_resumen;
-- El owner de la vista mantiene sus permisos sobre Silver.
-- PARAR: abrir la sesión del usuario de prueba y ejecutar las celdas siguientes por separado.

-- COMMAND ----------

-- 5. ANALISTA: ejecutar en la sesión de juan.salinas@atokongo.com, no en la del propietario.
SELECT current_user() AS usuario,
       lower(current_user()) = 'juan.salinas@atokongo.com' AS identidad_esperada,
       is_account_group_member('s14_alumno01_analistas') AS pertenece_al_grupo;

-- COMMAND ----------

SELECT * FROM workspace.s14_alumno01_gobierno.gold_siniestros_resumen
ORDER BY estado_siniestro;
-- Esperado: ABIERTO / 3 / 300.00; CERRADO / 3 / 2700.00.

-- COMMAND ----------

SELECT * FROM workspace.s14_alumno01_gobierno.silver_siniestros;
-- Debe quedar sin acceso. Registrar el mensaje y confirmar existencia como propietario.
-- Si devuelve datos, revisar las vías de acceso antes de pasar a Power BI.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Estado final
-- MAGIC Mantener al usuario en el grupo y conservar SELECT de la vista para Power BI.
-- MAGIC Configurar CAN USE sobre el SQL Warehouse; autenticar Power BI como el analista.
-- MAGIC El laboratorio termina al cargar la vista y verificar los indicadores en Power BI Desktop.
