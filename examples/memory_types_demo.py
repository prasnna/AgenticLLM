#!/usr/bin/env python3
"""
Example script demonstrating different types of memory in AI agents using LangMem.

This script shows how to implement and use three types of memory:
1. Semantic Memory: Facts, knowledge, and concepts (what the agent knows)
2. Episodic Memory: Past experiences and events (what the agent has experienced)
3. Procedural Memory: How to perform tasks (how the agent should behave)

All memories are stored in a PostgreSQL database for persistence.
"""

import sys
import os
import time
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.env_utils import load_env_vars, get_env_var
from langchain_aws import ChatBedrockConverse
from langchain_community.chat_models import BedrockChat
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.prebuilt import create_react_agent
from langgraph.utils.config import get_store
from langmem import (
    create_search_memory_tool
)
from src.utils.memory_extraction import extract_multiple_memory_types
from psycopg_pool import ConnectionPool

# Define memory schemas
class SemanticMemory(BaseModel):
    """
    Semantic memory stores facts, knowledge, and concepts.
    This can include user preferences, general facts, and structured knowledge.
    """
    content: str = Field(..., description="The factual information or knowledge")
    category: str = Field(..., description="Category of the information (e.g., preference, fact, knowledge)")
    importance: int = Field(default=1, description="Importance level from 1-5, with 5 being most important")
    source: str = Field(default="conversation", description="Where this information came from")

class EpisodicMemory(BaseModel):
    """
    Episodic memory stores specific past experiences and events.
    This includes the context, thought process, action, and outcome.
    """
    observation: str = Field(..., description="The situation and relevant context")
    thoughts: str = Field(..., description="Key considerations and reasoning process")
    action: str = Field(..., description="What was done in response")
    result: str = Field(..., description="What happened and why it worked")
    timestamp: str = Field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"),
                          description="When this episode occurred")

class ProceduralMemory(BaseModel):
    """
    Procedural memory contains knowledge about how to perform tasks.
    This includes instructions, rules, and procedures.
    """
    task: str = Field(..., description="The task or situation this procedure applies to")
    procedure: str = Field(..., description="Step-by-step instructions on how to perform the task")
    context: str = Field(..., description="When and why to use this procedure")
    effectiveness: int = Field(default=3, description="How effective this procedure is (1-5)")

class MemoryAgent:
    """
    An agent with multiple types of memory capabilities using AWS Bedrock and LangMem.

    This agent demonstrates three types of memory:
    1. Semantic Memory: Facts, knowledge, and concepts
    2. Episodic Memory: Past experiences and events
    3. Procedural Memory: How to perform tasks

    All memories are stored in a PostgreSQL database for persistence.
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
        Initialize the MemoryAgent with multiple memory types.

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

        # Initialize memory store with embedding capabilities
        self.store = InMemoryStore(
            index={
                "dims": 1536,
                "embed": "openai:text-embedding-3-small",
            }
        )

        # Initialize Bedrock LLM
        self.llm = ChatBedrockConverse(
            provider="anthropic",
            model=model_id,
            credentials_profile_name=credentials_profile_name,
        )

        # # Create a BedrockChat instance for memory managers
        # bedrock_chat = BedrockChat(
        #     self.llm,
        #     credentials_profile_name=credentials_profile_name,
        #     model_kwargs={"temperature": 0.2}
        # )

        # # Initialize Bedrock Chat for memory extraction
        # self.bedrock_chat = BedrockChat(
        #     model_id=model_id,
        #     credentials_profile_name=credentials_profile_name,
        #     model_kwargs={"temperature": 0.2},
        #     model_provider="anthropic"
        # )

        self.bedrock_chat = self.llm

        # Define memory extraction instructions
        self.semantic_instructions = "Extract important facts, preferences, and knowledge from the conversation. Focus on extracting factual information that would be useful to remember about the user."
        self.episodic_instructions = "Extract noteworthy experiences and interactions, capturing the full context and outcome. Focus on specific events, their context, and results."
        self.procedural_instructions = "Extract procedures, methods, and techniques for handling specific tasks or situations. Focus on step-by-step guides and methodologies."

        # No prompt optimizer for procedural memory
        # We'll use a simpler approach for procedural memory

        # Create agent with memory capabilities
        self.agent = create_react_agent(
            self.llm,
            prompt=self._prompt_function,
            tools=[
                # Add memory search tools
                create_search_memory_tool(namespace=("semantic_memories",)),
                create_search_memory_tool(namespace=("episodic_memories",)),
                create_search_memory_tool(namespace=("procedural_memories",)),
            ],
            # Provide checkpointer for conversation history
            checkpointer=self.checkpointer,
            # Provide store for memories
            store=self.store
        )

        # Initialize system prompt
        self.system_prompt = """You are a helpful assistant with multiple types of memory:

