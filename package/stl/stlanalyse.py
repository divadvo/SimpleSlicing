import stlbinar
import stlascii

# Analysiert STL und gibt die Daten zuruck.
# Ruft dafur eine andere Funktion auf, je nach Art der STL
def stl_analysieren(stl_datei):
    if ist_stl_binar(stl_datei):
        return stlbinar.stl_binar_analysieren(stl_datei)
    else:
        return stlascii.stl_ascii_analysieren(stl_datei)

# Entscheided welcher Typ von STL vorliegt
def ist_stl_binar(stl_datei):
    with open(stl_datei, "r") as f:
        erste_zeile = f.readline().strip() # Erste Zeile ohne Lehrzeichen
        # ASCII STL fangt mit 'solid ...' an
        return not erste_zeile.startswith('solid')
