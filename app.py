import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, after_this_request, render_template, request, send_file

from awesome_youtube_captioner.transcriber import DeepgramTranscriber, TranscriberConfig
from awesome_youtube_captioner.yt_downloader import YouTubeDownloader

load_dotenv()

app = Flask(__name__)

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
VIDEO_DIRECTORY = Path("downloaded_videos")

downloader = YouTubeDownloader()


def process_video(youtube_url, output_format):
    try:
        audio_file_path = downloader.download_audio(youtube_url, VIDEO_DIRECTORY)

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
            timeout=600,
        )
        transcriber = DeepgramTranscriber(config)

        srt_path, csv_path, df = transcriber.process_audio(audio_file_path)

        if output_format == "srt":
            return srt_path
        elif output_format == "csv":
            return csv_path
        elif output_format == "json":
            json_path = csv_path.with_suffix(".json")
            df.to_json(json_path, orient="records", lines=True)
            return json_path
        else:
            raise ValueError(f"Unsupported format: {output_format}")

    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_url = request.form["youtube_url"]
        output_format = request.form["format"]

        try:
            output_file = process_video(youtube_url, output_format)

            @after_this_request
            def remove_file(response):
                try:
                    os.remove(output_file)
                except Exception as error:
                    app.logger.error(
                        "Error removing or closing downloaded file handle", error
                    )
                return response

            return send_file(output_file, as_attachment=True)

        except Exception as e:
            return f"An error occurred: {str(e)}"

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
