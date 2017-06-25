import serial

ser = serial.Serial('/dev/tty.usbserial', 9600)

def get_befehle_an_arduino(gcode_datei):
    with open(gcode_datei, "r") as f:
       zeilen = f.readlines()

    zeilen = [zeile.strip() for zeile in zeilen]
    return zeilen

def sende_befehl_an_arduino(befehl):
    ser.write(befehl + '\n')
