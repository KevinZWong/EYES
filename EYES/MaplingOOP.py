
import sys
import os
current_directory = os.getcwd()
sys.path.append(current_directory)
from EYES.Mapling_EYES import *
from moviepy.editor import ImageClip
from EYES.Mapling_EYES.DynamicEffects import DynamicPositionClip
from EYES.Mapling_EYES.Spline3D import Spline3D
import cv2
import random

class VideoCreator:
    def __init__(self, resolution="1920x1080", frame_rate=60, clip_duration=7, upscale=1.5, movement_files= ["EYES/Mapling_EYES/mapling_models/spline_data_loop.json"]):
        self.resolution = resolution
        self.frame_rate = frame_rate
        self.clip_duration = clip_duration
        self.upscale = upscale
        self.movement_files = movement_files


    def resize_image(self, image_path, new_width, new_height):
        img = cv2.imread(image_path)
        img_resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
        return img_resized
    def shuffle_movement_files(self):
        last = self.movement_files[0]
        self.movement_files.pop(0)
        random.shuffle(self.movement_files)
        self.movement_files.append(last)
        

    def create_video(self, image_path):
        bg_width, bg_height = map(int, self.resolution.split("x"))    
        clip = ImageClip(image_path)
        width, height = clip.size

        max_final_res = max(bg_height, bg_width) * self.upscale
        if width < height:
            new_height = int(max_final_res)
            new_width = int(width / height * max_final_res)
        else:
            new_height = int(height / width * max_final_res)
            new_width = int(max_final_res)

        img_resized = self.resize_image(image_path, new_width, new_height)
        image_temp = "temp.jpg"
        cv2.imwrite(image_temp, img_resized)

        dynamic_clip = DynamicPositionClip(self.frame_rate, bg_width, bg_height)
        movement_model = Spline3D()
        movement_model.load_data("EYES/Mapling_EYES/mapling_models/"+ self.movement_files[0])
        composite = dynamic_clip.generate_video(image_temp, self.clip_duration, movement_model)
        os.remove(image_temp)
        return composite

if __name__ == "__main__":
    directory = "Mapling_EYES/mapling_models"
    movement_files = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    video_creator = VideoCreator(resolution="1920x1080", frame_rate=60, clip_duration=7, upscale=1.5, movement_files = movement_files)
    video_creator.shuffle_movement_files()
    video_creator.create_video(
        image_path="Mapling_EYES/images/corgi.jpg",
    )