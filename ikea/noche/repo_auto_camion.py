import pandas as pd
from noche.juntar_camiones import junta_camion
from noche.check_shipments import shipment_duplicados

def read_excel():
    archivo = './noche/static/noche/archivos/PROPUESTA_FINAL.xlsx'
    df2 = pd.read_excel(archivo, sheet_name="PICKING")
    df = df2[["LV", "MV", "HASTA", "DESDE", "REF", "NOMBRE"]].dropna()
    df["REF"] = df["REF"].astype(int)
    return df

pares_pasillos = ("8", "10", "12", "14", "16", "18", "20", "22")
impares_pasillos = ("5", "7", "9", "11", "13", "15", "17", "19")
pax_pasillos = ("21", "23")
veinticuatro_pasillos = ("24", "26")
fondopar_pasillos = ("28", "30", "32", "34", "36", "38", "40", "42")
fondoimpar_pasillos = ("25", "27", "29", "31", "33", "35", "37", "39", "41")
pasillo1a3_pasillos = ("1", "3")
cabeceras_pasillos = ("5000","6000","7000","8000","9000","1000","1100","1200","1300","1400","1500","1600","1700","1800","1900","2000","2100","2200","2300","2400","2500","2600",
             "2700","2800","2900","3000","3100","3200","3300","3400","3500","3600","3700","3800","3900","4000","4100","4200")

def repo_auto():
    df = read_excel()

    zona1 = 0
    zona2 = 0
    zona3 = 0
    zona4 = 0
    pasillo1a3 = 0
    impares = 0
    pares = 0
    pax = 0
    veinticuatro = 0
    fondopar = 0
    fondoimpar = 0
    cabeceras = 0

    articulo = df[(df['MV'] == 1) & (df["HASTA"] == "Sales") & (df["DESDE"].str.contains("-", regex=False, na=False))]
    for referencia in articulo["LV"]:
        if str(referencia).startswith("1") and len(str(referencia)) <= 3:
            zona1 += 1
        elif str(referencia).startswith("2") and len(str(referencia)) <= 3:
            zona2 += 1
        elif str(referencia).startswith("3") and len(str(referencia)) <= 3:
            zona3 += 1
        elif str(referencia).startswith("4") and len(str(referencia)) <= 3:
            zona4 += 1
        elif str(referencia).startswith(cabeceras_pasillos):
            cabeceras += 1
        elif str(referencia).startswith(pasillo1a3_pasillos) and len(str(referencia)) <= 5:
            pasillo1a3 += 1
        elif str(referencia).startswith(pares_pasillos):
            pares += 1
        elif str(referencia).startswith(impares_pasillos):
            impares += 1
        elif str(referencia).startswith(pax_pasillos):
            pax += 1
        elif str(referencia).startswith(veinticuatro_pasillos):
            veinticuatro += 1
        elif str(referencia).startswith(fondopar_pasillos):
            fondopar += 1
        elif str(referencia).startswith(fondoimpar_pasillos):
            fondoimpar += 1
    return zona1, zona2, zona3, zona4, pares, impares, pax, veinticuatro, fondopar, fondoimpar, pasillo1a3, cabeceras


def camiones_auto():
    df = read_excel()

    dic_camiones = {}
    full_cam = junta_camion()
    x = shipment_duplicados()
    for shipment in x:
        zona1 = 0
        zona2 = 0
        zona3 = 0
        zona4 = 0
        pasillo1a3 = 0
        impares = 0
        pares = 0
        pax = 0
        veinticuatro = 0
        fondopar = 0
        fondoimpar = 0
        cabeceras = 0

        articulos = df[(df["DESDE"] == shipment) & (df['MV'] == 1)][["REF", "NOMBRE","LV","HASTA"]]
        detalles_articulos = []

        for _, articulo in articulos.iterrows():
            detalles_articulos.append(articulo.to_dict()) 
            if str(articulo["LV"]).startswith("1") and len(str(articulo["LV"])) <= 3 and (articulo['HASTA'] == 'Sales'):
                zona1 += 1
            elif str(articulo["LV"]).startswith("2") and len(str(articulo["LV"])) <= 3 and (articulo['HASTA'] == 'Sales'):
                zona2 += 1
            elif str(articulo["LV"]).startswith("3") and len(str(articulo["LV"])) <= 3 and (articulo['HASTA'] == 'Sales'):
                zona3 += 1
            elif str(articulo["LV"]).startswith("4") and len(str(articulo["LV"])) <= 3 and (articulo['HASTA'] == 'Sales'):
                zona4 += 1
            elif str(articulo["LV"]).startswith(cabeceras_pasillos) and (articulo['HASTA'] == 'Sales'):
                cabeceras += 1
            elif str(articulo["LV"]).startswith(pasillo1a3_pasillos) and len(str(articulo["LV"])) <= 5 and (articulo['HASTA'] == 'Sales'):
                pasillo1a3 += 1
            elif str(articulo["LV"]).startswith(pares_pasillos) and (articulo['HASTA'] == 'Sales'):
                pares += 1
            elif str(articulo["LV"]).startswith(impares_pasillos) and (articulo['HASTA'] == 'Sales'):
                impares += 1
            elif str(articulo["LV"]).startswith(pax_pasillos) and (articulo['HASTA'] == 'Sales'):
                pax += 1
            elif str(articulo["LV"]).startswith(veinticuatro_pasillos) and (articulo['HASTA'] == 'Sales'):
                veinticuatro += 1
            elif str(articulo["LV"]).startswith(fondopar_pasillos) and (articulo['HASTA'] == 'Sales'):
                fondopar += 1
            elif str(articulo["LV"]).startswith(fondoimpar_pasillos) and (articulo['HASTA'] == 'Sales'):
                fondoimpar += 1

        for cami in full_cam:
            p = full_cam[cami]
            if shipment in p:
                if cami in dic_camiones:
                    camion = {"pares": pares, "impares": impares, "fondopar": fondopar, "fondoimpar": fondoimpar,
                              "pax": pax, "2426": veinticuatro, "1a3": pasillo1a3, "zona1": zona1,
                              "zona2": zona2, "zona3": zona3, "zona4": zona4, "cabeceras": cabeceras, "Articulos": detalles_articulos}
                    combined_dict = {}
                    for k in camion.keys():
                        combined_dict[k] = dic_camiones[cami][f"{p}"].get(k, 0) + camion.get(k, 0)
                    dic_camiones[cami][f"{p}"] = combined_dict
                else:
                    dic_camiones.update({f"{cami}": {f"{p}": {"pares": 0}}})
                    camion = {"pares": pares, "impares": impares, "fondopar": fondopar, "fondoimpar": fondoimpar,
                              "pax": pax, "2426": veinticuatro, "1a3": pasillo1a3, "zona1": zona1,
                              "zona2": zona2, "zona3": zona3, "zona4": zona4, "cabeceras": cabeceras, "Articulos": detalles_articulos}
                    dic_camiones[f"{cami}"][f"{p}"].update(camion)
                    for camion, detalles in dic_camiones.items():
                        for shipment, info in detalles.items():
                            info["Articulos"].sort(key=lambda x: str(x["LV"]))
    return dic_camiones