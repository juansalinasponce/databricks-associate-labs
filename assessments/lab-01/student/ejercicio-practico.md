# Ejercicio práctico 1 — Reporte de pólizas vigentes

## Metadata

- Tipo: `ASSESSMENT`; duración: 60 minutos, incluida la entrega.
- Nivel: fundamental; cobertura: sesiones 01 a 05.
- Modalidad principal: `PRACTICO_FREE`.
- Alternativa S3: `PRACTICO_CONDICIONAL`, solo con acceso previamente validado.
- Dataset: `data/polizas_evaluacion_01.csv`; 500 filas sintéticas.
- Requiere GitHub: únicamente descargar materiales; no se evalúa Git.
- Conceptos previos: tabla, schema, notebook, SQL, DataFrame, selección,
  filtros, tipos, limpieza, deduplicación y agregaciones.
- Puntaje: 60 puntos.

## Contexto de negocio

Operaciones de `aseguradora_demo` necesita un resumen de las pólizas vigentes
por producto y moneda para la fecha de corte **2026-09-30**. El archivo recibido
contiene variaciones de texto, canales vacíos y filas repetidas que pueden
distorsionar el reporte. Todas las primas corresponden a datos ficticios.

## Objetivo de aprendizaje

Demostrar que puedes cargar o localizar una fuente, prepararla, consultar el
resultado y explicar qué herramientas utilizaste.

## Qué aplicarás

Selección de herramientas de Databricks, inspección del schema, limpieza
básica, consulta de una tabla y explicación de un indicador. No se introduce
contenido nuevo.

## Requisitos previos

El instructor confirmará compute disponible y un catálogo y schema con permisos.
Te asignará un identificador, por ejemplo `p07`. Con ese ejemplo, los nombres son:

```text
workspace.default.polizas_fuente_e1_p07
workspace.default.polizas_preparadas_e1_p07
```

Reemplaza catálogo, schema e identificador por los que te asignen. Conserva la
fuente y escribe solo en tu tabla de salida. Puedes usar SQL o PySpark para la
preparación; basta una solución completa en uno de los dos lenguajes.

## Dataset

| Campo | Significado | Tipo final requerido |
| --- | --- | --- |
| `id_poliza` | Identificador ficticio de póliza | STRING |
| `id_asegurado` | Identificador ficticio de asegurado | STRING |
| `id_producto` | Producto de seguro | STRING |
| `fecha_inicio` | Inicio de vigencia | DATE |
| `fecha_fin` | Fin de vigencia | DATE |
| `estado_poliza` | Estado de la póliza | STRING |
| `prima` | Importe de prima | DECIMAL(12,2) |
| `moneda` | PEN o USD | STRING |
| `canal_venta` | Canal de comercialización | STRING |
| `departamento` | Departamento ficticio del registro | STRING |
| `fecha_actualizacion` | Fecha y hora de actualización | TIMESTAMP |

Las fechas del archivo usan `yyyy-MM-dd` y la actualización usa
`yyyy-MM-dd HH:mm:ss`. El CSV tiene encabezado, separador coma y codificación
UTF-8. Los defectos de esta prueba se limitan a texto no estandarizado, canales
vacíos y duplicados exactos; no hay fechas malformadas ni primas inválidas.

## Opción A — práctica principal

Utiliza **New → Add or upload data → Create or modify a table**, o la opción
equivalente disponible en tu interfaz. Carga el CSV y crea tu tabla fuente en el
schema asignado. Mantén las once columnas como STRING para representar la
entrada original: desactiva la detección automática de tipos o revisa cada tipo
antes de crear la tabla. Conserva el encabezado y el delimitador coma.

Si el instructor ha validado S3 para todos, puedes leer el mismo CSV desde el
prefijo asignado. No debes configurar credenciales ni crear ubicaciones externas.
La ruta de S3 es opcional y no concede puntos adicionales.

## Opción B — fallback para Free Edition

Si no puedes cargar el archivo, el instructor proporcionará la misma tabla
fuente con las once columnas STRING. Registra el nombre completo y el bloqueo
en tu entrega. Para evidenciar la ingesta, explica cómo configurarías encabezado,
delimitador y tipos, y revisa muestra, schema y cantidad de filas de la fuente.

Continúa las mismas actividades sobre esa tabla. Si la cuota o una caída impide
ejecutar consultas, conserva el código y solicita al instructor el procedimiento
de contingencia; no se evalúa la resolución de infraestructura.

## Escenario y reglas de negocio