1. Semantic Memory: Facts, knowledge, and concepts you've learned
2. Episodic Memory: Past experiences and interactions you've had
3. Procedural Memory: How to perform tasks and follow procedures

Use these memories to provide helpful, informed responses. When you learn something new or have a successful interaction, store it in the appropriate memory type.
"""

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
        semantic_memories = store.search(
            ("semantic_memories",),
            query=state["messages"][-1].content,
        )

        episodic_memories = store.search(
            ("episodic_memories",),
            query=state["messages"][-1].content,
        )

        procedural_memories = store.search(
            ("procedural_memories",),
            query=state["messages"][-1].content,
        )

        # Create system message with memories
        system_msg = f"""{self.system_prompt}

## Semantic Memories (Facts & Knowledge)
<semantic_memories>
{semantic_memories}
</semantic_memories>

## Episodic Memories (Past Experiences)
<episodic_memories>
{episodic_memories}
</episodic_memories>

## Procedural Memories (How to Perform Tasks)
<procedural_memories>
{procedural_memories}
</procedural_memories>

You can store important information using the manage_memory tools.
You can search for information using the search_memory tools.
When you learn something important, make sure to store it in the appropriate memory type.
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
        config = {"configurable": {"thread_id": thread_id}, "recursion_limit": 50}
        return self.agent.invoke({"messages": messages}, config=config)

    def stream(self, messages: List[Dict[str, str]], thread_id: str = "default"):
        """
        Stream the agent's response.

        Args:
            messages: A list of messages to send to the agent.
            thread_id: The ID of the conversation thread.

        Returns:
            A generator yielding chunks of the response.
        """
        config = {"configurable": {"thread_id": thread_id}, "recursion_limit": 50}
        return self.agent.stream({"messages": messages}, config=config)

    def update_memories(self, messages: List[Dict[str, str]]):
        """
        Update all memory types based on the conversation.

        Args:
            messages: A list of messages from the conversation.
        """
        # Extract all memory types using our custom extraction function
        extracted_memories = extract_multiple_memory_types(
            llm=self.bedrock_chat,
            messages=messages,
            schema_classes=[SemanticMemory, EpisodicMemory, ProceduralMemory],
            instructions="Extract important information from the conversation based on the memory type.",
        )

        # Process semantic memories
        semantic_memories = extracted_memories.get("SemanticMemory", [])
        print(f"Extracted {len(semantic_memories)} semantic memories")

        # Store semantic memories in the store
        for memory in semantic_memories:
            self.store.put(
                ("semantic_memories",),
                memory["id"],
                {"kind": "SemanticMemory", "content": memory}
            )

        # Process episodic memories
        episodic_memories = extracted_memories.get("EpisodicMemory", [])
        print(f"Extracted {len(episodic_memories)} episodic memories")

        # Store episodic memories in the store
        for memory in episodic_memories:
            self.store.put(
                ("episodic_memories",),
                memory["id"],
                {"kind": "EpisodicMemory", "content": memory}
            )

        # Process procedural memories
        procedural_memories = extracted_memories.get("ProceduralMemory", [])
        print(f"Extracted {len(procedural_memories)} procedural memories")

        # Store procedural memories in the store
        for memory in procedural_memories:
            self.store.put(
                ("procedural_memories",),
                memory["id"],
                {"kind": "ProceduralMemory", "content": memory}
            )

        return {
            "semantic": semantic_memories,
            "episodic": episodic_memories,
            "procedural": procedural_memories
        }

    # No system prompt update needed for this implementation

    def display_conversation_history(self, thread_id: str):
        """
        Display the conversation history for a thread.

        Args:
            thread_id: The ID of the conversation thread.
        """
        try:
            # Get the conversation history from the checkpointer
            config = {"configurable": {"thread_id": thread_id}}
            checkpoint = self.checkpointer.get(config)

            if not checkpoint:
                print(f"No conversation history found for thread {thread_id}")
                return

            messages = checkpoint.get("channel_values", {}).get("messages", [])

            print(f"\nConversation History (Thread: {thread_id}):")
            for i, message in enumerate(messages):
                role = message.type if hasattr(message, "type") else message.__class__.__name__.replace("Message", "").lower()
                content = message.content if hasattr(message, "content") else str(message)
                print(f"{i+1}. {role.upper()}: {content[:100]}{'...' if len(content) > 100 else ''}")

        except Exception as e:
            print(f"Error retrieving conversation history: {str(e)}")

    def list_checkpoints(self, thread_id: str):
        """
        List all checkpoints for a thread.

        Args:
            thread_id: The ID of the conversation thread.

        Returns:
            A list of checkpoint versions.
        """
        try:
            # Get all versions for the thread
            config = {"configurable": {"thread_id": thread_id}}
            checkpoints = list(self.checkpointer.list(config))
            return checkpoints
        except Exception as e:
            print(f"Error listing checkpoints: {str(e)}")
            return []

