"""Notion integration service."""
import logging
from typing import Any, Dict

from notion_client import AsyncClient

from app.utils.error_handler import handle_errors

logger = logging.getLogger(__name__)


class NotionService:
    """Service for interacting with Notion API."""

    def __init__(self, api_token: str, database_id: str) -> None:
        """
        Initialize Notion service.

        Args:
            api_token: Notion API token
            database_id: Target Notion database ID
        """
        self.client = AsyncClient(auth=api_token)
        self.database_id = database_id

    @handle_errors
    async def add_entry(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new entry to the Notion database.

        Args:
            data: Entry data containing email_id, subject, sender, date, and summary

        Returns:
            Created Notion page data
        """
        page = await self.client.pages.create(
            parent={"database_id": self.database_id},
            properties={
                "Email ID": {"title": [{"text": {"content": data["email_id"]}}]},
                "Subject": {"rich_text": [{"text": {"content": data["subject"]}}]},
                "Sender": {"rich_text": [{"text": {"content": data["sender"]}}]},
                "Date": {"date": {"start": data["date"]}},
                "Summary": {"rich_text": [{"text": {"content": data["summary"]}}]},
            },
        )
        return page
