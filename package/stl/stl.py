from __future__ import division

class STLData:
    def __init__(self, header, dreiecke, ist_binar):
        self.header = header
        self.dreiecke = dreiecke
        self.ist_binar = ist_binar
        self.hilfswerte_berechnen()

    def hilfswerte_berechnen(self):
        # Alle Eckpunkte nehmen
        alle_dreieck_eckpunkte = []
        for dreieck in self.dreiecke:
            for eckpunkt_vektor in dreieck.eckpunkte:
                alle_dreieck_eckpunkte.append(eckpunkt_vektor)

        # Die kleinsten Koordinaten
        min_vektor = STLVektor3(
            min(alle_dreieck_eckpunkte, key=lambda v: v.x).x,
            min(alle_dreieck_eckpunkte, key=lambda v: v.y).y,
            min(alle_dreieck_eckpunkte, key=lambda v: v.z).z
        )

        # Die grossten Koordinaten
        max_vektor = STLVektor3(
            max(alle_dreieck_eckpunkte, key=lambda v: v.x).x,
            max(alle_dreieck_eckpunkte, key=lambda v: v.y).y,
            max(alle_dreieck_eckpunkte, key=lambda v: v.z).z
        )

        self.hilfswerte = STLHilfsWerte(min_vektor, max_vektor)

    def verschiebe_zum_ursprung(self):
        # Vektor: Verschiebung vom Ursprung
        vektor_verschiebung = self.hilfswerte.min.skalarmultiplikation(-1.0)

        # Verschiebe alle Dreiecke
        for dreieck in self.dreiecke:
            dreieck.verschieben(vektor_verschiebung)

        # Update hilfswerte
        # self.hilfswerte_berechnen()

    def sortiere_dreiecke_nach_z(self):
        # Sortiere nach z-Wert (von unten nach oben)

        # Gucke auf alle eckpunkte und nehme den kleinsten z-Wert
        # Sortiere alle Dreiecke nach diesem Wert
        self.dreiecke.sort(key=lambda dreieck: min(eckpunkt.z for eckpunkt in dreieck.eckpunkte))


class STLHilfsWerte:
    def __init__(self, min_vektor, max_vektor):
        self.min = min_vektor
        self.max = max_vektor


class STLDreieck:
    def __init__(self, normalenvektor, e0 = None, e1 = None, e2 = None, attributes = None):
        self.normalenvektor = normalenvektor
        self.eckpunkte = [e0, e1, e2]
        self.attributes = attributes

    def verschieben(self, vektor_verschiebung):
        # Verschiebe alle Eckpunkte und speicher sie
        self.eckpunkte = [(eckpunkt + vektor_verschiebung) for eckpunkt in self.eckpunkte]

    def __str__(self):
        return "{}".format(self.eckpunkte)

    def __repr__(self):
        return "{}".format(self.eckpunkte)


class STLVektor3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return STLVektor3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return STLVektor3(self.x - other.x, self.y - other.y, self.z - other.z)

    def verschieben(self, vektor_verschiebung):
        self.x += vektor_verschiebung.x
        self.y += vektor_verschiebung.y
        self.z += vektor_verschiebung.z

    def skalarmultiplikation(self, skalar):
        return STLVektor3(skalar * self.x, skalar * self.y, skalar * self.z)

    def skalarprodukt(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __str__(self):
        return "({} {} {})".format(self.x, self.y, self.z)

    def __repr__(self):
        return "({} {} {})".format(self.x, self.y, self.z)

class STLEbene:
    def __init__(self, z):
        # n*x + d = 0
        self.normalenvektor = STLVektor3(0, 0, 1)
        self.d = -z

    def schnittpunkte_mit_dreieck(self, dreieck):
        eckpunkte = dreieck.eckpunkte
        schnittpunkte = []

        # A B
        schnittpunkt = self.schnittpunkt_mit_strecke(eckpunkte[0], eckpunkte[1])
        schnittpunkte += [schnittpunkt] if schnittpunkt is not None else []

        # B C
        schnittpunkt = self.schnittpunkt_mit_strecke(eckpunkte[1], eckpunkte[2])
        schnittpunkte += [schnittpunkt] if schnittpunkt is not None else []

        # A C
        schnittpunkt = self.schnittpunkt_mit_strecke(eckpunkte[0], eckpunkte[2])
        schnittpunkte += [schnittpunkt] if schnittpunkt is not None else []

        return schnittpunkte

    def abstand_ebene_punkt(self, punkt):
        # n*p + d
        return self.normalenvektor.skalarprodukt(punkt) + self.d

    def schnittpunkt_mit_strecke(self, punkt1, punkt2):
        abstand1 = self.abstand_ebene_punkt(punkt1)
        abstand2 = self.abstand_ebene_punkt(punkt2)

        # Punkte auf der gleichen Seite der Ebene
        if abstand1 * abstand2 > 0:
            return None

        # TODO: / 0 ???
        t = abstand1 / (abstand1 - abstand2) # __future__ division!!!
        schnittpunkt = punkt1 + (punkt2 - punkt1).skalarmultiplikation(t)
        return schnittpunkt

if __name__ == "__main__":
    pass
    #ebene = STLEbene(1)
    #dreieck = STLDreieck(STLVektor3(0,1,0), STLVektor3(0,0,0), STLVektor3(0,0,2), STLVektor3(1,0,0))
    #punkt = STLVektor3(0,0,1)
    #print ebene.abstand_ebene_punkt(punkt)
    #print ebene.schnittpunkte_mit_dreieck(dreieck)
