-- Databricks notebook source
-- DP-SEG-016 | DEV | contrato 1.0.0
-- Destino único: workspace.s16. Datos sintéticos. Revisar antes de ejecutar.


ALTER TABLE workspace.s16.dim_fecha ADD CONSTRAINT pk_dim_fecha PRIMARY KEY (id_fecha);

ALTER TABLE workspace.s16.dim_producto ADD CONSTRAINT pk_dim_producto PRIMARY KEY (id_producto);

ALTER TABLE workspace.s16.dim_canal ADD CONSTRAINT pk_dim_canal PRIMARY KEY (id_canal);

ALTER TABLE workspace.s16.dim_estado ADD CONSTRAINT pk_dim_estado PRIMARY KEY (id_estado);

ALTER TABLE workspace.s16.fact_polizas ADD CONSTRAINT pk_fact_polizas PRIMARY KEY (id_hecho_poliza);

ALTER TABLE workspace.s16.fact_siniestros ADD CONSTRAINT pk_fact_siniestros PRIMARY KEY (id_hecho_siniestro);

ALTER TABLE workspace.s16.fact_polizas ADD CONSTRAINT fk_fact_polizas_id_fecha FOREIGN KEY (id_fecha) REFERENCES workspace.s16.dim_fecha (id_fecha);

ALTER TABLE workspace.s16.fact_polizas ADD CONSTRAINT fk_fact_polizas_id_producto FOREIGN KEY (id_producto) REFERENCES workspace.s16.dim_producto (id_producto);

ALTER TABLE workspace.s16.fact_polizas ADD CONSTRAINT fk_fact_polizas_id_canal FOREIGN KEY (id_canal) REFERENCES workspace.s16.dim_canal (id_canal);

ALTER TABLE workspace.s16.fact_siniestros ADD CONSTRAINT fk_fact_siniestros_id_fecha FOREIGN KEY (id_fecha) REFERENCES workspace.s16.dim_fecha (id_fecha);

ALTER TABLE workspace.s16.fact_siniestros ADD CONSTRAINT fk_fact_siniestros_id_producto FOREIGN KEY (id_producto) REFERENCES workspace.s16.dim_producto (id_producto);

ALTER TABLE workspace.s16.fact_siniestros ADD CONSTRAINT fk_fact_siniestros_id_canal FOREIGN KEY (id_canal) REFERENCES workspace.s16.dim_canal (id_canal);

ALTER TABLE workspace.s16.fact_siniestros ADD CONSTRAINT fk_fact_siniestros_id_estado FOREIGN KEY (id_estado) REFERENCES workspace.s16.dim_estado (id_estado);
