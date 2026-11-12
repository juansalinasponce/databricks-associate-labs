-- Databricks notebook source
-- DP-SEG-016 | DEV | contrato 1.0.0
-- Destino único: workspace.s16. Datos sintéticos. Revisar antes de ejecutar.


-- COMMAND ----------

CREATE SCHEMA workspace.s16 COMMENT 'DP-SEG-016 - DEV - formación S16';

-- COMMAND ----------

CREATE TABLE workspace.s16.matricula (
  codigo_dp STRING NOT NULL COMMENT 'Identificador estable del único Data Product',
  nombre STRING NOT NULL COMMENT 'Nombre técnico del Data Product',
  dominio STRING NOT NULL COMMENT 'Dominio de negocio ficticio',
  owner_negocio STRING NOT NULL COMMENT 'Rol responsable del producto; no concede permisos UC',
  steward STRING NOT NULL COMMENT 'Rol que revisa definiciones y calidad',
  descripcion STRING NOT NULL COMMENT 'Necesidad que resuelve',
  consumidores STRING NOT NULL COMMENT 'Roles consumidores ficticios',
  freshness_objetivo STRING NOT NULL COMMENT 'Objetivo de actualización; no programa ejecuciones',
  calidad STRING NOT NULL COMMENT 'Reglas del contrato de datos',
  seguridad STRING NOT NULL COMMENT 'Clasificación y acceso previsto',
  slo_objetivo STRING NOT NULL COMMENT 'Objetivo didáctico, no garantía de Free Edition',
  version_contrato STRING NOT NULL COMMENT 'Versión del contrato, independiente del ambiente',
  estado STRING NOT NULL COMMENT 'Estado documental de la matrícula',
  fecha_corte DATE NOT NULL COMMENT 'Fecha de referencia del dataset histórico',
  fuente STRING NOT NULL COMMENT 'Origen sintético de referencia'
) USING DELTA
COMMENT 'Una fila: matrícula de un Data Product de referencia.'
TBLPROPERTIES ('training.codigo_dp'='DP-SEG-016', 'training.ambiente'='DEV', 'training.version_contrato'='1.0.0');

-- COMMAND ----------

CREATE TABLE workspace.s16.ambientes (
  codigo_dp STRING NOT NULL COMMENT 'Mismo código en todos los ambientes',
  ambiente STRING NOT NULL COMMENT 'DEV, TEST, UAT o PRD',
  catalogo STRING NOT NULL COMMENT 'Catálogo existente autorizado; el script no lo crea',
  esquema STRING NOT NULL COMMENT 'Schema que se creará en el catálogo seleccionado',
  habilitado STRING NOT NULL COMMENT 'SI permite generar SQL; NO conserva solo la referencia',
  nombre_genie STRING NOT NULL COMMENT 'Nombre propuesto; se crea manualmente en la UI',
  nombre_dashboard STRING NOT NULL COMMENT 'Nombre propuesto; se crea manualmente en la UI'
) USING DELTA
COMMENT 'Cuatro referencias de ambiente para el mismo Data Product; no implica despliegue.'
TBLPROPERTIES ('training.codigo_dp'='DP-SEG-016', 'training.ambiente'='DEV', 'training.version_contrato'='1.0.0');

-- COMMAND ----------

CREATE TABLE workspace.s16.proceso (
  codigo_proceso STRING NOT NULL COMMENT 'Identificador estable del proceso de referencia',
  codigo_dp STRING NOT NULL COMMENT 'Data Product que publica el proceso',
  nombre STRING NOT NULL COMMENT 'Nombre del proceso de publicación',
  entrada STRING NOT NULL COMMENT 'Fuente de los datos de referencia',
  pasos STRING NOT NULL COMMENT 'Validación y publicación que realiza el proceso',
  salida STRING NOT NULL COMMENT 'Activos que consume el negocio en el ambiente seleccionado',
  ejecucion STRING NOT NULL COMMENT 'Modo efectivo de ejecución; no crea un Job',
  responsable STRING NOT NULL COMMENT 'Rol técnico ficticio'
) USING DELTA
COMMENT 'Un proceso de referencia que publica el único Data Product; ejecución manual.'
TBLPROPERTIES ('training.codigo_dp'='DP-SEG-016', 'training.ambiente'='DEV', 'training.version_contrato'='1.0.0');

-- COMMAND ----------

