# S14-G01 — Acceso a indicadores mediante un grupo

## Metadata

- Módulo: gobierno de datos y Unity Catalog; complemento solicitado para la sesión 14.
- Tema: permisos recibidos por pertenencia a un grupo.
- Tipo: `GUIDED` + `PRACTICE`, sin calificación oficial.
- Duración estimada: 30 minutos, con usuarios y compute preparados previamente.
- Nivel: fundamental.
- Modalidad: `PRACTICO_CONDICIONAL`; alternativa `DEMO_INSTRUCTOR` / `CONCEPTUAL`.
- Requiere S3: no. Requiere GitHub: solo para descargar materiales.
- Dataset: seis siniestros sintéticos del laboratorio 14.
- Conceptos previos: SELECT, vista, USE CATALOG, USE SCHEMA, GRANT y REVOKE.

## Contexto de negocio

Dos analistas de una aseguradora ficticia necesitan indicadores de siniestros.
Al incorporarse al equipo reciben acceso al resumen; al salir del equipo lo
pierden. Operaciones quiere administrar una concesión al equipo y mantener su
lista de integrantes.

## Objetivo de aprendizaje

Conceder lectura a un grupo y comprobar cómo cambia el acceso al agregar o
retirar integrantes. Comparar ese cambio con revocar el permiso del grupo.

## Qué aprenderás

```text
Ana y Luis → integrantes del grupo → permisos del grupo → vista Gold
```

