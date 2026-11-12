# Genie del Data Product DP-SEG-016

Se crea **un agente para DEV**. Los otros ambientes son referencias de la
matrícula; no se mezclan sus fuentes. La interfaz puede llamarlo **Genie Agent**
o **Genie Space**. La guía oficial describe los requisitos de Unity Catalog,
permisos de datos y warehouse:
[crear un Genie Agent](https://docs.databricks.com/aws/en/genie-agents/set-up).

## Ficha del asistente

| Campo | Referencia |
| --- | --- |
| Nombre | DP-SEG-016 - DEV - Genie |
| Propósito | Consultar indicadores sintéticos de siniestros y emisiones de 2025 |
| Usuarios | Supervisor y analista ficticios |
| Fuentes | Cuatro dimensiones, dos hechos y tres vistas de `workspace.s16` |
| Preguntas admitidas | Cantidades, montos, distribución por producto/canal/mes, cierre al corte |
| Límites | Sin datos personales, sin decisiones actuariales, sin explicación causal ni predicción |
| Validación | Comparación con Q3–Q7 de `sql/03-validar-y-consultar.sql` |

## 1. Generar y revisar SQL con Genie Code

En SQL Editor abre Genie Code y adjunta `workspace.s16.vw_indicadores` como
contexto si el selector lo permite. Usa este prompt:

```text
Genera solo una consulta SELECT de Databricks SQL usando
workspace.s16.vw_indicadores, del Data Product DP-SEG-016, ambiente DEV.
Muestra los siniestros reportados por mes de referencia durante 2025.
Cada fila es un grupo por mes, producto y canal: usa SUM(cantidad_siniestros).
Ordena por la fecha. El estado y los montos corresponden al corte 2025-12-31.
No modifiques datos. Muéstrame el SQL y explica qué cuenta cada fila.
```

Contrasta con Q5: 12 meses; enero 150 y diciembre 238. Revisa la fuente,
agregación y fechas antes de ejecutar. Si no aparece el asistente de código,
utiliza Q5 y explica la consulta.

## 2. Crear el Genie Agent

1. Abre **Genie Agents → New**, o la opción equivalente del workspace.
2. Nómbralo `DP-SEG-016 - DEV - Genie`.
3. Selecciona el SQL Warehouse existente y las fuentes:
   `workspace.s16.dim_fecha`, `dim_producto`, `dim_canal`, `dim_estado`,
   `fact_polizas`, `fact_siniestros`, `vw_siniestros`, `vw_polizas` y
   `vw_indicadores`, todas en `workspace.s16`.
4. Mantén todas las fuentes en DEV. `matricula`, `proceso` y `ambientes`
   son opcionales para preguntas sobre la documentación del Data Product;
   no representan operaciones de seguros. Si las incluyes, el agente tendrá
   los 12 objetos del laboratorio.
5. Revisa las descripciones propuestas y añade las instrucciones del apartado 4.

El creador necesita acceso a datos y uso del warehouse. Los usuarios del agente
necesitan sus permisos de datos y acceso al agente según el modelo de la
plataforma. El nombre del owner escrito en Excel no proporciona ese acceso.
En Free Edition personal el participante actúa como propietario y consumidor.

## 3. Configurar las siete relaciones

Si ejecutaste `05-relaciones-opcionales.sql`, revisa las relaciones reconocidas
por Genie. Si faltan, añádelas en **Configure → Examples → Add → Joins** o en
la sección equivalente de relaciones. Selecciona **Many to one** desde el hecho
hacia la dimensión y usa igualdad de las columnas indicadas:

| Hecho | Columna FK | Dimensión | Columna PK |
| --- | --- | --- | --- |
| fact_polizas | id_fecha | dim_fecha | id_fecha |
| fact_polizas | id_producto | dim_producto | id_producto |
| fact_polizas | id_canal | dim_canal | id_canal |
| fact_siniestros | id_fecha | dim_fecha | id_fecha |
| fact_siniestros | id_producto | dim_producto | id_producto |
| fact_siniestros | id_canal | dim_canal | id_canal |
| fact_siniestros | id_estado | dim_estado | id_estado |

La dimensión fecha toma el rol de **mes de emisión** para pólizas y **mes de
reporte** para siniestros. No añadas una relación entre ambos hechos ni entre
la vista agregada y los hechos: puede duplicar cantidades y primas.

Las relaciones y ejemplos se configuran como contexto del agente; el
procedimiento está en [ajustar la calidad de Genie](https://docs.databricks.com/aws/en/genie-agents/tune-quality).

## 4. General Instructions — instrucciones listas para copiar

En la configuración del Genie Agent, abre **General Instructions** y pega
el contenido del siguiente bloque. Revisa las fuentes seleccionadas antes de
guardar para que las vistas mencionadas estén disponibles en el agente.

```markdown
Eres un asistente de análisis para el Data Product DP-SEG-016:
Indicadores de Siniestros de una aseguradora ficticia.
Contrato 1.0.0, ambiente DEV.

## Idioma y presentación

- Responde en español, con explicaciones claras para usuarios de negocio.
- Presenta cantidades como enteros, montos en PEN con dos decimales
  y porcentajes con dos decimales.
- Indica siempre el período, los filtros y la fuente utilizados.
- Calcula las respuestas consultando los datos disponibles.

## Alcance

- Utiliza únicamente las fuentes seleccionadas de workspace.s16.
- Los datos son sintéticos y corresponden a 2025.
- El estado de los siniestros y sus montos acumulados corresponden
  al corte 31/12/2025.
- Si no se especifica un período, utiliza todo 2025 e indícalo.
- Si preguntan por “hoy”, “este mes” o información actual,
  explica el período disponible antes de responder.

## Selección de fuentes

- Usa vw_siniestros para analizar siniestros y su estado al corte.
- Usa vw_polizas para analizar pólizas emitidas y prima emitida.
- Usa vw_indicadores para preguntas que combinen pólizas y siniestros.
- Comprueba que cada columna exista en la fuente elegida.
- prima_emitida y cantidad_polizas_emitidas están en vw_polizas
  y vw_indicadores.
- cantidad_siniestros, monto_pagado y monto_reservado están
  en vw_siniestros y vw_indicadores.
- matricula, ambientes y proceso describen el Data Product;
  no representan operaciones de seguros.

## Definiciones de negocio

- “Cantidad de siniestros” significa SUM(cantidad_siniestros).
- “Pólizas emitidas” significa SUM(cantidad_polizas_emitidas).
- “Prima emitida” significa SUM(prima_emitida).
- “Monto pagado” significa SUM(monto_pagado).
- “Monto reservado” significa SUM(monto_reservado).
- COUNT(*) cuenta filas o grupos agregados.
- dim_producto representa productos de seguro: AUTO, SALUD y HOGAR.
- El porcentaje de cierre se calcula sobre las sumas en vw_indicadores
  o vw_siniestros:
  100.0 * SUM(cantidad_cerrados) /
  NULLIF(SUM(cantidad_siniestros), 0).
- No sumes ni promedies porcentajes calculados por fila.

## Interpretación temporal y relaciones

- mes_emision corresponde a la emisión de pólizas.
- mes_reporte corresponde al reporte de siniestros.
- En vw_indicadores, mes_referencia representa ambos roles.
- ABIERTO y CERRADO describen el estado al corte.
- El monto pagado es acumulado al corte y se agrupa por mes de reporte;
  no representa necesariamente pagos realizados durante ese mes.
- Utiliza las relaciones declaradas entre hechos y dimensiones.
- No unas directamente fact_polizas con fact_siniestros:
  usa vw_indicadores para evitar duplicar cantidades y montos.
- La comparación mensual no vincula cada siniestro con una póliza
  emitida durante ese mismo mes.
- No combines vistas y hechos para sumar dos veces los mismos datos.

## Preguntas que requieren información adicional

- Si una pregunta es ambigua, solicita la precisión necesaria.
- Para cierres o pagos ocurridos en una fecha, explica que faltan
  las fechas de cada cierre o pago.
- No interpretes pólizas emitidas como pólizas vigentes.
- No calcules siniestralidad actuarial: no hay exposición
  ni prima devengada.
- Distingue los resultados observados de las posibles explicaciones;
  no atribuyas causas que los datos no permiten demostrar.
```

Complementa las instrucciones con las fórmulas en **Measures** y las relaciones
en **Joins**. General Instructions aporta contexto global; las expresiones y
relaciones también deben quedar definidas en sus secciones correspondientes.
Véase [configuración de instrucciones y conocimiento de Genie](https://docs.databricks.com/aws/en/genie-agents/tune-quality).

Para otro ambiente, copia estas instrucciones y sustituye catálogo, ambiente y
los nombres del agente/dashboard según la matrícula. La versión debe coincidir
con la ficha exportada.

## 5. Ejemplos SQL y preguntas de control

Registra al menos Q4 y Q6 de `sql/03-validar-y-consultar.sql` como ejemplos
pregunta–SQL, si la interfaz lo permite. Prueba las siguientes preguntas sobre
el Excel original:

| Pregunta | Control | Respuesta |
| --- | --- | --- |
| ¿Cuántos siniestros se reportaron en 2025? | Q3 | 2328 |
| ¿Qué tipo de seguro tiene mayor monto pagado al corte para los reportados en 2025? | Q4 | AUTO, PEN 630600.00 |
| ¿Cuántos siniestros reportados en 2025 están abiertos y cerrados al corte? | Q7 | 558 abiertos; 1770 cerrados |
| Para enero de 2025, AUTO y DIRECTO, muestra emisiones, prima, siniestros y monto pagado al corte. | Q6 | 135; PEN 81000.00; 25; PEN 20500.00 |
| ¿Cuál es el porcentaje de cierre de esos siniestros de enero/AUTO/DIRECTO al corte? | Q6 | 80.00% |
| ¿Cuántos siniestros se cerraron durante enero de 2025? | Límite de cobertura | No hay fecha de cierre; no se puede responder con estos datos |

Para cada respuesta, revisa el SQL o sus detalles, ejecútalo en SQL Editor y
compáralo con el control. Si la interfaz no muestra SQL, registra esa limitación
y conserva la comparación numérica. Un resultado con un número correcto y
una interpretación temporal incorrecta también debe corregirse.

## 6. Conectar al dashboard

Sigue `DASHBOARD.md`. Si aparece **Settings → General → Enable Genie → Link
existing Genie Agent**, vincula el agente DEV que acabas de configurar.
Formula las preguntas con los filtros escritos explícitamente en el texto:
los filtros del dashboard no pasan al contexto de un agente vinculado.
Véase [Genie con dashboards](https://docs.databricks.com/aws/en/dashboards/genie-spaces).

Si la opción no aparece, conserva el agente y dashboard separados, conectados
a las mismas vistas. Si el dashboard crea un Genie automático, comprueba su
fuente y sus respuestas; no asumas que heredó las instrucciones del agente
configurado manualmente.

## Evidencia y fallback

Entrega la ficha del asistente, una captura de fuentes/relaciones y dos
preguntas con SQL y comparación. Si Genie no está habilitado, completa la
misma ficha, utiliza los SQL de control y marca **simulación sin Genie**.

Fuentes oficiales consultadas el **11 de noviembre de 2026**.
