#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
import textwrap


SCRIPT_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = SCRIPT_DIR / "prompts"
TEMPLATES_DIR = SCRIPT_DIR / "templates"

PROMPT_01_OVERVIEW = "01_service_overview.md"
PROMPT_02_DOMAIN = "02_domain_files.md"
PROMPT_03_SCAFFOLD = "03_repo_scaffold.md"


def load_prompt(filename: str) -> str:
    path = PROMPTS_DIR / filename
    if not path.exists():
        print(f"Error: prompt file not found: {path}", file=sys.stderr)
        sys.exit(1)
    return path.read_text(encoding="utf-8")


def extract_first_json_block(text: str) -> str | None:
    # Accept either a fenced block ```json ... ``` or raw JSON.
    m = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"(\{\s*\"files\"\s*:\s*\[.*?\]\s*(?:,\s*\"summary\"\s*:\s*\{.*?\})?\s*\})", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return None


def write_files_from_json(json_text: str, *, created: list[Path]):
    try:
        payload = json.loads(json_text)
    except json.JSONDecodeError as e:
        print("Error: failed to parse JSON from Claude output.", file=sys.stderr)
        print(str(e), file=sys.stderr)
        raise

    files = payload.get("files")
    if not isinstance(files, list):
        print("Error: JSON must include 'files' as a list.", file=sys.stderr)
        raise ValueError("missing_or_invalid_files_list")

    for item in files:
        if not isinstance(item, dict):
            continue
        path = item.get("path")
        content = item.get("content")
        if not isinstance(path, str) or not isinstance(content, str):
            continue
        target = (Path.cwd() / path).resolve()
        if Path.cwd().resolve() not in target.parents and target != Path.cwd().resolve():
            print(f"Error: unsafe path outside project root: {path}", file=sys.stderr)
            raise ValueError(f"unsafe path outside project root: {path}")
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            created.append(target)
        target.write_text(content.rstrip() + "\n", encoding="utf-8")


def run_claude_and_write(prompt: str, *, created: list[Path]):
    def try_once(p: str) -> str:
        out = run_claude(p)
        json_block = extract_first_json_block(out)
        if not json_block:
            raise ValueError("no_json_payload")
        write_files_from_json(json_block, created=created)
        return out

    try:
        return try_once(prompt)
    except Exception:
        # One-time retry: ask for JSON only.
        retry_prompt = (
            prompt
            + "\n\n---\n\n"
            + "出力がJSONとして解釈できませんでした。次は **JSON 1個のみ** を出力してください。"
            + " 余計な文章、Markdown、コードフェンスは不要です。"
        )
        try:
            return try_once(retry_prompt)
        except Exception as e:
            print("Error: failed to obtain valid JSON output from Claude.", file=sys.stderr)
            print(str(e), file=sys.stderr)
            sys.exit(4)



def run_claude(prompt: str) -> str:
    try:
        result = subprocess.run(["claude", "-p", prompt], capture_output=True, text=True, check=True)
        return result.stdout
    except FileNotFoundError:
        print("Error: 'claude' command not found.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print("Claude CLI returned non-zero exit status", file=sys.stderr)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        sys.exit(1)


def ensure_docs_dir() -> Path:
    docs_dir = Path.cwd() / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "logs").mkdir(parents=True, exist_ok=True)
    return docs_dir


def get_service_overview_path() -> Path:
    return Path.cwd() / "docs" / "service-overview.md"


def read_service_overview() -> str | None:
    p = get_service_overview_path()
    if not p.exists():
        return None
    txt = p.read_text(encoding="utf-8").strip()
    return txt if txt else None


def is_overview_approved(text: str) -> bool:
    # Explicit gate for non-engineer workflow.
    # Requirements:
    # - Status: APPROVED
    # - All checklist items in "承認チェックリスト" are checked ([x] / [X]).
    if "Status: APPROVED" not in text:
        return False

    m = re.search(r"##\s*9\.?\s*承認チェックリスト（人間が確認してチェック）\s*(.*)", text, re.DOTALL)
    if not m:
        return False
    checklist_block = m.group(1)
    items = re.findall(r"^\s*-\s*\[(.| )\]\s+.+$", checklist_block, re.MULTILINE)
    if not items:
        return False
    # All must be checked
    for mark in items:
        if mark.lower() != "x":
            return False
    return True


def bootstrap_templates(created: list[Path]):
    # docs
    docs_templates_dir = TEMPLATES_DIR / "docs_templates"
    if docs_templates_dir.exists():
        docs_dir = ensure_docs_dir()
        for tmpl in docs_templates_dir.rglob("*.md"):
            rel = tmpl.relative_to(docs_templates_dir)
            target = docs_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                target.write_text(tmpl.read_text(encoding="utf-8"), encoding="utf-8")
                created.append(target)

    # cursor rules
    rules_templates_dir = TEMPLATES_DIR / "rules_templates"
    if rules_templates_dir.exists():
        rules_dir = Path.cwd() / ".cursor" / "rules"
        rules_dir.mkdir(parents=True, exist_ok=True)
        for tmpl in rules_templates_dir.glob("*.mdc"):
            target = rules_dir / tmpl.name
            if not target.exists():
                target.write_text(tmpl.read_text(encoding="utf-8"), encoding="utf-8")
                created.append(target)

    # dotfiles
    dotfiles_dir = TEMPLATES_DIR / "dotfiles_templates"
    if dotfiles_dir.exists():
        mapping = {
            "gitignore": ".gitignore",
            "env.example": ".env.example",
        }
        for src_name, dest_name in mapping.items():
            src = dotfiles_dir / src_name
            dest = Path.cwd() / dest_name
            if src.exists() and not dest.exists():
                dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
                created.append(dest)


