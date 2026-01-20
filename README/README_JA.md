# SAP MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## プロジェクト概要

SAP MCP（Model Context Protocol）Serverは、SAPシステムの管理と制御を行うためのプラットフォームであり、ユーザーがSAPシステムと対話するための一連のツールとインターフェースを提供します。

## 機能

### コア機能

1. **ツールリスト管理**：SAP_MCPツールリストデータを取得
2. **ツール詳細クエリ**：ツールIDに基づいてツール詳細を取得（入出力パラメータを含む）
3. **ツール実行**：ツール詳細に基づいてデータを認識可能な形式に変換し、SAP_MCPツールを呼び出して実行結果を取得

### GUI管理インターフェース

1. **サービス状態管理**：
   - MCPサービスの実行状態を表示
   - MCPサービスの開始/停止
   - サービスログのリアルタイム表示
   - ポート占有率検出と競合処理

2. **設定管理**：
   - SAPシステム設定（Base URL、Client ID、ユーザー名、パスワード、タイムアウト）
   - MCPサーバー設定（ホスト、ポート、パス）
   - 設定ファイルのリアルタイム保存

3. **プロジェクト情報表示**：
   - プロジェクト基本情報
   - 開発者情報
   - 製品プロモーションコンテンツ

4. **システムトレイ機能**：
   - システムトレイに最小化
   - バックグラウンドでサービス実行
   - トレイアイコンのツールチップ「SAP_MCP」
   - 右クリックメニューでのクイック操作

## プロジェクト構造

```
SAP_MCP/
├── .gitignore                  # Git無視ファイル
├── LICENSE                     # MITライセンス
├── README.md                   # プロジェクトドキュメント
├── CHANGELOG.md                # 変更ログ
├── pyproject.toml            # プロジェクト設定ファイル
├── requirements.txt           # プロジェクト依存関係
├── config.py                 # 設定ファイル（バージョン管理にコミットしない）
├── config.example.py         # 設定ファイルの例
├── server/                   # サーバーモジュール
│   ├── __init__.py          # パッケージ初期化ファイル
│   ├── sap_mcp_server.py   # MCPサーバー
│   ├── sap_mcp_client.py   # MCPクライアント
│   └── http_client.py      # HTTPクライアント
├── web/                      # Web管理モジュール
│   ├── static/               # 静的ファイル（CSS、JS）
│   ├── templates/            # HTMLテンプレート
│   └── main.py              # Webサーバーエントリーファイル
├── log/                      # ログファイルディレクトリ
└── mcpDemo/                 # MCPサンプルコード
    ├── my_server.py        # サンプルサーバー
    └── my_client.py        # サンプルクライアント
```

## 技術スタック

- **Python**: >= 3.8
- **FastMCP**: MCPプロトコル実装
- **httpx**: HTTPクライアント
- **pydantic**: データ検証と設定管理
- **FastAPI**: Web管理インターフェースフレームワーク
- **Uvicorn**: ASGIサーバー
- **Bootstrap 5**: フロントエンドCSSフレームワーク

## インストール手順

### システム要件

- Python 3.8以上
- SAPシステムアクセス権限

### インストール手順

1. **プロジェクトのクローン**:
   ```bash
   git clone https://github.com/example/sap-mcp.git
   cd SAP_MCP
   ```

2. **仮想環境の作成**（推奨）:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **依存関係のインストール**:
   ```bash
   pip install -r requirements.txt
   ```

4. **アプリケーションの設定**:
   ```bash
   cp config.example.py config.py
   # config.pyを編集して実際の設定情報を入力
   ```

## 設定

### SAPインターフェース設定

`config.py`ファイルでSAPインターフェース情報を設定します：

```python
SAP_CONFIG = {
    "base_url": "http://sap-s4d-app.example.com:8000/sap/zmcp",
    "client_id": "300",
    "sap-user": "YOUR_SAP_USER",
    "sap-password": "YOUR_SAP_PASSWORD",
    "timeout": 30
}
```

### MCPサーバー設定

```python
MCP_SERVER_CONFIG = {
    "host": "127.0.0.1",
    "port": 8000,
    "path": "/mcp"
}
```

## 使用方法

### サービスの開始

#### 方法1：Web管理インターフェースを使用

