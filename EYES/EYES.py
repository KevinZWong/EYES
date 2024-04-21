from transformers import pipeline
from EYES.alignmentOOP import AudioTextAligner
from EYES.ScriptProcessingOOP import ScriptProcessing
from EYES.textGeneration import TextGenerator
from EYES.ConcurrentImagesOOP import ConcurrentImageProcessing
from EYES.MaplingOOP import VideoCreator
from EYES.moviePyOOP import VideoGenerator
from moviepy.editor import *
from PIL import Image
class EYES:
    def __init__(self):
        pass

    def audio_recognition(self, audio_file):
        whisper = pipeline('automatic-speech-recognition', model = 'openai/whisper-medium', device = "cuda")
        return whisper(audio_file)["text"]
    
    def caption_script(self, script, script_file):
        script_processing = ScriptProcessing()
        caption_script = script_processing.format_script(script, 5)
        for i in range(0, len(caption_script)):
            caption_script[i] = caption_script[i] + "\n"
        with open(script_file, 'w') as file:
            file.writelines(caption_script)
        

    def forced_audio_alignment(self, audio_file, script_file, sync_map_file):
        aligner = AudioTextAligner(
            audio_file_path=audio_file,
            text_file_path=script_file,
            sync_map_path=sync_map_file
        )
        aligner.process_task()
        aligner.output_sync_map()
    
    def image_script(self, script, max_tokens=77):
        script_processing = ScriptProcessing()
        
        image_script = script_processing.format_script(script, 20)
        descriptions = []
        text_generator = TextGenerator()
        for segment in image_script:
            prompt = """

            Turn the following sentence into a ultra realistic image or artwork
            Only include the description
            """
            prompt += segment
            generated_text = text_generator.generate_text(prompt, max_tokens)
            descriptions.append(generated_text)

            
        print("Image Describing Done")
        text_generator.cleanup()
        return descriptions


    def generate_images(self, image_descriptions, imageFilePath):
        print("Images Scripts Parsed")
        print("Images to Generate: ", len(image_descriptions))
        concurrent_images = ConcurrentImageProcessing()
        # [[index of prompt, file where image based on prompt is saved]]
        return concurrent_images.generate_images(image_descriptions, imageFilePath)
    
    def mapling_animation(self, imageFiles, audio_file):
        def get_dimentions(image_path):
            
            img = Image.open(image_path)

            width, height = img.size
            return f"{width}x{height}"

        def getLengthAudioFile(fname):
            audio = AudioFileClip(fname)
            duration = audio.duration
            return duration
        

        audioFileLength = getLengthAudioFile(audio_file) 
        models_directory = "EYES/Mapling_EYES/mapling_models"
        movement_files = [file for file in os.listdir(models_directory) if os.path.isfile(os.path.join(models_directory, file))]
        image_duration = audioFileLength / len(imageFiles)
        print("checkpoint1")
        print("imageFiles", imageFiles)
        image_resolution  = get_dimentions(imageFiles[0][1])
        print("image_resolution", image_resolution)

        video_creator = VideoCreator(resolution="1920x1080", frame_rate=60, clip_duration=image_duration, upscale=1.5, movement_files = movement_files)
        mapling_clips = []
        for image in imageFiles:
            video_creator.shuffle_movement_files()
            mapling_clips.append(video_creator.create_video(image_path=image[1]))
        return mapling_clips
    
    def edit_video(self, audio_file, mapling_clips, sync_map_file, title):
        video_gen = VideoGenerator()
        
        totalVideolength = video_gen.getLengthAudioFile(audio_file) 
        print("Video length:", totalVideolength)
        VideoClips = concatenate_videoclips(mapling_clips)
        print("Video Generated from Images")
        VideoClips = video_gen.overlay_audio_video(VideoClips,  audio_file)
        print("Audio Added to Video")
        start_end_times = video_gen.compute_times(sync_map_file)
        print("start_end_times", start_end_times)

        VideoClips = video_gen.add_text_overlay(VideoClips, start_end_times)
        print("Text Overlay Added")
        audio = AudioFileClip(audio_file)

        title = title.replace(" ", "")
        if VideoClips.duration > audio.duration:
            VideoClips = VideoClips.subclip(0, audio.duration)
        VideoClips = VideoClips.fx(vfx.speedx, factor=1.05)

        print("checkpoint4")
        VideoClips.write_videofile(f"{title}.mp4", fps=24)
        VideoClips.close()
        print(title, "sucessfully generated")


