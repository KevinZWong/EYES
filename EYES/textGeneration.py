from transformers import AutoModelForCausalLM, AutoTokenizer
from accelerate import Accelerator
import torch
import time
import os 
import gc

class TextGenerator:
    def __init__(self, model_path="mistralai/Mistral-7B-Instruct-v0.2", max_tokens=4000, token="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"):
        torch.cuda.empty_cache()
        self.max_tokens = max_tokens
        # cognitivecomputations/dolphin-2.6-mistral-7b
        # Initialize the environment variable required by the model.
        os.environ['CURL_CA_BUNDLE'] = ''
        
        # Load the model and tokenizer.
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="auto",
            torch_dtype=torch.bfloat16
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, device_map="auto", token="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")
        # Initialize the Accelerator.
        self.accelerator = Accelerator()
        self.accelerator.wait_for_everyone()

    def generate_text(self, prompt, max_tokens):
        # Tokenize the prompt.
        prompt_tokenized = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        
        # Generate text.
        with self.accelerator.autocast():
            output_tokenized = self.model.generate(**prompt_tokenized, max_new_tokens=max_tokens, temperature=1.0)[0]
        
        # Remove the prompt from the output to return only the generated text.
        output_tokenized = output_tokenized[len(prompt_tokenized["input_ids"][0]):]
        
        return self.tokenizer.decode(output_tokenized)
    def cleanup(self):
        del self.model
        gc.collect()
        torch.cuda.empty_cache()


if __name__ == "__main__":
    text_generator = TextGenerator()
    prompt = "How do i make an omelette, be very spesific."
    generated_text = text_generator.generate_text(prompt, 400)
    print(generated_text)
