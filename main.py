import os
import sys
import time
import pandas as pd

from scripts.generate_logs import func_msg

from scripts.utils import crear_conexion, preprocess_text_column
from scripts.utils import preprocess_read_reps_data, fix_divipola_codes

from scripts.extract_sql_data import extract_bd_data

func_msg('start processing...')
sys.path.append('scripts')
start_time = time.time()

try:
    
    
    # Crear la carpeta 'data/processed' si no existe
    ruta_db = 'data/processed/reps_data.db'
    os.makedirs(os.path.dirname(ruta_db), exist_ok=True)
    
    ## Concectar con la base de datos
    func_msg(f'Creando la base de datos en la ruta: "{ruta_db}"')
    conn = crear_conexion(ruta_db)
    
    func_msg('Base de datos creada correctamente!\n')
    
    ########################################################################
    ####################### preprocesar municipios #########################
    ########################################################################
    
    ## Leer el dataframe
    func_msg('Leyendo tabla de municipios...')
    data_path = 'data/raw/Municipios.xlsx'
    df_municipios = pd.read_excel(data_path)
    
    func_msg('Preprocesando municipios...')
    ## Preprocesar las columnas de departamento y municipio
    for col in ['Departamento', 'Municipio']:
        df_municipios[col] = preprocess_text_column(df_municipios[col])

    ## Fix MPIO codes
    df_municipios['MPIO'] = fix_divipola_codes(df_municipios['MPIO'], fix_len=4)
    df_municipios['DP'] = fix_divipola_codes(df_municipios['DP'], fix_len=1)
    
    func_msg('Cargando municipios a la base de datos...')
    ## Enviar datos limpios a la db en data/processed
    df_municipios.to_sql(name='reps_municipios', con=conn, 
                         if_exists='replace', index=False)
    
    func_msg('Tabla de reps_municipios creada correctamente en base de datos!\n')
    
    ########################################################################
    ####################### preprocesar servicios ##########################
    ########################################################################
    
    ## Leer la tabla de servicios
    func_msg('Leyendo tabla de servicios...')
    func_msg('Preprocesando servicios...')
    data_path = 'data/raw/Servicios.zip'
    df_servicios = preprocess_read_reps_data(data_path)
    
    ## Enviar datos limpios a la db en data/processed
    func_msg('Cargando servicios a la base de datos...')
    df_servicios.to_sql(name='reps_servicios', con=conn, 
                        if_exists='replace', index=False)  
    
    func_msg('Tabla de reps_servicios creada correctamente en base de datos!\n')
        
    ########################################################################
    ######################### preprocesar sedes ############################
    ########################################################################
    
    ## Leer la tabla de sedes
    func_msg('Leyendo tabla de sedes...')
    func_msg('Preprocesando sedes...')
    data_path = 'data/raw/Sedes.zip'
    df_sedes = preprocess_read_reps_data(data_path)
    
    ## Enviar datos limpios a la db en data/processed
    func_msg('Cargando sedes a la base de datos...')
    df_sedes.to_sql(name='reps_sedes', con=conn, 
                    if_exists='replace', index=False)  
    func_msg('Tabla de reps_sedes creada correctamente en base de datos!\n')

    ########################################################################
    ######################### preprocesar sedes ############################
    ########################################################################
    
    ## Disponibilizar cruce de información en processed como un csv
    func_msg('Leyendo y cruzando información usando SQL...')
    extract_bd_data(conn)
    func_msg('Tabla cruzada generada correctamente!\n')
    
    func_msg('Proceso finalizado\n')

except Exception as e:
    func_msg(f'[ERROR] {e}')

finally:
    total_time = time.time() - start_time
    conn.close()
    func_msg(f'Total elapsed time: {total_time:,.2f}')
