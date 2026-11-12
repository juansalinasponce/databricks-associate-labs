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
| Fuentes | Cuatro dimensiones, dos hechos y `vw_indicadores` de `workspace.s16` |
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
   `fact_polizas`, `fact_siniestros` y `vw_indicadores`, todas en `workspace.s16`.
4. No añadas tablas de otros ambientes. `matricula`, `proceso` y `ambientes`
   documentan la publicación; no son medidas del negocio y no se agregan como
   fuentes del asistente en esta práctica.
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

## 4. Instrucciones listas para copiar

```text
Eres un asistente de indicadores sintéticos de seguros.
Data Product DP-SEG-016, contrato 1.0.0, ambiente DEV.
Usa exclusivamente las fuentes seleccionadas de workspace.s16.

El año es 2025 y el corte es 2025-12-31. No uses CURRENT_DATE() para estas preguntas.
Todos los montos están en PEN. Los datos y los roles son ficticios.

fact_siniestros: una fila por mes de reporte, producto, canal y estado al corte.
Cuenta siniestros con SUM(cantidad_siniestros). COUNT(*) cuenta grupos.
El monto pagado es acumulado al corte y se atribuye al mes de reporte.
ABIERTO/CERRADO es el estado al corte, no una fecha de cierre.
Para cerrado usa dim_estado.estado_siniestro = 'CERRADO'.

fact_polizas: una fila por mes de emisión, producto y canal.
Usa SUM(cantidad_polizas_emitidas) y SUM(prima_emitida).
No hay pólizas individuales, vigencia, exposición ni prima devengada.
dim_producto representa productos de seguro, no múltiples Data Products.

Usa los joins hecho-dimensión declarados. Para preguntas que combinen
emisiones y siniestros, utiliza workspace.s16.vw_indicadores.
No unas hechos directamente ni sumes resultados de vistas y hechos juntos.
La vista compara reportes y emisiones del mismo mes; no vincula cada siniestro
a una póliza emitida ese mes.

Porcentaje de cierre = 100.0 * SUM(cantidad_cerrados) /
NULLIF(SUM(cantidad_siniestros), 0) en vw_indicadores.
No sumes porcentajes ni promedies porcentajes por fila.

Si piden cierres ocurridos en un mes, pagos realizados en un mes,
siniestralidad, fraude, predicciones o causalidad, explica qué datos faltan.
Si un mes, un producto o un canal es ambiguo, pide precisarlo.
Explica el período, filtros, moneda y fuente utilizados y permite revisar el SQL.
```

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
