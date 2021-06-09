import threading
import tkinter.font as tkFont
from time import sleep
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

import pygame
import pygame._sdl2 as sdl2
import serial
import serial.tools.list_ports
from PIL import Image, ImageTk
from pygame import mixer

global ser
global comport
global start
global tot_timer

on_air = False

__version__ = "0.9.9-alpha (GUI)"
root = Tk()
root.title("PTT v" + __version__)
# root.geometry("525x175")
# root.geometry("525x435")
root.resizable(width=False, height=False)
#root.iconbitmap('pics/ptt.ico')
root.config(bg="grey")
icon = ImageTk.PhotoImage(Image.open('/pics/ptt.png').resize((100, 100)))
#icon = ImageTk.PhotoImage(Image.open('ptt.png').resize((100, 100)))
fontStyle = tkFont.Font(family="Lucida Grande", size=18)

label1 = Label(root, image=icon, bg="grey")
label1.grid(row=0, column=0)
label2 = Label(root, text="PTT v" + __version__ + "\n\xa9 03/2021 by Erik Schauer, DO1FFE", font=fontStyle, bg="grey")
label2.grid(row=0, column=1, columnspan=4)

current_volume = float(0.5)
tot_timer = 0

# COM-Ports aus dem System auslesen und in das Dropdown-Menü einbinden.
OptionList = []
ports = serial.tools.list_ports.comports(include_links=False)
x = 0
for port in ports:
    OptionList.insert(x, port.device)
    x = +1

# Wiedergabe-Devices auslesen und in das Dropdown-Menü einbinden.
WiedergabeDevice = []
pygame.init()
is_capture = 0  # zero to request playback devices, non-zero to request recording devices
num = sdl2.get_num_audio_devices(is_capture)
names = [str(sdl2.get_audio_device_name(i, is_capture), encoding="utf-8") for i in range(num)]
# print("\n".join(names))
WiedergabeDevice = names
pygame.quit()

# Aufnahme-Devices auslesen und in das Dropdown-Menü einbinden.
AufnahmeDevice = []
pygame.init()
is_capture = 1  # zero to request playback devices, non-zero to request recording devices
num = sdl2.get_num_audio_devices(is_capture)
names = [str(sdl2.get_audio_device_name(i, is_capture), encoding="utf-8") for i in range(num)]
# print("\n".join(names))
AufnahmeDevice = names
pygame.quit()

# print(WiedergabeDevice)
# print(AufnahmeDevice)

tot_times = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def tot(tot_timer):
    while on_air and tot_timer != 0:
        print(f"Schlafe {tot_timer} Minute(n)...")
        timer = int(tot_timer) * 60
        sleep(timer)
        mixer.music.pause()
        ser.setRTS(False)
        ser.setDTR(False)
        print("PAUSE")
        sleep(1)
        print("UNPAUSE")
        ser.setRTS(True)
        ser.setDTR(True)
        mixer.music.unpause()


def tot_auswahl(e):
    global tot_timer
    tot_timer = tot_combo.get()


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

def tx():
    t1 = threading.Thread(target=senden)
    t1.start()

def senden():
    global on_air
    on_air = True
    ser.setRTS(True)
    ser.setDTR(True)
    tx_button.config(state=DISABLED)
    rx_button.config(state=ACTIVE)
    status.config(text=f"TX auf {comport}")
    while tot_timer != 0:
        tot1 = threading.Thread(target=tot(tot_timer))
        tot1.start()


def nicht_senden():
    global on_air
    on_air = False
    ser.setRTS(False)
    ser.setDTR(False)
    rx_button.config(state=DISABLED)
    tx_button.config(state=ACTIVE)
    status.config(text=f"Kein TX auf {comport}")
    stop()


def com_schliessen():
    global on_air
    on_air = False
    rx_button.config(state=DISABLED)
    tx_button.config(state=DISABLED)
    close_com.config(state=DISABLED)
    com_combo.config(state=ACTIVE)
    com_label.config(text="<-- COM wählen!")
    status.config(text=f"{comport} geschlossen.")
    ser.setRTS(False)
    ser.setDTR(False)
    ser.close()
    stop()


status = Label(root, text=f"Willkommen bei PTT v{__version__}...", bg="grey", bd=2, relief=SUNKEN, anchor=E)
status.grid(row=10, column=0, columnspan=5, sticky=W + E)


