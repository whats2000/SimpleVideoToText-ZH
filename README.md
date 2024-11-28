# 影片語音轉文字 (Belle Whisper Model)

## 環境準備 (Conda)

### 1. 安裝 Conda
- 建議使用 Miniconda 或 Anaconda
- 從官網下載並安裝：https://docs.conda.io/en/latest/miniconda.html

### 2. 創建並激活虛擬環境
```bash
# 創建環境
conda env create -f environment.yml

# 激活環境
conda activate video-to-text
```

### 3. 使用方法
```bash
# 直接運行腳本
python video_to_text.py
```

## 功能特點
- 中文語音識別
- 使用 Belle-whisper-large-v3-turbo 模型
- 支持 GPU 加速
- Conda 環境管理

## 環境要求
- Conda (Miniconda/Anaconda)
- Python 3.9+
- CUDA (可選，用於 GPU 加速)

## 疑難排除
1. 如遇模型下載問題，請檢查網絡
2. GPU 支持需要正確配置 CUDA
3. 音訊質量會影響轉錄準確性

## 模型信息
- 模型：BELLE-2/Belle-whisper-large-v3-turbo-zh
- 支持語言：中文
- 識別精度：高