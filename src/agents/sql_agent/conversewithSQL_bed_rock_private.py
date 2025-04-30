from langchain_aws import ChatBedrock
from langchain_community.utilities import SQLDatabase
#from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.agent_toolkits import SQLDatabaseToolkit
import os
from src.agents.sql_agent.prompts import sql_agent_chat_template_v2
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
#from src.agents.sql_agent.SQLKnowledgeBaseTool import query_help_tool as query_help_tool_v1
from src.utils.env_utils import load_env_vars, get_env_var
from langchain_community.agent_toolkits.sql.prompt import (
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

# Load environment variables
load_env_vars()

# Set OpenAI API key as an environment variable
os.environ["OPENAI_API_KEY"] = get_env_var("OPENAI_API_KEY")
#os.environ['LANGCHAIN_TRACING_V2'] = get_env_var("LANGCHAIN_TRACING_V2", "true")
#os.environ['LANGCHAIN_ENDPOINT'] = get_env_var("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
#os.environ['LANGCHAIN_API_KEY'] = get_env_var("LANGCHAIN_API_KEY")

# Get database URL from environment variables
db_url = get_env_var("DB_URL")
if not db_url:
    url = get_env_var("URL")
    db_url = f"mssql+pyodbc://{url}?driver=SQL+Server+Native+Client+10.0"

db = SQLDatabase.from_uri(db_url)

#model = ChatOpenAI(temperature=0)

model = ChatBedrock(
    credentials_profile_name=get_env_var("BED_ROCK_AWS_PROFILE", "saml"),
    provider="anthropic",
    model_id=get_env_var("MODEL_ID"),
    model_kwargs={"temperature": 0}
)

toolkit = SQLDatabaseToolkit(db=db,llm= model)
tools = toolkit.get_tools()

agent_executor = create_sql_agent(
    llm=model,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    #extra_tools= [query_help_tool_v1],
    prompt= PromptTemplate.from_template(sql_agent_chat_template_v2),
    top_k=2
)

#agent_executor.invoke(input = "find all the ")

#agent_executor.invoke(input = "find how many agents are there with an email address of donotsend@prac.com")

# more context, this RAG can be done enhancing meta data where it holds relations like one to one, one to many etc...by Reveiw Agent/Feed back Agent

#agent_executor.invoke(input = "find count of agent level code with at least one contact having email donotsend@prac.com")

# no context try

#agent_executor.invoke(input = "find  agent details with contracts in the state of MA and lob  Personal Auto")



#agent_executor.invoke(input = "query to find all distinct  states from address for agent with level code 'CW02', output can be 'level code', list of comma separated states eg) ABC,[NJ,NY,..etc]",handle_parsing_errors=True)

#agent_executor.invoke(input = "query to find the  top 2 'agents' in the 'NJ' 'state', output should include distinct level code,address,email")

#agent_executor.invoke(input = "query to find the  top 2 'agents' in the 'NJ' 'state', output should include distinct level code,address,email")

#agent_executor.invoke(input = "query to find the number of 'agents' in the 'NY' 'state'")

#agent_executor.invoke(input = "only create a query to soft delete agent with the following level code: 'A0D9459'")

#agent_executor.invoke(input = "only create a query to delete the following level code: 'A0D9459'  by updating deleted flag to 'D' and level code to 'D-A0D9459'")

#agent_executor.invoke(input = "query to find 'Channel Code' of  agent with level code CW02")

#agent_executor.invoke(input = "query to find count of distinct level code of agents where there is at least one contact with email donotsend@prac.com")

#agent_executor.invoke(input = "find how many agents are there with an email address of donotsend@prac.com , output should be just a query grouped by agent (first name + last name),count")

#agent_executor.invoke(input = "query to find number of agents where there is at least one contact with email donotsend@prac.com")

#handle_parsing_errors=True