def open_song():
    global current_song
    global song_title
    filename = filedialog.askopenfilename(initialdir="C:/", title="Bitte MP3-Datei auswählen")
    current_song = filename
    song_title = filename.split("/")
    song_title = song_title[-1]


def volume(x):
    mixer.music.set_volume(volume_slider.get())
    cur_vol = float(volume_slider.get()) * 100
    cur_vol = int(cur_vol)
    volume_text.config(text=cur_vol, bg="grey")


def play():
    try:
        mixer.pre_init(devicename=play_device)
        mixer.init()
        mixer.music.load(current_song)
        # mixer.music.set_volume(current_volume)
        mixer.music.play()
        song_title_label.config(fg="green", bg="grey", text="Wird abgespielt: " + str(song_title))
    except Exception as e:
        print(e)
        song_title_label.config(fg="red", bg="grey", text="Fehler beim abspielen.")


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

tx_button = Button(root, text="NO TX", state=DISABLED, command=tx)
tx_button.grid(row=1, column=3)

rx_button = Button(root, text="TX AUS", state=DISABLED, command=nicht_senden)
rx_button.grid(row=1, column=4)

close_com = Button(root, text="COM-Port schliessen", state=DISABLED, command=com_schliessen)
close_com.grid(row=2, column=0)

tot_frame = LabelFrame(root, text="TOT in Min.", bg="gray")
tot_frame.grid(row=2, column=3)
tot_combo = ttk.Combobox(tot_frame, value=tot_times)
tot_combo.config(width=4, font=('Helvetica', 12))
tot_combo.pack()
tot_combo.bind("<<ComboboxSelected>>", tot_auswahl)

song_title_box = LabelFrame(root, bg="grey")
song_title_box.grid(sticky="N", row=4, column=0, columnspan=5)
song_title_label = Label(song_title_box, font=("Calibri", 12), bg="grey")
song_title_label.pack()

Button(root, text="Audio-Datei auswählen", font=("Calibri", 12), command=open_song).grid(row=3, columnspan=5,
                                                                                         sticky="N")
button_frame = LabelFrame(root, text="Steuerung", bg="gray")
button_frame.grid(row=5, rowspan=4, column=0, pady=20)
Button(button_frame, text="Play", font=("Calibri", 12), fg="gray", command=play).pack(pady=5)
Button(button_frame, text="Pause", font=("Calibri", 12), command=pause).pack(pady=5)
Button(button_frame, text="Resume", font=("Calibri", 12), command=resume).pack(pady=5)
Button(button_frame, text="Stop", font=("Calibri", 12), command=stop).pack(pady=5)

volume_frame = LabelFrame(root, text="Volume", bg="gray")
volume_frame.grid(row=5, rowspan=4, column=1, pady=20)
volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, value=1, command=volume)
volume_slider.pack(pady=10)
volume_text = Label(volume_frame, text="100", bg="gray")
volume_text.pack()

sound_frame = LabelFrame(root, text="Sounddevices", bg="gray")
sound_frame.grid(row=5, rowspan=4, column=2, columnspan=3)
wiedergabe_box = LabelFrame(sound_frame, text="Output", bg="gray")
wiedergabe_box.pack(pady=10, padx=10)
wiedergabe_combo = ttk.Combobox(wiedergabe_box, value=WiedergabeDevice)
wiedergabe_combo.config(width=20, font=('Helvetica', 10))
wiedergabe_combo.pack(pady=10, padx=10)
wiedergabe_combo.bind("<<ComboboxSelected>>", wiedergabe_select)

aufnahme_box = LabelFrame(sound_frame, text="Input", bg="gray")
aufnahme_box.pack(pady=10, padx=10)
aufnahme_combo = ttk.Combobox(aufnahme_box, value=AufnahmeDevice, state=DISABLED)
aufnahme_combo.config(width=20, font=('Helvetica', 10))
aufnahme_combo.pack(pady=10, padx=10)
aufnahme_combo.bind("<<ComboboxSelected>>", aufnahme_select)

root.mainloop()
on_air = False
ser.setRTS(False)
ser.setDTR(False)
ser.close()
stop()
mixer.stop()
