# Event Management API

FastAPI-based REST API backend for managing events with DynamoDB storage.

## 概要

このAPIは、イベント管理システムのバックエンドを提供します。イベントの作成、取得、更新、削除（CRUD操作）をサポートしています。

## 機能

- イベントの作成、取得、更新、削除
- ステータスによるイベントのフィルタリング
- DynamoDBを使用した永続化
- CORS対応
- 入力検証とエラーハンドリング
- AWS Lambda + API Gatewayでのサーバーレスデプロイ

## イベントモデル

各イベントには以下のプロパティがあります：

- `eventId` (string): イベントの一意識別子
- `title` (string): イベントのタイトル
- `description` (string): イベントの説明
- `date` (string): イベントの日付（YYYY-MM-DD形式）
- `location` (string): イベントの場所
- `capacity` (integer): イベントの定員
- `organizer` (string): イベント主催者
- `status` (string): イベントのステータス（active, cancelled, completed）

## ローカル開発

### セットアップ

```bash
pip install -r requirements.txt
```

### 環境変数

```bash
export DYNAMODB_TABLE_NAME=EventsTable
export AWS_DEFAULT_REGION=us-west-2
```

### 実行

```bash
uvicorn main:app --reload
```

APIは http://localhost:8000 で利用可能になります。

## API エンドポイント

### 全イベントを取得

```bash
GET /events
GET /events?status=active
```

**レスポンス例:**
```json
[
  {
    "eventId": "event-123",
    "title": "Tech Conference 2024",
    "description": "Annual technology conference",
    "date": "2024-12-15",
    "location": "Seattle Convention Center",
    "capacity": 500,
    "organizer": "Tech Corp",
    "status": "active"
  }
]
```

### イベントを作成

```bash
POST /events
Content-Type: application/json

{
  "eventId": "event-123",
  "title": "Tech Conference 2024",
  "description": "Annual technology conference",
  "date": "2024-12-15",
  "location": "Seattle Convention Center",
  "capacity": 500,
  "organizer": "Tech Corp",
  "status": "active"
}
```

**レスポンス:** 201 Created

### 特定のイベントを取得

```bash
GET /events/{eventId}
```

**レスポンス:** 200 OK

### イベントを更新

```bash
PUT /events/{eventId}
Content-Type: application/json

{
  "title": "Updated Title",
  "capacity": 600
}
```

**レスポンス:** 200 OK

### イベントを削除

```bash
DELETE /events/{eventId}
```

**レスポンス:** 200 OK

## デプロイ

このAPIはAWS CDKを使用してデプロイされます。詳細は `../infrastructure/README.md` を参照してください。

## ドキュメント

APIドキュメントは `docs/` フォルダに生成されています。

- HTML形式のドキュメント: `docs/main.html`

## テスト

```bash
# ヘルスチェック
curl https://your-api-url.amazonaws.com/prod/health

# イベント一覧取得
curl https://your-api-url.amazonaws.com/prod/events

# イベント作成
curl -X POST https://your-api-url.amazonaws.com/prod/events \
  -H "Content-Type: application/json" \
  -d '{
    "eventId": "test-event-1",
    "title": "Test Event",
    "description": "This is a test event",
    "date": "2024-12-20",
    "location": "Test Location",
    "capacity": 100,
    "organizer": "Test Organizer",
    "status": "active"
  }'
```

## 技術スタック

- **FastAPI**: 高性能なPython Webフレームワーク
- **Pydantic**: データ検証とシリアライゼーション
- **Boto3**: AWS SDK for Python
- **Mangum**: FastAPIをAWS Lambdaで実行するためのアダプター
- **DynamoDB**: NoSQLデータベース
- **API Gateway**: RESTful APIエンドポイント
- **AWS Lambda**: サーバーレスコンピューティング
