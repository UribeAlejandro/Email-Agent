import os

from dotenv import find_dotenv, load_dotenv


def load_env() -> None:
    """Load environment variables from .env file."""
    _ = load_dotenv(find_dotenv())


def get_openai_api_key() -> str | None:
    """Get the OpenAI API key from the environment."""
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key
