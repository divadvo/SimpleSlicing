import stl.stl
import aussenwaende
import infill

# Parameter, alle in Millimeter
DEFAULT_PARAMETERS = {
    "infill": 0.2,
    "layer_height": 0.2,
    "nozzle_diameter": 0.4,
    "start_x": 40.0,
    "start_y": 40.0
}

def slice(stl_data, parameter=DEFAULT_PARAMETERS):
    stl_data.sortiere_dreiecke_nach_z()
    stl_data.verschiebe_zum_ursprung()

    # Strecken berechnen
    perimeters = aussenwaende.generiere_aussenwaende(stl_data, parameter)
    infill_result = infill.generate_infill_and_supports(stl_data.hilfswerte, parameter, perimeters)

    # Zusammenfugen: Rahmen und Infill
    sliced = perimeters + infill_result

    # Sortiere nach z Achse und infill (erst Rahmen, dann Infill)
    sliced = sorted(sliced, key = lambda strecke: (strecke.z1, strecke.infill))

    return sliced
