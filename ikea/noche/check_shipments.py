import pandas as pd

def read_excel():
    archivo = './noche/static/noche/archivos/PROPUESTA_FINAL.xlsx'
    df2 = pd.read_excel(archivo, sheet_name="PICKING")
    df = df2[["DESDE"]].dropna()
    return df


camiones_duplicados = []
camiones_shipment = []


def shipment_duplicados():

    df = read_excel()
    for shipment in df["DESDE"]:
        if type(shipment) == str and shipment != "BACKFLOW":
            camiones_duplicados.append(shipment)

    for camion in camiones_duplicados:
        if camion not in camiones_shipment:
            camiones_shipment.append(camion)
    return camiones_shipment

