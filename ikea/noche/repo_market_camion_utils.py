import pandas as pd
from noche.juntar_camiones import junta_camion
from noche.check_shipments import shipment_duplicados



def read_excel():
    archivo = './noche/static/noche/archivos/PROPUESTA_FINAL.xlsx'
    df2 = pd.read_excel(archivo, sheet_name="PICKING")
    df = df2[["DESDE", "LV", "HASTA", "HFB", "MV", "NOMBRE", "REF"]].dropna()
    df["REF"] = df["REF"].astype(int)
    df = df.drop(df[(df['MV'] == 2) | (df['MV'] == 1)].index)
    return df


menajelista = ("M14", "M15", "B14", "B15", "C14", "C15", "O14", "O15", "V14", "V15")
textil12lista = ("M12", "B12", "C12", "O12", "V12")
textil11lista = ("M11", "B11", "C11", "O11", "V11")
ordenlista = ("M18", "B18", "C18", "O18", "V18")
banoslista = ("M06", "B06", "C06", "O06", "V06")
ilulista = ("M10", "B10", "C10", "O10", "V10")
decolista = ("M16", "B16", "C16", "O16", "V16")
actividadeslista = ("AO", "BDC", "MOW", "SFF", "T07", "V01", "V08", "ACHS", "T01")
ninoslista = ("S09", "B09", "C09", "O09")
cocinaslista = ("S07", "B07", "C07", "O07")
alfombraslista = ("M13", "B13", "C13", "O13", "V13")


def repo_market():
    df = read_excel()
    extras = []
    menaje = 0
    textil11 = 0
    textil12 = 0
    orden = 0
    banos = 0
    ilu = 0
    alfombras = 0
    deco = 0
    ninos = 0
    cocinas = 0
    actividades = 0

    articulos = df[(df['MV'] == 0) & (df["HASTA"] == "Sales") & (df["DESDE"].str.contains("-", regex=False, na=False))]

    for articulo in articulos["LV"]:
        if type(articulo) == str:
            if articulo.startswith(menajelista):
                menaje += 1
            elif articulo.startswith(textil11lista):
                textil11 += 1
            elif articulo.startswith(textil12lista):
                textil12 += 1
            elif articulo.startswith(ordenlista):
                orden += 1
            elif articulo.startswith(banoslista):
                banos += 1
            elif articulo.startswith(ilulista):
                ilu += 1
            elif articulo.startswith(decolista):
                deco += 1
            elif articulo.startswith(ninoslista):
                ninos += 1
            elif articulo.startswith(cocinaslista):
                cocinas += 1
            elif articulo.startswith(alfombraslista):
                alfombras += 1
            elif articulo.startswith(actividadeslista):
                actividades += 1
            else:
                extras.append(articulo)

    return menaje, textil12, textil11, orden, banos, ilu, deco, ninos, cocinas, actividades, alfombras


def camiones_market():
    df = read_excel()
    dic_camiones = {}
    full_cam = junta_camion()
    x = shipment_duplicados()
    for shipment in x:

        menaje = 0
        textil11 = 0
        textil12 = 0
        orden = 0
        banos = 0
        ilu = 0
        deco = 0
        ninos = 0
        cocinas = 0
        actividades = 0
        alfombras = 0

        articulos = df[(df["DESDE"] == shipment) & (df['MV'] == 0)][["REF", "NOMBRE","LV","HASTA"]]
        detalles_articulos = []

        for _, articulo in articulos.iterrows():
            detalles_articulos.append(articulo.to_dict()) 
            if type(articulo["LV"]) == str and (articulo['HASTA'] == 'Sales'):
                if articulo["LV"].startswith(menajelista):
                    menaje += 1
                elif articulo["LV"].startswith(textil11lista):
                    textil11 += 1
                elif articulo["LV"].startswith(textil12lista):
                    textil12 += 1
                elif articulo["LV"].startswith(ordenlista):
                    orden += 1
                elif articulo["LV"].startswith(banoslista):
                    banos += 1
                elif articulo["LV"].startswith(ilulista):
                    ilu += 1
                elif articulo["LV"].startswith(decolista):
                    deco += 1
                elif articulo["LV"].startswith(ninoslista):
                    ninos += 1
                elif articulo["LV"].startswith(cocinaslista):
                    cocinas += 1
                elif articulo["LV"].startswith(alfombraslista):
                    alfombras += 1
                elif articulo["LV"].startswith(actividadeslista):
                    actividades += 1   

        for cami in full_cam:
            p = full_cam[cami]
            if shipment in p:
                if cami in dic_camiones:
                    camion = {"Menaje": menaje, "Textil11": textil11, "Textil12": textil12, "Orden": orden,
                              "Banos": banos,
                              "Iluminacion": ilu,
                              "Deco": deco, "Ninos": ninos, "Cocinas": cocinas, "Actividades": actividades,
                              "Alfombras": alfombras,"Articulos": detalles_articulos}
                    combined_dict = {}
                    for k in camion.keys():
                        combined_dict[k] = dic_camiones[cami][f"{p}"].get(k, 0) + camion.get(k, 0)
                    dic_camiones[cami][f"{p}"] = combined_dict
                else:
                    dic_camiones.update({f"{cami}": {f"{p}": {"Menaje": 0}}})
                    camion = {"Menaje": menaje, "Textil11": textil11, "Textil12": textil12, "Orden": orden,
                              "Banos": banos,
                              "Iluminacion": ilu,
                              "Deco": deco, "Ninos": ninos, "Cocinas": cocinas, "Actividades": actividades,
                              "Alfombras": alfombras,"Articulos": detalles_articulos}
                    dic_camiones[f"{cami}"][f"{p}"].update(camion)
                    for camion, detalles in dic_camiones.items():
                        for shipment, info in detalles.items():
                            info["Articulos"].sort(key=lambda x: str(x["LV"]))
    return dic_camiones