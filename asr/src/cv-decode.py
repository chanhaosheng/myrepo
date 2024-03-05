import logging
import os

import pandas as pd
import requests
from omegaconf import DictConfig, OmegaConf

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def load_config() -> DictConfig:
    """Load the application configuration from a YAML file.

    Returns:
        DictConfig: Loaded configuration object.
    """
    config_path = "conf/config.yaml"
    return OmegaConf.load(config_path)


def transcribe_audio(file_path: str, config: DictConfig) -> str:
    """Transcribe audio from a file using a specified API.

    Args:
        file_path (str): Path to the audio file to be transcribed.
        config (DictConfig): Application configuration including the API URL.

    Returns:
        str: Transcribed text or an error message.
    """
    url = config.url
    files = {"file": open(file_path, "rb")}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        data = response.json()
        transcription = data.get("transcription", "")
        duration = data.get("duration", "0.0")
        return transcription, duration
    else:
        logging.error("Error: Failed to transcribe file {file_path}")
        return


def input_to_csv(config: DictConfig) -> None:
    """Transcribe audio files iteratively and update to column in dataset
        1. Read a dataset from CSV
        2. transcribe audio files for audio files that matches dataset list
        3. updated column of dataset with transcription
        4. save updated dataset

    Args:
        config (DictConfig): Filepath of dataset
    """
    transcribed_dataset = pd.read_csv(config.data.csv_file_path)

    transcriptions = []
    durations = []

    for filename in transcribed_dataset["filename"]:
        mp3_file_path = os.path.join(config.data.data_dir, filename)
        if os.path.exists(mp3_file_path):
            transcription, duration = transcribe_audio(mp3_file_path, config)
            logging.info(f"Transcribed {filename}")
        else:
            transcription, duration = "", 0.0
            logging.warning(f"Skipped {filename}")

        transcriptions.append(transcription.lower())
        durations.append(float(duration))

    transcribed_dataset["generated_text"] = transcriptions
    transcribed_dataset["duration"] = durations

    transcribed_dataset.to_csv(config.data.updated_csv_filepath, index=False)
    logging.info(f"Updated CSV saved to {config.data.updated_csv_filepath}")


if __name__ == "__main__":
    config = load_config()
    input_to_csv(config)
