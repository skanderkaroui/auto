import io

import numpy as np
import sounddevice as sd
from google.cloud import texttospeech
from pydub import AudioSegment


class TextToSpeech:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def text_to_speech(self, text):
        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Convert binary audio content to an audio segment
        audio_segment = AudioSegment.from_mp3(io.BytesIO(response.audio_content))

        # Convert the audio segment to a numpy array
        samples = np.array(audio_segment.get_array_of_samples())

        # Play the audio
        sd.play(samples, samplerate=audio_segment.frame_rate)
        sd.wait()  # Wait until the audio is done playing

#
# if __name__ == "__main__":
#     tts = TextToSpeech()
#
#     # Sample text to be converted to speech
#     text = "Hey, this is Jennifer from Play. Please hold on a moment, let me just pull up your details real quick."
#
#     # Convert text to speech
#     tts.text_to_speech(text)
