# Gmail Credentials

このディレクトリには以下のGmail API認証関連ファイルを配置します：

1. `credentials.json`
   - Google Cloud ConsoleからダウンロードするOAuth 2.0クライアントの認証情報
   - このファイルはGitにコミットしません

2. `token.json`
   - OAuth認証後に生成されるアクセストークン情報
   - このファイルはGitにコミットしません

## セットアップ手順

1. Google Cloud Consoleで新しいプロジェクトを作成
2. Gmail APIを有効化
3. OAuth 2.0クライアントIDを作成
4. `credentials.json`をダウンロードし、このディレクトリに配置
5. アプリケーション初回起動時にOAuth認証を実行すると`token.json`が自動生成されます
