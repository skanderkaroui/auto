import asyncio
import os
import sys
import threading
import torch

from faster_whisper import WhisperModel

from audio_transcriber import AppOptions
from audio_transcriber import AudioTranscriber
from openai_api import OpenAIAPI
from source.utils.audio_utils import get_valid_input_devices, base64_to_audio
from source.utils.file_utils import read_json, write_json, write_audio

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

transcriber: AudioTranscriber = None
event_loop: asyncio.AbstractEventLoop = None
thread: threading.Thread = None
openai_api: OpenAIAPI = None


def get_valid_devices():
    devices = get_valid_input_devices()
    return [
        {
            "index": d["index"],
            "name": f"{d['name']} {d['host_api_name']} ({d['max_input_channels']} in)",
        }
        for d in devices
    ]


def get_dropdown_options():
    data_types = ["model_sizes", "compute_types", "languages"]

    dropdown_options = {}
    for data_type in data_types:
        data = read_json("assets", data_type)
        dropdown_options[data_type] = data[data_type]

    return dropdown_options


def get_user_settings():
    data_types = ["app_settings", "model_settings", "transcribe_settings"]
    user_settings = {}

    try:
        data = read_json("settings", "user_settings")
        for data_type in data_types:
            user_settings[data_type] = data[data_type]
    except Exception as e:
        print(f"Error: {str(e)}")

    return user_settings


def start_transcription(user_settings):
    global transcriber, event_loop, thread, openai_api
    try:
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA GPU is not available. Please check your CUDA installation.")

        # Get the total number of GPUs available
        num_gpus = torch.cuda.device_count()

        # Set the GPU device index
        device_index = user_settings["app_settings"].get("device_index", 0)
        if device_index >= num_gpus:
            raise RuntimeError(f"Invalid GPU device index {device_index}. Available GPUs: {num_gpus}")

        whisper_model = WhisperModel(
            user_settings["model_settings"]["model_size_or_path"],
            device=user_settings["model_settings"]["compute_type"],
            device_index=user_settings["app_settings"]["input_device"],
        )
        app_settings = AppOptions(**user_settings["app_settings"])
        event_loop = asyncio.new_event_loop()

        if app_settings.use_openai_api:
            openai_api = OpenAIAPI()

        transcriber = AudioTranscriber(
            event_loop,
            whisper_model,
            user_settings["transcribe_settings"],
            app_settings,
            openai_api,
        )
        asyncio.set_event_loop(event_loop)
        thread = threading.Thread(target=event_loop.run_forever, daemon=True)
        thread.start()

        transcription_future = asyncio.run_coroutine_threadsafe(
            transcriber.start_transcription(), event_loop
        )
        transcription_result = transcription_future.result()
        print("Transcription Result:")
        print(transcription_result)
    except Exception as e:
        print(f"Error: {str(e)}")


def stop_transcription():
    global transcriber, event_loop, thread, openai_api
    if transcriber is None:
        print("Transcription stopped.")
        return
    transcriber_future = asyncio.run_coroutine_threadsafe(
        transcriber.stop_transcription(), event_loop
    )
    transcriber_future.result()

    if thread.is_alive():
        event_loop.call_soon_threadsafe(event_loop.stop)
        thread.join()
    event_loop.close()
    transcriber = None
    event_loop = None
    thread = None
    openai_api = None

    print("Transcription stopped.")


def audio_transcription(user_settings, base64data):
    global transcriber, openai_api
    try:
        whisper_model = WhisperModel(
            user_settings["model_settings"]["model_size_or_path"],
            device=user_settings["model_settings"]["compute_type"],
            device_index=user_settings["app_settings"]["input_device"],
        )
        app_settings = AppOptions(**user_settings["app_settings"])

        if app_settings.use_openai_api:
            openai_api = OpenAIAPI()

        transcriber = AudioTranscriber(
            event_loop,
            whisper_model,
            user_settings["transcribe_settings"],
            app_settings,
            openai_api,
        )

        audio_data = base64_to_audio(base64data)
        if len(audio_data) > 0:
            write_audio("web", "voice", audio_data)
            transcriber.batch_transcribe_audio(audio_data)

    except Exception as e:
        print(f"Error: {str(e)}")

    openai_api = None


def get_filtered_app_settings(settings):
    valid_keys = AppOptions.__annotations__.keys()
    return {k: v for k, v in settings.items() if k in valid_keys}


def get_filtered_model_settings(settings):
    valid_keys = WhisperModel.__init__.__annotations__.keys()
    return {k: v for k, v in settings.items() if k in valid_keys}


def get_filtered_transcribe_settings(settings):
    valid_keys = WhisperModel.transcribe.__annotations__.keys()
    return {k: v for k, v in settings.items() if k in valid_keys}


def extracting_each_setting(user_settings):
    filtered_app_settings = get_filtered_app_settings(user_settings["app_settings"])
    filtered_model_settings = get_filtered_model_settings(
        user_settings["model_settings"]
    )
    filtered_transcribe_settings = get_filtered_transcribe_settings(
        user_settings["transcribe_settings"]
    )

    write_json(
        "settings",
        "user_settings",
        {
            "app_settings": filtered_app_settings,
            "model_settings": filtered_model_settings,
            "transcribe_settings": filtered_transcribe_settings,
        },
    )

    return filtered_app_settings, filtered_model_settings, filtered_transcribe_settings


def on_close():
    print("Application was closed")

    if transcriber and transcriber.transcribing:
        stop_transcription()
    sys.exit()


if __name__ == "__main__":
    print("Starting the transcription application")
    user_settings = {
        "app_settings": {
            "use_openai_api": False,
            "input_device": 4,
        },
        "model_settings": {
            "model_size_or_path": "base",
            "compute_type": "auto",
            "language": "en",
        },
        "transcribe_settings": {
            "no_speech_prob": 0.6,
            "logprob": -1,
            "beam_size": 5,
        },
    }

    print("User settings:", user_settings)

    start_transcription(user_settings)

    print("Transcription started. Press Ctrl+C to stop.")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        on_close()
