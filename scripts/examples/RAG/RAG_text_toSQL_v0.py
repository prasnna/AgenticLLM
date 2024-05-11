import os
import pickle
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter




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

# Set up text splitter and Hugging Face embeddings
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_text(sql_text)
embeddings = HuggingFaceEmbeddings(model_name="bert-base-uncased")

# Generate embeddings for the SQL snippets
# Generate embeddings for the SQL snippets
embeddings = embeddings.embed_documents(splits)

print(embeddings[:3])

# Save embeddings to a file
embeddings_file_path = "embeddings.pkl"
with open(embeddings_file_path, "wb") as f:
    pickle.dump(embeddings, f)
