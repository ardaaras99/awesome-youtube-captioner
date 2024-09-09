# Awesome YouTube Captioner

## Overview

Awesome YouTube Captioner is a Python-based tool that leverages the Deepgram API to transcribe YouTube videos. It provides a streamlined pipeline for downloading YouTube audio, converting it into both SRT (SubRip Subtitle) and CSV (Comma-Separated Values) formats, making it easy to work with transcribed audio in various applications.

## Features

- Download audio from YouTube videos
- Transcribe audio files using Deepgram's advanced speech recognition technology
- Generate SRT files for use in video subtitling
- Create CSV files for easy data manipulation and analysis
- Avoid redundant processing by checking for existing transcription files
- Configurable transcription parameters including language, model, smart formatting, and speaker diarization

## Installation

To use Awesome YouTube Captioner in your project, add it as a dependency using Poetry:

1. If you haven't already, initialize your project with Poetry:

   ```
   poetry init
   ```

2. Add Awesome YouTube Captioner as a dependency:

   ```
   poetry add git+https://github.com/ardaaras99/awesome-youtube-captioner.git
   ```

   This will add the following line to your `pyproject.toml`:

   ```toml
   [tool.poetry.dependencies]
   awesome-youtube-captioner = {git = "https://github.com/ardaaras99/awesome-youtube-captioner.git"}
   ```

3. Install the dependencies:

   ```
   poetry install
   ```

## Configuration

Before using the Awesome YouTube Captioner, you need to set up your Deepgram API key:

1. Sign up for a Deepgram account at <https://deepgram.com/>
2. Obtain your API key from the Deepgram dashboard
3. Create a `.env` file in your project root and add your API key:

   ```
   DEEPGRAM_API_KEY=your_api_key_here
   ```

## Usage

1. In your Python script, import the necessary classes:

   ```python
   from pathlib import Path
   from dotenv import load_dotenv
   import os
   from awesome_youtube_captioner import TranscriberConfig, DeepgramTranscriber

   load_dotenv()  # Load environment variables from .env file
   ```

2. Create a `TranscriberConfig` object:

   ```python
   config = TranscriberConfig(
       api_key=os.getenv("DEEPGRAM_API_KEY"),
       language="en",
       model="general",
       smart_format=True,
       diarize=True,
       timeout=600
   )
   ```

3. Create a `DeepgramTranscriber` instance:

   ```python
   transcriber = DeepgramTranscriber(config)
   ```

4. Process a YouTube video:

   ```python
   youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
   srt_path, csv_path, df = transcriber.process_youtube_video(youtube_url)
   ```

5. The `process_youtube_video` method returns:
   - `srt_path`: Path to the generated SRT file
   - `csv_path`: Path to the generated CSV file
   - `df`: Pandas DataFrame containing the transcription data

## Configuration Options

The `TranscriberConfig` class accepts the following parameters:

- `api_key` (str, required): Your Deepgram API key
- `language` (str, optional): The language of the audio (default: "en")
- `model` (str, optional): The Deepgram model to use (default: "general")
- `smart_format` (bool, optional): Whether to use smart formatting (default: True)
- `diarize` (bool, optional): Whether to perform speaker diarization (default: True)
- `timeout` (int, optional): API call timeout in seconds (default: 600)

## Example

```python
from pathlib import Path
from dotenv import load_dotenv
import os
from awesome_youtube_captioner import TranscriberConfig, DeepgramTranscriber

load_dotenv()  # Load environment variables from .env file

# Set up configuration
config = TranscriberConfig(
    api_key=os.getenv("DEEPGRAM_API_KEY"),
    language="en",
    model="general",
    smart_format=True,
    diarize=True,
    timeout=600
)

# Create transcriber instance
transcriber = DeepgramTranscriber(config)

# Process YouTube video
youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
srt_path, csv_path, df = transcriber.process_youtube_video(youtube_url)

# Print results
print(f"SRT file created: {srt_path}")
print(f"CSV file created: {csv_path}")
print(f"Transcript DataFrame shape: {df.shape}")
print(df.head())
```

## Contributing

Contributions to improve Awesome YouTube Captioner are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project uses the [Deepgram API](https://deepgram.com/) for speech recognition.
- Thanks to the developers of `deepgram-captions` for providing SRT generation capabilities.
- This project uses `yt-dlp` for handling YouTube downloads.
