import os
import queue
import torch
import numpy as np
import sounddevice as sd
import threading
import time
from faster_whisper import WhisperModel


class RealTimeTranscriber:
    def __init__(self, model_size="base.en", sample_rate=16000, block_size=1024):
        self.model_size = model_size
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.audio_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.model = None

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
            print("Recording... Press Ctrl+C to stop.")
            try:
                while not self.stop_event.is_set():
                    time.sleep(0.1)
            except KeyboardInterrupt:
                pass

        print("Recording stopped.")
        sd.stop()

    def transcribe_audio(self):
        audio_data = np.array([], dtype=np.float32)
        while not self.stop_event.is_set() or not self.audio_queue.empty():
            try:
                block = self.audio_queue.get(timeout=1)
                audio_data = np.concatenate((audio_data, block.flatten()), axis=0)
                if len(audio_data) >= self.sample_rate * 5:  # Process every 5 seconds of audio
                    self.process_audio_segment(audio_data)
                    audio_data = np.array([], dtype=np.float32)
            except queue.Empty:
                pass

        if len(audio_data) > 0:
            self.process_audio_segment(audio_data)
        print("Transcription stopped.")

    def process_audio_segment(self, audio_data):
        segments, info = self.model.transcribe(audio_data, beam_size=5)
        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
        for segment in segments:
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

    def start(self):
        self.initialize_model()

        record_thread = threading.Thread(target=self.record_audio)
        transcribe_thread = threading.Thread(target=self.transcribe_audio)

        record_thread.start()
        transcribe_thread.start()

        try:
            record_thread.join()
            transcribe_thread.join()
        except KeyboardInterrupt:
            self.stop_event.set()
            record_thread.join()
            transcribe_thread.join()
            print("\nRecording and transcription have been terminated.")


if __name__ == "__main__":
    transcriber = RealTimeTranscriber()
    transcriber.start()
