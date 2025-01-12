import os
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# .envファイルの読み込み
load_dotenv()

class Settings(BaseSettings):
    # アプリケーション設定
    APP_NAME: str = "email_summary_system"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # メール取得の設定
    EMAIL_FETCH_INTERVAL: int = 300  # 5分ごと
    EMAIL_MAX_RESULTS: int = 10      # 1回あたりの最大取得数
    
    # サマリー生成の設定
    SUMMARY_MAX_LENGTH: int = 500    # サマリーの最大文字数
    SUMMARY_LANGUAGE: str = "ja"     # サマリーの言語
    
    # リトライ設定
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 5  # seconds
    
    # ログ設定
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    class Config:
        case_sensitive = True

settings = Settings()