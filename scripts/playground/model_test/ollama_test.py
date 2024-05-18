from langchain_community.llms import Ollama

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

llm = Ollama(model="llama2",temperature=0)

print(llm.invoke(template))