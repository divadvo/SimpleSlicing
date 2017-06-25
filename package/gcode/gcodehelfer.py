from __future__ import print_function
import math

class GCodeStrecke:
    def __init__(self, x1, y1, z1, x2, y2, z2):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1

        self.x2 = x2
        self.y2 = y2
        self.z2 = z2

def export(sliced, gcode_anfang, gcode_ende, ausgabe_datei):

    with open(ausgabe_datei, "w") as f:

        # Anfang kopieren
        # if gcode_anfang is not None:
        #     with open(gcode_anfang, "r") as g:
        #         for zeile in g:
        #             # Kopiere jede Zeile in die Ausgabedatei
        #             # und losche alle Lehrzeichen am Anfang und Ende
        #             # jeder Zeile
        #             print(zeile.strip(), file=f)

        # Alles kopieren
        e_off = 0
        for strecke in sliced:
            if e_off > 100:
                e_off = 0
                print("G92 E0", file=f)

            e_dist = math.hypot(strecke.x2 - strecke.x1, strecke.y2 - strecke.y1)
            print("G1 X{:0.5f} Y{:0.5f} Z{:0.5f}".format(strecke.x1, strecke.y1, strecke.z1), file=f)
            print("G1 X{:0.5f} Y{:0.5f} E{:0.5f}".format(strecke.x2, strecke.y2, e_off + e_dist), file=f)
            e_off += e_dist


        # Ende kopieren
        # if gcode_ende is not None:
        #     with open(gcode_ende, "r") as g:
        #         for zeile in g:
        #             print(zeile.strip(), file=f)
