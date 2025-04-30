# SQL Agent

This directory contains a SQL agent that can interact with a database using natural language queries.

## Setup

1. Make sure you have the required environment variables set in your `.env` file:
   - `DB_URL` or `URL`: The database connection URL
   - `BED_ROCK_AWS_PROFILE`: AWS profile for Bedrock (default: 'saml')
   - `OPENAI_API_KEY`: OpenAI API key
   - `SQL_DIR_PATH`: Directory path containing SQL files (default: 'data/sql_scripts')
   - `SQL_LIST_MINI`: Comma-separated list of SQL files to include (optional)

2. Install the required packages:
   ```
   pip install langchain-huggingface
   ```

## Running the SQL Agent

Use the wrapper script to run the SQL agent:

```
python run_sql_agent.py [query]
```

If a query is provided as a command-line argument, it will be used as input to the SQL agent. Otherwise, the default query from the script will be used.

### Example Queries

Here are some example queries you can try:

- `find how many agents are there with an email address of donotsend@prac.com`
- `find count of agent level code with at least one contact having email donotsend@prac.com`
- `find agent details with contracts in the state of MA and lob Personal Auto`
- `query to find all distinct states from address for agent with level code 'CW02'`
- `query to find the top 2 'agents' in the 'NJ' 'state'`

## Troubleshooting

If you encounter a `ModuleNotFoundError: No module named 'src'` error, it means Python can't find the 'src' module. The wrapper script fixes this by adding the project root to the Python path.

If you see LangChain deprecation warnings, you can ignore them or update the imports as suggested in the warnings.

If the script hangs or takes too long to run, it might be due to database connection issues. Press Ctrl+C to cancel the operation.

## Files

- `run_sql_agent.py`: Wrapper script to run the SQL agent
- `src/agents/sql_agent/conversewithSQL_bed_rock_private.py`: Main SQL agent script
- `src/agents/sql_agent/SQLKnowledgeBaseTool.py`: Custom tool to retrieve relevant SQL scripts
- `src/agents/sql_agent/prompts.py`: Prompt templates for the SQL agent
- `src/utils/env_utils.py`: Utility functions for handling environment variables
