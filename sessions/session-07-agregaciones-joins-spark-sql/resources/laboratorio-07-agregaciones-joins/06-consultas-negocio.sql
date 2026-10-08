-- 06 — Consultar las tablas de la aseguradora
-- Abrir desde otra consulta en SQL Editor: todas las fuentes son tablas persistentes.
-- Ejecutar primero con el lote 2026-10-06 y comparar despues de 2026-10-07.

USE CATALOG workspace;
USE SCHEMA bronze;

-- Repaso: seleccionar, filtrar y calcular una referencia mensual.
SELECT id_poliza, id_producto, prima, ROUND(prima / 12, 2) AS prima_mensual_referencia
FROM workspace.bronze.s07_silver_polizas
WHERE prima >= 1000
ORDER BY id_poliza;

-- GROUP BY produce una fila por producto; los montos desconocidos no son cero.
-- COUNT(*) cuenta polizas; COUNT(prima) cuenta primas informadas.
SELECT
  id_producto,
  COUNT(*) AS cantidad_polizas,
  COUNT(prima) AS primas_informadas,
  SUM(prima) AS prima_total,
  ROUND(AVG(prima), 2) AS prima_promedio,
  MIN(prima) AS prima_minima,
  MAX(prima) AS prima_maxima,
  COUNT(*) - COUNT(prima) AS primas_faltantes,
  ROUND(SUM(prima) / 12, 2) AS prima_mensual_referencia
FROM workspace.bronze.s07_silver_polizas
GROUP BY id_producto ORDER BY id_producto;

-- INNER conserva coincidencias: 11 filas despues del primer lote.
SELECT p.id_poliza, p.id_producto, pr.nombre_producto
FROM workspace.bronze.s07_silver_polizas AS p
INNER JOIN workspace.bronze.s07_silver_productos AS pr ON p.id_producto = pr.id_producto
ORDER BY p.id_poliza;

-- LEFT conserva la cartera: 12 filas despues del primer lote, incluida P99.
SELECT p.id_poliza, p.id_producto, pr.nombre_producto
FROM workspace.bronze.s07_silver_polizas AS p
LEFT JOIN workspace.bronze.s07_silver_productos AS pr ON p.id_producto = pr.id_producto
ORDER BY p.id_poliza;

-- RIGHT conserva productos: incluye P04; no incluye P99.
SELECT p.id_poliza, pr.id_producto, pr.nombre_producto
FROM workspace.bronze.s07_silver_polizas AS p
RIGHT JOIN workspace.bronze.s07_silver_productos AS pr ON p.id_producto = pr.id_producto
ORDER BY pr.id_producto, p.id_poliza;

-- FULL conserva ambos lados: 13 filas despues del primer lote.
SELECT p.id_poliza, p.id_producto AS producto_poliza,
       pr.id_producto AS producto_catalogo, pr.nombre_producto
FROM workspace.bronze.s07_silver_polizas AS p
FULL OUTER JOIN workspace.bronze.s07_silver_productos AS pr ON p.id_producto = pr.id_producto
ORDER BY p.id_poliza;

-- Columnas duplicadas: calificar cada fecha con su alias y nombrar el resultado.
SELECT p.id_poliza, p.fecha_actualizacion AS fecha_actualizacion_poliza,
       pr.fecha_actualizacion AS fecha_actualizacion_producto
FROM workspace.bronze.s07_silver_polizas AS p
LEFT JOIN workspace.bronze.s07_silver_productos AS pr ON p.id_producto = pr.id_producto
ORDER BY p.id_poliza;

-- Nulos: POL003 no tiene prima informada en el primer lote.
SELECT id_poliza, prima, canal_venta
FROM workspace.bronze.s07_silver_polizas WHERE prima IS NULL;

-- Texto y fechas usadas en reportes.
SELECT id_poliza, LOWER(canal_venta) AS canal_en_minusculas,
       YEAR(fecha_inicio) AS anio_inicio, MONTH(fecha_inicio) AS mes_inicio
FROM workspace.bronze.s07_silver_polizas ORDER BY id_poliza;

SELECT id_siniestro, DATEDIFF(fecha_reporte, fecha_siniestro) AS dias_reporte
FROM workspace.bronze.s07_silver_siniestros ORDER BY id_siniestro;

-- Una Window mantiene el detalle; GROUP BY produce un resumen.
-- Numerar y elegir dos polizas activas por producto, con desempate por id.
SELECT id_producto, id_poliza, prima,
       ROW_NUMBER() OVER (
         PARTITION BY id_producto ORDER BY prima DESC, id_poliza ASC
       ) AS posicion
FROM workspace.bronze.s07_silver_polizas
WHERE estado_poliza = 'ACTIVA' AND prima IS NOT NULL
QUALIFY posicion <= 2
ORDER BY id_producto, posicion;

SELECT * FROM workspace.bronze.s07_gold_cartera ORDER BY id_producto;

-- ## Practica: dos consultas breves
-- 1. Consultar nombre_producto, cantidad_polizas y prima_total desde Gold,
-- ordenando por prima_total descendente. Identificar el producto principal.
-- 2. Contar polizas por canal_venta desde s07_silver_polizas.
-- Explicar por que el segundo lote agrega una poliza, pero cambia varias primas.
-- Explicar por que Bronze puede tener varios registros de la misma clave.
