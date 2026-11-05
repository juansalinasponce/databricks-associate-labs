-- Databricks notebook source
-- MAGIC %md
-- MAGIC # Validar desde la identidad del analista
-- MAGIC Abre tu propio SQL Editor o importa este notebook en tu sesión del mismo workspace.
-- MAGIC No uses la identidad del creador, un Job que ejecute como propietario ni resultados compartidos.
-- MAGIC Sustituye `workspace` y `alumno01`. Ejecuta cada consulta por separado.
-- MAGIC Repite las consultas tras cada etapa A–G del instructor y registra resultado e identidad.
-- MAGIC Los errores de autorización esperados son evidencia; no uses Run all.

-- COMMAND ----------

SELECT current_user() AS identidad_que_prueba;

-- COMMAND ----------

-- Prueba V: consumo autorizado. En fase B o G: dos filas y total 3000.00.
SELECT * FROM workspace.s14_alumno01_gobierno.gold_siniestros_resumen
ORDER BY estado_siniestro;

-- COMMAND ----------

-- Prueba T: acceso al detalle. Debe fallar en B, C, F y G.
SELECT * FROM workspace.s14_alumno01_gobierno.silver_siniestros
ORDER BY id_siniestro;

-- COMMAND ----------

-- Prueba M: modificación. Debe fallar en todas las fases.
-- Asigna el mismo valor para que un permiso excesivo inesperado no cambie el monto.
UPDATE workspace.s14_alumno01_gobierno.silver_siniestros
SET monto_pagado = monto_pagado
WHERE id_siniestro = 'SIN001';
-- Si se ejecuta correctamente, reporta permiso excesivo; no lo interpretes como éxito del control.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Cómo interpretar un fallo
-- MAGIC Registra el mensaje exacto. Un fallo por cuota, compute, nombre mal escrito o tabla
-- MAGIC inexistente no demuestra revocación. El instructor debe confirmar que el objeto existe.
-- MAGIC Ejecuta de nuevo la consulta después del cambio; no reutilices una cuadrícula anterior.
-- MAGIC Aplicación diaria: comprobar el acceso efectivo desde la identidad del consumidor.
