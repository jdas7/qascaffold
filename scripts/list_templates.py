#!/usr/bin/env python3
"""List frameworks that already have a published template branch."""

from __future__ import annotations

import sys

from validate_template import load_registered_templates, origin_has_branch


def main() -> int:
    try:
        templates = load_registered_templates()
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    print(f"{'framework':<16} {'language':<12} {'type':<10} {'branch':<28} origin")
    for item in templates:
        present = "yes" if origin_has_branch(item["id"]) else "no"
        print(
            f"{item['framework']:<16} {item['language']:<12} {item['type']:<10} "
            f"{item['id']:<28} {present}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
