
from EYES import EYES


# Get text from audio file



script_file = 'ScriptFiles/script.txt'
audio_file = 'AudioFiles/story.mp3'
sync_map_file = 'SyncMap/syncmap.json'
image_folder = "imageFiles/"

eyes = EYES()

#eyes.audio_recognition(audio_file)
script = "Once upon a time, there was a young girl named Goldilocks who wandered into the forest and stumbled upon a cottage. The cottage belonged to three bears, a Papa Bear, a Mama Bear, and a Baby Bear. Finding the bears away, Goldilocks entered the cottage and explored. She tried their porridge. Papa Bear was too hot. Mama Bear was too cold. But Baby Bear was just right. So she ate it all. Then she tried their chairs. Papa Bear was too hard. Mama Bear was too soft. But Baby Bear was just right, though it broke under her weight. Finally, feeling tired, Goldilocks tried their beds. Papa Bear's was too firm, Mama Bear's was too soft, but Baby Bear's was just right, and she fell asleep. When the bears returned and found her, Goldilocks woke up, got scared, and ran away back to her home, never to return to the forest again."



eyes.caption_script(script, script_file)

eyes.forced_audio_alignment(audio_file, script_file, sync_map_file)

descriptions = eyes.image_script(script)

print("descriptions", descriptions)


# [[index of prompt, file where image based on prompt is saved]]
image_files = eyes.generate_images(descriptions, image_folder)
print("image_files", image_files)


image_files = [[0, 'imageFiles/image0.jpg'], [1, 'imageFiles/image1.jpg'], [2, 'imageFiles/image2.jpg'], [3, 'imageFiles/image3.jpg'], [4, 'imageFiles/image4.jpg'], [5, 'imageFiles/image5.jpg'], [6, 'imageFiles/image6.jpg'], [7, 'imageFiles/image7.jpg'], [8, 'imageFiles/image8.jpg'], [9, 'imageFiles/image9.jpg'], [10, 'imageFiles/image10.jpg'], [11, 'imageFiles/image11.jpg'], [12, 'imageFiles/image12.jpg'], [13, 'imageFiles/image13.jpg'], [14, 'imageFiles/image14.jpg']]







mapling_clips = eyes.mapling_animation(image_files, "AudioFiles/story.mp3")
eyes.edit_video("AudioFiles/story.mp3", mapling_clips, "SyncMap/syncmap.json", "Goldilocks")

print("aint no way this worked")

