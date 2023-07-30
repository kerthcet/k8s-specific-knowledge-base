from typing import Any, List, Optional

from langchain import HuggingFacePipeline
from transformers import pipeline as hf_pipeline


class LocalPipeline(HuggingFacePipeline):
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self.pipeline(
            prompt, temperature=0.1, max_new_tokens=256, do_sample=True
        )

        # TODO: support other tasks.
        if self.pipeline.task == "text-generation":
            # Text generation return includes the starter text.
            print(f"Response is: {response}")
            text = response[0]["generated_text"][len(prompt):]
        else:
            raise ValueError(f"Got invalid task {self.pipeline.task}. ")
        return text

    @classmethod
    def from_model_id(
        cls,
        model_id: str,
        task: str,
        device: Optional[str] = None,
        model_kwargs: Optional[dict] = None,
        **kwargs: Any,
    ):
        pipeline = hf_pipeline(
            model=model_id,
            task=task,
            device=device,
            model_kwargs=model_kwargs,
        )
        return cls(
            pipeline=pipeline,
            model_id=model_id,
            model_kwargs=model_kwargs,
            **kwargs,
        )
