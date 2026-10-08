-- Solo si ya se crearon las tablas con la version anterior del laboratorio,
-- en la que Bronze no tenia fecha_carga. No ejecutar en una instalacion nueva.
-- Revisar las columnas antes: DESCRIBE TABLE workspace.bronze.s07_bronze_polizas;
-- Ejecutar cada ALTER solamente si fecha_carga no existe en esa tabla.

ALTER TABLE workspace.bronze.s07_bronze_polizas ADD COLUMNS (fecha_carga DATE);
ALTER TABLE workspace.bronze.s07_bronze_productos ADD COLUMNS (fecha_carga DATE);
ALTER TABLE workspace.bronze.s07_bronze_siniestros ADD COLUMNS (fecha_carga DATE);

-- Los registros anteriores no incluyen la fecha real de su ingesta;
-- conservar NULL en ellos. Las nuevas cargas usaran CURRENT_DATE().
-- Despues ejecutar 00 para crear el volumen y la tabla de entregas pendientes.
