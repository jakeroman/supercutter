import json
from whisper import load_model
import warnings

# Ignore warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="whisper")
warnings.filterwarnings("ignore", category=UserWarning, module="whisper.transcribe")


class VideoTranscriber:
    def __init__(self):
        self.model = load_model("base") # Load whisper model

    def transcribe(self, video_path: str, output_path: str):

        # Perform transcription
        result = self.model.transcribe(video_path, word_timestamps=True)
        with open(output_path, "w") as file:
            json.dump(result, file)
