import pandas as pd
import os


def read_excel():
    archivo = './noche/static/noche/archivos/PROPUESTA_FINAL.xlsx'
    df2 = pd.read_excel(archivo, sheet_name="PICKING")
    df = df2[["MV", "HASTA", "DESDE", "TIE"]].dropna()
    return df

def obtener_datos():
    df = read_excel()  # Asume que esta función carga tus datos en un DataFrame

    # Inicializa los contadores en cero
    aire = {'aire0': 0, 'aire1': 0, 'aire2': 0}
    repo = {'repo_mv0': 0, 'repo_mv1': 0, 'repo_mv2': 0}
    check_tie_dormunt = {'tie00d': 0, 'tie01d': 0, 'tie02d': 0}

    # Filtrar y contar usando operaciones vectorizadas
    buffer_condition = (df["DESDE"].str.contains("-", regex=False, na=False) & (df["HASTA"] == "Buffer"))
    sales_condition = (df["DESDE"].str.contains("-", regex=False, na=False) & (df["HASTA"] == "Sales"))

    aire['aire0'] = len(df[(buffer_condition) & (df['MV'] == 0)])
    aire['aire1'] = len(df[(buffer_condition) & (df['MV'] == 1)])
    aire['aire2'] = len(df[(buffer_condition) & (df['MV'] == 2)])

    repo['repo_mv0'] = len(df[(sales_condition) & (df['MV'] == 0)])
    repo['repo_mv1'] = len(df[(sales_condition) & (df['MV'] == 1)])
    repo['repo_mv2'] = len(df[(sales_condition) & (df['MV'] == 2)])

    dormunt_condition = (df['TIE'] == 0) & (df["HASTA"] == "Sales") & (df["DESDE"].str.contains("064-", regex=False, na=False))

    check_tie_dormunt['tie00d'] = len(df[(dormunt_condition) & (df['MV'] == 0)])
    check_tie_dormunt['tie01d'] = len(df[(dormunt_condition) & (df['MV'] == 1)])
    check_tie_dormunt['tie02d'] = len(df[(dormunt_condition) & (df['MV'] == 2)])

    return aire, repo, check_tie_dormunt

def file_upload():
    # Ruta al directorio donde deberían estar los archivos
    directorio_archivos = './noche/static/noche/archivos/'

    # Nombres de los archivos que esperas encontrar
    nombres_archivos = ['PROPUESTA_FINAL.xlsx']  # Reemplaza con los nombres correctos

    # Verifica si todos los archivos están presentes en el directorio
    archivos_presentes = all(os.path.isfile(os.path.join(directorio_archivos, archivo)) for archivo in nombres_archivos)

    return archivos_presentes