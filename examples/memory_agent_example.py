#!/usr/bin/env python3
"""
Example script demonstrating the usage of the Bedrock Memory Agent.

This script shows how to initialize and use the BedrockMemoryAgent to have
conversations with memory persistence.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.memory_agent import BedrockMemoryAgent
from src.utils.env_utils import load_env_vars

def main():
    """Run the memory agent example."""
    # Load environment variables
    load_env_vars()
    
    print("Initializing Bedrock Memory Agent...")
    # Initialize the agent
    agent = BedrockMemoryAgent()
    
    # First conversation - provide information
    print("\n--- First Conversation ---")
    user_input = "My name is Sarah and I prefer dark mode in all applications. I also like cats."
    print(f"User: {user_input}")
    
    response = agent.invoke(
        [{"role": "user", "content": user_input}],
        thread_id="user-123"
    )
    print(f"Agent: {response['messages'][-1].content}")
    
    # Second conversation - ask about preferences
    print("\n--- Second Conversation ---")
    user_input = "What are my display preferences?"
    print(f"User: {user_input}")
    
    response = agent.invoke(
        [{"role": "user", "content": user_input}],
        thread_id="user-123"
    )
    print(f"Agent: {response['messages'][-1].content}")
    
    # Third conversation - ask about pets
    print("\n--- Third Conversation ---")
    user_input = "What kind of pets do I like?"
    print(f"User: {user_input}")
    
    response = agent.invoke(
        [{"role": "user", "content": user_input}],
        thread_id="user-123"
    )
    print(f"Agent: {response['messages'][-1].content}")
    
    # New thread - test memory persistence across threads
    print("\n--- New Thread ---")
    user_input = "Do you know my name or preferences?"
    print(f"User: {user_input}")
    
    response = agent.invoke(
        [{"role": "user", "content": user_input}],
        thread_id="user-456"
    )
    print(f"Agent: {response['messages'][-1].content}")
    
    print("\nExample completed.")

if __name__ == "__main__":
    main()
