import json
import os
if __name__ == "__main__":
    raise NotImplementedError("This file is not meant to be run as a script.")

#This file has the configuration for the training of the model
#It also loads the API token from the secrets.json file
#This file is used by the run_finetune.py file

#Load the HF token from the secrets.json file
with open("./secrets.json", "rt") as f:
    HF_TOKEN=json.load(f)["hf_token"]

#Base model name used for fine-tuning
BASE_MODEL_NAME = os.environ.get("HF_BASE_MODEL_ID", "meta-llama/Meta-Llama-3-8B-Instruct") 
print("Will fine-tune model", BASE_MODEL_NAME)

#How LoRA works
#The original paper https://arxiv.org/pdf/2106.09685
#We have a pre-trained weight matrix W0 of size d x k
#We then update this matrix by adding a product of two low-rank matrices
#W = W0 + B*A, where B is d x r and A is r x k
#r is a hyperparameter that determines the rank of the low-rank matrices
#E.g. for the forward pass, we have the following:
#h = W0*x + B*A*x
#B*A*x is further scaled by a factor (r / alpha), where alpha is a hyperparameter, r is the rank
#The matrices B and A are updated using gradient descent
#This technique is applied to the attention weights in the transformer model
#They are smaller and be stored efficiently

#QLoRA is the same, but for quantized models, for memory efficiency

#These are the QLoRA hyperparameters
#R is Rank (r in the above explanation) - number of parameters in the adaptation layers
#More -> More parameters -> more complex tasks possible
#The original paper tested up to rank 64, so we set to 64
QLORA_R = 64
#Alpha is the weight scaling factor for LoRA matrices
#People https://datascience.stackexchange.com/a/123630
#Generally set to 16
QLORA_ALPHA = 16
#Dropout rate, set to 0.2 to avoid overfitting
QLORA_DROPOUT = 0.2

#Where to store model checkpoints
RESULT_DIR="./checkpoints"
#For how many epochs to train
NUM_EPOCHS=int(os.environ.get("FT_NUM_EPOCHS", 32))
#Batch size for training
#The default is currently set to barely fit a H100 for a 8B model
BATCH_SIZE=int(os.environ.get("FT_BATCH_SIZE", 12))
#Maximum norm for gradient clipping
#see https://neptune.ai/blog/understanding-gradient-clipping-and-how-it-can-fix-exploding-gradients-problem
#This helps to avoid exploding gradients and with numerical stability
GRAD_CLIPPING_MAX_NORM=0.5
#Learning rate
LEARNING_RATE=5e-4
#L2 regularization
#https://paperswithcode.com/method/weight-decay
WEIGHT_DECAY=0.01
#Use AdamW
OPTIMIZER="paged_adamw_32bit"
#Save a checkpoint every N batches
LOGSAVE_STEPS=int(os.environ.get("FT_LOGSAVE_STEPS", 50))
