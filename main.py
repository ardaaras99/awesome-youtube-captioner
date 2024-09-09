from pathlib import Path

from awesome_youtube_captioner import DEEPGRAM_API_KEY
from src.transcriber import DeepgramTranscriber, TranscriberConfig
from src.yt_downloader import YouTubeDownloader

YOUTUBE_URL = "https://www.youtube.com/watch?v=BQO9Xu6zgwg"
VIDEO_DIRECTORY = Path(
    "/Users/ardaaras/Documents/awesome-youtube-captioner/downloaded_videos"
)
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
