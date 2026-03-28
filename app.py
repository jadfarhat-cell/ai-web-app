"""
AI Voice Companion

A real-time voice chat application that combines:
- Claude AI for natural conversation
- OpenAI Whisper for speech-to-text
- ElevenLabs for text-to-speech with custom voices

Built with Flask and vanilla JavaScript.
"""

import base64
import logging
import os
import tempfile
from typing import Any

from anthropic import Anthropic
from elevenlabs import ElevenLabs
from flask import Flask, jsonify, render_template, request
from flask.wrappers import Response
from openai import OpenAI

from config import MIME_TYPE_EXTENSIONS, SYSTEM_PROMPT, config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """
    Create and configure the Flask application.

    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)

    # Validate configuration on startup
    missing = config.validate()
    if missing:
        logger.warning(f"Missing configuration: {', '.join(missing)}")
        logger.warning("Some features may not work without proper API keys.")

    return app


# Initialize Flask app
app = create_app()

# Initialize API clients
claude_client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
eleven_client = ElevenLabs(api_key=config.ELEVENLABS_API_KEY)
openai_client = OpenAI(api_key=config.OPENAI_API_KEY)

# Conversation history (in-memory for simplicity)
# For production, consider using Redis or a database
conversation_history: list[dict[str, str]] = []


@app.route("/")
def index() -> str:
    """Serve the main chat interface."""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat() -> tuple[Response, int] | Response:
    """
    Process a chat message and return AI response with audio.

    Expected JSON payload:
        {"message": "user's message text"}

    Returns:
        JSON with 'text' (AI response) and 'audio' (base64 encoded audio)
    """
    global conversation_history

    try:
        data: dict[str, Any] = request.get_json() or {}
        user_message: str = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        logger.info(f"Received message: {user_message[:50]}...")

        # Add user message to conversation history
        conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Trim history to prevent context overflow
        if len(conversation_history) > config.MAX_CONVERSATION_HISTORY:
            conversation_history = conversation_history[-config.MAX_CONVERSATION_HISTORY:]

        # Generate AI response
        response = claude_client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=config.MAX_RESPONSE_TOKENS,
            system=SYSTEM_PROMPT,
            messages=conversation_history
        )

        assistant_message: str = response.content[0].text
        logger.info(f"AI response: {assistant_message[:50]}...")

        # Add assistant message to history
        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        # Generate voice audio
        audio_generator = eleven_client.text_to_speech.convert(
            voice_id=config.ELEVENLABS_VOICE_ID,
            text=assistant_message,
            model_id=config.ELEVENLABS_MODEL
        )

        # Collect audio bytes from generator
        audio_bytes = b"".join(chunk for chunk in audio_generator)
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

        logger.info(f"Generated {len(audio_bytes)} bytes of audio")

        return jsonify({
            "text": assistant_message,
            "audio": audio_base64
        })

    except Exception as e:
        logger.error(f"Chat error: {type(e).__name__}: {e}")
        return jsonify({"error": "Failed to process message"}), 500


@app.route("/transcribe", methods=["POST"])
def transcribe() -> tuple[Response, int] | Response:
    """
    Transcribe audio to text using OpenAI Whisper.

    Expected JSON payload:
        {"audio": "base64 encoded audio", "mimeType": "audio/webm"}

    Returns:
        JSON with 'text' (transcribed text)
    """
    try:
        data: dict[str, Any] = request.get_json() or {}
        audio_base64: str = data.get("audio", "")
        mime_type: str = data.get("mimeType", "audio/webm")

        if not audio_base64:
            return jsonify({"error": "No audio provided"}), 400

        # Determine file extension from MIME type
        ext = MIME_TYPE_EXTENSIONS.get(mime_type, ".webm")

        # Decode base64 audio
        audio_bytes = base64.b64decode(audio_base64)
        logger.info(f"Received {len(audio_bytes)} bytes of audio ({mime_type})")

        # Save to temporary file (Whisper API requires a file)
        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as f:
            f.write(audio_bytes)
            temp_path = f.name

        try:
            # Transcribe with Whisper
            with open(temp_path, "rb") as audio_file:
                transcript = openai_client.audio.transcriptions.create(
                    model=config.WHISPER_MODEL,
                    file=audio_file
                )

            text = transcript.text.strip()
            logger.info(f"Transcribed: {text[:50]}...")
            return jsonify({"text": text})

        finally:
            # Clean up temporary file
            os.unlink(temp_path)

    except Exception as e:
        logger.error(f"Transcription error: type(e).__name__}: {e}")
        return jsonify({"error": "Failed to transcribe audio"}), 500


@app.route("/reset", methods=["POST"])
def reset() -> Response:
    """
    Reset the conversation history.

    Returns:
        JSON with status confirmation
    """
    global conversation_history
    conversation_history = []
    logger.info("Conversation history reset")
    return jsonify({"status": "ok"})


@app.route("/health")
def health() -> Response:
    """
    Health check endpoint for monitoring and deployment.

    Returns:
        JSON with health status
    """
    return jsonify({
        "status": "healthy",
        "version": "1.0.0"
    })


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  AI Voice Companion")
    print("=" * 50)
    print(f"\n  Open http://localhost:{config.PORT} in your browser\n")

    app.run(
        debug=config.DEBUG,
        host=config.HOST,
        port=config.PORT
    )
