from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = "prod"
    CLASSIFIER_PATH: str = "model/classifier.joblib"
    ENBEDDER_PATH: str = "model/sentence_transformer.model"

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, value: str) -> str:
        if value not in ("test", "prod"):
            raise ValueError("ENVIRONMENT must be one of: test, prod")
        return value