def main():
    """Run the memory types demonstration."""
    # Load environment variables from .env file
    load_env_vars()

    print("Checking PostgreSQL environment variables...")
    required_vars = ["PG_HOST", "PG_DB", "PG_USER", "PG_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]

    if missing_vars:
        print(f"ERROR: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your .env file before running this example.")
        return

    print("Initializing Memory Agent with multiple memory types...")
    # Initialize the agent with PostgreSQL storage
    agent = MemoryAgent(
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

    # Demonstrate semantic memory
    print("\n--- Demonstrating Semantic Memory ---")
    user_input = "My name is Alex and I work as a data scientist. I prefer dark mode in all applications and I'm allergic to peanuts."
    print(f"User: {user_input}")

    response = agent.invoke(
        [{"role": "user", "content": user_input}],
        thread_id="memory-demo-1"
    )
    print(f"Agent: {response['messages'][-1].content}")

    # Update memories based on the conversation
    agent.update_memories([
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": response['messages'][-1].content}
    ])

    # Demonstrate episodic memory
    print("\n--- Demonstrating Episodic Memory ---")
    user_input = "I'm struggling to explain gradient descent to my team. Can you help me come up with a good analogy?"
    print(f"User: {user_input}")

    response = agent.invoke(
        [{"role": "user", "content": user_input}],
        thread_id="memory-demo-1"
    )
    print(f"Agent: {response['messages'][-1].content}")

    # User provides feedback on the analogy
    user_input = "That hiking analogy was perfect! My team really understood it. Thanks!"
    print(f"User: {user_input}")

    response = agent.invoke(
        [{"role": "user", "content": user_input}],
        thread_id="memory-demo-1"
    )
    print(f"Agent: {response['messages'][-1].content}")

    # Update memories based on the conversation
    agent.update_memories([
        {"role": "user", "content": "I'm struggling to explain gradient descent to my team. Can you help me come up with a good analogy?"},
        {"role": "assistant", "content": response['messages'][-2].content},
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": response['messages'][-1].content}
    ])

    # Demonstrate procedural memory
    print("\n--- Demonstrating Procedural Memory ---")
    user_input = "What's the best way to prepare for a data science interview?"
    print(f"User: {user_input}")

    response = agent.invoke(
        [{"role": "user", "content": user_input}],
        thread_id="memory-demo-1"
    )
    print(f"Agent: {response['messages'][-1].content}")

    # Update memories based on the conversation
    agent.update_memories([
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": response['messages'][-1].content}
    ])

    # Test memory recall across all types
    print("\n--- Testing Memory Recall ---")
    user_input = "Can you remind me about my food allergies and also give me another example for explaining machine learning concepts to non-technical people?"
    print(f"User: {user_input}")

    response = agent.invoke(
        [{"role": "user", "content": user_input}],
        thread_id="memory-demo-1"
    )
    print(f"Agent: {response['messages'][-1].content}")

    # Start a new thread to test memory persistence across threads
    print("\n--- Testing Memory Persistence Across Threads ---")
    user_input = "Do you remember who I am and what I do for work?"
    print(f"User: {user_input}")

    response = agent.invoke(
        [{"role": "user", "content": user_input}],
        thread_id="memory-demo-2"
    )
    print(f"Agent: {response['messages'][-1].content}")

    # Display conversation history
    agent.display_conversation_history("memory-demo-1")
    agent.display_conversation_history("memory-demo-2")

    # List all checkpoints
    print("\n--- Checkpoints ---")
    checkpoints = agent.list_checkpoints("memory-demo-1")
    print(f"Found {len(checkpoints)} checkpoints for thread memory-demo-1")

    print("\nExample completed.")

if __name__ == "__main__":
    main()
