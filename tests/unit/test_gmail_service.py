"""Unit tests for Gmail Service."""

from typing import Any, Dict
from unittest.mock import Mock, mock_open, patch

import pytest
from google.oauth2.credentials import Credentials

from app.config import settings
from app.services.gmail_service import GmailService


@pytest.fixture(name="mock_credentials")
def mock_credentials() -> Mock:
    """Mock Gmail credentials."""
    creds = Mock(spec=Credentials)
    creds.token = "dummy_token"
    creds.refresh_token = "dummy_refresh_token"
    creds.token_uri = "dummy_uri"
    creds.client_id = "dummy_client_id"
    creds.client_secret = "dummy_secret"
    creds.scopes = ["https://www.googleapis.com/auth/gmail.readonly"]
    creds.valid = True
    creds.expired = False
    return creds


@pytest.fixture(name="mock_gmail_service")
def mock_gmail_service() -> Mock:
    """Mock Gmail API service."""
    users = Mock()
    messages = Mock()
    list_method = Mock()
    list_method.execute.return_value = {
        "messages": [
            {"id": "123", "threadId": "thread123"},
            {"id": "456", "threadId": "thread456"},
        ]
    }
    messages.list.return_value = list_method
    messages.get.return_value.execute.return_value = {}
    users.messages.return_value = messages
    service = Mock()
    service.users.return_value = users
    return service


@pytest.fixture(name="sample_email_data")
def sample_email_data() -> Dict[str, Any]:
    """Sample email data for testing."""
    return {
        "id": "123",
        "threadId": "thread123",
        "labelIds": ["INBOX", "UNREAD"],
        "payload": {
            "headers": [
                {"name": "Subject", "value": "Test Email"},
                {"name": "From", "value": "sender@example.com"},
                {"name": "Date", "value": "Wed, 1 Jan 2025 10:00:00 +0000"},
            ],
            "body": {
                "data": "VGVzdCBlbWFpbCBib2R5"  # Base64 encoded "Test email body"
            },
        },
    }


