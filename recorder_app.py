import tkinter as tk
from tkinter import PhotoImage, messagebox, filedialog
import threading
import pyaudio
import wave
import os

class RecorderApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 2
        self.rate = 44100
        self.recording = False
        self.p = pyaudio.PyAudio()
        self.setup_ui()

    def setup_ui(self):
        self.record_img = PhotoImage(file="images/record.png")
        self.stop_img = PhotoImage(file="images/stop.png")

        left_frame = tk.Frame(self)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        right_frame = tk.Frame(self)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.record_button = tk.Button(left_frame, image=self.record_img, command=self.toggle_recording)
        self.record_button.pack(pady=10)
        self.status_label = tk.Label(left_frame, text="Press 'Record' to start recording.", font=('Helvetica', 12))
        self.status_label.pack(pady=10)

        self.select_file_img = PhotoImage(file="images/select_file.png")
        self.select_file_button = tk.Button(right_frame, image=self.select_file_img, command=self.select_file)
        self.select_file_button.pack(pady=10)
        self.file_label = tk.Label(right_frame, text="No file selected", font=('Helvetica', 12))
        self.file_label.pack(pady=10)

    def toggle_recording(self):
        if self.recording:
            self.recording = False
            self.record_button.config(image=self.record_img)
            self.status_label.config(text="Recording stopped. Press 'Record' to start recording.")
            self.finish_recording()
        else:
            self.recording = True
            self.record_button.config(image=self.stop_img)
            self.status_label.config(text="Recording... press 'Stop' to finish.")
            self.start_recording()
    def start_recording(self):
        threading.Thread(target=self.record).start()

    def record(self):
        self.stream = self.p.open(format=self.format, channels=self.channels, rate=self.rate, input=True, frames_per_buffer=self.chunk)
        frames = []
        while self.recording:
            data = self.stream.read(self.chunk)
            frames.append(data)
        self.stream.stop_stream()
        self.stream.close()
        output_file = "output.wav"
        wf = wave.open(output_file, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        messagebox.showinfo("Recorder", f"Recording saved as {output_file}")

    def finish_recording(self):
        pass

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
        if file_path:
            self.file_label.config(text=os.path.basename(file_path))
            self.controller.set_audio_file(file_path) 
