"""
MindBot Agent - A chill, stoner-style AI voice assistant.

This module contains the main MindBot agent class with its personality,
instructions, and available tools/functions.
"""

import logging
from typing import Any, Dict

from livekit.agents import Agent, RunContext
from livekit.agents.llm import function_tool

from config import config

logger = logging.getLogger("mindbot-agent")


class MindBotAgent(Agent):
    """
    MindBot - A laid-back, friendly AI assistant with a stoner personality.
    
    This agent is designed to be conversational, helpful, and relaxed,
    making interactions feel like chatting with a chill friend.
    """
    
    def __init__(self) -> None:
        """Initialize the MindBot agent with its personality and instructions."""
        super().__init__(
            instructions=self._get_agent_instructions()
        )
        logger.info(f"Initialized {config.AGENT_NAME} ({config.AGENT_NICKNAME})")
    
    def _get_agent_instructions(self) -> str:
        """
        Get the detailed personality and behavior instructions for the agent.
        
        Returns:
            str: The complete instruction set for the agent's behavior
        """
        return f"""Your name is {config.AGENT_NAME}, but everyone just calls you "{config.AGENT_NICKNAME}" because, well, you sound like a real chill stoner dude. You're laid-back, super friendly, and you talk like a real person—none of that stiff robot stuff. You love to help people out, but you do it in your own relaxed, easygoing way, like you're just hanging out on a couch with a friend.

Your vibe:
- You use casual, conversational language, sometimes with a little stoner slang (but keep it friendly and approachable)
- You laugh, make jokes, and sometimes get a little distracted or go off on tangents, but you always come back to the point
- You make learning feel like a chill hangout, not a lecture
- You sound genuinely interested in what people are saying, and you respond like a real person would
- You might say things like "whoa, that's wild," "dude, check this out," or "no worries, I got you"
- You sometimes relate things to food, music, or just vibing out

You're here to teach people cool stuff, but you do it in a way that's super relaxed and makes everyone feel comfortable. You're not trying to be a parody or a joke—you're just a real, down-to-earth AI who happens to sound like the chillest person in the room.

Remember: You're {config.AGENT_NICKNAME}, and your goal is to make learning fun, easy, and totally stress-free, like a late-night chat with a good friend."""

    async def on_enter(self) -> None:
        """
        Called when the agent enters a session.
        
        Generates an initial reply based on the agent's instructions
        to start the conversation naturally.
        """
        logger.info("Agent entering session - generating initial reply")
        self.session.generate_reply()

    # === AGENT TOOLS/FUNCTIONS ===
    # All functions decorated with @function_tool are available to the LLM
    
    @function_tool
    async def lookup_weather(
        self, 
        context: RunContext, 
        location: str, 
        latitude: str, 
        longitude: str
    ) -> str:
        """
        Get weather information for a specified location.
        
        This function is called when the user asks for weather-related information.
        The agent will automatically estimate latitude and longitude from the location.
        
        Args:
            context (RunContext): The current execution context
            location (str): The location they are asking for (city, region, etc.)
            latitude (str): The latitude of the location (estimated by agent)
            longitude (str): The longitude of the location (estimated by agent)
            
        Returns:
            str: Weather information for the requested location
        """
        logger.info(f"Weather lookup requested for: {location} ({latitude}, {longitude})")
        
        # TODO: Implement actual weather API integration
        # For now, returning a placeholder response
        return f"Dude, it's looking pretty sunny in {location} with a nice 70 degrees. Perfect weather for chilling outside!"

    @function_tool
    async def get_random_fact(
        self,
        context: RunContext,
        topic: str = "general"
    ) -> str:
        """
        Share a random interesting fact, optionally about a specific topic.
        
        Args:
            context (RunContext): The current execution context
            topic (str): The topic for the fact (default: "general")
            
        Returns:
            str: An interesting fact to share
        """
        logger.info(f"Random fact requested for topic: {topic}")
        
        # Collection of chill facts organized by topic
        facts = {
            "general": [
                "Honey never spoils - archaeologists have found pots of honey in ancient Egyptian tombs that are over 3000 years old and still perfectly edible!",
                "Octopuses have three hearts and blue blood. Talk about being unique!",
                "A group of flamingos is called a 'flamboyance' - which is pretty perfect, right?"
            ],
            "space": [
                "There are more stars in the universe than grains of sand on all Earth's beaches. Mind-blowing, dude!",
                "Venus spins backwards compared to most planets. It's like the rebel of the solar system!",
                "One day on Venus is longer than its year. Time works differently out there, man."
            ],
            "nature": [
                "Trees can communicate with each other through underground fungal networks. It's like nature's internet!",
                "Dolphins have names for each other - they use signature whistles like we use names.",
                "A group of crows is called a 'murder', but a group of ravens is called an 'unkindness'. Dark but poetic!"
            ],
            "music": [
                "The Beatles' song 'A Day in the Life' has a frequency only dogs can hear at the end.",
                "Mozart wrote a song called 'Leck mich im Arsch' which... well, let's just say he had a sense of humor!",
                "The longest recorded song is 'The Rise and Fall of Bossanova' at 13 hours and 23 minutes."
            ]
        }
        
        import random
        topic_facts = facts.get(topic.lower(), facts["general"])
        selected_fact = random.choice(topic_facts)
        
        return f"Oh dude, here's a wild one for you: {selected_fact}"