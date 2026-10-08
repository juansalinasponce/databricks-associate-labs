-- 01 — Cargar desde el volumen y detectar entregas pendientes
-- SQL directo: copiar en SQL Editor y ejecutar en orden.
USE CATALOG workspace;
USE SCHEMA bronze;

SELECT CURRENT_DATE() AS fecha_servidor, CURRENT_TIMESTAMP() AS hora_servidor;

-- Cargar archivos nuevos a Bronze y registrar la fecha calculada por el servidor.
COPY INTO workspace.bronze.s07_bronze_polizas
FROM (
  SELECT
    id_lote,
    id_poliza,
    id_asegurado,
    id_producto,
    fecha_inicio,
    fecha_fin,
    estado_poliza,
    prima,
    moneda,
    canal_venta,
    departamento,
    fecha_actualizacion,
    CURRENT_DATE() AS fecha_carga
  FROM '/Volumes/workspace/bronze/s07_archivos/polizas/'
)
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'false', 'nullValue' = '', 'mode' = 'FAILFAST')
COPY_OPTIONS ('force' = 'false', 'mergeSchema' = 'false');

SELECT id_lote, fecha_carga, COUNT(*) AS filas_recibidas
FROM workspace.bronze.s07_bronze_polizas
GROUP BY id_lote, fecha_carga
ORDER BY id_lote;

-- Cargar archivos nuevos a Bronze y registrar la fecha calculada por el servidor.
COPY INTO workspace.bronze.s07_bronze_productos
FROM (
  SELECT
    id_lote,
    id_producto,
    nombre_producto,
    tipo_seguro,
    segmento,
    fecha_actualizacion,
    CURRENT_DATE() AS fecha_carga
  FROM '/Volumes/workspace/bronze/s07_archivos/productos/'
)
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'false', 'nullValue' = '', 'mode' = 'FAILFAST')
COPY_OPTIONS ('force' = 'false', 'mergeSchema' = 'false');

SELECT id_lote, fecha_carga, COUNT(*) AS filas_recibidas
FROM workspace.bronze.s07_bronze_productos
GROUP BY id_lote, fecha_carga
ORDER BY id_lote;

-- Cargar archivos nuevos a Bronze y registrar la fecha calculada por el servidor.
COPY INTO workspace.bronze.s07_bronze_siniestros
FROM (
  SELECT
    id_lote,
    id_siniestro,
    id_poliza,
    fecha_siniestro,
    fecha_reporte,
    estado_siniestro,
    monto_pagado,
    fecha_actualizacion,
    CURRENT_DATE() AS fecha_carga
  FROM '/Volumes/workspace/bronze/s07_archivos/siniestros/'
)
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'false', 'nullValue' = '', 'mode' = 'FAILFAST')
COPY_OPTIONS ('force' = 'false', 'mergeSchema' = 'false');

SELECT id_lote, fecha_carga, COUNT(*) AS filas_recibidas
FROM workspace.bronze.s07_bronze_siniestros
GROUP BY id_lote, fecha_carga
ORDER BY id_lote;

-- El CSV identifica su entrega. No hay fechas ni parametros que ingresar al ejecutar.
-- Conservar pendientes permite recuperar una ejecucion fallida incluso otro dia.
MERGE INTO workspace.bronze.s07_entregas_pendientes AS destino
USING (
  SELECT r.id_lote, MIN(r.fecha_carga) AS fecha_recepcion
  FROM (
    SELECT id_lote, fecha_carga FROM workspace.bronze.s07_bronze_polizas
    UNION ALL
    SELECT id_lote, fecha_carga FROM workspace.bronze.s07_bronze_productos
    UNION ALL
    SELECT id_lote, fecha_carga FROM workspace.bronze.s07_bronze_siniestros
  ) AS r
  WHERE NOT EXISTS (
    SELECT 1 FROM workspace.bronze.s07_control_lotes AS c WHERE c.id_lote = r.id_lote
  )
  GROUP BY r.id_lote
) AS origen
ON destino.id_lote = origen.id_lote
WHEN NOT MATCHED THEN INSERT (id_lote, fecha_recepcion)
VALUES (origen.id_lote, origen.fecha_recepcion);

-- Cada entrega del laboratorio incluye las tres entidades.
SELECT assert_true(COUNT(*) = 0, 'Falta el archivo de polizas de una entrega pendiente')
FROM workspace.bronze.s07_entregas_pendientes AS e
WHERE NOT EXISTS (
  SELECT 1 FROM workspace.bronze.s07_bronze_polizas AS b WHERE b.id_lote = e.id_lote
);

-- Cada entrega del laboratorio incluye las tres entidades.
SELECT assert_true(COUNT(*) = 0, 'Falta el archivo de productos de una entrega pendiente')
FROM workspace.bronze.s07_entregas_pendientes AS e
WHERE NOT EXISTS (
  SELECT 1 FROM workspace.bronze.s07_bronze_productos AS b WHERE b.id_lote = e.id_lote
);

-- Cada entrega del laboratorio incluye las tres entidades.
SELECT assert_true(COUNT(*) = 0, 'Falta el archivo de siniestros de una entrega pendiente')
FROM workspace.bronze.s07_entregas_pendientes AS e
WHERE NOT EXISTS (
  SELECT 1 FROM workspace.bronze.s07_bronze_siniestros AS b WHERE b.id_lote = e.id_lote
);

SELECT * FROM workspace.bronze.s07_entregas_pendientes ORDER BY id_lote;
