# MindBot LiveKit Agent - Production Docker Image
# This Dockerfile creates a minimal, secure container for running the MindBot agent

# Use Python 3.11 slim image for smaller size and better security
ARG PYTHON_VERSION=3.11.6
FROM python:${PYTHON_VERSION}-slim

# Prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Create non-privileged user for security
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "\" \
    --home "/home/mindbot\" \
    --shell "/sbin/nologin\" \
    --uid "${UID}\" \
    mindbot

# Install system dependencies required for building Python packages
RUN apt-get update && \
    apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create cache directory and set permissions
RUN mkdir -p /home/mindbot/.cache && \
    chown -R mindbot:mindbot /home/mindbot/.cache

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies as non-root user
USER mindbot
RUN python -m pip install --user --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=mindbot:mindbot . .

# Pre-download models and dependencies to improve startup time
RUN python mindbot_main.py --help 2>/dev/null || true

# Expose port (if needed for health checks)
EXPOSE 8080

# Health check to ensure the agent is responsive
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health', timeout=5)" || exit 1

# Set the entrypoint to our main application
ENTRYPOINT ["python", "mindbot_main.py"]

# Default command is to start in production mode
CMD ["start"]

# Labels for better container management
LABEL maintainer="Your Name <your.email@example.com>"
LABEL description="MindBot - Chill AI Voice Assistant built with LiveKit Agents"
LABEL version="1.0.0"
LABEL org.opencontainers.image.source="https://github.com/yourusername/mindbot"
LABEL org.opencontainers.image.documentation="https://github.com/yourusername/mindbot/blob/main/README.md"