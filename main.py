# import serial
# import time
from tkinter import *
import tkinter.font as tkFont
from PIL import Image, ImageTk

ver = "0.9-alpha (GUI)"
root = Tk()
root.title("PTT v"+ver)
root.geometry("600x400")
root.iconbitmap('ptt.ico')
icon = ImageTk.PhotoImage(Image.open('ptt.png').resize((100, 100)))
fontStyle = tkFont.Font(family="Lucida Grande", size=20)
global comport

label1 = Label(root, image=icon)
label1.grid(column=0, row=0)
label2 = Label(root, text="PTT v"+ver+"\n\xa9 12/2020 by Erik Schauer, DO1FFE", font=fontStyle)
label2.grid(column=1, row=0, padx=20)

OptionList = [
"COM1",
"COM2",
"COM3",
"COM4"
]

variable = StringVar(root)
variable.set(OptionList[0])

auswahl1 = OptionMenu(root, variable, *OptionList)
auswahl1.config(width=7, font=('Helvetica', 12))
auswahl1.grid(column=0, row=1, pady=20)

def callback(*args):
    button1.configure(text="{} benutzen...".format(variable.get()))
    comport = format(variable.get())


button1_text = "COM-Port auswählen"
button1 = Button(root, text=button1_text)
button1.grid(column=0, row=2, pady=5)

variable.trace("w", callback)
print(comport)
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
