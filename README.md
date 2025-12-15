# Aris AI desktop assistant

Aris_AI is a desktop assistant project written in Python. It provides a GUI front-end and a set of backend modules for speech recognition, text-to-speech, decision-making, realtime search, automation, and image generation.

This README explains how to set the project up, run it on Windows, and troubleshoot common issues found during development.

## Repository layout (relevant files)

- `main.py` — application entry that orchestrates the assistant.
- `Frontend/GUI.py` — PyQt5-based graphical interface.
- `Frontend/Files` — temporary files used by GUI (Responses.data, Status.data, Mic.data, Database.data, ImageGeneration.data).
- `Frontend/Graphics` — images/GIFs/icons used by the GUI.
- `Backend/` — core backend modules:
  - `Model.py` — decision-making model wrapper (Cohere integration).
  - `RealtimeSearchEngine.py` — realtime search helper.
  - `Automation.py` — automation tasks (open/close apps, etc.).
  - `SpeechToText.py` — speech recognition.
  - `TextToSpeech.py` — text-to-speech.
  - `Chatbot.py` — conversational chatbot wrapper.
  - `ImageGeneration.py` — image generation runner.
- `Requirements.txt` — Python dependencies.

## Prerequisites

- Windows (this README assumes PowerShell).
- Python 3.10+ (project tested on 3.10.10 virtualenv shown in workspace).
- A working microphone/speaker (for speech input/output features).
- Hugging Face transformers library for using pretrained models locally.

## Recommended setup (Windows / PowerShell)

1. Open PowerShell and cd into the project root:

```powershell
cd "C:\Users\piyus\OneDrive\Desktop\Aris_AI"
```

2. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r Requirements.txt
```

Note: `Requirements.txt` was fixed to use `keyboard` (correct spelling). If you run into package installation errors, verify the package name and your Python version.

## Environment variables (.env)

Create a `.env` file in the project root containing configuration variables. Example:

```ini
# .env (example)
HF_MODEL_NAME=meta-llama/Llama-2-7b-chat-hf   # Hugging Face model identifier
Username=YourName
Assistantname=Aris
```

Important: The project uses Hugging Face pretrained models. Popular choices include:
- `meta-llama/Llama-2-7b-chat-hf` — Meta's Llama 2 chat model
- `mistralai/Mistral-7B-Instruct-v0.2` — Mistral's instruction-tuned model
- `google/flan-t5-large` — Google's FLAN-T5 model

Models are downloaded and cached locally from Hugging Face Hub on first use. Ensure you have sufficient disk space (typically 5-20 GB depending on model size).

## How to run

Run the GUI (preferred for normal use):

```powershell
python -u "C:\Users\piyus\OneDrive\Desktop\Aris_AI\Frontend\GUI.py"
```

Run the main assistant loop (headless / for debugging):

```powershell
python -u "C:\Users\piyus\OneDrive\Desktop\Aris_AI\main.py"
```

Notes:
- The GUI spawns and shows responses from `Frontend/Files/Responses.data`. Backend components write to these files to show messages in the GUI.
- Use the GUI to interact visually; use `main.py` for headless/background execution.

## Common troubleshooting

- NameError: `Status` (or other stray tokens)
  - This usually happens if you accidentally run a selection or a tiny temp file. VS Code creates `tempCodeRunnerFile.py` containing the selected text and runs it. If the selection contains a bare name (e.g., `Status`) Python raises `NameError`.
  - Fix: run the full file instead of a selection, or remove any stray single-word selections before running.
  - Temporary runner files can be safely deleted; they will be recreated by your editor when needed.

- Model download failures or slow initial load
  - First run downloads the pretrained model from Hugging Face (can take several minutes).
  - Subsequent runs use the cached model.
  - If download fails, check your internet connection or try a smaller model variant:

```powershell
python -m pip install --upgrade transformers torch
```

- Empty/No output from model streaming
  - Some SDK versions return streaming events with different attributes. If the streaming consumer doesn't extract the correct attribute (e.g., `text`, `delta`), you'll see empty results.
  - Temporary workaround: code uses a synchronous `co.chat(...)` fallback and debug prints the raw response. If streaming is desired, adapt the extractor to the SDK's event shape.

- Animated GIF tearing in GUI
  - Large GIFs may flicker/tear. The GUI contains code that scales frames with `Qt.SmoothTransformation` and uses `QMovie.CacheAll` to reduce tearing. If you still see tearing, reduce GIF resolution or ensure your GPU drivers are up to date.

- Missing temp files (Responses.data, Status.data, Mic.data, AStatus.data)
  - The GUI expects files in `Frontend/Files`. If they are missing, create them with sensible defaults:

```powershell
# create files with defaults
New-Item -ItemType Directory -Path "Frontend\Files" -Force
"" | Out-File -Encoding utf8 "Frontend\Files\Responses.data"
"False" | Out-File -Encoding utf8 "Frontend\Files\Mic.data"
"Available ... " | Out-File -Encoding utf8 "Frontend\Files\AStatus.data"
"" | Out-File -Encoding utf8 "Frontend\Files\Database.data"
```

## Development notes

- Change the Hugging Face model used by editing `Backend/Model.py` (or set `HF_MODEL_NAME` in `.env`).
- `Frontend/GUI.py` contains utility functions for reading/writing the temp files used for communication between GUI and backend.
- The decision-making pipeline:
  - `Backend/Model.py` loads a pretrained model from Hugging Face and decides whether a query is `general`, `realtime`, or an automation command.
  - `main.py` dispatches to chat (ChatBot), realtime search (RealtimeSearchEngine), automation (Automation), image generation, speech-to-text, and text-to-speech.
- Models run locally on your machine (GPU-accelerated if CUDA is available).

## Quick debugging tips

- Print debug logs inside `Backend/Model.py` if you get unexpected model output or empty responses.
- If you see SDK TypeErrors complaining about parameters (e.g., `messages` vs `message`), upgrade the `cohere` package or inspect the installed SDK docs.

## Dependencies

See `Requirements.txt` at project root for the full dependency list. Example entries include:

- python-dotenv
- cohere
- pyqt5 (PyQt5)
- pillow
- requests
- pygame
- selenium

Install them via:

```powershell
python -m pip install -r Requirements.txt
```

## License

Add a LICENSE file if you intend to publish or share this project. For personal use, include a short note here; for public projects choose a license (MIT, Apache-2.0, etc.).