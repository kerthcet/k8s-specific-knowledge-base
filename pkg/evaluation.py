from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("../models/chatglm2-6b",
                                          trust_remote_code=True)
model = AutoModel.from_pretrained(
    "../models/chatglm2-6b", trust_remote_code=True).half().cuda()

model = model.eval()
response, history = model.chat(tokenizer, "Kubernetes 可以用来做什么？", history=[])
print(response)
