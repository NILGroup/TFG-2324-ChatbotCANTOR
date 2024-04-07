# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 12:55:02 2024

@author: Marta
"""

import os
os.environ["HF_TOKEN"] = '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'
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("google/gemma-7b")
model = AutoModelForCausalLM.from_pretrained("google/gemma-7b")

input_text = "Write me a poem about Machine Learning."
input_ids = tokenizer(input_text, return_tensors="pt")

outputs = model.generate(**input_ids)
print(tokenizer.decode(outputs[0]))