# docs/ インデックス（まずここ）

この `docs/` は「会話履歴に頼らず、AIと人が同じ前提で作業する」ための拠点です。

## 何が “正(SSOT)” か
- **不変のルール**: `CLAUDE.md` / `.cursor/rules/*`
- **可変の現在地**: `docs/project-status.md`
- **不変の履歴（検証・意思決定）**: `docs/logs/*`

## まず更新するファイル
- **`docs/project-status.md`**: いまのPhase / Next Actions / Blockers を更新
- **`docs/development-progress.md`**: 開発進捗、現在作業中の部品、完了状況

## 業務理解・進捗管理
- `docs/business-and-system-overview.md`: 業務プロセス、システム部品、全体像（非エンジニア向け）
- `docs/development-progress.md`: 開発進捗トラッカー（今どの部品を作っているか）

## 仕様の置き場所
- `docs/domain.md`: 目的・ユーザー・ユースケース・制約
- `docs/api-contract.md`: APIのI/O例、認証/認可、エラー
- `docs/architecture.md`: 構成・ディレクトリ構造・データフロー
- `docs/glossary.md`: 用語の定義（表記ゆれ防止）

## ログの残し方
- 重要な検証/判断をしたら `docs/logs/YYYY-MM-DD_*.md` を追加
- テンプレ: `docs/logs/YYYY-MM-DD_template.md`
