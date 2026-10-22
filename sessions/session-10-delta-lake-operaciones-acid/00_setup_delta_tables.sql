-- ============================================================
-- LABORATORIO MEDALLION DE SEGUROS
-- 00 - CREACIÓN DE SCHEMAS Y TABLAS DELTA
-- ============================================================
--
-- Catálogo utilizado según el entorno:
--   workspace
--
-- Capas:
--   workspace.bronze
--   workspace.silver
--   workspace.gold
--
-- Las tablas se crean como MANAGED DELTA TABLES.
-- Los CSV de Landing permanecen en el Volume conectado a S3.
-- ============================================================


-- ============================================================
-- 1. SCHEMAS
-- ============================================================

CREATE SCHEMA IF NOT EXISTS workspace.bronze;
CREATE SCHEMA IF NOT EXISTS workspace.silver;
CREATE SCHEMA IF NOT EXISTS workspace.gold;


-- ============================================================
-- 2. BRONZE
-- ============================================================

CREATE TABLE IF NOT EXISTS workspace.bronze.polizas_medallion (
    id_poliza              STRING,
    id_asegurado           STRING,
    nro_documento          STRING,
    nombre_asegurado       STRING,
    producto               STRING,
    plan                   STRING,
    prima_mensual          DECIMAL(18,2),
    suma_asegurada         DECIMAL(18,2),
    estado_poliza          STRING,
    canal_venta            STRING,
    departamento           STRING,
    fecha_inicio_poliza    DATE,
    fecha_fin_poliza       DATE,
    fecha_actualizacion    TIMESTAMP,

    -- Columnas técnicas
    fecha_ingestion        TIMESTAMP,
    origen_sistema         STRING,
    archivo_origen         STRING,
    id_ejecucion           STRING
)
USING DELTA
COMMENT 'Bronze - eventos/versiones de pólizas recibidas desde Landing';


CREATE TABLE IF NOT EXISTS workspace.bronze.siniestros_medallion (
    id_siniestro           STRING,
    id_poliza              STRING,
    tipo_siniestro         STRING,
    fecha_ocurrencia       DATE,
    fecha_reporte          DATE,
    estado_siniestro       STRING,
    monto_reserva          DECIMAL(18,2),
    monto_pagado           DECIMAL(18,2),
    canal_reporte          STRING,
    ajustador              STRING,
    fecha_actualizacion    TIMESTAMP,

    -- Columnas técnicas
    fecha_ingestion        TIMESTAMP,
    origen_sistema         STRING,
    archivo_origen         STRING,
    id_ejecucion           STRING
)
USING DELTA
COMMENT 'Bronze - eventos/versiones de siniestros recibidos desde Landing';


-- ============================================================
-- 3. SILVER - SCD TYPE 2
-- ============================================================
--
-- Cada cambio real en los atributos genera una nueva versión.
--
-- fecha_inicio_vigencia:
--   desde cuándo es válida la versión.
--
-- fecha_fin_vigencia:
--   hasta cuándo es válida.
--
-- es_actual:
--   TRUE = versión vigente.
-- ============================================================

CREATE TABLE IF NOT EXISTS workspace.silver.polizas_scd2 (
    sk_poliza_scd2         STRING,
    id_poliza              STRING,
    id_asegurado           STRING,
    nro_documento          STRING,
    nombre_asegurado       STRING,
    producto               STRING,
    plan                   STRING,
    prima_mensual          DECIMAL(18,2),
    suma_asegurada         DECIMAL(18,2),
    estado_poliza          STRING,
    canal_venta            STRING,
    departamento           STRING,
    fecha_inicio_poliza    DATE,
    fecha_fin_poliza       DATE,

    -- SCD2
    hash_registro          STRING,
    fecha_inicio_vigencia  TIMESTAMP,
    fecha_fin_vigencia     TIMESTAMP,
    es_actual              BOOLEAN,

    -- Columnas técnicas
    fecha_ingestion        TIMESTAMP,
    fecha_procesamiento    TIMESTAMP,
    origen_sistema         STRING,
    archivo_origen         STRING,
    id_ejecucion           STRING
)
USING DELTA
COMMENT 'Silver - historial SCD Type 2 de pólizas';


