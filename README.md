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

# 開発用パッケージのインストール
pip install pre-commit

# pre-commitフックのインストール
pre-commit install
```

## 開発ワークフロー

1. 新しい機能の開発を始める前に:
   ```bash
   git pull origin main
   git checkout -b feature/your-feature-name
   ```

2. 開発中:
   - コードスタイルはBlackとisortによって自動的にフォーマットされます
   - コミット前にpre-commitフックが実行され、コードの品質チェックが行われます
   - もし変更が必要な場合は自動的に修正されるか、エラーが表示されます

3. テストの実行:
   ```bash
   pytest
   ```

4. 変更のコミット:
   ```bash
   git add .
   git commit -m "feat: Add new feature description"
   ```
   - コミットメッセージは[Conventional Commits](https://www.conventionalcommits.org/)の形式に従ってください

5. プルリクエストの作成:
   - GitHubでプルリクエストを作成
   - CI/CDパイプラインが自動的に実行されます

## コード品質管理

このプロジェクトでは以下のツールを使用しています：

- **Black**: Pythonコードのフォーマット
- **isort**: importの整理
- **flake8**: コードスタイルチェック
- **mypy**: 型チェック
- **pytest**: テスト実行
- **pre-commit**: コミット前の自動チェック

pre-commitは以下のチェックを自動的に実行します：
- ファイル末尾の空白の削除
- ファイル末尾の改行の追加
- YAMLファイルの構文チェック
- 大きなファイルの追加チェック
- Pythonのimport整理
- コードフォーマット
- 型チェック
