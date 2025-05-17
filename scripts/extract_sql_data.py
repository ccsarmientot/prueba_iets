import pandas as pd

def extract_bd_data(conn) -> None:
    """
    Para este ejercicio específico, usando las columnas 'ESPECIFICIDAD_ONCOLOGICO' 
    y 'ESPECIFICIDAD_TRASPLANTE_RENAL' se quiere generar un dato de la 
    cantidad de sedes que tienen la marcación 'SI' en estas columnas y 
    generar una cantidad por cada 100.000 habitantes para regiones y una 
    por cada 10.000 habitantes para municipios. 
    """
    # Generate the sql query
    query = (
        """
        -- Crear cte para procesar tablas y facilitar la lectura del código
        
        -- traer la tabla de servicios oncologicos y la cantidad de sedes por 
        -- municipios.
        WITH servicios AS (
            SELECT CODIGO_HABILITACION
                , COMPLEJIDADES
                , SERV_NOMBRE
                , ESPECIFICIDAD_ONCOLOGICO
                , ESPECIFICIDAD_TRASPLANTE_RENAL 
                , SUBSTRING(CODIGO_HABILITACION, 1, 5) AS COD_MUNICIPIO
                , CODIGO_HABILITACION || NUMERO_SEDE AS COD_SEDE

            FROM reps_servicios
            WHERE  1 = 1
                AND HABILITADO = 'SI'
        )
        
        -- Traer la tabla de municipios
        , municipios AS (
            SELECT MPIO AS COD_MUNICIPIO
                , Municipio
                , Departamento
                , Region
                , PopTot
            FROM reps_municipios
        )
        
        -- Agrupar la tabla por servicios para tener conteos por tipo de servicio
        , servicios_oncologico AS (
            SELECT COD_MUNICIPIO, COUNT(DiSTINCT COD_SEDE) AS SEDES_ONCOLOGICO
                , 'ONCOLOGICO' AS tipo_servicio
            FROM servicios
            WHERE 1 = 1
                AND ESPECIFICIDAD_ONCOLOGICO = 'SI'
            
            GROUP BY COD_MUNICIPIO
        )
        , servicios_renal AS (
            SELECT COD_MUNICIPIO, COUNT(DiSTINCT COD_SEDE) AS SEDES_RENAL
                , 'ONCOLOGICO' AS tipo_servicio
            FROM servicios
            WHERE 1 = 1
                AND ESPECIFICIDAD_TRASPLANTE_RENAL = 'SI'
            
            GROUP BY COD_MUNICIPIO
        )

        -- Hacer la unión con la tabla de municipios para hallar la cantidad de sedes
        -- para las dos especialidades específicas por municipio
        SELECT municipios.COD_MUNICIPIO
            , municipios.Municipio
            , municipios.Departamento
            , municipios.Region
            , municipios.PopTot
            , COALESCE(SEDES_ONCOLOGICO, 0) AS SEDES_ONCOLOGICO
            , COALESCE(SEDES_RENAL, 0) AS SEDES_RENAL
        FROM municipios
        LEFT JOIN servicios_oncologico 
        ON servicios_oncologico.COD_MUNICIPIO = municipios.COD_MUNICIPIO
        
        LEFT JOIN servicios_renal 
        ON servicios_renal.COD_MUNICIPIO = municipios.COD_MUNICIPIO
        
        """
    )

    ## Use pandas to query de reps_sedes database
    df = pd.read_sql_query(query, conn)
    df.to_csv('data/processed/conteos_sedes.csv', sep='|', index=False)
    
    pass