from unittest.mock import MagicMock

import pytest
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

from src.core.exception import InvalidInputError
from src.core.sentiment_analyzer import SentimentAnalyzer


@pytest.fixture
def mock_embedder():
    yield MagicMock(spec=SentenceTransformer)


@pytest.fixture
def mock_classifier():
    yield MagicMock(spec=LogisticRegression)


@pytest.fixture
def sentiment_analyzer(mock_embedder, mock_classifier):
    yield SentimentAnalyzer(mock_embedder, mock_classifier)


def test_predict_with_empty_input(sentiment_analyzer):
    with pytest.raises(InvalidInputError, match="Text cannot be empty"):
        sentiment_analyzer.predict("")

    with pytest.raises(InvalidInputError, match="Text cannot be empty"):
        sentiment_analyzer.predict("   ")

    with pytest.raises(InvalidInputError, match="Text cannot be empty"):
        sentiment_analyzer.predict(None)


def test_predict_negative_label(sentiment_analyzer, mock_embedder, mock_classifier):
    # given
    text = "Im very sad"
    mock_embedder.encode.return_value = [[-1.0] * 10]
    mock_classifier.predict.return_value = [0]

    # when
    result = sentiment_analyzer.predict(text)

    # then
    assert result == "negative"
    mock_embedder.encode.assert_called_once_with([text])
    mock_classifier.predict.assert_called_once_with([[-1.0] * 10])


def test_predict_neutral_label(sentiment_analyzer, mock_embedder, mock_classifier):
    # given
    text = "Im neutral"
    mock_embedder.encode.return_value = [[0.0] * 10]
    mock_classifier.predict.return_value = [1]

    # when
    result = sentiment_analyzer.predict(text)

    # then
    assert result == "neutral"
    mock_embedder.encode.assert_called_once_with([text])
    mock_classifier.predict.assert_called_once_with([[0.0] * 10])


def test_predict_positive_label(sentiment_analyzer, mock_embedder, mock_classifier):
    # given
    text = "Im happy"
    mock_embedder.encode.return_value = [[1.0] * 10]
    mock_classifier.predict.return_value = [2]

    # when
    result = sentiment_analyzer.predict(text)

    # then
    assert result == "positive"
    mock_embedder.encode.assert_called_once_with([text])
    mock_classifier.predict.assert_called_once_with([[1.0] * 10])
