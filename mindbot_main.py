"""
Main entry point for the MindBot LiveKit Agent.

This is the primary application file that sets up the agent session,
configures all the services (STT, LLM, TTS), and handles the connection
to the LiveKit room.

Usage:
    python mindbot_main.py console  # Run in console mode for testing
    python mindbot_main.py dev      # Run in development mode with hot reload
    python mindbot_main.py start    # Run in production mode
"""

import logging
from typing import Any, Dict

from livekit.agents import (
    AgentSession,
    JobContext,
    JobProcess,
    RoomInputOptions,
    RoomOutputOptions,
    WorkerOptions,
    cli,
    metrics,
)
from livekit.agents.voice import MetricsCollectedEvent
from livekit.plugins import deepgram, openai, silero, elevenlabs
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Import our custom components
from agents import MindBotAgent
from config import config
from utils import setup_logging, get_logger

# Uncomment to enable Krisp background voice/noise cancellation
# from livekit.plugins import noise_cancellation

# Set up logging
setup_logging()
logger = get_logger("mindbot-main")


def prewarm(proc: JobProcess) -> None:
    """
    Prewarm function to initialize models and resources before agent sessions.
    
    This function is called during the worker startup to preload models
    and other resources that can be shared across multiple agent sessions.
    This improves performance by avoiding cold starts.
    
    Args:
        proc (JobProcess): The job process instance
    """
    logger.info("Prewarming models and resources...")
    
    try:
        # Preload the Voice Activity Detection (VAD) model
        # This model is used to detect when users are speaking
        proc.userdata["vad"] = silero.VAD.load()
        logger.info("VAD model loaded successfully")
        
        # TODO: Add other model prewarming here if needed
        # For example: preload TTS models, embedding models, etc.
        
    except Exception as e:
        logger.error(f"Error during prewarming: {e}")
        raise


async def entrypoint(ctx: JobContext) -> None:
    """
    Main entrypoint for agent sessions.
    
    This function is called for each new user session. It sets up the
    agent configuration, initializes all the AI services (STT, LLM, TTS),
    and manages the session lifecycle.
    
    Args:
        ctx (JobContext): The job context containing room and process information
    """
    logger.info(f"Starting new agent session for room: {ctx.room.name}")
    
    # Validate configuration before starting
    if not config.validate():
        logger.error("Invalid configuration - missing required API keys")
        raise ValueError("Missing required API keys in configuration")
    
    # Add room context to all log entries for this session
    ctx.log_context_fields = {
        "room": ctx.room.name,
        "agent": config.AGENT_NAME,
    }
    
    try:
        # Initialize the agent session with all required services
        session = AgentSession(
            # Voice Activity Detection - detects when users are speaking
            vad=ctx.proc.userdata["vad"],
            
            # Large Language Model configuration
            # Using OpenAI's GPT-4.1 with conversation storage enabled
            llm=openai.LLM(
                model=config.LLM_MODEL,
                store="True"  # Enable conversation storage
            ),
            
            # Speech-to-Text configuration  
            # Using Deepgram's Nova-3 model with multilingual support
            stt=deepgram.STT(
                model=config.STT_MODEL,
                language=config.STT_LANGUAGE
            ),
            
            # Text-to-Speech configuration
            # Using ElevenLabs with a specific voice and model
            tts=elevenlabs.TTS(
                voice_id=config.TTS_VOICE_ID,
                model=config.TTS_MODEL
            ),
            
            # Turn detection - uses a transformer model to detect when user is done speaking
            # This helps reduce interruptions and makes conversations more natural
            turn_detection=MultilingualModel(),
        )
        
        # Set up metrics collection for monitoring and analytics
        usage_collector = metrics.UsageCollector()
        
        @session.on("metrics_collected")
        def _on_metrics_collected(ev: MetricsCollectedEvent) -> None:
            """
            Handle metrics collection events.
            
            This function is called whenever metrics are collected during the session.
            It logs the metrics and adds them to the usage collector for summary reporting.
            """
            metrics.log_metrics(ev.metrics)
            usage_collector.collect(ev.metrics)
        
        async def log_usage() -> None:
            """Log usage summary when the session ends."""
            summary = usage_collector.get_summary()
            logger.info(f"Session usage summary: {summary}")
        
        # Register shutdown callback to log usage when session ends
        ctx.add_shutdown_callback(log_usage)
        
        # Start the agent session
        logger.info("Starting agent session...")
        await session.start(
            agent=MindBotAgent(),
            room=ctx.room,
            room_input_options=RoomInputOptions(
                # Uncomment to enable Krisp background voice/noise cancellation
                # noise_cancellation=noise_cancellation.BVC(),
            ),
            room_output_options=RoomOutputOptions(
                # Enable real-time transcription for all participants
                transcription_enabled=True
            ),
        )
        
        # Connect to the LiveKit room
        logger.info("Connecting to LiveKit room...")
        await ctx.connect()
        
        logger.info("Agent session started successfully")
        
    except Exception as e:
        logger.error(f"Error in agent session: {e}")
        raise


def main() -> None:
    """
    Main function to run the LiveKit agent.
    
    This sets up the worker with the entrypoint and prewarm functions,
    then starts the CLI application.
    """
    logger.info(f"Starting {config.AGENT_NAME} LiveKit Agent")
    logger.info(f"Configuration: LLM={config.LLM_MODEL}, STT={config.STT_MODEL}, TTS={config.TTS_MODEL}")
    
    # Configure worker options
    worker_options = WorkerOptions(
        entrypoint_fnc=entrypoint,
        prewarm_fnc=prewarm
    )
    
    # Start the CLI application
    # This handles command-line arguments and starts the appropriate mode
    # (console, dev, or start)
    cli.run_app(worker_options)


if __name__ == "__main__":
    main()