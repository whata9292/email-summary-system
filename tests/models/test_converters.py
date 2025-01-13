"""Test cases for data converters."""
from datetime import datetime

from app.models.converters import email_to_notion_data
from app.models.email import EmailData


def test_email_to_notion_data() -> None:
    """Test conversion from EmailData to Notion data format."""
    # Given
    email = EmailData(
        message_id="test123",
        subject="Test Subject",
        sender="test@example.com",
        received_at=datetime(2024, 1, 1, 12, 0),
        content="Test content",
    )

    # When
    result = email_to_notion_data(email)

    # Then
    assert result["title"] == "Test Subject"
    assert result["content"] == "Test content"
