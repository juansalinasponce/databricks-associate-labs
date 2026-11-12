# Sesión 16 — Matrícula de un Data Product, Genie y dashboard

Un solo Data Product de referencia: **`DP-SEG-016` — `dp_siniestros_operativos`**.
Su proceso de publicación se identifica como `PRC-SEG-016`. El Excel registra
la ficha, el proceso, los ambientes y un modelo de datos pequeño para consultas.

- [Excel de matrícula](resources/laboratorio-16-data-product/matricula-data-product.xlsx).
- [Guía del laboratorio y orden de ejecución](resources/laboratorio-16-data-product/README.md).
- [Configurar Genie y validar preguntas](resources/laboratorio-16-data-product/GENIE.md).
- [Construir el dashboard](resources/laboratorio-16-data-product/DASHBOARD.md).
- [Paquete descargable](resources/laboratorio-16-data-product.zip).

El código del producto permanece igual en `DEV`, `TEST`, `UAT` y `PRD`.
El ambiente determina el catálogo de destino y los nombres de los activos.
La referencia ejecutable es **`DEV → workspace.s16`**. Los otros ambientes
figuran en la plantilla y se habilitan únicamente cuando exista su catálogo.

Las nueve tablas se crean y cargan como **tablas Delta administradas en Unity
Catalog**, bajo `workspace.s16`. El Excel documenta y suministra los valores;
Genie y el dashboard consultan las tablas y vistas registradas en ese catálogo.
Después de ejecutar los SQL `00`–`02`, utiliza
[06-verificar-catalog.sql](resources/laboratorio-16-data-product/sql/06-verificar-catalog.sql)
y revisa **Catalog → workspace → s16**.

## Objetivos

1. Documentar un Data Product y distinguir código, versión, ambiente y objeto.
2. Identificar dimensiones, hechos y sus siete relaciones.
3. Configurar preguntas de Genie y contrastar el SQL con resultados conocidos.
4. Reutilizar una vista de indicadores en un AI/BI Dashboard.

## Organización de los 120 minutos

| Bloque | Minutos | Resultado |
| --- | ---: | --- |
| Conceptos y recorrido de las láminas | 25 | Distinguir Data Product, Genie, dashboard y gobierno |
| Revisar matrícula, proceso y ambientes | 15 | Excel completado con un único código |
| Demo de publicación y relaciones | 20 | Schema `s16`, dimensiones, hechos y vistas |
| Configurar Genie y validar consultas | 25 | Dos respuestas contrastadas con SQL |
| Crear dashboard y probar filtros | 25 | KPIs, gráficos y filtro comprobados |
| Evidencias y aplicación diaria | 10 | Decisión justificada del canal de consumo |

El instructor lleva la exportación preparada. Los participantes no necesitan
instalar Python ni librerías para ejecutar los SQL incluidos.

## Revisión de la presentación existente

Se revisaron las diez diapositivas de
`Sesion16_genie + AI_BI Dashboards.pptx`, incluidas las imágenes que contienen
el texto. Las láminas 3–5 explican Genie, su flujo y su comparación con
dashboard; las 6–7 describen el Data Product y su contrato; la 8 presenta
Data Mesh; las 9–10 conectan disponibilización y arquitectura de consumo.

La frase de ejemplo «¿cuántos siniestros se cerraron este mes?» requiere fechas
de cierre. Este dataset solo contiene mes de reporte y estado al corte: se
usará «¿cuántos de los reportados en enero de 2025 están cerrados al corte?».
Esta distinción forma parte de la validación humana de Genie.

`Docs/cronograma.md` y `Docs/syllabus.md` ubican Genie en la Sesión 16 y la
formalización de Data Products en la 17. Por solicitud expresa del docente,
este material incorpora una matrícula de referencia y el modelo dimensional
para acompañar la PPT existente. No cambia el cronograma ni las evaluaciones.
La PPT se conserva sin modificaciones.

## Validación técnica

Desde la raíz, con openpyxl, PySpark y Java compatibles:

```bash
python3 scripts/validation/validar-sesion-16.py
```

El validador comprueba el Excel, su correspondencia con los CSV/SQL,
selección de ambiente, integridad de relaciones, KPIs, filtros y recarga.
Ejecuta el SQL con Spark local usando Parquet en lugar de Delta.
Unity Catalog, sus restricciones, Genie y el dashboard se comprueban en el
workspace de la clase. Fuentes de plataforma verificadas el 11/11/2026.
