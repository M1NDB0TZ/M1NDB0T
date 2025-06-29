"""
Configuration settings for the MindBot Agent.

This module contains all configuration constants and settings
for the LiveKit Agents application.
"""

import os
from dataclasses import dataclass
from typing import Optional

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

@dataclass
class AgentConfig:
    """Configuration class for the MindBot Agent."""
    
    # Agent personality and behavior
    AGENT_NAME: str = "MindBot"
    AGENT_NICKNAME: str = "Stoner MindBot"
    
    # Model configurations
    LLM_MODEL: str = "gpt-4.1"
    STT_MODEL: str = "nova-3"
    STT_LANGUAGE: str = "multi"
    TTS_VOICE_ID: str = "5I61ElyiGkOaijpW7NOD"
    TTS_MODEL: str = "eleven_flash_v2_5"
    
    # API Keys (loaded from environment)
    DEEPGRAM_API_KEY: Optional[str] = os.getenv("DEEPGRAM_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ELEVEN_API_KEY: Optional[str] = os.getenv("ELEVEN_API_KEY")
    
    # LiveKit connection settings
    LIVEKIT_URL: Optional[str] = os.getenv("LIVEKIT_URL")
    LIVEKIT_API_KEY: Optional[str] = os.getenv("LIVEKIT_API_KEY")
    LIVEKIT_API_SECRET: Optional[str] = os.getenv("LIVEKIT_API_SECRET")
    
    def validate(self) -> bool:
        """Validate that all required configuration is present."""
        required_keys = [
            self.DEEPGRAM_API_KEY,
            self.OPENAI_API_KEY,
            self.ELEVEN_API_KEY
        ]
        return all(key is not None for key in required_keys)

# Global configuration instance
config = AgentConfig()