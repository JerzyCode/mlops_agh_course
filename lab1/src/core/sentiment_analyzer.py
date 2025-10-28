from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

from src.core.exception import InvalidInputError


class SentimentAnalyzer:
    def __init__(self, embedder: SentenceTransformer, classifier: LogisticRegression):
        self.embedder = embedder
        self.classifier = classifier

    def predict(self, text: str) -> str:
        if text is None or text.strip() == "":
            raise InvalidInputError("Text cannot be empty")

        embedding = self.embedder.encode([text])
        label = self.classifier.predict(embedding)[0]

        return self._map_label(label)

    def _map_label(self, label: int) -> str:
        if label == 0:
            return "negative"
        elif label == 1:
            return "neutral"
        elif label == 2:
            return "positive"
        else:
            raise ValueError(f"Unknown label: {label}")
