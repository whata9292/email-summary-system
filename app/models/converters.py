"""Data conversion utilities."""

from typing import Any, Dict

from app.models.email import EmailData


def email_to_notion_data(email: EmailData) -> Dict[str, Any]:
    """
    Convert EmailData to Notion compatible format.

    Args:
        email: EmailData instance to convert

    Returns:
        Dict containing Notion-compatible data format with title and content only
    """
    return {
        "title": email.subject,  # タイトルにメールの件名を使用
        "content": email.content,  # 本文に要約を使用
    }
