import logging

from app.config import settings


def setup_logger(name: str) -> logging.Logger:
    """
    ロガーの設定を行う
    """
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)
    
    formatter = logging.Formatter(settings.LOG_FORMAT)
    
    # コンソール出力
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # ファイル出力
    file_handler = logging.FileHandler('logs/app.log', encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger