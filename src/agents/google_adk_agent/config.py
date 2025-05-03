"""Configuration for the Google ADK agent."""

import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables
load_dotenv()

class AgentSettings(BaseModel):
    """Settings for the agent."""
    name: str = "google_adk_agent"
    model: str = os.getenv("GOOGLE_ADK_MODEL_ID", "gemini-2.5-pro-preview-03-25")

class Config(BaseModel):
    """Configuration for the agent."""
    agent_settings: AgentSettings = AgentSettings()
    app_name: str = "google_adk_demo"
