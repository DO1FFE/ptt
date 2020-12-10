import serial
import time
# import serial.tools.list_ports
#
ver = "1.0.0"
print("###########################################################")
print("# PTT Emulator v"+ver+" (c) 12/2020 by Erik Schauer, DO1FFE #")
print("###########################################################")
print("\n\n")
com = input("Welchen COM-Port [1/2/3/..]? : ")
comport = "COM"+com
print("Öffne "+comport+"...")
ser = serial.Serial(comport)
print("OK")
print("\n\nEingabe 1 = RTS AN | 0 = RTS AUS | \"x\" beendet das Programm!")
onoff = "0"
while onoff != "x":
    time.sleep(1)
    onoff = input("RTS [0/1/x]? : ")
    if onoff == "0":
        print("RTS auf COM"+com+" AUS.")
        ser.setRTS(False)
        ser.setDTR(False)
    elif onoff == "1":
        print("RTS auf COM"+com+" AN.")
        ser.setRTS(True)
        ser.setDTR(True)
else:
    print("RTS auf COM"+com+" AUS.")
    ser.setRTS(False)
    ser.setDTR(False)
    print("Schliesse COM"+com+"...")
    ser.close()

print("Programm beendet...")
time.sleep(3)
