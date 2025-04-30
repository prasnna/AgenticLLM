"""
Memory Agent module for implementing agents with memory capabilities.

This module provides two implementations:
1. BedrockMemoryAgent - Uses in-memory storage (for development/testing)
2. PostgresMemoryAgent - Uses PostgreSQL for persistent storage (for production)
"""

from .bedrock_agent_with_memory import BedrockMemoryAgent
from .postgres_memory_agent import PostgresMemoryAgent

__all__ = ["BedrockMemoryAgent", "PostgresMemoryAgent"]
