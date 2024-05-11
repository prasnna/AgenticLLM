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
sql_dir_path = "C:/sql-scripts/"


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

# Define customize tool
class QueryHelpTool(BaseTool):
    name = "query_help_tool"
    description = "Always use this tool to get relevant columns names or table joins needed to form the query before forming the final query."

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
query_help_tool = QueryHelpTool()