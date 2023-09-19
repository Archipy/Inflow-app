import pandas as pd

def read_excel():
    plan_descarga = './noche/static/noche/archivos/PLAN.xlsx'
    df = pd.read_excel(plan_descarga, sheet_name="PLAN", header=1, engine="openpyxl")
    df = df[["Shipment ID", "Consignment ID"]]
    return df

def junta_camion():
    full_cam = {}
    df = read_excel()
    # Itera a través de las filas del DataFrame
    for index, row in df.iterrows():
        valor_columna_a = str(row['Shipment ID'])
        valores_columna_b = str(row['Consignment ID']).split(',')  # Separa los valores por comas y los convierte en una lista
        valores_columna_b = [valor.strip() for valor in valores_columna_b]  # Elimina los espacios que se quedan entre shipments

        # Asocia los valores de la Columna A con la lista de valores de la Columna B en el diccionario
        full_cam[valor_columna_a] = valores_columna_b
    return full_cam
    # Imprime el diccionario resultante
