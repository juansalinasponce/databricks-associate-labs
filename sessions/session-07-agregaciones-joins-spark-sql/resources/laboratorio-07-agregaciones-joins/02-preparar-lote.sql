-- 02 — Limpiar solo los registros del lote recibido
-- Ejecutar las sentencias en orden. Tablas en workspace.bronze.

USE CATALOG workspace;
USE SCHEMA bronze;

-- Bronze conserva duplicados y versiones; las tablas de lote sirven para revisarlos.
-- Cada lote se publica completo y cerrado antes de ejecutar este script.

SELECT id_poliza, COUNT(*) AS filas_recibidas
FROM workspace.bronze.s07_bronze_polizas
WHERE id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
GROUP BY id_poliza
HAVING COUNT(*) > 1;

-- Una fila por clave del lote. El orden elige la actualizacion mas reciente.
-- Los empates de este dataset son copias exactas.
-- NOT EXISTS impide volver a insertar una clave del mismo lote en una reejecucion.
INSERT INTO workspace.bronze.s07_lote_polizas
SELECT
  b.id_lote,
  b.id_poliza,
  b.id_asegurado,
  b.id_producto,
  CAST(b.fecha_inicio AS DATE) AS fecha_inicio,
  CAST(b.fecha_fin AS DATE) AS fecha_fin,
  UPPER(TRIM(b.estado_poliza)) AS estado_poliza,
  CAST(b.prima AS DECIMAL(12,2)) AS prima,
  b.moneda,
  COALESCE(UPPER(TRIM(b.canal_venta)), 'SIN_CANAL') AS canal_venta,
  b.departamento,
  CAST(b.fecha_actualizacion AS TIMESTAMP) AS fecha_actualizacion
FROM workspace.bronze.s07_bronze_polizas AS b
WHERE b.id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
  AND NOT EXISTS (
    SELECT 1 FROM workspace.bronze.s07_lote_polizas AS l
    WHERE l.id_lote = b.id_lote AND l.id_poliza = b.id_poliza
  )
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY b.id_lote, b.id_poliza
  ORDER BY CAST(b.fecha_actualizacion AS TIMESTAMP) DESC
) = 1;

SELECT * FROM workspace.bronze.s07_lote_polizas
WHERE id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
ORDER BY id_poliza;

SELECT id_producto, COUNT(*) AS filas_recibidas
FROM workspace.bronze.s07_bronze_productos
WHERE id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
GROUP BY id_producto
HAVING COUNT(*) > 1;

-- Una fila por clave del lote. El orden elige la actualizacion mas reciente.
-- Los empates de este dataset son copias exactas.
-- NOT EXISTS impide volver a insertar una clave del mismo lote en una reejecucion.
INSERT INTO workspace.bronze.s07_lote_productos
SELECT
  b.id_lote,
  b.id_producto,
  b.nombre_producto,
  b.tipo_seguro,
  b.segmento,
  CAST(b.fecha_actualizacion AS TIMESTAMP) AS fecha_actualizacion
FROM workspace.bronze.s07_bronze_productos AS b
WHERE b.id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
  AND NOT EXISTS (
    SELECT 1 FROM workspace.bronze.s07_lote_productos AS l
    WHERE l.id_lote = b.id_lote AND l.id_producto = b.id_producto
  )
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY b.id_lote, b.id_producto
  ORDER BY CAST(b.fecha_actualizacion AS TIMESTAMP) DESC
) = 1;

SELECT * FROM workspace.bronze.s07_lote_productos
WHERE id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
ORDER BY id_producto;

SELECT id_siniestro, COUNT(*) AS filas_recibidas
FROM workspace.bronze.s07_bronze_siniestros
WHERE id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
GROUP BY id_siniestro
HAVING COUNT(*) > 1;

-- Una fila por clave del lote. El orden elige la actualizacion mas reciente.
-- Los empates de este dataset son copias exactas.
-- NOT EXISTS impide volver a insertar una clave del mismo lote en una reejecucion.
INSERT INTO workspace.bronze.s07_lote_siniestros
SELECT
  b.id_lote,
  b.id_siniestro,
  b.id_poliza,
  CAST(b.fecha_siniestro AS DATE) AS fecha_siniestro,
  CAST(b.fecha_reporte AS DATE) AS fecha_reporte,
  UPPER(TRIM(b.estado_siniestro)) AS estado_siniestro,
  CAST(b.monto_pagado AS DECIMAL(12,2)) AS monto_pagado,
  CAST(b.fecha_actualizacion AS TIMESTAMP) AS fecha_actualizacion
FROM workspace.bronze.s07_bronze_siniestros AS b
WHERE b.id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
  AND NOT EXISTS (
    SELECT 1 FROM workspace.bronze.s07_lote_siniestros AS l
    WHERE l.id_lote = b.id_lote AND l.id_siniestro = b.id_siniestro
  )
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY b.id_lote, b.id_siniestro
  ORDER BY CAST(b.fecha_actualizacion AS TIMESTAMP) DESC
) = 1;

SELECT * FROM workspace.bronze.s07_lote_siniestros
WHERE id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
ORDER BY id_siniestro;
