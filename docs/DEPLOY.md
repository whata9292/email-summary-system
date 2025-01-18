# デプロイガイド

## 前提条件

- AWS CLIのインストールと設定
- Dockerのインストール
- 必要なIAM権限の設定

## デプロイ手順

### ローカルからのデプロイ

1. リポジトリをクローン
```bash
git clone https://github.com/whata9292/email-summary-system.git
cd email-summary-system
```

2. デプロイスクリプトに実行権限を付与
```bash
chmod +x deploy.sh
```

3. デプロイの実行
```bash
./deploy.sh
```

### GitHub Actionsによる自動デプロイ

1. 以下のシークレットをGitHubリポジトリに設定
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY

2. mainブランチにプッシュすると自動的にデプロイが実行されます

## 環境変数の設定

1. AWS Secrets Managerでシークレットを設定
```json
{
  "GMAIL_CREDENTIALS": "your-credentials-here",
  "CLAUDE_API_KEY": "your-api-key-here",
  "NOTION_API_KEY": "your-api-key-here",
  "SLACK_WEBHOOK_URL": "your-webhook-url-here"
}
```

## トラブルシューティング

### よくある問題と解決方法

1. ECRへのプッシュ失敗
- AWS認証情報の確認
- ECRリポジトリの存在確認

2. Lambdaのタイムアウト
- タイムアウト設定の確認（現在: 300秒）
- 処理の最適化検討

3. シークレットの取得エラー
- Secrets Managerの設定確認
- IAMロールの権限確認

## モニタリング

- CloudWatch Logsでログを確認
- Lambda関数のメトリクスを監視
- エラー通知の設定