from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

#os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

chat = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")

template = """
You are a SQL agent
Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [sql_db_query, sql_db_schema, sql_db_list_tables, sql_db_query_checker, query_help_tool]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: What is the total number of agents present
Thought: I can use query_help_tool to finding relevant columns and tables first. Then I should query the schema of the most relevant tables"""

system = "You are a helpful assistant."
human = "{text}"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

chain = prompt | chat
print(chain.invoke({"text": template}))