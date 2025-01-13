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
            data: Entry data containing title and content

        Returns:
            Created Notion page data
        """
        # ログにタイトルと要約内容を出力
        logger.info("Adding new entry to Notion - Title: %s", data["title"])
        logger.info("Summary content: %s", data["content"])

        # まずページを作成
        page = await self.client.pages.create(
            parent={"database_id": self.database_id},
            properties={
                "Name": {"title": [{"text": {"content": data["title"]}}]},
            },
        )

        # ページにコンテンツブロックを追加
        await self.client.blocks.children.append(
            block_id=page["id"],
            children=[
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {"type": "text", "text": {"content": data["content"]}}
                        ]
                    },
                }
            ],
        )

        # 成功時のログも出力
        logger.info(
            "Successfully added entry to Notion - URL: %s", page.get("url", "N/A")
        )

        return page
