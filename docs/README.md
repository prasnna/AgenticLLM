# AgenticLLM Documentation

This directory contains documentation for the AgenticLLM project.

## Contents

- [Project Overview](../README.md)
- [SQL Agent](sql_agent.md)
- [Installation Guide](installation.md)
- [Usage Examples](usage_examples.md)

## SQL Agent

The SQL Agent allows you to query databases using natural language. It uses LangChain and OpenAI to translate natural language queries into SQL and execute them against a database.

### Features

- Natural language to SQL translation
- Database schema exploration
- Query execution and result formatting
- Knowledge base integration for SQL help

### Usage

```python
from src.agents.sql_agent.conversewithSQL import agent_executor

result = agent_executor.invoke(input="What are the top 5 agents by sales?")
print(result)
```

## Future Documentation

Additional documentation will be added as the project evolves.
