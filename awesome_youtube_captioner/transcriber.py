import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
from deepgram import DeepgramClient, FileSource, PrerecordedOptions
from deepgram_captions import DeepgramConverter, srt


@dataclass
class TranscriberConfig:
    api_key: str
    model: str = None
    language: str = None
    punctuate: bool = False
    smart_format: bool = False
    paragraphs: bool = False
    utterances: bool = False
    utt_split: float = None
    replace: list = None
    search: bool = False
    keywords: list = None
    diarize: bool = False


class DeepgramTranscriber:
    def __init__(self, config: TranscriberConfig):
        self.config = config
        self.deepgram = DeepgramClient(config.api_key)

    def process_audio(self, audio_file_path: Path) -> Tuple[Path, Path, pd.DataFrame]:
        """
        Process an audio file to create SRT and CSV transcripts if they don't exist.

        Args:
            audio_file_path (Path): Path to the MP3 audio file

        Returns:
            Tuple[Path, Path, pd.DataFrame]: Paths to the SRT and CSV files, and the DataFrame of the transcript
        """
        srt_path = audio_file_path.with_name("transcript.srt")
        csv_path = audio_file_path.with_name("transcript.csv")

        # Check if both SRT and CSV files already exist
        if srt_path.exists() and csv_path.exists():
            print("SRT and CSV files already exist. Loading existing files.")
            df = pd.read_csv(csv_path)
            return srt_path, csv_path, df

        # If SRT doesn't exist, transcribe the audio
        if not srt_path.exists():
            srt_path = self.transcribe(audio_file_path)

        # If CSV doesn't exist, create it from the SRT
        if not csv_path.exists():
            df = self.srt_to_dataframe(srt_path)
            df.to_csv(csv_path, index=False)
            print(f"Transcript CSV saved to: {csv_path}")
        else:
            df = pd.read_csv(csv_path)

        return srt_path, csv_path, df

    def transcribe(self, audio_file_path: Path) -> Path:
        print(f"Transcribing audio from {audio_file_path}")
        with audio_file_path.open("rb") as file:
            buffer_data = file.read()

        payload: FileSource = {"buffer": buffer_data}

        options = PrerecordedOptions(
            model=self.config.model,
            language=self.config.language,
            punctuate=self.config.punctuate,
            smart_format=self.config.smart_format,
            paragraphs=self.config.paragraphs,
            utterances=self.config.utterances,
            utt_split=self.config.utt_split,
            replace=self.config.replace,
            search=self.config.search,
            keywords=self.config.keywords,
            diarize=self.config.diarize,
        )

        response = self.deepgram.listen.prerecorded.v("1").transcribe_file(
            payload,
            options,
            timeout=self.config.timeout,
        )
        json_response = response.to_json()
        return self.generate_srt(
            json_response, audio_file_path.with_name("transcript.srt")
        )

    def generate_srt(self, transcription_json: str, transcript_path: Path) -> Path:
        my_json = json.loads(transcription_json)
        captioner = DeepgramConverter(my_json)
        captions = srt(captioner, 10)

        transcript_path.write_text(captions, encoding="utf-8")
        print(f"Transcript generated and saved to: {transcript_path}")
        return transcript_path

    def parse_srt_file(self, file_path: Path) -> List[Dict]:
        with open(file_path, encoding="utf-8") as file:
            content = file.read()

        subtitle_entries = re.split(r"\n\n+", content.strip())
        parsed_subtitles = []
        current_speaker = None

        for entry in subtitle_entries:
            lines = entry.split("\n")
            if len(lines) < 3:
                continue

            timestamp = lines[1]
            start, end = timestamp.split(" --> ")

            text = " ".join(lines[2:])

            # Check if there's a speaker label
            speaker_match = re.match(r"\[speaker (\d+)\](.*)", text)
            if speaker_match:
                current_speaker = speaker_match.group(1)
                text = speaker_match.group(2).strip()

            parsed_subtitles.append(
                {
                    "start_time": start,
                    "end_time": end,
                    "speaker": current_speaker,
                    "text": text,
                }
            )

        return parsed_subtitles

    def srt_to_dataframe(self, srt_file_path: Path) -> pd.DataFrame:
        parsed_subtitles = self.parse_srt_file(srt_file_path)
        df = pd.DataFrame(parsed_subtitles)
        return df


# Usage example
if __name__ == "__main__":
    API_KEY = "YOUR_DEEPGRAM_API_KEY"
    AUDIO_FILE_PATH = Path("/path/to/audio/file.mp3")

    config = TranscriberConfig(
        api_key=API_KEY,
        language="en",
        model="general",
        smart_format=True,
        diarize=True,
        timeout=600,
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
