-- Databricks notebook source
-- DP-SEG-016 | DEV. Ejecutar después de 00 y 01.
-- Son vistas lógicas sobre los datos del Excel, sin otra copia física.

CREATE OR REPLACE VIEW workspace.s16.vw_siniestros
COMMENT 'Grano: mes de reporte + producto + canal + estado al corte 2025-12-31. SUM de cantidades, no COUNT de filas.'
AS
SELECT 'DP-SEG-016' AS codigo_dp, 'DEV' AS ambiente,
       f.id_hecho_siniestro, d.mes_referencia AS mes_reporte,
       p.nombre_producto, p.tipo_seguro, c.canal, e.estado_siniestro,
       f.cantidad_siniestros, f.monto_pagado, f.monto_reservado,
       CASE WHEN e.estado_siniestro = 'CERRADO' THEN f.cantidad_siniestros ELSE 0 END AS cantidad_cerrados,
       f.fecha_corte, f.moneda
FROM workspace.s16.fact_siniestros f
JOIN workspace.s16.dim_fecha d ON f.id_fecha = d.id_fecha
JOIN workspace.s16.dim_producto p ON f.id_producto = p.id_producto
JOIN workspace.s16.dim_canal c ON f.id_canal = c.id_canal
JOIN workspace.s16.dim_estado e ON f.id_estado = e.id_estado;

-- COMMAND ----------

CREATE OR REPLACE VIEW workspace.s16.vw_polizas
COMMENT 'Grano: mes de emisión + producto + canal. Emisiones de 2025; no pólizas vigentes ni exposición.'
AS
SELECT 'DP-SEG-016' AS codigo_dp, 'DEV' AS ambiente,
       f.id_hecho_poliza, d.mes_referencia AS mes_emision,
       p.nombre_producto, p.tipo_seguro, c.canal,
       f.cantidad_polizas_emitidas, f.prima_emitida, f.moneda
FROM workspace.s16.fact_polizas f
JOIN workspace.s16.dim_fecha d ON f.id_fecha = d.id_fecha
JOIN workspace.s16.dim_producto p ON f.id_producto = p.id_producto
JOIN workspace.s16.dim_canal c ON f.id_canal = c.id_canal;

-- COMMAND ----------

-- Agregar cada hecho ANTES de unirlos: los estados multiplicarían la prima.
-- El FULL OUTER conserva grupos que solo existan en uno de los hechos.
CREATE OR REPLACE VIEW workspace.s16.vw_indicadores
COMMENT 'Mes de referencia + producto + canal. Compara emisiones y reportes del mes, sin vincular siniestros a pólizas individuales. Corte fijo 2025-12-31. Fuente recomendada para dashboard y preguntas combinadas.'
AS
WITH polizas AS (
  SELECT id_fecha, id_producto, id_canal,
         SUM(cantidad_polizas_emitidas) AS cantidad_polizas_emitidas,
         SUM(prima_emitida) AS prima_emitida
  FROM workspace.s16.fact_polizas
  GROUP BY id_fecha, id_producto, id_canal
), siniestros AS (
  SELECT f.id_fecha, f.id_producto, f.id_canal,
         SUM(f.cantidad_siniestros) AS cantidad_siniestros,
         SUM(CASE WHEN e.estado_siniestro = 'CERRADO' THEN f.cantidad_siniestros ELSE 0 END) AS cantidad_cerrados,
         SUM(f.monto_pagado) AS monto_pagado,
         SUM(f.monto_reservado) AS monto_reservado
  FROM workspace.s16.fact_siniestros f
  JOIN workspace.s16.dim_estado e ON f.id_estado = e.id_estado
  GROUP BY f.id_fecha, f.id_producto, f.id_canal
)
SELECT 'DP-SEG-016' AS codigo_dp, 'DEV' AS ambiente,
       COALESCE(p.id_fecha, s.id_fecha) AS id_fecha,
       COALESCE(p.id_producto, s.id_producto) AS id_producto,
       COALESCE(p.id_canal, s.id_canal) AS id_canal,
       d.mes_referencia, r.nombre_producto, r.tipo_seguro, c.canal,
       COALESCE(p.cantidad_polizas_emitidas, 0) AS cantidad_polizas_emitidas,
       COALESCE(p.prima_emitida, 0) AS prima_emitida,
       COALESCE(s.cantidad_siniestros, 0) AS cantidad_siniestros,
       COALESCE(s.cantidad_cerrados, 0) AS cantidad_cerrados,
       COALESCE(s.monto_pagado, 0) AS monto_pagado,
       COALESCE(s.monto_reservado, 0) AS monto_reservado,
       DATE '2025-12-31' AS fecha_corte, 'PEN' AS moneda
FROM polizas p
FULL OUTER JOIN siniestros s
  ON p.id_fecha = s.id_fecha AND p.id_producto = s.id_producto AND p.id_canal = s.id_canal
JOIN workspace.s16.dim_fecha d ON d.id_fecha = COALESCE(p.id_fecha, s.id_fecha)
JOIN workspace.s16.dim_producto r ON r.id_producto = COALESCE(p.id_producto, s.id_producto)
JOIN workspace.s16.dim_canal c ON c.id_canal = COALESCE(p.id_canal, s.id_canal);
