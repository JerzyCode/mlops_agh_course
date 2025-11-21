from fastapi import FastAPI
import torch
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModel
import torch.nn as nn

app = FastAPI()
model_name = "sentence-transformers/multi-qa-mpnet-base-cos-v1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

model_quantized = torch.ao.quantization.quantize_dynamic(
    model,
    {nn.Linear},
    dtype=torch.qint8
)

model_quantized.eval()
model_quantized = torch.compile(model_quantized)


class Input(BaseModel):
    text: str

@app.post("/torch-app/predict")
def predict(data: Input):
    inputs = tokenizer(
        data.text, padding=True, truncation=True, return_tensors="pt"
    )

    with torch.no_grad():
        outputs = model_quantized(inputs["input_ids"], inputs["attention_mask"])

    embedding = outputs[0]

    return {
        "input": data.text,
        "embedding": embedding.squeeze().tolist()
    }


if __name__ =="__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)