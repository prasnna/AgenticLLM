# AgenticLLM

A project for implementing and learning about agentic flows with Large Language Models (LLMs).

## Project Overview

This repository contains various implementations of agentic LLM systems, including:

- **SQL Agent**: Text-to-SQL implementation using the LangChain framework
- **Research Agent**: Agent for conducting research tasks
- **Coding Agent**: Agent for assisting with coding tasks
- **CSV Agent**: Agent for working with CSV data

## Project Structure

```
agenticllm/
├── data/                  # Data files and resources
│   ├── embedded_data/     # Embedded data files
│   └── sql_scripts/       # SQL scripts for the SQL agent
├── docs/                  # Documentation
├── notebooks/             # Jupyter notebooks
├── src/                   # Source code
│   ├── agents/            # Agent implementations
│   │   ├── coding_agent/  # Coding agent
│   │   ├── csv_agent/     # CSV agent
│   │   ├── research_agent/# Research agent
│   │   └── sql_agent/     # SQL agent
│   ├── config/            # Configuration files
│   ├── models/            # Model implementations
│   └── utils/             # Utility functions
└── tests/                 # Test files
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/agenticllm.git
   cd agenticllm
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package in development mode:
   ```
   pip install -e .
   ```

## Usage

### SQL Agent

The SQL Agent allows you to query databases using natural language:

```python
from src.agents.sql_agent.conversewithSQL import agent_executor

result = agent_executor.invoke(input="What are the top 5 agents by sales?")
print(result)
```

## Screenshots

![SQL Agent Demo](docs/images/image.png)
![Agent Interaction](docs/images/image-1.png)
![Results Visualization](docs/images/image-2.png)

## License

This project is licensed under the terms of the license included in the repository.
