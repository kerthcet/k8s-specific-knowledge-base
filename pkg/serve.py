import os
from typing import List

from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS
from starlette.requests import Request
from langchain.chains.question_answering import load_qa_chain
from ray import serve
import torch

from const import BASE_MODEL, FAISS_INDEX_PATH
from embedding import LocalEmbedding
from pipeline import LocalPipeline
from dataset import load_data

template = """
If you don't know the answer, just say that you don't know. Don't try to make
up an answer. Please answer the following question using the context provided.

CONTEXT:
{context}
=========
QUESTION: {question}
ANSWER: <|ASSISTANT|>"""

PROMPT = PromptTemplate(
    template=template,
    input_variables=["context", "question"],
    )


# TODO: integrate with FastAPI

@serve.deployment(
    ray_actor_options={"num_gpus": 1},
    autoscaling_config={"min_replicas": 1, "max_replicas": 10},
)
class QADeployment:
    def __init__(self) -> None:
        dirname = os.path.dirname(os.path.abspath(__file__))
        root_path = os.path.dirname(dirname)

        self.embeddings = LocalEmbedding()
        self.db = FAISS.load_local(
            folder_path=os.path.join(root_path, FAISS_INDEX_PATH),
            embeddings=self.embeddings,
            )

        self.llm = LocalPipeline.from_model_id(
            model_id=BASE_MODEL,
            task="text-generation",
            model_kwargs={"device_map": "auto", "torch_dtype": torch.float16},
        )
        self.chain = load_qa_chain(
            llm=self.llm,
            chain_type="stuff",
            prompt=PROMPT,
            )

    def qa(self, query):
        search_results = self.db.similarity_search(query)
        result = self.chain({"input_documents": search_results,
                             "question": query})

        print(f"Result is: {result}")
        return result["output_text"]

    async def __call__(self, request: Request) -> List[str]:
        return self.qa(request.query_params["query"])


deployment = QADeployment.bind()
