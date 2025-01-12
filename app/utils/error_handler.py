"""Error handling utilities."""

import functools
import logging
from typing import Awaitable, Callable, ParamSpec, TypeVar

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


def handle_errors(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
    """
    Handle errors in async functions.

    Args:
        func: The async function to decorate

    Returns:
        Decorated async function with error handling
    """

    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error("Error in %s: %s", func.__name__, str(e))
            raise

    return wrapper
