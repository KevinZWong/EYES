
import torch
from EYES.ImageGenerationOOP import ImageCreator
#from ImageGenerationOOP import ImageCreator
import subprocess
import threading
import multiprocessing
import concurrent.futures
import gc

class ConcurrentImageProcessing:
    def __init__(self):
        pass

        
    def result_processing(self, orginal_data, result_data):
        #[prompt, prompt, prompt]
        #[[gpu_num, prompt, output_file], [gpu_num, prompt, output_file], [gpu_num, prompt, output_file]]

        reformat_original = []
        for i in range(0, len(orginal_data)):
            reformat_original.append([orginal_data[i], len(orginal_data)])
        # reformate new to [[prompt_num, gpu_num, prompt, output_file], [prompt_num, gpu_num, prompt, output_file], [prompt_num, gpu_num, prompt, output_file]]
        
        for i in range(0, len(orginal_data)):
            for j in range(0, len(orginal_data)):
                if result_data[j][1] == orginal_data[i]:
                    result_data[j] = [i] + result_data[j]
        
        #[[1, 0, 'prompt2', 'file1.jpg'], [2, 1, 'prompt3', 'file2.jpg'], [0, 0, 'prompt1', 'file3.jpg']]
        #print(result_data)

        return_list = []
        # [[index of prompt, file where image based on prompt is saved]]
        for i in range(0, len(orginal_data)):
            return_list.append([result_data[i][0], result_data[i][3]])
        #print(return_list)
        return return_list




        
        
    def run_generation_command(self, gpu_num, prompt, output):
        print(f"Generating image {output}, gpu_num = {gpu_num}")

        command = ["python3", "EYES/ImageGenerationOOP.py", "--gpu_number", str(gpu_num), "--prompt", prompt, "--output_file", output]
        return_code = subprocess.call(command)  

        if return_code == 0:
            print(f"Image Generation Successful {output}, gpu_num = {gpu_num}")
        else:
            print(f"Error executing Image Generation:{output}, gpu_num = {gpu_num}")
        print(f"GPU{gpu_num}, Done")
        return gpu_num, prompt, output

    def generate_images(self, image_descriptions, imageFilePath):
        images_to_generated = len(image_descriptions)
        gpu_count = torch.cuda.device_count()
        gpu_status = [True for i in range(gpu_count)]

        pooled_results = []
        futures = []
        current_image_index = 0
        executor = concurrent.futures.ThreadPoolExecutor()
        while len(pooled_results) != len(image_descriptions):
                if any(gpu_status) and images_to_generated != 0:
                    print(gpu_status)
                    gpu_avaible = gpu_status.index(True)
                    current_image_index = len(image_descriptions) - images_to_generated
                    image_name = f"{imageFilePath}image{current_image_index}.jpg"
                    futures.append(executor.submit(self.run_generation_command, gpu_avaible, image_descriptions[current_image_index], image_name))
                    gpu_status[gpu_avaible] = False
                    images_to_generated -= 1
                else:
                    future_status = [future.done() for future in futures]
                    if any(future_status):
                        current_future_index = future_status.index(True)
                        gpu_num, prompt, output_file = futures[current_future_index].result()
                        pooled_results.append([gpu_num, prompt, output_file])
                        futures.pop(current_future_index)
                        gpu_status[gpu_num] = True


        print("image_descriptions: ", image_descriptions)
        print("pooled_results: ", pooled_results)

        # pooled_results outputs only teh first 2 thread results
        return self.result_processing(image_descriptions, pooled_results)
        # [[index of prompt, file where image based on prompt is saved]]

        



if __name__ == "__main__":

    image_descriptions = []
    input1 = "1"
    while(input1 != "0"):
        input1 = input("Please enter a image description or 0 to stop")
        image_descriptions.append(input1)


    concurrent_images = ConcurrentImageProcessing()

    print(concurrent_images.generate_images(image_descriptions))


