あなたはリポジトリ初期化の専門家です。提供されたサービス概要に基づき、ドメイン固有ファイルを生成してください。

重要:
- 出力は **JSON 1個のみ**（それ以外の文章は一切出さない）
- あなた自身はファイル作成を実行しない（スクリプト側が書き込みます）
- 既存ファイルがある前提でも、ここでは「最終的にこうあるべき内容」を提示する

入力（サービス概要）:
{service_overview}

生成・更新するファイル（JSONの files に含める）:
1. `.cursor/rules/domain-[サービス名をkebab-case].mdc`
   - front-matter: description
   - globs: ["**/*.ts","**/*.tsx"]（言語が違う場合は概要に合わせて調整）
   - セクション: ビジネスルール、データ設計、API原則、失敗時リカバリ（具体例あり）

2. `docs/domain.md`

3. `docs/api-contract.md`

4. `docs/glossary.md`

出力JSONスキーマ:

```json
{
  "files": [
    {"path": "docs/domain.md", "content": "..."},
    {"path": "docs/api-contract.md", "content": "..."}
  ],
  "summary": {
    "highlights": ["..."],
    "assumptions": ["..."],
    "open_questions": ["..."]
  },
  "next_actions": [
    "..."
  ]
}
```
