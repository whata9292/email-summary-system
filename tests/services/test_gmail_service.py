"""Test cases for Gmail service."""

from unittest.mock import MagicMock, patch

import pytest

from app.services.gmail_service import GmailService


@pytest.fixture
def mock_gmail_service() -> GmailService:
    """Create a mock Gmail service.

    Returns:
        GmailService: A mocked instance of GmailService
    """
    with patch("app.services.gmail_service.build") as mock_build:
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        gmail_service = GmailService()
        gmail_service._service = mock_service
        return gmail_service


@pytest.mark.asyncio
async def test_delete_email_success(mock_gmail_service: GmailService) -> None:
    """Test successful email deletion."""
    # Arrange
    email_id = "test_email_id"
    mock_messages = mock_gmail_service._service.users().messages()
    mock_messages.delete.return_value.execute = MagicMock(return_value={})

    # Act
    result = await mock_gmail_service.delete_email(email_id)

    # Assert
    assert result is True
    mock_messages.delete.assert_called_once_with(userId="me", id=email_id)


@pytest.mark.asyncio
async def test_delete_email_failure(mock_gmail_service: GmailService) -> None:
    """Test failed email deletion."""
    # Arrange
    email_id = "test_email_id"
    mock_messages = mock_gmail_service._service.users().messages()
    mock_messages.delete.return_value.execute.side_effect = Exception("API Error")

    # Act
    result = await mock_gmail_service.delete_email(email_id)

    # Assert
    assert result is False
    mock_messages.delete.assert_called_once_with(userId="me", id=email_id)
