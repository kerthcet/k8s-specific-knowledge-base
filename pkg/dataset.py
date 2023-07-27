from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from ray.data import read_binary_files, ActorPoolStrategy

import const
from embedding import LocalEmbedding
from utils import convert_to_text


def split_text(text: str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
    )
    text: List[str] = text_splitter.split_text(text)
    return [t.replace("\n", "") for t in text]


def load_data():
    embeddings = []

    # Loading the books, they're PDFs.
    ds = read_binary_files("../contents/books")
    ds.flat_map(convert_to_text)
    ds.flat_map(split_text)
    ds.map_batches(
        LocalEmbedding,
        # Large batch size may lead to GPU OOM.
        batch_size=100,
        compute=ActorPoolStrategy(min_size=1, max_size=2,),
        num_gpus=1,
    )
    embeddings.append([row for row in ds.iter_rows()])

    # Loading the blogs.
    ds = read_binary_files("../contents/posts")
    ds.flat_map(split_text)
    ds.map_batches(
        LocalEmbedding,
        # Large batch size may lead to GPU OOM.
        batch_size=100,
        compute=ActorPoolStrategy(min_size=1, max_size=2,),
        num_gpus=1,
    )
    embeddings.append([row for row in ds.iter_rows()])

    # Loading the websites.
    ds = read_binary_files("../contents/website")
    ds.flat_map(split_text)
    ds.map_batches(
        LocalEmbedding,
        # Large batch size may lead to GPU OOM.
        batch_size=100,
        compute=ActorPoolStrategy(min_size=1, max_size=2,),
        num_gpus=1,
    )
    embeddings.append([row for row in ds.iter_rows()])

    # Save to vector store.
    vector_store = FAISS.from_embeddings(
        embeddings,
        embedding=LocalEmbedding(),
        )
    vector_store.save_local(const.FAISS_INDEX)


if __name__ == "__main__":
    load_data()
