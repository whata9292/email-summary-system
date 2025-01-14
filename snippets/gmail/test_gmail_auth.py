"""Test Gmail authentication script."""

import logging
import os
import sys

from dotenv import load_dotenv

# プロジェクトルートディレクトリをPYTHONPATHに追加とenv読み込みを先に実行
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(project_root)
load_dotenv(os.path.join(project_root, ".env"))

# 環境設定後にGmailServiceをインポート
from app.services.gmail_service import GmailService  # noqa: E402

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
