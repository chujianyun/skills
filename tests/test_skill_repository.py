import json
import tempfile
import unittest
from pathlib import Path

from scripts.skill_repository import discover_skills, load_taxonomy, validate_skill


class SkillRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "config").mkdir()
        (self.root / "skills" / "knowledge").mkdir(parents=True)
        self.write_taxonomy({"knowledge": ["example-skill"]})
        self.write_skill()
        self.write_marketplace("./skills/knowledge/example-skill")
        (self.root / "README.md").write_text(
            "[example](skills/knowledge/example-skill/SKILL.md)\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_taxonomy(self, categories):
        data = {
            "categories": {
                name: {"description": name, "skills": skills}
                for name, skills in categories.items()
            }
        }
        (self.root / "config" / "skill-categories.json").write_text(
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
        skill_dir = self.root / "skills" / "knowledge" / directory
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

    def test_load_taxonomy_rejects_duplicate_membership(self):
        self.write_taxonomy(
            {"knowledge": ["example-skill"], "review": ["example-skill"]}
        )
        with self.assertRaisesRegex(ValueError, "more than one category"):
            load_taxonomy(self.root)

    def test_discovery_rejects_duplicate_skill_names(self):
        duplicate = self.root / "skills" / "review" / "example-skill"
        duplicate.mkdir(parents=True)
        (duplicate / "SKILL.md").write_text("duplicate\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Duplicate Skill"):
            discover_skills(self.root)

    def test_unknown_category_is_reported(self):
        source = self.root / "skills" / "knowledge" / "example-skill"
        target = self.root / "skills" / "misc" / "example-skill"
        target.parent.mkdir()
        source.rename(target)
        errors = validate_skill(self.root, "example-skill")
        self.assertTrue(any("unknown category" in error for error in errors), errors)

    def test_missing_taxonomy_membership_is_reported(self):
        self.write_taxonomy({"knowledge": []})
        errors = validate_skill(self.root, "example-skill")
        self.assertTrue(any("not listed in the taxonomy" in error for error in errors), errors)

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

    def test_marketplace_path_must_match_classified_path(self):
        self.write_marketplace("./skills/example-skill")
        errors = validate_skill(self.root, "example-skill")
        self.assertTrue(any("marketplace" in error for error in errors), errors)

    def test_marketplace_plugin_name_may_differ_from_skill_name(self):
        self.write_marketplace(
            "./skills/knowledge/example-skill", plugin_name="example-skill-bundle"
        )
        self.assertEqual([], validate_skill(self.root, "example-skill"))

    def test_legacy_readme_link_is_reported(self):
        (self.root / "README.md").write_text(
            "[example](skills/example-skill/SKILL.md)\n", encoding="utf-8"
        )
        errors = validate_skill(self.root, "example-skill")
        self.assertTrue(any("legacy README path" in error for error in errors), errors)

    def test_common_secret_pattern_is_reported(self):
        skill_dir = self.root / "skills" / "knowledge" / "example-skill"
        (skill_dir / "secret.txt").write_text(
            "token = sk-abcdefghijklmnopqrstuvwxyz123456\n", encoding="utf-8"
        )
        errors = validate_skill(self.root, "example-skill")
        self.assertTrue(any("possible secret" in error for error in errors), errors)

    def test_sk_substring_inside_identifier_is_not_a_secret(self):
        skill_dir = self.root / "skills" / "knowledge" / "example-skill"
        (skill_dir / "styles.css").write_text(
            ".task-approval-blocked-path { color: red; }\n", encoding="utf-8"
        )
        self.assertEqual([], validate_skill(self.root, "example-skill"))

    def test_absolute_example_output_link_is_not_a_repository_reference(self):
        self.write_skill(body="![output](/Users/example/Downloads/output.png)\n")
        self.assertEqual([], validate_skill(self.root, "example-skill"))


if __name__ == "__main__":
    unittest.main()
