-- Databricks notebook source
-- MAGIC %md
-- MAGIC # Gold de siniestros — preparación desde la cuenta principal
-- MAGIC Datos ficticios: enero–diciembre de 2025. Corte: 2025-12-31. Moneda: PEN.
-- MAGIC Sustituye `workspace` si tu catálogo tiene otro nombre.
-- MAGIC Usa un schema nuevo. Si ya existe, detente y revisa si esta práctica ya está preparada.
-- MAGIC Ejecuta cada sentencia completa; ante un error, detente antes del INSERT.

-- COMMAND ----------

SELECT current_user() AS identidad, current_catalog() AS catalogo_actual;
SHOW CATALOGS;

-- COMMAND ----------

CREATE SCHEMA workspace.gold_s15_seguros
COMMENT 'Gold didactico de seguros. Datos sinteticos de 2025. Sesion 15.';

-- COMMAND ----------

CREATE TABLE workspace.gold_s15_seguros.siniestros_mensuales (
  mes_reporte DATE COMMENT 'Primer dia del mes en que se reportaron los siniestros.',
  tipo_seguro STRING COMMENT 'AUTO, SALUD o HOGAR; categorias ficticias.',
  estado_siniestro STRING COMMENT 'ABIERTO o CERRADO al corte 2025-12-31.',
  cantidad_siniestros INT COMMENT 'Cantidad agregada: sumar este campo para contar siniestros.',
  monto_pagado DECIMAL(14,2) COMMENT 'Pago acumulado en PEN al corte para este grupo de siniestros.',
  monto_reservado DECIMAL(14,2) COMMENT 'Saldo estimado pendiente ficticio en PEN; sin regla actuarial real.'
) USING DELTA
COMMENT 'Una fila por mes de reporte, tipo de seguro y estado al corte 2025-12-31. Owner de negocio ficticio: Operaciones demo. Carga SQL de entrenamiento, sin datos personales.';

-- COMMAND ----------

-- OVERWRITE reemplaza SOLO las filas de esta tabla didactica y permite repetir la carga.
-- Ejecutar como propietario unicamente sobre la tabla de este laboratorio.
-- INSERT INTO agregaria filas y duplicaria los indicadores al repetirlo.
INSERT OVERWRITE workspace.gold_s15_seguros.siniestros_mensuales
  (mes_reporte, tipo_seguro, estado_siniestro, cantidad_siniestros, monto_pagado, monto_reservado)
