---
inclusion: fileMatch
fileMatchPattern: '**/*api*.py|**/main.py|**/routes/**/*.py'
---

# API Standards and Best Practices

このステアリングファイルは、プロジェクト全体で一貫したAPI開発標準を維持するためのガイドラインを提供します。

## REST API規則

### HTTPメソッド

- **GET**: リソースの取得（冪等性あり、副作用なし）
- **POST**: 新しいリソースの作成（201 Createdを返す）
- **PUT**: リソースの完全な更新（200 OKまたは204 No Contentを返す）
- **PATCH**: リソースの部分的な更新（200 OKを返す）
- **DELETE**: リソースの削除（200 OK、204 No Content、または202 Acceptedを返す）

### HTTPステータスコード

#### 成功レスポンス (2xx)
- **200 OK**: リクエスト成功（GET、PUT、PATCH、DELETE）
- **201 Created**: リソース作成成功（POST）
- **204 No Content**: リクエスト成功、レスポンスボディなし

#### クライアントエラー (4xx)
- **400 Bad Request**: 不正なリクエスト（バリデーションエラー）
- **401 Unauthorized**: 認証が必要
- **403 Forbidden**: 認証済みだが権限なし
- **404 Not Found**: リソースが見つからない
- **409 Conflict**: リソースの競合（重複など）
- **422 Unprocessable Entity**: バリデーションエラー（詳細なエラー情報付き）

#### サーバーエラー (5xx)
- **500 Internal Server Error**: サーバー内部エラー
- **503 Service Unavailable**: サービス一時的に利用不可

## JSONレスポンスフォーマット標準

### 成功レスポンス

#### 単一リソース
```json
{
  "id": "resource-123",
  "attribute1": "value1",
  "attribute2": "value2"
}
```

#### リソースリスト
```json
[
  {
    "id": "resource-1",
    "attribute": "value"
  },
  {
    "id": "resource-2",
    "attribute": "value"
  }
]
```

#### ページネーション付きリスト（推奨）
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "pageSize": 20,
  "hasNext": true
}
```

### エラーレスポンス

#### 標準エラーフォーマット
```json
{
  "detail": "エラーメッセージ"
}
```

#### 詳細なエラーフォーマット（バリデーションエラー）
```json
{
  "detail": [
    {
      "loc": ["body", "fieldName"],
      "msg": "フィールドは必須です",
      "type": "value_error.missing"
    }
  ]
}
```

## API設計のベストプラクティス

### エンドポイント命名規則

- **複数形の名詞を使用**: `/events` (良い) vs `/event` (悪い)
- **階層構造**: `/events/{eventId}/attendees`
- **ケバブケース**: `/event-registrations` (推奨) または `/event_registrations`
- **動詞は避ける**: `/events` (良い) vs `/getEvents` (悪い)

### クエリパラメータ

- **フィルタリング**: `?status=active&category=tech`
- **ソート**: `?sort=date&order=desc`
- **ページネーション**: `?page=1&limit=20`
- **検索**: `?search=keyword`

### リクエストボディ

- **JSON形式を使用**
- **camelCaseまたはsnake_caseで一貫性を保つ**
- **必須フィールドと任意フィールドを明確に区別**

### レスポンスヘッダー

- **Content-Type**: `application/json`
- **CORS**: 適切なCORSヘッダーを設定
- **Rate Limiting**: `X-RateLimit-*` ヘッダー（該当する場合）

## FastAPI固有のベストプラクティス

### Pydanticモデル

- **明確なバリデーションルールを定義**
- **Fieldを使用して制約を指定**
- **ドキュメント文字列を追加**

```python
class Event(BaseModel):
    """イベントモデル"""
    eventId: str = Field(..., pattern=r'^[a-zA-Z0-9\-_]+$', description="イベントID")
    title: str = Field(..., min_length=1, max_length=200, description="タイトル")
```

### エンドポイント定義

- **明確なステータスコードを指定**
- **詳細なドキュメント文字列を追加**
- **適切な例外処理を実装**

```python
@app.get("/events/{event_id}", status_code=status.HTTP_200_OK)
async def get_event(event_id: str):
    """
    特定のイベントを取得
    
    Args:
        event_id: イベントID
    
    Returns:
        イベント情報
    
    Raises:
        HTTPException: イベントが見つからない場合（404）
    """
    # 実装
```

### エラーハンドリング

- **HTTPExceptionを使用**
- **適切なステータスコードとメッセージを提供**
- **機密情報を含めない**

```python
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Event with id {event_id} not found"
)
```

## DynamoDB使用時の注意事項

### 予約語の回避

DynamoDBの予約語（status, capacity, date, location など）を属性名として使用する場合は、プレフィックスを追加：

```python
item = {
    'eventId': event.eventId,
    'event_status': event.status,  # 'status'は予約語
    'event_capacity': event.capacity,  # 'capacity'は予約語
    'event_date': event.date,  # 'date'は予約語
}
```

### ExpressionAttributeNames の使用

予約語を使用する場合は、ExpressionAttributeNamesを使用：

```python
table.update_item(
    Key={'eventId': event_id},
    UpdateExpression='SET #status = :status',
    ExpressionAttributeNames={'#status': 'event_status'},
    ExpressionAttributeValues={':status': 'active'}
)
```

## セキュリティのベストプラクティス

- **入力検証を常に実行**
- **SQLインジェクション対策（該当する場合）**
- **機密情報をログに出力しない**
- **適切な認証・認可を実装**
- **CORS設定を適切に制限（本番環境）**

## パフォーマンスのベストプラクティス

- **適切なインデックスを使用**
- **ページネーションを実装**
- **キャッシングを検討**
- **N+1クエリ問題を回避**

## テストのベストプラクティス

- **各エンドポイントのユニットテストを作成**
- **正常系と異常系の両方をテスト**
- **エッジケースをカバー**
- **モックを使用して外部依存を分離**

---

これらの標準に従うことで、一貫性があり、保守しやすく、スケーラブルなAPIを構築できます。
