from fastapi import FastAPI, HTTPException

from src.api.models.sentiment_analysis import SentimentCommand, SentimentResponse
from src.core.exception import InvalidInputError
from src.core.model_repository import load_classifier_s3, load_text_embedder_s3
from src.core.sentiment_analyzer import SentimentAnalyzer
from src.utils.config import Settings
from src.utils.logger import log

settings = Settings()

app = FastAPI()
embedder = load_text_embedder_s3(
    settings.S3_BUCKET_NAME, settings.S3_EMBEDDER_KEY, settings.ENBEDDER_PATH
)

classifier = load_classifier_s3(
    settings.S3_BUCKET_NAME, settings.S3_CLASSIFIER_KEY, settings.CLASSIFIER_PATH
)
analyzer = SentimentAnalyzer(embedder, classifier)


@app.get("/health")
async def health_check():
    return {"status": "Running!"}


@app.post("/predict")
async def predict_sentiment(
    command: SentimentCommand,
) -> SentimentResponse:
    log.debug(f"Analyzing sentiment for text: {command.text}")
    try:
        prediction = analyzer.predict(command.text)
        return SentimentResponse(prediction=prediction)
    except InvalidInputError as e:
        log.error(f"Invalid input: {e}")
        raise HTTPException(status_code=400, detail=str(e))