CREATE TABLE workspace.s16.dim_fecha (
  id_fecha INT NOT NULL COMMENT 'PK mensual YYYYMM01',
  mes_referencia DATE NOT NULL COMMENT 'Primer día del mes: reporte de siniestros o emisión de pólizas',
  anio INT NOT NULL COMMENT 'Año del mes de referencia',
  mes INT NOT NULL COMMENT 'Número de mes para ordenar',
  nombre_mes STRING NOT NULL COMMENT 'Etiqueta del mes; ordenar por mes_referencia'
) USING DELTA
COMMENT 'Una fila por mes de 2025; dimensión mensual compartida.'
TBLPROPERTIES ('training.codigo_dp'='DP-SEG-016', 'training.ambiente'='DEV', 'training.version_contrato'='1.0.0');

-- COMMAND ----------

CREATE TABLE workspace.s16.dim_producto (
  id_producto INT NOT NULL COMMENT 'PK del producto ficticio',
  nombre_producto STRING NOT NULL COMMENT 'Nombre del producto de referencia',
  tipo_seguro STRING NOT NULL COMMENT 'AUTO, SALUD o HOGAR'
) USING DELTA
COMMENT 'Una fila por producto ficticio; no es el registro de Data Products.'
TBLPROPERTIES ('training.codigo_dp'='DP-SEG-016', 'training.ambiente'='DEV', 'training.version_contrato'='1.0.0');

-- COMMAND ----------

CREATE TABLE workspace.s16.dim_canal (
  id_canal INT NOT NULL COMMENT 'PK del canal ficticio',
  canal STRING NOT NULL COMMENT 'Canal atribuido al grupo de pólizas o siniestros'
) USING DELTA
COMMENT 'Una fila por canal ficticio.'
TBLPROPERTIES ('training.codigo_dp'='DP-SEG-016', 'training.ambiente'='DEV', 'training.version_contrato'='1.0.0');

-- COMMAND ----------

CREATE TABLE workspace.s16.dim_estado (
  id_estado INT NOT NULL COMMENT 'PK del estado al corte',
  estado_siniestro STRING NOT NULL COMMENT 'ABIERTO o CERRADO al 2025-12-31'
) USING DELTA
COMMENT 'Una fila por estado de siniestro al corte 2025-12-31.'
TBLPROPERTIES ('training.codigo_dp'='DP-SEG-016', 'training.ambiente'='DEV', 'training.version_contrato'='1.0.0');

-- COMMAND ----------

CREATE TABLE workspace.s16.fact_polizas (
  id_hecho_poliza INT NOT NULL COMMENT 'PK técnica del grupo; no es un id de póliza individual',
  id_fecha INT NOT NULL COMMENT 'FK a dim_fecha: mes de emisión',
  id_producto INT NOT NULL COMMENT 'FK a dim_producto',
  id_canal INT NOT NULL COMMENT 'FK a dim_canal',
  cantidad_polizas_emitidas INT NOT NULL COMMENT 'Cantidad de emisiones del grupo: usar SUM',
  prima_emitida DECIMAL(18,2) NOT NULL COMMENT 'Prima de las emisiones del grupo en PEN',
  moneda STRING NOT NULL COMMENT 'PEN; no mezclar monedas'
) USING DELTA
COMMENT 'Una fila por mes de emisión, producto y canal; emisiones de 2025.'
TBLPROPERTIES ('training.codigo_dp'='DP-SEG-016', 'training.ambiente'='DEV', 'training.version_contrato'='1.0.0');

-- COMMAND ----------

CREATE TABLE workspace.s16.fact_siniestros (
  id_hecho_siniestro INT NOT NULL COMMENT 'PK técnica del grupo; no es un id de siniestro individual',
  id_fecha INT NOT NULL COMMENT 'FK a dim_fecha: mes de reporte, no fecha de pago ni cierre',
  id_producto INT NOT NULL COMMENT 'FK a dim_producto',
  id_canal INT NOT NULL COMMENT 'FK a dim_canal',
  id_estado INT NOT NULL COMMENT 'FK a dim_estado: estado al corte',
  cantidad_siniestros INT NOT NULL COMMENT 'Cantidad de siniestros del grupo: usar SUM',
  monto_pagado DECIMAL(18,2) NOT NULL COMMENT 'Pago acumulado al corte en PEN, por cohorte de reporte',
  monto_reservado DECIMAL(18,2) NOT NULL COMMENT 'Saldo pendiente ficticio en PEN, sin regla actuarial',
  fecha_corte DATE NOT NULL COMMENT 'Corte único 2025-12-31; no sumar snapshots',
  moneda STRING NOT NULL COMMENT 'PEN; no mezclar monedas'
) USING DELTA
COMMENT 'Una fila por mes de reporte, producto, canal y estado al corte 2025-12-31.'
TBLPROPERTIES ('training.codigo_dp'='DP-SEG-016', 'training.ambiente'='DEV', 'training.version_contrato'='1.0.0');
