"""Slack notification service."""
import logging
from typing import Any, Dict

from slack_sdk.web.async_client import AsyncWebClient

from app.utils.error_handler import handle_errors

logger = logging.getLogger(__name__)


class SlackService:
    """Service for sending notifications to Slack."""

    def __init__(self, api_token: str, channel_id: str) -> None:
        """
        Initialize Slack service.

        Args:
            api_token: Slack API token
            channel_id: Target Slack channel ID
        """
        self.client = AsyncWebClient(token=api_token)
        self.channel_id = channel_id

    @handle_errors
    async def send_notification(self, message: str) -> Dict[str, Any]:
        """
        Send a notification to the configured Slack channel.

        Args:
            message: The message to send

        Returns:
            Slack API response
        """
        response = await self.client.chat_postMessage(
            channel=self.channel_id, text=message
        )
        if isinstance(response.data, dict):
            return dict(response.data)
        return {"status": "sent", "raw_response": str(response.data)}