class TestGmailService:
    """Test cases for GmailService class."""

    service: GmailService

    @pytest.fixture(autouse=True)
    def setup(self, mock_credentials: Mock, mock_gmail_service: Mock) -> None:
        """Set up test environment."""
        with (
            patch(
                "app.services.gmail_service.Credentials", return_value=mock_credentials
            ),
            patch("app.services.gmail_service.build", return_value=mock_gmail_service),
            patch("builtins.open", mock_open(read_data='{"token": "dummy_token"}')),
            patch(
                "json.load",
                return_value={
                    "token": "dummy_token",
                    "refresh_token": "dummy_refresh_token",
                    "token_uri": "dummy_uri",
                    "client_id": "dummy_client_id",
                    "client_secret": "dummy_secret",
                    "scopes": ["https://www.googleapis.com/auth/gmail.readonly"],
                },
            ),
            patch("os.path.exists", return_value=True),
        ):
            self.service = GmailService(
                token_path="dummy_token.json", credentials_path="dummy_creds.json"
            )
            # リセットカウンター
            mock_gmail_service.reset_mock()

    @pytest.mark.asyncio
    async def test_fetch_recent_emails_success(
        self, mock_gmail_service: Mock, sample_email_data: Dict[str, Any]
    ) -> None:
        """Test successful email fetching."""
        # Mock the get() method for individual email fetching
        messages_mock = mock_gmail_service.users.return_value.messages.return_value
        messages_mock.get.return_value.execute.return_value = sample_email_data

        # Test email fetching
        emails = await self.service.fetch_recent_emails(hours=24, max_results=2)

        # Verify results
        assert len(emails) == 2
        assert emails[0]["id"] == "123"
        assert emails[0]["subject"] == "Test Email"
        assert emails[0]["sender"] == "sender@example.com"

        # APIの呼び出しを検証
        messages_mock.list.assert_called_once()
        assert messages_mock.get.call_count == 2

    @pytest.mark.asyncio
    async def test_fetch_recent_emails_no_results(
        self, mock_gmail_service: Mock
    ) -> None:
        """Test behavior when no emails are found."""
        # Mock empty results
        messages_mock = mock_gmail_service.users.return_value.messages.return_value
        messages_mock.list.return_value.execute.return_value = {}

        # Test email fetching with no results
        result = await self.service.fetch_recent_emails()

        # Verify results
        assert len(result) == 0
        messages_mock.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_fetch_recent_emails_with_labels(
        self, mock_gmail_service: Mock, sample_email_data: Dict[str, Any]
    ) -> None:
        """Test email fetching with label filtering."""
        messages_mock = mock_gmail_service.users.return_value.messages.return_value
        messages_mock.get.return_value.execute.return_value = sample_email_data

        # Test email fetching with labels
        await self.service.fetch_recent_emails(label_ids=["INBOX", "UNREAD"])

        # Verify label parameter was passed
        list_call_kwargs = messages_mock.list.call_args[1]
        assert "labelIds" in list_call_kwargs
        assert list_call_kwargs["labelIds"] == ["INBOX", "UNREAD"]

    def test_parse_payload_data(self, sample_email_data: Dict[str, Any]) -> None:
        """Test email parsing functionality."""
        parsed_email = self.service.parse_email(sample_email_data)

        assert parsed_email["id"] == "123"
        assert parsed_email["thread_id"] == "thread123"
        assert parsed_email["subject"] == "Test Email"
        assert parsed_email["sender"] == "sender@example.com"
        assert parsed_email["labels"] == ["INBOX", "UNREAD"]
        assert parsed_email["body"] == "Test email body"

    @pytest.mark.asyncio
    async def test_fetch_recent_emails_api_error(
        self, mock_gmail_service: Mock
    ) -> None:
        """Test error handling during API calls."""
        # Mock API error
        messages_mock = mock_gmail_service.users.return_value.messages.return_value
        messages_mock.list.return_value.execute.side_effect = Exception("API Error")

        # Test error handling
        with pytest.raises(Exception) as exc_info:
            await self.service.fetch_recent_emails()

        assert str(exc_info.value) == "API Error"

    def test_get_payload_body_with_parts(self) -> None:
        """Test email body extraction from multipart emails."""
        payload = {
            "parts": [
                {
                    "mimeType": "text/plain",
                    "body": {"data": "VGVzdCBlbWFpbCBib2R5"},  # "Test email body"
                }
            ]
        }
        body = self.service.parse_email_body(payload)
        assert body == "Test email body"

    def test_get_payload_body_simple(self) -> None:
        """Test email body extraction from simple emails."""
        payload = {"body": {"data": "VGVzdCBlbWFpbCBib2R5"}}  # "Test email body"
        body = self.service.parse_email_body(payload)
        assert body == "Test email body"

    @pytest.mark.asyncio
    async def test_fetch_recent_emails_with_subject_filter(
        self, mock_gmail_service: Mock
    ) -> None:
        """Test that the query includes the subject filter."""
        messages_mock = mock_gmail_service.users.return_value.messages.return_value
        messages_mock.list.return_value.execute.return_value = {}

        await self.service.fetch_recent_emails(hours=24)

        # クエリパラメータの検証
        list_call_kwargs = messages_mock.list.call_args[1]
        assert "q" in list_call_kwargs
        assert f'subject:"{settings.email_subject_filter}"' in list_call_kwargs["q"]

    def test_parse_email_with_subject_filter(self) -> None:
        """Test email parsing with subject filter."""
        email_data = {
            "id": "123",
            "threadId": "thread123",
            "labelIds": ["INBOX"],
            "payload": {
                "headers": [
                    {"name": "Subject", "value": "The Briefing: Test"},
                    {"name": "From", "value": "test@example.com"},
                    {"name": "Date", "value": "2024-01-13"},
                ],
                "body": {"data": "VGVzdCBlbWFpbCBib2R5"},  # "Test email body"
            },
        }

        parsed_email = self.service.parse_email(email_data)
        assert parsed_email["subject"] == "The Briefing: Test"
