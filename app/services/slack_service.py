from slack_sdk.errors import SlackApiError
from slack_sdk.web.async_client import AsyncWebClient

from app.utils.error_handler import handle_errors
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class SlackService:
    def __init__(self, token: str, channel_id: str):
        self.client = AsyncWebClient(token=token)
        self.channel_id = channel_id
        self.logger = logger

    @handle_errors(logger)
    async def send_notification(self, subject: str, summary: str, link: str = None):
        """
        Slackにサマリーを通知する
        """
        try:
            message = f"*新着メール*\n>件名: {subject}\n>サマリー: {summary}"
            if link:
                message += f"\n>リンク: {link}"

            await self.client.chat_postMessage(
                channel=self.channel_id, text=message, unfurl_links=False
            )
        except SlackApiError as e:
            self.logger.error(f"Error sending Slack notification: {str(e)}")
            raise
