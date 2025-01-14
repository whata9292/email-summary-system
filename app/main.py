"""Main application module."""

import asyncio
import logging
from email.utils import parsedate_to_datetime
from typing import Tuple

from app.config import Settings
from app.models.converters import email_to_notion_data
from app.models.email import EmailData
from app.services.claude_service import ClaudeService
from app.services.gmail_service import GmailService
from app.services.notion_service import NotionService
from app.services.slack_service import SlackService

logger = logging.getLogger(__name__)
settings = Settings()


def initialize_services() -> (
    Tuple[GmailService, ClaudeService, NotionService, SlackService]
):
    """
    Initialize and return service instances.

    Returns:
        Tuple containing initialized service instances
        for Gmail, Claude, Notion, and Slack.
    """
    if not settings.claude_api_key:
        raise ValueError("CLAUDE_API_KEY is required")
    if not settings.notion_api_key or not settings.notion_database_id:
        raise ValueError("NOTION_API_KEY and NOTION_DATABASE_ID are required")
    if not settings.slack_bot_token or not settings.slack_channel_id:
        raise ValueError("SLACK_BOT_TOKEN and SLACK_CHANNEL_ID are required")

    gmail_service = GmailService()
    claude_service = ClaudeService(api_token=settings.claude_api_key)
    notion_service = NotionService(
        api_token=settings.notion_api_key, database_id=settings.notion_database_id
    )
    slack_service = SlackService(
        api_token=settings.slack_bot_token, channel_id=settings.slack_channel_id
    )

    return gmail_service, claude_service, notion_service, slack_service


async def process_emails() -> None:
    """
    Process emails through the email summary pipeline.

    1. Fetch recent emails
    2. Generate summaries using Claude
    3. Store in Notion
    4. Send notifications to Slack
    5. Delete processed emails
    """
    try:
        (
            gmail_service,
            claude_service,
            notion_service,
            slack_service,
        ) = initialize_services()

        # Fetch recent emails
        emails = await gmail_service.fetch_recent_emails(
            hours=settings.email_lookup_hours,
            max_results=settings.max_emails_to_process,
        )

        if not emails:
            logger.info("No new emails to process")
            return

        logger.info("Processing %d emails", len(emails))

        for email in emails:
            try:
                # メール本文のみをClaudeに渡して要約を生成
                summary = await claude_service.generate_summary(email["body"])

                # Gmailの日付文字列をdatetimeに変換
                received_at = parsedate_to_datetime(email["date"])

                # EmailDataモデルを作成
                email_data = EmailData(
                    message_id=email["id"],
                    subject=email["subject"],
                    sender=email["sender"],
                    received_at=received_at,
                    content=summary,
                )

                # NotionServiceのデータ形式に変換
                notion_data = email_to_notion_data(email_data)

                # Notionに保存
                notion_page = await notion_service.add_entry(notion_data)

                # Send Slack notification
                await slack_service.send_notification(
                    f"メール要約が作成されました\n"
                    f"件名: {email_data.subject}\n"
                    f"要約: {email_data.content}\n"
                    f"Notionリンク: {notion_page['url'] if notion_page else 'N/A'}"
                )

                # 処理が完了したメールを削除
                if await gmail_service.delete_email(email["id"]):
                    logger.info("Successfully deleted processed email: %s", email["id"])
                else:
                    logger.warning("Failed to delete email: %s", email["id"])

            except Exception as e:
                logger.error("Error processing email %s: %s", email["id"], str(e))
                continue  # Continue with next email even if current one fails

    except Exception as e:
        logger.error("Error processing emails: %s", str(e))
        raise


async def scheduled_execution() -> None:
    """Execute the email processing task on a scheduled interval."""
    while True:
        try:
            await process_emails()
        except Exception as e:
            logger.error("Error in scheduled execution: %s", str(e))

        await asyncio.sleep(settings.processing_interval_seconds)


def main() -> None:
    """Start the email summary application."""
    try:
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        # Start scheduled execution
        asyncio.run(scheduled_execution())

    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error("Application error: %s", str(e))
        raise


if __name__ == "__main__":
    main()
