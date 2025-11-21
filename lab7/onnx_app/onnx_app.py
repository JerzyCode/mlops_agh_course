from fastapi import FastAPI
from pydantic import BaseModel
import onnxruntime as ort
import numpy as np

app = FastAPI()

NON_OPT_MODEL_PATH = "non_opt_model.onnx"
OPT_MODEL_PATH = "opt_model.onnx"

sess_options = ort.SessionOptions()
sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_EXTENDED
sess_options.intra_op_num_threads = 16
sess_options.inter_op_num_threads = 2
sess_options.enable_cpu_mem_arena = True
sess_options.optimized_model_filepath = OPT_MODEL_PATH

ort_session = ort.InferenceSession(NON_OPT_MODEL_PATH, sess_options=sess_options, providers=["CPUExecutionProvider"])

class Input(BaseModel):
    pass

@app.post("/onnx-app/predict")
def predict(data: Input):
    pass