import argparse
import logging
import os
import sys

import torch
from moviepy.video.io.VideoFileClip import VideoFileClip
from transformers import pipeline

# 配置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def extract_audio(video_path):
    """從影片中提取音訊"""
    try:
        video = VideoFileClip(video_path)
        audio_path = "temp_audio.wav"
        video.audio.write_audiofile(audio_path, logger=None)
        video.close()  # 顯式關閉影片資源
        return audio_path
    except Exception as e:
        logger.error(f"音訊提取失敗: {e}")
        raise

def transcribe_audio(audio_path, model_name='openai/whisper-base'):
    """使用指定模型進行語音轉文字"""
    try:
        # 自動檢測設備
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"使用設備: {device}")
        logger.info(f"使用模型: {model_name}")

        # 配置長音頻處理
        transcriber = pipeline(
            "automatic-speech-recognition", 
            model=model_name,
            device=device,
            chunk_length_s=30,  # 分段處理，每段30秒
            return_timestamps=True  # 返回時間戳
        )
        
        # 執行語音轉文字
        transcription = transcriber(audio_path)
        
        # 如果返回多段，合併文本
        if isinstance(transcription, list):
            full_text = "\n".join([
                f"[{chunk['timestamp'][0]:.2f}s - {chunk['timestamp'][1]:.2f}s] {chunk['text']}" 
                for chunk in transcription
            ])
            return full_text
        else:
            return transcription['text']
    except Exception as e:
        logger.error(f"語音轉文字失敗: {e}")
        raise

def video_to_text(video_path, model_name='openai/whisper-base'):
    """完整的影片語音轉文字流程"""
    # 提取音訊
    audio_path = extract_audio(video_path)
    
    try:
        # 轉文字
        text = transcribe_audio(audio_path, model_name)
        return text
    finally:
        # 清理臨時音訊檔案
        if os.path.exists(audio_path):
            os.remove(audio_path)

def main():
    # 創建參數解析器
    parser = argparse.ArgumentParser(description='影片語音轉文字工具')
    parser.add_argument('video_path', type=str, help='輸入影片路徑')
    parser.add_argument('--model', type=str, default='openai/whisper-base', 
                        help='指定語音識別模型 (默認: openai/whisper-base)')
    parser.add_argument('--output', type=str, 
                        help='指定輸出文件路徑（可選）')

    # 解析參數
    args = parser.parse_args()

    try:
        # 檢查文件是否存在
        if not os.path.exists(args.video_path):
            logger.error("文件不存在，請檢查路徑")
            return
        
        logger.info("開始處理影片...")
        result = video_to_text(args.video_path, args.model)
        
        print("\n=== 轉錄結果 ===")
        print(result)
        
        # 確定輸出文件路徑
        if args.output:
            output_file = args.output
        else:
            output_file = os.path.splitext(args.video_path)[0] + "_transcript.txt"
        
        # 寫入結果
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        logger.info(f"轉錄結果已保存到 {output_file}")
    
    except Exception as e:
        logger.error(f"處理過程發生錯誤: {e}")

if __name__ == "__main__":
    main()