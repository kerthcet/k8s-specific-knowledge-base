from typing import List, Dict
import random
import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
# from ray.data import read_text, read_binary_files
from ray.data import read_binary_files
from ray.data import ActorPoolStrategy, DataContext
from ray.data.datasource import FileExtensionFilter

from const import FAISS_INDEX_PATH
from embedding import Embed, LocalEmbedding
from utils import convert_to_text


def split_text(text: Dict[str, str]) -> List[Dict[str, str]]:
    # Use chunk_size of 1000.
    # We felt that the answer we would be looking for would be
    # around 200 words, or around 1000 characters.
    # This parameter can be modified based on your documents and use case.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
    )

    result: List[str] = text_splitter.split_text(text["text"])
    return [{"text": r.replace("\n", " ")} for r in result]


def load_data():
    # Report detailed progress in loading data.
    DataContext.get_current().execution_options.verbose_progress = True

    dirname = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.dirname(dirname)

    # Loading the books, they're PDFs.
    print("Loading books.")
    ds = read_binary_files(os.path.join(root_path, "contents/books"),
                           partition_filter=FileExtensionFilter("pdf"),
                           )

    ds = ds.flat_map(convert_to_text)
    ds = ds.flat_map(split_text)
    ds = ds.map_batches(
        Embed,
        # Large batch size may lead to GPU OOM.
        batch_size=100,
        compute=ActorPoolStrategy(min_size=1, max_size=1),
        num_gpus=1,
        zero_copy_batch=True,
    )
    text_embeddings = []
    for row in ds.iter_batches(batch_size=None):
        text_embeddings.append((row["text"], row["embeddings"]))

    for i in range(0, len(text_embeddings)):
        num = random.randint(0, len(text_embeddings)-1)
        print(text_embeddings[num])
        if i == 20:
            break

    # # Loading the blogs with the extension of ".md".
    # print("Loading posts.")
    # ds = read_text(os.path.join(root_path, "contents/posts"),
    #                partition_filter=FileExtensionFilter("md"),
    #                )
    # ds = ds.flat_map(split_text)
    # ds = ds.map_batches(
    #     Embed,
    #     batch_size=100,
    #     compute=ActorPoolStrategy(min_size=1, max_size=1,),
    #     num_gpus=1,
    #     zero_copy_batch=True,
    # )
    # for row in ds.iter_batches():
    #     text_embeddings.append((row["text"], row["embeddings"]))

    # for i in range(0, len(text_embeddings)):
    #     num = random.randint(0, len(text_embeddings)-1)
    #     print(text_embeddings[num])
    #     if i == 20:
    #         break

    # # Loading the websites.
    # print("Loading websites.")
    # ds = read_text(os.path.join(root_path, "contents/website"),
    #                partition_filter=FileExtensionFilter("md"),
    #                )
    # ds = ds.flat_map(split_text)
    # ds = ds.map_batches(
    #     Embed,
    #     # Large batch size may lead to GPU OOM.
    #     batch_size=100,
    #     compute=ActorPoolStrategy(min_size=1, max_size=1),
    #     num_gpus=1,
    #     zero_copy_batch=True,
    # )
    # for row in ds.iter_batches():
    #     text_embeddings.append((row["text"], row["embeddings"]))

    # for i in range(0, len(text_embeddings)):
    #     num = random.randint(0, len(text_embeddings)-1)
    #     print(text_embeddings[num])
    #     if i == 30:
    #         break

    vector_store = FAISS.from_embeddings(
        text_embeddings,
        # Used for embedding the query.
        embedding=LocalEmbedding(),
        )
    vector_store.save_local(os.path.join(root_path, FAISS_INDEX_PATH))


if __name__ == "__main__":
    load_data()
