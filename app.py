import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")
print(torch.cuda.is_available())
print(torch.cuda.device_count())
print(torch.cuda.current_device())

if __name__ == "__main__":
    pass
