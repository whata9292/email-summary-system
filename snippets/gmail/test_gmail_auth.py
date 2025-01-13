"""Test Gmail authentication script."""

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


def test_gmail_auth() -> GmailService:
    """Test Gmail authentication process and return the service instance."""
    try:
        # GmailServiceのインスタンス作成（この時点で認証が実行される）
        service = GmailService()
        logger.info("Gmail authentication successful!")
        return service
    except Exception as e:
        logger.error(f"Failed to authenticate with Gmail: {e}")
        raise


if __name__ == "__main__":
    test_gmail_auth()
