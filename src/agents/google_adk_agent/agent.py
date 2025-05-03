"""Agent module for the Google ADK agent."""

import logging
from dotenv import load_dotenv
from google.adk import Agent

from .config import Config
from .tools.tools import (
    get_weather,
    get_current_time,
)

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Get configuration
configs = Config()

# Create the root agent
root_agent = Agent(
    model=configs.agent_settings.model,
    name=configs.agent_settings.name,
    description="Agent to answer questions about the time, weather, and perform web searches.",
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather "
        "in a city, and perform web searches to find information."
    ),
    tools=[
        get_weather,
        get_current_time,
    ],
)
