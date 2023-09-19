import pandas as pd

def read_excel():
    archivo = './noche/static/noche/archivos/AR.xlsx'
    df = pd.read_excel(archivo, sheet_name="Listado Alta Rotación", usecols=["REFERENCIA", "NOMBRE ARTICULO", "LV", "PICKING", "TOTAL SGF"], header=1)
    df.fillna(0, inplace=True)
    df['REFERENCIA'] = df['REFERENCIA'].astype(int)
    df['TOTAL SGF'] = df['TOTAL SGF'].astype(int)
    filas = len(df['REFERENCIA'])

    df.rename(columns={"NOMBRE ARTICULO": "NOMBRE_ARTICULO", "TOTAL SGF": "TOTAL_SGF"}, inplace=True)  
    return df,filas