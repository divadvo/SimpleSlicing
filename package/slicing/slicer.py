import stl.stl
import aussenwaende
import infill

# Parameter, alle in Millimeter
DEFAULT_PARAMETERS = {
    "infill": 0.2,
    "schicht_hohe": 0.2,
    "dusen_durchmesser": 0.4,
    "start_x": 40.0,
    "start_y": 40.0
}

def slice(stl_data, parameter=DEFAULT_PARAMETERS):
    stl_data.sortiere_dreiecke_nach_z()
    stl_data.verschiebe_zum_ursprung()

    # Strecken berechnen
    rahmen = aussenwaende.generiere_aussenwaende(stl_data, parameter)
    infill_strecken = infill.errechne_infill(stl_data.hilfswerte, parameter, rahmen)

    # Zusammenfugen: Rahmen und Infill
    zusammen = rahmen + infill_strecken

    # Sortiere nach z Achse und infill (erst Rahmen, dann Infill)
    zusammen = sorted(zusammen, key = lambda strecke: (strecke.z1, strecke.infill))

    return zusammen
