import os
from typing import List

from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS
from starlette.requests import Request
# from langchain.chains.question_answering import load_qa_chain
from ray import serve
# import torch
from transformers import AutoTokenizer, AutoModel

from const import BASE_MODEL, FAISS_INDEX_PATH
from embedding import LocalEmbedding
# from pipeline import LocalPipeline

template = """
你是一个专业的，基于事实的问答机器人，精通 Kubernetes 知识。
你的回答要详细且准确。
目前已知：{context}
请回答：{question}
"""

PROMPT = PromptTemplate(
    template=template,
    input_variables=["context", "question"],
    )


@serve.deployment(
    ray_actor_options={"num_gpus": 1},
    autoscaling_config={"min_replicas": 1, "max_replicas": 10},
)
# We didn't use pipeline for issue below:
# # https://github.com/kerthcet/k8s-specific-knowledge-base/issues/1
class QADeployment:
    def __init__(self) -> None:
        dirname = os.path.dirname(os.path.abspath(__file__))
        root_path = os.path.dirname(dirname)

        self.embeddings = LocalEmbedding()
        self.db = FAISS.load_local(
            folder_path=os.path.join(root_path, FAISS_INDEX_PATH),
            embeddings=self.embeddings,
            )

        self.tokenizer = AutoTokenizer.from_pretrained(
            BASE_MODEL, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(
            BASE_MODEL, trust_remote_code=True).quantize(8).half().cuda()
        self.model = self.model.eval()

    # TODO: support history.
    def qa(self, query: str):
        result, _ = self.model.chat(self.tokenizer, query, history=[])
        print(f"Primitive results: {result}")

        search_results = self.db.similarity_search(query, k=5)
        embedding_results = []
        for r in search_results:
            embedding_results.append(r.page_content)

        prompt = PROMPT.format(
            context=" ".join(embedding_results),
            question=query,
            )
        print(f"Prompt: {prompt}")

        result, _ = self.model.chat(self.tokenizer, prompt, history=[])
        print(f"Summarize results: {result}")
        return result

    # def __init__(self) -> None:
    #     dirname = os.path.dirname(os.path.abspath(__file__))
    #     root_path = os.path.dirname(dirname)

    #     self.embeddings = LocalEmbedding()
    #     self.db = FAISS.load_local(
    #         folder_path=os.path.join(root_path, FAISS_INDEX_PATH),
    #         embeddings=self.embeddings,
    #         )

    #     self.llm = LocalPipeline.from_model_id(
    #         model_id=BASE_MODEL,
    #         task="text-generation",
    #         trust_remote_code=True,
    #         model_kwargs={"device_map": "auto",
    #                       "torch_dtype": torch.float16,
    #                       },
    #     )
    #     self.chain = load_qa_chain(
    #         llm=self.llm,
    #         chain_type="stuff",
    #         prompt=PROMPT,
    #         )

    # def qa(self, query):
    #     search_results = self.db.similarity_search(query)
    #     result = self.chain({"input_documents": search_results,
    #                          "question": query})

    #     print(f"Result is: {result}")
    #     return result["output_text"]

    async def __call__(self, request: Request) -> List[str]:
        return self.qa(request.query_params["query"])


deployment = QADeployment.bind()
