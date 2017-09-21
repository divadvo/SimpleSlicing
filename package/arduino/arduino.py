import serial

#ser = serial.Serial('/dev/tty.usbserial', 9600)

def sende_befehl(befehl):
    print befehl
    #ser.write(befehl + '\n')
    # while True:
    #     if "$" in ser.readline()
    #         return
    import time
    time.sleep(0.0005)
