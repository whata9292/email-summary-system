"""Gmail list emails test snippet."""

import asyncio
import logging
import sys
from pathlib import Path

# プロジェクトのルートディレクトリをPYTHONPATHに追加
project_root = str(Path(__file__).parents[2])
sys.path.insert(0, project_root)

from app.services.gmail_service import GmailService  # noqa: E402

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def list_recent_emails() -> None:
    """List recent emails and their IDs."""
    try:
        # GmailServiceのインスタンスを作成
        gmail_service = GmailService()

        # メール一覧を取得（デフォルトで直近24時間分）
        emails = await gmail_service.fetch_recent_emails(hours=24, max_results=10)

        logger.info("Found %d recent emails:", len(emails))
        for email in emails:
            logger.info("ID: %s", email["id"])
            logger.info("Subject: %s", email["subject"])
            logger.info("From: %s", email["sender"])
            logger.info("Date: %s", email["date"])
            logger.info("-" * 50)

    except Exception as e:
        logger.error("Error listing emails: %s", str(e))


if __name__ == "__main__":
    asyncio.run(list_recent_emails())
