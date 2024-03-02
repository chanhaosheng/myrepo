import os
import pandas as pd
import requests
from omegaconf import OmegaConf


def load_config():
    config_path = "conf/config.yaml"
    return OmegaConf.load(config_path)


def transcribe_audio(file_path, config):
    url = config.url
    files = {'file': open(file_path, 'rb')}
    response = requests.post(url, files=files)
    if response.status_code == 200:
        data = response.json()
        return data.get("transcription", "")
    else:
        return "Error: Failed to transcribe"


def input_to_csv(config):
    # Step 1: Read the CSV
    transcribed_dataset = pd.read_csv(config.data.csv_file_path)

    # Step 2: Iterate over audio files and transcribe
    transcriptions_dict = {}
    for filename in transcribed_dataset['filename']:
        mp3_file_path = os.path.join(config.data.data_dir, filename)
        if os.path.exists(mp3_file_path):
            transcription = transcribe_audio(mp3_file_path, config)
            transcriptions_dict[filename] = transcription
            print(f"Transcribed {filename}")

    # Step 3: Update dataset with transcriptions
    transcribed_dataset['generated_text'] = \
        transcribed_dataset['filename'].apply(
            lambda x: transcriptions_dict.get(x, "")
        )

    # Step 4: Save updated dataset as CSV
    transcribed_dataset.to_csv(config.data.updated_csv_filepath, index=False)
    print(f"Updated CSV saved to {config.data.updated_csv_filepath}")


if __name__ == "__main__":
    config = load_config()
    input_to_csv(config)