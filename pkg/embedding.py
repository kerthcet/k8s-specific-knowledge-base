from typing import List

import const
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings


class LocalEmbedding(Embeddings):
    def __init__(self):
        # We use GPU for accelerating.
        self.model = SentenceTransformer(const.EMBEDDING_MODEL, device="cuda")

    def embed_documents(self, text_batch: List[str]) -> List[List[float]]:
        """Embed a list of documents using a locally running
           Hugging Face Sentence Transformer model

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
        """
        embeddings = self.model.encode(text_batch, device="cuda")
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        """Embed a query using a locally running HF
        Sentence transformer.

        Args:
            text: The text to embed.

        Returns:
            Embeddings for the text.
        """
        embedding = self.model.encode(text, device="cuda")
        return list(map(float, embedding))
