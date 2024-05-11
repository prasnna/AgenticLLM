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

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = langchain_key

# use local cache, ~ 500 MB download size


#C:\Users\pparthasarathy\.cache\huggingface\hub\models--sentence-transformers--all-mpnet-base-v2\snapshots\84f2bcc00d77236f9e89c8a360a00fb1139bf47d

# Directory path containing SQL files
sql_dir_path = "C:/sql-scripts/"


# List to store SQL file contents
sql_contents = []

# Read SQL files from the directory
for filename in os.listdir(sql_dir_path):
    if filename.endswith(".sql") and filename in ['sql list']:
        print('Embedding', filename)
        with open(os.path.join(sql_dir_path, filename), "r") as file:
            sql_content = file.read()
            sql_contents.append(sql_content)



# Embed
vectorstore = Chroma.from_texts(texts=sql_contents,
                                    embedding=HuggingFaceEmbeddings(model_name=model_ckpt_path))# HuggingFaceEmbeddings(model_name="bert-base-uncased"))

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

#### RETRIEVAL and GENERATION ####


docs = retriever.get_relevant_documents("test")

print(docs)