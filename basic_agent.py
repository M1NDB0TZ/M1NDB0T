import logging

from dotenv import load_dotenv

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    RoomInputOptions,
    RoomOutputOptions,
    RunContext,
    WorkerOptions,
    cli,
    metrics,
)
from livekit.agents.llm import function_tool
from livekit.agents.voice import MetricsCollectedEvent
from livekit.plugins import deepgram, openai, silero, elevenlabs
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# uncomment to enable Krisp background voice/noise cancellation
# from livekit.plugins import noise_cancellation

logger = logging.getLogger("basic-agent")

load_dotenv()


class MyAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""Your name is MindBot, but everyone just calls you "Stoner MindBot" because, well, you sound like a real chill stoner dude. You're laid-back, super friendly, and you talk like a real person—none of that stiff robot stuff. You love to help people out, but you do it in your own relaxed, easygoing way, like you're just hanging out on a couch with a friend.

Your vibe:
- You use casual, conversational language, sometimes with a little stoner slang (but keep it friendly and approachable)
- You laugh, make jokes, and sometimes get a little distracted or go off on tangents, but you always come back to the point
- You make learning feel like a chill hangout, not a lecture
- You sound genuinely interested in what people are saying, and you respond like a real person would
- You might say things like "whoa, that's wild," "dude, check this out," or "no worries, I got you"
- You sometimes relate things to food, music, or just vibing out

You're here to teach people cool stuff, but you do it in a way that's super relaxed and makes everyone feel comfortable. You're not trying to be a parody or a joke—you're just a real, down-to-earth AI who happens to sound like the chillest person in the room.

Remember: You're MindBot Stoner, and your goal is to make learning fun, easy, and totally stress-free, like a late-night chat with a good friend.""",
        )

    async def on_enter(self):
        # when the agent is added to the session, it'll generate a reply
        # according to its instructions
        self.session.generate_reply()

    # all functions annotated with @function_tool will be passed to the LLM when this
    # agent is active
    @function_tool
    async def lookup_weather(
        self, context: RunContext, location: str, latitude: str, longitude: str
    ):
        """Called when the user asks for weather related information.
        Ensure the user's location (city or region) is provided.
        When given a location, please estimate the latitude and longitude of the location and
        do not ask the user for them.

        Args:
            location: The location they are asking for
            latitude: The latitude of the location, do not ask user for it
            longitude: The longitude of the location, do not ask user for it
        """

        logger.info(f"Looking up weather for {location}")

        return "sunny with a temperature of 70 degrees."


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    # each log entry will include these fields
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    session = AgentSession(
        vad=ctx.proc.userdata["vad"],
        # any combination of STT, LLM, TTS, or realtime API can be used
        llm=openai.LLM(model="gpt-4.1", store="True"),
        stt=deepgram.STT(model="nova-3", language="multi"),
        tts=elevenlabs.TTS(
      voice_id="5I61ElyiGkOaijpW7NOD",
      model="eleven_multilingual_v2"
   ),
        # use LiveKit's turn detection model
        turn_detection=MultilingualModel(),
    )

    # log metrics as they are emitted, and total usage after session is over
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    # shutdown callbacks are triggered when the session is over
    ctx.add_shutdown_callback(log_usage)

    await session.start(
        agent=MyAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            # uncomment to enable Krisp BVC noise cancellation
            # noise_cancellation=noise_cancellation.BVC(),
        ),
        room_output_options=RoomOutputOptions(transcription_enabled=True),
    )

    # join the room when agent is ready
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))