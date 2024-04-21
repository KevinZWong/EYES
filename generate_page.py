import tkinter as tk
from tkinter import PhotoImage, filedialog
import os
import webbrowser  # Used for opening video files with the default system application
import threading
from EYES.EYES import EYES
from pydub import AudioSegment


class GeneratePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        self.update_text_img = PhotoImage(file="images/generate.png")

        self.text_widget = tk.Text(self, height=20, width=145)
        self.text_widget.pack(pady=10, padx=20)

        self.update_button = tk.Button(self, image=self.update_text_img, command=self.start_process)
        self.update_button.pack(pady=10)

        # This button will be created after updating the text
        self.open_video_button = None  # Initially, there is no button

    def start_process(self):
        # Start the long-running process in a new thread to keep the GUI responsive
        threading.Thread(target=self.update_textbox, daemon=True).start()

    def update_textbox(self):
        def convert_wav_to_mp3(wav_file_path, mp3_file_path, bitrate="192k"):
            audio = AudioSegment.from_wav(wav_file_path)
            audio.export(mp3_file_path, format="mp3", bitrate=bitrate)


        # Ensure the text widget is editable
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete('1.0', tk.END)
        
        self.text_widget.insert(tk.END, "Starting Generation\n")
        self.text_widget.update_idletasks()  # Update the GUI
        
        script_file = 'EYES/ScriptFiles/script.txt'
        audio_file = 'EYES/AudioFiles/story.mp3'
        sync_map_file = 'EYES/SyncMap/syncmap.json'
        image_folder = "EYES/imageFiles/"

        eyes = EYES()

        self.text_widget.insert(tk.END, "Starting Voice Recognition\n")
        self.text_widget.update_idletasks()
        file_path = self.controller.get_audio_file()
        convert_wav_to_mp3(file_path, audio_file)
        print("reviieved", file_path)
 
        script = eyes.audio_recognition(audio_file)
        print("script:", script)


        self.text_widget.insert(tk.END, "Finished Voice Recognition\n")
        self.text_widget.update_idletasks()

        #script = "Once upon a time a little girl named Goldilocks was playing in the woods near her home. A yummy smell drifted down the pebbly path. Goldilocks followed the smell to a little house. She knocked on the front door. But there was no one home. Goldilocks was so hungry she followed the smell inside. In the kitchen she saw a big bowl, a medium sized bowl and a teeny tiny bowl of porridge. First Goldilocks tried the porridge in the biggest bowl but it was too cold. Next she tried the porridge in the medium sized bowl, but it was too hot. Finally she tried the porridge in the smallest bowl. It was just right and she ate it all up. Then Goldilocks went into the living room for a rest. Goldilocks sat in the big chair, but it was too high up. She sat in the medium sized chair, but it was too squishy. Then Goldilocks sat in the tiny chair and it was just right. But then, crack! The chair broke into teeny tiny pieces. Oh! Goldilocks gasped in surprise. Perhaps I should lie down instead. Upstairs Goldilocks lay down on the big bed. But it was too hard. Then she lay down on the medium sized bed. But it was too soft. Finally she lay down on the teeny tiny bed. It was just right and she fell fast asleep. Meanwhile a big daddy bear, a medium sized mommy bear and a teeny tiny baby bear returned home. They had been for a walk while their hot porridge cooled down. Someone's been eating my porridge! Roared daddy bear. Someone's been eating my porridge too! growled mommy bear look! squeaked baby bear my porridge is all gone hmmm the three bears went into the living room someone's been sitting in my chair roared daddy bear someone's been sitting in my chair too growled mommy bear someone's been sitting in my chair squeaked baby bear and they've broken it hmmm The three bears went upstairs. Someone's been sleeping in my bed! roared Daddy Bear. Someone's been sleeping in my bed too! growled Mommy Bear. Someone's been sleeping in my bed! squeaked Baby Bear. And she is still there! Roar! At that moment Goldilocks woke up. When she saw the three bears, she ran out of their house and all the way home. She never visited the house of the three bears ever again."

        
        self.text_widget.insert(tk.END, "Starting Formatting Caption Script\n")
        eyes.caption_script(script, script_file)
        self.text_widget.insert(tk.END, "Finished Formatting Caption Script\n")
        self.text_widget.update_idletasks()

        self.text_widget.insert(tk.END, "Starting Forced Audio Alignment\n")
        eyes.forced_audio_alignment(audio_file, script_file, sync_map_file)
        self.text_widget.insert(tk.END, "Finished Forced Audio Alignment\n")
        self.text_widget.update_idletasks()

        self.text_widget.insert(tk.END, "Starting Image Describing\n")
        descriptions = eyes.image_script(script)
        self.text_widget.insert(tk.END, "Finished Image Describing\n")
        self.text_widget.update_idletasks()

        self.text_widget.insert(tk.END, "Starting Image Generation\n")
        print("descriptions", descriptions)
        print("image_folder", image_folder)
        image_files = eyes.generate_images(descriptions, image_folder)
        
        self.text_widget.insert(tk.END, "Finished Image Generation\n")
        self.text_widget.update_idletasks()
        #image_files = [[0, 'imageFiles/image0.jpg'], [1, 'imageFiles/image1.jpg'], [2, 'imageFiles/image2.jpg'], [3, 'imageFiles/image3.jpg'], [4, 'imageFiles/image4.jpg'], [5, 'imageFiles/image5.jpg'], [6, 'imageFiles/image6.jpg'], [7, 'imageFiles/image7.jpg'], [8, 'imageFiles/image8.jpg'], [9, 'imageFiles/image9.jpg'], [10, 'imageFiles/image10.jpg'], [11, 'imageFiles/image11.jpg'], [12, 'imageFiles/image12.jpg'], [13, 'imageFiles/image13.jpg'], [14, 'imageFiles/image14.jpg']]


        # Assuming mapling_animation is synchronous
        self.text_widget.insert(tk.END, "Starting Video Animations\n")
        mapling_clips = eyes.mapling_animation(image_files, audio_file)
        self.text_widget.insert(tk.END, "Finishing Video Animations\n")
        self.text_widget.update_idletasks()

        self.text_widget.insert(tk.END, "Video Compiling...\n")
        print("audio_file", audio_file)
        print("sync_map_file", sync_map_file)
        eyes.edit_video(audio_file, mapling_clips, sync_map_file, "FinishedVideo")
        self.text_widget.insert(tk.END, "Done Compiling. Enjoy!\n")
        self.text_widget.update_idletasks()

        self.text_widget.config(state=tk.DISABLED)

        # Create video opening button
        self.create_video_button()

    def create_video_button(self):
        # Create the button if it doesn't exist
        if not self.open_video_button:
            self.open_video_button = tk.Button(self, text="Open Video File", command=self.open_file)
            self.open_video_button.pack(pady=10)

    def open_file(self):
        # Let the user select a video file
        video_path = filedialog.askopenfilename(title="Select a video file", filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
        if video_path:
            # Open the video file with the default application
            webbrowser.open(video_path)
