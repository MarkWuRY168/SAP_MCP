# SAP MCP 操作ガイド

このドキュメントでは、SAP MCPプロジェクトの詳細なインストール、設定、使用手順を提供します。

## 目次

1. [前提条件](#前提条件)
2. [SAP Httpインターフェースサービスの有効化](#sap-httpインターフェースサービスの有効化)
3. [手動デプロイ](#手動デプロイ)
4. [使用ガイド](#使用ガイド)
5. [よくある問題](#よくある問題)

---

## 前提条件

- Python 3.8以上
- Git（オプション、リポジトリのクローン用）
- ネットワーク接続（依存関係のインストール用）
- SAPシステム管理者権限

---

## SAP Httpインターフェースサービスの有効化

このプロジェクトをインストールする前に、SAPシステムでHttpインターフェースサービスを有効化する必要があります。以下の手順に従ってください。

### ステップ1：SAPシステムプログラムコードのインポート

SAPリクエストインポートプログラムドキュメントを参照してください：`Request\SAP Request\Y_UPLOAD_TRANSPORT_REQUEST.md`

### ステップ2：SAPリクエストインポートプログラムの実行

SAPリクエストインポートプログラムを実行して、開発パッケージをインポートします。

![SAPリクエストインポート](/Doc/Picture/image-1.png)

### ステップ3：SICFによるZMCPサービスの有効化

トランザクションコードSICFを使用してZMCPサービスを有効化し、サービスが正常に動作しているかテストします。

![SICFサービス有効化](/Doc/Picture/image-2.png)

### ステップ4：トランザクションコードZMCP_CONFIGによるSAPツールリストの設定

トランザクションコードZMCP_CONFIGを使用してSAPツールリストを設定します。

![ツール設定](/Doc/Picture/image-3.png)

SAPツールサンプルデータ：
|MCPツールID|有効フラグ|MCP名|ツール説明|バージョン|タイムアウト（秒）|再試行回数|優先度|カテゴリ|タグ|タイプ|名前|インジケーター|インジケーター|作成者|作成日|作成時間|修正者|修正日|修正時間|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|CHECK_MATNR|X|物料番号チェック|物料番号を入力して返信する|0|10|0|2|MM|MM|FUNC|BAPI_MATERIAL_EXISTENCECHECK|||||0:00:00|||0:00:00|
|GET_MATNR_DETAILS|X|物料詳細取得|物料番号を入力して詳細を取得|0|10|0|2|MM|MM|FUNC|ZMCP_GET_MATNR_DETAILS|||||0:00:00|||0:00:00|
|GET_MATNR_FROM_DES|X|物料番号取得|物料説明と言語を入力|0|10|0|2|MM|MM|FUNC|ZMCP_GET_MATNR_FROM_DES|||||0:00:00|||0:00:00|
|GET_MATNR_WERKS_LIST|X|工場物料リスト取得|工場番号を入力して全ての物料を取得|0|10|0|2|MM|MM|FUNC|ZMCP_GET_WERKS_MATNR_LIST|||||0:00:00|||0:00:00|
|GET_MATNR_WERKS_STOC|X|工場倉庫リスト取得|物料番号と工場番号を入力|0|10|0|2|MM|MM|FUNC|ZMCP_GET_MATNR_WERKS_STOCK|||||0:00:00|||0:00:00|
|GET_PERNR_FROM_DES|X|従業員ID取得|氏名を入力して従業員IDを取得|0|10|0|2|PA|PA|FUNC|ZMCP_GET_PERNR_FROM_DES|||||0:00:00|||0:00:00|
|GET_PERNR_ORG|X|組織情報取得|従業員IDと照会日を入力|0|10|0|2|PA|PA|FUNC|ZMCP_GET_PERNR_ORG|||||0:00:00|||0:00:00|
|GET_PERNR_WORK_PLAN|X|勤務計画取得|従業員IDと年月を入力|0|10|0|2|PT|PT|FUNC|ZMCP_GET_PERNR_WORK_PLAN|||||0:00:00|||0:00:00|
|GET_WERKS_FROM_DES|X|工場番号取得|工場説明を入力して工場番号を取得|0|10|0|2|MM|MM|FUNC|ZMCP_GET_WERKS_FROM_DES|||||0:00:00|||0:00:00|
|REVERSE_MATERIAL|X|物料伝票取消|物料伝票情報を入力して取消|0|10|0|2|MM|MM|FUNC|BAPI_GOODSMVT_CANCEL|||||0:00:00|||0:00:00|
|TOOL_DETAIL|X|ツール詳細|ツール詳細|0|10|0|0|BASE|ABAP|FUNC|ZIDT_FM_MCP_TOOL_DETAIL|X|X|ADMIN||0:00:00|||0:00:00|
|TOOL_LIST|X|ツールリスト|ツールリスト|0|10|0|0|BASE|ABAP|FUNC|ZIDT_FM_MCP_TOOL_LIST|X|X|ADMIN||0:00:00|||0:00:00|
|TOOL_USED|X|ツール使用|ツール使用|0|10|0|0|BASE|ABAP|FUNC|ZIDT_FM_MCP_TOOL_USED|X|X|ADMIN||0:00:00|||0:00:00|

---

## 手動デプロイ

### 1.1 プロジェクトコードの取得

**方法1：Gitリポジトリからクローン**
```bash
git clone https://github.com/MarkWuRY168/SAP_MCP
cd SAP_MCP
```

**方法2：ファイルを直接コピー**
- プロジェクトフォルダ全体をサーバーにコピー

### 1.2 仮想環境の作成

```bash
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 1.3 依存関係のインストール

```bash
# pipのアップグレード
python -m pip install --upgrade pip

# プロジェクトの依存関係のインストール
pip install -r requirements.txt

# プロジェクトのインストール
pip install -e .
```

### 1.4 プロジェクトの設定

```bash
# 設定サンプルファイルのコピー
cp utils/config.example.py utils/config.py

# 設定ファイルの編集（環境に合わせて変更）
# 任意のテキストエディタを使用できます
# notepad config.py      # Windows
# vim config.py          # Linux/Mac
```

**設定ファイル例：**
```python
# SAPインターフェース設定
SAP_CONFIG = {
    "base_url": "http://your-sap-server:port/sap/zmcp",
    "client_id": "your-client-id",
    "sap-user": "your-sap-username",
    "sap-password": "your-sap-password",
    "timeout": 30
}

# MCPサーバー設定
MCP_SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 6688,
    "path": "/mcp"
}

# WEBサーバー設定
WEB_SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 6680,
    "reload": False
}
```

**環境変数設定：**

プロジェクトは環境変数を通じて機密情報を設定することをサポートしており、ハードコードを回避できます。サポートされている環境変数は以下の通りです：

| 環境変数 | 説明 | デフォルト値 |
|---------|------|-----------|
| MCP_HOST | MCPサーバーホスト | 0.0.0.0 |
| MCP_PORT | MCPサーバーポート | 6688 |
| MCP_PATH | MCPサーバーパス | /mcp |
| WEB_HOST | Webサーバーホスト | 0.0.0.0 |
| WEB_PORT | Webサーバーポート | 6680 |
| WEB_RELOAD | Webサーバー自動再読み込み（開発環境） | True |
| SAP_BASE_URL | SAPインターフェースベースURL | - |
| SAP_CLIENT_ID | SAPクライアントID | - |
| SAP_SAP_USER | SAPユーザー名 | - |
| SAP_SAP_PASSWORD | SAPパスワード | - |
| SAP_TIMEOUT | SAPリクエストタイムアウト（秒） | 30 |

サービスを開始する前にこれらの環境変数を設定するか、`.env`ファイルを作成して保存することができます。

### 1.5 サービスの開始

#### 方法1：MCPサーバーのみ開始

```bash
# MCPサーバーの開始
python server/sap_mcp_server.py
```

#### 方法2：Web管理インターフェースの開始

```bash
# Web管理インターフェースの開始
python web/main.py
```

またはuvicornを使用して直接開始：

```bash
# Web管理インターフェースの開始
python -m uvicorn web.main:app --host 0.0.0.0 --port 8080
```

---

## 使用ガイド

### Web管理インターフェースへのアクセス

サービスを開始した後、ブラウザで以下を開きます：`http://localhost:6680`

### サービス管理ページ

1. **サービス状態の表示**：MCPサービスの現在の実行状態を表示
2. **サービスの開始**：「サービス開始」ボタンをクリックしてMCPサーバーを開始
3. **サービスの停止**：「サービス停止」ボタンをクリックしてMCPサーバーを停止
4. **ログの表示**：サービス実行ログをリアルタイムで表示

### ツール管理ページ

1. **ツールリストの表示**：使用可能な全てのSAPツールが左側に表示
2. **ツールの検索**：検索ボックスを使用してツールを迅速に検索
3. **ツール詳細の表示**：ツールリストのツールをクリックすると、右側にツール詳細とパラメータが表示
4. **ツールの実行**：
   - パラメータフォームにパラメータ値を入力
   - 「ツール実行」ボタンをクリック
   - 実行結果を表示

### サーバー設定ページ

1. **SAPインターフェース設定**：
   - ベースURL
   - クライアントID
   - SAPユーザー名
   - SAPパスワード
   - タイムアウト

2. **MCPサーバー設定**：
   - ホストアドレス
   - ポート
   - パス

3. **インターフェーステスト**：「インターフェーステスト」ボタンをクリックしてSAPインターフェース接続を検証

4. **設定の保存**：「設定保存」ボタンをクリックして全ての設定を保存

### ログ表示ページ

1. **ログの更新**：「ログ更新」ボタンをクリックして最新のログを表示
2. **ログレベルフィルタ**：ログレベルを選択してフィルタリング
3. **ログのクリア**：「ログクリア」ボタンをクリックして全てのログをクリア

---

## AIツールの設定

### 対応AIツールタイプ

このサービスは様々なAIツールと統合できます：
- **チャットツール**：ChatGPT、Cherry Studioなど
- **プログラミングツール**：Cursor、Claude Codeなど
- **プラットフォームツール**：LangChain、Difyなど

### MCPサービスアドレスの設定

AIツールでMCPサービスアドレスを以下のように設定します：

```json 
{
  "SAP_MCP": {
    "transport": "streamable_http",
    "url": "http://localhost:6688/mcp"
  }
}
```

---

## よくある問題

### MCPサービスにアクセスできない

**問題**：Web管理インターフェースからMCPサービスを開始した後、外部からアクセスできない。

**解決策**：

1. MCPサーバーで設定されたホストが`0.0.0.0`であることを確認（`127.0.0.1`ではない）
2. ポートマッピングが正しく設定されていることを確認
3. ファイアウォール設定を確認

### 設定ファイルの変更が反映されない

**問題**：設定ファイルを変更した後、サービスが新しい設定を使用していない。

**解決策**：

1. Web管理インターフェースサービスを再起動
2. MCPサービスを停止して再起動

---

## 技術サポート

ご質問がある場合は、以下までお問い合わせください：

- **製品デザイナー**: Mark (Wu Rangyu)
- **開発者**: Mark (Wu Rangyu)
- **電話番号**: 18685095797
- **QQ**: 121980331
- **メール**: 121980331@qq.com
