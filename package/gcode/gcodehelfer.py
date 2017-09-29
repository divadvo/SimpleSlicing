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

class GCodeBefehl:
    def __init__(self, art, x, y, z, e, text):
        self.art = art
        self.x = x
        self.y = y
        self.z = z
        self.e = e
        self.text = text

def z(zahl):
    s = "{:0.5f}".format(zahl)
    return float(s)

def export(sliced, ausgabe_datei, gcode_anfang=None, gcode_ende=None, mitte_x=0, mitte_y=0):
    print('export')
    print(ausgabe_datei)
    print(gcode_anfang, gcode_ende, mitte_x, mitte_y)
    befehle = []

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
        e_off = 0
        for strecke in sliced:
            if e_off > 5:
                e_off = 0
                s = "G92 E0"
                print(s, file=f)
                befehle.append(GCodeBefehl("G92", None, None, None, None, "G92 E0"))

            #e_dist = math.hypot(strecke.x2 - strecke.x1, strecke.y2 - strecke.y1)
            e_dist = math.sqrt((strecke.x2 - strecke.x1)**2 + (strecke.y2 - strecke.y1)**2) / 10 # * a
            print (e_dist)
            s1 = "G1 X{:0.5f} Y{:0.5f} Z{:0.5f}".format(strecke.x1 + mitte_x, strecke.y1 + mitte_y, strecke.z1)
            s2 = "G1 X{:0.5f} Y{:0.5f} E{:0.5f}".format(strecke.x2 + mitte_x, strecke.y2 + mitte_y, e_off + e_dist)

            befehle.append(GCodeBefehl("G1", z(strecke.x1), z(strecke.y1), z(strecke.z1), None, s1))
            befehle.append(GCodeBefehl("G1", z(strecke.x2), z(strecke.y2), None, z(e_off + e_dist), s2))

            print(s1, file=f)
            print(s2, file=f)
            e_off += e_dist


        # Ende kopieren
        if gcode_ende is not None:
            with open(gcode_ende, "r") as g:
                for zeile in g:
                    print(zeile.strip(), file=f)

        print('finished')


        return befehle
