from main import export_envs, load_secrets
from settings import Settings


def test_settings_loaded_correctly():
    load_secrets()
    export_envs("test")

    settings = Settings()

    assert settings.APP_NAME is not None
    assert settings.ENVIRONMENT is not None
    assert settings.GEMINI_TOKEN is not None

    assert isinstance(settings.GEMINI_TOKEN, str)
    assert isinstance(settings.APP_NAME, str)
    assert isinstance(settings.ENVIRONMENT, str)
    assert len(settings.GEMINI_TOKEN) > 0
