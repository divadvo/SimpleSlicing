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