import math
import numpy as np
import stl.stl
import gcode.gcodehelfer

class Quadrat:
    def __init__(self, unit, x=0, y=0):
        # oben, unten, rechts, links
        self.unit = unit
        self.x = x
        self.y = y

        self.o = (x + 0,            y + 0.5 * unit)
        self.u = (x + 0,            y + -0.5 * unit)
        self.r = (x + 0.5 * unit,   y +  0)
        self.l = (x + -0.5 * unit,  y + 0)

    def get_alle_strecken(self):
        return [
            (self.o, self.r),
            (self.r, self.u),
            (self.u, self.l),
            (self.l, self.o)
        ]

    def fuelle_flache(self, max_x, max_y):
        quadrate = []
        for x_off in np.arange(0, max_x + self.unit, self.unit):
            for y_off in np.arange(0, max_y + self.unit, self.unit):
                quadrate.append(Quadrat(self.unit, self.x + x_off, self.y + y_off))

        strecken = []
        for quadrat in quadrate:
            strecken += quadrat.get_alle_strecken()

        return strecken



def generate_infill_and_supports(hilfswerte, parameter, perimeters):
    if parameter["infill"] == 0:
            return []

    max_x = hilfswerte.max.x - hilfswerte.min.x
    max_y = hilfswerte.max.y - hilfswerte.min.y
    max_z = hilfswerte.max.z - hilfswerte.min.z
    unit = math.sqrt(max_x * max_y) * (1.00000001 - parameter["infill"]) / 2

    quadrat = Quadrat(unit)
    strecken = quadrat.fuelle_flache(max_x, max_y)

    # TODO: round strecken

    result = [strecke for strecke in strecken if
        0 <= round(strecke[0][0], 2) <= max_x and
        0 <= round(strecke[1][0], 2) <= max_x and

        0 <= round(strecke[0][1], 2) <= max_y and
        0 <= round(strecke[1][1], 2) <= max_y
    ]

    infill = []
    for z_off in np.arange(0, max_z, parameter["layer_height"]):
        infill += [gcode.gcodehelfer.GCodeStrecke(x1, y1, z_off, x2, y2, z_off) for ((x1, y1), (x2, y2)) in result]

    return infill
