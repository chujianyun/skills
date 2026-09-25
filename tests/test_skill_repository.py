import json
import tempfile
import unittest
from pathlib import Path

from scripts.skill_repository import discover_skills, load_registry, validate_skill


class SkillRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "config").mkdir()
        (self.root / "skills").mkdir()
        self.write_registry(["example-skill"])
        self.write_skill()
        self.write_marketplace("./skills/example-skill")
        (self.root / "README.md").write_text(
            "[example](skills/example-skill/SKILL.md)\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_registry(self, skills):
        data = {"skills": skills}
        (self.root / "config" / "skills.json").write_text(
            json.dumps(data), encoding="utf-8"
        )

    def write_skill(
        self,
        *,
        directory="example-skill",
        name="example-skill",
        frontmatter_extra="",
        body="# Example\n\nUse [guide](references/guide.md).\n",
    ):
        skill_dir = self.root / "skills" / directory
        (skill_dir / "references").mkdir(parents=True, exist_ok=True)
        (skill_dir / "references" / "guide.md").write_text("guide\n", encoding="utf-8")
        (skill_dir / "SKILL.md").write_text(
            "---\n"
            f"name: {name}\n"
            "description: Use when an example Skill is needed.\n"
            f"{frontmatter_extra}"
            "---\n\n"
            f"{body}",
            encoding="utf-8",
        )
        return skill_dir

    def write_marketplace(self, skill_path, plugin_name="example-skill"):
        plugin = {
            "name": plugin_name,
            "description": "example",
            "source": "./",
            "strict": False,
            "skills": [skill_path],
        }
        path = self.root / ".claude-plugin" / "marketplace.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"plugins": [plugin]}), encoding="utf-8")

    def test_valid_skill_passes(self):
        self.assertEqual([], validate_skill(self.root, "example-skill"))

    def test_load_registry_rejects_duplicate_membership(self):
        self.write_registry(["example-skill", "example-skill"])
        with self.assertRaisesRegex(ValueError, "more than once"):
            load_registry(self.root)

    def test_discovery_ignores_nested_skill_files(self):
        nested = self.root / "skills" / "archive" / "old-skill"
        nested.mkdir(parents=True)
        (nested / "SKILL.md").write_text("nested\n", encoding="utf-8")
        self.assertEqual(["example-skill"], sorted(discover_skills(self.root)))

    def test_missing_registry_membership_is_reported(self):
        self.write_registry(["other-skill"])
        errors = validate_skill(self.root, "example-skill")
        self.assertTrue(any("not listed in the registry" in error for error in errors), errors)

    def test_frontmatter_rejects_extra_keys(self):
        self.write_skill(frontmatter_extra="version: 1\n")
        errors = validate_skill(self.root, "example-skill")
        self.assertTrue(any("unsupported keys" in error for error in errors), errors)

    def test_directory_must_match_frontmatter_name(self):
        self.write_skill(name="different-name")
        errors = validate_skill(self.root, "example-skill")
        self.assertTrue(any("does not match directory" in error for error in errors), errors)

    def test_missing_local_markdown_reference_is_reported(self):
        self.write_skill(body="Use [missing](references/missing.md).\n")
        errors = validate_skill(self.root, "example-skill")
        self.assertTrue(any("missing local reference" in error for error in errors), errors)

    def test_marketplace_path_must_match_flat_path(self):
        self.write_marketplace("./skills/knowledge/example-skill")
        errors = validate_skill(self.root, "example-skill")
        self.assertTrue(any("marketplace" in error for error in errors), errors)

    def test_marketplace_plugin_name_may_differ_from_skill_name(self):
        self.write_marketplace(
            "./skills/example-skill", plugin_name="example-skill-bundle"
        )
        self.assertEqual([], validate_skill(self.root, "example-skill"))

    def test_legacy_readme_link_is_reported(self):
        (self.root / "README.md").write_text(
            "[example](skills/knowledge/example-skill/SKILL.md)\n", encoding="utf-8"
        )
        errors = validate_skill(self.root, "example-skill")
        self.assertTrue(any("legacy README path" in error for error in errors), errors)

    def test_common_secret_pattern_is_reported(self):
        skill_dir = self.root / "skills" / "example-skill"
        (skill_dir / "secret.txt").write_text(
            "token = sk-abcdefghijklmnopqrstuvwxyz123456\n", encoding="utf-8"
        )
        errors = validate_skill(self.root, "example-skill")
        self.assertTrue(any("possible secret" in error for error in errors), errors)

    def test_sk_substring_inside_identifier_is_not_a_secret(self):
        skill_dir = self.root / "skills" / "example-skill"
        (skill_dir / "styles.css").write_text(
            ".task-approval-blocked-path { color: red; }\n", encoding="utf-8"
        )
        self.assertEqual([], validate_skill(self.root, "example-skill"))

    def test_absolute_example_output_link_is_not_a_repository_reference(self):
        self.write_skill(body="![output](/Users/example/Downloads/output.png)\n")
        self.assertEqual([], validate_skill(self.root, "example-skill"))


if __name__ == "__main__":
    unittest.main()