1. Web管理インターフェースを起動：
   ```bash
   python -m uvicorn web.main:app --reload --host 0.0.0.0 --port 8080
   ```

2. Webブラウザを開き、`http://localhost:8080`にアクセス

3. Webインターフェースで「サービス開始」ボタンをクリック

#### 方法2：コマンドラインで開始

1. MCPサーバーを起動：
   ```bash
   python server/sap_mcp_server.py
   ```

2. サーバーは`http://127.0.0.1:8000/mcp`で実行されます

### Web管理インターフェースの使用

1. **サービス管理ページ**：
   - サービス実行状態の表示
   - サービスの開始/停止
   - サービス設定の確認

2. **ツール管理ページ**：
   - SAP MCPツールの閲覧と検索
   - ツールの詳細とパラメータの表示
   - インタラクティブフォームによるツール実行
   - ツール実行結果の表示

3. **設定ページ**：
   - SAPインターフェース設定の変更
   - MCPサーバー設定の変更
   - 設定変更の保存

4. **ログページ**：
   - フィルタリングオプションを備えたサービスログの表示
   - 確認付きのログクリア
   - リアルタイムログ更新

### クライアント接続例

```python
import asyncio
from fastmcp import Client

async def main():
    client = Client("http://localhost:8000/mcp")
    async with client:
        # ツールリストを取得
        result = await client.call_tool("get_tool_list", {})
        print(result)

asyncio.run(main())
```

### ツール呼び出し例

1. **ツールリストの取得**：
   ```python
   result = await client.call_tool("get_tool_list", {})
   ```

2. **ツール詳細の取得**：
   ```python
   result = await client.call_tool("get_tool_details", {"TOOL_ID": "TOOL_ID"})
   ```

3. **ツールの使用**：
   ```python
   result = await client.call_tool("use_tool", {
       "TOOL_ID": "TOOL_ID",
       "param1": "value1",
       "param2": "value2"
   })
   ```

## 開発ガイド

### コードスタイル

プロジェクトは[PEP 8](https://www.python.org/dev/peps/pep-0008/)コードスタイルガイドラインに従います。

コードのフォーマットとチェックには以下のツールを使用します：

```bash
# コードフォーマット
black .

# コードチェック
flake8 .

# タイプチェック
mypy .
```

### テストの実行

```bash
# すべてのテストを実行
pytest

# テストを実行してカバレッジレポートを生成
pytest --cov=server --cov-report=html
```

### ビルドと公開

```bash
# 配布パッケージのビルド
python -m build

# PyPIに公開
python -m twine upload dist/*
```

## トラブルシューティング

### 一般的な問題

1. **ポート占有率エラー**：
   - ポート8000が他のプログラムで使用されているか確認
   - `config.py`のポート番号を変更

2. **SAPインターフェース接続エラー**：
   - SAPサーバーアドレスが正しいか確認
   - ネットワーク接続を確認
   - ユーザー名とパスワードを確認

3. **Webインターフェースの応答なし**：
   - Webサーバーが正常に実行されているか確認
   - サーバーログのエラーを確認
   - Webサーバーアプリケーションを再起動

## 開発者

- **製品デザイン**：Mark（Wu Rangyu）
- **開発者**：Mark（Wu Rangyu）
- **電話番号**：18685095797
- **QQ**：121980331
- **メール**：121980331@qq.com

## ライセンス

このプロジェクトは[MIT License](LICENSE)の下でライセンスされています。

## 貢献

貢献を歓迎します！以下の手順に従ってください：

1. このプロジェクトをフォーク
2. 機能ブランチを作成（`git checkout -b feature/AmazingFeature`）
3. 変更をコミット（`git commit -m 'Add some AmazingFeature'`）
4. ブランチにプッシュ（`git push origin feature/AmazingFeature`）
5. プルリクエストを開く

## 変更ログ

詳細な変更ログについては、[CHANGELOG.md](CHANGELOG.md)を参照してください。

## サポート

質問や提案がある場合は、以下の方法でお問い合わせください：

- [Issue](https://github.com/example/sap-mcp/issues)を送信
- メール送信：121980331@qq.com

## 謝辞

このプロジェクトに貢献してくれたすべての開発者に感謝します！

---

**注意**：機密情報を含む設定ファイルをバージョン管理システムにコミットしないでください。
