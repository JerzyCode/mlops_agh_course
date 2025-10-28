import argparse
from dotenv import load_dotenv
import yaml
from settings import Settings
import os


def export_envs(environment: str = "dev") -> None:
    load_dotenv(f".config/.env.{environment}")


def load_secrets() -> None:
    with open("secrets.yaml", "r") as file:
        secrets = yaml.safe_load(file)

        os.environ["GEMINI_TOKEN"] = secrets["gemini"]["token"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Load environment variables from specified.env file."
    )
    parser.add_argument(
        "--environment",
        type=str,
        default="dev",
        help="The environment to load (dev, test, prod)",
    )
    args = parser.parse_args()

    load_secrets()
    export_envs(args.environment)

    settings = Settings()

    print("APP_NAME: ", settings.APP_NAME)
    print("ENVIRONMENT: ", settings.ENVIRONMENT)
    print("GEMINI_TOKEN: ", settings.GEMINI_TOKEN)
