import pyaudio
import wave
import os
from queue import Queue
from faster_whisper import WhisperModel
import torch


# Function to transcribe a chunk of audio
def transcribe_chunk(model, file_path):
    segments, info = model.transcribe(file_path)
    return ' '.join(segment.text for segment in segments)

# Function to record a chunk of audio
def record_chunk(p, stream, file_path, chunk_length=1):
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

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f'Using device: {device}')

def capture_voice(queue: Queue):
    # Choose your model settings
    model_size = "medium"
    model = WhisperModel(model_size, device=device, compute_type="float16")

    p = pyaudio.PyAudio()
    stream = p.open(formatranscribe_chunkt=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

    accumulated_transcription = ""

    try:
        while True:
            chunk_file = "temp_chunk.wav"
            record_chunk(p, stream, chunk_file, chunk_length=1)  # Adjust chunk length as needed
            transcription = (model, chunk_file)
            print(transcription)
            os.remove(chunk_file)
            queue.put(transcription)
    except KeyboardInterrupt:
        print("Stopping...")
        with open("log.txt", "w") as log_file:
            log_file.write(accumulated_transcription)
    finally:
        print("LOG:" + accumulated_transcription)
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    q = Queue()
    capture_voice(q)