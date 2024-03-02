import os
import pandas as pd
import requests
from omegaconf import DictConfig, OmegaConf


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
    files = {'file': open(file_path, 'rb')}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        data = response.json()
        return data.get("transcription", "")
    else:
        return "Error: Failed to transcribe"


def input_to_csv(config: DictConfig) -> None:
    """ Transcribe audio files iteratively and update to column in dataset
        1. Read a dataset from CSV
        2. transcribe audio files for audio files that matches dataset list
        3. updated column of dataset with transcription
        4. save updated dataset

    Args:
        config (DictConfig): Filepath of dataset
    """
    transcribed_dataset = pd.read_csv(config.data.csv_file_path)

    transcriptions_dict = {}
    for filename in transcribed_dataset['filename']:
        mp3_file_path = os.path.join(config.data.data_dir, filename)
        if os.path.exists(mp3_file_path):
            transcription = transcribe_audio(mp3_file_path, config)
            transcriptions_dict[filename] = transcription
            print(f"Transcribed {filename}")

    transcribed_dataset['generated_text'] = \
        transcribed_dataset['filename'].apply(
            lambda x: transcriptions_dict.get(x, "")
        )

    transcribed_dataset.to_csv(config.data.updated_csv_filepath, index=False)
    print(f"Updated CSV saved to {config.data.updated_csv_filepath}")


if __name__ == "__main__":
    config = load_config()
    input_to_csv(config)