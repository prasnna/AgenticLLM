from langchain.tools import BaseTool
from typing import Optional
from langchain_core.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
import bs4
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
#from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from config import *
import os

# Directory path containing SQL files
sql_dir_path = path

# List to store SQL file contents
sql_contents = []

# Read SQL files from the directory
for filename in os.listdir(sql_dir_path):
    if filename.endswith(".sql") and filename in sql_list_MINI:
        print('Embedding', filename)
        with open(os.path.join(sql_dir_path, filename), "r") as file:
            sql_content = file.read()
            sql_contents.append(sql_content)



# Embed
vectorstore = Chroma.from_texts(texts=sql_contents,
                                    embedding=HuggingFaceEmbeddings(model_name=model_ckpt_path))# HuggingFaceEmbeddings(model_name="bert-base-uncased"))

retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

# You are an SQL agent but DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database. If the question does not seem related to the database, just return "I don't know" as the answer. You have access to the following tools:

# sql_db_query: Input to this tool is a detailed and correct SQL query, output is a result from the database. If the query is not correct, an error message will be returned. If an error is returned, rewrite the query, check the query, and try again. If you encounter an issue with Unknown column 'xxxx' in 'field list', use sql_db_schema to query the correct table fields.
# sql_db_schema: Input to this tool is a comma-separated list of tables, output is the schema and sample rows for those tables. Be sure that the tables actually exist by calling sql_db_list_tables first! Example Input: table1, table2, table3
# sql_db_list_tables: Input is an empty string, output is a comma-separated list of tables in the database.
# sql_db_query_checker: Use this tool to double check if your query is correct before executing it. Always use this tool before executing a query with sql_db_query!
# query_help_tool: Always use this tool to get relevant columns names or table joins needed to form the query before forming the final query.

class QueryHelpTool(BaseTool):
    name = "query_help_tool"
    description = "Use this tool to get relevant columns names or table joins.Input to this tool can be {input}, output is relevant tables to form the query "

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        global retriever
        relevant_doc = retriever.get_relevant_documents(query)
        if len(relevant_doc) == 0 or len(query) == 0:
            return "There are no  examples to be used in this scenario."
        else:
            return relevant_doc[0].page_content

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

# Init teradata search tool
query_help_tool_v1= QueryHelpTool()