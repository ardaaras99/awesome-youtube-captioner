import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
DOWNLOADED_VIDEOS_DIRECTORY = Path.cwd().parent / "downloaded_videos"
