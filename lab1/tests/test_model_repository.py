from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

from src.core.model_repository import load_classifier, load_text_embedder
from src.utils.config import Settings

settings = Settings()


def test_load_embedder():
    embedder = load_text_embedder(settings.ENBEDDER_PATH)

    assert embedder is not None
    assert isinstance(embedder, SentenceTransformer)
    assert embedder.encode("test") is not None


def test_load_classifier():
    classifier = load_classifier(settings.CLASSIFIER_PATH)

    assert classifier is not None
    assert isinstance(classifier, LogisticRegression)
