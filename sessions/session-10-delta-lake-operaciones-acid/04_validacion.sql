-- ============================================================
-- 04 - VALIDACIÓN DEL LABORATORIO MEDALLION
-- ============================================================


-- ============================================================
-- 1. BRONZE
-- ============================================================

SELECT COUNT(*) AS registros
FROM workspace.bronze.polizas_medallion;

SELECT COUNT(*) AS registros
FROM workspace.bronze.siniestros_medallion;


-- Ver las versiones recibidas.
SELECT
    id_poliza,
    estado_poliza,
    plan,
    prima_mensual,
    fecha_actualizacion
FROM workspace.bronze.polizas_medallion
ORDER BY id_poliza, fecha_actualizacion;


-- ============================================================
-- 2. SILVER SCD TYPE 2
-- ============================================================

-- Historial de pólizas.
SELECT
    id_poliza,
    plan,
    prima_mensual,
    estado_poliza,
    fecha_inicio_vigencia,
    fecha_fin_vigencia,
    es_actual
FROM workspace.silver.polizas_scd2
ORDER BY id_poliza, fecha_inicio_vigencia;


-- Mostrar únicamente versiones actuales.
SELECT *
FROM workspace.silver.polizas_scd2
WHERE es_actual = true
ORDER BY id_poliza;


-- Historial de un siniestro.
SELECT
    id_siniestro,
    estado_siniestro,
    monto_reserva,
    monto_pagado,
    fecha_inicio_vigencia,
    fecha_fin_vigencia,
    es_actual
FROM workspace.silver.siniestros_scd2
WHERE id_siniestro = 'SIN-0001'
ORDER BY fecha_inicio_vigencia;


-- Validar que solo exista una versión actual por póliza.
SELECT
    id_poliza,
    COUNT(*) AS versiones_actuales
FROM workspace.silver.polizas_scd2
WHERE es_actual = true
GROUP BY id_poliza
HAVING COUNT(*) <> 1;


-- Debe devolver 0 filas.


-- ============================================================
-- 3. GOLD
-- ============================================================

SELECT COUNT(*) FROM workspace.gold.dim_asegurado;
SELECT COUNT(*) FROM workspace.gold.dim_producto;
SELECT COUNT(*) FROM workspace.gold.dim_poliza;
SELECT COUNT(*) FROM workspace.gold.dim_tiempo;
SELECT COUNT(*) FROM workspace.gold.fact_poliza;
SELECT COUNT(*) FROM workspace.gold.fact_siniestro;


-- ============================================================
-- 4. CONSULTA ESTRELLA
-- ============================================================

SELECT
    a.nombre_asegurado,
    a.departamento,
    pr.producto,
    pr.plan,
    dp.id_poliza,
    f.id_siniestro,
    f.tipo_siniestro,
    f.estado_siniestro,
    f.monto_reserva,
    f.monto_pagado,
    f.dias_reporte
FROM workspace.gold.fact_siniestro f
LEFT JOIN workspace.gold.dim_poliza dp
    ON f.sk_poliza = dp.sk_poliza
LEFT JOIN workspace.gold.dim_asegurado a
    ON f.sk_asegurado = a.sk_asegurado
LEFT JOIN workspace.gold.dim_producto pr
    ON f.sk_producto = pr.sk_producto
ORDER BY
    a.nombre_asegurado,
    f.id_siniestro;


-- ============================================================
-- 5. MÉTRICAS DE NEGOCIO
-- ============================================================

SELECT
    pr.producto,
    f.tipo_siniestro,
    COUNT(*) AS cantidad_siniestros,
    ROUND(SUM(f.monto_reserva), 2) AS monto_reserva,
    ROUND(SUM(f.monto_pagado), 2) AS monto_pagado
FROM workspace.gold.fact_siniestro f
LEFT JOIN workspace.gold.dim_producto pr
    ON f.sk_producto = pr.sk_producto
GROUP BY
    pr.producto,
    f.tipo_siniestro
ORDER BY monto_reserva DESC;


-- ============================================================
-- 6. UBICACIÓN FÍSICA DELTA
-- ============================================================
--
-- Permite observar dónde se almacena físicamente cada tabla.

DESCRIBE DETAIL workspace.bronze.polizas_medallion;
DESCRIBE DETAIL workspace.silver.polizas_scd2;
DESCRIBE DETAIL workspace.gold.fact_siniestro;
