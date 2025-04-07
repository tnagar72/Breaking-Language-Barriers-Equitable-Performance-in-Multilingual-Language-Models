#Reimplementation of https://towardsdatascience.com/fine-tune-your-own-llama-2-model-in-a-colab-notebook-df9823a04a32
#For LLAMA 3
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig
from trl import SFTTrainer

from dataset import DATASET
import config

#Load the quantization configuration
#We will be working in 4-bit mode
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=False, #We have enough memory not to double quantize
)

#Load the base model
#We only use 1 GPU
#"Caulas LM" is the model type, basically means Next-Token Prediction
model = AutoModelForCausalLM.from_pretrained(
    config.BASE_MODEL_NAME,
    quantization_config=bnb_config,
    device_map={"": 0},
    token=config.HF_TOKEN,
)
model.config.use_cache = False
model.config.pretraining_tp = 1

#Load the base model tokenizer
#We will not modify it
tokenizer = AutoTokenizer.from_pretrained(
    config.BASE_MODEL_NAME, 
    trust_remote_code=True,
    token=config.HF_TOKEN,
)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

#Load the QLoRA configuration
#See the config.py file for more information about the parameters
peft_config = LoraConfig(
    lora_alpha=config.QLORA_ALPHA,
    lora_dropout=config.QLORA_DROPOUT,
    r=config.QLORA_R,
    bias="none",
    task_type="CAUSAL_LM",
)

#Create training arguments
#See the config.py file for more information about the parameters
training_arguments = TrainingArguments(
    output_dir=config.RESULT_DIR,
    num_train_epochs=config.NUM_EPOCHS,
    per_device_train_batch_size=config.BATCH_SIZE,
    gradient_accumulation_steps=1,
    optim=config.OPTIMIZER,
    save_steps=config.LOGSAVE_STEPS,
    logging_steps=config.LOGSAVE_STEPS,
    learning_rate=config.LEARNING_RATE,
    weight_decay=config.WEIGHT_DECAY,
    fp16=False,
    bf16=True, #This is supported on H100 and helps with efficiency
    max_grad_norm=config.GRAD_CLIPPING_MAX_NORM,
    max_steps=-1,
    warmup_ratio=0, #We do not use warmup, just start with normal LR
    group_by_length=True, #This helps with efficiency
    lr_scheduler_type="constant", #We don't use a scheduler
    report_to="none", #We don't use Tensorboard here (yet)
)

#Set up the trainer
#SFTTrainer -> Supervised Fine Tuning Trainer
trainer = SFTTrainer(
    model=model, #Base model
    train_dataset=DATASET, #Use our dataset from dataset.py
    peft_config=peft_config, #Apply LoRA to it
    dataset_text_field="text", #We use the "text" field for training
    max_seq_length=None,
    tokenizer=tokenizer, #Using the original tokenizer
    args=training_arguments, #And the training arguments
    packing=False,
)

#Run the train loop
trainer.train()

#Save the model
trainer.model.save_pretrained("LLAMA3-Finetuned-DONE")