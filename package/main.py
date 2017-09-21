import stl.stlanalyse
import slicing.slicer
import gcode.gcodehelfer
from copy import deepcopy


def start(stl_datei, parameter, gcode_anfang, gcode_ende, ausgabe_datei):
    # Parse
    stl_data = stl.stlanalyse.stl_analysieren(stl_datei)

    # Slice
    sliced = slicing.slicer.slice(stl_data) # default parameter

    # Export
    gcode.gcodehelfer.export(sliced, ausgabe_datei, gcode_anfang, gcode_ende)

    return stl_data


if __name__ == "__main__":
    start("/home/divadvo/Documents/3DPrinting/Uni/Uni_Programm/tests/models/cube.stl",
          deepcopy(slicing.slicer.DEFAULT_PARAMETERS),
          "/home/divadvo/Documents/3DPrinting/Uni/Uni_Programm/tests/config/anfang.gcode",
          "/home/divadvo/Documents/3DPrinting/Uni/Uni_Programm/tests/config/ende.gcode",
          "/home/divadvo/Documents/3DPrinting/Uni/Uni_Programm/tests/gcode/cube.gcode"
    )

    print('-----------------')

    start("/home/divadvo/Documents/3DPrinting/Uni/Uni_Programm/tests/models/testcube_10mm.stl",
          deepcopy(slicing.slicer.DEFAULT_PARAMETERS),
          "/home/divadvo/Documents/3DPrinting/Uni/Uni_Programm/tests/config/anfang.gcode",
          "/home/divadvo/Documents/3DPrinting/Uni/Uni_Programm/tests/config/ende.gcode",
          "/home/divadvo/Documents/3DPrinting/Uni/Uni_Programm/tests/gcode/testcube_10mm.gcode"
    )


    # print('-----------------')
    #
    # start("/home/divadvo/Documents/3DPrinting/Uni/Uni_Programm/tests/models/yoda.stl",
    #       deepcopy(slicing.slicer.DEFAULT_PARAMETERS),
    #       "/home/divadvo/Documents/3DPrinting/Uni/Uni_Programm/tests/config/anfang.gcode",
    #       "/home/divadvo/Documents/3DPrinting/Uni/Uni_Programm/tests/config/ende.gcode",
    #       "/home/divadvo/Documents/3DPrinting/Uni/Uni_Programm/tests/gcode/yoda.gcode"
    # )


if __name__ == "__main__":
    import math
    print '------- TEST:'
    n = 6
    r = 0.5
    for i in range(n):
        print r * math.cos(2 * math.pi * i / n), r * math.sin(2 * math.pi * i / n)
