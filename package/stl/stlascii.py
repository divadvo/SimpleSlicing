import stl

def stl_ascii_analysieren(stl_datei):

    dreiecke = []

    with open(stl_datei, "r") as f:
        # Zeilen ohne lehrzeichen am Anfang und Ende
        zeilen = f.readlines()
        zeilen = [x.strip() for x in zeilen]

        for i in range(len(zeilen)):
            zeile = zeilen[i]

            if zeile.startswith("facet normal"):
                dreieck = read_dreieck(zeilen, i)
                dreiecke.append(dreieck)

    stl_data = stl.STLData(None, dreiecke, False)
    return stl_data

def read_dreieck(zeilen, i):
    # Normalenvektor (x, y, z) des Dreiecks
    normalenvektor = read_vec3_ignoriere(zeilen, i, 2)

    # 3 Eckpunkte jeweils (x, y, z) der Eckpunte des Dreiecks
    e0, e1, e2 = read_dreieck_eckpunkte(zeilen, i+2)

    dreieck = stl.STLDreieck(normalenvektor, e0, e1, e2)
    return dreieck


def read_dreieck_eckpunkte(zeilen, i):
    eckpunkte = []

    for k in range(3):
        zeile = zeilen[i + k]
        if zeile.startswith("vertex"):
            eckpunkt = read_vec3_ignoriere(zeilen, i + k, 1)
            eckpunkte.append(eckpunkt)
        else:
            print("ERROR: less than 3 vertices")

    return eckpunkte


def read_vec3_ignoriere(zeilen, i, ignoriere_anzahl_worter):
    zeile = zeilen[i]

    # Trenne in einzelne Teilstrings
    # Ignoriere die ersten x worte
    werte_als_string = zeile.split()[ignoriere_anzahl_worter:]

    # in Kommazahlen umwandeln
    werte = map(float, werte_als_string)

    # Vektor erstellen
    vektor = stl.STLVektor3(werte[0], werte[1], werte[2])

    return vektor
