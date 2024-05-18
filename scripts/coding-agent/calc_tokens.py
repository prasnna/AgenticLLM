from transformers import AutoTokenizer

import os

from dotenv import load_dotenv

load_dotenv()

model_ckpt_path = os.environ['model_ckpt_path']

tokenizer = AutoTokenizer.from_pretrained(model_ckpt_path)

with open("scripts\code-analysis\code_files.txt", "r") as file:
    text = file.read()

input_ids = tokenizer.encode(text, return_tensors="pt")
num_tokens = len(input_ids[0])
print(f"Number of tokens: {num_tokens}")