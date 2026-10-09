# TouchGrass AI

**Less scrolling. More living.**

TouchGrass AI is a local-AI-powered web app that helps people spend more time outdoors through personalized nature missions.

## Features

- Generate outdoor missions for 15, 30, or 60 minutes.
- Choose nature exploration, walking, birdwatching, or gardening.
- Select an experience level.
- Generate missions using a locally running Ollama model.
- Track completed missions in browser local storage.
- Use the app without a paid hosted AI API.

## Tech Stack

- Python and Flask
- Ollama
- Qwen 2.5 1.5B
- HTML, CSS, and JavaScript
- Pytest

## Requirements

- Windows, macOS, or Linux
- Python 3.13 or a compatible version
- Ollama installed
- Sufficient RAM and disk space for the selected AI model

## Setup

### 1. Install Ollama

Download Ollama from https://ollama.com/download.

### 2. Download the AI model

Open a terminal and run:

```bash
ollama pull qwen2.5:1.5b
```

### 3. Clone the repository

```bash
git clone https://github.com/utkarshydv27/TouchGrassAI.git
cd TouchGrassAI
```

### 4. Create a virtual environment

On Windows PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Run the application

Keep Ollama running, then start the Flask app:

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Run Tests

With the virtual environment activated, run:

```bash
python -m pytest -v
```

## Why Open Innovation Matters

TouchGrass AI uses Ollama to send prompts to a model running locally instead of relying on a hosted AI API.

- **Privacy:** The app's AI requests go to the local Ollama service, rather than a hosted AI API.
- **Accessibility:** After setup, users can generate missions without paying for a hosted AI API.
- **Model choice:** Developers can experiment with compatible local models.
- **Offline potential:** Mission generation can work without internet access once the model and dependencies are installed, provided the local Ollama service is available.

The application code and the AI model have separate licenses. See the model's own terms before redistributing or using it.

## Privacy and Limitations

- Mission progress is stored in browser local storage.
- Completion is self-reported; it is not GPS-verified.
- The app does not currently determine the user's actual location.
- It does not provide live weather, location-specific facts, or real-time safety information.
- AI-generated outdoor suggestions should be reviewed using human judgment.
- Ollama and a downloaded model are required for AI generation.

## License

The TouchGrass AI application code is licensed under the MIT License. See [LICENSE](LICENSE).

The AI model and other third-party components remain subject to their respective licenses and terms.
