from typing import List, Dict
import numpy as np

from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings

from const import DEVICE, EMBEDDING_MODEL

device = None if DEVICE == "" else DEVICE


class Embed:
    def __init__(self):
        # We use GPU for accelerating.
        self.model = SentenceTransformer(EMBEDDING_MODEL, device=device)

    def __call__(self, batch: Dict[str, np.ndarray]) -> Dict[str, list]:
        # We manually encode using sentence_transformer since LangChain
        # HuggingfaceEmbeddings does not support specifying a batch size yet.
        embeddings = self.model.encode(
            batch["text"],
            batch_size=100,
            device=device,
        ).tolist()

        batch["embeddings"] = embeddings
        return batch


class LocalEmbedding(Embeddings):
    def __init__(self):
        # We use GPU for accelerating.
        self.model = SentenceTransformer(EMBEDDING_MODEL, device=device)

    def embed_documents(self, text_batch: List[str]) -> List[List[float]]:
        """Embed a list of documents using a locally running
           Hugging Face Sentence Transformer model

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
        """
        embeddings = self.model.encode(text_batch, device=device).tolist()
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        """Embed a query using a locally running Sentence transformer.

        Args:
            text: The text to embed.

        Returns:
            Embeddings for the text.
        """
        embedding = self.model.encode(text, device=device)
        return list(map(float, embedding))
