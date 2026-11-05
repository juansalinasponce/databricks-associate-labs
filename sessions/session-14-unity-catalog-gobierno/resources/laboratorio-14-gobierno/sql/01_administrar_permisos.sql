-- Databricks notebook source
-- MAGIC %md
-- MAGIC # Administrar permisos por etapas — propietario / instructor
-- MAGIC **No ejecutar todo.** Detente después de cada etapa y espera la prueba del analista.
-- MAGIC Cambia `workspace`, `alumno01` y `s14_alumno01_analistas` en todo el archivo.
-- MAGIC El principal debe existir: grupo de cuenta del laboratorio o usuario del mismo entorno.
-- MAGIC El analista no debe ser propietario, administrador ni recibir permisos amplios por otros grupos.
-- MAGIC No se crean usuarios ni grupos con GRANT. Preparación de identidades: guía del instructor.

-- COMMAND ----------

-- A. INSPECCIONAR. Guardar línea base antes de cualquier GRANT.
SELECT current_user() AS administrador_de_la_practica;
SHOW GRANTS ON CATALOG workspace;
SHOW GRANTS ON SCHEMA workspace.s14_alumno01_gobierno;
SHOW GRANTS ON TABLE workspace.s14_alumno01_gobierno.silver_siniestros;
SHOW GRANTS ON VIEW workspace.s14_alumno01_gobierno.gold_siniestros_resumen;
-- Revisar también membresías del analista. Estos resultados no sustituyen esa revisión.
-- PARAR: el analista prueba las consultas de 02_validar_analista.sql (fase A).

-- COMMAND ----------

-- B1. ACCESO AL CATÁLOGO. Solo si el principal lo necesita y estás autorizado.
-- El propietario de un schema no necesariamente puede concederlo sobre el catálogo.
-- Si ya dispone de USE CATALOG por un grupo, omite esta celda.
GRANT USE CATALOG ON CATALOG workspace TO `s14_alumno01_analistas`;

-- COMMAND ----------

-- B2. LECTURA MÍNIMA: acceder al schema y consultar únicamente la vista.
GRANT USE SCHEMA ON SCHEMA workspace.s14_alumno01_gobierno
TO `s14_alumno01_analistas`;
GRANT SELECT ON VIEW workspace.s14_alumno01_gobierno.gold_siniestros_resumen
TO `s14_alumno01_analistas`;
SHOW GRANTS ON VIEW workspace.s14_alumno01_gobierno.gold_siniestros_resumen;
-- PARAR: el analista prueba fase B. Vista: 2 filas; tabla y UPDATE: denegados.

-- COMMAND ----------

-- C. REVOCAR solo la lectura de la vista; conservar uso de los padres.
REVOKE SELECT ON VIEW workspace.s14_alumno01_gobierno.gold_siniestros_resumen
FROM `s14_alumno01_analistas`;
SHOW GRANTS ON VIEW workspace.s14_alumno01_gobierno.gold_siniestros_resumen;
-- PARAR: el analista vuelve a consultar la vista (fase C): debe fallar por acceso.

-- COMMAND ----------

-- D. HERENCIA CONTROLADA: únicamente en este schema aislado con datos ficticios.
-- SELECT en el schema cubre sus tablas/vistas actuales y futuras.
GRANT SELECT ON SCHEMA workspace.s14_alumno01_gobierno
TO `s14_alumno01_analistas`;
-- Añadimos también un permiso directo para comparar ambas procedencias.
GRANT SELECT ON TABLE workspace.s14_alumno01_gobierno.silver_siniestros
TO `s14_alumno01_analistas`;
-- PARAR: analista fase D. Tabla: 6 filas; vista: 2 filas. UPDATE sigue denegado.

-- COMMAND ----------

-- E. QUITAR EL DIRECTO. El permiso heredado del schema continúa vigente.
REVOKE SELECT ON TABLE workspace.s14_alumno01_gobierno.silver_siniestros
FROM `s14_alumno01_analistas`;
SHOW GRANTS ON SCHEMA workspace.s14_alumno01_gobierno;
SHOW GRANTS ON TABLE workspace.s14_alumno01_gobierno.silver_siniestros;
-- PARAR: analista fase E. Tabla y vista aún se leen por herencia.

-- COMMAND ----------

-- F. QUITAR LA FUENTE DE LA HERENCIA.
REVOKE SELECT ON SCHEMA workspace.s14_alumno01_gobierno
FROM `s14_alumno01_analistas`;
SHOW GRANTS ON SCHEMA workspace.s14_alumno01_gobierno;
-- PARAR: analista fase F. Tabla y vista deben fallar si no hay otra vía de acceso.

-- COMMAND ----------

-- G. ESTADO FINAL: restaurar únicamente el consumo autorizado de Gold.
GRANT SELECT ON VIEW workspace.s14_alumno01_gobierno.gold_siniestros_resumen
TO `s14_alumno01_analistas`;
SHOW GRANTS ON VIEW workspace.s14_alumno01_gobierno.gold_siniestros_resumen;
-- PARAR: analista fase G. Vista sí; tabla y escritura no.
-- Aplicación diaria: retirar acceso temporal y conservar solo el producto acordado.
