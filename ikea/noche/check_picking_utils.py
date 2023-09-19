import pandas as pd


pares_pasillos = ("8", "10", "12", "14", "16", "18", "20", "22")
impares_pasillos = ("5", "7", "9", "11", "13", "15", "17", "19")
pax_pasillos = ("21", "23")
veinticuatro_pasillos = ("24", "26")
fondopar_pasillos = ("28", "30", "32", "34", "36", "38", "40", "42")
fondoimpar_pasillos = ("25", "27", "29", "31", "33", "35", "37", "39", "41")
pasillo1a3_pasillos = ("1", "3")
cabeceras_pasillos = ("5000","6000","7000","8000","9000","1000","1100","1200","1300","1400","1500","1600","1700","1800","1900","2000","2100","2200","2300","2400","2500","2600",
             "2700","2800","2900","3000","3100","3200","3300","3400","3500","3600","3700","3800","3900","4000","4100","4200")

menajelista = ("M14", "M15", "B14", "B15", "C14", "C15", "O14", "O15", "V14", "V15")
textil12lista = ("M12", "B12", "C12", "O12", "V12")
textil11lista = ("M11", "B11", "C11", "O11", "V11")
ordenlista = ("M18", "B18", "C18", "O18", "V18")
banoslista = ("M06", "B06", "C06", "O06", "V06")
ilulista = ("M10", "B10", "C10", "O10", "V10")
decolista = ("M16", "B16", "C16", "O16", "V16")
actividadeslista = ("AO", "BDC", "MOW", "SFF", "T07", "V01", "V08", "ACHS", "T01")
ninoslista = ("S09", "B09", "C09", "O09","V09")
cocinaslista = ("S07", "B07", "C07", "O07","V07")
alfombraslista = ("M13", "B13", "C13", "O13", "V13")

import pandas as pd

def read_excel():
    archivo = './noche/static/noche/archivos/SG010.xlsx'  
    try:
        df = pd.read_excel(archivo, sheet_name="Data")
    except ValueError:
        # Si la hoja "Data" no existe, intenta leer la hoja "Export"
        df = pd.read_excel(archivo, sheet_name="Export")
    df2 = df[["PRIMARY", "UNCONF_OUT"]].dropna()
    return df2





def sgf_pickingmv1():
    df = read_excel()
    df["UNCONF_OUT"] = pd.to_numeric(df["UNCONF_OUT"], errors="coerce")
    df2 = df[["PRIMARY", "UNCONF_OUT"]][df["UNCONF_OUT"] > 0].dropna()

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

    for lv in df2["PRIMARY"]:
        if str(lv).startswith("0001"):
            zona1 += 1
        elif str(lv).startswith("0002"):
            zona2 += 1
        elif str(lv).startswith("0003"):
            zona3 += 1
        elif str(lv).startswith("0004"):
            zona4 += 1
        elif str(lv).startswith(pasillo1a3_pasillos) and len(str(lv)) <= 5:
            pasillo1a3 += 1
        elif str(lv).startswith(cabeceras_pasillos):
            cabeceras +=1
        elif str(lv).startswith(pares_pasillos):
            pares += 1
        elif str(lv).startswith(impares_pasillos):
            impares += 1
        elif str(lv).startswith(pax_pasillos):
            pax += 1
        elif str(lv).startswith(veinticuatro_pasillos):
            veinticuatro += 1
        elif str(lv).startswith(fondopar_pasillos):
            fondopar += 1
        elif str(lv).startswith(fondoimpar_pasillos):
            fondoimpar += 1

    return zona1, zona2, zona3, zona4, pares, impares, pax, veinticuatro, fondopar, fondoimpar, pasillo1a3, cabeceras


def sgf_pickingmv0():
    df = read_excel()
    df["UNCONF_OUT"] = pd.to_numeric(df["UNCONF_OUT"], errors="coerce")
    df2 = df[["PRIMARY", "UNCONF_OUT"]][df["UNCONF_OUT"] > 0].dropna()

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

    for articulo in df2["PRIMARY"]:
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