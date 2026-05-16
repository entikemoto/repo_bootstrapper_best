# Repo Bootstrapper (Best)

このフォルダには、非エンジニアでも「要件定義 → 初期リポジトリ作成 → 開発」を迷わず進めるためのツールが入っています。

このツールでできること:
- `spec.md`（あなたの要件メモ）を元に
- `docs/service-overview.md`（サービス概要）を作り
- それをあなたが承認した後にだけ
- `CLAUDE.md` / `.cursor/rules/*` / `docs/*` を生成して、開発のレールを敷きます

特徴:
- **業務プロセスの可視化**: 「現状の業務フロー」と「システムで変える部分」を明確にします
- **システム部品の説明**: 非エンジニアでも「どんな部品で構成されるか」が理解できます
- **開発進捗の追跡**: 「今どこを作っているか」が常にわかります

重要:
- **サービス概要が承認される前に `CLAUDE.md` や `.cursor/rules` は作りません**（事故防止）

---

## 1. まず知っておく用語（ここだけ読めばOK）

- **プロジェクトフォルダ**
  - あなたが作るアプリのフォルダです（例: `~/Projects/my-service/`）
- **プロジェクトルート**
  - プロジェクトフォルダの一番上の階層（例: `my-service/`）
  - コマンドは基本ここで実行します
- **`spec.md`**
  - あなたが用意する「要件メモ」です（長文OK）
- **`docs/service-overview.md`**
  - ツールが作る「サービス概要」です（DRAFT → あなたがAPPROVEDにする）
- **`docs/business-and-system-overview.md`**
  - 「業務プロセス」と「システム部品」を説明するファイルです（開発エージェントと一緒に埋める）
- **`docs/development-progress.md`**
  - 「今どこを作っているか」を追跡するファイルです
- **Claude Code（ターミナルの `claude`）**
  - 司令塔（計画・調査・コマンド実行・次の3つ提案が得意）
- **Cursor（エディタ/チャット）**
  - 実装の手（具体的なファイル編集が得意）
- **Windsurf（このチャット）**
  - 要件/設計/運用の壁打ち（言語化して `docs/*` に落とすのが得意）

---

## 2. 必要なもの（前提）

- Python 3.11+
- Claude Code CLI（`claude`）
  - インストール済み
  - `claude login` 済み

---

## 3. ツール本体の置き場所（推奨）

ツールは「この場所」を正本として固定するのがおすすめです。

```text
/Users/takeshiikemoto/Obsidian Vaults/MainVault/methods/development/repo_bootstrapper_best/
```

理由:
- 手順書（README）とツールが同じ場所にあるので迷いにくい
- Obsidian内で更新・管理しやすい
- 「公式のやり方」を1箇所に固定できる

（任意）コマンドを短くしたい場合:
- `~/Scripts/` にコピー／ショートカットを作ってもOKです（正本はVaultに残すのがおすすめ）

ツールの実体（フルパス）:

```text
/Users/takeshiikemoto/Obsidian Vaults/MainVault/methods/development/repo_bootstrapper_best/init_repo_best.py
```

---

## 4. 使い方（迷わない手順）

ここからは「そのまま順番にやるだけ」です。

### Step 0: プロジェクトフォルダを作る

例:

```bash
mkdir -p ~/Projects/my-service
```

Cursorでこのフォルダを開きます。

### Step 1: `spec.md`（要件メモ）を作る

おすすめの場所はプロジェクト内です。

フォルダ作成とファイル作成を一度に行います（プロジェクトルートで実行）。

```bash
mkdir -p ./specs && cat > ./specs/spec.md << 'EOF'
# サービス要件メモ（ドラフト）

## 1. 目的（何を解決する？）
-

## 2. 対象ユーザー（誰が使う？）
-

## 3. MVPでやること（機能）
-

## 4. MVPでやらないこと（スコープ外）
-

## 5. 代表的な利用シーン（3本）
-

## 6. 制約
- 予算/期限:
- 使う端末（Web/スマホ等）:
- ログイン要否:
- データ/プライバシー:

## 7. 参考（既存サービス、URL、メモ）
-
EOF
```

実行後の構造:

```text
my-service/
  specs/
    spec.md
```

`spec.md` の内容を確認・編集して、要件を埋めてください。

### Step 2: サービス概要（DRAFT）を生成する

「プロジェクトルート（`my-service/`）」で実行します。

このステップで生成されるのは **`docs/service-overview.md` のみ** です。
（`CLAUDE.md` や `.cursor/rules/*` などは、Step 3 で承認した後の Step 4 で生成します）

```bash
python3.11 "/Users/takeshiikemoto/Obsidian Vaults/MainVault/methods/development/repo_bootstrapper_best/init_repo_best.py" \
  --stage overview \
  --spec-file "./specs/spec.md"
```

生成されるファイル:
- `docs/service-overview.md`（DRAFT）

### Step 3: サービス概要を承認する（ここが重要）

`docs/service-overview.md` を開いて、次の2つを必ず行います。

1. `Status: DRAFT` を `Status: APPROVED` に変える
2. 末尾の **承認チェックリスト** をすべて `[x]` にする

この条件を満たさないと、次のステップ（full）は止まります。

### Step 4: 初期リポジトリ雛形を生成する（full）

