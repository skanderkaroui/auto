import os

from google.cloud import texttospeech

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "text_to_speech_google_key.json"


class TextToSpeech():
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

        # The response's audio_content is binary.
        with open("output.mp3", "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to file "output.mp3"')


if __name__ == "__main__":
    playht_tts = TextToSpeech()

    # Sample text to be converted to speech
    text = "Hey, this is Jennifer from Play. Please hold on a moment, let me just pull up your details real quick."

    # Convert text to speech
    TextToSpeech.text_to_speech(text)
