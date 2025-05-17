import csv
import sqlite3
import os
import pandas as pd

def preprocess_text_column(col:pd.Series) -> pd.Series:
    """
    Arregla texto de una columna que contiene caracteres especiales
    y espacios.
    """

    ## Remove special chars
    series = col.replace(r'[^\w\sáéíóúÁÉÍÓÚñÑ]', '', regex=True)

    ## Remove double white spaces
    series = series.replace(r'\s+', ' ', regex=True)
    series = series.str.strip()
    series = series.str.lower()

    ## Capitalize what columns cointains. "valle del cauca" -> "Valle Del Cauca"
    series = series.apply(lambda t: ' '.join([l.capitalize() for l in t.split(' ')]))
    return series


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


def crear_conexion(db_file):
    """Crea una conexión a la base de datos SQLite especificada por db_file.
    :param db_file: Ruta del archivo de la base de datos.
    :return: Objeto de conexión o None.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    return conn


## Fix MPIO codes
def fix_divipola_codes(series:pd.Series, fix_len:int=4) -> pd.Series:
    """
    
    """
    series = series.astype(str)
    series = series.apply(lambda t: f'0{t}' if len(t) == fix_len else t)
    return series