import joblib
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

from src.utils.logger import log


def load_text_embedder(path: str) -> SentenceTransformer:
    log.info("Loading text embedder...")
    model = SentenceTransformer(path)
    return model


def load_classifier(path: str) -> LogisticRegression:
    log.info("Loading text classifier...")
    return joblib.load(path)
