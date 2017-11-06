import stl
import struct

def stl_binar_analysieren(stl_datei):
    with open(stl_datei, "rb") as f:
        header = f.read(80)

        anzahl_dreiecke = read_unsigned_int(f)
        dreiecke = []

        for i in range(anzahl_dreiecke):
            dreieck = read_dreieck(f)
            dreiecke.append(dreieck)

        stl_data = stl.STLData(header, dreiecke, True)
        return stl_data


def read_unsigned_int(f):
    uint_bytes = f.read(4)
    return struct.unpack('I', uint_bytes)[0]

# Man muss alle Informationen auslesen, weil ich nicht auf eine bestimmte Zeile 
# zugreifen kann und es nicht markiert ist, wo Informationen anfangen/zu Ende sind
def read_dreieck(f):
    normalenvektor = lese_vec3(f)
    v0 = lese_vec3(f)
    v1 = lese_vec3(f)
    v2 = lese_vec3(f)
    attributes = lese_UINT16(f)

    return stl.STLDreieck(normalenvektor, v0, v1, v2, attributes)


def lese_vec3(f):
    x = lese_float(f)
    y = lese_float(f)
    z = lese_float(f)

    return stl.STLVektor3(x, y, z)


def lese_float(f):
    float_bytes = f.read(4)
    return struct.unpack('f', float_bytes)[0]


def lese_UINT16(f):
    uint16_bytes = f.read(2)
    return struct.unpack('H', uint16_bytes)[0]
