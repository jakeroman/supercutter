import json
import torch
import warnings
import whisper

WHISPER_MODEL = "medium" # Change to "base", "small", or "tiny" if large model is too much for the hardware.

# Ignore warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="whisper")
warnings.filterwarnings("ignore", category=UserWarning, module="whisper.transcribe")

class VideoTranscriber:
    def __init__(self):
        # Detect GPU and move model to CUDA if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisper.load_model(WHISPER_MODEL).to(self.device)  # Load model on GPU
        print("Running Whisper on",self.device.upper())

    def transcribe(self, video_path: str, output_path: str):
        # Perform transcription with GPU optimization
        result = self.model.transcribe(
            video_path, 
            word_timestamps=True,
            temperature=0,  
            beam_size=5,   
            best_of=5,         
            no_speech_threshold=0.2, 
            fp16=True if self.device == "cuda" else False  # Enable FP16 only for GPU
        )

        # Save transcription to a JSON file
        with open(output_path, "w") as file:
            json.dump(result, file)