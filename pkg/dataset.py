from typing import List
import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from ray.data import ActorPoolStrategy, read_text
from ray.data.datasource import FileExtensionFilter

from const import FAISS_INDEX
from embedding import Embed, LocalEmbedding


def split_text(text: str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
    )
    text: List[str] = text_splitter.split_text(text)
    return [t.replace("\n", "") for t in text]


def load_data():
    # Struct as [(text_batch1, embeddings1), (text_batch2, embeddings2), ...]
    text_embeddings = []

    # # Loading the books, they're PDFs.
    # ds = read_binary_files("../contents/books")
    # ds.flat_map(convert_to_text)
    # ds.flat_map(split_text)
    # ds.map_batches(
    #     Embed,
    #     # Large batch size may lead to GPU OOM.
    #     batch_size=100,
    #     compute=ActorPoolStrategy(min_size=1, max_size=4,),  # up to 4 GPUs
    #     num_gpus=1,
    #     zero_copy_batch=True,
    # )
    # text_embeddings.append([row for row in ds.iter_rows()])

    dirname = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.dirname(dirname)
    print("root_path", root_path)

    # Loading the blogs with the extension of ".md".
    ds = read_text(os.path.join(root_path, "contents/posts"),
                   partition_filter=FileExtensionFilter("md"),
                   parallelism=16,
                   )
    ds.flat_map(split_text)

    ds = ds.map_batches(
        Embed,
        batch_size=100,
        compute=ActorPoolStrategy(min_size=1, max_size=1,),
        num_gpus=1,
    )
    for row in ds.iter_rows():
        text_embeddings.append(row)

    # # Loading the websites.
    # ds = read_binary_files("../contents/website")
    # ds.flat_map(split_text)
    # ds.map_batches(
    #     Embed,
    #     # Large batch size may lead to GPU OOM.
    #     batch_size=100,
    #     compute=ActorPoolStrategy(min_size=1, max_size=4),
    #     num_gpus=1,
    #     zero_copy_batch=True,
    # )
    # text_embeddings.append([row for row in ds.iter_rows()])

    vector_store = FAISS.from_embeddings(
        text_embeddings,
        # Used for embedding the query.
        embedding=LocalEmbedding(),
        )
    vector_store.save_local(FAISS_INDEX)


if __name__ == "__main__":
    load_data()
