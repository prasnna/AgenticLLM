import bs4
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.embeddings import HuggingFaceEmbeddings

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from config import *
import os

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = langchain_key


# Directory path containing SQL files
sql_dir_path = "/Desktop/AgenticLLM/AgenticLLM/"

# List to store SQL file contents
sql_contents = []

# Read SQL files from the directory
for filename in os.listdir(sql_dir_path):
    if filename.endswith(".sql"):
        with open(os.path.join(sql_dir_path, filename), "r") as file:
            sql_contents.append(file.read())

# Join SQL contents into a single string
sql_text = "\n\n".join(sql_contents)

print(sql_text)



# Split
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_text(sql_text)


# Embed
vectorstore = Chroma.from_texts(texts=splits,
                                    embedding=OpenAIEmbeddings())# HuggingFaceEmbeddings(model_name="bert-base-uncased"))

retriever = vectorstore.as_retriever()

#### RETRIEVAL and GENERATION ####

# Prompt
prompt = hub.pull("rlm/rag-prompt")

# LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# Post-processing
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Question
rag_chain.invoke("generate SQL query to find an agency with first name like KAPLAN?")