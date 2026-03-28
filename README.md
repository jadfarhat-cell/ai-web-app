# AI Voice Companion

A real-time voice chat application that combines Claude AI for natural conversation, OpenAI Whisper for speech recognition, and ElevenLabs for lifelike text-to-speech.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0+-green?logo=flask&logoColor=white)
![Claude](https://img.shields.io/badge/Claude-AI-purple?logo=anthropic&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- **Voice Input**: Hold-to-record with real-time transcription via OpenAI Whisper
- **AI Conversation**: Natural dialogue powered by Claude (Anthropic)
- **Voice Output**: Lifelike speech synthesis with ElevenLabs (supports custom voice clones)
- **Mobile-First UI**: Responsive dark theme optimized for touch devices
- **Conversation Memory**: Maintains context across messages
- **Text Fallback**: Type messages when voice isn't convenient

## Demo

https://github.com/user-attachments/assets/demo-placeholder

> *Hold the mic button to speak, release to send. The AI responds with both text and voice.*

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   Browser UI    │────▶│   Flask API     │────▶│   Claude AI     │
│   (JavaScript)  │     │   (Python)      │     │   (Anthropic)   │
│                 │◀────│                 │◀────│                 │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
           ┌───────────────┐         ┌───────────────┐
           │               │         │               │
           │ OpenAI Whisper│         │  ElevenLabs   │
           │ (Speech-to-   │         │  (Text-to-    │
           │  Text)        │         │   Speech)     │
           │               │         │               │
           └───────────────┘         └───────────────┘
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Flask (Python) |
| LLM | Claude 3.5 Sonnet (Anthropic) |
| Speech-to-Text | OpenAI Whisper |
| Text-to-Speech | ElevenLabs |
| Frontend | Vanilla JavaScript, CSS3 |
| Audio | Web Audio API, MediaRecorder |

## Quick Start

### Prerequisites

- Python 3.10+
- API keys for:
  - [Anthropic](https://console.anthropic.com/) (Claude)
  - [OpenAI](https://platform.openai.com/) (Whisper)
  - [ElevenLabs](https://elevenlabs.io/) (Text-to-Speech)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-voice-companion.git
   cd ai-voice-companion
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   ```
   http://localhost:5000
   ```

## Configuration

Create a `.env` file with the following variables:

```env
# Required API Keys
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=your_voice_id

# Optional Settings
HOST=0.0.0.0
PORT=5000
DEBUG=false
```

### Getting Your Voice ID

1. Go to [ElevenLabs Voice Lab](https://elevenlabs.io/voice-lab)
2. Select a pre-made voice or clone your own
3. Click the voice and copy the Voice ID from the URL or settings

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve the chat interface |
| `/chat` | POST | Send message, get AI response + audio |
| `/transcribe` | POST | Convert audio to text |
| `/reset` | POST | Clear conversation history |
| `/health` | GET | Health check for deployment |

## Deployment

### Docker

```bash
docker build -t ai-voice-companion .
docker run -p 5000:5000 --env-file .env ai-voice-companion
```

### Railway / Render / Heroku

The app includes a `Dockerfile` and is ready for one-click deployment:

1. Connect your GitHub repository
2. Set environment variables in the platform dashboard
3. Deploy

## Project Structure

```
ai-voice-companion/
├── app.py              # Main Flask application
├── config.py           # Configuration and settings
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container configuration
├── .env.example        # Environment template
├── templates/
│   └── index.html      # Chat interface
└── static/
    └── style.css       # Styling
```

## Customization

### Changing the AI Personality

Edit the `SYSTEM_PROMPT` in `config.py` to customize how the AI responds:

```python
SYSTEM_PROMPT = """You are a helpful assistant who speaks concisely..."""
```

### Using a Different Voice

Update `ELEVENLABS_VOICE_ID` in your `.env` file with any ElevenLabs voice ID.

## License

MIT License - feel free to use this project for learning or as a starting point for your own applications.

## Acknowledgments

- [Anthropic](https://anthropic.com) for Claude AI
- [OpenAI](https://openai.com) for Whisper
- [ElevenLabs](https://elevenlabs.io) for voice synthesis
