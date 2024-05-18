import os
import pickle
from langchain.chat_models import ChatOpenAI
from langchain_core.runnables.passthrough import RunnablePassthrough
from langchain_core.output_parsers.string import  StrOutputParser
from langchain import hub
from langchain_core.runnables.base import Runnable
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from langchain.embeddings import HuggingFaceEmbeddings

class EmbeddingsRetriever(Runnable):
    def __init__(self, embeddings, dataset_embeddings, dataset_texts):
        self.embeddings = embeddings
        self.dataset_embeddings = dataset_embeddings
        self.dataset_texts = dataset_texts

    def retrieve_text(self, embedding):
        similarities = cosine_similarity([embedding], self.dataset_embeddings)
        closest_index = np.argmax(similarities)
        return self.dataset_texts[closest_index]

    def run(self, input_data):
        # Assuming input_data is a list of embeddings
        return [self.retrieve_text(embedding) for embedding in input_data]

    def invoke(self, input_data):
        return self.run(input_data)

embeddings = None

# Define the file path where the embeddings are stored
embeddings_file_path = "embeddings.pkl"

# Load embeddings from the pickle file
with open(embeddings_file_path, "rb") as f:
    embeddings = pickle.load(f)

print(embeddings)

hgfc = HuggingFaceEmbeddings(model_name="bert-base-uncased")

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



# Retrieve and generate using the SQL snippets
retriever = EmbeddingsRetriever(embeddings, hgfc.embed_documents(sql_text), sql_text)
prompt = hub.pull("rlm/rag-prompt")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Run RAG chain to retrieve relevant snippets from the SQL files
retrieved_snippets = rag_chain.invoke("test")