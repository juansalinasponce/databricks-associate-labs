-- 04 — Actualizar indicadores de los productos afectados
-- Ejecutar despues de 03 Las entregas pendientes se detectan automaticamente.
-- Los indicadores describen la cartera vigente, acumulada hasta esta ejecucion.

USE CATALOG workspace;
USE SCHEMA bronze;

-- Paso 1: resumir siniestros ANTES de unirlos con la cartera.
-- Una poliza con dos eventos debe aportar su prima una sola vez.
-- Recalcular las polizas de los productos afectados permite corregir importes
-- y mover un siniestro de una poliza a otra, sin acumular dos veces el pago.
MERGE INTO workspace.bronze.s07_siniestros_por_poliza AS destino
USING (
  SELECT
    p.id_poliza,
    COUNT(s.id_siniestro) AS cantidad_siniestros,
    COUNT(s.id_siniestro) - COUNT(s.monto_pagado) AS siniestros_sin_monto,
    COALESCE(SUM(s.monto_pagado), 0) AS monto_pagado_registrado
  FROM workspace.bronze.s07_silver_polizas AS p
  LEFT JOIN workspace.bronze.s07_silver_siniestros AS s ON p.id_poliza = s.id_poliza
  WHERE p.id_producto IN (
    SELECT id_producto FROM workspace.bronze.s07_productos_afectados
    WHERE id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
  )
  GROUP BY p.id_poliza
) AS origen
ON destino.id_poliza = origen.id_poliza
WHEN MATCHED THEN UPDATE SET
  cantidad_siniestros = origen.cantidad_siniestros,
  siniestros_sin_monto = origen.siniestros_sin_monto,
  monto_pagado_registrado = origen.monto_pagado_registrado
WHEN NOT MATCHED THEN INSERT
  (id_poliza, cantidad_siniestros, siniestros_sin_monto, monto_pagado_registrado)
VALUES
  (origen.id_poliza, origen.cantidad_siniestros, origen.siniestros_sin_monto, origen.monto_pagado_registrado);

-- Paso 2: cargar otra tabla persistente, con una fila por producto.
-- Se reemplazan los indicadores de los productos afectados mediante MERGE.
-- No sumar el total del lote al total previo: una actualizacion no es un alta.
MERGE INTO workspace.bronze.s07_gold_cartera AS destino
USING (
  SELECT
    p.id_producto,
    COALESCE(pr.nombre_producto, 'SIN_CATALOGO') AS nombre_producto,
    COUNT(*) AS cantidad_polizas,
    SUM(CASE WHEN p.estado_poliza = 'ACTIVA' THEN 1 ELSE 0 END) AS polizas_activas,
    COUNT(p.prima) AS primas_informadas,
    SUM(p.prima) AS prima_total,
    ROUND(AVG(p.prima), 2) AS prima_promedio,
    MIN(p.prima) AS prima_minima,
    MAX(p.prima) AS prima_maxima,
    SUM(s.cantidad_siniestros) AS siniestros_reportados,
    SUM(s.siniestros_sin_monto) AS siniestros_sin_monto,
    SUM(s.monto_pagado_registrado) AS monto_pagado_registrado
  FROM workspace.bronze.s07_silver_polizas AS p
  LEFT JOIN workspace.bronze.s07_silver_productos AS pr ON p.id_producto = pr.id_producto
  LEFT JOIN workspace.bronze.s07_siniestros_por_poliza AS s ON p.id_poliza = s.id_poliza
  WHERE p.id_producto IN (
    SELECT id_producto FROM workspace.bronze.s07_productos_afectados
    WHERE id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
  )
  GROUP BY p.id_producto, pr.nombre_producto
) AS origen
ON destino.id_producto = origen.id_producto
WHEN MATCHED THEN UPDATE SET
  nombre_producto = origen.nombre_producto,
  cantidad_polizas = origen.cantidad_polizas,
  polizas_activas = origen.polizas_activas,
  primas_informadas = origen.primas_informadas,
  prima_total = origen.prima_total,
  prima_promedio = origen.prima_promedio,
  prima_minima = origen.prima_minima,
  prima_maxima = origen.prima_maxima,
  siniestros_reportados = origen.siniestros_reportados,
  siniestros_sin_monto = origen.siniestros_sin_monto,
  monto_pagado_registrado = origen.monto_pagado_registrado
WHEN NOT MATCHED THEN INSERT
  (id_producto, nombre_producto, cantidad_polizas, polizas_activas, primas_informadas,
   prima_total, prima_promedio, prima_minima, prima_maxima,
   siniestros_reportados, siniestros_sin_monto, monto_pagado_registrado)
VALUES
  (origen.id_producto, origen.nombre_producto, origen.cantidad_polizas,
   origen.polizas_activas, origen.primas_informadas, origen.prima_total,
   origen.prima_promedio, origen.prima_minima, origen.prima_maxima,
   origen.siniestros_reportados, origen.siniestros_sin_monto, origen.monto_pagado_registrado);

-- Paso 3: si el ultimo contrato de un producto se traslado, quitar su indicador.
-- La eliminacion se limita a productos afectados que ya no tienen cartera.
DELETE FROM workspace.bronze.s07_gold_cartera
WHERE id_producto IN (
  SELECT id_producto FROM workspace.bronze.s07_productos_afectados
  WHERE id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
)
AND NOT EXISTS (
  SELECT 1 FROM workspace.bronze.s07_silver_polizas AS p
  WHERE p.id_producto = s07_gold_cartera.id_producto
);

SELECT * FROM workspace.bronze.s07_gold_cartera ORDER BY id_producto;
