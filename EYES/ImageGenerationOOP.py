import argparse
import os
from diffusers import DiffusionPipeline
import torch
class ImageCreator:
    def __init__(self, gpu_index):
        # Set CUDA_VISIBLE_DEVICES to specify GPU index
        print("gpu_index", gpu_index)
        os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_index)
        # Load both base & refiner
        self.base = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
        )
        self.base.enable_model_cpu_offload()
        self.refiner = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-refiner-1.0",
            text_encoder_2=self.base.text_encoder_2,
            vae=self.base.vae,
            torch_dtype=torch.float16,
            use_safetensors=True,
            variant="fp16",
        )

        self.refiner.enable_model_cpu_offload()

        
    def generate_image(self, prompt, n_steps=40, high_noise_frac=0.8):
        # Run both experts
        image = self.base(
            prompt=prompt,
            num_inference_steps=n_steps,
            denoising_end=high_noise_frac,
            output_type="latent",
        ).images
        image = self.refiner(
            prompt=prompt,
            num_inference_steps=n_steps,
            denoising_start=high_noise_frac,
            image=image,
        ).images[0]
        
        return image

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate an image using Diffusion model on multiple gpus")
    parser.add_argument("--gpu_number", type=str, default="0", help="GPU index to use")
    parser.add_argument("--prompt", type=str, default="Default prompt", help="Prompt for image generation")
    parser.add_argument("--output_file", type=str, default="output.jpg", help="Output file name for the generated image")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    # Initialize ImageCreator with specified GPU index

    generator = ImageCreator(args.gpu_number)

    # Generate image with the provided prompt
    generated_image = generator.generate_image(args.prompt)

    # Save the generated image to the specified output file
    generated_image.save(args.output_file)
