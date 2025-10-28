from src.utils.config import Settings

settings = Settings()


def test_settings():
    assert settings is not None
    assert settings.ENBEDDER_PATH is not None
    assert settings.CLASSIFIER_PATH is not None
