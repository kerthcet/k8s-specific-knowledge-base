# BASE_MODEL = "THUDM/chatglm2-6b"
# See ../deploy/rayservice-serving.yaml for details
BASE_MODEL = "/workspace/models/chatglm2-6b"
EMBEDDING_MODEL = "multi-qa-mpnet-base-dot-v1"
FAISS_INDEX_PATH = "faiss_index"
GPU_MAX_NUMBER = 1
# If you want to use GPU, set this to cuda.
DEVICE = "cuda"
