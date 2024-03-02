import librosa
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC


class AudioTranscriber:
    """Transcribes audio files using a Wav2Vec model.

    Attributes:
        model_name (str): Name of pre-trained Wav2Vec model.
        target_sr (int): Target sampling rate for audio files.
        processor (Wav2Vec2Processor): Processor of the Wav2Vec model.
        model (Wav2Vec2ForCTC): Pre-trained Wav2Vec model.
    """
    def __init__(self, config: dict) -> None:
        """Initializes audio transcriber with model and target sampling rate.

        Args:
            config (dict):
            Parameters relating to model name and target sampling rate.
        """
        self.model_name = config.audio_transcriber.model_name
        self.target_sr = config.audio_transcriber.target_sr
        self.processor = Wav2Vec2Processor.from_pretrained(self.model_name)
        self.model = Wav2Vec2ForCTC.from_pretrained(self.model_name)

    def transcribe_audio(self, file_path: str) -> tuple[str, str]:
        """Transcribes audio from a given file path.

        Args:
            file_path (str): The path to the audio file to be transcribed.

        Returns:
            Tuple[str, str]:
            Containing transcription of the audio and its duration in seconds.
        """
        audio_resampled, _ = librosa.load(file_path, sr=self.target_sr)
        input_values = self.processor(audio_resampled,
                                      return_tensors="pt",
                                      sampling_rate=self.target_sr,
                                      padding="longest").input_values
        logits = self.model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)
        duration = librosa.get_duration(y=audio_resampled, sr=self.target_sr)
        return transcription[0], f"{duration:.1f}"