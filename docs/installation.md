# Installation Guide

This guide will help you set up the AgenticLLM project on your local machine.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/agenticllm.git
cd agenticllm
```

## Step 2: Create a Virtual Environment

It's recommended to use a virtual environment to avoid conflicts with other Python packages.

### On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### On macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

Install the package in development mode:

```bash
pip install -e .
```

This will install all the required dependencies listed in the `setup.py` file.

## Step 4: Configure Environment Variables

Create a `.env` file in the root directory of the project with the following content:

```
# Database connections
URL=your_database_username:your_database_password@your_database_host/your_database_name
DB_URL=mssql+pyodbc://${URL}?driver=SQL+Server+Native+Client+10.0

# SQL files
SQL_LIST_MINI=meta_data.sql
SQL_DIR_PATH=data/sql_scripts

# API Keys
OPENAI_API_KEY=your_openai_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
GROQ_API_KEY=your_groq_api_key

# AWS
BED_ROCK_AWS_PROFILE=your_aws_profile

# LangChain settings
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

Replace the placeholders with your actual API keys, database connection strings, and other configuration values.

## Step 5: Verify Installation

Run a simple test to verify that the installation was successful:

```bash
python -c "from src.agents.sql_agent.conversewithSQL import agent_executor; print('Installation successful!')"
```

If you see "Installation successful!" without any errors, the installation was successful.

## Troubleshooting

If you encounter any issues during installation, please check the following:

1. Make sure you have the correct Python version (3.8 or higher)
2. Make sure all the required dependencies are installed
3. Make sure the environment variables are set correctly
4. Check the logs for any error messages

If you still have issues, please open an issue on the GitHub repository.