VALUES
  (DATE '2025-01-01', 'AUTO',  'CERRADO', 40, 40000.00,     0.00),
  (DATE '2025-01-01', 'AUTO',  'ABIERTO', 10,  1000.00, 20000.00),
  (DATE '2025-01-01', 'SALUD', 'CERRADO', 60, 30000.00,     0.00),
  (DATE '2025-01-01', 'SALUD', 'ABIERTO', 15,   750.00, 12000.00),
  (DATE '2025-01-01', 'HOGAR', 'CERRADO', 20, 30000.00,     0.00),
  (DATE '2025-01-01', 'HOGAR', 'ABIERTO',  5,   750.00, 15000.00),
  (DATE '2025-02-01', 'AUTO',  'CERRADO', 42, 42000.00,     0.00),
  (DATE '2025-02-01', 'AUTO',  'ABIERTO', 11,  1100.00, 22000.00),
  (DATE '2025-02-01', 'SALUD', 'CERRADO', 62, 31000.00,     0.00),
  (DATE '2025-02-01', 'SALUD', 'ABIERTO', 16,   800.00, 12800.00),
  (DATE '2025-02-01', 'HOGAR', 'CERRADO', 21, 31500.00,     0.00),
  (DATE '2025-02-01', 'HOGAR', 'ABIERTO',  6,   900.00, 18000.00),
  (DATE '2025-03-01', 'AUTO',  'CERRADO', 44, 44000.00,     0.00),
  (DATE '2025-03-01', 'AUTO',  'ABIERTO', 12,  1200.00, 24000.00),
  (DATE '2025-03-01', 'SALUD', 'CERRADO', 64, 32000.00,     0.00),
  (DATE '2025-03-01', 'SALUD', 'ABIERTO', 17,   850.00, 13600.00),
  (DATE '2025-03-01', 'HOGAR', 'CERRADO', 22, 33000.00,     0.00),
  (DATE '2025-03-01', 'HOGAR', 'ABIERTO',  7,  1050.00, 21000.00),
  (DATE '2025-04-01', 'AUTO',  'CERRADO', 46, 46000.00,     0.00),
  (DATE '2025-04-01', 'AUTO',  'ABIERTO', 13,  1300.00, 26000.00),
  (DATE '2025-04-01', 'SALUD', 'CERRADO', 66, 33000.00,     0.00),
  (DATE '2025-04-01', 'SALUD', 'ABIERTO', 18,   900.00, 14400.00),
  (DATE '2025-04-01', 'HOGAR', 'CERRADO', 23, 34500.00,     0.00),
  (DATE '2025-04-01', 'HOGAR', 'ABIERTO',  8,  1200.00, 24000.00),
  (DATE '2025-05-01', 'AUTO',  'CERRADO', 48, 48000.00,     0.00),
  (DATE '2025-05-01', 'AUTO',  'ABIERTO', 14,  1400.00, 28000.00),
  (DATE '2025-05-01', 'SALUD', 'CERRADO', 68, 34000.00,     0.00),
  (DATE '2025-05-01', 'SALUD', 'ABIERTO', 19,   950.00, 15200.00),
  (DATE '2025-05-01', 'HOGAR', 'CERRADO', 24, 36000.00,     0.00),
  (DATE '2025-05-01', 'HOGAR', 'ABIERTO',  9,  1350.00, 27000.00),
  (DATE '2025-06-01', 'AUTO',  'CERRADO', 50, 50000.00,     0.00),
  (DATE '2025-06-01', 'AUTO',  'ABIERTO', 15,  1500.00, 30000.00),
  (DATE '2025-06-01', 'SALUD', 'CERRADO', 70, 35000.00,     0.00),
  (DATE '2025-06-01', 'SALUD', 'ABIERTO', 20,  1000.00, 16000.00),
  (DATE '2025-06-01', 'HOGAR', 'CERRADO', 25, 37500.00,     0.00),
  (DATE '2025-06-01', 'HOGAR', 'ABIERTO', 10,  1500.00, 30000.00),
  (DATE '2025-07-01', 'AUTO',  'CERRADO', 52, 52000.00,     0.00),
  (DATE '2025-07-01', 'AUTO',  'ABIERTO', 16,  1600.00, 32000.00),
  (DATE '2025-07-01', 'SALUD', 'CERRADO', 72, 36000.00,     0.00),
  (DATE '2025-07-01', 'SALUD', 'ABIERTO', 21,  1050.00, 16800.00),
  (DATE '2025-07-01', 'HOGAR', 'CERRADO', 26, 39000.00,     0.00),
  (DATE '2025-07-01', 'HOGAR', 'ABIERTO', 11,  1650.00, 33000.00),
  (DATE '2025-08-01', 'AUTO',  'CERRADO', 54, 54000.00,     0.00),
  (DATE '2025-08-01', 'AUTO',  'ABIERTO', 17,  1700.00, 34000.00),
  (DATE '2025-08-01', 'SALUD', 'CERRADO', 74, 37000.00,     0.00),
  (DATE '2025-08-01', 'SALUD', 'ABIERTO', 22,  1100.00, 17600.00),
  (DATE '2025-08-01', 'HOGAR', 'CERRADO', 27, 40500.00,     0.00),
  (DATE '2025-08-01', 'HOGAR', 'ABIERTO', 12,  1800.00, 36000.00),
  (DATE '2025-09-01', 'AUTO',  'CERRADO', 56, 56000.00,     0.00),
  (DATE '2025-09-01', 'AUTO',  'ABIERTO', 18,  1800.00, 36000.00),
  (DATE '2025-09-01', 'SALUD', 'CERRADO', 76, 38000.00,     0.00),
  (DATE '2025-09-01', 'SALUD', 'ABIERTO', 23,  1150.00, 18400.00),
  (DATE '2025-09-01', 'HOGAR', 'CERRADO', 28, 42000.00,     0.00),
  (DATE '2025-09-01', 'HOGAR', 'ABIERTO', 13,  1950.00, 39000.00),
  (DATE '2025-10-01', 'AUTO',  'CERRADO', 58, 58000.00,     0.00),
  (DATE '2025-10-01', 'AUTO',  'ABIERTO', 19,  1900.00, 38000.00),
  (DATE '2025-10-01', 'SALUD', 'CERRADO', 78, 39000.00,     0.00),
  (DATE '2025-10-01', 'SALUD', 'ABIERTO', 24,  1200.00, 19200.00),
  (DATE '2025-10-01', 'HOGAR', 'CERRADO', 29, 43500.00,     0.00),
  (DATE '2025-10-01', 'HOGAR', 'ABIERTO', 14,  2100.00, 42000.00),
  (DATE '2025-11-01', 'AUTO',  'CERRADO', 60, 60000.00,     0.00),
  (DATE '2025-11-01', 'AUTO',  'ABIERTO', 20,  2000.00, 40000.00),
  (DATE '2025-11-01', 'SALUD', 'CERRADO', 80, 40000.00,     0.00),
  (DATE '2025-11-01', 'SALUD', 'ABIERTO', 25,  1250.00, 20000.00),
  (DATE '2025-11-01', 'HOGAR', 'CERRADO', 30, 45000.00,     0.00),
  (DATE '2025-11-01', 'HOGAR', 'ABIERTO', 15,  2250.00, 45000.00),
  (DATE '2025-12-01', 'AUTO',  'CERRADO', 62, 62000.00,     0.00),
  (DATE '2025-12-01', 'AUTO',  'ABIERTO', 21,  2100.00, 42000.00),
  (DATE '2025-12-01', 'SALUD', 'CERRADO', 82, 41000.00,     0.00),
  (DATE '2025-12-01', 'SALUD', 'ABIERTO', 26,  1300.00, 20800.00),
  (DATE '2025-12-01', 'HOGAR', 'CERRADO', 31, 46500.00,     0.00),
  (DATE '2025-12-01', 'HOGAR', 'ABIERTO', 16,  2400.00, 48000.00);

-- COMMAND ----------

SELECT COUNT(*) AS filas, COUNT(DISTINCT mes_reporte) AS meses,
       MIN(mes_reporte) AS primer_mes, MAX(mes_reporte) AS ultimo_mes,
       SUM(cantidad_siniestros) AS total_siniestros
FROM workspace.gold_s15_seguros.siniestros_mensuales;
-- Esperado: 72 filas, 12 meses, 2025-01-01, 2025-12-01, 2328 siniestros.
