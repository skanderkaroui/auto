import sounddevice as sd
from scipy.io.wavfile import write

sd.default.channels = 4, None

#   minimum of 16,000 Hz sampling rate 
#   FLAC/LINEAR 16 for audio transmission 
#   Applying noise reduction can decrease accuracy



def record_audio(filename, duration, fs=16000):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    write(filename, fs, recording)
    print("Recording saved to", filename)

record_audio('input.wav', 5)  # Record for 5 seconds

print(sd.query_devices())
