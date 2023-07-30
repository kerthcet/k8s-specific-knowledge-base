from typing import List

import const
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings
# Embed is mostly used for ds.map_batches() because we want the result
# as ((text_batch1, embeddings1), (text_batch2, embedding2), ...)

device = None if const.DEVICE == "" else const.Device


class Embed:
    def __init__(self):
        # We use GPU for accelerating.
        self.model = SentenceTransformer(const.EMBEDDING_MODEL, device=device)

    def __call__(self, batch: List[str]):
        content = batch["text"]

        # We manually encode using sentence_transformer since LangChain
        # HuggingfaceEmbeddings does not support specifying a batch size yet.
        embeddings = self.model.encode(
            content,
            batch_size=100,
            device=device,
        ).tolist()
        return list(zip(content, embeddings))


class LocalEmbedding(Embeddings):
    def __init__(self):
        # We use GPU for accelerating.
        self.model = SentenceTransformer(const.EMBEDDING_MODEL, device=device)

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
