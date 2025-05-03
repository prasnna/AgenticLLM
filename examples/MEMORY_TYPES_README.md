# Memory Types in AI Agents

This example demonstrates the implementation of different types of memory in AI agents using LangMem and PostgreSQL for persistent storage.

## Overview

AI agents can benefit from different types of memory, each serving distinct functions. This example implements three primary memory types:

### 1. Semantic Memory

Semantic memory stores facts, knowledge, and concepts. This is what most people think of as "memory" - the ability to recall information.

**Implementation:**
- Stores facts, preferences, and knowledge as structured data
- Categorizes information by importance and type
- Enables the agent to remember user preferences, facts, and general knowledge

**Example:**
```python
class SemanticMemory(BaseModel):
    content: str = Field(..., description="The factual information or knowledge")
    category: str = Field(..., description="Category of the information (e.g., preference, fact, knowledge)")
    importance: int = Field(default=1, description="Importance level from 1-5, with 5 being most important")
    source: str = Field(default="conversation", description="Where this information came from")
```

### 2. Episodic Memory

Episodic memory stores specific past experiences and events. This allows the agent to learn from past interactions and apply that learning to new situations.

**Implementation:**
- Captures the full context of an interaction
- Records the thought process, actions taken, and outcomes
- Enables the agent to recall successful approaches and adapt them to new situations

**Example:**
```python
class EpisodicMemory(BaseModel):
    observation: str = Field(..., description="The situation and relevant context")
    thoughts: str = Field(..., description="Key considerations and reasoning process")
    action: str = Field(..., description="What was done in response")
    result: str = Field(..., description="What happened and why it worked")
    timestamp: str = Field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"), 
                          description="When this episode occurred")
```

### 3. Procedural Memory

Procedural memory contains knowledge about how to perform tasks. This is the "how-to" memory that guides the agent's behavior and responses.

**Implementation:**
- Stores procedures, methods, and techniques for specific tasks
- Includes context for when to apply each procedure
- Enables the agent to follow consistent processes and improve them over time

**Example:**
```python
class ProceduralMemory(BaseModel):
    task: str = Field(..., description="The task or situation this procedure applies to")
    procedure: str = Field(..., description="Step-by-step instructions on how to perform the task")
    context: str = Field(..., description="When and why to use this procedure")
    effectiveness: int = Field(default=3, description="How effective this procedure is (1-5)")
```

## How It Works

1. **Memory Extraction**: The agent analyzes conversations to extract different types of memories
2. **Memory Storage**: Memories are stored in a PostgreSQL database for persistence
3. **Memory Retrieval**: When responding to a user, the agent retrieves relevant memories of all types
4. **Memory Application**: The agent uses these memories to provide more informed, personalized responses
5. **Memory Optimization**: The agent's procedural memory (system prompt) is optimized based on interactions

## Benefits of Multiple Memory Types

- **Personalization**: Semantic memory allows the agent to remember user preferences and details
- **Learning from Experience**: Episodic memory enables the agent to improve based on past interactions
- **Consistent Behavior**: Procedural memory ensures the agent follows effective processes
- **Persistence**: All memories are stored in PostgreSQL, allowing them to persist across sessions

## Requirements

- PostgreSQL database (Aurora PostgreSQL recommended)
- AWS account with Bedrock access
- Python packages:
  - `langchain-aws`
  - `langmem`
  - `langgraph`
  - `psycopg2-binary`

## Configuration

Configure the PostgreSQL connection in your `.env` file:

```
# PostgreSQL for agent memory
PG_HOST = "your-postgres-host"
PG_DB = "your-database-name"
PG_USER = "your-username"
PG_PASSWORD = "your-password"
PG_PORT = "5432"
```

## Usage

Run the example:

```bash
python examples/memory_types_demo.py
```

The example demonstrates:
1. Storing and retrieving semantic memories (facts about the user)
2. Creating and using episodic memories (successful explanations)
3. Developing procedural memories (how to perform tasks)
4. Testing memory persistence across conversation threads

## Extending the Example

You can extend this example by:
- Adding more memory types or subtypes
- Implementing memory consolidation (merging similar memories)
- Adding memory decay (reducing importance of old memories)
- Implementing memory reflection (analyzing memories to extract higher-level patterns)
