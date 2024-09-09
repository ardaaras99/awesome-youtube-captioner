from pathlib import Path
from awesome_youtube_captioner.transcriber import DeepgramTranscriber, TranscriberConfig
from awesome_youtube_captioner.yt_downloader import YouTubeDownloader
from dotenv import load_dotenv
import os

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
    language="tr",
    model="nova-2",
    smart_format=True,
    diarize=True,
    timeout=200,
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