def write_service_overview(text: str, *, force: bool, created: list[Path]) -> Path:
    docs_dir = ensure_docs_dir()
    out = docs_dir / "service-overview.md"
    if out.exists() and not force:
        print(f"[SKIP] {out.relative_to(Path.cwd())} already exists (use --force to overwrite)")
        return out
    out.write_text(textwrap.dedent(text).strip() + "\n", encoding="utf-8")
    created.append(out)
    print(f"[OK] service overview written to {out.relative_to(Path.cwd())}")
    return out


def print_created(created: list[Path]):
    if not created:
        return
    print("=== Created files ===")
    for p in created:
        print(f"- {p.relative_to(Path.cwd())}")


def read_spec_text(spec: str | None, spec_file: str | None) -> str:
    if spec and spec_file:
        print("Error: Use either --spec or --spec-file, not both.", file=sys.stderr)
        sys.exit(2)
    if spec_file:
        p = Path(spec_file).expanduser()
        if not p.exists():
            print(f"Error: spec file not found: {p}", file=sys.stderr)
            sys.exit(2)
        return p.read_text(encoding="utf-8").strip()
    return (spec or "").strip()


def normalize_idea_text(idea: str | None) -> str:
    return (idea or "").strip()


def main():
    parser = argparse.ArgumentParser(description="Init repository (best) with gated service overview")
    parser.add_argument("--idea", required=False, default=None, help="Optional short idea/title")
    parser.add_argument(
        "--spec",
        default=None,
        help="Optional long-form requirements/spec text (recommended to use --spec-file for long content)",
    )
    parser.add_argument(
        "--spec-file",
        default=None,
        help="Optional path to a markdown/text file containing long-form requirements/spec",
    )
    parser.add_argument(
        "--stage",
        choices=["overview", "domain", "full"],
        default="overview",
        help="overview: generate docs/service-overview.md. domain: generate domain docs/rules. full: generate CLAUDE.md + common rules/docs",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite docs/service-overview.md in overview stage")
    parser.add_argument(
        "--allow-unapproved-overview",
        action="store_true",
        help="Allow running domain/full even if docs/service-overview.md is not APPROVED (not recommended)",
    )
    args = parser.parse_args()

    idea_text = normalize_idea_text(args.idea)
    spec_text = read_spec_text(args.spec, args.spec_file)

    if not idea_text and not spec_text:
        print("Error: Provide at least one of --idea, --spec, or --spec-file.", file=sys.stderr)
        sys.exit(2)

    created: list[Path] = []

    if args.stage == "overview":
        ensure_docs_dir()
        raw = load_prompt(PROMPT_01_OVERVIEW)
        prompt = raw.replace("{idea}", idea_text).replace("{spec}", spec_text)
        print(">>> Generating service overview (docs/service-overview.md) ...")
        overview = run_claude(prompt)
        write_service_overview(overview, force=args.force, created=created)
        print_created(created)
        print("=== Overview stage finished ===")
        return

    overview_text = read_service_overview()
    if not overview_text:
        print(
            "Error: docs/service-overview.md not found. Run --stage overview first.",
            file=sys.stderr,
        )
        sys.exit(2)

    if not args.allow_unapproved_overview and not is_overview_approved(overview_text):
        print(
            "Error: docs/service-overview.md is not approved.\n"
            "Edit docs/service-overview.md and set 'Status: APPROVED', then rerun.\n"
            "If you really want to bypass this gate, pass --allow-unapproved-overview.",
            file=sys.stderr,
        )
        sys.exit(3)

    bootstrap_templates(created)

    if args.stage == "domain":
        raw = load_prompt(PROMPT_02_DOMAIN)
        prompt = raw.replace("{service_overview}", overview_text)
        print(">>> Generating domain-specific docs/rules ...")
        run_claude_and_write(prompt, created=created)
        print_created(created)
        print("=== Domain stage finished ===")
        return

    # full
    raw2 = load_prompt(PROMPT_02_DOMAIN)
    prompt2 = raw2.replace("{service_overview}", overview_text)
    print(">>> (1/2) Generating domain-specific docs/rules ...")
    run_claude_and_write(prompt2, created=created)

    raw3 = load_prompt(PROMPT_03_SCAFFOLD)
    prompt3 = raw3.replace("{service_overview}", overview_text)
    print(">>> (2/2) Generating common docs/rules + CLAUDE.md ...")
    run_claude_and_write(prompt3, created=created)

    print_created(created)
    print("=== Full initialization finished ===")


if __name__ == "__main__":
    main()
