import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline,
)
from transformers.pipelines.pt_utils import KeyDataset
from peft import PeftModel
from tqdm import tqdm
from datasets import Dataset

import json
import config

#Load base model from config
#We don't really need to quantize, as we are only doing inference here
base_model = AutoModelForCausalLM.from_pretrained(
    config.BASE_MODEL_NAME,
    torch_dtype=torch.float16,
    device_map={"": 0},
    token=config.HF_TOKEN,
)
base_model.config.use_cache = False

#Load the base model tokenizer
#We did not modify it on fine tune
tokenizer = AutoTokenizer.from_pretrained(
    config.BASE_MODEL_NAME, 
    trust_remote_code=True,
    token=config.HF_TOKEN,
)
tokenizer.pad_token = tokenizer.eos_token
#Left padding for correct generation
tokenizer.padding_side = "left"

#Extract end-of-tesxt tokens from the tokenizer
#LLAMA3 uses two terminators, the standard EOS token and a custom one
#We need to stop on both
terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

#Load the adaptation layers from the fine-tuned model directory
#Set the EOS tokens to the ones we extracted from the tokenizer
model = PeftModel.from_pretrained(model_id="./LLAMA3-Finetuned-DONE", model=base_model)
model.config.use_cache = False
model.generation_config.eos_token_id = terminators

#Initialize the text generation pipeline
pipe = pipeline(task="text-generation", 
                model=model, tokenizer=tokenizer, 
                max_length=2048, batch_size=config.BATCH_SIZE)

#Load the test data from JSON
with open("./llama3_test_qaps.json", "rt", encoding="utf-8") as f:
    test_data_raw = json.load(f)

#Convert the test data to a HF dataset object
#This will allow us to infer in parallel
test_data = Dataset.from_list([{"text": prompt} for prompt in test_data_raw])

model_responses = []
#Iterate over the test data and generate responses
for result in tqdm(pipe(KeyDataset(test_data, "text"), return_full_text=False), total=len(test_data_raw)):
    result_text = result[0]["generated_text"]
    model_responses.append(result_text)

#Save the responses to a JSON file
with open("./llama3_test_qaps_respones.json", "wt", encoding="utf-8") as f:
    json.dump(model_responses, f, indent=4)