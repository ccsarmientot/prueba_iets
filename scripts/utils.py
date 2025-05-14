
import os
import pandas as pd

def preprocess_read_reps_data(data_path:str) -> pd.DataFrame:
    """
    Función para leer información descargada de REPS. En las bases de datos de "Sedes"
    y "Servicios" tienen la particularidad de que al hacer la lectura con pandas se 
    corren los encabezados una columna. 
    """
    
    ## Read dataframe from data_path
    df = pd.read_csv(data_path, sep=';', encoding='ISO-8859-1', on_bad_lines='skip', dtype=str)
    
    ## Alocate first colum from index
    df = df.reset_index(names='wildcard')

    ## Clean columns names and assign correct order
    cols = [c.upper().strip() for c in df.columns]

    ## Move WILCARD column to last position
    cols = cols[1:] + ['WILDCARD']
    df.columns = cols
    
    ## Preprocess data to handle it as text to facilitate joins
    for col in df:
        df[col] = df[col].str.strip()
        df[col] = df[col].str.upper()

    return df


def create_dir():
    pass