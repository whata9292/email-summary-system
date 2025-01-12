"""Application configuration."""
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings."""

    # Application settings
    APP_NAME: str = "email_summary_system"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # API Keys and IDs
    claude_api_key: str = os.getenv("CLAUDE_API_KEY", "")
    notion_api_key: str = os.getenv("NOTION_API_KEY", "")
    notion_database_id: str = os.getenv("NOTION_DATABASE_ID", "")
    slack_bot_token: str = os.getenv("SLACK_BOT_TOKEN", "")
    slack_channel_id: str = os.getenv("SLACK_CHANNEL_ID", "")

    # Email fetch settings
    email_lookup_hours: int = 24
    max_emails_to_process: int = 10
    processing_interval_seconds: int = 300  # 5 minutes

    # Summary settings
    SUMMARY_MAX_LENGTH: int = 500
    SUMMARY_LANGUAGE: str = "ja"

    # Retry settings
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 5  # seconds

    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    class Config:
        """Pydantic config."""

        case_sensitive = True


settings = Settings()
