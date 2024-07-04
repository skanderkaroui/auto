import torch
from TTS.api import TTS

# Function to convert text to speech
def text_to_speech(text, output_path="output.wav"):
    # Initialize the TTS model
    model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=torch.cuda.is_available())

    # Generate speech
    model.tts_to_file(text=text, file_path=output_path)

if __name__ == "__main__":
    sample_text = "This is a sample text to be converted to speech."
    text_to_speech(sample_text)
