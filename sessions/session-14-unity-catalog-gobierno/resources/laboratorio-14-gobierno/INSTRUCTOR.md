# Guía del instructor — Laboratorio 14

El complemento [S14-G01 — Grupos](GRUPOS.md) incorpora creación del grupo,
altas y bajas de integrantes y revocación para el equipo, con
[SQL separado](sql/03_grupos.sql). Prepara acceso al workspace y compute
independiente del grupo para que las bajas permitan seguir probando consultas.

## Preparación antes de la clase

Reserva 70 minutos para el laboratorio. La extensión de Volumes añade 15
minutos si el ritmo de la sesión lo permite. La preparación de identidades y
permisos iniciales se realiza antes de la clase, fuera de esos tiempos.

1. Confirma catálogo, SQL Warehouse disponible y creación de objetos administrados.
2. Usa dos identidades del mismo entorno. La segunda debe poder ejecutar SQL
   y carecer de ownership o administración sobre los destinos de la práctica.
3. En un entorno con administración de cuenta habilitada, un administrador
   prepara un grupo de cuenta exclusivo `s14_<identificador>_analistas`, agrega
   al usuario analista y le permite acceder al workspace. Puede usar
   **Account Console → User management → Groups** si esa ruta está disponible.
   Comprueba en el selector de principales de Catalog que el grupo sea utilizable.
4. Si no puedes preparar un grupo, usa directamente un usuario ya presente y
   reemplaza el nombre del grupo en todo el SQL por su identificador entre
   backticks. Explica que el patrón por grupos evita mantener concesiones individuales.
5. En Free Edition no presupongas acceso a Account Console ni grupos de cuenta.
   Si no tienes segundo usuario apto, selecciona la opción B y anuncia qué se simulará.
6. Revisa grupos del analista y concesiones sobre catálogo y padres. No basta
   con que el grupo del laboratorio esté vacío de permisos: puede haber otras vías.
7. Comprueba el ciclo completo en un schema de ensayo propio antes de distribuirlo.
   No uses `default` ni cambies privilegios de `users` / `account users` para la demo.
8. Prepara capturas de B, C y E para el fallback si cuentas con un entorno habilitado.

Una segunda pestaña con el mismo usuario no es una segunda identidad. Dos
cuentas personales en workspaces distintos tampoco permiten esta validación.

## Guion de facilitación

| Minutos | Actividad | Frase o pregunta de apoyo |
| --- | --- | --- |
| 0–5 | Roles y matriz | «¿El analista necesita el documento o solo el indicador?» |
| 5–15 | Setup y navegación | «¿Qué objeto contiene los datos y cuál publica su resumen?» |
| 15–30 | Concesión y pruebas B | «¿Qué falta si solo concedo SELECT sin uso de padres?» |
| 30–40 | Revocación C | «Volvamos a ejecutar con la identidad del consumidor.» |
| 40–50 | Herencia D–G | «¿De dónde viene ahora el acceso que sigue funcionando?» |
| 50–65 | Contexto y lineage | «¿Quién aprueba el uso y qué se afecta si cambio monto_pagado?» |
| 65–70 | Evidencias y transferencia | «¿Qué acceso temporal retiramos?» |

En SQL Editor selecciona y ejecuta una sentencia o etapa a la vez. Al importar
los archivos como notebooks SQL, conserva las celdas `-- COMMAND ----------`.
**No ejecutar todo** en el administrador o el analista: se perderían los estados
intermedios y los errores esperados detendrían la secuencia.

## Solución y comprobaciones

- Datos: seis filas, total pagado **3000.00 PEN**.
- Vista: ABIERTO = 3 / 300.00; CERRADO = 3 / 2700.00.
- En A no hay acceso del analista; en B puede consultar solo Gold.
- C retira el SELECT de la vista; conserva los privilegios de uso para aislar la causa.
- D concede SELECT al schema y a la tabla; E elimina el directo, pero sigue
  el heredado. F retira SELECT del padre; G restaura únicamente Gold.
- UPDATE debe fallar siempre. La sentencia se asigna el mismo monto para no
  alterar el dato ante un permiso excesivo; si tiene éxito, el control falla.
- En producción no se debería conceder SELECT amplio a un schema con detalle
  restringido para este perfil. D existe para mostrar su efecto con datos ficticios.

Matriz de negocio: analista, lectura de Gold; ingeniero, lectura y modificación
de Silver existente; auditor, lectura o metadata de los activos autorizados
según la revisión acordada. No requiere conceder permisos a los tres perfiles.

