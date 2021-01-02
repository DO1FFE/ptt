import serial
import serial.tools.list_ports
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.font as tkFont
from PIL import Image, ImageTk
import pygame
import pygame._sdl2 as sdl2
from pygame import mixer
global ser
global comport


ver = "0.9.2-alpha (GUI)"
root = Tk()
root.title("PTT v"+ver)
#root.geometry("525x175")
root.geometry("525x435")
#root.resizable(width=False, height=False)
root.iconbitmap('pics/ptt.ico')
root.config(bg="grey")
icon = ImageTk.PhotoImage(Image.open('pics/ptt.png').resize((100, 100)))
fontStyle = tkFont.Font(family="Lucida Grande", size=18)

label1 = Label(root, image=icon, bg="grey")
label1.grid(row=0, column=0)
label2 = Label(root, text="PTT v"+ver+"\n\xa9 01/2021 by Erik Schauer, DO1FFE", font=fontStyle, bg="grey")
label2.grid(row=0, column=1, columnspan=4)

current_volume = float(0.5)

# COM-Ports aus dem System auslesen und in das Dropdown-Menü einbinden.
OptionList = []
ports = serial.tools.list_ports.comports(include_links=False)
x = 0
for port in ports:
    OptionList.insert(x, port.device)
    x =+1

# Wiedergabe-Devices auslesen und in das Dropdown-Menü einbinden.
WiedergabeDevice = []
pygame.init()
x = 0
is_capture = 0  # zero to request playback devices, non-zero to request recording devices
num = sdl2.get_num_audio_devices(is_capture)
names = [str(sdl2.get_audio_device_name(i, is_capture), encoding="utf-8") for i in range(num)]
#print("\n".join(names))
WiedergabeDevice.insert(x, "".join(names))
x =+1
pygame.quit()

# Aufnahme-Devices auslesen und in das Dropdown-Menü einbinden.
AufnahmeDevice = []
pygame.init()
x = 0
is_capture = 1  # zero to request playback devices, non-zero to request recording devices
num = sdl2.get_num_audio_devices(is_capture)
names = [str(sdl2.get_audio_device_name(i, is_capture), encoding="utf-8") for i in range(num)]
#print("\n".join(names))
AufnahmeDevice.insert(x, "".join(names))
x =+1
pygame.quit()

#print(WiedergabeDevice)
#print(AufnahmeDevice)

def wiedergabe_select(e):
    global play_device
    play_device = wiedergabe_combo.get()

def aufnahme_select(e):
    global rec_device
    rec_device = aufnahme_combo.get()

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
        mixer.pre_init(devicename=play_device)
        mixer.init()
        mixer.music.load(current_song)
        #mixer.music.set_volume(current_volume)
        mixer.music.play()
        song_title_label.config(fg="green", bg="grey", text="Wird abgespielt: "+ str(song_title))
#        volume_label.config(fg="green", bg="grey", text="Volume: "+ str(current_volume))
    except Exception as e:
        print(e)
        song_title_label.config(fg="red", bg="grey", text="Fehler beim abspielen.")

def volume(x):
    mixer.music.set_volume(volume_slider.get())
    cur_vol = float(volume_slider.get()) * 100
    cur_vol = int(cur_vol)
    volume_text.config(text=cur_vol, bg="gray")

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

def stop():
    try:
        mixer.music.stop()
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
song_title_label.grid(sticky="N", row=7, column=1, columnspan=3)
#volume_label = Label(root, font=("Calibri", 12), bg="grey")
#volume_label.grid(sticky="N", row=6, column=1, columnspan=3)

Button(root, text="MP3-Datei auswählen", font=("Calibri", 12), command=play_song).grid(row=3, columnspan=5, sticky="N")
Button(root, text="Pause", font=("Calibri", 12), command=pause).grid(row=4, column=0)
Button(root, text="Resume", font=("Calibri", 12), command=resume).grid(row=5, column=0)
Button(root, text="Stop", font=("Calibri", 12), command=stop).grid(row=6, column=0)
#Button(root, text="+", font=("Calibri", 12), width=5, command=increase_volume).grid(row=6, column=0)
#Button(root, text="-", font=("Calibri", 12), width=5, command=reduce_volume).grid(row=6, column=1)
volume_frame = LabelFrame(root, text="Volume", bg="gray")
volume_frame.grid(row=4, rowspan=3, column=1, pady=20)
volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=1, command=volume)
volume_slider.pack(pady=10)
volume_text = Label(volume_frame, text="100", bg="gray")
volume_text.pack()

sound_frame = LabelFrame(root, text="Sounddevices", bg="gray")
sound_frame.grid(row=4, column=2, columnspan=3)

wiedergabe_combo = ttk.Combobox(sound_frame, value=WiedergabeDevice)
wiedergabe_combo.config(width=20, font=('Helvetica', 10))
wiedergabe_combo.pack(pady=10, padx=10)
wiedergabe_combo.bind("<<ComboboxSelected>>", wiedergabe_select)

aufnahme_combo = ttk.Combobox(sound_frame, value=AufnahmeDevice)
aufnahme_combo.config(width=20, font=('Helvetica', 10))
aufnahme_combo.pack(pady=10, padx=10)
aufnahme_combo.bind("<<ComboboxSelected>>", aufnahme_select)



root.mainloop()
ser.setRTS(False)
ser.setDTR(False)
ser.close()
