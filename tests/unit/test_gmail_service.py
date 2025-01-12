"""Unit tests for Gmail Service."""
import pytest
import pickle
from datetime import datetime
from unittest.mock import Mock, patch, mock_open
from app.services.gmail_service import GmailService


@pytest.fixture
def mock_credentials():
    """Mock Gmail credentials."""
    creds = Mock()
    creds.expired = False
    return creds


@pytest.fixture
def mock_gmail_service():
    """Mock Gmail API service."""
    service = Mock()
    service.users().messages().list().execute.return_value = {
        'messages': [
            {'id': '123', 'threadId': 'thread123'},
            {'id': '456', 'threadId': 'thread456'}
        ]
    }
    return service


@pytest.fixture
def sample_email_data():
    """Sample email data for testing."""
    return {
        'id': '123',
        'threadId': 'thread123',
        'labelIds': ['INBOX', 'UNREAD'],
        'payload': {
            'headers': [
                {'name': 'Subject', 'value': 'Test Email'},
                {'name': 'From', 'value': 'sender@example.com'},
                {'name': 'Date', 'value': 'Wed, 1 Jan 2025 10:00:00 +0000'}
            ],
            'body': {
                'data': 'VGVzdCBlbWFpbCBib2R5'  # Base64 encoded "Test email body"
            }
        }
    }


class TestGmailService:
    """Test cases for GmailService class."""

    @pytest.fixture(autouse=True)
    def setup(self, mock_credentials, mock_gmail_service):
        """Setup test cases."""
        with patch('pickle.load', return_value=mock_credentials), \
             patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open()), \
             patch('app.services.gmail_service.build', return_value=mock_gmail_service):
            self.service = GmailService()

    @pytest.mark.asyncio
    async def test_fetch_recent_emails_success(self, mock_gmail_service, sample_email_data):
        """Test successful email fetching."""
        # Mock the get() method for individual email fetching
        mock_gmail_service.users().messages().get().execute.return_value = sample_email_data

        # Test email fetching
        emails = await self.service.fetch_recent_emails(hours=24, max_results=2)

        # Verify results
        assert len(emails) == 2
        assert emails[0]['id'] == '123'
        assert emails[0]['subject'] == 'Test Email'
        assert emails[0]['sender'] == 'sender@example.com'

        # Verify API calls
        mock_gmail_service.users().messages().list.assert_called_once()
        assert mock_gmail_service.users().messages().get.call_count == 2

    @pytest.mark.asyncio
    async def test_fetch_recent_emails_no_results(self, mock_gmail_service):
        """Test when no emails are found."""
        # Mock empty results
        mock_gmail_service.users().messages().list().execute.return_value = {}

        # Test email fetching
        emails = await self.service.fetch_recent_emails()

        # Verify results
        assert len(emails) == 0
        mock_gmail_service.users().messages().get.assert_not_called()

    @pytest.mark.asyncio
    async def test_fetch_recent_emails_with_labels(self, mock_gmail_service, sample_email_data):
        """Test email fetching with specific labels."""
        mock_gmail_service.users().messages().get().execute.return_value = sample_email_data
        
        # Test email fetching with labels
        emails = await self.service.fetch_recent_emails(
            label_ids=['INBOX', 'UNREAD']
        )

        # Verify label parameter was passed
        list_call_kwargs = mock_gmail_service.users().messages().list.call_args[1]
        assert 'labelIds' in list_call_kwargs
        assert list_call_kwargs['labelIds'] == ['INBOX', 'UNREAD']

    def test_parse_email(self, sample_email_data):
        """Test email parsing functionality."""
        parsed_email = self.service._parse_email(sample_email_data)

        assert parsed_email['id'] == '123'
        assert parsed_email['thread_id'] == 'thread123'
        assert parsed_email['subject'] == 'Test Email'
        assert parsed_email['sender'] == 'sender@example.com'
        assert parsed_email['labels'] == ['INBOX', 'UNREAD']
        assert parsed_email['body'] == 'Test email body'

    @pytest.mark.asyncio
    async def test_fetch_recent_emails_api_error(self, mock_gmail_service):
        """Test handling of API errors."""
        # Mock API error
        mock_gmail_service.users().messages().list().execute.side_effect = Exception("API Error")

        # Test error handling
        with pytest.raises(Exception) as exc_info:
            await self.service.fetch_recent_emails()

        assert str(exc_info.value) == "API Error"

    def test_get_email_body_with_parts(self):
        """Test email body extraction from multipart email."""
        payload = {
            'parts': [
                {
                    'mimeType': 'text/plain',
                    'body': {'data': 'VGVzdCBlbWFpbCBib2R5'}  # "Test email body"
                }
            ]
        }
        body = self.service._get_email_body(payload)
        assert body == 'Test email body'

    def test_get_email_body_simple(self):
        """Test email body extraction from simple email."""
        payload = {
            'body': {'data': 'VGVzdCBlbWFpbCBib2R5'}  # "Test email body"
        }
        body = self.service._get_email_body(payload)
        assert body == 'Test email body'
