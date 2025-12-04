---
inclusion: always
---

# プロジェクト概要

## プロジェクト構造

このプロジェクトは、イベント管理システムのモノレポです：

```
.
├── backend/              # FastAPI REST APIバックエンド
│   ├── main.py          # メインAPIファイル
│   ├── lambda_handler.py # Lambda用ハンドラー
│   ├── requirements.txt  # Python依存関係
│   └── docs/            # APIドキュメント
├── infrastructure/       # AWS CDK TypeScriptプロジェクト
│   ├── lib/             # CDKスタック定義
│   ├── bin/             # CDKアプリエントリーポイント
│   └── cdk.json         # CDK設定
└── .kiro/               # Kiro設定
    ├── settings/        # MCP設定など
    └── steering/        # ステアリングファイル
```

## 技術スタック

### バックエンド
- **FastAPI 0.115.5**: 高性能Python Webフレームワーク
- **Pydantic 2.10.3**: データ検証
- **boto3 1.35.72**: AWS SDK
- **Mangum 0.19.0**: Lambda用アダプター

### インフラストラクチャ
- **AWS CDK 2.215.0**: Infrastructure as Code
- **TypeScript**: CDKの実装言語
- **DynamoDB**: NoSQLデータベース
- **Lambda**: サーバーレスコンピューティング
- **API Gateway**: RESTful APIエンドポイント

## デプロイ環境

- **リージョン**: us-west-2
- **API URL**: https://ezlgcqjw65.execute-api.us-west-2.amazonaws.com/prod/
- **DynamoDBテーブル**: InfrastructureStack-EventsTableD24865E5-UDPD006R971M

## 開発ワークフロー

### バックエンド開発
1. `backend/`ディレクトリで作業
2. `main.py`でAPIエンドポイントを実装
3. Pydanticモデルでデータ検証
4. DynamoDB予約語に注意

### インフラストラクチャ変更
1. `infrastructure/lib/infrastructure-stack.ts`を編集
2. `npm run build`でビルド
3. `cdk diff`で変更を確認
4. `cdk deploy`でデプロイ

### Git管理
- **リポジトリ**: https://github.com/trymapper/kiro-challenge
- **ブランチ**: main
- コミット前に変更を確認
- 意味のあるコミットメッセージを使用

## 重要な注意事項

### DynamoDB予約語
以下のフィールドはプレフィックス付きで保存：
- `status` → `event_status`
- `capacity` → `event_capacity`
- `date` → `event_date`
- `location` → `event_location`
- `description` → `event_description`

### AWS認証情報
- コマンド実行前に必ず設定
- 新しいターミナルでは再設定が必要
- 有効期限に注意

### コーディング標準
- API標準に従う（api-standards.md参照）
- ドキュメント文字列を追加
- エラーハンドリングを適切に実装
- 型ヒントを使用

## テスト

### ローカルテスト
```bash
# ヘルスチェック
curl https://ezlgcqjw65.execute-api.us-west-2.amazonaws.com/prod/health

# イベント一覧
curl https://ezlgcqjw65.execute-api.us-west-2.amazonaws.com/prod/events
```

### デプロイ後の確認
1. API Gatewayエンドポイントの動作確認
2. DynamoDBテーブルのデータ確認
3. CloudWatch Logsでエラーチェック

## ドキュメント

- **バックエンドREADME**: `backend/README.md`
- **APIドキュメント**: `backend/docs/index.html`
- **インフラREADME**: `infrastructure/README.md`

---

このプロジェクト構造とワークフローに従って、一貫性のある開発を進めてください。
