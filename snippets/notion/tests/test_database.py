"""Provides test cases for Notion database integration."""

import asyncio
import os
import sys
from datetime import datetime
from typing import Any, Dict

from dotenv import load_dotenv

# プロジェクトルートディレクトリをPYTHONPATHに追加
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
sys.path.append(project_root)

# .envファイルの読み込み
load_dotenv()

from notion_client import AsyncClient  # noqa: E402


def check_environment() -> None:
    """Verify that required environment variables are set."""
    required_vars = ["NOTION_API_KEY", "NOTION_DATABASE_ID"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )


async def safe_get_property(
    properties: Dict[str, Any], property_name: str, default: str = "N/A"
) -> str:
    """Safely retrieve a property value from Notion properties object."""
    try:
        prop = properties.get(property_name, {})
        if property_name == "Name":
            return prop.get("title", [{}])[0].get("text", {}).get("content", default)
        elif property_name == "ステータス":
            return prop.get("status", {}).get("name", default)
        elif property_name == "URL":
            return prop.get("url", default)
        return default
    except Exception as e:
        print(f"プロパティ {property_name} の取得中にエラー: {str(e)}")
        return default


async def test_database_access() -> None:
    """Test database access and operations."""
    client = AsyncClient(auth=os.getenv("NOTION_API_KEY"))
    database_id = os.getenv("NOTION_DATABASE_ID")

    try:
        # データベース情報の取得
        database = await client.databases.retrieve(database_id=database_id)
        print("\n=== データベース情報 ===")
        print(
            f"データベース名: {database['title'][0]['plain_text'] if database.get('title') else 'Untitled'}"
        )

        # テストデータの作成
        current_time = datetime.now().isoformat()
        test_data = {
            "Name": f"How to test {current_time}",
            "URL": "https://example.com",
            "ステータス": "Unread",
        }

        # エントリの追加
        print("\n=== テストエントリの追加 ===")
        new_page = await client.pages.create(
            parent={"database_id": database_id},
            properties={
                "Name": {"title": [{"text": {"content": test_data["Name"]}}]},
                "URL": {"url": test_data["URL"]},
                "ステータス": {"status": {"name": test_data["ステータス"]}},
            },
        )
        print(f"作成されたエントリID: {new_page['id']}")

        # エントリの取得
        print("\n=== 作成したエントリの確認 ===")
        page = await client.pages.retrieve(page_id=new_page["id"])
        print("タイトル:", await safe_get_property(page["properties"], "Name"))
        print("作成日:", page["created_time"])
        print("ステータス:", await safe_get_property(page["properties"], "ステータス"))
        print("URL:", await safe_get_property(page["properties"], "URL"))

        # エントリの更新
        print("\n=== エントリの更新 ===")
        updated_page = await client.pages.update(
            page_id=new_page["id"],
            properties={"ステータス": {"status": {"name": "Unread"}}},
        )
        print("更新完了:", updated_page["last_edited_time"])

        # データベースのクエリ
        print("\n=== 最近のエントリ一覧 ===")
        query_result = await client.databases.query(
            database_id=database_id,
            sorts=[{"timestamp": "created_time", "direction": "descending"}],
            page_size=5,
        )
        for item in query_result["results"]:
            title = await safe_get_property(item["properties"], "Name")
            status = await safe_get_property(item["properties"], "ステータス")
            print(f"- {title} (ステータス: {status})")

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        raise e


async def main() -> None:
    """Execute the main test suite."""
    try:
        check_environment()
        await test_database_access()
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
