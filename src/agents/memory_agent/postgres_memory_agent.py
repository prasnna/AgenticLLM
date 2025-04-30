#!/usr/bin/env python3
"""
PostgreSQL Memory Agent: An agent with memory capabilities using AWS Bedrock and LangMem

This module implements an agent with memory capabilities using AWS Bedrock as the
base LLM and LangMem for memory management with PostgreSQL for persistent storage.
"""

import os
from typing import Dict, List, Any, Optional
from langchain_aws import ChatBedrockConverse
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.prebuilt import create_react_agent
from langgraph.utils.config import get_store
from langmem import create_manage_memory_tool, create_search_memory_tool
from src.utils.env_utils import get_env_var, load_env_vars


class PostgresMemoryAgent:
    """
    An agent with memory capabilities using AWS Bedrock and LangMem with PostgreSQL storage.

    This agent can store and retrieve information across conversations using
    LangMem's memory management tools and AWS Bedrock as the base LLM.
    The memories are stored in a PostgreSQL database for persistence.
    """

    def __init__(
        self,
        model_id: Optional[str] = None,
        credentials_profile_name: Optional[str] = None,
        embedding_model: str = "openai:text-embedding-3-small",
        embedding_dims: int = 1536,
        pg_host: Optional[str] = None,
        pg_db: Optional[str] = None,
        pg_user: Optional[str] = None,
        pg_password: Optional[str] = None,
        pg_port: Optional[str] = None,
    ):
        """
        Initialize the PostgresMemoryAgent.

        Args:
            model_id: The Bedrock model ID to use. If None, will use the MODEL_ID from environment.
            credentials_profile_name: AWS credentials profile name. If None, will use default credentials.
            embedding_model: The embedding model to use for memory storage.
            embedding_dims: The dimensions of the embedding vectors.
            pg_host: PostgreSQL host. If None, will use PG_HOST from environment.
            pg_db: PostgreSQL database name. If None, will use PG_DB from environment.
            pg_user: PostgreSQL username. If None, will use PG_USER from environment.
            pg_password: PostgreSQL password. If None, will use PG_PASSWORD from environment.
            pg_port: PostgreSQL port. If None, will use PG_PORT from environment.
        """
        # Load environment variables
        load_env_vars()

        # Get model ID from environment if not provided
        if model_id is None:
            model_id = get_env_var("MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")

        # Get AWS profile from environment if not provided
        if credentials_profile_name is None:
            credentials_profile_name = get_env_var("BED_ROCK_AWS_PROFILE", "saml")

        # Get PostgreSQL connection details from environment if not provided
        if pg_host is None:
            pg_host = get_env_var("PG_HOST")
        if pg_db is None:
            pg_db = get_env_var("PG_DB")
        if pg_user is None:
            pg_user = get_env_var("PG_USER")
        if pg_password is None:
            pg_password = get_env_var("PG_PASSWORD")
        if pg_port is None:
            pg_port = get_env_var("PG_PORT", "5432")  # Default port is typically 5432

        # Construct PostgreSQL connection string
        postgres_connection_string = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"

        # Initialize PostgreSQL checkpointer
        print(f"Initializing PostgreSQL checkpointer at {pg_host}...")
        # Create a connection pool to keep the connection alive
        try:
            print("Creating PostgreSQL connection...")
            from psycopg_pool import ConnectionPool
            # Store the pool as an instance variable to keep it alive
            # Set autocommit=True to allow CREATE INDEX CONCURRENTLY
            self.pool = ConnectionPool(postgres_connection_string, kwargs={"autocommit": True})
            # Create the checkpointer using the pool
            self.checkpointer = PostgresSaver(self.pool)
            # Setup the checkpointer to create the necessary tables
            print("Setting up PostgreSQL tables...")
            self.checkpointer.setup()
            print("PostgreSQL connection and tables created successfully")
        except Exception as e:
            print(f"Error creating PostgreSQL connection: {str(e)}")
            raise

        # Initialize Bedrock LLM
        self.llm = ChatBedrockConverse(
            model=model_id,
            credentials_profile_name=credentials_profile_name,
        )

        # Create agent with memory capabilities
        self.agent = create_react_agent(
            self.llm,
            prompt=self._prompt_function,
            tools=[
                # Add memory management tool
                create_manage_memory_tool(namespace=("memories",)),
                # Add memory search tool
                create_search_memory_tool(namespace=("memories",)),
            ],
            # Provide checkpointer for conversation history
            checkpointer=self.checkpointer,
        )

    def _prompt_function(self, state: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Prepare the messages for the LLM with relevant memories.

        Args:
            state: The current state of the conversation.

        Returns:
            A list of messages with the system message containing memories.
        """
        # Get store from configured contextvar
        store = get_store()

        # Search for relevant memories based on the latest message
        memories = ""
        if store is not None:
            try:
                memories = store.search(
                    ("memories",),
                    query=state["messages"][-1].content,
                )
            except Exception as e:
                print(f"Error searching memories: {str(e)}")
                # Continue with empty memories

        # Create system message with memories
        system_msg = f"""You are a helpful assistant with memory capabilities.

## Memories
<memories>
{memories}
</memories>

You can store important information about the user by using the manage_memory tool.
You can search for information using the search_memory tool.
When you learn something important about the user, make sure to store it in your memory.
"""

        # Return messages with system message first
        return [{"role": "system", "content": system_msg}, *state["messages"]]

    def invoke(self, messages: List[Dict[str, str]], thread_id: str = "default") -> Dict[str, Any]:
        """
        Invoke the agent with the given messages.

        Args:
            messages: A list of messages to send to the agent.
            thread_id: The ID of the conversation thread.

        Returns:
            The response from the agent.
        """
        config = {"configurable": {"thread_id": thread_id}}
        return self.agent.invoke({"messages": messages}, config=config)

    def stream(self, messages: List[Dict[str, str]], thread_id: str = "default"):
        """
        Stream the agent's response with the given messages.

        Args:
            messages: A list of messages to send to the agent.
            thread_id: The ID of the conversation thread.

        Returns:
            A generator yielding chunks of the agent's response.
        """
        config = {"configurable": {"thread_id": thread_id}}
        return self.agent.stream({"messages": messages}, config=config)

    def get_checkpoint(self, thread_id="default"):
        """
        Get the checkpoint for a specific thread.

        Args:
            thread_id: The ID of the conversation thread

        Returns:
            The checkpoint data
        """
        config = {"configurable": {"thread_id": thread_id}}
        return self.checkpointer.get(config)

    def list_checkpoints(self, thread_id="default"):
        """
        List all checkpoints for a specific thread.

        Args:
            thread_id: The ID of the conversation thread

        Returns:
            A list of checkpoint tuples
        """
        config = {"configurable": {"thread_id": thread_id}}
        return list(self.checkpointer.list(config))

    def display_conversation_history(self, thread_id="default"):
        """
        Display the conversation history for a specific thread.

        Args:
            thread_id: The ID of the conversation thread
        """
        checkpoint = self.get_checkpoint(thread_id)
        if not checkpoint:
            print(f"No conversation history found for thread {thread_id}")
            return

        messages = checkpoint.get("channel_values", {}).get("messages", [])

        print(f"=== Conversation History (Thread: {thread_id}) ===")
        print(f"Total messages: {len(messages)}")
        print("=" * 50)

        for i, message in enumerate(messages, 1):
            role = message.type if hasattr(message, 'type') else message.get('role', 'unknown')
            content = message.content if hasattr(message, 'content') else message.get('content', '')

            print(f"Message #{i} ({role})")
            print(f"Content: {content}")
            print("-" * 50)


# Example usage
def example_usage():
    """Example usage of the PostgresMemoryAgent."""
    # Initialize the agent
    agent = PostgresMemoryAgent()

    # First conversation - provide information
    response = agent.invoke(
        [{"role": "user", "content": "My name is John and I prefer dark mode in all applications."}],
        thread_id="thread-1"
    )
    print("First response:", response["messages"][-1].content)

    # Second conversation - ask about name
    response = agent.invoke(
        [{"role": "user", "content": "What's my name?"}],
        thread_id="thread-1"
    )
    print("Second response:", response["messages"][-1].content)

    # Third conversation - ask about preferences
    response = agent.invoke(
        [{"role": "user", "content": "What are my display preferences?"}],
        thread_id="thread-1"
    )
    print("Third response:", response["messages"][-1].content)

    # New thread - test memory persistence across threads
    response = agent.invoke(
        [{"role": "user", "content": "Do you know my name or preferences?"}],
        thread_id="thread-2"
    )
    print("New thread response:", response["messages"][-1].content)

    # Display conversation history
    print("\nConversation History (Thread 1):")
    agent.display_conversation_history("thread-1")

    print("\nConversation History (Thread 2):")
    agent.display_conversation_history("thread-2")

    # List all checkpoints
    print("\nCheckpoints for Thread 1:")
    checkpoints = agent.list_checkpoints("thread-1")
    print(f"Found {len(checkpoints)} checkpoints")


if __name__ == "__main__":
    example_usage()
