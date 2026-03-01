# SAP MCP サーバー

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0+-009688.svg)](https://fastapi.tiangolo.com)

SAPシステムツールをMCPサービスとして公開し、AI機能とSAPシステムの統合ソリューションを提供します

**Languages:** [中文](README_ZH.MD) | [English](README_EN.MD)

</div>

---

## 🚀 プロジェクトの特徴

### コア機能
- **AI主導のツール管理**：AI技術を活用してSAP_MCPツールリストデータを取得・管理し、インテリジェントなツール発見と分類を実現
- **インテリジェントなツール詳細クエリ**：AI能力を活用してツールIDを通じて包括的なツール詳細を取得し、構造化された入力/出力パラメータと使用パターンを提供
- **AI強化ツール実行**：AI主導のデータ変換を適用して入力をSAPが認識可能な形式に変換し、SAP_MCPツールを呼び出して最適化された実行結果を提供

### プロジェクトのメリット
- 一度デプロイすれば長期間使用可能。SAPシステムの設定テーブルでツールリストを管理し、毎回コードを更新する必要がありません

### 機能拡張
- 本サービスは複数のAIツールとの統合を可能にします：
  - チャットツール（例：ChatGPT、Cherry Studio）
  - プログラミングツール（例：Cursor、Claude Code）
  - プラットフォームツール（例：LangChain、Dify）

## 🎨 Web管理インターフェース

### サービス状態管理
- MCPサービス稼働状況のリアルタイム表示
- MCPサービスのワンクリック開始/停止
- サービスログのリアルタイム表示
- ポート占用検出と競合処理

### 設定管理
- SAPシステム設定（Base URL、Client ID、ユーザー名、パスワード、タイムアウト）
- MCPサーバー設定（ホスト、ポート、パス）
- Web管理インターフェース設定（ポート、パス）
- リアルタイム設定ファイル保存
- インターフェース接続テスト機能

### ツール管理
- SAP MCPツールの参照と検索
- ツール詳細とパラメータの表示
- インタラクティブフォームによるツール実行
- インテリジェントなパラメータ解析と表示

### ログ管理
- フィルタオプション付きログ表示
- 確認後ログ削除
- リアルタイムログ更新

### デプロイ方法

詳細なインストール、設定、使用手順については、以下をご参照ください：[操作ガイド](/Doc/USAGE/USAGE_JA.md)

## 🔗 アクセスアドレス

- **Web管理インターフェース**: http://localhost:6680
- **MCPサーバー**: http://localhost:6688/mcp
- **APIドキュメント (Swagger UI)**: http://localhost:6680/docs
- **APIドキュメント (ReDoc)**: http://localhost:6680/redoc
- **ヘルスチェック**: http://localhost:6680/api/health

## 🛡️ セキュリティ

- 設定ファイルを`.gitignore`に追加し、バージョン管理にコミットされないように設定
- 環境変数を通じて機密情報を設定する機能をサポート
- 設定例ファイル`utils/config.example.py`を提供

## 👥 開発者

- **製品デザイナー**: Mark (Wu Rangyu)
- **開発者**: Mark (Wu Rangyu)
- **電話番号**: 18685095797
- **QQ**: 121980331
- **メール**: 121980331@qq.com

## 📄 ライセンス

本プロジェクトは[MITライセンス](LICENSE)の下で提供されています。

---

<div align="center">
  <sub>このプロジェクトがお役に立てば、ぜひ⭐️スターをください！</sub>
</div>
