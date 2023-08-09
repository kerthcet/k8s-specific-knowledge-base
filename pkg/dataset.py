from typing import List, Dict
import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.vectorstores import FAISS
from ray.data import read_text, read_binary_files
from ray.data import ActorPoolStrategy
from ray.data.datasource import FileExtensionFilter

from const import FAISS_INDEX_PATH, GPU_MAX_NUMBER
from embedding import Embed, LocalEmbedding
from utils import convert_pdf_to_text, convert_md_to_text


def split_text(text: Dict[str, str]) -> List[Dict[str, str]]:
    # We felt that the answer we would be looking for would be
    # around 200 words, or around 1000 characters.
    # This parameter can be modified based on your documents and use case.
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "(?<=\。)"],
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
    )

    result: List[str] = text_splitter.split_text(text["text"])

    final_results = []
    for r in result:
        # Handle data
        r = r.replace("\n", " ")
        r = r.replace("Kubernetes权威指南从 Docker 到Kubernetes 实践全接触（第 5版）", "")
        final_results.append(r)

    return [{"text": r.replace("\n", " ")} for r in result]


def split_markdown(text: Dict[str, str]) -> List[Dict[str, str]]:
    text_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
            ("####", "Header 4"),
        ]
    )

    result: List[str] = text_splitter.split_text(text["text"])
    contents = [{"text": r.page_content} for r in result]

    final_results = []
    for content in contents:
        for i in split_text(content):
            final_results.append(i)

    return final_results


def load_data():
    dirname = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.dirname(dirname)

    # Loading the books, they're PDFs.
    print("Loading books ...")
    ds = read_binary_files(os.path.join(root_path, "contents/books"),
                           partition_filter=FileExtensionFilter("pdf"),
                           )

    ds = ds.flat_map(convert_pdf_to_text)
    ds = ds.flat_map(split_text)
    ds = ds.map_batches(
        Embed,
        # Large batch size may lead to GPU OOM.
        batch_size=100,
        compute=ActorPoolStrategy(min_size=1, max_size=GPU_MAX_NUMBER),
        num_gpus=1,
        zero_copy_batch=True,
    )
    text_embeddings = []
    for row in ds.iter_rows():
        text_embeddings.append((row["text"], row["embeddings"]))

    # Loading the blogs with the extension of ".md".
    print("Loading posts ...")
    ds = read_binary_files(os.path.join(root_path, "contents/posts"),
                           partition_filter=FileExtensionFilter("md"),
                           )
    ds = ds.flat_map(convert_md_to_text)
    ds = ds.flat_map(split_markdown)
    ds = ds.map_batches(
        Embed,
        batch_size=100,
        compute=ActorPoolStrategy(min_size=1, max_size=GPU_MAX_NUMBER),
        num_gpus=1,
        zero_copy_batch=True,
    )
    for row in ds.iter_rows():
        text_embeddings.append((row["text"], row["embeddings"]))

    # Loading the websites.
    print("Loading websites ...")
    ds = read_binary_files(os.path.join(root_path, "contents/website"),
                           partition_filter=FileExtensionFilter("md"),
                           )
    ds = ds.flat_map(convert_md_to_text)
    ds = ds.flat_map(split_markdown)
    ds = ds.map_batches(
        Embed,
        # Large batch size may lead to GPU OOM.
        batch_size=100,
        compute=ActorPoolStrategy(min_size=1, max_size=GPU_MAX_NUMBER),
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
