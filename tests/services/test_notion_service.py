"""Test cases for Notion service."""

from unittest.mock import AsyncMock

import pytest

from app.services.notion_service import NotionService


@pytest.mark.asyncio
async def test_add_entry() -> None:
    """Test adding an entry to Notion database."""
    # Given
    api_token = "test_token"
    database_id = "test_db"
    service = NotionService(api_token, database_id)
    service.client = AsyncMock()
    service.client.pages.create = AsyncMock()
    service.client.blocks.children.append = AsyncMock()

    test_data = {"title": "Test Subject", "content": "Test content"}

    # Mock response from pages.create
    mock_page = {"id": "test_page_id", "url": "https://notion.so/test_page"}
    service.client.pages.create.return_value = mock_page

    # When
    result = await service.add_entry(test_data)

    # Then
    service.client.pages.create.assert_called_once_with(
        parent={"database_id": database_id},
        properties={
            "Name": {"title": [{"text": {"content": "Test Subject"}}]},
        },
    )

    service.client.blocks.children.append.assert_called_once_with(
        block_id="test_page_id",
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": "Test content"}}]
                },
            }
        ],
    )

    assert result == mock_page
