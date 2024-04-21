import tkinter as tk
from recorder_app import RecorderApp
from generate_page import GeneratePage

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Page Application")
        self.geometry('1200x700')

        self.selected_audio_file = None  # Place to store the audio file path

        self.nav_frame = tk.Frame(self)
        self.nav_frame.pack(side="top", fill="x")

        self.recorder_button = tk.Button(self.nav_frame, text="Recorder",
                                         command=lambda: self.show_frame("RecorderApp"))
        self.recorder_button.pack(side="left")

        self.generate_button = tk.Button(self.nav_frame, text="Generate",
                                         command=lambda: self.show_frame("GeneratePage"))
        self.generate_button.pack(side="left")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (RecorderApp, GeneratePage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("RecorderApp")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def set_audio_file(self, path):
        self.selected_audio_file = path

    def get_audio_file(self):
        return self.selected_audio_file

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()




