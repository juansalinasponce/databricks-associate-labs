# Cierre del laboratorio — Vista gobernada conectada a Power BI

## Metadata

- Módulo: gobierno de datos, Unity Catalog y consumo analítico.
- Tema: mínimo privilegio y conexión de una vista a Power BI Desktop.
- Tipo: `GUIDED`; cierre formativo del laboratorio 14.
- Duración estimada: 30 minutos, con Power BI Desktop en Windows y las identidades disponibles.
- Nivel: fundamental.
- Modalidad: `PRACTICO_CONDICIONAL`; fallback: demo del instructor y evidencia de SQL.
- Requiere S3: no. Requiere GitHub: solo para descargar los materiales.
- Dataset: seis siniestros ficticios ya cargados; dos filas de resumen Gold.
- Conceptos previos: grupos, vistas, permisos, SQL Warehouse y consultas SQL.

## Contexto de negocio

El analista necesita indicadores de siniestros en Power BI. Operaciones publica
un resumen autorizado; el detalle individual se conserva restringido.

## Objetivo de aprendizaje y qué aprenderás

Conservar lectura únicamente de la vista entre los activos del laboratorio,
probar la identidad consumidora y conectar ese resultado a Power BI Desktop.

```text
juan.salinas@atokongo.com
  → grupo s14_alumno01_analistas
  → CAN USE del SQL Warehouse + permisos de lectura de la vista
  → Power BI Desktop: resumen de siniestros
```

## Escenario y resultado final acordado

| Elemento | Configuración |
| --- | --- |
| Propietario | Cuenta original que creó los objetos; mantiene acceso a Silver |
| Consumidor | `juan.salinas@atokongo.com`, distinto del propietario y sin administración |
| Grupo existente | `s14_alumno01_analistas` |
| Catálogo / schema | `workspace.s14_alumno01_gobierno` |
| Vista autorizada | `gold_siniestros_resumen` |
| Tabla restringida | `silver_siniestros` |
| Datos | Solo `estado_siniestro`, `cantidad_siniestros`, `monto_pagado_total` |
| Herramienta de consumo | Power BI Desktop en Windows, modo Import |
| Final del laboratorio | Vista cargada en Power BI y totales verificados |

El usuario queda en el grupo y conserva la lectura para Power BI. Las pruebas
de retirar integrantes y revocar SELECT pertenecen a los ejercicios anteriores;
si se realizaron, restaura la lectura mínima antes de este cierre. Aquí usamos
el schema **gobierno** existente; no recrees tablas ni vuelvas a cargar datos.

## Requisitos previos

