import json
import tempfile
import unittest
from pathlib import Path

from scripts.record_optimizer_review import skill_digest, write_optimizer_review


class OptimizerReviewTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.skill_dir = self.root / "skills" / "knowledge" / "example-skill"
        self.skill_dir.mkdir(parents=True)
        (self.skill_dir / "SKILL.md").write_text("example\n", encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_digest_is_stable_for_unchanged_files(self):
        first = skill_digest(self.skill_dir)
        second = skill_digest(self.skill_dir)
        self.assertEqual(first, second)
        self.assertEqual(64, len(first))

    def test_digest_changes_when_skill_content_changes(self):
        before = skill_digest(self.skill_dir)
        (self.skill_dir / "SKILL.md").write_text("changed\n", encoding="utf-8")
        self.assertNotEqual(before, skill_digest(self.skill_dir))

    def test_ignored_generated_files_do_not_change_digest(self):
        before = skill_digest(self.skill_dir)
        (self.skill_dir / ".DS_Store").write_bytes(b"generated")
        cache = self.skill_dir / "__pycache__"
        cache.mkdir()
        (cache / "module.pyc").write_bytes(b"generated")
        self.assertEqual(before, skill_digest(self.skill_dir))

    def test_passed_review_writes_required_attestation(self):
        report_path = write_optimizer_review(
            self.root, "example-skill", self.skill_dir, status="passed"
        )
        report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual("example-skill", report["skill"])
        self.assertEqual("knowledge", report["category"])
        self.assertEqual("passed", report["status"])
        self.assertEqual("skill-optimizer", report["reviewer"])
        self.assertEqual(skill_digest(self.skill_dir), report["digest"])
        self.assertRegex(report["reviewed_at"], r"Z$")

    def test_non_passed_review_cannot_create_publishable_report(self):
        with self.assertRaisesRegex(ValueError, "Only a passed"):
            write_optimizer_review(
                self.root, "example-skill", self.skill_dir, status="failed"
            )


if __name__ == "__main__":
    unittest.main()
