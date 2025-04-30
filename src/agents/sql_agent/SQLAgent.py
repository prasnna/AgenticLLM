"""
This script demonstrates how to create an SQL agent using Langchain and various language models.
It connects to a SQL Server database and allows you to interact with the agent to perform SQL-related tasks.
"""

# Import necessary libraries
from langchain_community.llms import OpenAI, Bedrock, Ollama
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
import os
from langchain.agents import create_sql_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
import ast
from src.utils.env_utils import load_env_vars, get_env_var

from langchain.agents.agent_toolkits.sql.prompt import (
    SQL_FUNCTIONS_SUFFIX,
    SQL_PREFIX,
    SQL_SUFFIX,
)
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.prompts import PromptTemplate
from src.agents.sql_agent.prompts import sql_agent_chat_template_v2, sql_agent_chat_template_v3
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_env_vars()

# Set environment variables for OpenAI API key, Langchain tracing, and Langchain endpoint
os.environ["OPENAI_API_KEY"] = get_env_var("OPENAI_API_KEY", "")
os.environ["LANGCHAIN_TRACING_V2"] = get_env_var("LANGCHAIN_TRACING_V2", "true")
os.environ["LANGCHAIN_ENDPOINT"] = get_env_var("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
os.environ["LANGCHAIN_API_KEY"] = get_env_var("LANGCHAIN_API_KEY", "")

# Initialize SQL database connection
db_url = get_env_var("DB_URL")
if not db_url:
    url = get_env_var("URL")
    db_url = f"mssql+pyodbc://{url}?driver=SQL+Server+Native+Client+10.0"

db = SQLDatabase.from_uri(db_url)

# Initialize language model (either OpenAI or Anthropic's Bedrock)
# model = ChatOpenAI(temperature=0)
# model = Bedrock(
#     credentials_profile_name="saml",
#     model_id="anthropic.claude-v2",
#     model_kwargs={"temperature": 0},
# )

#local model
#model = Ollama(model="phi3",temperature=0) #phi3 #llama3 #vicuna

#groq
model = ChatGroq(temperature=0, model_name="llama3-70b-8192")

#gemini
#model = ChatGoogleGenerativeAI(model="gemini-pro")


# Create SQL toolkit with the database and language model
toolkit = SQLDatabaseToolkit(db=db,llm=model)
tools = toolkit.get_tools()

#stub an extra tool

from langchain.tools import tool


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@tool
def query_help_tool(query: str) -> str:
    """Use this tool to get relevant SQL scripts based on your input query."""
    sql_dir_path = get_env_var("SQL_DIR_PATH", "data/sql_scripts")
    sql_file = get_env_var("SQL_LIST_MINI", "meta_data.sql")
    return read_file(f"{sql_dir_path}/{sql_file}")

@tool
def sql_db_list_columns(query: str) -> str:
    """Use this tool to get relevant table names, Input to this script can be a key word from users input."""
    try:
        # Get the column names
        query = f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE COLUMN_NAME LIKE '%{query}%'"
        result = db.run(query, fetch='all', include_columns=True)
        print(type(result))
        if result:
            # Remove the leading and trailing '[' and ']' characters
           cleaned_string = result.lstrip('[').rstrip(']')

           # Convert the string to a list of dictionaries
           list_of_dicts = [ast.literal_eval(item) for item in cleaned_string.split(', ')]
           table_names = [table['TABLE_NAME'] for table in list_of_dicts]
           return  ', '.join(table_names)

        else:
            return f"No tables found with columns matching '{query}'."

    except Exception as e:
        return f"Error: {e}"

#Create SQL agent with the language model, toolkit, and additional tools/prompt
agent_executor = create_sql_agent(
    llm=model,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    extra_tools=[query_help_tool,sql_db_list_columns],
    prompt=PromptTemplate.from_template(sql_agent_chat_template_v2),
    top_k=2
)

# Example usage: Invoke the agent with a prompt
#prompt = "where is the product ID configured"
prompt = "prompt"
result = agent_executor.invoke(input=prompt, handle_parsing_errors=True)
print(result)

#print(sql_db_list_columns('product'))