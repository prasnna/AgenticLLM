"""
This script demonstrates how to create a custom tool for Langchain that retrieves relevant SQL
scripts from a directory based on the user's input query. The retrieved SQL scripts can be used
as a knowledge base or reference for building SQL queries or performing other SQL-related tasks.
"""

from langchain.tools import BaseTool
from typing import Optional
from langchain_core.callbacks.manager import CallbackManagerForToolRun
import os
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
# Updated import for HuggingFaceEmbeddings
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    # Fallback to old import if langchain_huggingface is not installed
    from langchain_community.embeddings import HuggingFaceEmbeddings
from src.utils.env_utils import load_env_vars, get_env_var, get_env_list

# Load environment variables
load_env_vars()

# Directory path containing SQL files
SQL_DIR_PATH = get_env_var("SQL_DIR_PATH", "data/sql_scripts")

# List of SQL files to include (Optional)
SQL_FILE_LIST = get_env_list("SQL_LIST_MINI", ",") or ['meta_data.sql']

# Load SQL file contents
sql_contents = []
for filename in os.listdir(SQL_DIR_PATH):
    if filename.endswith(".sql") and (not SQL_FILE_LIST or filename in SQL_FILE_LIST):
        with open(os.path.join(SQL_DIR_PATH, filename), "r") as file:
            sql_content = file.read()
            print(sql_content)
            sql_contents.append(sql_content)

# Embed SQL contents and create a vector store
vectorstore = Chroma.from_texts(
    texts=sql_contents,
    embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

class QueryHelpTool(BaseTool):
    """
    Custom tool to retrieve relevant SQL scripts based on the user's input query.
    """
    name: str = "query_help_tool"
    description: str = "Use this tool to get relevant SQL scripts based on your input query."

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool to retrieve relevant SQL scripts."""
        relevant_doc = retriever.get_relevant_documents(query)
        if not relevant_doc:
            return "No relevant SQL scripts found for the given query."
        return relevant_doc[0].page_content

    async def _arun(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Asynchronous version of the tool (not implemented)."""
        raise NotImplementedError("This tool does not support async execution.")

# Initialize the custom tool
query_help_tool = QueryHelpTool()