-- ============================================================
-- EVALUACIÓN 2 GUIADA - 03 GOLD DECLARATIVE PIPELINE
-- Se despliega como PIPELINE_EVAL2_GOLD
-- Catalog: workspace
-- Schema: gold
-- ============================================================

CREATE OR REFRESH MATERIALIZED VIEW eval2_pagos_por_siniestro
COMMENT 'Pagos procesados agregados por siniestro'
AS
SELECT
    id_siniestro,
    COUNT(*) AS cantidad_pagos,
    SUM(CASE WHEN estado_pago = 'PROCESADO' THEN 1 ELSE 0 END)
        AS cantidad_pagos_procesados,
    ROUND(
        SUM(
            CASE
                WHEN estado_pago = 'PROCESADO'
                THEN COALESCE(monto_pago, 0)
                ELSE 0
            END
        ),
        2
    ) AS monto_pagado
FROM workspace.silver.eval2_pagos
GROUP BY id_siniestro;


CREATE OR REFRESH MATERIALIZED VIEW eval2_resumen_siniestros
COMMENT 'Resumen analítico de siniestros y pagos'
AS
SELECT
    s.tipo_siniestro,
    COUNT(DISTINCT s.id_siniestro) AS cantidad_siniestros,
    ROUND(SUM(s.monto_reserva), 2) AS reserva_total,
    ROUND(SUM(COALESCE(p.monto_pagado, 0)), 2) AS monto_pagado,
    SUM(COALESCE(p.cantidad_pagos_procesados, 0))
        AS pagos_procesados
FROM workspace.silver.eval2_siniestros s
LEFT JOIN eval2_pagos_por_siniestro p
    ON s.id_siniestro = p.id_siniestro
GROUP BY s.tipo_siniestro;
