"""Service for interfacing with Claude API."""

import logging

from anthropic import Anthropic
from anthropic.types import Message

from app.utils.error_handler import handle_errors

logger = logging.getLogger(__name__)


class ClaudeService:
    """Service for generating summaries using Claude API."""

    def __init__(self, api_token: str) -> None:
        """
        Initialize Claude service.

        Args:
            api_token: Claude API token
        """
        self.client = Anthropic(api_key=api_token)

    @handle_errors
    async def generate_summary(self, text: str) -> str:
        """
        Generate a summary of the provided text.

        Args:
            text: Text to summarize

        Returns:
            Generated summary text
        """
        prompt = (
            "Please provide a concise summary of the following email. "
            "Focus on key points and action items if any:\n\n"
            f"{text}"
        )

        message: Message = self.client.messages.create(
            max_tokens=1024,
            model="claude-3.5-sonnet-20241022",
            messages=[{"role": "user", "content": prompt}],
        )

        if message.content and len(message.content) > 0:
            content = message.content[0]
            if hasattr(content, "text"):
                return content.text

        return "No summary generated"
