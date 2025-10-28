import argparse
import os
from typing import Tuple

import joblib
import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression


def load_data() -> Tuple[np.ndarray, np.ndarray]:
    return load_iris(return_X_y=True)


def train_model() -> LogisticRegression:
    model = LogisticRegression(max_iter=200)
    X, y = load_data()
    model.fit(X, y)
    return model


def save_model(model_path: str, model: LogisticRegression) -> None:
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    joblib.dump(model, model_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train and save a model.")
    parser.add_argument(
        "--model_path",
        type=str,
        default="models/logistic_model.pkl",
        help="Path to save the trained model",
    )
    args = parser.parse_args()

    model = train_model()
    save_model(args.model_path, model)
    print(f"Model saved to {args.model_path}")
