from anthropic import AsyncAnthropic

from app.utils.error_handler import handle_errors
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class ClaudeService:
    def __init__(self, api_key: str):
        self.client = AsyncAnthropic(api_key=api_key)
        self.logger = logger

    @handle_errors(logger)
    async def generate_summary(self, email_content: str, max_length: int = 500) -> str:
        """
        メール本文からサマリーを生成する
        """
        try:
            prompt = f"""
            以下のメール本文から重要なポイントを抽出し、{max_length}文字以内で要約してください：

            {email_content}
            """

            response = await self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content
        except Exception as e:
            self.logger.error(f"Error generating summary: {str(e)}")
            raise