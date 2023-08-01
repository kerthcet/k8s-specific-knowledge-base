from typing import List
import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from ray.data import read_text, read_binary_files
from ray.data import ActorPoolStrategy, DataContext
from ray.data.datasource import FileExtensionFilter

from const import FAISS_INDEX_PATH
from embedding import Embed, LocalEmbedding
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
    # Report detailed progress in loading data.
    DataContext.get_current().execution_options.verbose_progress = True

    text_embeddings = []

    dirname = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.dirname(dirname)

    # Loading the books, they're PDFs.
    ds = read_binary_files(os.path.join(root_path, "contents/books"),
                           partition_filter=FileExtensionFilter("pdf"),
                           parallelism=8,
                           )
    ds.flat_map(convert_to_text)
    ds.flat_map(split_text)

    ds.map_batches(
        Embed,
        # Large batch size may lead to GPU OOM.
        batch_size=100,
        compute=ActorPoolStrategy(min_size=1, max_size=1,),  # up to 4 GPUs
        num_gpus=1,
        zero_copy_batch=True,
    )
    for row in ds.iter_rows():
        text_embeddings.append((str(row["bytes"]), row["embeddings"]))

    # Loading the blogs with the extension of ".md".
    ds = read_text(os.path.join(root_path, "contents/posts"),
                   partition_filter=FileExtensionFilter("md"),
                   parallelism=8,
                   )
    ds.flat_map(split_text)

    ds = ds.map_batches(
        Embed,
        batch_size=100,
        compute=ActorPoolStrategy(min_size=1, max_size=1,),
        num_gpus=1,
        zero_copy_batch=True,
    )
    for row in ds.iter_rows():
        text_embeddings.append((row["text"], row["embeddings"]))

    # Loading the websites.
    ds = read_text(os.path.join(root_path, "contents/website"),
                   partition_filter=FileExtensionFilter("md"),
                   parallelism=8,
                   )
    ds.flat_map(split_text)

    ds.map_batches(
        Embed,
        # Large batch size may lead to GPU OOM.
        batch_size=100,
        compute=ActorPoolStrategy(min_size=1, max_size=1),
        num_gpus=1,
        zero_copy_batch=True,
    )
    for row in ds.iter_rows():
        text_embeddings.append((row["text"], row["embeddings"]))

    vector_store = FAISS.from_embeddings(
        text_embeddings,
        # Used for embedding the query.
        embedding=LocalEmbedding(),
        )
    vector_store.save_local(os.path.join(root_path, FAISS_INDEX_PATH))


if __name__ == "__main__":
    load_data()
