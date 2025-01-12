"""Gmail service for email operations."""

import base64
import logging
import os.path
import pickle
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, cast

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib import flow
from googleapiclient.discovery import Resource, build

from app.utils.error_handler import handle_errors

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


class GmailService:
    """Service for Gmail API operations."""

    def __init__(self) -> None:
        """Initialize Gmail service with authentication."""
        self.creds = self._get_credentials()
        self._service: Resource = build("gmail", "v1", credentials=self.creds)

    def _get_credentials(self) -> Credentials:
        """
        Get or refresh Gmail API credentials.

        Returns:
            Valid credentials for Gmail API access
        """
        creds = None
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow_instance = flow.InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow_instance.run_local_server(port=0)

            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        if not isinstance(creds, Credentials):
            raise ValueError("Failed to obtain valid credentials")

        return creds

    @handle_errors
    async def fetch_recent_emails(
        self,
        hours: int = 24,
        max_results: int = 10,
        label_ids: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch recent emails from Gmail.

        Args:
            hours: How many hours back to look for emails
            max_results: Maximum number of emails to retrieve
            label_ids: Optional list of label IDs to filter by

        Returns:
            List of processed email data
        """
        try:
            query = (
                f"after:{int((datetime.now() - timedelta(hours=hours)).timestamp())}"
            )

            # Cast to Any to handle dynamic attributes of the Gmail service
            gmail_service = cast(Any, self._service)
            messages_service = gmail_service.users().messages()

            response = messages_service.list(
                userId="me",
                q=query,
                maxResults=max_results,
                labelIds=label_ids,
            ).execute()

            messages = response.get("messages", [])
            if not messages:
                logger.info("No emails found")
                return []

            emails = []
            for message in messages:
                try:
                    email_data = messages_service.get(
                        userId="me", id=message["id"], format="full"
                    ).execute()
                    emails.append(self.parse_email(email_data))
                except Exception as e:
                    logger.error("Error processing email %s: %s", message["id"], str(e))

            logger.info("Successfully fetched %d emails", len(emails))
            return emails

        except Exception as e:
            logger.error("Error fetching emails: %s", str(e))
            raise

    def parse_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse raw email data into structured format.

        Args:
            email_data: Raw email data from Gmail API

        Returns:
            Structured email data
        """
        headers = {
            header["name"].lower(): header["value"]
            for header in email_data["payload"]["headers"]
        }

        return {
            "id": email_data["id"],
            "thread_id": email_data["threadId"],
            "labels": email_data.get("labelIds", []),
            "subject": headers.get("subject", ""),
            "sender": headers.get("from", ""),
            "date": headers.get("date", ""),
            "body": self.parse_email_body(email_data["payload"]),
        }

    def parse_email_body(self, payload: Dict[str, Any]) -> str:
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
                    return base64.urlsafe_b64decode(
                        part["body"]["data"].encode("UTF-8")
                    ).decode("UTF-8")
        elif "body" in payload and "data" in payload["body"]:
            return base64.urlsafe_b64decode(
                payload["body"]["data"].encode("UTF-8")
            ).decode("UTF-8")

        return ""
