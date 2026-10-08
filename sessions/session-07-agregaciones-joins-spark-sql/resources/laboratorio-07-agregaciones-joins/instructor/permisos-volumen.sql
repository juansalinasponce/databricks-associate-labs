-- Preparacion del instructor: sustituir el nombre del grupo de participantes.
-- El volumen debe existir antes de ejecutar estas instrucciones.
GRANT USE CATALOG ON CATALOG workspace TO `<GRUPO_PARTICIPANTES>`;
GRANT USE SCHEMA ON SCHEMA workspace.bronze TO `<GRUPO_PARTICIPANTES>`;
GRANT READ VOLUME, WRITE VOLUME ON VOLUME workspace.bronze.s07_archivos
TO `<GRUPO_PARTICIPANTES>`;

SHOW GRANTS ON VOLUME workspace.bronze.s07_archivos;
