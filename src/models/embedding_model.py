"""
Module for embedding models
"""
from typing import List
from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    """
    A class for generating embeddings from text
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding model
        
        Args:
            model_name: The name of the sentence-transformers model to use
        """
        self.model = SentenceTransformer(model_name)
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts
        
        Args:
            texts: A list of texts to embed
            
        Returns:
            A list of embeddings, one for each text
        """
        return self.model.encode(texts).tolist()
    
    def get_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding for a single text
        
        Args:
            text: The text to embed
            
        Returns:
            The embedding for the text
        """
        return self.model.encode(text).tolist()
    
    def similarity(self, text1: str, text2: str) -> float:
        """
        Calculate the cosine similarity between two texts
        
        Args:
            text1: The first text
            text2: The second text
            
        Returns:
            The cosine similarity between the two texts
        """
        embedding1 = self.model.encode(text1)
        embedding2 = self.model.encode(text2)
        return self.model.similarity(embedding1, embedding2)
