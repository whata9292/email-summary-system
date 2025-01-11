# メールサマリーシステム

Gmailからメールを取得し、Claude APIを使用してサマリーを生成し、Notionデータベースと
Slackに通知するシステムです。

## 機能

- Gmailからのメール取得
- Claude APIを使用したサマリー生成
- Notionデータベースへの保存
- Slack通知

## セットアップ

1. 必要な環境変数を`.env`ファイルに設定
2. 仮想環境の作成とパッケージのインストール
3. Notionデータベースの設定
4. アプリケーションの起動

## 環境変数

必要な環境変数は`.env.example`を参照してください。

## 開発環境のセットアップ

```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
source venv/bin/activate  # Linuxの場合
venv\Scripts\activate    # Windowsの場合

# パッケージのインストール
pip install -r requirements.txt
```