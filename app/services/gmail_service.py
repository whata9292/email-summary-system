"""Gmail service for email fetching and processing."""
import base64
import logging
import os
import pickle
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource, build

logger = logging.getLogger(__name__)


class GmailService:
    """Service class for Gmail API interactions."""

    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

    def __init__(self) -> None:
        """Initialize Gmail service with credentials."""
        self.service: Resource = self._get_gmail_service()

    def _get_gmail_service(self) -> Resource:
        """Get Gmail API service instance."""
        creds = None
        token_path = "token.pickle"

        # Load existing credentials if available
        if os.path.exists(token_path):
            with open(token_path, "rb") as token:
                creds = pickle.load(token)

        # Refresh credentials if expired
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # Create new credentials if none exist
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", self.SCOPES
            )
            creds = flow.run_local_server(port=0)

            # Save credentials for future use
            with open(token_path, "wb") as token:
                pickle.dump(creds, token)

        return build("gmail", "v1", credentials=creds)

    async def fetch_recent_emails(
        self,
        hours: int = 24,
        max_results: int = 100,
        label_ids: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch recent emails from Gmail.

        Args:
            hours: Number of hours to look back
            max_results: Maximum number of emails to fetch
            label_ids: List of Gmail label IDs to filter by

        Returns:
            List of email dictionaries containing parsed email data
        """
        try:
            # Calculate time range
            time_range = datetime.now() - timedelta(hours=hours)
            query = f'after:{time_range.strftime("%Y/%m/%d")}'

            # Prepare request parameters
            params: Dict[str, Any] = {
                "userId": "me",
                "q": query,
                "maxResults": max_results,
            }
            if label_ids:
                params["labelIds"] = label_ids

            # Fetch email list
            results = self.service.users().messages().list(**params).execute()
            messages = results.get("messages", [])

            if not messages:
                logger.info("No emails found in the specified time range")
                return []

            # Fetch full email content
            emails = []
            for message in messages:
                email_data = (
                    self.service.users()
                    .messages()
                    .get(userId="me", id=message["id"], format="full")
                    .execute()
                )

                parsed_email = self._parse_email(email_data)
                emails.append(parsed_email)

            logger.info(f"Successfully fetched {len(emails)} emails")
            return emails

        except Exception as e:
            logger.error(f"Error fetching emails: {str(e)}")
            raise

    def _parse_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse raw email data into a structured format.

        Args:
            email_data: Raw email data from Gmail API

        Returns:
            Dictionary containing parsed email information
        """
        headers = email_data["payload"]["headers"]

        # Extract email metadata
        subject = next(
            (
                header["value"]
                for header in headers
                if header["name"].lower() == "subject"
            ),
            "No Subject",
        )
        sender = next(
            (header["value"] for header in headers if header["name"].lower() == "from"),
            "Unknown Sender",
        )
        date = next(
            (header["value"] for header in headers if header["name"].lower() == "date"),
            "",
        )

        # Extract email body
        body = self._get_email_body(email_data["payload"])

        return {
            "id": email_data["id"],
            "thread_id": email_data["threadId"],
            "subject": subject,
            "sender": sender,
            "date": date,
            "body": body,
            "labels": email_data["labelIds"],
        }

    def _get_email_body(self, payload: Dict[str, Any]) -> str:
        """
        Extract email body from payload.

        Args:
            payload: Email payload data

        Returns:
            Decoded email body text
        """
        if "parts" in payload:
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain":
                    return base64.urlsafe_b64decode(part["body"]["data"]).decode(
                        "utf-8"
                    )
        elif "body" in payload and "data" in payload["body"]:
            return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")

        return ""
