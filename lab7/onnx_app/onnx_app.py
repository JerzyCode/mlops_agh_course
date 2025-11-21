from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer

import onnxruntime as ort
import numpy as np

model_name = "sentence-transformers/multi-qa-mpnet-base-cos-v1"

app = FastAPI()

NON_OPT_MODEL_PATH = "non_opt_model.onnx"

sess_options = ort.SessionOptions()
sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_EXTENDED
sess_options.intra_op_num_threads = 1
sess_options.inter_op_num_threads = 2
sess_options.enable_cpu_mem_arena = True
tokenizer = AutoTokenizer.from_pretrained(model_name)

ort_session = ort.InferenceSession(NON_OPT_MODEL_PATH, sess_options=sess_options, providers=["CPUExecutionProvider"])

class Input(BaseModel):
    text: str

@app.post("/onnx-app/predict")
def predict(data: Input):
    encoded = tokenizer(data.text, padding=True, truncation=True, return_tensors="np")
    ort_inputs = {}

    for inp in ort_session.get_inputs():
        name = inp.name
        if name in encoded:
            arr = encoded[name]
            if np.issubdtype(arr.dtype, np.integer) and arr.dtype != np.int64:
                arr = arr.astype(np.int64)
            ort_inputs[name] = arr

    outputs = ort_session.run(None, ort_inputs)
    embedding = np.array(outputs[0])
    return {
        "input": data.text,
        "embedding": embedding.squeeze().tolist()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)