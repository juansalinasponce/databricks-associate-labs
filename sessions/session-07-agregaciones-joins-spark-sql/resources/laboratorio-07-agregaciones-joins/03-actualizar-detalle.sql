-- 03 — Aplicar altas y cambios a las tablas de detalle
-- Ejecutar las sentencias en orden. Tablas en workspace.bronze.

USE CATALOG workspace;
USE SCHEMA bronze;

-- Si una poliza cambia de producto, deben actualizarse ambos productos.
-- Tambien conservamos el producto anterior de un siniestro que cambia de poliza.
MERGE INTO workspace.bronze.s07_productos_afectados AS destino
USING (
  SELECT id_lote, id_producto FROM workspace.bronze.s07_lote_polizas WHERE id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
  UNION
  SELECT l.id_lote, p.id_producto
  FROM workspace.bronze.s07_lote_polizas AS l
  INNER JOIN workspace.bronze.s07_silver_polizas AS p ON l.id_poliza = p.id_poliza
  WHERE l.id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
  UNION
  SELECT id_lote, id_producto FROM workspace.bronze.s07_lote_productos WHERE id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
  UNION
  SELECT l.id_lote, p.id_producto
  FROM workspace.bronze.s07_lote_siniestros AS l
  INNER JOIN workspace.bronze.s07_silver_siniestros AS s ON l.id_siniestro = s.id_siniestro
  INNER JOIN workspace.bronze.s07_silver_polizas AS p ON s.id_poliza = p.id_poliza
  WHERE l.id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
) AS origen
ON destino.id_lote = origen.id_lote AND destino.id_producto = origen.id_producto
WHEN NOT MATCHED THEN INSERT (
  id_lote, id_producto
)
VALUES (
  origen.id_lote, origen.id_producto
);

-- Si hay varias entregas pendientes, se elige una version por clave.
-- MERGE compara la clave: actualiza una version mas reciente o agrega una nueva.
-- Un lote repetido o antiguo no reemplaza una version vigente mas reciente.
MERGE INTO workspace.bronze.s07_silver_polizas AS destino
USING (
  SELECT * FROM workspace.bronze.s07_lote_polizas WHERE id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
  QUALIFY ROW_NUMBER() OVER (
    PARTITION BY id_poliza ORDER BY fecha_actualizacion DESC, id_lote DESC
  ) = 1
) AS origen
ON destino.id_poliza = origen.id_poliza
WHEN MATCHED AND origen.fecha_actualizacion > destino.fecha_actualizacion THEN UPDATE SET
  id_lote = origen.id_lote,
  id_asegurado = origen.id_asegurado,
  id_producto = origen.id_producto,
  fecha_inicio = origen.fecha_inicio,
  fecha_fin = origen.fecha_fin,
  estado_poliza = origen.estado_poliza,
  prima = origen.prima,
  moneda = origen.moneda,
  canal_venta = origen.canal_venta,
  departamento = origen.departamento,
  fecha_actualizacion = origen.fecha_actualizacion
WHEN NOT MATCHED THEN INSERT (
  id_lote, id_poliza, id_asegurado,
  id_producto, fecha_inicio, fecha_fin,
  estado_poliza, prima, moneda,
  canal_venta, departamento, fecha_actualizacion
)
VALUES (
  origen.id_lote, origen.id_poliza, origen.id_asegurado,
  origen.id_producto, origen.fecha_inicio, origen.fecha_fin,
  origen.estado_poliza, origen.prima, origen.moneda,
  origen.canal_venta, origen.departamento, origen.fecha_actualizacion
);

-- Si hay varias entregas pendientes, se elige una version por clave.
-- MERGE compara la clave: actualiza una version mas reciente o agrega una nueva.
-- Un lote repetido o antiguo no reemplaza una version vigente mas reciente.
MERGE INTO workspace.bronze.s07_silver_productos AS destino
USING (
  SELECT * FROM workspace.bronze.s07_lote_productos WHERE id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
  QUALIFY ROW_NUMBER() OVER (
    PARTITION BY id_producto ORDER BY fecha_actualizacion DESC, id_lote DESC
  ) = 1
) AS origen
ON destino.id_producto = origen.id_producto
WHEN MATCHED AND origen.fecha_actualizacion > destino.fecha_actualizacion THEN UPDATE SET
  id_lote = origen.id_lote,
  nombre_producto = origen.nombre_producto,
  tipo_seguro = origen.tipo_seguro,
  segmento = origen.segmento,
  fecha_actualizacion = origen.fecha_actualizacion
WHEN NOT MATCHED THEN INSERT (
  id_lote, id_producto, nombre_producto,
  tipo_seguro, segmento, fecha_actualizacion
)
VALUES (
  origen.id_lote, origen.id_producto, origen.nombre_producto,
  origen.tipo_seguro, origen.segmento, origen.fecha_actualizacion
);

-- Si hay varias entregas pendientes, se elige una version por clave.
-- MERGE compara la clave: actualiza una version mas reciente o agrega una nueva.
-- Un lote repetido o antiguo no reemplaza una version vigente mas reciente.
MERGE INTO workspace.bronze.s07_silver_siniestros AS destino
USING (
  SELECT * FROM workspace.bronze.s07_lote_siniestros WHERE id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
  QUALIFY ROW_NUMBER() OVER (
    PARTITION BY id_siniestro ORDER BY fecha_actualizacion DESC, id_lote DESC
  ) = 1
) AS origen
ON destino.id_siniestro = origen.id_siniestro
WHEN MATCHED AND origen.fecha_actualizacion > destino.fecha_actualizacion THEN UPDATE SET
  id_lote = origen.id_lote,
  id_poliza = origen.id_poliza,
  fecha_siniestro = origen.fecha_siniestro,
  fecha_reporte = origen.fecha_reporte,
  estado_siniestro = origen.estado_siniestro,
  monto_pagado = origen.monto_pagado,
  fecha_actualizacion = origen.fecha_actualizacion
WHEN NOT MATCHED THEN INSERT (
  id_lote, id_siniestro, id_poliza,
  fecha_siniestro, fecha_reporte, estado_siniestro,
  monto_pagado, fecha_actualizacion
)
VALUES (
  origen.id_lote, origen.id_siniestro, origen.id_poliza,
  origen.fecha_siniestro, origen.fecha_reporte, origen.estado_siniestro,
  origen.monto_pagado, origen.fecha_actualizacion
);

-- Con el detalle ya actualizado, registrar el producto vigente de cada siniestro del lote.
MERGE INTO workspace.bronze.s07_productos_afectados AS destino
USING (
  SELECT DISTINCT l.id_lote, p.id_producto
  FROM workspace.bronze.s07_lote_siniestros AS l
  INNER JOIN workspace.bronze.s07_silver_polizas AS p ON l.id_poliza = p.id_poliza
  WHERE l.id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes)
) AS origen
ON destino.id_lote = origen.id_lote AND destino.id_producto = origen.id_producto
WHEN NOT MATCHED THEN INSERT (
  id_lote, id_producto
)
VALUES (
  origen.id_lote, origen.id_producto
);

SELECT * FROM workspace.bronze.s07_productos_afectados
WHERE id_lote IN (SELECT id_lote FROM workspace.bronze.s07_entregas_pendientes) ORDER BY id_producto;

SELECT id_poliza, id_producto, prima, estado_poliza, id_lote
FROM workspace.bronze.s07_silver_polizas ORDER BY id_poliza;