Para Unity Catalog utiliza un **grupo de cuenta**, incluido uno aprovisionado
desde el proveedor de identidad. Un grupo local heredado del workspace no
puede recibir permisos sobre datos de Unity Catalog. Consulta los
[tipos de grupos](https://docs.databricks.com/aws/en/admin/users-groups/groups).

## Requisitos previos

- Un administrador autorizado para crear un grupo y cambiar sus integrantes.
  Ser propietario de una tabla no concede esa administración de identidades.
- El propietario de los activos del laboratorio y dos usuarios de prueba
  existentes, llamados **Ana** y **Luis** en esta guía. Sustituye esos nombres
  por participantes del entorno; no necesitas crear cuentas con esos nombres.
- Los analistas acceden al mismo workspace y pueden usar SQL Editor y el
  SQL Warehouse por una asignación independiente del grupo del ejercicio.
  Así, retirar un integrante permite comprobar datos sin perder la sesión completa.
- Ningún analista es administrador, propietario ni recibe SELECT amplio desde
  el catálogo. Tampoco utiliza roles asumidos que aporten acceso adicional.
- El propietario puede crear un schema nuevo en un catálogo autorizado y
  consultar `workspace.s14_alumno01_gobierno.silver_siniestros`.
- Cambia `workspace` y `alumno01` en toda la guía y el SQL según tu entorno.

**Con dos identidades en total** (propietario y un analista), puedes realizar
el mismo ciclo sin Luis; quedará pendiente observar el efecto simultáneo sobre
dos integrantes. Con una sola identidad usa la opción B.

## Dataset

Se reutiliza Silver del laboratorio principal, sin volver a insertar datos.
Si todavía no existe, ejecuta una sola vez el
[setup original](sql/00_preparar_datos.sql).

El [SQL de este ejercicio](sql/03_grupos.sql) crea un schema exclusivo
`s14_alumno01_grupos` y una vista de resumen que referencia Silver. Esto separa
las concesiones de las realizadas previamente en el schema `gobierno`.

## Escenario

| Elemento | Nombre de ejemplo |
| --- | --- |
| Grupo de cuenta del laboratorio | `s14_alumno01_analistas` |
| Schema nuevo | `workspace.s14_alumno01_grupos` |
| Vista publicada | `workspace.s14_alumno01_grupos.gold_siniestros_resumen` |
| Integrantes de prueba | Ana y Luis, usuarios existentes sin permisos administrativos |

## Actividades

## Opción A — práctica principal

### 1. Preparar el grupo y agregar a Ana — 5 min

Usa **el mismo grupo del laboratorio principal**, `s14_alumno01_analistas`.
Si ya lo creaste, ábrelo y revisa sus integrantes; no crees otro grupo.
El nombre debe coincidir en todos los GRANT, REVOKE y consultas de membresía.

**Administrador de identidades:** en un workspace con federación de identidades
y controles habilitados, abre **Settings → Identity and access → Groups → Manage**.
Si todavía no existe, usa **Add Group → Add new** para crear `s14_alumno01_analistas`.
Como alternativa, un administrador de cuenta puede usar **Account Console →
User management → Groups → Add group**.

En el grupo, abre **Members → Add members** y agrega solo a Ana. Verifica que
el origen del grupo sea **Account** y que esté disponible en el workspace.
Estas rutas se basan en [administración de grupos](https://docs.databricks.com/aws/en/admin/users-groups/manage-groups).

Utiliza un grupo dedicado al laboratorio. Si ya recibió permisos en el schema
`gobierno`, esos permisos se conservan; este ejercicio prueba otra vista en el
schema nuevo `grupos`. Comprueba que no tenga SELECT previo sobre la nueva vista
ni heredado de su schema o catálogo. No utilices un grupo general del workspace.
No necesitas conceder a los analistas la capacidad de administrar el grupo ni
asignarles el rol de administrador.

### 2. Preparar una vista y comprobar el estado inicial — 5 min

**Propietario:** ejecuta únicamente las etapas **0 y 1** de
[03_grupos.sql](sql/03_grupos.sql). Si el schema ya existe, elige otro sufijo.
No ejecutes todo el archivo: cada etapa requiere una comprobación intermedia.

**Ana y Luis**, cada uno desde su propia sesión, ejecutan:

```sql
SELECT current_user() AS usuario,
       is_account_group_member('s14_alumno01_analistas') AS pertenece_al_grupo;
```

Ana debería obtener `true` y Luis `false`. La pertenencia al grupo todavía no
concede lectura: ambos prueban la vista y deben quedar sin acceso.

```sql
SELECT *
FROM workspace.s14_alumno01_grupos.gold_siniestros_resumen
ORDER BY estado_siniestro;
```

Si la vista ya se puede leer, revisa la identidad, grupos y concesiones de los
padres antes de continuar. No retires permisos generales del entorno.

### 3. Conceder permisos una sola vez al grupo — 5 min

**Propietario o administrador de permisos:** ejecuta la etapa **2**. Necesitas
autoridad sobre cada objeto; omite la concesión de USE CATALOG si ya existe.

```sql
GRANT USE CATALOG ON CATALOG workspace TO `s14_alumno01_analistas`;
GRANT USE SCHEMA ON SCHEMA workspace.s14_alumno01_grupos TO `s14_alumno01_analistas`;
GRANT SELECT ON VIEW workspace.s14_alumno01_grupos.gold_siniestros_resumen TO `s14_alumno01_analistas`;
```

En **Catalog → vista → Permissions**, confirma que el destinatario del SELECT
sea el grupo. También puedes concederlo desde **Grant**, seleccionando ese
grupo. La administración de privilegios admite grupos como principales:
[referencia de GRANT y REVOKE](https://docs.databricks.com/aws/en/data-governance/unity-catalog/manage-privileges).

**Ana:** consulta la vista; debe ver dos filas. **Luis:** repite la consulta;
debe continuar sin acceso. No se concede SELECT directamente a ninguno.

### 4. Incorporar y retirar integrantes — 7 min

**Administrador de identidades:** agrega a Luis en **Members**. No ejecutes
otro GRANT. Luis comprueba su membresía y vuelve a consultar; ahora debe leer.

Después, retira **solo la membresía de Ana en este grupo** desde la lista de
integrantes. Conserva su cuenta y su asignación independiente al workspace.
Ana vuelve a comprobar pertenencia y consulta; debe perder la lectura. Luis
continúa consultando. La etapa **3** del SQL contiene estas instrucciones.

Los cambios de membresía pueden tardar unos minutos en propagarse. Actualiza
la comprobación y vuelve a ejecutar SQL; si la membresía todavía no refleja
el cambio, no atribuyas el resultado al permiso de la vista.

**Propietario:** ejecuta SHOW GRANTS de la etapa 3. El permiso del grupo sigue
presente aunque Ana ya no pertenezca a él. No se necesitó un REVOKE por usuario.

### 5. Revocar el acceso del equipo — 5 min

**Propietario:** ejecuta la etapa **4**:

```sql
REVOKE SELECT ON VIEW workspace.s14_alumno01_grupos.gold_siniestros_resumen FROM `s14_alumno01_analistas`;
```

Luis sigue siendo integrante del grupo, pero ya no puede consultar el resumen.
Ana tampoco puede hacerlo. Conserva los permisos de uso de los padres para
aislar el efecto del SELECT.

### 6. Registrar la decisión — 3 min

Guarda la consulta, `current_user()`, pertenencia al grupo y resultado observado.
Un error de compute o sintaxis no demuestra una denegación de datos.

| Fase | Ana pertenece | Luis pertenece | Ana lee | Luis lee |
| --- | --- | --- | --- | --- |
| Grupo creado, sin SELECT | Sí | No | No | No |
| SELECT concedido al grupo | Sí | No | Sí | No |
| Luis incorporado | Sí | Sí | Sí | Sí |
| Ana retirada | No | Sí | No | Sí |
| SELECT revocado al grupo | No | Sí | No | No |

## Opción B — fallback para Free Edition

Si no aparecen las opciones de administración de grupos o falta otro usuario:

1. Crea la vista de la etapa 1 en un schema propio si tienes permisos.
2. Dibuja Ana → grupo → vista y Luis fuera del grupo.
3. Predice cada fila de la matriz antes de comparar con los resultados esperados.
4. Escribe cuál cambio afecta a una persona y cuál afecta a todo el equipo.
5. Observa la demo del instructor si dispone de un entorno habilitado.

Marca el resultado como **simulación** o **demo**, según lo realizado. No
ejecutes GRANT hacia un grupo inexistente ni pruebes la pérdida de acceso con
el propietario. Free Edition no ofrece Account Console; las capacidades de tu
workspace deben comprobarse, según sus
[limitaciones oficiales](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations).

## Resultado esperado

Los integrantes acceden mediante el permiso del grupo. Al consultar obtienen
ABIERTO = 3 / 300.00 y CERRADO = 3 / 2700.00, en PEN, si mantienen el dataset
original. El final del ejercicio deja al grupo sin SELECT sobre esta vista.

## Validación

El instructor comprueba tres evidencias: Luis empieza a leer al incorporarse
sin un GRANT adicional; Ana deja de leer al retirarse mientras Luis conserva
acceso; al revocar SELECT del grupo, Luis pierde la lectura pese a seguir siendo
integrante. Cualquier acceso por otras vías debe registrarse e investigarse.

| Situación | Qué revisar |
| --- | --- |
| No aparece el grupo en Catalog | Origen Account, asignación al entorno y permisos del administrador |
| Ana sigue leyendo tras retirarla | Propagación, concesiones individuales, otros grupos, padres y ownership |
| Luis pierde acceso a todo el workspace | Su acceso al workspace dependía solo de ese grupo; preparar asignación independiente |
| Se intenta CREATE GROUP desde SQL | Administrar el grupo mediante los controles de identidades de esta guía; GRANT no crea grupos |

## Qué cambia en producción

Los grupos pueden venir del proveedor corporativo de identidades. La membresía
de esos grupos se mantiene en su sistema de origen, con responsables y procesos
de alta y baja. Administrar integrantes y conceder permisos sobre datos son
responsabilidades diferentes. La revisión de acceso considera todas sus vías.

## Aplicación en el trabajo diario

Al incorporar analistas a un equipo de siniestros, puedes agregarlos al grupo
autorizado en vez de repetir concesiones sobre cada vista. Cuando alguien cambia
de función, actualizas su membresía y compruebas el acceso que conserva por
otros grupos o concesiones directas.

## Extensión opcional

Si además necesitas column masking, puedes definir una función que consulte
`is_account_group_member('nombre_del_grupo_autorizado')` para decidir si devuelve
el documento o asteriscos. Diseña un grupo distinto para ver documentos:
**pertenecer al equipo de indicadores no implica necesitar datos identificables**.
El usuario necesita permiso de lectura y una regla de máscara adecuada;
ambos controles cumplen funciones diferentes.

Documentación consultada el **4 de noviembre de 2026**. SQL y rutas preparados
para revisión; la autorización real requiere validación en el workspace.
