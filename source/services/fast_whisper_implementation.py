import os
import queue
import threading
import time

import keyboard
import numpy as np
import sounddevice as sd
import torch
from faster_whisper import WhisperModel

from openai_api import OpenAIAPI


class RealTimeTranscriber:
    def __init__(self, model_size="base.en", sample_rate=16000, block_size=1024):
        self.model_size = model_size
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.audio_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.model = None
        self.openai_api = OpenAIAPI()

    def initialize_model(self):
        torch.cuda.empty_cache()
        os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
        self.model = WhisperModel(self.model_size, device="cuda", compute_type="float16")

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.audio_queue.put(indata.copy())

    def record_audio(self):
        with sd.InputStream(samplerate=self.sample_rate, blocksize=self.block_size, channels=1,
                            callback=self.audio_callback):
            print("Recording... Press 'esc' to stop.")
            while not self.stop_event.is_set():
                time.sleep(0.1)
            print("Recording stopped.")
            sd.stop()

    def transcribe_audio(self):
        audio_data = []
        first_message = True
        while not self.stop_event.is_set() or not self.audio_queue.empty():
            try:
                block = self.audio_queue.get(timeout=1)
                audio_data.append(block)
            except queue.Empty:
                pass

        if len(audio_data) > 0:
            audio_data = np.concatenate(audio_data, axis=0).flatten()
            segments, info = self.model.transcribe(audio_data, beam_size=5)

            transcribed_text = ""
            for segment in segments:
                transcribed_text += segment.text + " "

            print("Transcribed Text: ", transcribed_text)

            # Send transcribed text to ChatGPT
            try:
                response = self.openai_api.response_generation(transcribed_text, first_message=first_message)
                print("ChatGPT Response: ", response)
                first_message = False
            except Exception as e:
                print("Error sending to ChatGPT: ", str(e))

            # for segment in segments:
            #     print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        print("Transcription stopped.")

    def run(self):
        while True:
            self.stop_event.clear()
            self.audio_queue = queue.Queue()  # Reset the queue for the new recording session
            record_thread = threading.Thread(target=self.record_audio)
            transcribe_thread = threading.Thread(target=self.transcribe_audio)

            record_thread.start()
            transcribe_thread.start()

            keyboard.add_hotkey('esc', lambda: self.stop_event.set())  # Using 'esc' as an example stop key
            print("Press 'esc' to stop recording and transcription.")
            while not self.stop_event.is_set():
                time.sleep(0.1)

            self.stop_event.set()
            record_thread.join()
            transcribe_thread.join()
            print("Recording and transcription have been terminated.")
            print("Starting a new recording now.")


if __name__ == "__main__":
    transcriber = RealTimeTranscriber()
    transcriber.initialize_model()
    transcriber.run()
