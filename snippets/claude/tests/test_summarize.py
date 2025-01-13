"""Provides test cases for Claude summarization features."""

import asyncio
import os
import sys

from dotenv import load_dotenv

# プロジェクトルートディレクトリをPYTHONPATHに追加
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
sys.path.append(project_root)

# .envファイルの読み込み
load_dotenv()

from snippets.claude.advanced_prompts import process_with_template  # noqa: E402
from snippets.claude.summarize_email import summarize_with_priorities  # noqa: E402


def check_environment() -> None:
    """Verify that required environment variables are set."""
    if not os.getenv("CLAUDE_API_KEY"):
        raise EnvironmentError("CLAUDE_API_KEY is not set in .env file")


async def test_basic_summary() -> None:
    """Test basic summarization functionality."""
    email_content = """
    件名：四半期プロジェクトレビュー会議の開催について

    チームの皆様

    来週火曜日14:00より、第2四半期のプロジェクトレビュー会議を開催いたします。

    議題：
    1. 各チームの進捗報告（10分×3チーム）
    2. 課題と解決策の討議（20分）
    3. 次四半期の計画確認（15分）

    準備いただきたいもの：
    - 進捗報告資料（期限：月曜日17:00まで）
    - 課題リスト（担当分）

    場所：会議室A（リモート参加も可）

    よろしくお願いいたします。
    """

    # 基本要約のテスト
    summary_result = await summarize_with_priorities(email_content)
    print("\n=== 基本要約のテスト ===")
    print(summary_result)

    # 会議用テンプレートのテスト
    meeting_result = await process_with_template(email_content, "meeting_summary")
    print("\n=== 会議用テンプレートのテスト ===")
    print(meeting_result)


def main() -> None:
    """Execute the main test suite."""
    try:
        # 環境変数のチェック
        check_environment()
        # テストの実行
        asyncio.run(test_basic_summary())
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")


if __name__ == "__main__":
    main()
