# Bedrock Memory Agent

This module implements an agent with memory capabilities using AWS Bedrock as the base LLM and LangMem for memory management.

## Overview

The Bedrock Memory Agent can:
- Store important information about users in long-term memory
- Retrieve relevant memories during conversations
- Maintain context across multiple conversation threads
- Use AWS Bedrock's powerful language models for natural interactions

## Requirements

- AWS account with Bedrock access
- Appropriate AWS credentials configured
- Python packages:
  - `langchain-aws`
  - `langmem`
  - `langgraph`

## Usage

### Basic Usage

```python
from src.agents.memory_agent import BedrockMemoryAgent

# Initialize the agent
agent = BedrockMemoryAgent()

# Have a conversation
response = agent.invoke(
    [{"role": "user", "content": "My name is John and I prefer dark mode."}],
    thread_id="user-123"
)
print(response["messages"][-1].content)

# Continue the conversation
response = agent.invoke(
    [{"role": "user", "content": "What's my name?"}],
    thread_id="user-123"
)
print(response["messages"][-1].content)
```

### Configuration

You can configure the agent with different models and settings:

```python
agent = BedrockMemoryAgent(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    credentials_profile_name="my-aws-profile",
    embedding_model="openai:text-embedding-3-small",
    embedding_dims=1536
)
```

### Streaming Responses

For streaming responses:

```python
for chunk in agent.stream(
    [{"role": "user", "content": "Tell me about yourself."}],
    thread_id="user-123"
):
    print(chunk.text(), end="")
```

## Memory Management

The agent automatically manages memories using LangMem's tools:

- `manage_memory_tool`: Allows the agent to create, update, and delete memories
- `search_memory_tool`: Allows the agent to search for relevant memories

Memories are stored in a vector database and retrieved based on semantic similarity to the current conversation.

## Environment Variables

The agent uses the following environment variables:

- `MODEL_ID`: The Bedrock model ID to use (default: "anthropic.claude-3-sonnet-20240229-v1:0")
- `BED_ROCK_AWS_PROFILE`: AWS credentials profile name (default: "saml")

## Implementation Details

The agent is built using:

- LangGraph's `create_react_agent` for the agent framework
- LangMem for memory management
- AWS Bedrock for the language model
- InMemoryStore for storing memories (can be replaced with a persistent store in production)
