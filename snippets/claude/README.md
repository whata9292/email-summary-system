# メール要約システム - Claude スニペット

このディレクトリには、Claude APIを使用したメール要約機能のサンプルコードが含まれています。

## 機能概要
- メール内容のClaudeによる要約生成
- 重要ポイントと優先度の抽出
- アクションアイテムの特定
- 返信案の生成（オプション）

## 前提条件
- 環境変数の設定（既存の.envファイルに設定済み）
- 必要なパッケージのインストール（requirements.txtに含まれる）

## スニペット一覧
- `summarize_email.py`: メール要約の基本実装例
- `advanced_prompts.py`: 様々なユースケース向けのプロンプトテンプレート

## 使用例

```python
from snippets.claude.summarize_email import summarize_with_priorities

email_content = """
Subject: プロジェクト進捗報告
...
"""

summary = await summarize_with_priorities(email_content)
print(summary)
```

## プロジェクト統合のポイント
- app/config.pyの設定を利用
- app/utils/error_handlerを活用したエラーハンドリング
- プロジェクト標準のロギング設定を使用

## 注意事項
- プロンプトのカスタマイズ時は、既存の要約品質を維持すること
- 大量のリクエストを行う場合は、プロジェクトの設定値（MAX_RETRIES等）に注意
