import pandas as pd

# Ruta al archivo Excel
archivo = './noche/static/noche/archivos/PROPUESTA_FINAL.xlsx'

def read_excel():
    df2 = pd.read_excel(archivo, sheet_name="PICKING", usecols=["NOMBRE", "MV", "REF", "DESDE"]).dropna()
    return df2

def repeticiones():
    df = read_excel()
    
    # Filtrar registros que contienen "-"
    df = df[df["DESDE"].str.contains("-", regex=False, na=False)]
    
    df["REF"] = df["REF"].astype(int)
    df["REPETICIONES"] = df.groupby("REF")["REF"].transform("count")
    
    # Filtrar registros con más de 10 repeticiones y eliminar duplicados
    df_filtrado = df[df["REPETICIONES"] > 10].drop_duplicates(subset="REF")
    
    # Ordenar por REPETICIONES de forma descendente
    resultado_ordenado = df_filtrado.sort_values(by="REPETICIONES", ascending=False)
    
    # Convertir el DataFrame en una tabla HTML
    repeticiones_html = resultado_ordenado.to_html(classes="table table-primary table-striped table-bordered table-sm text-center",
                                                   index=False, justify="center", columns=["NOMBRE", "REF", "REPETICIONES"])
    
    return repeticiones_html