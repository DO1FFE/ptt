import serial
# import time
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
from PIL import Image, ImageTk

global ser
global comport

ver = "0.9-alpha (GUI)"
root = Tk()
root.title("PTT v"+ver)
root.geometry("600x200")
root.iconbitmap('ptt.ico')
root.config(bg="grey")
icon = ImageTk.PhotoImage(Image.open('ptt.png').resize((100, 100)))
fontStyle = tkFont.Font(family="Lucida Grande", size=18)

label1 = Label(root, image=icon, bg="grey")
label1.grid(row=0, column=0)
label2 = Label(root, text="PTT v"+ver+"\n\xa9 12/2020 by Erik Schauer, DO1FFE", font=fontStyle, bg="grey")
label2.grid(row=0, column=1, columnspan=4)

OptionList = [
    "COM1",
    "COM2",
    "COM3",
    "COM4"
]

def com_select(e):
    global ser
    global comport
    comport = com_combo.get()
    ser = serial.Serial(comport)
    com_label.config(text=f"{comport}, 9600,8,N,1")
    com_combo.config(state=DISABLED)
    tx_button.config(text=f"{comport} TX", state=ACTIVE)
    close_com.config(state=ACTIVE)

def senden():
    ser.setRTS(True)
    ser.setDTR(True)
    tx_button.config(state=DISABLED)
    rx_button.config(state=ACTIVE)

def nicht_senden():
    ser.setRTS(False)
    ser.setDTR(False)
    rx_button.config(state=DISABLED)
    tx_button.config(state=ACTIVE)

def com_schliessen():
    rx_button.config(state=DISABLED)
    tx_button.config(state=DISABLED)
    close_com.config(state=DISABLED)
    com_combo.config(state=ACTIVE)
    com_label.config(text="<-- COM wählen!")
    ser.setRTS(False)
    ser.setDTR(False)
    ser.close()

com_combo = ttk.Combobox(root, value=OptionList)
com_combo.config(width=7, font=('Helvetica', 12))
com_combo.grid(row=1, column=0)
com_combo.bind("<<ComboboxSelected>>", com_select)

com_label = Label(root, text="<-- COM wählen!")
com_label.config(width=20, font=('Helvetica', 12))
com_label.grid(row=1, column=1)

tx_button = Button(root, text="NO TX", state=DISABLED, command=senden)
tx_button.grid(row=1, column=3)

rx_button = Button(root, text="TX AUS", state=DISABLED, command=nicht_senden)
rx_button.grid(row=1, column=4)

close_com = Button(root, text="COM-Port schliessen", state=DISABLED, command=com_schliessen)
close_com.grid(row=2, column=0)

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
ser.setRTS(False)
ser.setDTR(False)
ser.close()