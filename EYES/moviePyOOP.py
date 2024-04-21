
from moviepy.editor import *
from moviepy.video.fx.all import crop, resize
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import AudioArrayClip
from moviepy.video.compositing.transitions import crossfadein
from PIL import Image
from random import uniform
import concurrent.futures
import os
import subprocess
import ffmpeg
import numpy as np
from queue import Queue
from threading import Thread
import json

class VideoGenerator:
    def __init__(self):
        self.size = (1080,1920)
        self.font= "fonts/theBoldFont.ttf"
        self.color="white"
        self.bg_color=(0, 0, 0, 0)
        self.fontsize= 30  
        self.framerate = 24

            
    def getFontsize(self):
        return self.fontsize
    def setFontsize(self, initFontsize): 
        self.fontsize = initFontsize
    def getSize(self):
        return self.size
    def setSize(self, initSize): 
        self.size = initSize
    def getFont(self):
        return self.font
    def setFont(self, initFont): 
        self.font = initFont
    def getColor(self):
        return self.color
    def setColor(self, initColor): 
        self.color = initColor
    def getBg_color(self):
        return self.bg_color
    def setBg_color(self, initBg_color): 
        self.bg_color = initBg_color

    def getLengthAudioFile(self, fname):
        audio = AudioFileClip(fname)
        duration = audio.duration
        return duration


    def combine_audio_files(self, file_list, output_file):
        # Combine the audio files into a single file
        command = ['ffmpeg', '-y']
        for file in file_list:
            command += ['-i', file]
        command += ['-filter_complex', 'concat=n={}:v=0:a=1'.format(len(file_list)), '-vn', output_file]
        subprocess.run(command)

    def make_silence(self, duration, fps):
        """Create a silent audio clip of the given duration and fps."""
        silence = AudioClip(lambda t: [0, 0], duration=duration)
        silence.fps = fps
        return silence

    def overlay_audio_video(self, video_clip, audio_file_path):
        # Load the audio file
        audio = AudioFileClip(audio_file_path)
        
        # Calculate the duration of silence needed
        silence_duration = video_clip.duration - audio.duration

        # If the audio is longer than the video, we need to cut it
        if audio.duration > video_clip.duration:
            audio = audio.subclip(0, video_clip.duration)
        # If the video is longer than the audio, we need to add silence to the audio
        elif silence_duration > 0:
            # Create a silent audio clip of the required duration
            silence = self.make_silence(silence_duration, audio.fps)
            
            # Concatenate the original audio with the silence
            audio = concatenate_audioclips([audio, silence])

        # Set the audio of the video clip
        video_clip = video_clip.set_audio(audio)

        return video_clip
    def add_text_overlay(self, video_clip, text_list):
        clips = []
        print("text_list", text_list)

        for text, start_time, end_time in text_list:
            subclip = video_clip.subclip(start_time, end_time)
            txt_clip = (TextClip(text, fontsize=self.fontsize, color=self.color, transparent=True, font = self.font)
                        .set_position(('center', 'center'))
                        .set_start(0)
                        .set_duration(subclip.duration))

            result = CompositeVideoClip([subclip, txt_clip])
            clips.append(result)

        final_clip = concatenate_videoclips(clips)


        return final_clip

    
    def compute_times(self, sync_map_file, overlap=0.05):

        with open(sync_map_file, 'r') as file:
            sync_map = json.load(file)

        start_end_times = []
        print("sync_map['fragments']", sync_map['fragments'])


        for fragment in sync_map['fragments']:
            start_time = fragment['begin']
            end_time = fragment['end']
            lines = fragment['lines']

            print(f"From {start_time} to {end_time}: {lines}")  
            
    
            start_end_times.append([lines[0], start_time, end_time])


        for i in range(0, len(start_end_times)):
            if float(start_end_times[i][1]) != 0.0:
                start_end_times[i][1] = str(float(start_end_times[i][1]) - overlap)
            if float(start_end_times[i][2]) != start_end_times[len(start_end_times)-1][2]:
                start_end_times[i][2] = str(float(start_end_times[i][2]) - overlap)

        return start_end_times



    
    def get_dimentions(self, image_path):
        
        img = Image.open(image_path)

        width, height = img.size
        return f"{width}x{height}"


