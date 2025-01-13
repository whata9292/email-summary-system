# Notion テストスニペット

このディレクトリには、Notion APIのテストと機能確認用のスニペットが含まれています。

## 前提条件
- .envファイルに以下の設定が必要です：
  ```
  NOTION_API_KEY=your_api_key_here
  NOTION_DATABASE_ID=your_database_id_here
  ```

## 含まれるスニペット
- `test_database.py`: データベースの基本操作テスト
  - データベースの存在確認
  - エントリの追加
  - エントリの取得
  - エントリの更新

## 使用方法
```bash
# データベーステストの実行
python -m snippets.notion.tests.test_database
```

## テスト用データベース構造
以下の列を持つデータベースを想定しています：
- Email ID (タイトル列)
- Subject (リッチテキスト)
- Sender (リッチテキスト)
- Date (日付)
- Summary (リッチテキスト)
