from langchain_community.llms import OpenAI
from langchain_community.utilities import SQLDatabase
#from langchain_experimental.sql import SQLDatabaseChain
from  dotenv import load_dotenv
from langchain_community.agent_toolkits import SQLDatabaseToolkit
import os
from config import *
from langchain.agents import create_sql_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from scripts.SQLKnowledgeBaseTool import query_help_tool_v1
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

# # check the local ODBC driver and make sure it match with the traget database instance
# import pyodbc
# for driver in pyodbc.drivers():
#     print(driver)

# Set OpenAI API key as an environment variable
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = langchain_key



db = SQLDatabase.from_uri(f"mssql+pyodbc://{url}?driver=SQL+Server+Native+Client+10.0")

model = ChatOpenAI(temperature=0)

toolkit = SQLDatabaseToolkit(db=db,llm= model)
tools = toolkit.get_tools()


# Step 3. Define Prefix

template = """ You are an SQL agent but DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database. If the question does not seem related to the database, just return "I don't know" as the answer. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: I can use  query_help_tool to finding relevant columns and tables first.  Then I should query the schema of the most relevant tables.
{agent_scratchpad}"""


agent_executor = create_sql_agent(
    llm=model,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    extra_tools= [query_help_tool_v1],
    prompt= PromptTemplate.from_template(template),
    top_k=2
)


agent_executor.invoke(input = "prompt")