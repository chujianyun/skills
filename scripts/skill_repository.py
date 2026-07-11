"""Discovery and deterministic validation for classified Agent Skills."""

from __future__ import annotations

import json
import re
from pathlib import Path


FRONTMATTER_KEYS = {"name", "description"}
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"][^'\"]{12,}['\"]"),
)
IGNORED_SCAN_PARTS = {".DS_Store", "__pycache__"}


def load_taxonomy(root: Path) -> dict[str, set[str]]:
    """Load the category-to-Skill mapping and reject ambiguous membership."""
    path = root / "config" / "skill-categories.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    categories = data.get("categories")
    if not isinstance(categories, dict) or not categories:
        raise ValueError("Taxonomy must define a non-empty 'categories' object")

    result: dict[str, set[str]] = {}
    owners: dict[str, str] = {}
    for category, definition in categories.items():
        if not isinstance(definition, dict) or not isinstance(definition.get("skills"), list):
            raise ValueError(f"Category '{category}' must define a skills list")
        result[category] = set()
        for skill in definition["skills"]:
            if not isinstance(skill, str) or not skill:
                raise ValueError(f"Category '{category}' contains an invalid Skill name")
            if skill in owners:
                raise ValueError(
                    f"Skill '{skill}' belongs to more than one category: "
                    f"'{owners[skill]}' and '{category}'"
                )
            owners[skill] = category
            result[category].add(skill)
    return result


def discover_skills(root: Path) -> dict[str, Path]:
    """Discover `skills/<category>/<name>/SKILL.md` entries by unique name."""
    skills_root = root / "skills"
    result: dict[str, Path] = {}
    for skill_file in sorted(skills_root.rglob("SKILL.md")):
        relative = skill_file.relative_to(skills_root)
        if len(relative.parts) != 3:
            continue
        name = relative.parts[1]
        skill_dir = skill_file.parent
        if name in result:
            raise ValueError(
                f"Duplicate Skill name '{name}' at '{result[name]}' and '{skill_dir}'"
            )
        result[name] = skill_dir
    return result


def parse_frontmatter(skill_file: Path) -> tuple[dict[str, str], list[str]]:
    """Parse the small YAML subset permitted by this repository."""
    text = skill_file.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, ["SKILL.md must start with YAML frontmatter"]
    try:
        closing = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return {}, ["SKILL.md frontmatter is missing its closing delimiter"]

    values: dict[str, str] = {}
    errors: list[str] = []
    for line in lines[1:closing]:
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"unsupported frontmatter syntax: {line.strip()}")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key in values:
            errors.append(f"duplicate frontmatter key: {key}")
        values[key] = value

    unsupported = sorted(set(values) - FRONTMATTER_KEYS)
    if unsupported:
        errors.append(f"unsupported keys in frontmatter: {', '.join(unsupported)}")
    missing = sorted(FRONTMATTER_KEYS - set(values))
    if missing:
        errors.append(f"missing frontmatter keys: {', '.join(missing)}")
    return values, errors


def _local_reference_errors(skill_file: Path) -> list[str]:
    text = skill_file.read_text(encoding="utf-8")
    errors: list[str] = []
    for raw_target in MARKDOWN_LINK.findall(text):
        target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
        if not target or target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        if any(marker in target for marker in ("<", ">", "{", "}")):
            continue
        path_text = target.split("#", 1)[0]
        if path_text and not (skill_file.parent / path_text).exists():
            errors.append(f"missing local reference: {target}")
    return errors


def _secret_errors(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file() or any(part in IGNORED_SCAN_PARTS for part in path.parts):
            continue
        if path.suffix in {".pyc", ".jpg", ".jpeg", ".png", ".gif", ".pdf"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            errors.append(f"possible secret in {path.relative_to(skill_dir)}")
    return errors


def _marketplace_errors(root: Path, name: str, category: str) -> list[str]:
    path = root / ".claude-plugin" / "marketplace.json"
    try:
        plugins = json.loads(path.read_text(encoding="utf-8")).get("plugins", [])
    except (OSError, json.JSONDecodeError) as exc:
        return [f"marketplace JSON is invalid: {exc}"]
    expected = f"./skills/{category}/{name}"
    matches = [
        plugin
        for plugin in plugins
        if isinstance(plugin, dict) and plugin.get("name") == name
    ]
    if len(matches) != 1:
        return [f"marketplace must contain exactly one plugin named '{name}'"]
    if matches[0].get("skills") != [expected]:
        return [f"marketplace path for '{name}' must be '{expected}'"]
    return []


def validate_skill(root: Path, name: str) -> list[str]:
    """Return deterministic validation errors for one named Skill."""
    root = root.resolve()
    errors: list[str] = []
    try:
        taxonomy = load_taxonomy(root)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return [str(exc)]
    try:
        discovered = discover_skills(root)
    except ValueError as exc:
        return [str(exc)]
    skill_dir = discovered.get(name)
    if skill_dir is None:
        return [f"Skill '{name}' was not found under skills/<category>/<name>"]

    category = skill_dir.parent.name
    if category not in taxonomy:
        errors.append(f"unknown category '{category}' for Skill '{name}'")
    elif name not in taxonomy[category]:
        errors.append(f"Skill '{name}' is not listed in the taxonomy category '{category}'")

    frontmatter, frontmatter_errors = parse_frontmatter(skill_dir / "SKILL.md")
    errors.extend(frontmatter_errors)
    if frontmatter.get("name") and frontmatter["name"] != skill_dir.name:
        errors.append(
            f"frontmatter name '{frontmatter['name']}' does not match directory '{skill_dir.name}'"
        )
    description = frontmatter.get("description", "")
    if description and not re.search(r"(?i)\buse when\b|用于|适用|当用户|触发", description):
        errors.append("description must state when the Skill should be used")

    errors.extend(_local_reference_errors(skill_dir / "SKILL.md"))
    errors.extend(_secret_errors(skill_dir))
    if category in taxonomy:
        errors.extend(_marketplace_errors(root, name, category))

    readme = root / "README.md"
    if readme.exists():
        legacy = re.compile(rf"skills/{re.escape(name)}/SKILL\.md")
        if legacy.search(readme.read_text(encoding="utf-8")):
            errors.append(f"legacy README path remains for Skill '{name}'")
    return errors

