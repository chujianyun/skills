import json
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.publish_skill import PublishError, publish_skill
from scripts.record_optimizer_review import write_optimizer_review


class PublishSkillTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.skill_dir = self.root / "skills" / "knowledge" / "example-skill"
        self.skill_dir.mkdir(parents=True)
        (self.root / "config").mkdir()
        (self.root / ".claude-plugin").mkdir()
        (self.skill_dir / "SKILL.md").write_text(
            "---\n"
            "name: example-skill\n"
            "description: Use when an example Skill is needed.\n"
            "---\n\n"
            "# Example\n",
            encoding="utf-8",
        )
        taxonomy = {
            "categories": {
                "knowledge": {
                    "description": "knowledge",
                    "skills": ["example-skill"],
                }
            }
        }
        (self.root / "config" / "skill-categories.json").write_text(
            json.dumps(taxonomy), encoding="utf-8"
        )
        marketplace = {
            "plugins": [
                {
                    "name": "example-skill",
                    "description": "example",
                    "source": "./",
                    "strict": False,
                    "skills": ["./skills/knowledge/example-skill"],
                }
            ]
        }
        (self.root / ".claude-plugin" / "marketplace.json").write_text(
            json.dumps(marketplace), encoding="utf-8"
        )
        (self.root / "README.md").write_text(
            "[example](skills/knowledge/example-skill/SKILL.md)\n",
            encoding="utf-8",
        )
        self.publisher = self.root / "publisher"
        self.write_publisher("#!/bin/sh\nprintf '%s\\n' \"$@\" > publisher.log\n")

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_publisher(self, body):
        self.publisher.write_text(body, encoding="utf-8")
        self.publisher.chmod(self.publisher.stat().st_mode | stat.S_IXUSR)

    def write_report(self):
        return write_optimizer_review(
            self.root, "example-skill", self.skill_dir, status="passed"
        )

    def init_git(self, branch="codex/test"):
        subprocess.run(
            ["git", "init", "-b", branch], cwd=self.root, check=True, capture_output=True
        )
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test"], cwd=self.root, check=True
        )
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-m", "baseline"],
            cwd=self.root,
            check=True,
            capture_output=True,
        )

    def commit_count(self):
        return subprocess.run(
            ["git", "rev-list", "--count", "HEAD"],
            cwd=self.root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    def test_missing_market_adapter_stops_immediately(self):
        with self.assertRaisesRegex(PublishError, "SKILLS_MARKET_PUBLISHER"):
            publish_skill(self.root, "example-skill", publisher=None, no_git=True)

    def test_stale_optimizer_digest_is_rejected(self):
        report = self.write_report()
        (self.skill_dir / "SKILL.md").write_text("changed\n", encoding="utf-8")
        with self.assertRaisesRegex(PublishError, "stale"):
            publish_skill(
                self.root,
                "example-skill",
                publisher=str(self.publisher),
                report_path=report,
                no_git=True,
            )

    def test_deterministic_validation_failure_prevents_market_upload(self):
        report = self.write_report()
        (self.root / ".claude-plugin" / "marketplace.json").write_text(
            json.dumps({"plugins": []}), encoding="utf-8"
        )
        with self.assertRaisesRegex(PublishError, "validation failed"):
            publish_skill(
                self.root,
                "example-skill",
                publisher=str(self.publisher),
                report_path=report,
                no_git=True,
            )
        self.assertFalse((self.root / "publisher.log").exists())

    def test_market_failure_does_not_create_git_commit(self):
        self.write_publisher("#!/bin/sh\nexit 7\n")
        self.init_git()
        report = self.write_report()
        before = self.commit_count()
        with self.assertRaisesRegex(PublishError, "market upload failed"):
            publish_skill(
                self.root,
                "example-skill",
                publisher=str(self.publisher),
                report_path=report,
                no_git=False,
            )
        self.assertEqual(before, self.commit_count())

    def test_main_branch_is_forbidden_before_market_upload(self):
        self.init_git(branch="main")
        report = self.write_report()
        with self.assertRaisesRegex(PublishError, "main"):
            publish_skill(
                self.root,
                "example-skill",
                publisher=str(self.publisher),
                report_path=report,
                no_git=False,
            )
        self.assertFalse((self.root / "publisher.log").exists())

    def test_dirty_unrelated_file_is_rejected(self):
        self.init_git()
        (self.skill_dir / "SKILL.md").write_text(
            (self.skill_dir / "SKILL.md").read_text(encoding="utf-8") + "\nChanged.\n",
            encoding="utf-8",
        )
        report = self.write_report()
        (self.root / "unrelated.txt").write_text("do not stage\n", encoding="utf-8")
        with self.assertRaisesRegex(PublishError, "unrelated"):
            publish_skill(
                self.root,
                "example-skill",
                publisher=str(self.publisher),
                report_path=report,
                no_git=False,
            )
        self.assertFalse((self.root / "publisher.log").exists())

    def test_successful_no_git_run_invokes_market_with_contract(self):
        report = self.write_report()
        publish_skill(
            self.root,
            "example-skill",
            publisher=str(self.publisher),
            report_path=report,
            no_git=True,
        )
        arguments = (self.root / "publisher.log").read_text(encoding="utf-8").splitlines()
        self.assertEqual(
            [
                "--skill-dir",
                str(self.skill_dir.resolve()),
                "--name",
                "example-skill",
                "--category",
                "knowledge",
            ],
            arguments,
        )


if __name__ == "__main__":
    unittest.main()
