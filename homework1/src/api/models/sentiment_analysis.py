from pydantic import BaseModel, Field


class SentimentCommand(BaseModel):
    text: str = Field(..., min_length=1)


class SentimentResponse(BaseModel):
    prediction: str


class ErrorResponse(BaseModel):
    message: str
