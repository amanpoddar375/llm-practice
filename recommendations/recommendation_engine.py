from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
from products.models import Product


class LLMRecommendationEngine:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        """
        Initialize the recommendation engine with a pre-trained embedding model

        Args:
            model_name (str): Sentence transformer model for semantic embeddings
        """
        self.embedding_model = SentenceTransformer(model_name)

    def generate_product_embedding(self, product_description: str) -> np.ndarray:
        """
        Generate embedding for a product description

        Args:
            product_description (str): Product description text

        Returns:
            np.ndarray: Dense vector representation
        """
        return self.embedding_model.encode(product_description)

    def compute_semantic_similarity(self, query_embedding: np.ndarray,
                                    product_embeddings: List[np.ndarray]) -> List[float]:
        """
        Compute cosine similarity between query and product embeddings

        Args:
            query_embedding (np.ndarray): Embedding of user query/preference
            product_embeddings (List[np.ndarray]): List of product embeddings

        Returns:
            List[float]: Similarity scores
        """
        similarities = [
            np.dot(query_embedding, product_emb) /
            (np.linalg.norm(query_embedding) * np.linalg.norm(product_emb))
            for product_emb in product_embeddings
        ]
        return similarities

    def generate_recommendations(self,
                                 user_preferences: str,
                                 top_k: int = 5) -> List[Dict]:
        """
        Generate personalized product recommendations

        Args:
            user_preferences (str): User's textual preferences
            top_k (int): Number of recommendations to generate

        Returns:
            List[Dict]: Top K recommended products
        """
        # Fetch all products
        products = Product.objects.all()

        # Generate embedding for user preferences
        user_preference_embedding = self.generate_product_embedding(user_preferences)

        # Generate embeddings for all products
        product_embeddings = [
            self.generate_product_embedding(product.description)
            for product in products
        ]

        # Compute similarities
        similarities = self.compute_semantic_similarity(
            user_preference_embedding,
            product_embeddings
        )

        # Sort products by similarity and return top K
        sorted_recommendations = sorted(
            zip(products, similarities),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]

        return [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "score": float(score)  # Convert to native float
            }
            for product, score in sorted_recommendations
        ]