-- Databricks notebook source
-- MAGIC %md
-- MAGIC # Preparar los activos de gobierno
-- MAGIC Ejecuta como propietario. Sustituye `workspace` y `alumno01` en todo el archivo.
-- MAGIC Usa un schema nuevo por pareja. Si ya existe, elige otro sufijo: no borres objetos ajenos.
-- MAGIC Ejecutar una sola vez. Si ya completaste el setup, continuar con 01; no repetir el INSERT.
-- MAGIC Dataset sintético; no representa datos ni reglas internas de La Positiva.

-- COMMAND ----------

SELECT current_user() AS identidad, current_catalog() AS catalogo_actual;
SHOW CATALOGS;

-- COMMAND ----------

-- Sin IF NOT EXISTS: una colisión de nombre debe detener la preparación.
CREATE SCHEMA workspace.s14_alumno01_gobierno
COMMENT 'Laboratorio 14. Datos sinteticos de siniestros. Uso formativo.';

-- COMMAND ----------

CREATE TABLE workspace.s14_alumno01_gobierno.silver_siniestros (
  id_siniestro STRING,
  id_poliza STRING,
  numero_documento STRING,
  departamento STRING,
  estado_siniestro STRING,
  monto_pagado DECIMAL(12,2)
) USING DELTA;

INSERT INTO workspace.s14_alumno01_gobierno.silver_siniestros VALUES
  ('SIN001', 'POL001', 'DOC-DEMO-001', 'LIMA',     'CERRADO', 1200.00),
  ('SIN002', 'POL002', 'DOC-DEMO-002', 'AREQUIPA', 'ABIERTO',    0.00),
  ('SIN003', 'POL003', 'DOC-DEMO-003', 'LIMA',     'CERRADO',  800.00),
  ('SIN004', 'POL004', 'DOC-DEMO-004', 'PIURA',    'ABIERTO',  300.00),
  ('SIN005', 'POL005', 'DOC-DEMO-005', 'LIMA',     'ABIERTO',    0.00),
  ('SIN006', 'POL006', 'DOC-DEMO-006', 'AREQUIPA', 'CERRADO',  700.00);

-- COMMAND ----------

-- El resumen permite consumir indicadores sin publicar documentos individuales.
CREATE VIEW workspace.s14_alumno01_gobierno.gold_siniestros_resumen AS
SELECT estado_siniestro,
       COUNT(*) AS cantidad_siniestros,
       SUM(monto_pagado) AS monto_pagado_total
FROM workspace.s14_alumno01_gobierno.silver_siniestros
GROUP BY estado_siniestro;

-- COMMAND ----------

-- Ejecuta la sentencia completa hasta el punto y coma; IS requiere el texto entre comillas.
COMMENT ON TABLE workspace.s14_alumno01_gobierno.silver_siniestros IS 'Siniestros ficticios. Fuente didactica de Gold. Responsable de negocio: Operaciones demo. Documento reservado para practicar minimizacion.';

-- COMMAND ----------

COMMENT ON COLUMN workspace.s14_alumno01_gobierno.silver_siniestros.numero_documento IS 'Identificador ficticio DOC-DEMO; tratar como dato restringido en este ejercicio.';

-- COMMAND ----------

-- COMMENT ON TABLE también se utiliza para comentar una vista en Databricks.
COMMENT ON TABLE workspace.s14_alumno01_gobierno.gold_siniestros_resumen IS 'Indicadores sinteticos por estado, moneda PEN. Owner de negocio: Operaciones demo. Consumidor: Analitica demo. Fuente: silver_siniestros. Actualizacion al consultar la vista.';

-- COMMAND ----------

SELECT COUNT(*) AS filas, SUM(monto_pagado) AS monto_pagado_total
FROM workspace.s14_alumno01_gobierno.silver_siniestros;
-- Esperado: 6 / 3000.00

SELECT * FROM workspace.s14_alumno01_gobierno.gold_siniestros_resumen
ORDER BY estado_siniestro;
-- ABIERTO: 3 / 300.00; CERRADO: 3 / 2700.00

-- COMMAND ----------

DESCRIBE TABLE EXTENDED workspace.s14_alumno01_gobierno.silver_siniestros;
DESCRIBE TABLE EXTENDED workspace.s14_alumno01_gobierno.gold_siniestros_resumen;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Tags opcionales — ejecutar únicamente si están habilitados
-- MAGIC Usa las claves didácticas en Catalog Explorer o descomenta las sentencias.
-- MAGIC Si una clave es gobernada, requiere además ASSIGN; en ese caso usa la ficha de evidencias.
-- MAGIC Un tag descriptivo por sí solo no concede permisos ni aplica una máscara.

-- COMMAND ----------

-- ALTER TABLE workspace.s14_alumno01_gobierno.silver_siniestros
-- SET TAGS ('s14_dominio' = 'siniestros', 's14_clasificacion' = 'restringido_demo');
-- ALTER TABLE workspace.s14_alumno01_gobierno.silver_siniestros
-- ALTER COLUMN numero_documento SET TAGS ('s14_sensible' = 'documento_demo');
