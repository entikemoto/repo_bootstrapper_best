あなたはリポジトリ初期化コーチ兼コンテキストエンジニアです。
以下のサービス概要（ドメイン前提）に基づき、共通ルール/ドキュメントを生成してください。

重要:
- 出力は **JSON 1個のみ**（それ以外の文章は一切出さない）
- あなた自身はファイル作成を実行しない（スクリプト側が書き込みます）

入力（サービス概要）:
{service_overview}

生成・更新するファイル（JSONの files に含める）:
1. `CLAUDE.md`
2. `.cursor/rules/core-guidelines.mdc`
3. `.cursor/rules/tech-stack.mdc`（概要の技術スタックに合わせる）
4. `.cursor/rules/security-baseline.mdc`
5. `.cursor/rules/testing-standards.mdc`
6. `.cursor/rules/frontend-style.mdc`
7. `.cursor/rules/backend-architecture.mdc`
8. `docs/project-status.md`
9. `docs/architecture.md`
10. `docs/_INDEX.md`

品質:
- `CLAUDE.md` には Purpose / Tech Stack / Operational Commands(Build/Test/Lint) / Initial Tasks / Key Constraints を含める
- `CLAUDE.md` には必ず **Implementation Gate（実装開始ゲート）** または同等の節を含める
- `CLAUDE.md` には必ず「コスト意識」または同等の節を含め、モデル使い分けを明記する
- `CLAUDE.md` の末尾には必ず「Development Communication Rules（開発時の報告ルール）」セクションを含める（下記参照）
- `CLAUDE.md` には必ず「Task Routing Protocol（司令塔ルーティング）」セクションを含める（下記参照）
- `.cursor/rules/core-guidelines.mdc` と `CLAUDE.md` で矛盾がないようにする

---

`CLAUDE.md` に必ず含める「Implementation Gate（実装開始ゲート）」セクション:

```markdown
## Implementation Gate（実装開始ゲート）

以下が揃っていれば、実装を進めてよい。

1. `docs/business-and-system-overview.md` が作成済みである
2. `docs/development-progress.md` または `docs/project-status.md` に現在地が書かれている

`続けてください` `おすすめで` `お願いします` はすべて実装続行の指示とみなす。
タスクが完了したら次のタスクへ自動で進む。都度確認しない。

### 必ず止まって確認する場合（これだけ）

- 設計の前提が根本から変わるとき
- 取り返しのつかない破壊的操作（データ削除・外部送信など）
- ビルド崩壊・クラッシュ・セキュリティ事故（P0）
- `delete` `rm` `move` `rename` を含む操作（ファイル削除・移動・名前変更）は必ず確認してから実行する
```

---

`CLAUDE.md` の「コスト意識」節に必ず含めるルール:

```markdown
### コスト意識（「正しい意思決定あたりコスト」を最小化する）

最適化目標はトークン単価ではなく「手戻り・事故・誤判断を含めた総コスト」。
安いモデルで誤った設計を選ぶ方が、高いモデルで正しい設計を選ぶより総コストは高い。

- Claude Code の既定モデルは **Sonnet 4.6** とし、通常実装・小修正・テスト修正はそのまま進める
- 仕様策定、アーキテクチャ選定、トレードオフ比較、または 2 回以上修正が空振りした場合は Plan mode + **Opus 4.7** に切り替える
- 広い範囲のコードベース探索は **Haiku 4.5** subagent へ委譲する。ただし最終的な判断は親エージェントが行う
- 設計の穴探し、反証、安全性レビューは `/harden` または Codex 相談を使い、Opus 4.7 単独で確定しない
- 高ステークス領域（医療・決済・認証・個人情報）の設計は Opus 4.7 + `/harden` を必須とする
- 推奨設定: `~/.claude/settings.json` の `"model": "opusplan"` + `"CLAUDE_CODE_SUBAGENT_MODEL": "haiku"`
```

---

