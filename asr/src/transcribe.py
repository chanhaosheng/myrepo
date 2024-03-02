import librosa
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC


class AudioTranscriber:
    def __init__(self, config):
        self.model_name = config.audio_transcriber.model_name
        self.target_sr = config.audio_transcriber.target_sr
        self.processor = Wav2Vec2Processor.from_pretrained(self.model_name)
        self.model = Wav2Vec2ForCTC.from_pretrained(self.model_name)

    def transcribe_audio(self, file_path):
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