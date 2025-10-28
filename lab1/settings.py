from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str
    APP_NAME: str
    GEMINI_TOKEN: str

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, value):
        if value not in {"dev", "test", "prod"}:
            raise ValueError
        return value
