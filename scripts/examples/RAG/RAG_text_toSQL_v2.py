import bs4
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from config import *
import os

os.environ['OPENAI_API_KEY'] = 'OPENAI_API_KEY'
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = langchain_key





# List to store SQL file contents
sql_contents = []

# Read SQL files from the directory
for filename in os.listdir(sql_dir_path):
    if filename.endswith(".sql") and filename in sql_list:
        print('Embedding', filename)
        with open(os.path.join(sql_dir_path, filename), "r") as file:
            sql_content = file.read()
            sql_contents.append(sql_content)



# Embed
vectorstore = Chroma.from_texts(texts=sql_contents,embedding=HuggingFaceEmbeddings(model_name=model_ckpt_path))

retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

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
rag_chain.invoke("select agents with NY contract")