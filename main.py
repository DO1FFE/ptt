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
