import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression

MODEL_PATH = "models/logistic_model.pkl"

LABELS = {
    0: "setosa",
    1: "versicolor",
    2: "virginica",
}


def load_model(model_path=MODEL_PATH) -> LogisticRegression:
    return joblib.load(model_path)


def predict_single(model: LogisticRegression, features: list[float]) -> str:
    data = np.array([features])
    pred_class = model.predict(data)[0]
    return LABELS[int(pred_class)]
