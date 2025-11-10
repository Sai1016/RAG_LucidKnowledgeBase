#LLM Integration Module
from transformers import pipeline

# Initialize text generation pipeline
llm = pipeline(
    "text-generation",
    model="mistralai/Mistral-7B-Instruct-v0.2",
    dtype="auto",     # use torch_dtype, not dtype (safer and standard)
    device_map="auto"
)

def generate_answer(context: str, query: str) -> str:
    prompt = f"""You are a helpful assistant. Use the following context to answer the question.
Context: {context}
Question: {query}
Answer:"""
    
    output = llm(
        prompt,
        max_new_tokens=300,  
        temperature=0.3
    )
    
    return output[0]["generated_text"]

#error:ValueError: Using a `device_map`, `tp_plan`, `torch.device` context manager or setting `torch.set_default_device(device)` requires `accelerate`. You can install it with `pip install accelerate`..solution: certain functionalities related to device management in PyTorch, such as device_map, tp_plan, torch.device so installed accelerate library using pip install accelerate