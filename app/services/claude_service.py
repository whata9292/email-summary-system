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
            "# 指示\n"
            "あなたはプロの翻訳者です。以下の英文を完全な形で日本語に翻訳してください。\n\n"
            "# 重要な注意点\n"
            "- 文章を省略せず、全文を翻訳すること\n"
            "- 要約や省略をせず、原文の内容を完全に翻訳すること\n"
            "- [Note: ...] のような注釈は付けないこと\n"
            "- 翻訳文のみを出力すること\n\n"
            "# 原文\n"
            f"{text}"
        )

        message: Message = self.client.messages.create(
            max_tokens=8192,
            model="claude-3-5-sonnet-20241022",
            messages=[{"role": "user", "content": prompt}],
        )

        if message.content and len(message.content) > 0:
            content = message.content[0]
            if hasattr(content, "text"):
                return content.text

        return "No summary generated"
