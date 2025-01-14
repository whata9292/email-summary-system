"""Example of using the Slack notification service."""

import asyncio
import logging
import os
import sys

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# プロジェクトルートディレクトリをPYTHONPATHに追加
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)

# .envファイルの読み込み
load_dotenv(os.path.join(project_root, ".env"), override=True)

from app.services.slack_service import SlackService  # noqa: E402


async def send_test_message() -> None:
    """Send a test message to Slack."""
    # Initialize Slack service
    slack_token = os.getenv("SLACK_BOT_TOKEN")
    channel_id = os.getenv("SLACK_CHANNEL_ID")

    logger.info("Token prefix: %s...", slack_token[:10] if slack_token else "None")
    logger.info("Channel ID: %s", channel_id)

    if not slack_token or not channel_id:
        raise ValueError("Slack credentials not found in environment variables")

    slack_service = SlackService(slack_token, channel_id)

    # Send test message
    message = "This is a test message from the Email Summary System"
    response = await slack_service.send_notification(message)
    print(f"Message sent successfully: {response}")


if __name__ == "__main__":
    # 環境変数の読み込み状態を確認
    logger.info("Current working directory: %s", os.getcwd())
    logger.info("Project root: %s", project_root)

    asyncio.run(send_test_message())
