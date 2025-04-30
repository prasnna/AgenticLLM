#!/usr/bin/env python3
"""
Bedrock Memory Agent: An agent with memory capabilities using AWS Bedrock and LangMem

This module implements an agent with memory capabilities using AWS Bedrock as the
base LLM and LangMem for memory management. The agent can store and retrieve
information across conversations.
"""

from typing import Dict, List, Any, Optional
from langchain_aws import ChatBedrockConverse
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langgraph.utils.config import get_store
from langmem import create_manage_memory_tool, create_search_memory_tool
from src.utils.env_utils import get_env_var


class BedrockMemoryAgent:
    """
    An agent with memory capabilities using AWS Bedrock and LangMem.

    This agent can store and retrieve information across conversations using
    LangMem's memory management tools and AWS Bedrock as the base LLM.
    """

    def __init__(
        self,
        model_id: Optional[str] = None,
        credentials_profile_name: Optional[str] = None,
        embedding_model: str = "openai:text-embedding-3-small",
        embedding_dims: int = 1536,
    ):
        """
        Initialize the BedrockMemoryAgent.

        Args:
            model_id: The Bedrock model ID to use. If None, will use the MODEL_ID from environment.
            credentials_profile_name: AWS credentials profile name. If None, will use default credentials.
            embedding_model: The embedding model to use for memory storage.
            embedding_dims: The dimensions of the embedding vectors.
        """
        # Get model ID from environment if not provided
        if model_id is None:
            model_id = get_env_var("MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")

        # Get AWS profile from environment if not provided
        if credentials_profile_name is None:
            credentials_profile_name = get_env_var("BED_ROCK_AWS_PROFILE", "saml")

        # Initialize memory store
        self.store = InMemoryStore(
            index={
                "dims": embedding_dims,
                "embed": embedding_model,
            }
        )

        # Initialize Bedrock LLM
        self.llm = ChatBedrockConverse(
            provider="anthropic",
            model_id=model_id,
            credentials_profile_name=credentials_profile_name,
        )

        # Create checkpointer for conversation history
        self.checkpointer = MemorySaver()

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
            # Provide store for memories
            store=self.store,
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
        memories = store.search(
            ("memories",),
            query=state["messages"][-1].content,
        )

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


# Example usage
def example_usage():
    """Example usage of the BedrockMemoryAgent."""
    # Initialize the agent
    agent = BedrockMemoryAgent()

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


if __name__ == "__main__":
    example_usage()
