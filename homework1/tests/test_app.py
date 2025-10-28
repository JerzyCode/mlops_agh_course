import pytest
from pydantic import ValidationError

from src.api.models.sentiment_analysis import SentimentCommand


def test_sentiment_command_shold_pass():
    SentimentCommand(text="test")


def test_sentiment_command_raise():
    with pytest.raises(ValidationError):
        SentimentCommand()

    with pytest.raises(ValidationError):
        SentimentCommand(text="")

    with pytest.raises(ValidationError):
        SentimentCommand(text=None)
