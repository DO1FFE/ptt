# import serial
# import time
from tkinter import *

ver = "0.9-alpha (GUI)"
root = Tk()
root.title("PTT v"+ver)
root.geometry("500x400")
root.iconbitmap('ptt.ico')
icon = PhotoImage(file='ptt.png')

label1 = Label(root, image=icon)
label1.grid(column=0, row=0)
auswahl1 = Listbox(root, bg="black", fg="white", width=6)
auswahl1.grid(column=1, row=0)
auswahl1.insert('1', 'COM1')
auswahl1.insert('2', 'COM2')
auswahl1.insert('3', 'COM3')
comport = auswahl1.curselection()
button1_text = "COM benutzen"
button1 = Button(root, text=button1_text)
button1.grid(column=1, row=1)


'''
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
'''
root.mainloop()
