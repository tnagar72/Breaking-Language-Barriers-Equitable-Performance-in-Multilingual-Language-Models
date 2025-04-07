if __name__ == "__main__":
    raise NotImplementedError("This file is not meant to be run as a script.")

#This loads the prompts from JSON and builds an HF dataset object out of it

import json
with open("./llama3_train_qaps.json") as f:
    _RAW_PROMPTS = json.load(f)
print("Loaded", len(_RAW_PROMPTS), "prompts.")


from datasets import Dataset
_dataset_list = [{"text": p} for p in _RAW_PROMPTS]
DATASET = Dataset.from_list(_dataset_list)