import asyncio
import logging
from functools import wraps
from typing import Callable

from app.config import settings


def handle_errors(logger: logging.Logger) -> Callable:
    """
    エラーハンドリングを行うデコレータ
    リトライ処理も含む
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> any:
            retries = 0
            while retries < settings.MAX_RETRIES:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    logger.error(f"Error in {func.__name__}: {str(e)}")
                    if retries < settings.MAX_RETRIES:
                        wait_time = settings.RETRY_DELAY * (
                            2 ** (retries - 1)
                        )  # 指数バックオフ
                        logger.info(
                            f"Retrying in {wait_time} seconds... (Attempt {retries + 1}/{settings.MAX_RETRIES})"
                        )
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(
                            f"Maximum retries ({settings.MAX_RETRIES}) reached for {func.__name__}"
                        )
                        raise
            return None

        return wrapper

    return decorator