- Estandariza `estado_poliza`, `moneda` y `canal_venta` en mayúsculas y sin
  espacios exteriores.
- Reemplaza canales sin valor por `SIN_INFORMACION`.
- Aplica los tipos finales indicados en el diccionario.
- Elimina únicamente filas completamente duplicadas; no elijas arbitrariamente
  una versión por identificador.
- Añade `estado_vigencia`: `VIGENTE` si el estado es `ACTIVA` y
  `fecha_inicio <= 2026-09-30 <= fecha_fin`; `NO_VIGENTE` en los demás casos.
  Ambos extremos del intervalo están incluidos.
- Conserva todas las pólizas únicas en la tabla preparada. El filtro de vigencia
  se aplica para el reporte.
- Calcula las primas por moneda. No sumes PEN y USD como si fueran una sola unidad.

## Actividades

| Actividad | Tiempo sugerido | Puntos |
| --- | ---: | ---: |
| 1. Fuente e inspección | 10 min | 8 |
| 2. Preparación | 18 min | 18 |
| 3. Tabla de salida y comprobaciones | 8 min | 10 |
| 4. Reporte | 12 min | 14 |
| 5. Explicación y evidencias | 12 min | 10 |
| Total | 60 min | 60 |

### 1. Fuente e inspección

Carga o identifica la fuente asignada. Muestra una muestra de filas, su cantidad
y su schema. Indica dos problemas de calidad observados y la función de
Workspace, Catalog y compute en tu recorrido.

### 2. Preparación

Aplica las reglas de negocio y construye un resultado con las once columnas
originales más `estado_vigencia`. Usa SQL o PySpark. No es necesario preparar
un pipeline, desarrollar ambas soluciones ni introducir otras entidades.

### 3. Tabla de salida y comprobaciones

Guarda el resultado como tu tabla Delta administrada `polizas_preparadas_e1_<ID>`
en el schema asignado. Comprueba el nombre completo y las columnas en Catalog
Explorer. Registra las filas antes y después de preparar los datos y cuántas
se eliminaron por duplicidad. Comprueba que el canal no tenga valores faltantes
y que prima y fechas tengan los tipos requeridos.

No uses el nombre de las tablas de las sesiones anteriores como destino.

### 4. Reporte

Sobre la tabla preparada, presenta un resumen **solo de pólizas VIGENTE** con:

```text
id_producto
moneda
cantidad_polizas
prima_total
prima_promedio
```

Muestra los importes con dos decimales y ordena por prima total descendente.
Construye una visualización sencilla de `cantidad_polizas` por producto para
**PEN** usando el resultado de tu consulta o notebook; no se exige un dashboard
publicado. Explica qué producto tiene la mayor prima total entre las pólizas
vigentes en PEN y qué significa ese resultado, sin compararlo con USD.

### 5. Explicación y evidencias

Completa `entrega.md` y exporta el código. En 4 a 6 líneas explica por qué elegiste
SQL Editor o notebook, dónde está registrada la tabla y qué cambió respecto de
la arquitectura con origen en S3 si utilizaste el fallback.

## Resultado esperado

Una tabla preparada consultable, un resumen por producto y moneda, una
visualización y una explicación apoyada por evidencia. No se entregan conteos
finales ni resultados numéricos de referencia durante la prueba.

## Validación

- [ ] La fuente tiene las once columnas y puedo mostrar sus tipos y cantidad.
- [ ] La fuente original permanece disponible.
- [ ] Apliqué todas las reglas y revisé los tipos finales.
- [ ] Justifiqué la diferencia entre filas de entrada y salida.
- [ ] Revisé los canales faltantes y los duplicados.
- [ ] Mi reporte usa solo pólizas vigentes y mantiene separadas las monedas.
- [ ] La tabla está en mi nombre de salida asignado y es visible en Catalog.
- [ ] Entregué código, evidencia e interpretación dentro del tiempo.

## Qué cambia en producción

El origen puede estar en S3 con acceso gobernado y roles de IAM. La preparación
se ejecutaría como proceso recurrente con controles y responsables. Aquí se
evalúa un archivo pequeño y una ejecución acotada, sin crear infraestructura.

## Aplicación en el trabajo diario

Puedes reutilizar este flujo para revisar archivos de pólizas recibidos por
Operaciones, corregir categorías inconsistentes, evitar contar filas duplicadas
y presentar primas por producto sin mezclar monedas.

## Extensión opcional

Después del cierre, compara tu preparación con el otro lenguaje. No da puntos
ni consume tiempo de la evaluación.