承認が終わったら、同じくプロジェクトルートで実行します。

```bash
python3.11 "/Users/takeshiikemoto/Obsidian Vaults/MainVault/methods/development/repo_bootstrapper_best/init_repo_best.py" \
  --stage full \
  --spec-file "./specs/spec.md"
```

生成されるもの（例）:
- `CLAUDE.md`（Claude Code の"憲法"）
- `.cursor/rules/*`（Cursorチャットの"憲法"）
- `docs/*`（現在地・仕様・ログの置き場）
- `docs/business-and-system-overview.md`（テンプレート）
- `docs/development-progress.md`（テンプレート）

### Step 5: 業務プロセスとシステム概要を整理する（推奨）

開発を始める前に、Claude Codeと一緒に以下を整理すると、開発がスムーズになります。

```markdown
業務プロセスと構築しようとしているシステム概要を教えてください。
- 現状の業務フロー（Before）
- どこをシステムで変えるのか（After）
- そのためにどんな部品が必要か
```

Claude Codeが説明してくれたら、その内容を `docs/business-and-system-overview.md` に保存してもらいます。

これにより:
- 非エンジニアでも「何を作っているか」が常にわかる
- 開発中に「今どの部品を作っているか」が追跡できる
- 部品完了時に進捗サマリーが自動で提示される

---

## 5.5（任意・おすすめ）ゲート運用を追加する（agentic_dev_os）

このツール（`repo_bootstrapper_best`）は、**プロジェクトの土台作り（初期化）**に最適化されています。  
一方、実装フェーズでは「AIが勝手に進みすぎる/直ったか判断できない/迷走する」事故が起きることがあります。

それを防ぐため、初期化後に **追加レイヤー（オーバーレイ）**として `agentic_dev_os` を導入できます（既存の `CLAUDE.md` や `.cursor/rules/*` は壊さず、追加ファイルで強化します）。

### 追加するもの（最小2ファイル）
- `.cursor/rules/agentic-overlay.mdc`（証拠必須・P0優先・ドリフト対策）
- `docs/agentic-dev-os.md`（運用の正本）

（推奨）さらに最初の成果物として  
- `docs/business-and-system-overview.md` を DRAFT→APPROVED で固める  
（業務→自動化→部品→依存→成功条件→MVPステップ）

### 導入方法（安全：既存は上書きしない）

```bash
python3.11 "/Users/takeshiikemoto/Obsidian Vaults/MainVault/methods/development/agentic_dev_os/scripts/apply_overlay.py" \
  --project-root "/path/to/your-project"
```

詳しい運用は、次を参照してください：
- `/Users/takeshiikemoto/Obsidian Vaults/MainVault/methods/development/agentic_dev_os/README.md`

---

## 6. 開発の進め方（以前の「おすすめで」運用を再現）

迷ったらこれだけ:
- **司令塔は Claude Code**（毎回ここから始める）
- **まず Claude Code に「次の3つ」を出させる**
- 仕様や要件の言語化が必要なら **Windsurf で整理してから Claude Code に渡す**
- 具体的な編集になったら **Cursor に投げる**

受け渡しルール（事故防止）:
- 正（SSOT）は必ずファイル（`CLAUDE.md` / `.cursor/rules/*` / `docs/*`）
- 指示は「次の1アクション」単位で渡す（大きく混ぜない）

### Claude Code（ターミナル）に貼る開始プロンプト

```markdown
あなたはこのプロジェクトの開発エージェントです。

1. まず `CLAUDE.md` を読み、プロジェクトの目的・技術スタック・運用コマンドを把握してください。
2. 次に `docs/project-status.md` を読み、Phase / Next Actions / Blockers を要約してください。
3. 次に着手すべきタスクを **3つ** 提案し、優先度と理由を添えてください。
4. 私は基本的に「おすすめで」と言うので、その場合は最優先案を実行計画に落とし込んで進めてください。
```

### Windsurf（このチャット）に貼る開始プロンプト（要件/設計の整理）

```markdown
いまから要件/設計/運用の整理をしたいです。

1. まず私の要望を「目的 / ユーザー / スコープ / 制約 / 未確定事項」に分解して確認質問をしてください。
2. 合意できたら、更新すべきSSOTファイル（例: `docs/service-overview.md`, `docs/domain.md`, `docs/architecture.md`）を提案してください。
3. 最後に、Claude Code に渡す「次の1アクション指示」を短い文章で作ってください。
```

### Cursor（チャット）に投げるテンプレ（具体編集するとき）

```markdown
次の変更を、最小の差分で実装してください。
変更後に、確認コマンド（Build/Test/Lintなど）も提示してください。

対象ファイル:
- （ファイルパス）

やりたいこと:
- （箇条書き）
```

---

## 7. よくあるトラブル

- `full` が止まる
  - `docs/service-overview.md` が承認されていない可能性があります。
  - `Status: APPROVED` と、チェックリスト全 `[x]` を確認してください。
- `claude` が見つからない
  - Claude Code CLI をインストールして `claude login` まで完了させてください。
- `overview` をやり直したい
  - `--force` を付けると `docs/service-overview.md` を上書きできます。
  - 例: `python3.11 "...init_repo_best.py" --stage overview --spec-file "./specs/spec.md" --force`
