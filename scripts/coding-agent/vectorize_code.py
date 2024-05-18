from langchain.text_splitter import Language
# To load the files
from langchain_community.document_loaders.generic import GenericLoader
# In the Language Parser we will pass the extension of the programming language we are working with,
# Here we are working with Pyton programming language so we will add Python, if we are working with
#Java, C++ or any other programming language we can add that extension as well
from langchain_community.document_loaders.parsers import LanguageParser
# After loading all the code in a variable we will split the code into small chunks using Recursive Character Text Splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import sys
# We will download OpenAI Embeddings
from langchain.embeddings.openai import OpenAIEmbeddings
# We will save the embeddings in the Chroma Vector Store
from langchain_community.vectorstores import Chroma
# We will create a ChatOpenAI wrapper, to chat with our document
from langchain.chat_models import ChatOpenAI
# We can add memory to our Q/A chain using Conversation Summary Memory, it will look at the historical conversation
# Computer the Summary and add that to a subsequent conversation
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI
from  dotenv import load_dotenv
env = load_dotenv()
import os
from langchain_groq import ChatGroq
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
model_ckpt_path = os.environ['model_ckpt_path']
from langchain_community.embeddings import HuggingFaceEmbeddings,OllamaEmbeddings
import langchain_core


langchain_core.globals.set_debug(True)


model_ckpt_path = os.environ['model_ckpt_path']
repo_path = os.environ['repo_path']


# loader = GenericLoader.from_filesystem(path=repo_path,
#                                         glob = "**/*",
#                                        suffixes=[".java"],
#                                        show_progress= True,
#                                        parser = LanguageParser(language=Language.JAVA, parser_threshold=500)
# )


# documents = loader.load()

# print(len(documents))



# documents_splitter = RecursiveCharacterTextSplitter.from_language(language = Language.JAVA,
#                                                              chunk_size = 2000,
#                                                              chunk_overlap = 200)


# texts = documents_splitter.split_documents(documents)


# print(len(texts))



# vectordb = Chroma.from_documents(texts, embedding=OllamaEmbeddings(model='nomic-embed-text'), persist_directory='./embedded-data')


# vectordb.persist()

vectordb = Chroma(persist_directory="./embedded-data", embedding_function=OllamaEmbeddings(model='nomic-embed-text'))


# retriever = vectordb.as_retriever(
#    search_type="mmr",  search_kwargs={"score_threshold": 0.5,"fetch_k":100,"k":50}
# )

retriever = vectordb.as_retriever(search_kwargs={"k":10})

docs = retriever.invoke("prompt")

print(docs)


# llm = ChatGroq(temperature=0, model_name="llama3-70b-8192")


# memory = ConversationSummaryMemory(llm=llm, memory_key = "chat_history", return_messages=True)

# qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)

# question = "prompt"


# result = qa.invoke(question)


# print(result)
