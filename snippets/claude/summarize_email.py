"""Provides functionality for email summarization using Claude API."""

import logging
from typing import Any, Dict

from anthropic import Anthropic
from anthropic.types import Message

from app.config import settings
from app.utils.error_handler import handle_errors

logger = logging.getLogger(__name__)


@handle_errors
async def summarize_with_priorities(
    email_content: str, include_reply_suggestion: bool = False
) -> Dict[str, Any]:
    """Summarize email content with priority analysis and optional reply suggestions."""
    client = Anthropic(api_key=settings.claude_api_key)

    # プロンプトの構築
    base_prompt = (
        "以下のメールを分析し、日本語で以下の形式で出力してください：\n\n"
        "1. 要約（100文字程度）\n"
        "2. 優先度（High/Medium/Low）と理由\n"
        "3. アクションアイテム（箇条書き）\n"
    )

    if include_reply_suggestion:
        base_prompt += "4. 返信案（簡潔に）\n"

    prompt = f"{base_prompt}\nメール本文：\n{email_content}"

    message: Message = client.messages.create(
        max_tokens=1024,
        model="claude-3-sonnet-20240229",
        messages=[{"role": "user", "content": prompt}],
    )

    if not message.content or len(message.content) == 0:
        logger.error("No content received from Claude API")
        return {"success": False, "error": "No content received from API"}

    content = message.content[0]
    if not hasattr(content, "text"):
        logger.error("Unexpected message format received")
        return {"success": False, "error": "Invalid response format"}

    return {"success": True, "summary": content.text, "usage": message.usage}


@handle_errors
async def extract_action_items(email_content: str) -> Dict[str, Any]:
    """Extract and organize action items from email content."""
    client = Anthropic(api_key=settings.claude_api_key)

    prompt = (
        "以下のメールからアクションアイテムを抽出し、以下の形式で出力してください：\n\n"
        "1. 期限付きのアクション（締切日順）\n"
        "2. その他の要対応事項（優先度順）\n"
        "3. フォローアップが必要な事項\n\n"
        f"メール本文：\n{email_content}"
    )

    message: Message = client.messages.create(
        max_tokens=1024,
        model="claude-3-sonnet-20240229",
        messages=[{"role": "user", "content": prompt}],
    )

    if not message.content or len(message.content) == 0:
        return {"success": False, "error": "No content received"}

    content = message.content[0]
    if not hasattr(content, "text"):
        return {"success": False, "error": "Invalid response format"}

    return {"success": True, "action_items": content.text, "usage": message.usage}