El owner técnico es el principal que muestra Databricks. Data Owner, Steward y
Custodian son responsabilidades de gobierno que no se crean por escribir un
comentario. Un comentario documenta la decisión y un GRANT implementa acceso.

## Errores frecuentes y respuesta

| Síntoma | Investigación o ajuste |
| --- | --- |
| Error de sintaxis al final de `COMMENT ON ... IS` | Ejecutar el comando completo con el texto entre comillas y punto y coma. Para comentar la vista usar `COMMENT ON TABLE nombre_vista IS 'texto';`. |
| El grupo no aparece / principal inexistente | Verificar provisión e identidad de cuenta; usar usuario existente o fallback. GRANT no crea identidades. |
| No puedo conceder USE CATALOG | El creador del schema no administra necesariamente el catálogo; pedir al responsable la preparación o usar un catálogo autorizado. |
| SELECT concedido y consulta falla | Revisar padres y compute; en una vista también verificar permisos de su propietario sobre Silver. |
| Sigue leyendo después de C o F | Confirmar `current_user()`, padres, grupos, permisos amplios y ownership; no retirar permisos generales del workspace. |
| SHOW GRANTS no muestra todos los permisos | Ejecutar como propietario/administrador autorizado y revisar Catalog. La visibilidad depende de permisos. |
| UPDATE tiene éxito | Hay privilegios de escritura por alguna vía; registrar control fallido y revisar con el responsable. |
| Tag no se aplica | Revisar ownership/APPLY TAG y ASSIGN si es gobernado; registrar clasificación propuesta. |
| No aparece lineage | Confirmar ejecución SQL, permisos y rango temporal; usar diagrama etiquetado como tal. |
| Solo está el usuario creador | Usar opción B; revocarse SELECT a sí mismo no elimina su ownership. |
| Cambié una variable Python a «analista» | No cambia la identidad autenticada; no representa una prueba de autorización. |
| El setup se ejecutó dos veces parcialmente | No repetir INSERT. Verificar conteo y continuar la celda pendiente o elegir schema nuevo. |

## Aclaración sobre DENY

No utilizar `DENY SELECT ON TABLE ...` como remedio para la herencia en Unity
Catalog: la [sentencia DENY tradicional](https://docs.databricks.com/aws/en/sql/language-manual/security-deny)
corresponde al Hive metastore. Unity Catalog dispone además de
[políticas ABAC DENY en Beta](https://docs.databricks.com/aws/en/data-governance/unity-catalog/abac/deny-policies)
con alcance y requisitos específicos; no equivalen a ese comando y quedan fuera
del laboratorio. Aquí se retira la concesión donde se originó.

## Revisión formativa

No añade evaluación oficial. Marca logrado / por reforzar / no ejecutable por entorno:

- Identifica catálogo, schema, tabla, vista y principal.
- Propone mínimo privilegio para el consumidor.
- Distingue una consulta autorizada de una modificación no permitida.
- Comprueba una revocación desde otra identidad o explica que solo fue simulada.
- Explica el acceso heredado y retira el permiso desde su origen.
- Documenta responsable, propósito y clasificación; interpreta el lineage.

No marcar «revocación real lograda» basándose solo en SHOW GRANTS o en una
predicción. Registrar qué comportamiento fue observado.

## Retiro de accesos al terminar

El final G mantiene lectura del resumen para reutilizarlo. Si el grupo era
temporal y ya no lo necesita, el propietario puede retirar solo sus concesiones
creadas durante esta práctica, después de guardar las evidencias:

```sql
REVOKE SELECT ON VIEW workspace.s14_alumno01_gobierno.gold_siniestros_resumen
FROM `s14_alumno01_analistas`;
REVOKE USE SCHEMA ON SCHEMA workspace.s14_alumno01_gobierno
FROM `s14_alumno01_analistas`;
```

Si se realizó la extensión, comprobar que READ VOLUME de DEV ya se revocó y
retirar el USE SCHEMA de DEV concedido al grupo de la práctica si dejó de requerirse.
No se revoca USE CATALOG automáticamente: puede ser previo o compartido con
otros ejercicios. Comparar con la línea base y coordinar cualquier retiro.
No es necesario eliminar tablas, schemas, volúmenes ni identidades para completar
el aprendizaje. Mantener las evidencias y aplicar la política de retención del curso.

## Alcance de la verificación del material

Se revisaron las 11 diapositivas y las referencias oficiales enlazadas en la
guía, con fecha de consulta 4 de noviembre de 2026. Los conteos y agregados se
pueden verificar localmente; las pruebas de autorización requieren ejecución
con identidades distintas en Databricks. El material no incorpora credenciales
ni depende de datos o arquitectura real del cliente.
