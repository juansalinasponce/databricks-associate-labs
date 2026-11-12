-- Pegar únicamente este SELECT como un dataset del AI/BI Dashboard.
-- No contiene CREATE, INSERT ni variables; es compatible con el Genie vinculado.
SELECT codigo_dp, ambiente, mes_referencia, nombre_producto, tipo_seguro, canal,
       cantidad_polizas_emitidas, prima_emitida, cantidad_siniestros,
       cantidad_cerrados, monto_pagado, monto_reservado, fecha_corte, moneda
FROM workspace.s16.vw_indicadores;
