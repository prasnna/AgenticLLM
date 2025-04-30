import logging
from langchain_openai import OpenAI
from langchain_community.document_loaders.mongodb import MongodbLoader
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
import os
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.callbacks import StdOutCallbackHandler
from src.utils.env_utils import load_env_vars, get_env_var

#logging.basicConfig(level=logging.DEBUG)

# Load environment variables
load_env_vars()

# Set OpenAI API key as an environment variable
os.environ["OPENAI_API_KEY"] = get_env_var("OPENAI_API_KEY")

# Set up callbacks for verbose LLM interaction
stdio_handler = StdOutCallbackHandler()

llm = OpenAI(temperature=0.7,callbacks=[stdio_handler])

# Set up MongoDB connection
mongo_connection = get_env_var("MONGOV2")
mongo_loader = MongodbLoader(connection_string=mongo_connection, db_name='ciCommon',collection_name='NoSqlToCSVJobParameters')

# Load data from MongoDB
docs = mongo_loader.load()

# Create an embedding function
embeddings = OpenAIEmbeddings()

# Create a vector store
vector_store = FAISS.from_documents(docs, embeddings)

# Create a RetrievalQA instance
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_store.as_retriever(),verbose=True)

# Run a query
query = "explain the collection"
result = qa.run(query)
print(result)
