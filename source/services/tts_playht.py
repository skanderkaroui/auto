# tts_playht.py

import io

import numpy as np
import sounddevice as sd
from pydub import AudioSegment
from pyht import Client, TTSOptions, Format

from keys.authentications import PLAYHT_USER_ID, PLAYHT_SECRET_KEY


class PlayHTTTS:
    def __init__(self, user_id, api_key):
        self.client = Client(user_id, api_key)
        self.options = TTSOptions(
            voice="s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json",
            sample_rate=44100,
            format=Format.FORMAT_MP3,
            speed=1,
        )

    def text_to_speech(self, text):
        stream = sd.OutputStream(samplerate=44100, channels=2)
        stream.start()

        buffer = io.BytesIO()

        for chunk in self.client.tts(text=text, voice_engine="PlayHT2.0-turbo", options=self.options):
            buffer.write(chunk)
            buffer.seek(0)
            audio_segment = AudioSegment.from_mp3(buffer)
            audio_data = np.array(audio_segment.get_array_of_samples(), dtype=np.float32) / 32768.0
            audio_data = audio_data.reshape((-1, audio_segment.channels))
            stream.write(audio_data)
            buffer.seek(0)
            buffer.truncate(0)

        stream.stop()


if __name__ == "__main__":
    playht_tts = PlayHTTTS(PLAYHT_USER_ID, PLAYHT_SECRET_KEY)

    # Sample text to be converted to speech
    text = "Hey, this is Jennifer from Play. Please hold on a moment, let me just pull up your details real quick."

    # Convert text to speech
    playht_tts.text_to_speech(text)
