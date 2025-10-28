from fastapi import FastAPI

from src.api.models.iris import PredictRequest, PredictResponse
from src.core.inference import load_model, predict_single

model = load_model()
app = FastAPI()


@app.get("/")
def welcome_root():
    return {"message": "Welcome to the ML API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/predict")
def predict(request: PredictRequest) -> PredictResponse:
    prediction = predict_single(
        model,
        features=[
            request.sepal_length,
            request.sepal_width,
            request.petal_length,
            request.petal_width,
        ],
    )
    return PredictResponse(prediction=prediction)
