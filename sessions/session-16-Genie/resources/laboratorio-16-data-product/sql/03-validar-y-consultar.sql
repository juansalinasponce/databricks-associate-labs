-- Databricks notebook source
-- Controles del archivo de referencia sin editar. Datos sintéticos, año 2025.
-- Q1: tablas de referencia y grano de consumo.
SELECT 'matricula' AS objeto, COUNT(*) AS filas FROM workspace.s16.matricula
UNION ALL SELECT 'ambientes', COUNT(*) FROM workspace.s16.ambientes
UNION ALL SELECT 'proceso', COUNT(*) FROM workspace.s16.proceso
UNION ALL SELECT 'dim_fecha', COUNT(*) FROM workspace.s16.dim_fecha
UNION ALL SELECT 'dim_producto', COUNT(*) FROM workspace.s16.dim_producto
UNION ALL SELECT 'dim_canal', COUNT(*) FROM workspace.s16.dim_canal
UNION ALL SELECT 'dim_estado', COUNT(*) FROM workspace.s16.dim_estado
UNION ALL SELECT 'fact_polizas', COUNT(*) FROM workspace.s16.fact_polizas
UNION ALL SELECT 'fact_siniestros', COUNT(*) FROM workspace.s16.fact_siniestros
UNION ALL SELECT 'vw_indicadores', COUNT(*) FROM workspace.s16.vw_indicadores;

-- COMMAND ----------

-- Q2: matrícula única y cuatro referencias; no son cuatro Data Products.
SELECT m.codigo_dp, m.nombre, m.version_contrato, a.ambiente,
       a.catalogo, a.esquema, a.habilitado
FROM workspace.s16.matricula m
JOIN workspace.s16.ambientes a ON m.codigo_dp = a.codigo_dp
ORDER BY a.ambiente;

-- COMMAND ----------

-- Q3: KPIs del dashboard sin filtros.
SELECT SUM(cantidad_polizas_emitidas) AS polizas_emitidas,
       SUM(prima_emitida) AS prima_emitida_pen,
       SUM(cantidad_siniestros) AS siniestros,
       SUM(cantidad_cerrados) AS cerrados,
       SUM(monto_pagado) AS pagado_pen,
       SUM(monto_reservado) AS reservado_pen,
       ROUND(100.0 * SUM(cantidad_cerrados) / NULLIF(SUM(cantidad_siniestros), 0), 2) AS porcentaje_cierre
FROM workspace.s16.vw_indicadores;

-- COMMAND ----------

-- Q4: suma de siniestros por tipo, con relación hecho-dimensión explícita.
SELECT p.tipo_seguro, SUM(f.cantidad_siniestros) AS siniestros,
       SUM(f.monto_pagado) AS pagado_pen
FROM workspace.s16.fact_siniestros f
JOIN workspace.s16.dim_producto p ON f.id_producto = p.id_producto
GROUP BY p.tipo_seguro ORDER BY pagado_pen DESC;

-- COMMAND ----------

-- Q5: pregunta temporal reproducible; no CURRENT_DATE().
SELECT mes_referencia, SUM(cantidad_siniestros) AS siniestros
FROM workspace.s16.vw_indicadores
GROUP BY mes_referencia ORDER BY mes_referencia;

-- COMMAND ----------

-- Q6: filtro de comprobación del dashboard y de Genie.
SELECT SUM(cantidad_polizas_emitidas) AS polizas_emitidas,
       SUM(prima_emitida) AS prima_emitida_pen,
       SUM(cantidad_siniestros) AS siniestros,
       SUM(monto_pagado) AS pagado_pen,
       ROUND(100.0 * SUM(cantidad_cerrados) / NULLIF(SUM(cantidad_siniestros), 0), 2) AS porcentaje_cierre
FROM workspace.s16.vw_indicadores
WHERE mes_referencia = DATE '2025-01-01' AND tipo_seguro = 'AUTO' AND canal = 'DIRECTO';

-- COMMAND ----------

-- Q7: estados al corte; no representa cierres ocurridos en cada mes.
SELECT estado_siniestro, SUM(cantidad_siniestros) AS siniestros
FROM workspace.s16.vw_siniestros
GROUP BY estado_siniestro ORDER BY estado_siniestro;

-- COMMAND ----------

-- Q8: integridad de las siete relaciones. Todos los resultados deben ser 0.
SELECT 'polizas_fecha' AS relacion, COUNT(*) AS huerfanas
FROM workspace.s16.fact_polizas f LEFT ANTI JOIN workspace.s16.dim_fecha d ON f.id_fecha = d.id_fecha
UNION ALL SELECT 'polizas_producto', COUNT(*)
FROM workspace.s16.fact_polizas f LEFT ANTI JOIN workspace.s16.dim_producto d ON f.id_producto = d.id_producto
UNION ALL SELECT 'polizas_canal', COUNT(*)
FROM workspace.s16.fact_polizas f LEFT ANTI JOIN workspace.s16.dim_canal d ON f.id_canal = d.id_canal
UNION ALL SELECT 'siniestros_fecha', COUNT(*)
FROM workspace.s16.fact_siniestros f LEFT ANTI JOIN workspace.s16.dim_fecha d ON f.id_fecha = d.id_fecha
UNION ALL SELECT 'siniestros_producto', COUNT(*)
FROM workspace.s16.fact_siniestros f LEFT ANTI JOIN workspace.s16.dim_producto d ON f.id_producto = d.id_producto
UNION ALL SELECT 'siniestros_canal', COUNT(*)
FROM workspace.s16.fact_siniestros f LEFT ANTI JOIN workspace.s16.dim_canal d ON f.id_canal = d.id_canal
UNION ALL SELECT 'siniestros_estado', COUNT(*)
FROM workspace.s16.fact_siniestros f LEFT ANTI JOIN workspace.s16.dim_estado d ON f.id_estado = d.id_estado;

-- COMMAND ----------

-- Q9: el grano de la vista debe ser único. Esperado: ninguna fila.
SELECT id_fecha, id_producto, id_canal, COUNT(*) AS repeticiones
FROM workspace.s16.vw_indicadores
GROUP BY id_fecha, id_producto, id_canal HAVING COUNT(*) > 1;

-- COMMAND ----------

-- Q10: comparar los hechos originales con la vista de consumo. Diferencias = 0.
SELECT
 (SELECT SUM(prima_emitida) FROM workspace.s16.fact_polizas)
   - (SELECT SUM(prima_emitida) FROM workspace.s16.vw_indicadores) AS diferencia_prima,
 (SELECT SUM(cantidad_polizas_emitidas) FROM workspace.s16.fact_polizas)
   - (SELECT SUM(cantidad_polizas_emitidas) FROM workspace.s16.vw_indicadores) AS diferencia_polizas,
 (SELECT SUM(monto_pagado) FROM workspace.s16.fact_siniestros)
   - (SELECT SUM(monto_pagado) FROM workspace.s16.vw_indicadores) AS diferencia_pagado,
 (SELECT SUM(cantidad_siniestros) FROM workspace.s16.fact_siniestros)
   - (SELECT SUM(cantidad_siniestros) FROM workspace.s16.vw_indicadores) AS diferencia_siniestros;
