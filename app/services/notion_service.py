"""Notion integration service."""

import logging
from typing import Any, Dict, List

from notion_client import AsyncClient

from app.utils.error_handler import handle_errors

logger = logging.getLogger(__name__)


class NotionService:
    """Service for interacting with Notion API."""

    NOTION_TEXT_LIMIT = 2000  # Maximum character limit per Notion block

    def __init__(self, api_token: str, database_id: str) -> None:
        """
        Initialize Notion service.

        Args:
            api_token: Notion API token
            database_id: Target Notion database ID
        """
        self.client = AsyncClient(auth=api_token)
        self.database_id = database_id

    def _split_content(self, content: str) -> List[str]:
        """
        Split content into chunks of maximum 2000 characters.

        Maintains meaningful content blocks by splitting on newlines. Only forces
        a mid-paragraph split if a single paragraph exceeds the character limit.

        Args:
            content: The input text to be split

        Returns:
            A list of text chunks, each under 2000 characters
        """
        current_chunk = ""
        chunks = []
        paragraphs = content.split("\n")

        for paragraph in paragraphs:
            # Check chunk size after adding current paragraph
            new_chunk = current_chunk + ("\n" if current_chunk else "") + paragraph

            if len(new_chunk) > self.NOTION_TEXT_LIMIT:
                # Save current chunk if it exists
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = paragraph
                else:
                    # Force split if a single paragraph exceeds limit
                    chunks.append(paragraph[: self.NOTION_TEXT_LIMIT])
                    remaining = paragraph[self.NOTION_TEXT_LIMIT :]
                    if remaining:
                        current_chunk = remaining
            else:
                current_chunk = new_chunk

        # Add the final chunk
        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def _create_block_objects(self, chunks: List[str]) -> List[Dict[str, Any]]:
        """
        Create Notion block objects from text chunks.

        Args:
            chunks: List of text chunks to be converted to blocks

        Returns:
            List of Notion block objects ready for API submission
        """
        return [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": chunk}}]
                },
            }
            for chunk in chunks
        ]

    @handle_errors
    async def add_entry(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new entry to the Notion database.

        Args:
            data: Entry data containing title and content

        Returns:
            Created Notion page data
        """
        logger.info("Adding new entry to Notion - Title: %s", data["title"])

        # Create the page first
        page = await self.client.pages.create(
            parent={"database_id": self.database_id},
            properties={
                "Name": {"title": [{"text": {"content": data["title"]}}]},
            },
        )

        # Split content and create blocks
        content_chunks = self._split_content(data["content"])
        blocks = self._create_block_objects(content_chunks)

        # Add content blocks to the page
        await self.client.blocks.children.append(block_id=page["id"], children=blocks)

        logger.info(
            "Successfully added entry to Notion - URL: %s, Number of blocks: %d",
            page.get("url", "N/A"),
            len(blocks),
        )

        return page
