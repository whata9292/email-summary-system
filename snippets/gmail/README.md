# Gmailテストスニペット

Gmail APIの機能をテストするためのスクリプト集です。

## ファイル構成

1. `test_gmail_auth.py`
   - Gmail認証の基本的なテスト
   - 認証が正常に機能するか確認

2. `fetch_recent_emails.py`
   - 最近のメールを取得するテスト
   - メールのメタデータを表示

3. `analyze_email_structure.py`
   - メールの構造を詳細に分析
   - メッセージの各部分を確認

## セットアップ

1. 仮想環境の作成とパッケージのインストール
   ```bash
   # プロジェクトルートで実行
   python -m venv venv
   source venv/bin/activate  # Unix系
   pip install -r requirements.txt
   ```

2. 環境変数の設定
   - プロジェクトルートの`.env`ファイルに必要な環境変数を設定
   - `.env.example`を参考に作成

3. 認証情報の配置
   - `credentials/gmail/credentials.json` に認証情報を配置

## 実行方法

各スクリプトはプロジェクトルートから実行してください：

```bash
# 認証テスト
python snippets/gmail/test_gmail_auth.py

# メール取得テスト
python snippets/gmail/fetch_recent_emails.py

# メール構造分析
python snippets/gmail/analyze_email_structure.py
```

## トラブルシューティング

1. ModuleNotFoundError
   - プロジェクトルートから実行していることを確認
   - 仮想環境が有効化されていることを確認
   - 必要なパッケージがインストールされていることを確認

2. 認証エラー
   - credentials.jsonが正しく配置されているか確認
   - 環境変数が正しく設定されているか確認
