"""
Minimal LiveKit Worker Example

This is a basic example of a LiveKit worker that connects to a room
but doesn't implement any agent functionality. Useful for testing
connections and understanding the basic worker structure.

Usage:
    python examples/minimal_worker.py
"""

import logging
from dotenv import load_dotenv
from livekit.agents import JobContext, WorkerOptions, cli

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("minimal-worker")

# Load environment variables
load_dotenv()


async def entrypoint(ctx: JobContext) -> None:
    """
    Minimal entrypoint that just connects to the room.
    
    Args:
        ctx (JobContext): The job context containing room information
    """
    # Connect to the LiveKit room
    await ctx.connect()
    
    logger.info(f"Connected to room: {ctx.room.name}")
    logger.info("Minimal worker is running... (not doing much though!)")


def main() -> None:
    """Main function to run the minimal worker."""
    logger.info("Starting minimal LiveKit worker")
    
    # Configure and run the worker
    worker_options = WorkerOptions(entrypoint_fnc=entrypoint)
    cli.run_app(worker_options)


if __name__ == "__main__":
    main()