- Usuario asignado al mismo workspace, con acceso a Databricks SQL, al grupo
  indicado y al SQL Warehouse disponible. Agregar una cuenta requiere comprobar
  por separado workspace, datos y compute:
  [administración de usuarios](https://docs.databricks.com/aws/en/admin/users-groups/users).
- Identidad del consumidor sin ownership, administración o permisos amplios
  aportados por otros grupos sobre los activos de la práctica.
- Power BI Desktop actualizado en Windows, confirmado por el docente.
- Autenticación OAuth de Power BI habilitada en el entorno. Se verifica antes
  de la clase; si falta, utilizar la opción B sin sustituir al consumidor por el owner.

## Actividades — Opción A: práctica principal

### 1. Confirmar identidad y grupo — 5 min

Desde la cuenta administradora, abre **Settings → Identity and access → Groups →
Manage → s14_alumno01_analistas → Members** y verifica que esté
`juan.salinas@atokongo.com`. Agrega al usuario existente si aún falta.
La incorporación puede tardar unos minutos en propagarse:
[administración de grupos](https://docs.databricks.com/aws/en/admin/users-groups/manage-groups).

### 2. Dejar únicamente lectura de la vista — 7 min

Abre [04_publicar_vista_powerbi.sql](sql/04_publicar_vista_powerbi.sql).
Ejecuta como propietario las etapas de inspección y ajuste, una a la vez.

- Revisa permisos sobre catálogo, schema, Silver y Gold, y las membresías del usuario.
- Retira SELECT/MODIFY del schema y de Silver que se hayan concedido al grupo
  o directamente al usuario durante el laboratorio.
- Si existe SELECT sobre el catálogo, ALL PRIVILEGES, MANAGE u otra vía amplia,
  corrige su origen. No retires permisos a grupos generales del workspace.
- Si el ejercicio adicional publicó otra vista en `s14_alumno01_grupos`, retira
  su lectura para este grupo si quedó habilitada. Comprueba también concesiones
  directas u otras membresías del usuario sobre los activos del laboratorio.
- Conserva o concede los tres permisos mínimos:

```sql
GRANT USE CATALOG ON CATALOG workspace TO `s14_alumno01_analistas`;
GRANT USE SCHEMA ON SCHEMA workspace.s14_alumno01_gobierno TO `s14_alumno01_analistas`;
GRANT SELECT ON VIEW workspace.s14_alumno01_gobierno.gold_siniestros_resumen TO `s14_alumno01_analistas`;
```

USE CATALOG y USE SCHEMA permiten usar la jerarquía; no conceden lectura de
sus tablas por sí solos. Con un SQL Warehouse, el owner de la vista conserva
los permisos sobre Silver y el consumidor necesita SELECT en la vista, sin
necesitar SELECT en la tabla subyacente:
[permisos de las vistas](https://docs.databricks.com/aws/en/views/#requirements-for-querying-views).

Si ves nombres de otros objetos en un navegador, eso no demuestra lectura.
El alcance de esta práctica son sus datos; los catálogos públicos o de sistema
se administran por separado. Valida consultas reales para comprobar el acceso.

### 3. Habilitar el uso del SQL Warehouse — 3 min

En **SQL Warehouses**, localiza el existente, abre su menú **Permissions** y
concede **CAN USE** al grupo `s14_alumno01_analistas`. Revisa que el consumidor
no reciba permisos de administración sobre el warehouse por otra vía.
Este permiso habilita consultas; Unity Catalog sigue controlando qué datos lee:
[permisos de SQL Warehouses](https://docs.databricks.com/aws/en/security/auth/access-control#sql-warehouse-acls).

Abre el warehouse → **Connection details** y copia:

- **Server hostname**, solo el host.
- **HTTP Path**, la ruta de conexión del warehouse.

Usa los valores reales de esa pantalla, sin construir la ruta a partir del nombre.
No necesitas otro warehouse, un clúster clásico ni configurar S3.

### 4. Validar desde la sesión de Juan — 5 min

Abre otro perfil de navegador y entra al mismo workspace como
`juan.salinas@atokongo.com`. En SQL Editor, selecciona el warehouse y ejecuta:

```sql
SELECT current_user() AS usuario,
       lower(current_user()) = 'juan.salinas@atokongo.com' AS identidad_esperada,
       is_account_group_member('s14_alumno01_analistas') AS pertenece_al_grupo;
```

Las dos comprobaciones deben ser true. Ejecuta cada consulta siguiente por separado:

```sql
SELECT * FROM workspace.s14_alumno01_gobierno.gold_siniestros_resumen
ORDER BY estado_siniestro;
```

```sql
SELECT * FROM workspace.s14_alumno01_gobierno.silver_siniestros;
```

Gold debe devolver dos filas y Silver debe quedar sin acceso. Un error de
sintaxis o compute no acredita aislamiento. Si Silver devuelve datos, corrige
la concesión excesiva antes de conectar Power BI.

### 5. Conectar Power BI Desktop — 8 min

1. En **Obtener datos**, busca el conector **Databricks** para AWS con OAuth.
2. Introduce **Server hostname** y **HTTP Path** del warehouse. En opciones
   avanzadas puedes indicar catálogo `workspace` y base/schema
   `s14_alumno01_gobierno`.
3. Selecciona **Importar / Import** para las dos filas de este laboratorio.
4. Elige **OAuth / OAuth (OIDC)** e inicia sesión como
   **juan.salinas@atokongo.com** en la ventana de autenticación de Databricks.
   La cuenta con la que abriste Power BI no determina por sí sola qué identidad
   usa su conexión a Databricks. Comprueba el correo en la autenticación.
5. En el navegador de datos, selecciona únicamente
   `workspace → s14_alumno01_gobierno → gold_siniestros_resumen` y pulsa **Cargar**.
6. Presenta las tres columnas en un visual de tabla y verifica los resultados.

Conector, campos y credenciales:
[conector Databricks de Power Query](https://learn.microsoft.com/en-us/power-query/connectors/databricks).
No utilices la autenticación Microsoft Entra ID del conector Azure Databricks
para este workspace AWS; usa el flujo OAuth del conector Databricks.

Si Power BI reutiliza credenciales anteriores, abre **Archivo → Opciones y
configuración → Configuración de origen de datos**, selecciona este origen y
edita o borra sus credenciales para autenticarte como Juan:
[administrar autenticación del origen](https://learn.microsoft.com/en-us/power-query/connector-authentication).

Si el navegador no lista la vista aunque la consulta SQL funcione, utiliza
la opción **Native query / Consulta nativa**, si aparece, con catálogo y schema
configurados y esta consulta:

```sql
SELECT estado_siniestro, cantidad_siniestros, monto_pagado_total
FROM workspace.s14_alumno01_gobierno.gold_siniestros_resumen
```

No amplíes SELECT a Silver para resolver un problema de navegación. Las consultas
nativas están documentadas en
[Power BI Desktop con Databricks](https://docs.databricks.com/aws/en/partners/bi/power-bi/desktop#native-sql-queries).

### 6. Cierre y evidencias — 2 min

| estado_siniestro | cantidad_siniestros | monto_pagado_total |
| --- | ---: | ---: |
| ABIERTO | 3 | 300.00 |
| CERRADO | 3 | 2700.00 |
| Total | 6 | 3000.00 |

El total corresponde a sumar las dos filas, en PEN. Entrega evidencia de la
identidad de Juan, lectura Gold, denegación Silver y tabla cargada en Power BI.
Registra el estado final en [EVIDENCIAS.md](EVIDENCIAS.md).

**Aquí termina el laboratorio:** conexión realizada con la identidad autorizada,
resumen verificable en Power BI y permisos de lectura de la vista conservados.

## Opción B — fallback para Free Edition

Si fallan cuota, conector u OAuth, el instructor demuestra la conexión en un
entorno habilitado. El participante conserva las pruebas SQL de identidad,
lectura y denegación y registra que Power BI quedó como demo o pendiente.
Una exportación CSV no valida una conexión autenticada a Databricks.
No uses credenciales del propietario como sustituto ni pegues secretos en notebooks.
Las restricciones del entorno se revisan antes de la sesión:
[limitaciones de Free Edition](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations).

## Resultado esperado y validación

El usuario pertenece al grupo, tiene CAN USE del warehouse y lectura de la
vista del laboratorio; no puede leer Silver ni recibe permisos de escritura
sobre sus activos. Los permisos no se revocan después de cargar Power BI.
La guía prepara los pasos; no confirma su aplicación real en el workspace.

## Qué cambia en producción

Se definen identidad de actualización y permisos de distribución del reporte.
En Import, Power BI almacena una copia: retirar SELECT en Databricks impide
nuevas lecturas con esa identidad, pero no elimina automáticamente los datos
ya importados. El acceso al reporte también se gobierna en Power BI:
[modos de conexión y actualización](https://learn.microsoft.com/en-us/power-bi/connect-data/refresh-data).
Publicación y actualización programada quedan fuera de este cierre solicitado.

## Aplicación en el trabajo diario

Puedes publicar indicadores de siniestros como una vista reutilizable y dar
acceso al equipo BI mediante un grupo, manteniendo reservado el detalle.
La identidad usada para obtener los datos debe verificarse en cada conexión.

## Extensión opcional

No se requiere extensión para completar el laboratorio. Una práctica posterior
puede comparar Import y DirectQuery utilizando la misma vista autorizada.

Documentación consultada el **4 de noviembre de 2026**. Las pruebas de permisos
y conexión deben ejecutarse con las identidades y el warehouse del entorno.
