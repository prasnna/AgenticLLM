from langchain import OpenAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from  dotenv import load_dotenv
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
import os
from config import *
from langchain.agents import create_sql_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType

# # check the local ODBC driver and make sure it match with the traget database instance
# import pyodbc
# for driver in pyodbc.drivers():
#     print(driver)

# Set OpenAI API key as an environment variable
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY



db = SQLDatabase.from_uri(f"mssql+pyodbc://{url}?driver=SQL+Server+Native+Client+10.0")

toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0))

agent_executor = create_sql_agent(
    llm=ChatOpenAI(temperature=0),
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)


agent_executor.run("user prompt")