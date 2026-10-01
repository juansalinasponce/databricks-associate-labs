# 00 — Carga manual del CSV en Amazon S3

## Archivo que se debe cargar

```text
data/polizas_10000.csv
```

El archivo contiene 10,000 registros sintéticos de pólizas. No contiene datos
reales ni credenciales.

## Opción 1 — Consola de Amazon S3

1. Ingrese al bucket autorizado para la capacitación.
2. Cree o abra el prefijo `landing/polizas/`.
3. Seleccione **Upload** y cargue `polizas_10000.csv`.
4. Compruebe que el objeto final sea:

   ```text
   s3://<S3_BUCKET>/landing/polizas/polizas_10000.csv
   ```

## Opción 2 — AWS CloudShell o AWS CLI

Ejecute el comando desde el directorio del laboratorio:

```bash
aws s3 cp data/polizas_10000.csv \
  s3://<S3_BUCKET>/landing/polizas/polizas_10000.csv
```

Verifique el objeto sin descargarlo:

```bash
aws s3 ls s3://<S3_BUCKET>/landing/polizas/
```

## Verificación posterior de la tabla Delta

Después de ejecutar el ETL, liste la salida:

```bash
aws s3 ls s3://<S3_BUCKET>/bronze/polizas_delta/ --recursive
```

La salida debe incluir archivos similares a:

```text
bronze/polizas_delta/_delta_log/00000000000000000000.json
bronze/polizas_delta/part-00000-....snappy.parquet
```

`_delta_log` contiene el registro transaccional de Delta. Los archivos
`part-*.parquet` contienen los datos de la tabla.

## Seguridad

- Use solamente el bucket o prefijo asignado por el instructor.
- No copie credenciales AWS dentro de un notebook.
- No publique nombres de cuenta, roles o rutas privadas en GitHub.
- Solicite únicamente permisos sobre `landing/polizas/` y
  `bronze/polizas_delta/`.
