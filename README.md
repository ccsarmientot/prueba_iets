# Proyecto de Gestión y Análisis de Datos CSV a SQLite

Este proyecto tiene como objetivo gestionar archivos CSV, convertirlos a bases de datos SQLite, realizar transformaciones y preprocesamiento con SQL, y finalmente guardar los datos limpios para crear visualizaciones. El objetivo de negocio es poder realizar la verificación de cantidades de sedes con especificidades **Oncológicas** y de **Transplante renal** con respecto a la población que tienen distintos municipios, departamentos y regiones.

## Estructura del Proyecto

-   **`dashboard/`**: Contiene un archivo pbix generado para visualizar resultados.
-   **`data/raw/`**: Contiene los archivos CSV originales.
-   **`data/processed/`**: Almacena la base de datos SQLite creada y los archivos limpios.
-   **`notebooks/`**: Alberga los Jupyter Notebooks para la transformación y el análisis.
-   **`docs/`**: Contiene documentos de producción de análisis de información
    -   `analisis_exploratorio.ipynb`: Contiene toda la lógica de programación y pruebas realizadas para generar el archivo main.py
-   **`scripts/`**: Contiene scripts de Python reutilizables.
    -   `utils.py`: Contiene funciones de Python reutilizables.
    -   `generate_logs.py`: Tiene la lógica para generar logs interpretables
    -   `extract_sql_data.py`: Almacena queries SQL y las extrae en formato csv.
-   **`main.py`**: Orquesta la lectura de tablas a SQL y creación de información con datos limpios
-   **`README.md`**: Este archivo con la descripción del proyecto.

## Flujo de Trabajo

1.  Los archivos csv originales por defecto en `data/raw/`.
2.  Ejecutar el script `main.py` para crear la base de datos SQLite en `data/processed/reps_data.db`.
3.  El mismo archivo `main.py` orquesta la lectura, la limpieza y la creación de tablas en la base de datos
4.  `main.py` hace el procesamiento para las tablas de Sedes (fuente REPS), Servicios (fuente REPS) y Municipios (Fuente IETS)
5.  Una vez cargada la información a la base de datos, se genera un query de SQL cuya lógica se puede ver en `scripts/extract_sql_data.py`
6.  Los resultados del query de información se almacenan en `data/processed/conteos_sedes.csv` y son útiles para alimentar visualizaciones del archivo contenido en la carpeta **`dashboard/`**

## Requerimientos

1.  Python > 3.11
2.  Bibliotecas necesarias: `pandas`.
3.  Clonar este repositorio.
5.  Ejecutar `main.py` con un entorno activo que tenga instalado pandas.

## Próximos Pasos

-   Implementar queries SQL más complejas.
-   Considerar la automatización de algunos pasos del flujo de trabajo.

## Contacto

Cristian Sarmiento - ccsarmientot@gmail.com