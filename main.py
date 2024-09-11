import os
from pathlib import Path

from dotenv import load_dotenv

from awesome_youtube_captioner.transcriber import DeepgramTranscriber, TranscriberConfig
from awesome_youtube_captioner.yt_downloader import YouTubeDownloader

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
YOUTUBE_URL = "https://www.youtube.com/watch?v=BQO9Xu6zgwg"
VIDEO_DIRECTORY = Path("downloaded_videos")
downloader = YouTubeDownloader()

try:
    AUDIO_FILE_PATH = downloader.download_audio(YOUTUBE_URL, VIDEO_DIRECTORY)
    print(f"Audio file path: {AUDIO_FILE_PATH}")
except Exception as e:
    print(f"An error occurred: {str(e)}")


config = TranscriberConfig(
    api_key=DEEPGRAM_API_KEY,
    model="nova-2",
    language="tr",
    smart_format=True,
    paragraphs=True,
    utterances=True,
    utt_split=1.0,
    replace=None,
    search=None,
    keywords=None,
    diarize=True,
)
transcriber = DeepgramTranscriber(config)

try:
    srt_path, csv_path, df = transcriber.process_audio(AUDIO_FILE_PATH)
    print(f"SRT file: {srt_path}")
    print(f"CSV file: {csv_path}")
    print(f"Transcript DataFrame shape: {df.shape}")
    print(df.head())
except Exception as e:
    print(f"An error occurred: {str(e)}")
