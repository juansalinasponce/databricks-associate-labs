-- ============================================================
-- EVALUACIÓN 2 GUIADA - VALIDACIÓN EN SQL EDITOR
-- ============================================================

-- 1. Cantidad final de siniestros Silver.
SELECT COUNT(*) AS cantidad_silver
FROM workspace.silver.eval2_siniestros;

-- 2. Debe devolver cero filas.
SELECT id_siniestro, COUNT(*) AS cantidad
FROM workspace.silver.eval2_siniestros
GROUP BY id_siniestro
HAVING COUNT(*) > 1;

-- 3. Verificar schema evolution.
SELECT
    id_siniestro,
    prioridad,
    estado_siniestro,
    fecha_actualizacion
FROM workspace.silver.eval2_siniestros
WHERE prioridad IS NOT NULL
ORDER BY fecha_actualizacion DESC;

-- 4. Gold.
SELECT *
FROM workspace.gold.eval2_resumen_siniestros
ORDER BY reserva_total DESC;

-- 5. Detalle de siniestros y pagos.
SELECT
    s.id_siniestro,
    s.tipo_siniestro,
    s.estado_siniestro,
    p.id_pago,
    p.estado_pago,
    p.monto_pago
FROM workspace.silver.eval2_siniestros s
LEFT JOIN workspace.silver.eval2_pagos p
    ON s.id_siniestro = p.id_siniestro
ORDER BY s.id_siniestro, p.fecha_pago;
