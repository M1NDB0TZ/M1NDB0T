<!-- MindBot - LiveKit Voice Agent -->

<div align="center">

# 🤖 MindBot - Chill AI Voice Assistant

*A laid-back, stoner-style AI voice assistant built with LiveKit Agents*

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![LiveKit](https://img.shields.io/badge/LiveKit-Agents-green.svg)](https://livekit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## 🌟 Overview

MindBot (aka "Stoner MindBot") is a chill, conversational AI voice assistant that makes interactions feel like hanging out with a laid-back friend. Built on the LiveKit Agents framework, it combines real-time voice processing with a relaxed, approachable personality.

### ✨ Features

- **🎙️ Real-time Voice Conversations**: Natural speech-to-text and text-to-speech processing
- **🧠 Smart AI Responses**: Powered by OpenAI's GPT-4.1 with conversational memory
- **🌍 Multi-language Support**: Understands multiple languages via Deepgram Nova-3
- **🎵 High-Quality Voice**: ElevenLabs TTS with custom voice personality
- **🔧 Function Tools**: Weather lookup, random facts, and extensible tool system
- **📊 Usage Metrics**: Built-in analytics and monitoring
- **🚀 Production Ready**: Scalable architecture with Docker support

## 🏗️ Project Structure

```
mindbot/
├── agents/                 # Agent implementations
│   ├── __init__.py
│   └── mindbot_agent.py   # Main MindBot agent class
├── utils/                 # Utility functions and helpers
│   ├── __init__.py
│   └── logging_config.py  # Logging configuration
├── examples/              # Example implementations
│   └── minimal_worker.py  # Basic worker example
├── config.py              # Configuration and settings
├── mindbot_main.py        # Main application entry point
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── Dockerfile-example    # Docker configuration
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- API keys for:
  - [OpenAI](https://platform.openai.com/api-keys) (for LLM)
  - [Deepgram](https://console.deepgram.com/) (for STT)
  - [ElevenLabs](https://elevenlabs.io/) (for TTS)
- [LiveKit](https://livekit.io/) account (for hosting)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mindbot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Configure your API keys**
   ```bash
   # Required API keys in .env
   DEEPGRAM_API_KEY=your_deepgram_key
   OPENAI_API_KEY=your_openai_key
   ELEVEN_API_KEY=your_elevenlabs_key
   
   # LiveKit connection (for production)
   LIVEKIT_URL=your_livekit_url
   LIVEKIT_API_KEY=your_livekit_api_key
   LIVEKIT_API_SECRET=your_livekit_api_secret
   ```

### Running the Agent

#### 🖥️ Console Mode (Testing)
Perfect for quick testing with local audio:
```bash
python mindbot_main.py console
```

#### 🔧 Development Mode
Hot-reload enabled for development:
```bash
python mindbot_main.py dev
```

#### 🚀 Production Mode
Optimized for production deployment:
```bash
python mindbot_main.py start
```

## 🎯 Agent Personality

MindBot has a unique, chill personality:

- **Conversational & Casual**: Talks like a real person, not a robot
- **Laid-back Vibe**: Uses relaxed language and stoner-friendly expressions
- **Helpful & Friendly**: Always ready to help but in a chill way
- **Educational**: Makes learning feel like a fun hangout
- **Authentic**: No forced jokes or fake enthusiasm

### Example Interactions

```
User: "What's the weather like?"
MindBot: "Dude, it's looking pretty sunny with a nice 70 degrees. Perfect weather for chilling outside!"

User: "Tell me something interesting"
MindBot: "Oh dude, here's a wild one for you: Honey never spoils - archaeologists have found pots of honey in ancient Egyptian tombs that are over 3000 years old and still perfectly edible!"
```

## 🔧 Configuration

The agent can be customized through `config.py`:

```python
# Agent Configuration
AGENT_NAME = "MindBot"
AGENT_NICKNAME = "Stoner MindBot"

# AI Models
LLM_MODEL = "gpt-4.1"
STT_MODEL = "nova-3"
TTS_VOICE_ID = "5I61ElyiGkOaijpW7NOD"
TTS_MODEL = "eleven_flash_v2_5"
```

## 🛠️ Available Tools

MindBot comes with built-in function tools:

### Weather Lookup
```python
@function_tool
async def lookup_weather(location: str, latitude: str, longitude: str) -> str:
    """Get weather information for any location"""
```

### Random Facts
```python
@function_tool
async def get_random_fact(topic: str = "general") -> str:
    """Share interesting facts on various topics"""
```

### Adding Custom Tools

To add new tools, create functions in `agents/mindbot_agent.py`:

```python
@function_tool
async def your_custom_tool(self, context: RunContext, param: str) -> str:
    """Your tool description here"""
    # Implementation
    return "Tool response"
```

## 📊 Monitoring & Metrics

The agent includes built-in metrics collection:

- **Usage Tracking**: Token usage, API calls, session duration
- **Performance Metrics**: Response times, error rates
- **Session Analytics**: User interactions, conversation flow

Metrics are automatically logged and can be integrated with monitoring systems.

## 🐳 Docker Deployment

Use the provided Dockerfile for containerized deployment:

```bash
# Build the image
docker build -f Dockerfile-example -t mindbot .

# Run the container
docker run -d --env-file .env mindbot
```

## 🔒 Security & Privacy

- **API Key Management**: Secure environment variable handling
- **Data Privacy**: Configurable conversation storage
- **Access Control**: LiveKit room-based authentication
- **Logging**: Structured, secure logging without sensitive data

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with proper documentation
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LiveKit Team**: For the amazing Agents framework
- **OpenAI**: For powerful language models
- **Deepgram**: For accurate speech recognition
- **ElevenLabs**: For natural text-to-speech

## 📞 Support

For questions, issues, or feature requests:

- 📧 Create an issue in this repository
- 💬 Join the [LiveKit Community](https://livekit.io/join-slack)
- 📚 Check the [LiveKit Documentation](https://docs.livekit.io/agents/)

---

<div align="center">

**Made with ❤️ and a chill vibe**

*Keep it relaxed, keep it real* 🌿

</div>