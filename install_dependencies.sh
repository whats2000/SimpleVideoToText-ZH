#!/bin/bash

# 確保在正確的conda環境中
conda activate video-to-text

# 安裝必要的庫
pip install transformers torch soundfile
conda install -c conda-forge moviepy ffmpeg -y

# 安裝 HuggingFace模型相關依賴
pip install git+https://huggingface.co/BELLE-2/Belle-whisper-large-v3-turbo-zh