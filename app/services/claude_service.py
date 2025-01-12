"""Service for interfacing with Claude API."""

import logging

from anthropic import Anthropic, Message

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

        message: Message = await self.client.messages.create(
            max_tokens=1024,
            model="claude-3-sonnet-20240229",
            messages=[{"role": "user", "content": prompt}],
        )

        if message.content and len(message.content) > 0:
            return message.content[0].text

        return "No summary generated"
