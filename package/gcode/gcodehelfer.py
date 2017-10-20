from __future__ import print_function
import math

class GCodeStrecke:
    def __init__(self, x1, y1, z1, x2, y2, z2, infill=False):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1

        self.x2 = x2
        self.y2 = y2
        self.z2 = z2

        self.infill = infill

    def umdrehen(self):
        # swap
        self.x1, self.x2 = self.x2, self.x1
        self.y1, self.y2 = self.y2, self.y1
        self.z1, self.z2 = self.z2, self.z1

    def __str__(self):
        return "({} {} {}  {} {} {})".format(self.x1, self.y1, self.z1, self.x2, self.y2, self.z2)

    def __repr__(self):
        return "({} {} {}  {} {} {})".format(self.x1, self.y1, self.z1, self.x2, self.y2, self.z2)

def export(strecken, ausgabe_datei, gcode_anfang=None, gcode_ende=None, mitte_x=0, mitte_y=0):
    # Offne Datei
    with open(ausgabe_datei, "w") as f:

        # Anfang kopieren
        if gcode_anfang is not None:
            with open(gcode_anfang, "r") as g:
                for zeile in g:
                    # Kopiere jede Zeile in die Ausgabedatei
                    # und losche alle Lehrzeichen am Anfang und Ende
                    # jeder Zeile
                    print(zeile.strip(), file=f)

        # Alles kopieren
        e_menge = 0
        for strecke in strecken:
            if e_menge > 100:
                e_menge = 0
                s = "G92 E0"
                print(s, file=f)

            # 1mm pro 50mm Weg
            e_dist = math.sqrt((strecke.x2 - strecke.x1)**2 + (strecke.y2 - strecke.y1)**2) / 50

            s1 = "G1 X{:0.5f} Y{:0.5f} Z{:0.5f}".format(strecke.x1 + mitte_x, strecke.y1 + mitte_y, strecke.z1)
            s2 = "G1 X{:0.5f} Y{:0.5f} E{:0.5f}".format(strecke.x2 + mitte_x, strecke.y2 + mitte_y, e_menge + e_dist)

            # Speichern in Ausgabedatei
            print(s1, file=f)
            print(s2, file=f)

            e_menge += e_dist

        # Bisschen Hoch am Ende, 5mm
        s1 = "G1 Z{:0.5f}".format(strecken[-1].z1 + 5)
        print(s1, file=f)


        # Ende kopieren
        if gcode_ende is not None:
            with open(gcode_ende, "r") as g:
                for zeile in g:
                    print(zeile.strip(), file=f)

    # Anzahl an Zeilen im Gcode
    anzahl_zeilen = sum(1 for line in open(ausgabe_datei))
    return anzahl_zeilen
