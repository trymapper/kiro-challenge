---
inclusion: always
---

# AWS認証情報管理

## 重要な注意事項

Kiroがコマンドを実行する際、新しいターミナルセッションが作成されることがあり、その場合AWS認証情報が失われます。

## AWS認証情報の設定

AWSコマンド（aws cli、cdk deployなど）を実行する前に、必ず以下の環境変数が設定されていることを確認してください：

```powershell
$Env:AWS_DEFAULT_REGION="us-west-2"
$Env:AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"
$Env:AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"
$Env:AWS_SESSION_TOKEN="YOUR_SESSION_TOKEN"
```

## 実行時の手順

1. **AWSコマンドを実行する前に**、ユーザーに認証情報が設定されているか確認する
2. 認証情報が設定されていない場合、またはコマンドが認証エラーで失敗した場合は、ユーザーに認証情報の設定を促す
3. 長時間実行されるコマンド（cdk deployなど）の前には、特に注意する

## 認証情報の確認方法

```powershell
# 認証情報が設定されているか確認
echo $Env:AWS_ACCESS_KEY_ID
```

## ベストプラクティス

- **コマンド実行前に認証情報を設定**: 各AWSコマンドの実行前に、同じコマンドで認証情報を設定する
- **セッショントークンの有効期限**: 一時的な認証情報には有効期限があることを認識する
- **エラーハンドリング**: 認証エラーが発生した場合は、ユーザーに認証情報の再設定を促す

## 例

```powershell
# 認証情報を設定してからAWS CLIコマンドを実行
$Env:AWS_DEFAULT_REGION="us-west-2"; $Env:AWS_ACCESS_KEY_ID="..."; $Env:AWS_SECRET_ACCESS_KEY="..."; $Env:AWS_SESSION_TOKEN="..."; aws s3 ls
```

---

**注意**: 認証情報は機密情報です。ログやコードに含めないでください。
