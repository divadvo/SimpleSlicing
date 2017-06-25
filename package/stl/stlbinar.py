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


def read_dreieck(f):
    normalenvektor = read_vec3(f)
    v0 = read_vec3(f)
    v1 = read_vec3(f)
    v2 = read_vec3(f)
    attributes = read_UINT16(f)

    return stl.STLDreieck(normalenvektor, v0, v1, v2, attributes)


def read_vec3(f):
    x = read_float(f)
    y = read_float(f)
    z = read_float(f)

    return stl.STLVektor3(x, y, z)


def read_float(f):
    float_bytes = f.read(4)
    return struct.unpack('f', float_bytes)[0]


def read_UINT16(f):
    uint16_bytes = f.read(2)
    return struct.unpack('H', uint16_bytes)[0]