CREATE TABLE IF NOT EXISTS workspace.silver.siniestros_scd2 (
    sk_siniestro_scd2      STRING,
    id_siniestro           STRING,
    id_poliza              STRING,
    tipo_siniestro         STRING,
    fecha_ocurrencia       DATE,
    fecha_reporte          DATE,
    estado_siniestro       STRING,
    monto_reserva          DECIMAL(18,2),
    monto_pagado           DECIMAL(18,2),
    canal_reporte          STRING,
    ajustador              STRING,

    -- SCD2
    hash_registro          STRING,
    fecha_inicio_vigencia  TIMESTAMP,
    fecha_fin_vigencia     TIMESTAMP,
    es_actual              BOOLEAN,

    -- Columnas técnicas
    fecha_ingestion        TIMESTAMP,
    fecha_procesamiento    TIMESTAMP,
    origen_sistema         STRING,
    archivo_origen         STRING,
    id_ejecucion           STRING
)
USING DELTA
COMMENT 'Silver - historial SCD Type 2 de siniestros';


-- ============================================================
-- 4. GOLD - DIMENSIONES
-- ============================================================

CREATE TABLE IF NOT EXISTS workspace.gold.dim_asegurado (
    sk_asegurado           STRING,
    id_asegurado           STRING,
    nro_documento          STRING,
    nombre_asegurado       STRING,
    departamento           STRING,
    canal_venta            STRING,
    fecha_carga            TIMESTAMP,
    id_ejecucion           STRING
)
USING DELTA;


CREATE TABLE IF NOT EXISTS workspace.gold.dim_producto (
    sk_producto            STRING,
    producto               STRING,
    plan                   STRING,
    fecha_carga            TIMESTAMP,
    id_ejecucion           STRING
)
USING DELTA;


CREATE TABLE IF NOT EXISTS workspace.gold.dim_poliza (
    sk_poliza              STRING,
    id_poliza              STRING,
    sk_asegurado           STRING,
    sk_producto            STRING,
    estado_poliza          STRING,
    fecha_inicio_poliza    DATE,
    fecha_fin_poliza       DATE,
    canal_venta            STRING,
    fecha_carga            TIMESTAMP,
    id_ejecucion           STRING
)
USING DELTA;


CREATE TABLE IF NOT EXISTS workspace.gold.dim_tiempo (
    sk_fecha               INT,
    fecha                  DATE,
    anio                   INT,
    mes                    INT,
    nombre_mes             STRING,
    trimestre              INT,
    dia                    INT,
    dia_semana             INT,
    fecha_carga            TIMESTAMP,
    id_ejecucion           STRING
)
USING DELTA;


-- ============================================================
-- 5. GOLD - HECHOS
-- ============================================================

CREATE TABLE IF NOT EXISTS workspace.gold.fact_poliza (
    sk_fact_poliza         STRING,
    sk_poliza              STRING,
    sk_asegurado           STRING,
    sk_producto            STRING,
    sk_fecha_inicio        INT,
    prima_mensual          DECIMAL(18,2),
    suma_asegurada         DECIMAL(18,2),
    estado_poliza          STRING,
    fecha_carga            TIMESTAMP,
    id_ejecucion           STRING
)
USING DELTA;


CREATE TABLE IF NOT EXISTS workspace.gold.fact_siniestro (
    sk_fact_siniestro      STRING,
    id_siniestro           STRING,
    sk_poliza              STRING,
    sk_asegurado           STRING,
    sk_producto            STRING,
    sk_fecha_ocurrencia    INT,
    sk_fecha_reporte       INT,
    tipo_siniestro         STRING,
    estado_siniestro       STRING,
    monto_reserva          DECIMAL(18,2),
    monto_pagado           DECIMAL(18,2),
    dias_reporte           INT,
    fecha_carga            TIMESTAMP,
    id_ejecucion           STRING
)
USING DELTA;


-- ============================================================
-- 6. VALIDACIÓN
-- ============================================================

SHOW TABLES IN workspace.bronze;
SHOW TABLES IN workspace.silver;
SHOW TABLES IN workspace.gold;
