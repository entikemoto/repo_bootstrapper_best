#!/usr/bin/env python3

import importlib.util
import tempfile
import unittest
from unittest import mock
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parent / "init_repo_best.py"
SPEC = importlib.util.spec_from_file_location("init_repo_best", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ExtractFirstJsonPayloadTests(unittest.TestCase):
    def test_extracts_fenced_json_with_braces_in_content(self):
        text = """補足説明があります。

```json
{
  "files": [
    {
      "path": "docs/example.md",
      "content": "# Title\\nJSON sample: { \\"ok\\": true }\\n- item"
    }
  ],
  "summary": {
    "note": "done"
  }
}
```
"""

        payload = MODULE.extract_first_json_payload(text)

        self.assertIsNotNone(payload)
        self.assertEqual(payload["files"][0]["path"], "docs/example.md")
        self.assertIn('JSON sample: { "ok": true }', payload["files"][0]["content"])

    def test_extracts_raw_json_even_with_extra_prose(self):
        text = """以下が結果です。
{
  "files": [
    {
      "path": "CLAUDE.md",
      "content": "line1\\nline2"
    }
  ]
}
以上です。
"""

        payload = MODULE.extract_first_json_payload(text)

        self.assertIsNotNone(payload)
        self.assertEqual(payload["files"][0]["path"], "CLAUDE.md")


class EnsureGitRepoTests(unittest.TestCase):
    def test_skips_when_git_directory_already_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            (cwd / ".git").mkdir()
            with mock.patch.object(MODULE.Path, "cwd", return_value=cwd):
                with mock.patch.object(MODULE.subprocess, "run") as run_mock:
                    MODULE.ensure_git_repo()

            run_mock.assert_not_called()

    def test_runs_git_init_when_repository_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            completed = MODULE.subprocess.CompletedProcess(args=["git", "init"], returncode=0)

            with mock.patch.object(MODULE.Path, "cwd", return_value=cwd):
                with mock.patch.object(MODULE.subprocess, "run", return_value=completed) as run_mock:
                    MODULE.ensure_git_repo()

            run_mock.assert_called_once()
            args, kwargs = run_mock.call_args
            self.assertEqual(args[0], ["git", "init"])
            self.assertEqual(kwargs["stdin"], MODULE.subprocess.DEVNULL)
            self.assertTrue(kwargs["check"])


if __name__ == "__main__":
    unittest.main()
