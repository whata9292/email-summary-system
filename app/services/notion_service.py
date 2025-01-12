from datetime import datetime

from notion_client import AsyncClient

from app.models.email import EmailData
from app.utils.error_handler import handle_errors
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class NotionService:
    def __init__(self, token: str, database_id: str):
        self.client = AsyncClient(auth=token)
        self.database_id = database_id
        self.logger = logger

    @handle_errors(logger)
    async def save_summary(self, email_data: EmailData, summary: str):
        """
        メール情報とサマリーをNotionデータベースに保存する
        """
        try:
            await self.client.pages.create(
                parent={"database_id": self.database_id},
                properties={
                    "Title": {"title": [{"text": {"content": email_data.subject}}]},
                    "From": {"rich_text": [{"text": {"content": email_data.sender}}]},
                    "Received": {"date": {"start": email_data.received_at.isoformat()}},
                    "Summary": {"rich_text": [{"text": {"content": summary}}]},
                    "Status": {"select": {"name": "Processed"}},
                },
            )
        except Exception as e:
            self.logger.error(f"Error saving to Notion: {str(e)}")
            raise
