# Sesión 14 — Unity Catalog y gobierno de datos

Laboratorio guiado basado en las **11 diapositivas** de
`Sesion14_Unity_Catalog_Gobierno_de_datos.pptx`, incluidas las láminas incrustadas
como imágenes.

- [Laboratorio: permisos, revocación y gobierno paso a paso](resources/laboratorio-14-gobierno/README.md).
- [Ejercicio de grupos: agregar integrantes, conceder y revocar](resources/laboratorio-14-gobierno/GRUPOS.md).
- [Descargar el laboratorio completo en ZIP](resources/laboratorio-14-gobierno.zip).
- [SQL de preparación](resources/laboratorio-14-gobierno/sql/00_preparar_datos.sql).
- [SQL del instructor: conceder, revocar y revisar herencia](resources/laboratorio-14-gobierno/sql/01_administrar_permisos.sql).
- [Consultas del analista para comprobar el acceso](resources/laboratorio-14-gobierno/sql/02_validar_analista.sql).
- [Plantilla de evidencias](resources/laboratorio-14-gobierno/EVIDENCIAS.md).
- [Guía del instructor y resultados esperados](resources/laboratorio-14-gobierno/INSTRUCTOR.md).

## Relación con la PPT

| Diapositiva | Aplicación en el laboratorio |
| --- | --- |
| 1–2 | Presentación y evaluaciones; esta práctica es formativa, sin peso adicional. |
| 3 | Acceso, descubrimiento y trazabilidad como necesidades de gobierno. |
| 4 | Recorrido Catalog → Schema → Table / View; Volume en la extensión. |
| 5 | Propietario y analista separados; grupo de cuenta cuando esté habilitado. Service Principal como identidad de automatización conceptual. |
| 6 | Matriz de acceso y pruebas de lectura y escritura. |
| 7 | Cadena S3 → Storage Credential → External Location → objeto, mediante decisión de arquitectura. |
| 8 | Extensión con Volumes administrados DEV/PRD. |
| 9 | `USE CATALOG`, `USE SCHEMA`, `SELECT` y herencia. |
| 10 | Ciclo `SHOW GRANTS` → `GRANT` → consulta real → `REVOKE` → consulta real. |
| 11 | Comments, tags, owner y lineage desde Catalog Explorer. |

## Precisiones para explicar la PPT

- Una ruta `/Volumes/<catalog>/<schema>/<volume>/` puede corresponder a un
  volumen administrado o externo. La ruta no demuestra conexión a un bucket
  propio. El laboratorio usa almacenamiento administrado.
- Los nombres DEV/PRD organizan recursos; el aislamiento requiere permisos y,
  en producción, las fronteras que defina la arquitectura.
- Unity Catalog gobierna accesos realizados mediante sus objetos. Los accesos
  directos a S3 también deben restringirse mediante IAM y políticas del bucket.
- Quitar un permiso directo no elimina accesos recibidos por grupos o herencia.
  El propietario no sirve como usuario de prueba de una revocación de lectura.

**Ajuste de alcance:** `Docs/cronograma.md` y `Docs/syllabus.md` ubican gobierno
en la sesión 13 y organización/Git en la 14. Este material sigue la solicitud
explícita del docente y la PPT utilizada para la sesión 14, continuando el
criterio documentado en la sesión 13. No cambia el cronograma ni las evaluaciones.

Las capacidades se contrastaron con documentación oficial el **4 de noviembre
de 2026**; las fuentes están enlazadas en el laboratorio. No se ha ejecutado
contra un workspace Databricks desde este repositorio.
