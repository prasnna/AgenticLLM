# PostgreSQL Memory Agent

This module implements an agent with memory capabilities using AWS Bedrock as the base LLM and LangMem for memory management with PostgreSQL for persistent storage.

## Overview

The PostgreSQL Memory Agent can:
- Store important information about users in a PostgreSQL database for long-term persistence
- Retrieve relevant memories during conversations
- Maintain context across multiple conversation threads
- Use AWS Bedrock's powerful language models for natural interactions

## Requirements

- AWS account with Bedrock access
- Appropriate AWS credentials configured
- PostgreSQL database (Aurora PostgreSQL recommended)
- Python packages:
  - `langchain-aws`
  - `langmem`
  - `langgraph`
  - `psycopg2-binary`

## PostgreSQL Setup

The agent uses a PostgreSQL database for persistent storage. You need to configure the connection details through environment variables in your `.env` file:

```
# PostgreSQL for agent memory
PG_HOST = "your-postgres-host"
PG_DB = "your-database-name"
PG_USER = "your-username"
PG_PASSWORD = "your-password"
PG_PORT = "5432"
```

These environment variables are required:

- `PG_HOST`: PostgreSQL host
- `PG_DB`: PostgreSQL database name
- `PG_USER`: PostgreSQL username
- `PG_PASSWORD`: PostgreSQL password
- `PG_PORT`: PostgreSQL port (default: "5432")

## Usage

### Basic Usage

```python
from src.agents.memory_agent import PostgresMemoryAgent

# Initialize the agent
agent = PostgresMemoryAgent()

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

You can configure the agent with different models and PostgreSQL settings:

```python
agent = PostgresMemoryAgent(
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    credentials_profile_name="my-aws-profile",
    embedding_model="openai:text-embedding-3-small",
    embedding_dims=1536,
    pg_host="my-postgres-host",
    pg_db="my-database",
    pg_user="my-username",
    pg_password="my-password",
    pg_port="5432"
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

### Accessing Memories

You can access and display the memories stored in the PostgreSQL database:

```python
# Get all memories
memories = agent.get_memories()

# Get memories related to a specific topic
preferences = agent.get_memories(query="preferences")

# Display all memories in a readable format
agent.display_memories()
```

## Memory Management

The agent automatically manages memories using LangMem's tools:

- `manage_memory_tool`: Allows the agent to create, update, and delete memories
- `search_memory_tool`: Allows the agent to search for relevant memories

Memories are stored in a PostgreSQL database and retrieved based on semantic similarity to the current conversation.

## Environment Variables

The agent uses the following environment variables:

- `MODEL_ID`: The Bedrock model ID to use (default: "anthropic.claude-3-sonnet-20240229-v1:0")
- `BED_ROCK_AWS_PROFILE`: AWS credentials profile name (default: "saml")
- `PG_HOST`: PostgreSQL host
- `PG_DB`: PostgreSQL database name
- `PG_USER`: PostgreSQL username
- `PG_PASSWORD`: PostgreSQL password
- `PG_PORT`: PostgreSQL port

## Implementation Details

The agent is built using:

- LangGraph's `create_react_agent` for the agent framework
- LangMem for memory management
- AWS Bedrock for the language model
- PostgresSaver for storing conversation history in PostgreSQL

Note: In LangGraph 0.4.0 and later, the PostgreSQL integration has moved from `langgraph.store.postgres` to `langgraph.checkpoint.postgres`.

## Advantages of PostgreSQL Storage

Using PostgreSQL for memory storage offers several advantages over in-memory storage:

1. **Persistence**: Memories persist across application restarts
2. **Scalability**: PostgreSQL can handle large amounts of memory data
3. **Concurrency**: Multiple agents can access the same memory store
4. **Backup and Recovery**: Standard database backup procedures can be used
5. **Query Capabilities**: Advanced querying of memories is possible
