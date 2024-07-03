import pyaudio
import wave
import os
from faster_whisper import WhisperModel
import torch

# Function to record a chunk of audio
def record_chunk(p, stream, file_path, chunk_length):
    frames = []
    for _ in range(0, int(16000 / 1024 * chunk_length)):
        data = stream.read(1024)
        frames.append(data)
    
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()

# Function to transcribe a chunk of audio
def transcribe_chunk(model, file_path):
    segments, info = model.transcribe(file_path)
    return ' '.join(segment.text for segment in segments)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f'Using device: {device}')

def main():
    # Choose your model settings
    model_size = "medium"
    model = WhisperModel(model_size, device=device, compute_type="float16")

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1, rate=16000, input=True, frames_per_buffer=1024)

    # Initialize an empty string to accumulate transcriptions
    accumulated_transcription = ""

    try:
        while True:
            chunk_file = "temp_chunk.wav"
            record_chunk(p, stream, chunk_file, chunk_length=1)  # Adjust chunk length as needed
            transcription = transcribe_chunk(model, chunk_file)
            print(transcription)
            os.remove(chunk_file)
            accumulated_transcription += transcription + " "
    except KeyboardInterrupt:
        print("Stopping...")
        # Write the accumulated transcription to the log file
        with open("log.txt", "w") as log_file:
            log_file.write(accumulated_transcription)
    finally:
        print("LOG: " + accumulated_transcription)
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()













# import sounddevice as sd
# from scipy.io.wavfile import write

# sd.default.channels = 4, None

# #   minimum of 16,000 Hz sampling rate 
# #   FLAC/LINEAR 16 for audio transmission 
# #   Applying noise reduction can reduce the accuracy



# def record_audio(filename, duration, fs=16000):
#     print("Recording...")
#     recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
#     sd.wait()
#     write(filename, fs, recording)
#     print("Recording saved to", filename)

# record_audio('input.wav', 5)  # Record for 5 seconds

# print(sd.query_devices())