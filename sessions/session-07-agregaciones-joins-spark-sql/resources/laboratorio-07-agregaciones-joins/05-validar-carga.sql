-- 05 — Validar el resultado y registrar el lote procesado
-- Ejecutar despues de 04. assert_true detiene la tarea cuando un control falla.
-- El control del lote se registra solamente despues de las comprobaciones.

USE CATALOG workspace;
USE SCHEMA bronze;

-- No cerrar una entrega si alguno de sus cambios no llego al detalle.
SELECT assert_true(COUNT(*) = 0, 'Falta aplicar cambios de polizas')
FROM workspace.bronze.s07_bronze_polizas AS b
WHERE b.id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
AND NOT EXISTS (
  SELECT 1 FROM workspace.bronze.s07_silver_polizas AS d
  WHERE d.id_poliza = b.id_poliza
    AND d.fecha_actualizacion >= CAST(b.fecha_actualizacion AS TIMESTAMP)
);

-- No cerrar una entrega si alguno de sus cambios no llego al detalle.
SELECT assert_true(COUNT(*) = 0, 'Falta aplicar cambios de productos')
FROM workspace.bronze.s07_bronze_productos AS b
WHERE b.id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
AND NOT EXISTS (
  SELECT 1 FROM workspace.bronze.s07_silver_productos AS d
  WHERE d.id_producto = b.id_producto
    AND d.fecha_actualizacion >= CAST(b.fecha_actualizacion AS TIMESTAMP)
);

-- No cerrar una entrega si alguno de sus cambios no llego al detalle.
SELECT assert_true(COUNT(*) = 0, 'Falta aplicar cambios de siniestros')
FROM workspace.bronze.s07_bronze_siniestros AS b
WHERE b.id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
AND NOT EXISTS (
  SELECT 1 FROM workspace.bronze.s07_silver_siniestros AS d
  WHERE d.id_siniestro = b.id_siniestro
    AND d.fecha_actualizacion >= CAST(b.fecha_actualizacion AS TIMESTAMP)
);

-- Debe existir exactamente una fila vigente por clave.
SELECT assert_true(COUNT(*) = COUNT(DISTINCT id_poliza), 'Polizas duplicadas en detalle')
FROM workspace.bronze.s07_silver_polizas;

SELECT assert_true(COUNT(*) = COUNT(DISTINCT id_producto), 'Productos duplicados en detalle')
FROM workspace.bronze.s07_silver_productos;

SELECT assert_true(COUNT(*) = COUNT(DISTINCT id_siniestro), 'Siniestros duplicados en detalle')
FROM workspace.bronze.s07_silver_siniestros;

SELECT assert_true(COUNT(*) = COUNT(DISTINCT id_producto), 'Productos duplicados en indicadores')
FROM workspace.bronze.s07_gold_cartera;

SELECT assert_true(COUNT(*) = COUNT(DISTINCT id_poliza), 'Polizas duplicadas en resumen de siniestros')
FROM workspace.bronze.s07_siniestros_por_poliza;

-- Los indicadores deben cuadrar con el detalle vigente, cualquiera sea el lote.
SELECT
  assert_true(c.cantidad_polizas = g.cantidad_polizas, 'Revisar cantidad de polizas'),
  assert_true(c.polizas_activas = g.polizas_activas, 'Revisar polizas activas'),
  assert_true(c.primas_informadas = g.primas_informadas, 'Revisar primas desconocidas'),
  assert_true(c.prima_total = g.prima_total, 'Revisar prima total')
FROM (
  SELECT
    COUNT(*) AS cantidad_polizas,
    SUM(CASE WHEN estado_poliza = 'ACTIVA' THEN 1 ELSE 0 END) AS polizas_activas,
    COUNT(prima) AS primas_informadas,
    COALESCE(SUM(prima), 0) AS prima_total
  FROM workspace.bronze.s07_silver_polizas
) AS c
CROSS JOIN (
  SELECT
    COALESCE(SUM(cantidad_polizas), 0) AS cantidad_polizas,
    COALESCE(SUM(polizas_activas), 0) AS polizas_activas,
    COALESCE(SUM(primas_informadas), 0) AS primas_informadas,
    COALESCE(SUM(prima_total), 0) AS prima_total
  FROM workspace.bronze.s07_gold_cartera
) AS g;

-- Contar solamente siniestros asociados a polizas suministradas.
SELECT
  assert_true(s.cantidad_siniestros = g.cantidad_siniestros, 'Revisar siniestros asociados'),
  assert_true(s.siniestros_sin_monto = g.siniestros_sin_monto, 'Revisar montos desconocidos'),
  assert_true(s.monto_registrado = g.monto_registrado, 'Revisar monto registrado')
FROM (
  SELECT
    COUNT(*) AS cantidad_siniestros,
    COUNT(*) - COUNT(s.monto_pagado) AS siniestros_sin_monto,
    COALESCE(SUM(s.monto_pagado), 0) AS monto_registrado
  FROM workspace.bronze.s07_silver_siniestros AS s
  INNER JOIN workspace.bronze.s07_silver_polizas AS p ON s.id_poliza = p.id_poliza
) AS s
CROSS JOIN (
  SELECT
    COALESCE(SUM(siniestros_reportados), 0) AS cantidad_siniestros,
    COALESCE(SUM(siniestros_sin_monto), 0) AS siniestros_sin_monto,
    COALESCE(SUM(monto_pagado_registrado), 0) AS monto_registrado
  FROM workspace.bronze.s07_gold_cartera
) AS g;

-- Revisar referencias huerfanas por separado; SIN009 / POL999 es intencional.
SELECT s.id_siniestro, s.id_poliza, s.monto_pagado
FROM workspace.bronze.s07_silver_siniestros AS s
LEFT JOIN workspace.bronze.s07_silver_polizas AS p ON s.id_poliza = p.id_poliza
WHERE p.id_poliza IS NULL;

-- Registrar solo entregas pendientes despues de validar el resultado.
-- La fecha de procesamiento proviene del servidor.
MERGE INTO workspace.bronze.s07_control_lotes AS destino
USING (
  SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes
) AS origen
ON destino.id_lote = origen.id_lote
WHEN NOT MATCHED THEN INSERT (id_lote, fecha_proceso)
VALUES (origen.id_lote, CURRENT_TIMESTAMP());

-- El control ya confirma el cierre; liberar la lista de pendientes.
DELETE FROM workspace.bronze.s07_entregas_pendientes
WHERE id_lote IN (SELECT id_lote FROM workspace.bronze.s07_control_lotes);

SELECT * FROM workspace.bronze.s07_control_lotes ORDER BY id_lote;
SELECT * FROM workspace.bronze.s07_entregas_pendientes ORDER BY id_lote;
