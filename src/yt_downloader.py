import logging
import os
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from yt_dlp import YoutubeDL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class YouTubeDownloader:
    @staticmethod
    def get_video_id(url: str) -> str:
        """Extract the video ID from a YouTube URL."""
        query = urlparse(url).query
        return parse_qs(query)["v"][0]

    @staticmethod
    def download_audio(url: str, video_directory: Path) -> Path:
        """
        Download audio from YouTube video and save as MP3 in a folder named after the video ID.
        If the video has been previously downloaded, it will not download again.
        The video title is saved as a separate text file.

        Args:
            url (str): YouTube video URL
            video_directory (Path): Base directory for saving videos

        Returns:
            Path: Path to the audio file (either newly downloaded or existing)
        """
        try:
            if not video_directory.exists():
                logger.error(
                    f"The specified video directory does not exist: {video_directory}"
                )
                raise FileNotFoundError(f"Directory not found: {video_directory}")

            if not os.access(video_directory, os.W_OK):
                logger.error(
                    f"The specified video directory is not writable: {video_directory}"
                )
                raise PermissionError(
                    f"No write permission for directory: {video_directory}"
                )

            video_id = YouTubeDownloader.get_video_id(url)
            output_folder = video_directory / video_id
            audio_file = output_folder / "audio.mp3"
            title_file = output_folder / "title.txt"

            ydl_opts = {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                "no_warnings": True,
                "quiet": True,
            }

            with YoutubeDL(ydl_opts) as ydl:
                # Check if the video has already been downloaded
                if audio_file.exists() and title_file.exists():
                    logger.info(
                        f"Video {video_id} has already been downloaded. Skipping."
                    )
                    return audio_file

                # Extract video info
                info = ydl.extract_info(url, download=False)
                video_title = ydl.sanitize_info(info)["title"]

                logger.info(f"Attempting to download: {video_title} (ID: {video_id})")
                logger.info(f"Output folder: {output_folder}")

                # Create output folder
                output_folder.mkdir(parents=True, exist_ok=True)

                # Save video title
                with open(title_file, "w", encoding="utf-8") as f:
                    f.write(video_title)

                # Set the output template
                ydl.params["outtmpl"] = {
                    "default": str(output_folder / "audio.%(ext)s")
                }

                # Download the audio
                ydl.download([url])

                if not audio_file.exists():
                    logger.error(
                        f"Download seemed to complete, but file not found: {audio_file}"
                    )
                    raise FileNotFoundError(f"Downloaded file not found: {audio_file}")

                logger.info(f"Successfully downloaded: {audio_file}")
                return audio_file

        except Exception as e:
            logger.exception(f"An error occurred while downloading {url}: {str(e)}")
            raise
