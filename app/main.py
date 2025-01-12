import asyncio
import os

from app.config import settings
from app.services.claude_service import ClaudeService
from app.services.gmail_service import GmailService
from app.services.notion_service import NotionService
from app.services.slack_service import SlackService
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class EmailSummarySystem:
    def __init__(self):
        self.gmail_service = GmailService(os.getenv("GMAIL_API_KEY"))
        self.claude_service = ClaudeService(os.getenv("ANTHROPIC_API_KEY"))
        self.notion_service = NotionService(
            os.getenv("NOTION_API_KEY"),
            os.getenv("NOTION_DATABASE_ID")
        )
        self.slack_service = SlackService(
            os.getenv("SLACK_BOT_TOKEN"),
            os.getenv("SLACK_CHANNEL_ID")
        )

    async def process_emails(self):
        """
        メールの取得、サマリー生成、保存、通知を行う
        """
        try:
            # メールの取得
            emails = await self.gmail_service.fetch_emails(
                max_results=settings.EMAIL_MAX_RESULTS
            )
            
            for email in emails:
                # サマリーの生成
                summary = await self.claude_service.generate_summary(
                    email.content,
                    max_length=settings.SUMMARY_MAX_LENGTH
                )
                
                # Notionへの保存
                await self.notion_service.save_summary(email, summary)
                
                # Slack通知
                await self.slack_service.send_notification(
                    subject=email.subject,
                    summary=summary
                )
                
                logger.info(f"Processed email: {email.subject}")

        except Exception as e:
            logger.error(f"Error in process_emails: {str(e)}")
            raise

    async def run(self):
        """
        定期的にメール処理を実行する
        """
        while True:
            try:
                await self.process_emails()
                await asyncio.sleep(settings.EMAIL_FETCH_INTERVAL)
            except Exception as e:
                logger.error(f"Error in run: {str(e)}")
                await asyncio.sleep(60)  # エラー時は1分待機

async def main():
    app = EmailSummarySystem()
    await app.run()

if __name__ == "__main__":
    asyncio.run(main())