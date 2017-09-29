M107
M104 S200 ; set temperature
G28 ; home all axes
G1 Z5 F5000 ; lift nozzle

M109 S200 ; wait for temperature to be reached
G21 ; set units to millimeters
G90 ; use absolute coordinates
M82 ; use absolute distances for extrusion

G92 E0
G1 Z0.350 F7800.000
G1 E-2.00000 F2400.00000
G92 E0

G1 X100.000 Y0.000 E2.000 F100.000
G1 X100.000 Y100.000 E2.000 F100.000
G1 X0.000 Y100.000 E2.000 F100.000
G1 X0.000 Y0.000 E2.000 F100.000

G92 E0
