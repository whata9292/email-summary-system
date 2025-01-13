"""Fetch recent emails test script."""

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
load_dotenv(os.path.join(project_root, ".env"))

from app.services.gmail_service import GmailService  # noqa: E402


async def fetch_emails() -> None:
    """Fetch and display metadata of recent emails."""
    try:
        service = GmailService()
        # 過去24時間のメールを最大10件取得
        emails = await service.fetch_recent_emails(hours=24, max_results=10)

        logger.info(f"Retrieved {len(emails)} emails")

        # 各メールのメタデータを表示
        for i, email in enumerate(emails, 1):
            logger.info(f"\nEmail {i}:")
            logger.info(f"Subject: {email['subject']}")
            logger.info(f"From: {email['sender']}")
            logger.info(f"Date: {email['date']}")
            logger.info("Labels: " + ", ".join(email["labels"]))
            logger.info("-" * 50)

    except Exception as e:
        logger.error(f"Error fetching emails: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(fetch_emails())
