"""Gmail archive email test snippet."""

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


async def test_archive_email(email_id: str) -> None:
    """Test email archiving functionality.

    Args:
        email_id: ID of the email to archive
    """
    try:
        # GmailServiceのインスタンスを作成
        gmail_service = GmailService()

        # メッセージの情報を取得（存在確認のため）
        try:
            gmail_messages = gmail_service._service.users().messages()
            email_data = gmail_messages.get(userId="me", id=email_id).execute()

            # メールの基本情報をログ出力
            headers = {
                header["name"].lower(): header["value"]
                for header in email_data["payload"]["headers"]
            }
            logger.info("Found email:")
            logger.info("Subject: %s", headers.get("subject", "No subject"))
            logger.info("From: %s", headers.get("from", "Unknown sender"))
            logger.info("Date: %s", headers.get("date", "Unknown date"))

            # 自動的にyesとして処理を続行
            logger.info("Proceeding with archiving (auto-confirmed)")

            # メールのアーカイブを試行
            result = await gmail_service.archive_email(email_id)

            if result:
                logger.info("Successfully archived email: %s", email_id)
            else:
                logger.error("Failed to archive email: %s", email_id)

        except Exception as e:
            logger.error("Email not found or not accessible: %s", str(e))
            return

    except Exception as e:
        logger.error("Error during email archiving test: %s", str(e))


if __name__ == "__main__":
    # コマンドライン引数からemail_idを取得
    if len(sys.argv) != 2:
        print("Usage: python test_archive_email.py <email_id>")
        sys.exit(1)

    email_id = sys.argv[1]

    # テストの実行
    asyncio.run(test_archive_email(email_id))
