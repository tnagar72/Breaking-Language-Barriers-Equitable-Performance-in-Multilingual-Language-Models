#!/bin/bash
set -exuo pipefail

pip install accelerate \
    peft \
    bitsandbytes \
    transformers \
    trl
pip install torch torchvision torchaudio