`CLAUDE.md` に必ず含める「Development Communication Rules」セクション:

```markdown
---

## Development Communication Rules（開発時の報告ルール）

### 重要ドキュメント
| ファイル | 内容 |
|----------|------|
| `docs/business-and-system-overview.md` | 業務プロセス、システム全体像、部品の説明、依存関係 |
| `docs/development-progress.md` | 開発進捗、現在作業中の部品、完了状況 |

### 依存関係を考慮した開発方針
- **依存関係を最小化**: 各部品はなるべく独立して動作するよう設計する
- **インターフェースで分離**: 部品間は明確なインターフェース（API、型定義）で接続し、実装の詳細に依存しない
- **モック/スタブで並行開発**: 依存先が未完成でも、モックやスタブを使って開発を進める
- **依存関係の明示**: 新しい部品を作る際は、依存関係を `docs/business-and-system-overview.md` に記載する

### 開発セッション開始時
新しい開発セッションを開始する際は、以下を確認・提示すること：
1. `docs/development-progress.md` を読み、現在の進捗を把握
2. これから作業する部品と、それが業務フローのどこに対応するかを簡潔に説明

### 開発の区切り（マイルストーン）での報告
以下のタイミングで進捗サマリーを提示すること：
- 部品を1つ完了したとき
- Phaseを1つ完了したとき
- ユーザーから「進捗を教えて」と聞かれたとき

報告フォーマット：
\```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 進捗サマリー
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【業務フローの対応箇所】
  （業務フローのどこを実装中か）

【部品の進捗】
  [✓] ○○ - 完了
  [→] ○○ - 作業中 ←今ここ
  [ ] ○○ - 未着手

【依存関係】
  今作業中の部品: ○○
  依存先: ○○（完了済み）
  この部品に依存する部品: ○○（この完了後に着手可能）

【完了した作業】
  - ○○○○を実装
  - ○○○○を設定

【次のアクション】
  - ○○○○を実装予定
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
\```

### 進捗ファイルの更新
部品の作業が完了したら、`docs/development-progress.md` を更新すること
```

---

`CLAUDE.md` に必ず含める「Task Routing Protocol（司令塔ルーティング）」セクション:

```markdown
---

## Task Routing Protocol（司令塔ルーティング）

このリポジトリでは **Claude Code（CLI）が司令塔** です。
ユーザーから「こういうことをしたい」と言われたら、まず最初に必ず下記を返してください。

### 1) ルーティング宣言（最初に必ず）
- **担当**: Claude Code / Cursor / Windsurf のどれか
- **理由**: 1〜3行
- **次の1アクション**: 具体的に1つだけ

### 2) Cursor/Windsurf に回す場合は「コピペ用の指示文」を必ず作る

#### Cursor（編集担当）に渡すテンプレ
```markdown
次の変更を、最小差分で実装してください。変更後に確認コマンドも提示してください。

対象ファイル:
- （ファイルパス）

やりたいこと:
- （箇条書き）
```

#### Windsurf（要件/設計/運用の壁打ち）に渡すテンプレ
```markdown
要件/設計/運用を整理したいです。

1) 私の要望を「目的/ユーザー/スコープ/制約/未確定事項」に分解して確認質問してください
2) 更新すべきSSOTファイル（docs/）を提案してください
3) 最後に Claude Code に渡す「次の1アクション指示文」を1つ作ってください
```

### 3) 受け渡しルール（事故防止）
- 正（SSOT）は必ずファイル（`CLAUDE.md` / `.cursor/rules/*` / `docs/*`）
- 指示は「次の1アクション」単位で渡す（大きく混ぜない）
```

出力JSONスキーマ:

```json
{
  "files": [
    {"path": "CLAUDE.md", "content": "..."},
    {"path": ".cursor/rules/core-guidelines.mdc", "content": "..."}
  ],
  "summary": {
    "created_or_updated": ["..."],
    "notes": ["..."]
  }
}
```
