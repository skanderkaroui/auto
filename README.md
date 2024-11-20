# Auto: AI Voice Assistant

**Auto** is an AI-powered voice assistant designed for real-time voice-to-text detection, natural language processing, and text-to-speech synthesis. It leverages cutting-edge technologies including **Faster Whisper** for speech recognition, **OpenAI API** through Azure, and **Google Speech API** via GCP for text-to-speech functionality.

---

## Features

- **Voice-to-Text**: Utilizes **Faster Whisper** for accurate and fast speech recognition.
- **Text Processing**: Processes recognized text using the **OpenAI API** integrated via Azure for intelligent responses.
- **Text-to-Speech**: Converts processed text to speech using **Google Text-to-Speech API** from GCP.

---

## Project History

This project was initially designed as a bot to enhance meeting experiences. The original goal was to develop a browser extension that integrates seamlessly with **Google Meet**, allowing the assistant to join meetings and interact in real-time. However, due to the inability to output audio from a Google Meet API instance, the project transitioned to using the **Microsoft Graph API** to explore integration with **Microsoft Teams**.

Despite efforts to integrate with Microsoft Teams, the **Microsoft Graph API** presented accessibility challenges, preventing successful implementation. As a result, the project now focuses on running the assistant locally for testing and demonstrating its functionalities.

---

## Installation

### Prerequisites

1. **Python**: Ensure Python 3.8+ is installed on your system.
2. **CUDA**: For enhanced performance on systems with NVIDIA GPUs, install CUDA with the following command:
   ```bash
   pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/skanderkaroui/auto.git
   cd auto
   ```

2. Install dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   * Create a `.env` file and add:
     ```makefile
     AZURE_OPENAI_API_KEY=your_azure_openai_api_key
     AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
     ```
   * For Google Text-to-Speech, follow the steps to enable the API and initialize the `gcloud` CLI:
     ```bash
     gcloud init
     ```
     Refer to the Google Cloud Text-to-Speech documentation.

## Usage

1. **Check CUDA Availability**: Use the `app.py` file to test if CUDA is available on your system:
   ```bash
   python app.py
   ```

2. **Run the Assistant**: Start the conversation generator service:
   ```bash
   python source/services/conversation_generator_service.py
   ```

3. **Model Selection**: The assistant automatically uses the `base.en` model by default. You can customize the model by modifying the `model_sizes` in the script. Available models:
   ```json
   {
     "tiny": "tiny",
     "tiny.en": "tiny.en",
     "base": "base",
     "base.en": "base.en",
     "small": "small",
     "small.en": "small.en",
     "medium": "medium",
     "medium.en": "medium.en",
     "large-v1": "large-v1",
     "large-v2": "large-v2",
     "large-v3": "large-v3",
     "local_model": "local_model"
   }
   ```

## Notes and Troubleshooting

* If you encounter issues with dependencies, refer to `notes.txt` for additional installation tips and troubleshooting steps.

## Future Plans

* Explore integration with **Microsoft Graph API** for connecting with Microsoft Teams.
* Add support for browser-based usage once API limitations are resolved.

## References

- [Google Cloud Text-to-Speech Documentation](https://cloud.google.com/text-to-speech/docs/create-audio-text-command-line)
- [Faster Whisper](https://github.com/SYSTRAN/faster-whisper)
- [Azure OpenAI Service Implementation](https://learn.microsoft.com/en-us/azure/ai-services/openai/chatgpt-quickstart?tabs=command-line%2Cjavascript-keyless%2Ctypescript-keyless%2Cpython-new&pivots=programming-language-python)

Feel free to contribute or raise issues for improvements!
