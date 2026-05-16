# セキュリティチェックリスト

## 目的

OWASP Top 10 を中心に、よくある脆弱性を防ぐ。

---

## コミット前チェック（毎回）

### シークレット管理

- [ ] API キー、パスワードがコードに含まれていない
- [ ] `.env` ファイルが `.gitignore` に含まれている
- [ ] シークレットは環境変数または Secret Manager で管理

### 入力検証

- [ ] ユーザー入力をそのまま使っていない（サニタイズ済み）
- [ ] SQL クエリはパラメータ化されている（SQLi 対策）
- [ ] HTML 出力はエスケープされている（XSS 対策）

---

## PR レビュー時チェック

### 認証・認可

- [ ] 認証が必要なエンドポイントに認証チェックがある
- [ ] 認可チェック（権限確認）が適切に行われている
- [ ] セッション管理が適切（タイムアウト、無効化）

### データ保護

- [ ] 機密データは暗号化されている（保存時、通信時）
- [ ] PII（個人情報）のログ出力を避けている
- [ ] パスワードはハッシュ化されている（bcrypt, Argon2）

### エラーハンドリング

- [ ] エラーメッセージに内部情報を含めていない
- [ ] スタックトレースを本番環境で表示していない
- [ ] 適切なエラーログを記録している

---

## リリース前チェック

### OWASP Top 10 対応

| # | 脆弱性 | 対策 | 確認 |
|---|--------|------|------|
| 1 | Broken Access Control | 認可チェック | [ ] |
| 2 | Cryptographic Failures | 暗号化、HTTPS | [ ] |
| 3 | Injection | パラメータ化、エスケープ | [ ] |
| 4 | Insecure Design | 脅威モデリング | [ ] |
| 5 | Security Misconfiguration | デフォルト無効化、最小権限 | [ ] |
| 6 | Vulnerable Components | 依存関係の更新 | [ ] |
| 7 | Auth Failures | 多要素認証、レート制限 | [ ] |
| 8 | Data Integrity | 署名、検証 | [ ] |
| 9 | Logging Failures | 監査ログ、アラート | [ ] |
| 10 | SSRF | URL 検証、許可リスト | [ ] |

### 依存関係

- [ ] `npm audit` / `pip-audit` / `safety check` を実行
- [ ] 既知の脆弱性がある依存関係を更新
- [ ] 不要な依存関係を削除

### 設定

- [ ] デバッグモードが無効
- [ ] CORS が適切に設定されている
- [ ] セキュリティヘッダーが設定されている（CSP, HSTS など）

---

## 定期チェック（月次）

### 依存関係の更新

```bash
# Python
pip-audit
safety check

# Node.js
npm audit
```

### シークレットのローテーション

- [ ] API キーの有効期限を確認
- [ ] 必要に応じてローテーション

### アクセスログの確認

- [ ] 異常なアクセスパターンがないか
- [ ] 失敗した認証試行が多くないか

---

## インシデント対応

### 発見時

1. 影響範囲を特定
2. 一時的な緩和策を適用（必要なら機能停止）
3. 根本原因を調査
4. 修正をデプロイ
5. Postmortem を作成

### 報告先

- セキュリティチーム / Owner
- 必要に応じて利用者への通知

---

## ツール

### 静的解析

| 言語 | ツール |
|------|--------|
| Python | `bandit`, `safety` |
| JavaScript/TypeScript | `eslint-plugin-security`, `npm audit` |
| 全般 | `semgrep`, `snyk` |

### 動的解析

| 用途 | ツール |
|------|--------|
| Web アプリ | OWASP ZAP, Burp Suite |
| API | Postman (Security tests) |

---

## 参考リンク

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
