import threading
import tkinter.font as tkFont
from time import sleep
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

import pygame
import pygame._sdl2 as sdl2
import pyaudio
import serial
import serial.tools.list_ports
from PIL import Image, ImageTk
from pygame import mixer

global ser
global comport
global start
global tot_timer
global mic_to_speaker_running

on_air = False
mic_to_speaker_running = False

__version__ = "2023.4.1-alpha (GUI)"
root = Tk()
root.title("PTT v" + __version__)
root.resizable(width=False, height=False)
root.config(bg="grey")
icon = ImageTk.PhotoImage(Image.open('/pics/ptt.png').resize((100, 100)))
fontStyle = tkFont.Font(family="Lucida Grande", size=18)

label1 = Label(root, image=icon, bg="grey")
label1.grid(row=0, column=0)
label2 = Label(root, text="PTT v" + __version__ + "\n\xa9 03/2021 by Erik Schauer, DO1FFE", font=fontStyle, bg="grey")
label2.grid(row=0, column=1, columnspan=4)

current_volume = float(0.5)
tot_timer = 0

OptionList = []
ports = serial.tools.list_ports.comports(include_links=False)
x = 0
for port in ports:
    OptionList.insert(x, port.device)
    x = +1

WiedergabeDevice = []
pygame.init()
is_capture = 0
num = sdl2.get_num_audio_devices(is_capture)
names = [str(sdl2.get_audio_device_name(i, is_capture), encoding="utf-8") for i in range(num)]
WiedergabeDevice = names
pygame.quit()

AufnahmeDevice = []
pygame.init()
is_capture = 1
num = sdl2.get_num_audio_devices(is_capture)
names = [str(sdl2.get_audio_device_name(i, is_capture), encoding="utf-8") for i in range(num)]
AufnahmeDevice = names
pygame.quit()

tot_times = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def tot(tot_timer):
    while on_air and tot_timer != 0:
        print(f"Schlafe {tot_timer} Minute(n)...")
        timer = int(tot_timer) * 60 - 2
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
    status.config(text=f"{comport} geöffnet")

def close_com_click():
    global ser
    global comport
    ser.close()
    com_label.config(text="Kein COM-Port ausgewählt")
    com_combo.config(state=ACTIVE)
    tx_button.config(text="TX", state=DISABLED)
    close_com.config(state=DISABLED)
    status.config(text=f"{comport} geschlossen")

def load_mp3():
    filename = filedialog.askopenfilename(initialdir="/", title="MP3 Datei öffnen", filetypes=(("MP3 files", "*.mp3"), ("all files", "*.*")))
    if filename:
        mixer.init()
        mixer.music.load(filename)
        song_label.config(text=f"{filename}")
        play_button.config(state=ACTIVE)
        vol_button.config(state=ACTIVE)

def play_mp3():
    global on_air
    on_air = not on_air
    if on_air:
        play_button.config(text="Stop")
        ser.setRTS(True)
        ser.setDTR(True)
        mixer.music.play()
        if tot_timer > 0:
            threading.Thread(target=tot, args=(tot_timer,)).start()
    else:
        play_button.config(text="Play")
        ser.setRTS(False)
        ser.setDTR(False)
        mixer.music.stop()

def mic_to_speaker():
    global mic_to_speaker_running
    mic_to_speaker_running = not mic_to_speaker_running

    if mic_to_speaker_running:
        mic_button.config(text="Stop")
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100

        p = pyaudio.PyAudio()

        stream_in = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=AufnahmeDevice.index(rec_device))
        stream_out = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK, output_device_index=WiedergabeDevice.index(play_device))

        def callback():
            while mic_to_speaker_running:
                data = stream_in.read(CHUNK)
                stream_out.write(data)

        threading.Thread(target=callback).start()

    else:
        mic_button.config(text="Start")
        stream_in.stop_stream()
        stream_out.stop_stream()
        stream_in.close()
        stream_out.close()
        p.terminate()

root.mainloop()
