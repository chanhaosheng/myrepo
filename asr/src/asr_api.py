import os

from flask import Flask, jsonify, request
from omegaconf import OmegaConf
from transcribe import AudioTranscriber

app = Flask(__name__)


config_path = "conf/config.yaml"
config = OmegaConf.load(config_path)


transcriber = AudioTranscriber(config)


@app.route("/ping", methods=["GET"])
def ping():
    return "pong"


@app.route("/asr", methods=["POST"])
def transcribe_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    temp_dir = "data/temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    temp_path = os.path.join(temp_dir, file.filename)
    file.save(temp_path)

    transcription, duration = transcriber.transcribe_audio(temp_path)

    os.remove(temp_path)

    response = {"transcription": transcription, "duration": duration}
    return jsonify(response)


if __name__ == "__main__":
    app.run(port=8001)
