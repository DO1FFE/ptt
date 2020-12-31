import serial
import serial.tools.list_ports
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.font as tkFont
from PIL import Image, ImageTk
from pygame import mixer
global ser
global comport

ver = "0.9.1-alpha (GUI)"
root = Tk()
root.title("PTT v"+ver)
#root.geometry("525x175")
root.geometry("525x400")
root.resizable(width=False, height=False)
root.iconbitmap('pics/ptt.ico')
root.config(bg="grey")
icon = ImageTk.PhotoImage(Image.open('pics/ptt.png').resize((100, 100)))
fontStyle = tkFont.Font(family="Lucida Grande", size=18)

label1 = Label(root, image=icon, bg="grey")
label1.grid(row=0, column=0)
label2 = Label(root, text="PTT v"+ver+"\n\xa9 12/2020 by Erik Schauer, DO1FFE", font=fontStyle, bg="grey")
label2.grid(row=0, column=1, columnspan=4)

current_volume = float(0.5)

# COM-Ports aus dem System auslesen und in das Dropdown-Menü einbinden.
OptionList = []
ports = serial.tools.list_ports.comports(include_links=False)
x = 0
for port in ports:
    OptionList.insert(x, port.device)
    x =+1

def com_select(e):
    global ser
    global comport
    comport = com_combo.get()
    ser = serial.Serial(comport)
    com_label.config(text=f"{comport}, 9600,8,N,1")
    com_combo.config(state=DISABLED)
    tx_button.config(text=f"{comport} TX", state=ACTIVE)
    close_com.config(state=ACTIVE)
    status.config(text=f"{comport} geöffnet.")

def senden():
    ser.setRTS(True)
    ser.setDTR(True)
    tx_button.config(state=DISABLED)
    rx_button.config(state=ACTIVE)
    status.config(text=f"TX auf {comport}")

def nicht_senden():
    ser.setRTS(False)
    ser.setDTR(False)
    rx_button.config(state=DISABLED)
    tx_button.config(state=ACTIVE)
    status.config(text=f"Kein TX auf {comport}")

def com_schliessen():
    rx_button.config(state=DISABLED)
    tx_button.config(state=DISABLED)
    close_com.config(state=DISABLED)
    com_combo.config(state=ACTIVE)
    com_label.config(text="<-- COM wählen!")
    status.config(text=f"{comport} geschlossen.")
    ser.setRTS(False)
    ser.setDTR(False)
    ser.close()

status = Label(root, text=f"Willkommen bei PTT v{ver}...", bg="grey", bd=2, relief=SUNKEN, anchor=E)
status.grid(row=10, column=0, columnspan=5, sticky=W+E)

def play_song():
    filename = filedialog.askopenfilename(initialdir="C:/",title="Bitte MP3-Datei auswählen")
    current_song = filename
    song_title = filename.split("/")
    song_title = song_title[-1]
    try:
        mixer.init()
        mixer.music.load(current_song)
        mixer.music.set_volume(current_volume)
        mixer.music.play()
        song_title_label.config(fg="green", bg="grey", text="Wird abgespielt: "+ str(song_title))
        volume_label.config(fg="green", bg="grey", text="Volume: "+ str(current_volume))
    except Exception as e:
        print(e)
        song_title_label.config(fg="red", bg="grey", text="Fehler beim abspielen.")

def reduce_volume():
    try:
        global current_volume
        if current_volume <=0:
            volume_label.config(fg="red", bg="grey", text="Volume : Muted")
            return
        current_volume = current_volume - float(0.1)
        current_volume = round(current_volume,1)
        mixer.music.set_volume(current_volume)
        volume_label.config(fg="green", bg="grey", text="Volume: "+ str(current_volume))
    except Exception as e:
        print(e)
        song_title_label.config(fg="red", bg="grey", text="Keine MP3-Datei ausgewählt.")

def increase_volume():
    try:
        global current_volume
        if current_volume >=1:
            volume_label.config(fg="green", bg="grey", text="Volume : Max")
            return
        current_volume = current_volume + float(0.1)
        current_volume = round(current_volume,1)
        mixer.music.set_volume(current_volume)
        volume_label.config(fg="green", bg="grey", text="Volume: "+ str(current_volume))
    except Exception as e:
        print(e)
        song_title_label.config(fg="red", bg="grey", text="Keine MP3-Datei ausgewählt.")

def pause():
    try:
        mixer.music.pause()
    except Exception as e:
        print(e)
        song_title_label.config(fg="red", bg="grey", text="Keine MP3-Datei ausgewählt.")

def resume():
    try:
        mixer.music.unpause()
    except Exception as e:
        print(e)
        song_title_label.config(fg="red", bg="grey", text="Keine MP3-Datei ausgewählt.")


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


song_title_label = Label(root, font=("Calibri", 12), bg="grey")
song_title_label.grid(sticky="N", row=4, column=1, columnspan=3)
volume_label = Label(root, font=("Calibri", 12), bg="grey")
volume_label.grid(sticky="N", row=6, column=1, columnspan=3)

Button(root, text="MP3-Datei auswählen", font=("Calibri", 12), command=play_song).grid(row=3, columnspan=5,sticky="N")
Button(root, text="Pause", font=("Calibri", 12), command=pause).grid(row=4, columnspan=5,sticky="E")
Button(root, text="Resume", font=("Calibri", 12), command=resume).grid(row=4, columnspan=5,sticky="W")
Button(root, text="+", font=("Calibri", 12),width=5, command=increase_volume).grid(row=6, columnspan=5,sticky="E")
Button(root, text="-", font=("Calibri", 12),width=5, command=reduce_volume).grid(row=6, columnspan=5,sticky="W")

root.mainloop()
ser.setRTS(False)
ser.setDTR(False)
ser.close()
