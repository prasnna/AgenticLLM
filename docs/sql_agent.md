# SQL Agent Documentation

The SQL Agent is a component of the AgenticLLM project that allows users to interact with databases using natural language.

## Architecture

The SQL Agent consists of the following components:

1. **conversewithSQL.py**: The main entry point for the SQL Agent. It sets up the agent and handles the interaction with the user.
2. **SQLKnowledgeBaseTool.py**: A custom tool that provides SQL knowledge to the agent.
3. **prompts.py**: Contains the prompts used by the agent.
4. **sql_formatting/**: Contains utilities for formatting SQL queries.

## Configuration

The SQL Agent requires the following configuration in the `.env` file:

1. **Database Connection**: The agent needs to connect to a database. This is configured using the `URL` or `DB_URL` environment variables.
2. **OpenAI API Key**: The agent uses OpenAI's API for natural language processing. The API key is set using the `OPENAI_API_KEY` environment variable.
3. **SQL Scripts**: The agent uses SQL scripts as a knowledge base. These are stored in the `data/sql_scripts` directory, configured using the `SQL_DIR_PATH` environment variable.
4. **LangChain Settings**: The agent uses LangChain for orchestration. The API key is set using the `LANGCHAIN_API_KEY` environment variable.

## Usage

```python
from src.agents.sql_agent.conversewithSQL import agent_executor

# Ask a question in natural language
result = agent_executor.invoke(input="What are the top 5 agents by sales?")
print(result)
```

## Example Queries

- "What are the top 5 agents by sales?"
- "Show me the contracts that expire next month"
- "How many agents are in each state?"
- "What is the average contract value by line of business?"

## Limitations

- The agent cannot perform DML operations (INSERT, UPDATE, DELETE, DROP, etc.)
- The agent may not understand complex queries or domain-specific terminology
- The agent's performance depends on the quality of the SQL knowledge base
