"""
This script demonstrates how to create an SQL agent using Langchain and various language models.
It connects to a SQL Server database and allows you to interact with the agent to perform SQL-related tasks.
"""

# Import necessary libraries
from langchain_community.llms import OpenAI, Bedrock
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
from langchain_community.agent_toolkits import SQLDatabaseToolkit
import os
from langchain.agents import create_sql_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from SQLKnowledgeBaseTool import query_help_tool
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
from templates import sql_agent_chat_template_v2

# Load environment variables from .env file
load_dotenv()

# Set environment variables for OpenAI API key, Langchain tracing, and Langchain endpoint
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Initialize SQL database connection
DB_URL = os.getenv("DB_URL")
db = SQLDatabase.from_uri(DB_URL)

# Initialize language model (either OpenAI or Anthropic's Bedrock)
# model = ChatOpenAI(temperature=0)
model = Bedrock(
    credentials_profile_name="saml",
    model_id="anthropic.claude-v2",
    model_kwargs={"temperature": 0},
)

# Create SQL toolkit with the database and language model
toolkit = SQLDatabaseToolkit(db=db,llm=model)
tools = toolkit.get_tools()

# Create SQL agent with the language model, toolkit, and additional tools/prompt
agent_executor = create_sql_agent(
    llm=model,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    extra_tools=[query_help_tool],
    prompt=PromptTemplate.from_template(sql_agent_chat_template_v2),
    top_k=2,
)

# Example usage: Invoke the agent with a prompt
prompt = "What is the total number of orders placed in the year 2022?"
result = agent_executor.invoke(input=prompt)
print(result)