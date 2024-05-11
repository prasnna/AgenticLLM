from langchain_community.llms import OpenAI,Bedrock
from langchain_community.utilities import SQLDatabase
#from langchain_experimental.sql import SQLDatabaseChain
from  dotenv import load_dotenv
from langchain_community.agent_toolkits import SQLDatabaseToolkit
import os
from config import *
from templates import *
from langchain.agents import create_sql_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from query_tool_v1 import query_help_tool_v1
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

# Set OpenAI API key as an environment variable
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = langchain_key



db = SQLDatabase.from_uri(f"mssql+pyodbc://{url}?driver=SQL+Server+Native+Client+10.0")

#model = ChatOpenAI(temperature=0)

model = Bedrock(
    credentials_profile_name="saml", model_id="anthropic.claude-v2",
    model_kwargs={"temperature": 0}
)

toolkit = SQLDatabaseToolkit(db=db,llm= model)
tools = toolkit.get_tools()

agent_executor = create_sql_agent(
    llm=model,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    extra_tools= [query_help_tool_v1],
    prompt= PromptTemplate.from_template(sql_agent_chat_template_v2),
    top_k=2
)



#agent_executor.invoke(input = "prompt")
