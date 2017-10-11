from __future__ import division 
import math
import numpy as np
import stl.stl
import gcode.gcodehelfer


class InfillGerade:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

class Pattern:
    def __init__(self, unit, hilfswerte):
        # Erstelle das Gitter
        import math
        minX = 0
        minY = 0
        maxX = int(math.ceil(hilfswerte.max.x - hilfswerte.min.x))
        maxY = int(math.ceil(hilfswerte.max.y - hilfswerte.min.y))
        unitInt = int(unit)

        self.strecken = []
        for i in range(minX, maxX, unitInt):
            self.strecken.append(InfillGerade(i, minY, i, maxY))
        
        for i in range(minY, maxY, unitInt):
            self.strecken.append(InfillGerade(minX, i, maxX, i))

    def schnittpunkte_alle(self, perimeters):
        schnittpunkte = []
        for gerade in self.strecken:
            schnittpunkte.extend(self.schnittpunkte_errechnen(gerade, perimeters))
        return schnittpunkte

    # Berechne alle Schnittpunkte mit einer Strecke
    def schnittpunkte_errechnen(self, gerade, perimeters):
        schnittpunkte = []
        for strecke in perimeters:
            intersect = self.get_line_intersection(gerade, strecke)
            if intersect is not False:
                schnittpunkte.append(intersect)
        return schnittpunkte

    # Schnittpunkt von 2 Strecken (nicht geraden)
    def get_line_intersection(self, p, q):
        s1_x = p.x2 - p.x1
        s1_y = p.y2 - p.y1
        s2_x = q.x2 - q.x1
        s2_y = q.y2 - q.y1

        denom = s1_x * s2_y - s2_x * s1_y
        if denom == 0:
            return False

        s = (-s1_y * (p.x1 - q.x1) + s1_x * (p.y1 - q.y1)) / (-s2_x * s1_y + s1_x * s2_y)
        t = ( s2_x * (p.y1 - q.y1) - s2_y * (p.x1 - q.x1)) / (-s2_x * s1_y + s1_x * s2_y)

        if s >= 0 and s <= 1 and t >= 0 and t <= 1:
            return p.x1 + (t * s1_x), p.y1 + (t * s1_y)
        else:
            return False



def generate_infill_and_supports(hilfswerte, parameter, perimeters):
    if parameter["infill"] == 0:
            return []

    max_x = hilfswerte.max.x - hilfswerte.min.x
    max_y = hilfswerte.max.y - hilfswerte.min.y
    max_z = hilfswerte.max.z - hilfswerte.min.z
    unit = math.sqrt(max_x * max_y) * (1.00000001 - parameter["infill"]) / 2 #4

    pattern = Pattern(unit, hilfswerte)

    infill = []

    # Progressbar
    import wx
    progressMax = 100
    dialog = wx.ProgressDialog("Infill", "Bitte warten", progressMax,
            style=wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_SMOOTH | wx.PD_AUTO_HIDE)

    for z_off in np.arange(0, max_z, parameter["layer_height"]):
        percentage = z_off / max_z * 100
        dialog.Update(percentage)

        # Nur in derzeitigen Schicht 
        schnittpunkte = pattern.schnittpunkte_alle([x for x in perimeters if x.z1 == z_off])
        for i in range(0, len(schnittpunkte), 2):
            if i+1 < len(schnittpunkte):
                P1 = schnittpunkte[i]
                P2 = schnittpunkte[i+1]
                infill.append(gcode.gcodehelfer.GCodeStrecke(P1[0], P1[1], z_off, P2[0], P2[1], z_off, True))

    dialog.Destroy()

    return infill
