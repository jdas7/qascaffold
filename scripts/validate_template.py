#!/usr/bin/env python3
"""Validate published template branches from the governance checkout."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
BRANCH_NAME = re.compile(r"^[a-z0-9]+-[a-z0-9]+-[a-z0-9]+$")
GOVERNANCE_BRANCHES = {"master", "main"}
REQUIRED_FILES = ("README.md", ".gitignore")


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def fail(message: str) -> None:
    raise ValueError(message)


def git(args: list[str], check: bool = False) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if check and completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "git command failed").strip()
        fail(detail)
    return completed


def fetch_origin() -> None:
    git(["fetch", "origin", "--prune"], check=True)


def origin_has_branch(branch: str) -> bool:
    completed = git(["rev-parse", "--verify", "--quiet", f"refs/remotes/origin/{branch}"])
    return completed.returncode == 0 and bool(completed.stdout.strip())


def resolve_ref(branch: str) -> str | None:
    for ref in (f"origin/{branch}", branch):
        completed = git(["rev-parse", "--verify", "--quiet", ref])
        if completed.returncode == 0 and completed.stdout.strip():
            return ref
    return None


def remote_template_branches() -> set[str]:
    completed = git(
        ["for-each-ref", "--format=%(refname:short)", "refs/remotes/origin"],
        check=True,
    )
    names: set[str] = set()
    for line in completed.stdout.splitlines():
        short = line.strip()
        if not short.startswith("origin/"):
            continue
        branch = short.split("/", 1)[1]
        if branch in GOVERNANCE_BRANCHES or branch == "HEAD":
            continue
        if BRANCH_NAME.fullmatch(branch):
            names.add(branch)
    return names


def ref_path_exists(ref: str, path: str) -> bool:
    relative = path.strip().replace("\\", "/")
    while relative.startswith("./"):
        relative = relative[2:]
    relative = relative.rstrip("/")
    if not relative:
        return False
    completed = git(["ls-tree", "--name-only", ref, relative])
    return completed.returncode == 0 and bool(completed.stdout.strip())


def read_manifest(ref: str) -> dict:
    completed = git(["show", f"{ref}:template.yaml"])
    if completed.returncode != 0:
        fail(f"Missing required file: template.yaml on {ref}")
    manifest = yaml.safe_load(completed.stdout)
    if not isinstance(manifest, dict):
        fail(f"template.yaml on {ref} must contain a YAML object.")
    return manifest


def load_registered_templates() -> list[dict]:
    document = load_yaml(ROOT / "registry" / "templates.yaml")
    if not isinstance(document, dict) or not isinstance(document.get("templates"), list):
        fail("registry/templates.yaml must contain a templates list.")
    templates = document["templates"]
    seen: set[str] = set()
    for item in templates:
        if not isinstance(item, dict):
            fail("Each registry/templates.yaml entry must be an object.")
        branch = item.get("id")
        if not isinstance(branch, str) or not BRANCH_NAME.fullmatch(branch):
            fail(f"Invalid registered template id: {branch!r}.")
        if branch in seen:
            fail(f"Duplicate registered template: {branch}")
        seen.add(branch)
        parts = branch.split("-")
        actual = (item.get("language"), item.get("framework"), item.get("type"))
        if actual != tuple(parts):
            fail(
                f"Registered identity for {branch} must be "
                f"language={parts[0]}, framework={parts[1]}, type={parts[2]}."
            )
    return templates


def combination_allowed(language: str, framework: str, test_type: str) -> bool:
    languages = load_yaml(ROOT / "registry" / "languages.yaml")["languages"]
    frameworks = load_yaml(ROOT / "registry" / "frameworks.yaml")["frameworks"]
    test_types = load_yaml(ROOT / "registry" / "test-types.yaml")["test_types"]
    language_ids = {item["id"] for item in languages}
    type_ids = {item["id"] for item in test_types}
    if language not in language_ids or test_type not in type_ids:
        return False
    return any(
        item["id"] == framework
        and item["language"] == language
        and test_type in item["supported_types"]
        for item in frameworks
    )


def validate_branch(branch: str) -> None:
    if branch in GOVERNANCE_BRANCHES or not BRANCH_NAME.fullmatch(branch):
        fail(f"Invalid branch name: {branch!r}. Expected language-framework-type.")

    registered = {item["id"]: item for item in load_registered_templates()}
    if branch not in registered:
        fail(f"Unregistered template branch: {branch}")

    parts = branch.split("-")
    if not combination_allowed(parts[0], parts[1], parts[2]):
        fail(f"Unsupported combination: {branch}")

    ref = resolve_ref(branch)
    if ref is None:
        fail(f"Branch {branch!r} does not exist locally or on origin.")

    manifest = read_manifest(ref)
    schema = json.loads((ROOT / "schemas" / "template.schema.json").read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(manifest), key=lambda error: list(error.path))
    if errors:
        details = "; ".join(
            f"{'.'.join(map(str, error.path)) or '<root>'}: {error.message}"
            for error in errors
        )
        fail(f"Manifest schema validation failed: {details}")

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

    missing = [name for name in REQUIRED_FILES if not ref_path_exists(ref, name)]
    if missing:
        fail(f"Missing required template files on {ref}: {', '.join(missing)}")

    entry_point = manifest["project"]["entry_point"]
    if not ref_path_exists(ref, entry_point):
        fail(f"Configured project.entry_point does not exist on {ref}: {entry_point}")

    print(f"VALID: {branch}")


def validate_registered(branch: str | None) -> None:
    templates = load_registered_templates()
    registered_ids = {item["id"] for item in templates}
    targets = [branch] if branch else [item["id"] for item in templates]

    if branch is None:
        unknown = sorted(remote_template_branches() - registered_ids)
        if unknown:
            fail("Unregistered template branch: " + ", ".join(unknown))

    failures: list[str] = []
    for name in targets:
        try:
            validate_branch(name)
        except ValueError as exc:
            failures.append(str(exc))
            print(f"INVALID: {exc}", file=sys.stderr)
    if failures:
        raise SystemExit(1)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--branch",
        help="Exact template branch name. Defaults to every branch in registry/templates.yaml.",
    )
    parser.add_argument(
        "--no-fetch",
        action="store_true",
        help="Use local and remote-tracking refs without fetching origin.",
    )
    args = parser.parse_args()

    try:
        if not args.no_fetch:
            fetch_origin()
        validate_registered(args.branch)
    except ValueError as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
