#!/usr/bin/env python3
"""Validate a template branch's manifest, identity, registry combination, and required files."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def fail(message: str) -> None:
    raise ValueError(message)


def validate(branch: str, template_dir: Path) -> None:
    if not re.fullmatch(r"[a-z0-9]+-[a-z0-9]+-[a-z0-9]+", branch):
        fail(f"Invalid branch name: {branch!r}. Expected language-framework-type.")

    manifest_path = template_dir / "template.yaml"
    if not manifest_path.is_file():
        fail(f"Missing required file: {manifest_path}")

    manifest = load_yaml(manifest_path)
    if not isinstance(manifest, dict):
        fail("template.yaml must contain a YAML object.")

    schema = __import__("json").loads(
        (ROOT / "schemas" / "template.schema.json").read_text(encoding="utf-8")
    )
    errors = sorted(Draft202012Validator(schema).iter_errors(manifest), key=lambda e: list(e.path))
    if errors:
        details = "; ".join(
            f"{'.'.join(map(str, error.path)) or '<root>'}: {error.message}"
            for error in errors
        )
        fail(f"Manifest schema validation failed: {details}")

    parts = branch.split("-")
    technology = manifest["technology"]
    expected = {
        "id": branch,
        "language": parts[0],
        "framework": parts[1],
        "type": parts[2],
    }
    actual = {
        "id": manifest["template"]["id"],
        "language": technology["language"],
        "framework": technology["framework"],
        "type": technology["type"],
    }
    if actual != expected:
        fail(f"Branch/manifest mismatch. Expected {expected}; found {actual}.")

    languages = load_yaml(ROOT / "registry" / "languages.yaml")["languages"]
    frameworks = load_yaml(ROOT / "registry" / "frameworks.yaml")["frameworks"]
    test_types = load_yaml(ROOT / "registry" / "test-types.yaml")["test_types"]

    language_ids = {item["id"] for item in languages}
    type_ids = {item["id"] for item in test_types}
    if parts[0] not in language_ids:
        fail(f"Unregistered language: {parts[0]}")
    if parts[2] not in type_ids:
        fail(f"Unregistered test type: {parts[2]}")

    allowed = any(
        item["id"] == parts[1]
        and item["language"] == parts[0]
        and parts[2] in item["supported_types"]
        for item in frameworks
    )
    if not allowed:
        fail(f"Unsupported combination: {branch}")

    required_files = ["README.md", ".gitignore"]
    missing = [name for name in required_files if not (template_dir / name).is_file()]
    if missing:
        fail(f"Missing required template files: {', '.join(missing)}")

    entry_point = template_dir / manifest["project"]["entry_point"]
    if not entry_point.exists():
        fail(f"Configured project.entry_point does not exist: {entry_point}")

    print(f"VALID: {branch}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch", required=True, help="Exact template branch name.")
    parser.add_argument(
        "--template-dir",
        type=Path,
        default=Path.cwd(),
        help="Directory containing the checked-out template (default: current directory).",
    )
    args = parser.parse_args()

    try:
        validate(args.branch, args.template_dir.resolve())
    except Exception as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
