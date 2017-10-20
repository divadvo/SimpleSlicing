import numpy as np
import stl.stl
import gcode.gcodehelfer


def generiere_aussenwaende(stl_data, parameter):
    waende = []

    # Runden
    def runden(x, base):
        return round(base * round(float(x) / base), 1)

    schicht_dicke = parameter["schicht_hohe"]
    maximale_hohe = runden(stl_data.hilfswerte.max.z - stl_data.hilfswerte.min.z, schicht_dicke)

    import wx

    progressMax = 100
    dialog = wx.ProgressDialog("Aussenwaende", "Bitte warten", progressMax,
                               style=wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_SMOOTH | wx.PD_AUTO_HIDE)

    # Von Hohe 0 bis oben
    # in [schicht_dicke] Schritten
    # np.arange() fur dezimale Schritte
    for aktuelle_hohe in np.arange(0, maximale_hohe + schicht_dicke, schicht_dicke):
        percentage = aktuelle_hohe / (maximale_hohe + schicht_dicke) * 100
        # print "{0:.0f}%".format(percentage)
        dialog.Update(percentage)

        for dreieck in stl_data.dreiecke:
            min_z = min([eckpunkt.z for eckpunkt in dreieck.eckpunkte])
            max_z = max([eckpunkt.z for eckpunkt in dreieck.eckpunkte])

            # Benutze nur die Dreiecke die in der derzeitigen Schicht liegen
            if min_z - schicht_dicke < aktuelle_hohe <= max_z:
                waende += schneiden(dreieck, aktuelle_hohe,
                                    parameter, stl_data.hilfswerte)

    dialog.Destroy()


    # In einem Zug
    waende.sort(key=lambda strecke: strecke.z1)

    neue_wande = []

    for aktuelle_hohe in np.arange(0, maximale_hohe + schicht_dicke, schicht_dicke):
        alle = [strecke for strecke in waende if strecke.z1 == aktuelle_hohe]

        neue_alle = []
        c_x = 0
        c_y = 0
        length = len(alle)

        # Gehe alle Strecken durch
        # finde die am nachsten liegende
        # uberprufe nicht die schon benutzten
        for i in range(length):
            start = am_nachsten(c_x, c_y, alle)
            neue_alle.append(start)
            alle.remove(start)
            c_x = start.x2
            c_y = start.y2

        neue_wande += neue_alle

    return neue_wande


def am_nachsten(c_x, c_y, alle_strecken):

    def d2(strecke):
        return (strecke.x1 - c_x)**2 + (strecke.y1 - c_y)**2, (strecke.x2 - c_x)**2 + (strecke.y2 - c_y)**2

    smallest_d = 1000000
    closest = None
    umgedreht = False
    for idx, strecke in enumerate(alle_strecken):
        start_d, ende_d = d2(strecke)
        # Wenn das Ende der Strecke naher ist,
        # drehe um
        if start_d < smallest_d:
            smallest_d = start_d
            closest = strecke
        elif ende_d < smallest_d:
            smallest_d = ende_d
            closest = strecke
            closest.umdrehen()

    return closest


def schneiden(dreieck, aktuelle_hohe, parameter, hilfswerte):
    strecken = []

    punkte_uber_schicht = [eckpunkt for eckpunkt in dreieck.eckpunkte if eckpunkt.z > aktuelle_hohe + parameter["schicht_hohe"]]
    punkte_unter_schicht = [eckpunkt for eckpunkt in dreieck.eckpunkte if eckpunkt.z < aktuelle_hohe + parameter["schicht_hohe"]]
    punkte_in_schicht = [eckpunkt for eckpunkt in dreieck.eckpunkte if 
                        aktuelle_hohe <= eckpunkt.z <= aktuelle_hohe + parameter["schicht_hohe"]]

    # Fast Flach in der Ebene
    if 1.0 - parameter["dusen_durchmesser"] / 10.00 <= abs(dreieck.normalenvektor.z) <= 1.0 + parameter["dusen_durchmesser"] / 10.00:
        eckpunkte = dreieck.eckpunkte

        # Finde kleinste und grosste x Koordinate vom Dreieck
        x_min = min(eckpunkte, key=lambda v: v.x).x
        x_max = max(eckpunkte, key=lambda v: v.x).x

        # Wie sieht das Dreieck aus? 2 Punkte links? 2 Punkte rechts? 1 Mittig?
        links = [eckpunkt for eckpunkt in eckpunkte if eckpunkt.x == x_min]
        rechts = [eckpunkt for eckpunkt in eckpunkte if eckpunkt.x == x_max]
        zentral = [eckpunkt for eckpunkt in eckpunkte if eckpunkt not in links and eckpunkt not in rechts]

        def zwei_links(links1, links2, rechts):
            for x_ind in np.arange(links1.x, rechts.x, parameter["schicht_hohe"]):
                t1 = (x_ind - links1.x) / (rechts.x - links1.x)
                t2 = (x_ind - links2.x) / (rechts.x - links2.x)

                strecken.append(
                    gcode.gcodehelfer.GCodeStrecke(
                        x_ind, (rechts.y - links1.y) * t1 + links1.y, aktuelle_hohe,
                        x_ind, (rechts.y - links2.y) * t2 + links2.y, aktuelle_hohe
                    )
                )

        def zwei_rechts(links, rechts1, rechts2):
            for x_ind in np.arange(links.x, rechts1.x, parameter["schicht_hohe"]):
                t1 = (x_ind - links.x) / (rechts1.x - links.x)
                t2 = (x_ind - links.x) / (rechts2.x - links.x)

                strecken.append(
                    gcode.gcodehelfer.GCodeStrecke(
                        x_ind, (rechts1.y - links.y) * t1 + links.y, aktuelle_hohe,
                        x_ind, (rechts2.y - links.y) * t2 + links.y, aktuelle_hohe
                    )
                )

        if len(links) == 2:
            zwei_links(links[0], links[1], rechts[0])

        elif len(rechts) == 2:
            zwei_rechts(links[0], rechts[0], rechts[1])

        else:
            # Finde den Mittelpunkt
            x_mid = zentral[0].x
            t = (x_mid - links[0].x) / (rechts[0].x - links[0].x)
            y_mid = (rechts[0].y - links[0].y) * t + links[0].y
            mittelpunkt = stl.stl.STLVektor3(x_mid, y_mid, aktuelle_hohe)

            zwei_rechts(links[0], zentral[0], mittelpunkt)
            zwei_links(zentral[0], mittelpunkt, rechts[0])

    # Wenn nicht flach in der Ebene
    # Wie zum Beispiel Seite des Wurfels
    else:
        # Einfach Strecke erstellen
        if len(punkte_in_schicht) == 2:
            strecken.append(
                gcode.gcodehelfer.GCodeStrecke(
                    punkte_in_schicht[0].x, punkte_in_schicht[0].y, aktuelle_hohe,
                    punkte_in_schicht[1].x, punkte_in_schicht[1].y, aktuelle_hohe
                )
            )

        # Schnittpunkte berechnen: Dreieck <-> Ebene
        elif len(punkte_in_schicht) == 0:
            ebene = stl.stl.STLEbene(aktuelle_hohe)
            schnittpunkte = ebene.schnittpunkte_mit_dreieck(dreieck)

            strecken.append(
                gcode.gcodehelfer.GCodeStrecke(
                    schnittpunkte[0].x, schnittpunkte[0].y, aktuelle_hohe,
                    schnittpunkte[1].x, schnittpunkte[1].y, aktuelle_hohe
                )
            )

    return strecken
