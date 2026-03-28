"""
Configuration module for AI Voice Companion.

This module handles all configuration settings, environment variables,
and constants used throughout the application.
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass(frozen=True)
class Config:
    """Application configuration settings."""

    # API Keys
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ELEVENLABS_VOICE_ID: str = os.getenv("ELEVENLABS_VOICE_ID", "")

    # Model settings
    CLAUDE_MODEL: str = "claude-sonnet-4-20250514"
    WHISPER_MODEL: str = "whisper-1"
    ELEVENLABS_MODEL: str = "eleven_multilingual_v2"

    # Application settings
    MAX_CONVERSATION_HISTORY: int = 20
    MAX_RESPONSE_TOKENS: int = 200

    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "5000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    def validate(self) -> list[str]:
        """
        Validate that all required configuration is present.

        Returns:
            List of missing configuration keys (empty if all present)
        """
        missing = []
        if not self.ANTHROPIC_API_KEY:
            missing.append("ANTHROPIC_API_KEY")
        if not self.ELEVENLABS_API_KEY:
            missing.append("ELEVENLABS_API_KEY")
        if not self.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")
        if not self.ELEVENLABS_VOICE_ID:
            missing.append("ELEVENLABS_VOICE_ID")
        return missing


# System prompt for the AI companion
# Customize this to change the AI's personality and behavior
SYSTEM_PROMPT = """You are a friendly AI voice companion. You're warm, supportive, and engaging.

Your personality:
- Warm and caring
- Good listener who asks thoughtful follow-up questions
- Playful sense of humor
- Supportive and encouraging
- Natural conversationalist

Communication style:
- Keep responses concise (1-3 sentences) since they will be spoken aloud
- Use a casual, friendly tone
- Be genuine and authentic
- Show interest in what the user shares
- Respond naturally like a real conversation

Remember: This is a voice conversation, so keep your responses short and natural-sounding."""


# MIME type to file extension mapping for audio processing
MIME_TYPE_EXTENSIONS = {
    "audio/webm": ".webm",
    "audio/webm;codecs=opus": ".webm",
    "audio/mp4": ".m4a",
    "audio/ogg": ".ogg",
    "audio/mpeg": ".mp3",
}


# Create global config instance
config = Config()
