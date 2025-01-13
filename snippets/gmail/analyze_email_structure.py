"""Analyze email structure test script."""

import asyncio
import logging
import os
import sys

from dotenv import load_dotenv

from app.services.gmail_service import GmailService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# プロジェクトルートディレクトリをPYTHONPATHに追加
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)

# .envファイルの読み込み
load_dotenv(os.path.join(project_root, ".env"))


async def analyze_email_structure() -> None:
    """Analyze and display email structure in detail."""
    try:
        service = GmailService()
        # 最新のメール1件を取得
        emails = await service.fetch_recent_emails(hours=24, max_results=1)

        if not emails:
            logger.info("No emails found")
            return

        email = emails[0]

        # メールの詳細構造を分析
        logger.info("\nEmail Structure Analysis:")
        logger.info("=" * 50)
        logger.info("Basic Information:")
        logger.info(f"Message ID: {email['id']}")
        logger.info(f"Thread ID: {email['thread_id']}")

        logger.info("\nHeaders:")
        logger.info(f"Subject: {email['subject']}")
        logger.info(f"From: {email['sender']}")
        logger.info(f"Date: {email['date']}")

        logger.info("\nLabels:")
        for label in email["labels"]:
            logger.info(f"- {label}")

        logger.info("\nBody Sample:")
        # 本文の最初の200文字を表示
        body_sample = (
            email["body"][:200] + "..." if len(email["body"]) > 200 else email["body"]
        )
        logger.info(body_sample)

    except Exception as e:
        logger.error(f"Error analyzing email: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(analyze_email_structure())
