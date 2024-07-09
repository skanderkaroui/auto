import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")
print(torch.cuda.is_available())
print(torch.cuda.device_count())
print(torch.cuda.current_device())

import pyaudio

p = pyaudio.PyAudio()

for i in range(p.get_device_count()):
    print(f"Device {i}: {p.get_device_info_by_index(i)['name']}")

p.terminate()

if __name__ == "__main__":
    pass
