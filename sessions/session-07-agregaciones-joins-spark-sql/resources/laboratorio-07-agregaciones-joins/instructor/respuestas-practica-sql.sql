-- Respuestas de consultas breves — instructor

USE CATALOG workspace;
USE SCHEMA bronze;

SELECT nombre_producto, cantidad_polizas, prima_total
FROM workspace.bronze.s07_gold_cartera
ORDER BY prima_total DESC;

SELECT canal_venta, COUNT(*) AS cantidad_polizas
FROM workspace.bronze.s07_silver_polizas
GROUP BY canal_venta
ORDER BY canal_venta;

-- El lote 2026-10-07 contiene tres actualizaciones, una poliza nueva y su copia.
-- Bronze conserva 18 registros recibidos; detalle conserva 13 polizas vigentes.
-- El primer lote lo lidera Salud (4,000 PEN); el segundo Auto (4,900 PEN).
