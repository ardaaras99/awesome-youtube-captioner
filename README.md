# awesome-youtube-captioner

## Overview

Deepgram Transcriber is a Python-based tool that leverages the Deepgram API to transcribe audio files. It provides a streamlined pipeline for converting MP3 files into both SRT (SubRip Subtitle) and CSV (Comma-Separated Values) formats, making it easy to work with transcribed audio in various applications.

## Features

- Transcribe MP3 audio files using Deepgram's advanced speech recognition technology
- Generate SRT files for use in video subtitling
- Create CSV files for easy data manipulation and analysis
- Avoid redundant processing by checking for existing transcription files
- Configurable transcription parameters including language, model, smart formatting, and speaker diarization

## Requirements

- Python 3.12+
- Poetry for dependency management

## Dependencies

- `deepgram-sdk` (v3.5.1+)
- `yt-dlp` (v2024.8.6+)
- `tqdm` (v4.66.5+)
- `requests` (v2.32.3+)
- `python-dotenv` (v1.0.1+)
- `deepgram-captions` (v1.2.0+)
- `pandas` (v2.2.2+)

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/deepgram-transcriber.git
   cd deepgram-transcriber
   ```

2. Install Poetry if you haven't already:

   ```
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Install the project dependencies using Poetry:

   ```
   poetry install
   ```

4. Set up your Deepgram API key:
   - Sign up for a Deepgram account at <https://deepgram.com/>
   - Obtain your API key from the Deepgram dashboard
   - Create a `.env` file in the project root and add your API key:

     ```
     DEEPGRAM_API_KEY=your_api_key_here
     ```

## Usage

1. Activate the Poetry environment:

   ```
   poetry shell
   ```

2. In your Python script or interactive session, import the necessary classes and create a `TranscriberConfig` object:

   ```python
   from pathlib import Path
   from dotenv import load_dotenv
   import os
   from src.transcriber import TranscriberConfig, DeepgramTranscriber

   load_dotenv()  # Load environment variables from .env file

   config = TranscriberConfig(
       api_key=os.getenv("DEEPGRAM_API_KEY"),
       language="en",
       model="general",
       smart_format=True,
       diarize=True,
       timeout=600
   )
   ```

3. Create a `DeepgramTranscriber` instance with your config:

   ```python
   transcriber = DeepgramTranscriber(config)
   ```

4. Process an audio file:

   ```python
   audio_file_path = Path("/path/to/your/audio/file.mp3")
   srt_path, csv_path, df = transcriber.process_audio(audio_file_path)
   ```

5. The `process_audio` method returns:
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

## Output Files

1. SRT File:
   - Located in the same directory as the input audio file
   - Named "transcript.srt"
   - Contains timestamped subtitles with optional speaker labels

2. CSV File:
   - Located in the same directory as the input audio file
   - Named "transcript.csv"
   - Contains columns: start_time, end_time, speaker, text

## Example

```python
from pathlib import Path
from dotenv import load_dotenv
import os
from deepgram_transcriber import TranscriberConfig, DeepgramTranscriber

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

# Process audio file
audio_file_path = Path("/path/to/your/audio/file.mp3")
srt_path, csv_path, df = transcriber.process_audio(audio_file_path)

# Print results
print(f"SRT file created: {srt_path}")
print(f"CSV file created: {csv_path}")
print(f"Transcript DataFrame shape: {df.shape}")
print(df.head())
```

## Contributing

Contributions to improve Deepgram Transcriber are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project uses the [Deepgram API](https://deepgram.com/) for speech recognition.
- Thanks to the developers of `deepgram-captions` for providing SRT generation capabilities.
- This project uses `yt-dlp` for handling YouTube downloads.
