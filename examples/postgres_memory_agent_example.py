#!/usr/bin/env python3
"""
Example script demonstrating the usage of the PostgreSQL Memory Agent.

This script shows how to initialize and use the PostgresMemoryAgent to have
conversations with memory persistence in a PostgreSQL database.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.memory_agent import PostgresMemoryAgent
from src.utils.env_utils import load_env_vars

def main():
    """Run the PostgreSQL memory agent example."""
    # Load environment variables from .env file
    load_env_vars()

    print("Checking PostgreSQL environment variables...")
    required_vars = ["PG_HOST", "PG_DB", "PG_USER", "PG_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]

    if missing_vars:
        print(f"ERROR: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your .env file before running this example.")
        return

    print("Initializing PostgreSQL Memory Agent...")
    # Initialize the agent with PostgreSQL storage
    agent = PostgresMemoryAgent(
        # Environment variables from .env will be used by default
        # You can override them here if needed for testing:
        # pg_host="your-postgres-host",
        # pg_db="your-database",
        # pg_user="your-username",
        # pg_password="your-password",
        # pg_port="5432",
    )

    print("\nPostgreSQL connection successful!")
    print(f"Using PostgreSQL host: {os.environ.get('PG_HOST')}")
    print(f"Using PostgreSQL database: {os.environ.get('PG_DB')}")

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

    # Display conversation history
    print("\n--- Conversation History (Thread: user-123) ---")
    agent.display_conversation_history("user-123")

    print("\n--- Conversation History (Thread: user-456) ---")
    agent.display_conversation_history("user-456")

    # List all checkpoints
    print("\n--- Checkpoints ---")
    checkpoints = agent.list_checkpoints("user-123")
    print(f"Found {len(checkpoints)} checkpoints for thread user-123")

    print("\nExample completed.")

if __name__ == "__main__":
    main()
