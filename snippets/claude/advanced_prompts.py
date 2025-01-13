"""Implements advanced prompts for different email processing scenarios."""

from typing import Any, Dict

from anthropic import Anthropic

from app.config import settings
from app.utils.error_handler import handle_errors

PROMPT_TEMPLATES = {
    "meeting_summary": """
以下の会議関連のメールを分析し、以下の形式で出力してください：

1. 会議概要
   - 日時：
   - 参加者：
   - 目的：

2. 準備事項
   - 必要な資料：
   - 事前確認事項：

3. アジェンダ要点

4. 参加者のアクション
    """,
    "project_update": """
以下のプロジェクト更新メールを分析し、以下の形式で出力してください：

1. プロジェクト状況サマリー（進捗率、全体状況）

2. マイルストーン状況
   - 完了した項目
   - 進行中の項目
   - 遅延している項目

3. リスクと課題
   - 現在の課題
   - 対応策

4. 次のステップ
    """,
    "customer_inquiry": """
以下の問い合わせメールを分析し、以下の形式で出力してください：

1. 問い合わせ内容の要約

2. 優先度判定
   - 緊急度：
   - 影響度：
   - 対応期限：

3. 必要な対応
   - 即時対応事項：
   - 確認が必要な事項：
   - エスカレーション要否：

4. 返信案のポイント
    """,
}


@handle_errors
async def process_with_template(
    email_content: str, template_key: str
) -> Dict[str, Any]:
    """Process emails using a specified template."""
    if template_key not in PROMPT_TEMPLATES:
        return {"success": False, "error": f"Template '{template_key}' not found"}

    client = Anthropic(api_key=settings.claude_api_key)
    prompt = f"{PROMPT_TEMPLATES[template_key]}\n\nメール本文：\n{email_content}"

    message = client.messages.create(
        max_tokens=1024,
        model="claude-3-sonnet-20240229",
        messages=[{"role": "user", "content": prompt}],
    )

    if not message.content or len(message.content) == 0:
        return {"success": False, "error": "No content received"}

    content = message.content[0]
    if not hasattr(content, "text"):
        return {"success": False, "error": "Invalid response format"}

    return {
        "success": True,
        "analysis": content.text,
        "template_used": template_key,
        "usage": message.usage,
    }
